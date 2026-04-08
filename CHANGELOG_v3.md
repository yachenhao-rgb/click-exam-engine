# 智能出题引擎 - 文章生成器 v3.0 优化说明

## 版本信息
- **当前版本**: v3.0.0
- **发布日期**: 2024年
- **基于版本**: v2.0

---

## 一、优化概览

本次优化从v2.0升级到v3.0，主要实现了以下五大功能增强：

| 优化方向 | v2.0状态 | v3.0新增 |
|---------|---------|---------|
| 模板丰富化 | 4种题材 | 12+种题材 |
| AI集成 | 无 | 支持OpenAI/Claude/本地模型 |
| 词汇扩展 | 8个主题 | 18个主题 + 动态扩展接口 |
| 语法检查 | 无 | 内置规则 + 外部库可选 |
| 缓存机制 | 无 | LRU缓存 + 持久化 |

---

## 二、详细优化说明

### 1. 模板丰富化

#### 1.1 题材扩充（4种 → 12种）

| 题材ID | 题材名称 | 说明 | 新增 |
|--------|---------|------|------|
| 记叙文 | Narrative | 叙事性文章 | - |
| 说明文 | Explanatory | 说明解释性文章 | - |
| 议论文 | Argumentative | 议论性文章 | - |
| 应用文 | Practical | 书信/邮件等应用文 | - |
| 描写文 | Descriptive | 描写性文章 | ✅ 新增 |
| 看图作文 | Picture-based | 看图写话 | ✅ 新增 |
| 科幻文 | Science Fiction | 科幻题材 | ✅ 新增 |
| 日记 | Diary | 日记格式 | ✅ 新增 |
| 科技 | Technology | 科技主题 | ✅ 新增 |
| 历史 | History | 历史主题 | ✅ 新增 |
| 健康 | Health | 健康主题 | ✅ 新增 |
| 文化 | Culture | 文化主题 | ✅ 新增 |
| 体育 | Sports | 体育主题 | ✅ 新增 |
| 美食 | Food | 美食主题 | ✅ 新增 |
| 艺术 | Art | 艺术主题 | ✅ 新增 |
| 自然 | Nature | 自然主题 | ✅ 扩展 |
| 社会 | Social | 社会主题 | ✅ 新增 |
| 职业 | Career | 职业主题 | ✅ 新增 |
| 节日 | Festival | 庆典主题 | ✅ 新增 |

#### 1.2 结构变体

为部分题材增加了不同的篇章结构变体：

**记叙文结构变体:**
- `chronological`: 按时间顺序（First, Then, After that, Finally）
- `flashback`: 倒叙手法（从结局开始，回顾经过）
- `frame`: 框架结构（首尾呼应的框架）

**说明文结构变体:**
- 定义说明
- 分类说明
- 原因-结果说明
- 比较对比说明

**议论文结构变体:**
- 正反论证
- 立论-驳论
- 引论-本论-结论

---

### 2. AI集成

#### 2.1 支持的AI服务商

| 服务商 | Provider ID | 模型示例 | 说明 |
|--------|-------------|---------|------|
| OpenAI | `openai` | gpt-3.5-turbo, gpt-4 | 支持API代理 |
| Claude | `claude` | claude-3-sonnet, claude-3-opus | Anthropic系列 |
| 本地模型 | `local` | llama2, mistral, qwen | Ollama等本地部署 |

#### 2.2 智能降级机制

```
┌─────────────────┐
│  请求生成文章   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  use_ai=True?  │──否──→ 使用模板生成
└────────┬────────┘
         │是
         ▼
┌─────────────────┐
│  API可用?       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   是        否
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│ AI生成 │ │ 回退到  │
│        │ │ 模板生成│
└────────┘ └────────┘
```

#### 2.3 Prompt工程

内置了针对不同CEFR级别的Prompt模板：

- **A1级别**: 强调简单词汇和基础句型
- **A2级别**: 引入并列句和频率副词
- **B1级别**: 使用复合句和连接词
- **B2级别**: 要求学术词汇和复杂结构

---

### 3. 词汇扩展

#### 3.1 主题词库（8个 → 18个）

| 主题ID | 主题名称 | A1词汇 | A2词汇 | B1词汇 | B2词汇 |
|--------|---------|--------|--------|--------|--------|
| school | 校园生活 | 30+ | 40+ | 20+ | 20+ |
| family | 家庭亲情 | 30+ | 30+ | 15+ | 15+ |
| travel | 旅行 | 30+ | 35+ | 20+ | 15+ |
| nature | 自然 | 30+ | 30+ | 20+ | 15+ |
| sport | 运动 | 25+ | 30+ | 15+ | 15+ |
| environment | 环境 | 25+ | 30+ | 20+ | 20+ |
| hobby | 爱好 | 25+ | 30+ | 20+ | 15+ |
| holiday | 节日 | 25+ | 30+ | 15+ | 15+ |
| **technology** | 科技 | 15+ | 25+ | 20+ | 25+ |
| **food** | 美食 | 15+ | 25+ | 20+ | 20+ |
| **health** | 健康 | 15+ | 25+ | 20+ | 20+ |
| **culture** | 文化 | 15+ | 20+ | 20+ | 25+ |
| **history** | 历史 | 15+ | 20+ | 20+ | 20+ |
| **art** | 艺术 | 10+ | 20+ | 20+ | 20+ |
| **career** | 职业 | 10+ | 20+ | 15+ | 20+ |
| **science** | 科学 | 10+ | 20+ | 20+ | 20+ |
| **social** | 社会 | 10+ | 15+ | 20+ | 20+ |
| **festival** | 庆典 | 10+ | 15+ | 15+ | 20+ |

