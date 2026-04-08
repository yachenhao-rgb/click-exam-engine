# CLICK 智能出题引擎

基于中考真题基因的智能出题系统，支持多种题型一键生成。

## 功能特性

### 🎯 核心出题
- 完形填空（符合河北中考规律）
- 阅读理解
- 语法填空
- 判断题
- 开放问答
- 词汇匹配

### 🔧 轻量化工具（12个）
- 讨论问题生成器
- 词汇造句
- 核心词汇提取
- 对话生成器
- 利弊分析
- 名人名言
- 作文题目
- 趣味知识
- 标题选择
- 创意写作
- 找不同
- 改错题

### 📤 导出功能
- Word文档导出
- PDF导出
- 一键复制
- 打印友好

## 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置环境变量
export DEEPSEEK_API_KEY="你的API密钥"
export SECRET_KEY="随机密钥"

# 3. 运行
python app.py
```

访问 http://localhost:5000

## Railway 部署

### 方式一：连接GitHub（推荐）

1. Fork或Clone本仓库到你的GitHub
2. 访问 https://railway.app
3. 用GitHub登录
4. New Project → Deploy from GitHub repo
5. 选择此仓库
6. 添加环境变量：
   - `SECRET_KEY` = 随机32位字符串
   - `DEEPSEEK_API_KEY` = 你的Deepseek API密钥
7. 等待部署完成，获得公网地址

### 方式二：Railway CLI

```bash
# 安装CLI
npm i -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 添加环境变量
railway variables set SECRET_KEY=随机密钥
railway variables set DEEPSEEK_API_KEY=你的密钥

# 部署
railway up
```

## 环境变量

| 变量名 | 说明 | 必填 |
|--------|------|------|
| SECRET_KEY | Flask密钥（32位随机字符串） | ✅ |
| DEEPSEEK_API_KEY | Deepseek API密钥 | ✅ |

## 技术栈

- **后端**: Flask + SQLite
- **前端**: Bootstrap 5 + Vanilla JS
- **AI**: Deepseek API
- **导出**: python-docx + reportlab

## License

MIT
