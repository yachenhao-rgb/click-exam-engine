# -*- coding: utf-8 -*-
"""
Deepseek API 接入测试脚本
=========================
测试智能出题引擎与Deepseek API的集成

运行方式:
    python test_deepseek.py
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.article_generator import ArticleGenerator


def test_deepseek_connection():
    """测试Deepseek API连通性"""
    print("=" * 60)
    print("测试1: Deepseek API 连通性测试")
    print("=" * 60)
    
    # 配置
    config = {
        'use_ai': True,
        'ai_provider': 'deepseek',
        'api_key': 'sk-a5e4167c60104892b35620b53224be13',
        'base_url': 'https://api.deepseek.com/v1',
        'model': 'deepseek-chat',
        'temperature': 0.7,
        'max_tokens': 2000,
        'enable_cache': False,  # 测试时禁用缓存
        'use_grammar_check': True,
    }
    
    generator = ArticleGenerator(config)
    
    # 检查初始化
    if generator._init_llm():
        print("✓ Deepseek API 初始化成功!")
    else:
        print("✗ Deepseek API 初始化失败!")
        return False
    
    return True


def test_article_generation():
    """测试文章生成功能"""
    print("\n" + "=" * 60)
    print("测试2: 文章生成功能测试")
    print("=" * 60)
    
    config = {
        'use_ai': True,
        'ai_provider': 'deepseek',
        'api_key': 'sk-a5e4167c60104892b35620b53224be13',
        'base_url': 'https://api.deepseek.com/v1',
        'model': 'deepseek-chat',
        'temperature': 0.7,
        'max_tokens': 2000,
        'enable_cache': False,
        'use_grammar_check': True,
    }
    
    generator = ArticleGenerator(config)
    
    # 测试用例：主题"校园"，题材"记叙文"，字数100，难度"初二"
    print("\n测试参数:")
    print("  - 主题: 校园 (school)")
    print("  - 题材: 记叙文 (Narrative)")
    print("  - 字数: 约100词")
    print("  - 难度: 初二 (A2)")
    print()
    
    result = generator.generate_article(
        topic='school',
        genre='记叙文',
        word_count=100,
        grade_level='初二',
        use_ai=True,
        enable_grammar_check=True,
        use_cache=False
    )
    
    print("\n生成结果:")
    print("-" * 40)
    print(f"标题: {result['title']}")
    print("-" * 40)
    print(f"正文:\n{result['content']}")
    print("-" * 40)
    print(f"实际词数: {result['word_count']}")
    print(f"目标词数: {result['target_word_count']}")
    print(f"生成方式: {result['generated_by']}")
    print(f"AI提供者: {result.get('ai_provider', 'N/A')}")
    print(f"难度级别: {result['difficulty']}")
    print(f"题材: {result['genre']}")
    
    if result.get('grammar_errors'):
        print(f"\n语法检查发现 {len(result['grammar_errors'])} 个潜在问题")
    
    return True


def test_different_cefr_levels():
    """测试不同CEFR级别的文章生成"""
    print("\n" + "=" * 60)
    print("测试3: 不同难度级别的文章生成")
    print("=" * 60)
    
    config = {
        'use_ai': True,
        'ai_provider': 'deepseek',
        'api_key': 'sk-a5e4167c60104892b35620b53224be13',
        'base_url': 'https://api.deepseek.com/v1',
        'model': 'deepseek-chat',
        'temperature': 0.7,
        'max_tokens': 2000,
        'enable_cache': False,
        'use_grammar_check': False,
    }
    
    generator = ArticleGenerator(config)
    
    levels = [
        ('初一', 'A1'),
        ('初二', 'A2'),
        ('初三', 'B1'),
        ('高二', 'B2'),
    ]
    
    for grade, cefr in levels:
        print(f"\n--- {grade} ({cefr}) ---")
        result = generator.generate_article(
            topic='travel',
            genre='记叙文',
            word_count=80,
            grade_level=grade,
            use_ai=True,
            use_cache=False
        )
        print(f"标题: {result['title']}")
        content_preview = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
        print(f"内容预览: {content_preview}")
        print(f"词数: {result['word_count']}")


def test_template_fallback():
    """测试模板降级功能"""
    print("\n" + "=" * 60)
    print("测试4: 模板降级功能测试")
    print("=" * 60)
    
    config = {
        'use_ai': False,  # 禁用AI，强制使用模板
        'enable_cache': False,
        'use_grammar_check': False,
    }
    
    generator = ArticleGenerator(config)
    
    result = generator.generate_article(
        topic='technology',
        genre='说明文',
        word_count=100,
        grade_level='初三',
        use_ai=False,
        use_cache=False
    )
    
    print("\n模板生成结果:")
    print("-" * 40)
    print(f"标题: {result['title']}")
    print(f"正文:\n{result['content']}")
    print("-" * 40)
    print(f"生成方式: {result['generated_by']}")
    print(f"词数: {result['word_count']}")


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("智能出题引擎 v3.0 - Deepseek API 接入测试")
    print("=" * 60)
    
    try:
        # 测试1: 连通性测试
        if not test_deepseek_connection():
            print("\n警告: API连通性测试失败，继续其他测试...")
        
        # 测试2: 文章生成测试
        test_article_generation()
        
        # 测试3: 不同难度级别测试
        test_different_cefr_levels()
        
        # 测试4: 模板降级测试
        test_template_fallback()
        
        print("\n" + "=" * 60)
        print("测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
