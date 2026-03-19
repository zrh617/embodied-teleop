#!/bin/bash
# VR视频流集成快速启动脚本 (Linux/Mac)
# 作用：在一个命令中设置并启动所有必要的服务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置参数
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_VENV="$PROJECT_DIR/venv"
SERVER_PORT=8000
SERVER_IP=0.0.0.0

echo ""
echo "========================================"
echo "  VR视频流服务快速启动"
echo "========================================"
echo ""

# 检查Python是否已安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[错误] Python 3未安装${NC}"
    echo "请安装Python 3.8+:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3.8 python3-venv"
    echo "  Fedora: sudo dnf install python3"
    exit 1
fi

echo "[1/4] 检查Python版本..."
python3 --version
echo ""

# 创建虚拟环境（如果不存在）
if [ ! -d "$PYTHON_VENV" ]; then
    echo "[2/4] 创建虚拟环境..."
    python3 -m venv "$PYTHON_VENV"
    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] 虚拟环境创建失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}虚拟环境已创建: $PYTHON_VENV${NC}"
    echo ""
else
    echo "[2/4] 虚拟环境已存在"
    echo ""
fi

# 激活虚拟环境
echo "[3/4] 激活虚拟环境并安装依赖..."
source "$PYTHON_VENV/bin/activate"

# 升级pip
pip install --quiet --upgrade pip setuptools wheel

# 安装依赖
echo "安装依赖包..."
pip install --quiet fastapi uvicorn opencv-python numpy

# 尝试安装pyrealsense2（可能在某些平台上失败）
echo "安装RealSense SDK..."
if pip install --quiet pyrealsense2; then
    echo -e "${GREEN}[成功] pyrealsense2已安装${NC}"
else
    echo -e "${YELLOW}[警告] pyrealsense2安装可能失败${NC}"
    echo "如果之后出现问题，请手动安装:"
    echo "  https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python"
fi

# 检查RealSense SDK
echo ""
echo "[4/4] 检查RealSense库..."
if python3 -c "import pyrealsense2" 2>/dev/null; then
    echo -e "${GREEN}[成功] pyrealsense2已安装${NC}"
else
    echo -e "${YELLOW}[警告] pyrealsense2模块未找到${NC}"
    echo "请安装Intel RealSense SDK:"
    echo "  macOS: brew install librealsense"
    echo "  Ubuntu: sudo apt install librealsense2-dev python3-pyrealsense2"
    echo "  From source: https://github.com/IntelRealSense/librealsense"
fi

# 获取本机IP
echo ""
echo "========================================"
echo "  网络配置"
echo "========================================"

# macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
# Linux
elif [[ "$OSTYPE" == "linux"* ]]; then
    LOCAL_IP=$(hostname -I | awk '{print $1}')
else
    LOCAL_IP="<YOUR_IP>"
fi

echo "本机IP: $LOCAL_IP"
echo "服务监听: http://0.0.0.0:$SERVER_PORT"
echo ""
echo -e "${GREEN}[重要] 在VR应用中使用以下URL:${NC}"
echo "  http://$LOCAL_IP:$SERVER_PORT/stream/color"
echo "  http://$LOCAL_IP:$SERVER_PORT/stream/depth"
echo ""

# 检查防火墙（仅Linux）
if [[ "$OSTYPE" == "linux"* ]]; then
    echo "检查端口 $SERVER_PORT 是否开放..."
    if command -v ufw &> /dev/null; then
        if ! sudo ufw status | grep -q "$SERVER_PORT"; then
            echo -e "${YELLOW}[提示] 建议打开防火墙端口:${NC}"
            echo "  sudo ufw allow $SERVER_PORT"
        fi
    fi
fi

# 检查端口占用
echo "检查端口占用..."
if lsof -i :$SERVER_PORT &>/dev/null || netstat -tuln 2>/dev/null | grep -q ":$SERVER_PORT "; then
    echo -e "${YELLOW}[警告] 端口$SERVER_PORT已被占用${NC}"
else
    echo -e "${GREEN}端口$SERVER_PORT可用${NC}"
fi

# 启动服务器
echo ""
echo "========================================"
echo "  启动视频服务器"
echo "========================================"
echo ""
echo "服务器启动中... (按 Ctrl+C 停止)"
echo ""

cd "$PROJECT_DIR"
python3 video_server.py

# 清理（如果需要）
# deactivate
