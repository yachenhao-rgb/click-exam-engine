# ============================================
# 智能出题引擎 Web版 - Docker配置
# ============================================
# 使用方法:
#   构建: docker build -t smart-exam-engine .
#   运行: docker run -d -p 5000:5000 --env-file .env smart-exam-engine

FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# 安装系统依赖（用于Pillow等库）
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装生产服务器
RUN pip install --no-cache-dir gunicorn

# 复制应用代码
COPY . .

# 创建必要目录
RUN mkdir -p data/data data/知识库数据 output logs backups

# 设置目录权限
RUN chmod -R 755 data/ output/ logs/ backups/

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4"]
