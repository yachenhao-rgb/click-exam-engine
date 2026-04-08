# ============================================
# 智能出题引擎 Web版 - Docker配置
# Railway部署优化版
# ============================================

FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# 复制应用代码
COPY . .

# 创建必要目录
RUN mkdir -p data data/知识库数据 output logs backups && \
    chmod -R 755 data/ output/ logs/ backups/

# 暴露端口
EXPOSE 5000

# 启动命令
CMD gunicorn app:app --bind 0.0.0.0:5000 --workers 1 --threads 2 --timeout 120
