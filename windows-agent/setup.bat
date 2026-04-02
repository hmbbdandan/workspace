@echo off
echo ========================================
echo Windows Agent 安装脚本
echo ========================================
echo.

:: 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python未安装，正在尝试安装...
    echo 请稍候...
    
    :: 尝试通过Windows Store安装
    start ms-windows-store://search/python
    
    echo.
    echo 如果没有自动打开，请手动在Windows Store搜索"Python 3.11"
    echo 安装完成后，请重新运行此脚本
    pause
    exit /b
)

echo Python已安装
echo.

:: 检查Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git未安装，正在提示...
    echo.
    echo 请手动安装Git: https://git-scm.com/download/win
    echo 或使用Chocolatey: choco install git -y
    pause
    exit /b
)

echo Git已安装
echo.

:: 克隆仓库
echo 请在下方输入仓库URL（或直接下载agent.py）
echo.
echo 仓库地址: https://github.com/YuTan9/workspace
echo.
set /p repo_url="请输入仓库URL（直接回车跳过）: "

if not "%repo_url%"=="" (
    echo 克隆仓库...
    git clone %repo_url%
    cd windows-agent
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 运行方式:
echo   python agent.py
echo.
echo 按任意键退出...
pause >nul
