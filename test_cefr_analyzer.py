# -*- coding: utf-8 -*-
"""
CEFR分析器测试脚本
"""

import sys
import os
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.cefr_analyzer import CEFRAnalyzer, analyze_text


def test_basic_analysis():
    """测试基础分析功能"""
    print("=" * 60)
    print("测试1: 基础词汇和句法分析")
    print("=" * 60)
    
    analyzer = CEFRAnalyzer()
    
    # 测试文本
    test_text = """
    My name is Li Ming and I am a student at Beijing University. 
    Every day, I wake up early in the morning and go to the library to study. 
    I usually have classes from 8 o'clock until 5 o'clock in the afternoon. 
    After class, I often play basketball with my friends on the campus. 
    We also like to discuss interesting topics about science and technology.
    However, sometimes I feel stressed because of the heavy homework and upcoming examinations.
    """
    
    print(f"\n测试文本 ({len(test_text)} 字符):")
    print(test_text.strip()[:200] + "...")
    
    # 使用便捷函数进行完整分析
    print("\n--- 完整CEFR分析 ---")
    result = analyzer.analyze(test_text)
    
    print(f"总体等级: {result['overall_level']}")
    print(f"居间等级: {result['intermediate_level']}")
    print(f"单词数: {result['word_count']}")
    print(f"句子数: {result['sentence_count']}")
    
    print("\n词汇分布:")
    for level, data in result['distribution'].items():
        print(f"  {level}: {data['count']} ({data['percent']}%)")
    
    print("\n词汇识别:")
    print(f"  识别率: {result['vocabulary']['recognized_ratio']}%")
    print(f"  未识别率: {result['vocabulary']['unrecognized_ratio']}%")
    print(f"  主导等级: {result['vocabulary']['dominant_level']}")
    
    print("\n句法复杂度:")
    for key, value in result['complexity'].items():
        print(f"  {key}: {value}")
    
    print("\n话题分析:")
    print(f"  类别: {result['topic']['category']}")
    print(f"  熟悉度: {result['topic']['familiarity']}")
    
    return result


def test_different_levels():
    """测试不同难度的文本"""
    print("\n" + "=" * 60)
    print("测试2: 不同难度文本对比")
    print("=" * 60)
    
    analyzer = CEFRAnalyzer()
    
    texts = {
        "A1级别": "I am a boy. This is my book. I like apples. My mom is kind. We go to school. The cat is small. I can run fast.",
        "B1级别": "Yesterday, I went to the cinema with my friends. We watched a very interesting movie about history. Although it was quite long, we all enjoyed it very much. After the movie, we had dinner at a nearby restaurant.",
        "C1级别": "The unprecedented technological advancements have fundamentally transformed our understanding of human cognition and communication. Furthermore, the interdisciplinary nature of modern research necessitates a comprehensive approach."
    }
    
    for level, text in texts.items():
        print(f"\n--- {level} ---")
        result = analyzer.analyze(text)
        print(f"总体等级: {result['overall_level']}")
        print(f"居间等级: {result['intermediate_level']}")
        print(f"词汇识别率: {result['vocabulary']['recognized_ratio']}%")
        print(f"平均句长: {result['complexity']['avg_sentence_length']}")


def test_output_format():
    """测试输出格式是否符合要求"""
    print("\n" + "=" * 60)
    print("测试3: 输出格式验证")
    print("=" * 60)
    
    analyzer = CEFRAnalyzer()
    
    test_text = """
    My name is Tom and I am a student in Grade 10. Every morning, I wake up at six o'clock and have breakfast with my family. Then I go to school by bus. In school, I study many subjects such as English, Mathematics, and Science. After class, I usually play basketball with my classmates on the playground. Sometimes I feel tired because of the heavy homework, but I still enjoy my school life.
    """
    
    result = analyzer.analyze(test_text)
    
    # 验证输出字段
    required_fields = [
        'overall_level', 'intermediate_level', 'word_count', 'sentence_count', 
        'distribution', 'complexity', 'topic', 'vocabulary'
    ]
    
    print("\n验证输出字段:")
    for field in required_fields:
        if field in result:
            print(f"  ✓ {field}")
        else:
            print(f"  ✗ {field} (缺失)")
    
    # 验证distribution格式
    print("\ndistribution结构验证:")
    for level in ['A1', 'A2', 'B1', 'B2', 'C1']:
        if level in result['distribution']:
            dist = result['distribution'][level]
            if 'count' in dist and 'percent' in dist:
                print(f"  ✓ {level}: count={dist['count']}, percent={dist['percent']}%")
    
    # 验证complexity格式
    print("\ncomplexity结构验证:")
    complexity_fields = ['avg_sentence_length', 'clause_ratio', 'passive_ratio']
    for field in complexity_fields:
        if field in result['complexity']:
            print(f"  ✓ {field}: {result['complexity'][field]}")
    
    print("\n最终JSON输出:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def test_convenience_function():
    """测试便捷函数"""
    print("\n" + "=" * 60)
    print("测试4: 便捷函数")
    print("=" * 60)
    
    test_text = "I love learning English. It is a wonderful language."
    result = analyze_text(test_text)
    
    print(f"\n输入: {test_text}")
    print(f"总体等级: {result['overall_level']}")
    print(f"居间等级: {result['intermediate_level']}")


def test_topic_analysis():
    """测试话题分析"""
    print("\n" + "=" * 60)
    print("测试5: 话题分析")
    print("=" * 60)
    
    analyzer = CEFRAnalyzer()
    
    texts = {
        "校园话题": "My school has a big library. I often study there after class. My teachers are very kind and helpful. I have many friends at school. We often play sports together.",
        "科技话题": "The smartphone has changed our lives significantly. Artificial intelligence is becoming more popular. People use computers for work and entertainment. The internet connects billions of people worldwide.",
        "健康话题": "Regular exercise is important for health. A balanced diet can help you stay fit. Many people go to the gym to work out. Getting enough sleep is also essential for well-being."
    }
    
    for topic, text in texts.items():
        print(f"\n--- {topic} ---")
        result = analyzer.analyze(text)
        print(f"识别话题: {result['topic']['category']}")
        print(f"熟悉度: {result['topic']['familiarity']}")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("CEFR文本分析器测试")
    print("=" * 60)
    
    test_basic_analysis()
    test_different_levels()
    test_output_format()
    test_convenience_function()
    test_topic_analysis()
    
    print("\n" + "=" * 60)
    print("所有测试完成!")
    print("=" * 60)