#### 3.2 动态扩展接口

```python
# 添加新主题词汇
generator.add_topic_vocabulary(
    topic='环境保护',  # 主题ID
    cefr_level='B1',
    vocabulary={
        'places': ['环保中心', '回收站'],
        'activities': ['回收', '分类'],
        'adjectives': {'A1': [], 'A2': [], 'B1': ['可持续的'], 'B2': []},
        'verbs': {'A1': [], 'A2': [], 'B1': ['节约'], 'B2': []}
    }
)

# 添加通用级别词汇
generator.add_vocabulary(
    cefr_level='C1',  # 可扩展到C级别
    words=['vocabulary', 'words', ...],
    topic=None  # 通用词汇
)
```

---

### 4. 语法检查

#### 4.1 内置检查规则

| 规则类型 | 检查内容 | 示例 |
|---------|---------|------|
| 主谓一致 | 主语和谓语动词的一致性 | he have → he has |
| 冠词使用 | a/an的正确使用 | a apple → an apple |
| 时态一致 | 同一句子内的时态统一 | just difed → just did |
| 介词搭配 | 常见介词短语 | in Monday → on Monday |

#### 4.2 外部语法检查库（可选）

支持集成 `language-tool-python`：

```bash
pip install language-tool-python
```

```python
# 启用外部语法检查
config = {
    'use_grammar_check': True,
    'grammar_check_external': True  # 启用外部库
}
generator = ArticleGenerator(config)
```

---

### 5. 缓存机制

#### 5.1 LRU缓存策略

- 最大容量: 可配置（默认1000条）
- 淘汰策略: 最近最少使用（Least Recently Used）
- 线程安全: 支持并发访问

#### 5.2 缓存持久化

```
内存缓存 ←→ 磁盘文件
   ↕              ↕
  读取          持久化
```

- 缓存路径: 可配置（默认 `.article_cache.json`）
- 自动保存: 每次写入后延迟保存
- 启动加载: 启动时自动加载已有缓存

#### 5.3 缓存键设计

```
hash(topic + genre + word_count + cefr_level + style + use_ai)
```

---

## 三、向后兼容性

### 3.1 API兼容

v3.0保持与v2.0相同的核心接口：

```python
# v2.0 用法（仍然支持）
generator = ArticleGenerator()
result = generator.generate_article('travel', '记叙文', 150, '初二')

# v3.0 新增参数
result = generator.generate_article(
    topic='travel',
    genre='记叙文',
    word_count=150,
    grade_level='初二',
    style='chronological',  # 新增：结构风格
    use_ai=False,           # 新增：是否使用AI
    enable_grammar_check=True,  # 新增：语法检查
    use_cache=True          # 新增：缓存控制
)
```

### 3.2 返回值兼容

v3.0在v2.0返回值基础上新增了以下字段：

```python
{
    'title': '...',
    'content': '...',
    'word_count': 150,
    'target_word_count': 150,
    'genre': '记叙文',
    'topic': 'travel',
    'difficulty': 'A2',
    'grade_level': '初二',
    # v3.0 新增字段
    'generated_by': 'template',  # 或 'ai'
    'grammar_errors': [],         # 语法错误列表
    'from_cache': False,         # 是否来自缓存
    'ai_provider': None,         # AI服务商（仅AI生成时有）
}
```

---

## 四、配置方式

### 4.1 代码配置

```python
from article_generator import ArticleGenerator
from config import Config

# 方式1: 使用默认配置
generator = ArticleGenerator()

# 方式2: 使用字典配置
config = {
    'use_ai': True,
    'ai_provider': 'openai',
    'api_key': 'your-api-key',
    'enable_cache': True,
    'use_grammar_check': True,
}
generator = ArticleGenerator(config)

# 方式3: 使用Config类
config = Config(
    use_ai=True,
    ai_provider='claude',
    enable_cache=True
)
generator = ArticleGenerator(config.as_dict())
```

### 4.2 环境变量配置

```bash
# .env 文件
USE_AI=true
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
AI_MODEL=gpt-3.5-turbo
ENABLE_CACHE=true
CACHE_SIZE=500
USE_GRAMMAR_CHECK=true
```

