# 智能出题引擎 Web版 - 公网部署指南

> 本文档提供将智能出题引擎Web应用部署到公网的完整方案和详细步骤。

---

## 📋 目录

1. [项目概述](#1-项目概述)
2. [部署方案对比](#2-部署方案对比)
3. [方案A：Railway部署（推荐新手）](#3-方案arailway部署推荐新手)
4. [方案B：Render部署](#4-方案brender部署)
5. [方案C：阿里云ECS部署](#5-方案c阿里云ecs部署)
6. [必要配置文件准备](#6-必要配置文件准备)
7. [安全配置指南](#7-安全配置指南)
8. [域名与SSL配置](#8-域名与ssl配置)
9. [监控与运维](#9-监控与运维)
10. [成本估算汇总](#10-成本估算汇总)

---

## 1. 项目概述

### 1.1 技术栈
| 组件 | 技术 | 说明 |
|------|------|------|
| Web框架 | Flask 2.0+ | Python轻量级Web框架 |
| 数据库 | SQLite | 轻量级数据库，文件存储 |
| AI服务 | Deepseek API | 题目生成核心能力 |
| 前端 | HTML5 + CSS3 + JavaScript | 响应式设计 |

### 1.2 核心功能
- 📝 智能出题（选择题、填空题、判断题）
- 📊 CEFR难度分析
- 📄 文章生成与难度调整
- 📚 知识库管理
- 📥 文件导入（Word/Excel/PDF/TXT）

### 1.3 部署环境要求
- **Python版本**: 3.8+
- **内存**: 最低512MB，推荐1GB+
- **磁盘**: 最低1GB（包含SQLite数据库和上传文件）
- **网络**: 需要访问Deepseek API的外网访问能力

---

## 2. 部署方案对比

### 2.1 方案对比表

| 方案 | 平台 | 免费额度 | 付费起步 | 难度 | 性能 | 适用场景 |
|------|------|----------|----------|------|------|----------|
| **A** | Railway | $5/月额度 | $7/月 | ⭐ | ⭐⭐⭐⭐ | 快速上线，推荐新手 |
| **B** | Render | 750小时/月 | $7/月 | ⭐⭐ | ⭐⭐⭐⭐ | 长期项目，稳定性高 |
| **C** | 阿里云ECS | 无 | ¥60/月起 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 企业级，国内访问 |
| **D** | 腾讯云CVM | 无 | ¥65/月起 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 企业级，国内访问 |
| **E** | 飞书云空间 | 免费 | 免费 | ⭐ | ⭐⭐ | 轻量内网访问 |
| **F** | Coze国际版 | 免费 | 免费 | ⭐ | ⭐⭐⭐ | AI应用托管 |

### 2.2 方案推荐

#### 🏆 最佳推荐：Railway（方案A）

**优点：**
- ✅ 部署最简单，GitHub一键部署
- ✅ 每月$5免费额度（约350小时）
- ✅ 自动配置HTTPS
- ✅ 支持环境变量管理
- ✅ 欧洲/美国节点，速度较快

**缺点：**
- ❌ 国内访问速度一般
- ❌ 免费额度有限制

---

#### 🥈 次选推荐：阿里云ECS（方案C）

**优点：**
- ✅ 国内访问速度快
- ✅ 可绑定备案域名
- ✅ 完全控制服务器
- ✅ 可扩展性强

**缺点：**
- ❌ 需要备案（如需国内域名）
- ❌ 配置相对复杂
- ❌ 有最低月费

---

## 3. 方案A：Railway部署（推荐新手）

### 3.1 前期准备

#### 3.1.1 创建GitHub仓库

```bash
# 1. 在GitHub创建新仓库
# 仓库名称：smart-exam-engine
# 访问地址：https://github.com/你的用户名/smart-exam-engine

# 2. 将项目代码推送到仓库
cd 智能出题引擎Web
git init
git add .
git commit -m "Initial commit: 智能出题引擎Web"
git branch -M main
git remote add origin https://github.com/你的用户名/smart-exam-engine.git
git push -u origin main
```

#### 3.1.2 注册Railway账号

1. 访问 [https://railway.app](https://railway.app)
2. 使用GitHub账号登录
3. 完成邮箱验证

### 3.2 部署步骤

#### 3.2.1 创建新项目

```
1. 登录Railway控制台
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 授权GitHub访问权限
4. 选择 "smart-exam-engine" 仓库
5. Railway会自动检测Python项目
```

#### 3.2.2 配置环境变量

在Railway控制台 → 项目 → Variables中添加：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `SECRET_KEY` | `your-super-secret-key-here` | Flask密钥，生成随机字符串 |
| `DEEPSEEK_API_KEY` | `sk-xxxxxxxx` | Deepseek API密钥 |
| `USE_AI` | `true` | 启用AI生成 |
| `AI_PROVIDER` | `deepseek` | AI提供商 |
| `AI_MODEL` | `deepseek-chat` | 模型名称 |
| `API_BASE_URL` | `https://api.deepseek.com/v1` | API地址 |
| `FLASK_ENV` | `production` | 生产环境模式 |

**生成SECRET_KEY的方法：**
```python
import secrets
print(secrets.token_hex(32))
```

#### 3.2.3 配置启动命令

Railway会自动检测`Procfile`，确保项目根目录有`Procfile`文件：

```bash
# Procfile
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4
```

#### 3.2.4 等待部署完成

```
1. Railway会自动构建镜像
2. 完成后会显示访问URL：https://your-app-name.up.railway.app
3. 点击URL测试应用
```

### 3.3 自定义域名（可选）

```
1. 进入项目设置 → Domains
2. 添加自定义域名
3. 按提示配置DNS记录
4. Railway会自动申请SSL证书
```

### 3.4 Railway费用说明

| 套餐 | 价格 | 包含 |
|------|------|------|
| Starter | $5/月 | 500小时/月，1GB RAM，10GB存储 |
| Developer | $7/月 | 1000小时/月，2GB RAM，20GB存储 |
| Pro | 按量计费 | 灵活配置 |

> 💡 **提示**：Railway按使用时间计费，月末清零。月费套餐更划算。

---

## 4. 方案B：Render部署

### 4.1 前期准备

1. 注册 [Render账号](https://render.com)，推荐使用GitHub登录
2. 确保代码已推送到GitHub仓库

### 4.2 部署步骤

#### 4.2.1 创建Web Service

```
1. 登录Render控制台
2. 点击 "New +" → "Web Service"
3. 连接GitHub仓库
4. 选择 "smart-exam-engine" 仓库
```

#### 4.2.2 配置基础信息

| 配置项 | 值 |
|--------|-----|
| Name | smart-exam-engine |
| Region | Singapore（亚洲节点）或 United States |
| Branch | main |
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app -b 0.0.0.0:$PORT -w 2` |

#### 4.2.3 配置环境变量

在Environment选项卡中添加：

| 变量名 | 值 |
|--------|-----|
| `SECRET_KEY` | 随机密钥字符串 |
| `DEEPSEEK_API_KEY` | 你的API密钥 |
| `USE_AI` | true |
| `AI_PROVIDER` | deepseek |
| `AI_MODEL` | deepseek-chat |
| `API_BASE_URL` | https://api.deepseek.com/v1 |
| `FLASK_ENV` | production |

#### 4.2.4 选择套餐

| 套餐 | 价格 | 说明 |
|------|------|------|
| Free | 免费 | 睡眠后需唤醒，适合测试 |
| Starter | $7/月 | 永不睡眠，750MB RAM |
| Pro | $25/月 | 2.5GB RAM，自定义域名 |

### 4.3 费用说明

- **Free套餐**：750小时/月，但免费实例15分钟无活动会休眠
- **Starter套餐**：$7/月，适合个人项目
- **数据持久化**：免费套餐数据不持久化，建议使用付费套餐或对象存储

---

## 5. 方案C：阿里云ECS部署

### 5.1 前期准备

#### 5.1.1 购买服务器

1. 访问 [阿里云ECS](https://www.aliyun.com/product/ecs)
2. 选择配置：

| 配置项 | 推荐 |
|--------|------|
| 地域 | 华北2（北京）或华东1（杭州） |
| 实例规格 | ecs.s6-c1m2.small（1核2G） |
| 操作系统 | Ubuntu 22.04 LTS |
| 带宽 | 3Mbps（按固定带宽） |
| 存储 | 40GB SSD |

3. 设置root密码，记录登录信息

#### 5.1.2 域名准备（如需域名访问）

1. 在阿里云购买域名
2. 完成ICP备案（约2-3周）

### 5.2 服务器配置

#### 5.2.1 连接服务器

```bash
ssh root@你的服务器IP
```

#### 5.2.2 安装基础环境

```bash
# 更新系统
apt update && apt upgrade -y

# 安装Python环境
apt install -y python3 python3-pip python3-venv

# 安装Nginx
apt install -y nginx

# 安装Git
apt install -y git

# 安装Certbot（用于SSL证书）
apt install -y certbot python3-certbot-nginx
```

#### 5.2.3 创建应用用户

```bash
# 创建专门的应用用户
useradd -m -s /bin/bash examapp
usermod -aG sudo examapp

# 创建应用目录
mkdir -p /var/www/smart-exam-engine
chown examapp:examapp /var/www/smart-exam-engine
```

#### 5.2.4 部署应用代码

```bash
# 切换到应用用户
su - examapp

# 克隆代码（替换为你的仓库地址）
cd /var/www/smart-exam-engine
git clone https://github.com/你的用户名/smart-exam-engine.git .

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn
```

#### 5.2.5 配置环境变量

```bash
# 创建.env文件
cat > .env << EOF
SECRET_KEY=your-super-secret-key-here
DEEPSEEK_API_KEY=sk-xxxxxxxx
USE_AI=true
AI_PROVIDER=deepseek
AI_MODEL=deepseek-chat
API_BASE_URL=https://api.deepseek.com/v1
FLASK_ENV=production
EOF

# 设置文件权限
chmod 600 .env
```

#### 5.2.6 创建Systemd服务

```bash
# 创建服务文件
sudo cat > /etc/systemd/system/smart-exam.service << EOF
[Unit]
Description=Smart Exam Engine Web Application
After=network.target

[Service]
User=examapp
Group=examapp
WorkingDirectory=/var/www/smart-exam-engine
Environment="PATH=/var/www/smart-exam-engine/venv/bin"
EnvironmentFile=/var/www/smart-exam-engine/.env
ExecStart=/var/www/smart-exam-engine/venv/bin/gunicorn app:app -b 127.0.0.1:5000 --workers 2 --threads 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl start smart-exam
sudo systemctl enable smart-exam

# 检查服务状态
sudo systemctl status smart-exam
```

#### 5.2.7 配置Nginx反向代理

```bash
# 创建Nginx配置
sudo cat > /etc/nginx/sites-available/smart-exam << EOF
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名或IP

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # 超时设置
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }

    location /static {
        alias /var/www/smart-exam-engine/static;
        expires 30d;
    }
}
EOF

# 启用站点
sudo ln -s /etc/nginx/sites-available/smart-exam /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # 删除默认配置

# 测试并重启Nginx
sudo nginx -t
sudo systemctl restart nginx
```

#### 5.2.8 配置SSL证书（Let's Encrypt免费）

```bash
# 申请SSL证书（需要域名）
sudo certbot --nginx -d your-domain.com

# 自动续期设置
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# 测试续期
sudo certbot renew --dry-run
```

### 5.3 防火墙配置

```bash
# 配置防火墙
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 5.4 阿里云费用说明

| 配置项 | 月费用 |
|--------|--------|
| ECS实例（1核2G） | ¥60-80 |
| 公网带宽（3Mbps） | ¥20-30 |
| 云盘（40GB SSD） | ¥5-10 |
| **合计** | **¥85-120/月** |

---

## 6. 必要配置文件准备

### 6.1 目录结构

```
smart-exam-engine/
├── app.py                    # Flask应用入口
├── requirements.txt         # Python依赖
├── Procfile                  # 部署平台启动命令
├── Dockerfile                # Docker镜像配置
├── .env.example              # 环境变量示例
├── .gitignore               # Git忽略文件
├── data/                     # 数据目录（SQLite数据库）
│   ├── knowledge_base.db    # SQLite数据库
│   └── 知识库数据/           # 知识库文件
├── output/                   # 导出文件目录
├── core/                     # 核心模块
├── static/                   # 静态文件
└── templates/                # HTML模板
```

### 6.2 requirements.txt（已有，供参考）

```txt
# 智能出题引擎 Web版 - 依赖包

# Web框架
Flask>=2.0.0

# 文档处理
python-docx>=0.8.11
openpyxl>=3.0.0

# 文件上传与文本提取
Pillow>=9.0.0
pdfplumber>=0.10.0
PyPDF2>=3.0.0

# AI服务
requests>=2.28.0

# 生产服务器
gunicorn>=20.0.0

# 环境变量
python-dotenv>=0.19.0
```

### 6.3 Procfile（新建）

```bash
# Railway/Render启动命令
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4
```

### 6.4 Dockerfile（新建）

```dockerfile
# 智能出题引擎 Web版 - Docker配置
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 复制应用代码
COPY . .

# 创建必要目录
RUN mkdir -p data data/知识库数据 output

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2"]
```

### 6.5 .env.example（新建）

```bash
# ============================================
# 智能出题引擎 - 环境变量配置示例
# ============================================
# 复制此文件为 .env 并填写实际值

# Flask密钥（必须）- 生成方法：python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-super-secret-key-here

# Deepseek API密钥（必须）- 从 https://platform.deepseek.com 获取
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# AI功能开关
USE_AI=true

# AI提供商配置
AI_PROVIDER=deepseek
AI_MODEL=deepseek-chat
API_BASE_URL=https://api.deepseek.com/v1
AI_TEMPERATURE=0.7

# Flask环境
FLASK_ENV=production
```

### 6.6 .gitignore（新建）

```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/

# 环境变量
.env

# 数据库
*.db
data/*.db

# 缓存
*.json
!.article_cache.json.example

# 日志
*.log

# 操作系统
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# 上传和输出文件
output/*
!output/.gitkeep
data/知识库数据/*
!data/知识库数据/.gitkeep
data/backups/*
!data/backups/.gitkeep

# Docker
.docker/

# 临时文件
*.tmp
*.temp
```

---

## 7. 安全配置指南

### 7.1 环境变量安全

#### ✅ 必须配置

```bash
# 1. 使用强密钥
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# 2. API密钥绝不硬编码
# ❌ 错误：将密钥直接写在代码中
# ✅ 正确：使用环境变量

# 3. 生产环境禁止调试
FLASK_ENV=production
FLASK_DEBUG=0
```

#### ✅ 密钥轮换

```bash
# 定期更换API密钥
# 1. 在Deepseek平台生成新密钥
# 2. 更新所有部署环境
# 3. 验证新密钥可用
# 4. 旧密钥保留24小时后再删除
```

### 7.2 文件权限

```bash
# Linux服务器权限设置
chmod 700 .env           # 仅所有者可读写
chmod 755 data/          # 目录权限
chmod 644 data/*.db      # 数据库文件只读
chmod 755 output/        # 导出目录
```

### 7.3 数据库安全

```python
# app.py 中添加数据库路径检查
import os

# 确保使用绝对路径
DB_PATH = os.environ.get('DB_PATH', '/var/www/smart-exam-engine/data/knowledge_base.db')
```

### 7.4 上传文件安全

```python
# app.py 中添加文件验证
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 限制文件大小（已在原代码中配置）
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### 7.5 HTTPS强制跳转

```nginx
# Nginx配置中添加HTTPS强制跳转
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### 7.6 安全检查清单

| 检查项 | 状态 | 说明 |
|--------|------|------|
| SECRET_KEY已设置 | ☐ | 使用随机生成的32位以上字符串 |
| DEEPSEEK_API_KEY已配置 | ☐ | 从环境变量读取，不硬编码 |
| HTTPS已启用 | ☐ | 使用有效SSL证书 |
| 文件上传已限制 | ☐ | 限制文件类型和大小 |
| 目录权限已设置 | ☐ | .env文件权限600 |
| 防火墙已配置 | ☐ | 仅开放必要端口 |
| 调试模式已关闭 | ☐ | FLASK_ENV=production |
| 日志已配置 | ☐ | 监控异常访问 |

---

## 8. 域名与SSL配置

### 8.1 域名购买建议

| 平台 | 价格 | 特点 |
|------|------|------|
| 阿里云 | ¥20-50/年 | 国内，稳定，备案方便 |
| 腾讯云 | ¥20-50/年 | 国内，稳定，备案方便 |
| Namecheap | $10-20/年 | 国际，支持隐私保护 |
| Cloudflare Registrar | $8-10/年 | 价格低，附加服务多 |

### 8.2 ICP备案流程（国内必须）

#### 备案要求
- 服务器位于中国大陆
- 使用国内域名
- 个人/企业主体均可备案

#### 备案流程（约2-3周）

```
1. 购买域名和服务器
   ↓
2. 在服务商备案系统提交申请
   - 个人：身份证、域名证书、核验单
   - 企业：营业执照、法人身份证、域名证书、核验单
   ↓
3. 服务商初审（1-3天）
   ↓
4. 管局审核（7-20天）
   ↓
5. 备案成功，获得备案号
```

#### 备案平台

| 服务商 | 备案入口 |
|--------|----------|
| 阿里云 | https://beian.aliyun.com |
| 腾讯云 | https://console.cloud.tencent.com/beian |
| 华为云 | https://console.huaweicloud.com/beian |

### 8.3 SSL证书配置

#### Let's Encrypt免费证书

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 申请证书（需要域名已解析）
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

#### 证书有效期
- Let's Encrypt证书有效期：**90天**
- Certbot自动续期：每12小时检查，每天凌晨续期

### 8.4 DNS配置

| 记录类型 | 主机记录 | 记录值 | 说明 |
|----------|----------|--------|------|
| A | @ | 服务器IP | 主域名 |
| A | www | 服务器IP | WWW子域名 |
| CNAME | @ | your-app.railway.app | Railway平台 |
| CNAME | @ | your-app.onrender.com | Render平台 |

---

## 9. 监控与运维

### 9.1 日志收集

#### 应用日志（Python）

```python
# app.py 中添加日志配置
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    # 文件日志
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/app.log', maxBytes=10240000, backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Smart Exam Engine startup')
```

#### Nginx日志

```nginx
# /etc/nginx/nginx.conf
access_log /var/log/nginx/access.log;
error_log /var/log/nginx/error.log;
```

### 9.2 错误监控

#### Sentry错误追踪（推荐）

```bash
# 安装sentry-sdk
pip install sentry-sdk[flask]

# app.py 中集成
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="你的Sentry DSN地址",
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1
)
```

### 9.3 性能监控

#### 服务健康检查

```bash
# 创建健康检查脚本 health_check.sh
#!/bin/bash
response=$(curl -f -s -o /dev/null -w "%{http_code}" http://localhost:5000/)
if [ "$response" -ne 200 ]; then
    echo "Service unhealthy, response code: $response"
    exit 1
fi
echo "Service healthy"
exit 0

# 添加Cron任务：每5分钟检查一次
echo "*/5 * * * * /var/www/smart-exam-engine/health_check.sh" | sudo tee /etc/cron.d/health-check
```

### 9.4 备份策略

#### 自动备份脚本

```bash
#!/bin/bash
# backup.sh - 数据库自动备份脚本

BACKUP_DIR="/var/www/smart-exam-engine/data/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_FILE="/var/www/smart-exam-engine/data/knowledge_base.db"

# 创建备份
mkdir -p $BACKUP_DIR
cp $DB_FILE "$BACKUP_DIR/knowledge_base_$DATE.db"

# 压缩备份
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" \
    -C /var/www/smart-exam-engine data/

# 删除7天前的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.db" -mtime +7 -delete

echo "Backup completed: backup_$DATE.tar.gz"
```

#### Cron定时任务

```bash
# 添加每日凌晨2点备份
echo "0 2 * * * examapp /var/www/smart-exam-engine/backup.sh >> /var/log/backup.log 2>&1" | sudo tee /etc/cron.d/daily-backup
```

### 9.5 自动重启

```bash
# Systemd服务自动重启
# 已在5.2.6节的smart-exam.service中配置
Restart=always
RestartSec=5
```

---

## 10. 成本估算汇总

### 10.1 月度成本对比

| 方案 | 平台 | 最低成本 | 适用场景 |
|------|------|----------|----------|
| **Railway** | PaaS | $0-5/月 | 个人项目/学习/测试 |
| **Render** | PaaS | $0-7/月 | 个人项目/长期项目 |
| **阿里云ECS** | IaaS | ¥85-120/月 | 企业/国内访问 |
| **腾讯云CVM** | IaaS | ¥80-110/月 | 企业/国内访问 |
| **AWS EC2** | IaaS | $10-20/月 | 企业/全球访问 |
| **Vultr** | IaaS | $6-10/月 | 开发者/全球访问 |
| **DigitalOcean** | IaaS | $6-24/月 | 开发者/全球访问 |

### 10.2 各方案详细成本

#### Railway

| 套餐 | 月费 | vCPU | RAM | 存储 | 流量 |
|------|------|------|-----|------|------|
| Starter | $5 | 共享 | 1GB | 10GB | 按量 |
| Developer | $7 | 共享 | 2GB | 20GB | 按量 |
| Pro | $20+ | 2 | 4GB | 100GB | 按量 |

#### Render

| 套餐 | 月费 | RAM | 存储 | 说明 |
|------|------|-----|------|------|
| Free | $0 | 512MB | 共享 | 会休眠 |
| Starter | $7 | 512MB | 共享 | 永不休眠 |
| Pro | $25 | 2.5GB | 专用 | 高性能 |

#### 阿里云ECS（国内）

| 配置 | 月费 | 说明 |
|------|------|------|
| 1核2G基础款 | ¥60 |ecs.s6-c1m2.small |
| 2核4G标准款 | ¥120 | ecs.s6-c2m2 |
| 流量费 | ¥0.5-1/GB | 按实际使用 |

### 10.3 免费额度汇总

| 平台 | 免费额度 | 有效期 |
|------|----------|--------|
| Railway | $5/月 | 永久 |
| Render | 750小时/月 | 永久 |
| GitHub Codespaces | 120核心小时/月 | 永久 |
| Vercel | 无限制（100GB带宽） | 永久 |
| Netlify | 100GB带宽/月 | 永久 |
| 阿里云学生机 | ¥9.5/月 | 在校期间 |

### 10.4 升级建议

#### 初期（个人使用）
- 推荐：**Railway Starter** ($5/月) 或 **Render Free**
- 预期流量：100-500次/天

#### 成长期（小团队）
- 推荐：**Railway Developer** ($7/月) 或 **Render Starter** ($7/月)
- 预期流量：500-2000次/天

#### 成熟期（正式产品）
- 推荐：**阿里云ECS** (¥100+/月) 或 **Railway Pro** ($20+/月)
- 预期流量：2000+/天，需要数据库持久化和更高稳定性

---

## 附录A：快速部署清单

### 部署前检查

- [ ] 代码已推送到GitHub仓库
- [ ] `requirements.txt` 已包含所有依赖
- [ ] `SECRET_KEY` 已生成并准备
- [ ] `DEEPSEEK_API_KEY` 已获取
- [ ] 本地测试通过

### Railway部署检查

- [ ] GitHub仓库已连接
- [ ] 所有环境变量已配置
- [ ] `Procfile` 已创建
- [ ] 部署成功，可访问

### 阿里云部署检查

- [ ] 服务器已购买并连接
- [ ] Python环境已安装
- [ ] Nginx已配置
- [ ] Gunicorn服务已启动
- [ ] SSL证书已申请
- [ ] 防火墙已配置
- [ ] 域名已解析

### 上线后检查

- [ ] 应用可正常访问
- [ ] API调用正常（出题功能）
- [ ] 文件上传正常
- [ ] HTTPS已启用
- [ ] 错误日志无异常

---

## 附录B：常见问题

### Q1: Railway部署失败怎么办？

```
1. 检查Build日志
2. 确认requirements.txt格式正确
3. 确认Python版本（推荐3.11）
4. 查看环境变量是否遗漏
5. 尝试手动Deploy
```

### Q2: Deepseek API调用失败？

```
1. 检查API密钥是否正确
2. 确认API余额充足
3. 检查网络连接
4. 查看应用日志获取详细错误
```

### Q3: SQLite数据库无法写入？

```
1. 检查文件权限
2. 确认目录存在
3. 检查磁盘空间
4. 考虑迁移到云数据库
```

### Q4: 如何迁移到正式服务器？

```
1. 备份数据库：sqlite3 data/knowledge_base.db ".backup backup.db"
2. 导出知识库文件
3. 在新服务器克隆代码
4. 恢复数据库和文件
5. 更新环境变量
```

---

## 附录C：相关资源

### 官方文档
- [Flask部署指南](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Gunicorn文档](https://docs.gunicorn.org/)
- [Railway文档](https://docs.railway.app/)
- [Render部署文档](https://render.com/docs/deploy-flask)

### Deepseek API
- [官方平台](https://platform.deepseek.com/)
- [API文档](https://platform.deepseek.com/docs)

---

> 📝 文档版本：v1.0  
> 📅 更新日期：2025年  
> 💡 如有问题，请检查GitHub仓库的Issues页面
