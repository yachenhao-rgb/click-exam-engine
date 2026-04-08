@echo off
chcp 65001 > nul
echo ============================================
echo   智能出题引擎 Web版 启动中...
echo ============================================

REM 检查Python
python --version > nul 2>&1
if errorlevel 1 (
    echo 错误: 未检测到Python，请先安装Python 3.x
    pause
    exit /b 1
)

echo.
echo 检查依赖...
pip install -r requirements.txt

echo.
echo 初始化目录结构...
if not exist "data" mkdir "data"
if not exist "data\知识库数据" mkdir "data\知识库数据"
if not exist "output" mkdir "output"

REM 检查数据库
if not exist "data\knowledge_base.db" (
    echo.
    echo 首次运行，初始化数据库...
    python -c "from core.kb_manager import init_database; init_database('data/knowledge_base.db'); print('数据库初始化完成')"
)

echo.
echo ============================================
echo   启动服务...
echo   访问地址: http://localhost:5000
echo ============================================
echo.

python app.py

pause