```python
# 加载环境变量配置
config = Config.load()  # 自动读取.env文件
generator = ArticleGenerator(config.as_dict())
```

### 4.3 配置文件

创建 `config.json`:

```json
{
    "use_ai": true,
    "ai_provider": "openai",
    "api_key": "",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "enable_cache": true,
    "cache_size": 1000,
    "cache_path": ".article_cache.json",
    "use_grammar_check": true,
    "grammar_check_external": false,
    "wordlist_path": "./data/cefr_wordlist.json"
}
```

---

## 五、使用示例

### 5.1 基础用法

```python
from article_generator import ArticleGenerator

# 创建生成器
generator = ArticleGenerator()

# 生成文章
result = generator.generate_article(
    topic='environment',
    genre='议论文',
    word_count=200,
    grade_level='高二'
)

print(result['title'])
print(result['content'])
print(f"字数: {result['word_count']}")
```

### 5.2 启用AI生成

```python
config = {
    'use_ai': True,
    'ai_provider': 'openai',
    'api_key': os.environ.get('OPENAI_API_KEY'),
    'model': 'gpt-4'
}

generator = ArticleGenerator(config)

result = generator.generate_article(
    topic='technology',
    genre='说明文',
    word_count=250,
    grade_level='高三'
)

print(f"生成方式: {result['generated_by']}")
```

### 5.3 使用缓存

```python
generator = ArticleGenerator({
    'enable_cache': True,
    'cache_size': 500
})

# 第一次生成（缓存未命中）
result1 = generator.generate_article('travel', '记叙文', 150, '初二')

# 第二次相同请求（缓存命中）
result2 = generator.generate_article('travel', '记叙文', 150, '初二')
print(f"来自缓存: {result2['from_cache']}")

# 查看缓存统计
stats = generator.get_cache_stats()
print(f"缓存条目: {stats['size']}/{stats['max_size']}")

# 清空缓存
count = generator.clear_cache()
print(f"已清空 {count} 条缓存")
```

### 5.4 自定义词汇

```python
# 添加新主题
generator.add_topic_vocabulary(
    topic='人工智能',
    cefr_level='B2',
    vocabulary={
        'places': ['research lab', 'AI center'],
        'activities': ['programming', 'training'],
        'adjectives': {'A1': [], 'A2': [], 'B1': [], 'B2': ['revolutionary', 'cutting-edge']},
        'verbs': {'A1': [], 'A2': [], 'B1': [], 'B2': ['revolutionize', 'transform']}
    }
)

result = generator.generate_article(
    topic='人工智能',
    genre='说明文',
    word_count=200,
    grade_level='高二'
)
```

---

## 六、性能对比

### 6.1 生成速度

| 生成方式 | 首次生成 | 缓存命中 |
|---------|---------|---------|
| 模板生成 | ~50ms | ~1ms |
| AI生成 (GPT-3.5) | ~2-5s | ~1ms |
| AI生成 (GPT-4) | ~5-10s | ~1ms |

### 6.2 内存占用

| 配置项 | 内存占用 |
|-------|---------|
| 无缓存 | ~5MB |
| 1000条缓存 | ~15-20MB |
| 持久化文件 | 取决于缓存量 |

---

## 七、升级建议

### 7.1 从v2.0升级

1. **备份现有代码**
2. **替换article_generator.py文件**
3. **可选：添加config.py配置文件**
4. **逐步测试现有功能**
5. **根据需要启用新功能**

### 7.2 推荐配置

**轻量使用（无API）:**
```python
config = {
    'enable_cache': True,
    'use_grammar_check': True
}
```

**AI增强（推荐）:**
```python
config = {
    'use_ai': True,
    'ai_provider': 'openai',
    'enable_cache': True,
    'use_grammar_check': True
}
```

**生产环境:**
```python
config = {
    'use_ai': True,
    'ai_provider': 'openai',
    'enable_cache': True,
    'cache_size': 2000,
    'use_grammar_check': True,
    'grammar_check_external': True  # 需要安装language-tool-python
}
```

---

## 八、注意事项

1. **API密钥安全**: 不要将API密钥直接写入代码，使用环境变量
2. **缓存清理**: 定期清理缓存或设置合理的缓存大小
3. **AI生成成本**: GPT-4等高级模型成本较高，注意控制调用频率
4. **语法检查限制**: 内置检查仅覆盖常见错误，复杂语法问题建议使用外部库

---

## 九、文件清单

| 文件 | 说明 |
|-----|------|
| `article_generator.py` | 主生成器模块（v3.0） |
| `text_adjuster.py` | 文本调整器（v2.0，保持不变） |
| `config.py` | 配置文件（新增） |
| `cefr_wordlist.json` | 基础词库（扩充中） |
| `CHANGELOG_v3.md` | 本优化说明文档 |

---

## 十、联系与支持

如有问题或建议，请联系开发团队。

---

*文档版本: v3.0.0*
*最后更新: 2024年*
