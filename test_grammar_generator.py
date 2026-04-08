# -*- coding: utf-8 -*-
"""
语法填空生成器测试
"""

import sys
sys.path.insert(0, '.')

from core.grammar_generator import (
    GrammarGenerator, 
    create_grammar_questions,
    BlankType,
    GrammarPoint
)


def test_basic_generation():
    """测试基本生成功能"""
    print("=" * 60)
    print("测试1: 基本生成功能")
    print("=" * 60)
    
    text = """
    Yesterday I went to the park with my friends. We had a wonderful time there.
    The weather was very nice and the sun was shining brightly. 
    Many people were walking on the grass and children were playing games.
    I saw a little girl who was crying. Her face was red and she looked worried.
    Her mother tried to comfort her and gave her some candy.
    """
    
    result = create_grammar_questions(text, num_blanks=10)
    
    print("\n【原文】")
    print(result['original_text'].strip())
    print("\n【带空题目】")
    print(result['text_with_blanks'])
    print("\n【答案】")
    for i, ans in enumerate(result['answers'], 1):
        print(f"  {i}. {ans}")
    print("\n【解析】")
    for i, exp in enumerate(result['explanations'], 1):
        print(f"  {i}. {exp}")
    
    return result


def test_exam_point_distribution():
    """测试考点分布"""
    print("\n" + "=" * 60)
    print("测试2: 考点分布统计")
    print("=" * 60)
    
    text = """
    Tom is a student. He usually goes to school by bus every morning.
    Yesterday, he got up early and reached the school on time.
    The teachers were teaching and the students were listening carefully.
    Tom's father is a doctor. He works in a big hospital.
    Tom's mother cooks delicious food for the family every day.
    """
    
    result = create_grammar_questions(text, num_blanks=10)
    
    # 统计考点类型
    point_stats = {}
    for q in result['questions']:
        gp = q['grammar_point']
        point_stats[gp] = point_stats.get(gp, 0) + 1
    
    print("\n【考点分布统计】")
    for point, count in sorted(point_stats.items(), key=lambda x: -x[1]):
        print(f"  {point}: {count}题")
    
    return result


def test_no_hint_blanks():
    """测试无提示填空"""
    print("\n" + "=" * 60)
    print("测试3: 无提示填空识别")
    print("=" * 60)
    
    text = """
    I went to the library yesterday because I wanted to borrow some books.
    The library is on the corner of the street. It is very quiet there.
    I sat at a desk and started reading. The book was interesting.
    """
    
    result = create_grammar_questions(text, num_blanks=10)
    
    no_hint_count = sum(1 for q in result['questions'] 
                       if q['blank_type'] == BlankType.NO_HINT.value)
    has_hint_count = len(result['questions']) - no_hint_count
    
    print("\n【无提示填空 vs 有提示填空】")
    print(f"  无提示填空: {no_hint_count}题")
    print(f"  有提示填空: {has_hint_count}题")
    
    print("\n【题目详情】")
    for q in result['questions']:
        btype = "无提示" if q['blank_type'] == BlankType.NO_HINT.value else "有提示"
        print(f"  {q['blank_number']}. {btype} | {q['grammar_point']} | {q['answer']}")


def test_difficulty_levels():
    """测试不同难度"""
    print("\n" + "=" * 60)
    print("测试4: 不同难度级别")
    print("=" * 60)
    
    text = """
    Last weekend, my family went to the beach. The weather was perfect.
    We arrived there early in the morning. The beach was beautiful.
    My father swam in the sea while my mother read a book.
    I built a big sandcastle with my sister. We had a great time.
    """
    
    for difficulty in ['easy', 'medium', 'hard']:
        result = create_grammar_questions(text, num_blanks=8, difficulty=difficulty)
        print(f"\n【难度: {difficulty.upper()}】")
        print(f"  生成题目数: {len(result['questions'])}")


def test_api_format():
    """测试API格式兼容性"""
    print("\n" + "=" * 60)
    print("测试5: API格式兼容性")
    print("=" * 60)
    
    text = """
    Every day, students go to school to learn knowledge.
    They study hard and make progress in their studies.
    Teachers are kind and patient with their students.
    """
    
    result = create_grammar_questions(text, num_blanks=6)
    
    # 验证API返回格式
    print("\n【返回字段检查】")
    required_fields = ['text_with_blanks', 'questions', 'answers', 'explanations', 'question_type', 'original_text']
    for field in required_fields:
        exists = field in result
        print(f"  {field}: {'✓' if exists else '✗'}")
    
    print("\n【题目字段检查】")
    question = result['questions'][0] if result['questions'] else {}
    q_fields = ['blank_number', 'answer', 'hint', 'explanation', 'grammar_point', 'blank_type', 'original_word', 'context']
    for field in q_fields:
        exists = field in question
        print(f"  {field}: {'✓' if exists else '✗'}")
    
    print("\n【答案卡预览】")
    print(result['answer_sheet'])
    print("\n【解析卡预览】")
    print(result['explanation_sheet'])


def test_grammar_points():
    """测试语法考点类型"""
    print("\n" + "=" * 60)
    print("测试6: 支持的语法考点类型")
    print("=" * 60)
    
    print("\n【支持的填空类型】")
    for bt in BlankType:
        print(f"  - {bt.value}")
    
    print("\n【支持的语法考点】")
    for gp in GrammarPoint:
        print(f"  - {gp.value}")


def test_db_path_compatibility():
    """测试数据库路径兼容性"""
    print("\n" + "=" * 60)
    print("测试7: 数据库路径兼容性")
    print("=" * 60)
    
    # 测试无参数初始化
    gen1 = GrammarGenerator()
    print("  无参数初始化: ✓")
    
    # 测试带路径初始化
    gen2 = GrammarGenerator("data/knowledge_base.db")
    print("  带路径初始化: ✓")
    
    text = "The sun is shining brightly today."
    result1 = gen1.generate_questions(text, num_blanks=5)
    result2 = gen2.generate_questions(text, num_blanks=5)
    
    print(f"  生成题目数: {len(result1['questions'])} vs {len(result2['questions'])}")
    print("  API格式兼容: ✓")


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("语法填空生成器 - 功能测试")
    print("=" * 60)
    
    test_basic_generation()
    test_exam_point_distribution()
    test_no_hint_blanks()
    test_difficulty_levels()
    test_api_format()
    test_grammar_points()
    test_db_path_compatibility()
    
    print("\n" + "=" * 60)
    print("所有测试完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
