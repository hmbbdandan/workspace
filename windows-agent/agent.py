#!/usr/bin/env python3
"""
Windows Agent - 通过GitHub轮询执行命令
配合Mac上的主控端使用

用法: python agent.py
"""

import os
import sys
import time
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# 配置
REPO_RAW_URL = "https://raw.githubusercontent.com/YuTan9/workspace/main/windows-agent"
REPO_API_URL = "https://api.github.com/repos/YuTan9/workspace/contents/windows-agent"
GIT_EMAIL = "agent@windows.local"
GIT_NAME = "Windows-Agent"

# Windows特定路径
TEMP_DIR = Path(os.environ.get('TEMP', 'C:/Temp'))
AGENT_DIR = Path(__file__).parent.absolute()
RESULTS_DIR = AGENT_DIR / "results"
SCREENSHOTS_DIR = AGENT_DIR / "screenshots"
LOG_FILE = AGENT_DIR / "agent.log"

# 轮询间隔（秒）
POLL_INTERVAL = 30

def log(msg):
    """写日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def run_cmd(cmd, timeout=60):
    """执行命令，返回(output, returncode)"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "Command timed out", -1
    except Exception as e:
        return str(e), -1

def check_python():
    """检查Python是否安装"""
    try:
        version = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True
        ).stdout.strip()
        log(f"Python已安装: {version}")
        return True
    except:
        log("Python未安装，尝试安装...")
        return install_python()

def install_python():
    """安装Python"""
    log("请手动安装Python: https://www.python.org/downloads/")
    log("或在Windows Store搜索'Python'")
    
    # 尝试通过winget安装
    result, code = run_cmd("winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements")
    if code == 0:
        log("Python安装成功")
        return True
    return False

def check_git():
    """检查Git是否安装"""
    _, code = run_cmd("git --version")
    if code == 0:
        log("Git已安装")
        return True
    log("Git未安装")
    return False

def git_pull():
    """从Git拉取最新命令"""
    try:
        # 确保在正确目录
        os.chdir(AGENT_DIR)
        
        # 初始化git如果需要
        if not (AGENT_DIR / ".git").exists():
            log("初始化Git仓库...")
            run_cmd(f'git init')
            run_cmd(f'git remote add origin https://github.com/YuTan9/workspace.git')
        
        # 拉取
        run_cmd('git fetch origin main')
        run_cmd('git reset --hard origin/main')
        return True
    except Exception as e:
        log(f"Git pull失败: {e}")
        return False

def git_push(message):
    """推送结果到Git"""
    try:
        os.chdir(AGENT_DIR)
        run_cmd('git add -A')
        result, _ = run_cmd(f'git commit -m "{message}"')
        run_cmd('git push origin main --force')
        return True
    except Exception as e:
        log(f"Git push失败: {e}")
        return False

def get_pending_commands():
    """获取待执行的命令列表"""
    commands_dir = AGENT_DIR / "commands"
    if not commands_dir.exists():
        return []
    
    pending = []
    for f in sorted(commands_dir.glob("*.json")):
        if f.stem.startswith("done_"):
            continue
        pending.append(f)
    return pending

def execute_command(cmd_file):
    """执行单个命令"""
    log(f"执行命令: {cmd_file.name}")
    
    try:
        with open(cmd_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        command = data.get("command", "")
        cmd_id = data.get("id", cmd_file.stem)
        
        # 执行命令
        start_time = time.time()
        output, returncode = run_cmd(command, timeout=300)
        elapsed = time.time() - start_time
        
        # 保存结果
        result = {
            "id": cmd_id,
            "command": command,
            "returncode": returncode,
            "output": output,
            "elapsed": elapsed,
            "timestamp": datetime.now().isoformat(),
            "hostname": os.environ.get("COMPUTERNAME", "UNKNOWN")
        }
        
        result_file = RESULTS_DIR / f"{cmd_id}.json"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # 标记命令完成
        done_file = cmd_file.parent / f"done_{cmd_file.name}"
        cmd_file.rename(done_file)
        
        log(f"命令完成: {cmd_id}, 耗时: {elapsed:.1f}秒")
        return True
        
    except Exception as e:
        log(f"命令执行失败: {e}")
        return False

def take_screenshot():
    """截图"""
    try:
        # 使用PowerShell的截图功能
        import random
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = SCREENSHOTS_DIR / filename
        
        # PowerShell截图
        script = f'''
Add-Type -AssemblyName System.Windows.Forms
$screenshot = [System.Windows.Forms.Screen]::PrimaryScreen
$bitmap = New-Object System.Drawing.Bitmap($screenshot.Bounds.Width, $screenshot.Bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screenshot.Bounds.Location, [System.Drawing.Point]::Empty, $screenshot.Bounds.Size)
$bitmap.Save("{filepath}")
$graphics.Dispose()
$bitmap.Dispose()
'''
        run_cmd(f'powershell -Command "{script}"')
        
        if filepath.exists():
            log(f"截图保存: {filename}")
            return True
    except Exception as e:
        log(f"截图失败: {e}")
    return False

def system_info():
    """收集系统信息"""
    info = {}
    
    # 计算机名
    info["hostname"] = os.environ.get("COMPUTERNAME", "UNKNOWN")
    
    # 用户名
    info["username"] = os.environ.get("USERNAME", "UNKNOWN")
    
    # Python版本
    result, _ = run_cmd("python --version")
    info["python_version"] = result.strip()
    
    # Git版本
    result, _ = run_cmd("git --version")
    info["git_version"] = result.strip()
    
    # IP地址
    result, _ = run_cmd('ipconfig | findstr /i "IPv4"')
    info["ip"] = result.strip()
    
    # 磁盘空间
    result, _ = run_cmd('wmic logicaldisk get caption,freespace,size')
    info["disks"] = result.strip()
    
    return info

def main():
    log("=" * 50)
    log("Windows Agent 启动")
    log("=" * 50)
    
    # 创建必要目录
    RESULTS_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    (AGENT_DIR / "commands").mkdir(exist_ok=True)
    
    # 检查依赖
    log("检查环境...")
    check_python()
    check_git()
    
    # 发送系统信息
    log("收集系统信息...")
    info = system_info()
    info_file = RESULTS_DIR / "system_info.json"
    with open(info_file, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    log(f"系统: {info.get('hostname')}, Python: {info.get('python_version')}")
    
    # 尝试推送初始状态
    git_push("Agent启动")
    
    log(f"开始轮询，间隔{POLL_INTERVAL}秒...")
    log("按Ctrl+C停止")
    
    while True:
        try:
            # 拉取最新命令
            git_pull()
            
            # 获取待执行命令
            pending = get_pending_commands()
            if pending:
                log(f"发现{len(pending)}个待执行命令")
                for cmd_file in pending:
                    execute_command(cmd_file)
                # 推送结果
                git_push("命令执行结果")
            else:
                log("暂无新命令")
            
            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            log("收到停止信号，退出")
            break
        except Exception as e:
            log(f"轮询出错: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
