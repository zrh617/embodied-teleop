@echo off
REM VR视频流集成快速启动脚本
REM 作用：在一个命令中设置并启动所有必要的服务

setlocal enabledelayedexpansion

echo.
echo ========================================
echo  VR视频流服务快速启动
echo ========================================
echo.

REM 配置参数
set PROJECT_DIR=d:\XRTeleoperation2
set PYTHON_VENV=%PROJECT_DIR%\venv
set SERVER_PORT=8000
set SERVER_IP=0.0.0.0

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python未安装或未在PATH中
    echo 请从 https://www.python.org 安装Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 检查Python版本...
python --version
echo.

REM 创建虚拟环境（如果不存在）
if not exist "%PYTHON_VENV%" (
    echo [2/4] 创建虚拟环境...
    python -m venv "%PYTHON_VENV%"
    if errorlevel 1 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo 虚拟环境已创建: %PYTHON_VENV%
    echo.
) else (
    echo [2/4] 虚拟环境已存在
    echo.
)

REM 激活虚拟环境
echo [3/4] 激活虚拟环境并安装依赖...
call "%PYTHON_VENV%\Scripts\activate.bat"

REM 安装依赖
echo 安装依赖包...
pip install -q fastapi uvicorn opencv-python numpy pyrealsense2 okhttp3

if errorlevel 1 (
    echo [警告] 部分依赖安装失败，但尝试继续...
    REM 不中断，继续执行
)

REM 检查RealSense SDK
echo.
echo [4/4] 检查RealSense库...
python -c "import pyrealsense2; print('[成功] pyrealsense2已安装')" >nul 2>&1
if errorlevel 1 (
    echo [警告] pyrealsense2模块未找到
    echo 请安装RealSense SDK:
    echo   Windows: https://github.com/IntelRealSense/librealsense/releases
    echo   Linux: sudo apt install librealsense2-dev python3-pyrealsense2
)

REM 获取本机IP
echo.
echo ========================================
echo  网络配置
echo ========================================
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R "IPv4 Address"') do (
    set IP=%%a
    set IP=!IP:~1!
)
echo 本机IP: %IP%
echo 服务监听: http://0.0.0.0:%SERVER_PORT%
echo.
echo [重要] 在VR应用中使用以下URL:
echo   http://%IP%:%SERVER_PORT%/stream/color
echo   http://%IP%:%SERVER_PORT%/stream/depth
echo.

REM 检查防火墙
echo 检查端口 %SERVER_PORT% 是否开放...
netstat -an | findstr :%SERVER_PORT% >nul
if errorlevel 1 (
    echo [提示] 端口%SERVER_PORT%未被占用
) else (
    echo [警告] 端口%SERVER_PORT%已被占用，可能导致启动失败
)

REM 启动服务器
echo.
echo ========================================
echo  启动视频服务器
echo ========================================
echo.
echo 服务器启动中... （按 Ctrl+C 停止）
echo.

cd /d "%PROJECT_DIR%"
python video_server.py

REM 清理
endlocal
