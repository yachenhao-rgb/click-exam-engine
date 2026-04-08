# ============================================
# 智能出题引擎 Web版 - 部署平台启动命令
# ============================================
# 
# 【Railway / Render 部署】
# 这两个平台会自动识别Procfile
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120

# 【Fly.io 部署】
# 如果使用Fly.io，取消下面这行的注释
# web: gunicorn app:app --bind 0.0.0.0:8080 --workers 2 --threads 4 --timeout 120

# 【Heroku 部署】
# 如果使用Heroku，取消下面这行的注释
# web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
