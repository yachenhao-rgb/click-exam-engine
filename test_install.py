#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证智能出题引擎Web版是否正确安装
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("智能出题引擎Web版 - 安装验证")
print("=" * 50)

errors = []

# 测试1: 检查依赖
print("\n[1/6] 检查Python依赖...")
try:
    import flask
    print(f"  ✓ Flask {flask.__version__}")
except ImportError:
    errors.append("Flask未安装，请运行: pip install flask")

try:
    import docx
    print("  ✓ python-docx 已安装")
except ImportError:
    errors.append("python-docx未安装，请运行: pip install python-docx")

# 测试2: 核心模块
print("\n[2/6] 检查核心模块...")
try:
    from core.kb_manager import KnowledgeBaseManager, init_database
    print("  ✓ kb_manager")
except ImportError as e:
    errors.append(f"kb_manager导入失败: {e}")

try:
    from core.exam_generator import ExamGenerator
    print("  ✓ exam_generator")
except ImportError as e:
    errors.append(f"exam_generator导入失败: {e}")

try:
    from core.docx_exporter import WordExporter
    print("  ✓ docx_exporter")
except ImportError as e:
    errors.append(f"docx_exporter导入失败: {e}")

# 测试3: 检查数据库
print("\n[3/6] 检查数据库...")
db_path = "data/knowledge_base.db"
if os.path.exists(db_path):
    print(f"  ✓ 数据库文件存在: {db_path}")
else:
    print(f"  ⚠ 数据库文件不存在，将自动创建")

# 测试4: 检查目录
print("\n[4/6] 检查目录结构...")
dirs = ["data", "data/知识库数据", "output", "templates", "static/css", "static/js"]
for d in dirs:
    if os.path.exists(d):
        print(f"  ✓ {d}/")
    else:
        os.makedirs(d, exist_ok=True)
        print(f"  + {d}/ (已创建)")

# 测试5: 检查模板
print("\n[5/6] 检查模板文件...")
templates = ["index.html", "kb_manage.html", "history.html"]
for t in templates:
    path = os.path.join("templates", t)
    if os.path.exists(path):
        print(f"  ✓ templates/{t}")
    else:
        errors.append(f"模板文件缺失: templates/{t}")

# 测试6: 生成测试题目
print("\n[6/6] 测试题目生成...")
try:
    if not os.path.exists(db_path):
        init_database(db_path)
    
    kb = KnowledgeBaseManager(db_path)
    kb.connect()
    vocab_count = len(kb.get_all_vocab())
    trap_count = len(kb.get_all_traps())
    kb.close()
    print(f"  ✓ 知识库: {vocab_count}词汇, {trap_count}陷阱")
    
    generator = ExamGenerator(db_path)
    test_text = "Reading is one of the most important skills we can develop. It opens doors to new worlds and helps us understand different perspectives. Through reading, we can learn about different cultures and ideas."
    result = generator.generate_exam(test_text, 3)
    print(f"  ✓ 生成测试: {result['total_blanks']}道题目")
except Exception as e:
    errors.append(f"题目生成测试失败: {e}")

# 总结
print("\n" + "=" * 50)
if errors:
    print("发现以下问题:")
    for i, err in enumerate(errors, 1):
        print(f"  {i}. {err}")
    print("\n请解决上述问题后重新运行测试")
    sys.exit(1)
else:
    print("✓ 所有检查通过！")
    print("\n启动应用:")
    print("  Linux/Mac: ./run.sh")
    print("  Windows:   run.bat")
    print("  或直接:    python app.py")
    print("\n访问地址: http://localhost:5000")
    print("=" * 50)
