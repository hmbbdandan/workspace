# Windows Agent 使用说明

## 功能
- 定时从GitHub拉取命令
- 执行命令并记录结果
- 自动安装Python（如果未安装）
- 支持截图和日志回传

## 使用方法

### 方法1：直接下载运行（推荐）
1. 在Windows上用浏览器打开 GitHub 仓库
2. 点击 `agent.py` 文件
3. 点击 "Raw" 查看内容
4. 另存为 `agent.py`
5. 双击运行（或在CMD中运行 `python agent.py`）

### 方法2：使用启动脚本
1. 下载并运行 `setup.bat`
2. 脚本会自动安装Python（如果需要）
3. 自动启动Agent

## 首次设置
1. 确保Windows已联网
2. 确保已安装Git（如果没有，脚本会自动提示）
3. 首次运行可能需要几分钟安装依赖

## 查看状态
- 日志文件：`agent.log`
- 命令输出：`results/` 目录
- 截图：`screenshots/` 目录

## 常见问题
Q: 提示"不是内部或外部命令"
A: 确保Python已正确安装并添加到PATH

Q: Git连接失败
A: 检查网络连接，或配置Git代理
