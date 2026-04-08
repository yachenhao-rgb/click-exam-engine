#!/bin/bash
#
# 智能出题引擎 Web版 - 启动脚本
#

echo "============================================"
echo "  智能出题引擎 Web版 启动中..."
echo "============================================"

# 检查Python版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $PYTHON_VERSION"

# 检查依赖
echo ""
echo "检查依赖..."
if ! pip3 show flask > /dev/null 2>&1; then
    echo "正在安装Flask..."
    pip3 install -r requirements.txt
fi

if ! pip3 show python-docx > /dev/null 2>&1; then
    echo "正在安装python-docx..."
    pip3 install python-docx
fi

echo "依赖检查完成"

# 创建必要目录
echo ""
echo "初始化目录结构..."
mkdir -p data
mkdir -p data/知识库数据
mkdir -p output
mkdir -p static/css
mkdir -p static/js
mkdir -p templates
echo "目录初始化完成"

# 检查数据库
if [ ! -f "data/knowledge_base.db" ]; then
    echo ""
    echo "首次运行，初始化数据库..."
    python3 -c "
from core.kb_manager import init_database
init_database('data/knowledge_base.db')
print('数据库初始化完成')
"
fi

# 启动应用
echo ""
echo "============================================"
echo "  启动服务..."
echo "  访问地址: http://localhost:5000"
echo "============================================"
echo ""

python3 app.py
