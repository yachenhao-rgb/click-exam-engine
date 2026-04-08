# 智能出题引擎 - 导出增强功能说明

## 功能概述

本次更新为智能出题引擎添加了完整的导出增强功能，包括PDF导出、打印友好格式和一键复制功能。

## 新增功能

### 1. PDF导出
- **路由**: `/api/export/pdf/<task_id>`
- **功能**: 将生成的题目导出为高质量PDF文件
- **特点**:
  - 支持所有题型：完形填空、阅读理解、判断题、开放问答、词汇匹配
  - 可配置是否包含答案（`?include_answers=true/false`）
  - 排版美观，适合打印
  - 答案单独一页

### 2. 打印友好格式
- **触发方式**: 点击"打印"按钮
- **功能**: 打开打印预览窗口
- **CSS特性** (`@media print`):
  - 隐藏导航栏、按钮等非必要元素
  - 优化字体大小（12pt）和间距
  - 题目项 `page-break-inside: avoid` 避免分页断裂
  - 答案区域 `page-break-before: always` 独立成页

### 3. 一键复制到剪贴板
- **复制题目**: `/api/export/html/<task_id>`
  - 复制纯文本格式题目
  - 支持主流浏览器
  - 备用方法处理不支持 `navigator.clipboard` 的情况
  
- **复制答案**: `/api/export/answers/<task_id>`
  - 复制参考答案和解析

## 新增API接口

| 路由 | 方法 | 功能 |
|------|------|------|
| `/api/export/pdf/<task_id>` | GET | 导出PDF文件 |
| `/api/export/html/<task_id>` | GET | 获取HTML/纯文本内容 |
| `/api/export/answers/<task_id>` | GET | 获取答案文本 |

## 前端修改

### 按钮布局（结果区域）
```
[导出PDF] [导出Word] [复制题目] [复制答案] [打印] [重新出题]
```

### 新增JavaScript函数
- `exportPDF()` - 导出PDF（带答案）
- `exportPDFNoAnswer()` - 导出PDF（不含答案）
- `copyQuestions()` - 复制题目到剪贴板
- `copyAnswers()` - 复制答案到剪贴板
- `printQuestions()` - 打印预览
- `showToast(message, type)` - 显示操作反馈

## 新增文件

- `core/pdf_exporter.py` - PDF导出器核心类

## 依赖更新

`requirements.txt` 新增依赖:
```
reportlab>=4.0.0
```

安装方式:
```bash
pip install reportlab
```

## 使用说明

### 导出PDF
1. 生成题目后，点击"导出PDF"按钮
2. 浏览器自动下载PDF文件
3. 可选择是否包含答案

### 复制题目/答案
1. 生成题目后，点击"复制题目"或"复制答案"
2. 显示成功提示
3. 可直接粘贴到Word、文档等应用中

### 打印
1. 生成题目后，点击"打印"按钮
2. 弹出打印预览窗口
3. 选择打印机或另存为PDF

## 技术实现

### PDF生成
- 使用 `reportlab` 库
- A4纸张大小
- 支持中文（使用系统宋体）
- 分页控制

### 打印优化
- `@media print` CSS规则
- 隐藏非必要元素
- 优化排版
- 分页控制

### 复制功能
- `navigator.clipboard.writeText()` API
- `document.execCommand('copy')` 备用方案
- Toast提示反馈

## 注意事项

1. **PDF导出需要安装依赖**: `pip install reportlab`
2. **复制功能需要HTTPS或localhost环境**
3. **打印样式需测试浏览器兼容性**
