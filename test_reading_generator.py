# -*- coding: utf-8 -*-
"""
阅读理解模块测试
"""

import sys
sys.path.insert(0, '.')

from core.reading_generator import ReadingGenerator, generate_reading_questions

# 测试文本1 - 记叙文
TEST_TEXT_1 = """
Once upon a time, there was a young girl named Lily who loved to read books. 
Every day after school, she would go to the local library and spend hours reading 
stories about faraway places and magical adventures. Her favorite book was about 
a brave knight who saved a kingdom from a terrible dragon. Lily dreamed that one 
day she could be just as brave as the knight in her favorite story.

One day, when Lily was walking home from school, she noticed a small kitten 
trapped in a tree. The kitten was crying for help, but no one seemed to notice. 
Lily remembered the brave knight in her book and decided to help the frightened 
animal. She quickly called for her father, who brought a ladder and carefully 
rescued the poor kitten. The kitten was safe and happy, and Lily felt like a 
real hero.

From that day on, Lily understood that being brave was not about fighting dragons. 
It was about helping others when they needed help the most.
"""

# 测试文本2 - 说明文
TEST_TEXT_2 = """
Every year, millions of people travel to different countries for vacation. 
Traveling can be an exciting experience, but it also requires careful planning. 
First, you need to decide where you want to go. Consider your budget, the weather, 
and the activities available at your destination.

Next, you should book your flights and hotels early. During peak travel seasons, 
prices can increase significantly. Many travelers use the internet to compare prices 
and find the best deals. It is also important to check the visa requirements for 
your destination country.

When packing for your trip, remember to bring only the essentials. Heavy luggage 
can be a burden, especially if you plan to move around frequently. Bring comfortable 
shoes and appropriate clothing for the weather conditions. Do not forget important 
documents such as your passport and travel insurance information.

Finally, be open to new experiences. Try local food, learn about different cultures, 
and make friends with people from various backgrounds. The best memories from travel 
often come from unexpected moments and spontaneous adventures.
"""

# 测试文本3 - 议论文
TEST_TEXT_3 = """
Should students be allowed to use smartphones in school? This question has sparked 
heated debates among parents, teachers, and students alike. Some people believe that 
smartphones can be valuable learning tools, while others worry about their potential 
distractions.

On one hand, smartphones can provide students with instant access to educational 
apps, online libraries, and educational videos. Students can use them to research 
topics for their assignments or calculator functions for math problems. In case 
of emergencies, smartphones allow students to contact their parents quickly.

On the other hand, many teachers argue that smartphones often become a source of 
distraction in the classroom. Students may be tempted to play games or browse social 
media during lessons. There are also concerns about cyberbullying and students 
accessing inappropriate content.

In my opinion, the key is to find a balance. Schools should establish clear rules 
about when and how smartphones can be used. With proper guidance, students can learn 
to use these devices responsibly while still maintaining a focused learning environment.
"""


def test_reading_generator():
    """测试阅读理解生成器"""
    print("=" * 60)
    print("阅读理解模块测试")
    print("=" * 60)
    
    generator = ReadingGenerator()
    
    # 测试不同文章类型
    test_cases = [
        ("记叙文", TEST_TEXT_1),
        ("说明文", TEST_TEXT_2),
        ("议论文", TEST_TEXT_3)
    ]
    
    for article_type, test_text in test_cases:
        print(f"\n{'='*60}")
        print(f"测试：{article_type}")
        print(f"{'='*60}")
        
        # 生成4题
        result = generator.generate_questions(test_text, num_questions=4, difficulty='medium')
        
        print(f"\n标题: {result['title']}")
        print(f"文章类型: {result['article_type']}")
        print(f"词数: {result['word_count']}")
        print(f"题目数量: {result['total_questions']}")
        
        # 显示关键信息
        if 'key_info' in result:
            print("\n关键信息提取:")
            print(f"  - 人物: {result['key_info'].get('people', [])[:3]}")
            print(f"  - 数字: {result['key_info'].get('numbers', [])[:5]}")
            print(f"  - 主题: {result['key_info'].get('topics', [])[:5]}")
        
        print("\n生成题目:")
        for q in result['questions']:
            print(f"\n  第{q['number']}题 [{q['type']}]")
            print(f"  题目: {q['question']}")
            print(f"  选项:")
            for i, opt in enumerate(q['options']):
                letter = chr(65 + i)
                marker = "✓" if letter == q['correct'] else " "
                print(f"    {marker} {letter}. {opt[:50]}{'...' if len(opt) > 50 else ''}")
    
    # 测试格式化输出
    print("\n" + "=" * 60)
    print("测试格式化输出")
    print("=" * 60)
    
    raw_result = generator.generate_questions(TEST_TEXT_1, num_questions=4, difficulty='medium')
    formatted = generator._generate_reading_exam_output(raw_result)
    
    print(f"\nexam_type: {formatted.get('exam_type')}")
    print(f"article_title: {formatted.get('article_title')}")
    print(f"article_type: {formatted.get('article_type')}")
    print(f"word_count: {formatted.get('word_count')}")
    print(f"total_questions: {formatted.get('total_questions')}")
    print(f"total_score: {formatted.get('total_score')}")
    
    return formatted


def test_convenience_function():
    """测试便捷函数"""
    print("\n" + "=" * 60)
    print("测试便捷函数")
    print("=" * 60)
    
    result = generate_reading_questions(TEST_TEXT_2, num_questions=4, difficulty='medium')
    
    print(f"\n便捷函数返回结果:")
    print(f"exam_type: {result.get('exam_type')}")
    print(f"article_type: {result.get('article_type')}")
    print(f"total_questions: {result.get('total_questions')}")
    
    return result


def test_difficulty_levels():
    """测试不同难度级别"""
    print("\n" + "=" * 60)
    print("测试不同难度级别")
    print("=" * 60)
    
    generator = ReadingGenerator()
    
    for difficulty in ['easy', 'medium', 'hard']:
        print(f"\n难度级别: {difficulty}")
        result = generator.generate_questions(TEST_TEXT_1, num_questions=4, difficulty=difficulty)
        
        question_types = [q['type'] for q in result['questions']]
        print(f"  题型分布: {question_types}")
    
    return True


def test_question_type_distribution():
    """测试题型分配"""
    print("\n" + "=" * 60)
    print("测试题型分配")
    print("=" * 60)
    
    generator = ReadingGenerator()
    
    # 多次生成看分布
    all_types = []
    for _ in range(20):
        result = generator.generate_questions(TEST_TEXT_1, num_questions=4, difficulty='medium')
        all_types.extend([q['type_code'] for q in result['questions']])
    
    from collections import Counter
    type_counts = Counter(all_types)
    
    print("\n题型分布统计（100题）:")
    type_names = {
        'main_idea': '主旨大意题',
        'detail': '细节理解题',
        'inference': '推理判断题',
        'word_meaning': '词义猜测题'
    }
    for qtype, count in sorted(type_counts.items()):
        name = type_names.get(qtype, qtype)
        print(f"  {name}: {count} 题 ({count}%)")


def test_exporter():
    """测试Word导出（不实际创建文件）"""
    print("\n" + "=" * 60)
    print("测试导出数据结构")
    print("=" * 60)
    
    generator = ReadingGenerator()
    result = generator.generate_questions(TEST_TEXT_1, num_questions=4, difficulty='medium')
    formatted = generator._generate_reading_exam_output(result)
    
    # 检查必要的字段
    required_fields = ['exam_type', 'title', 'article', 'questions', 'total_questions']
    missing_fields = [f for f in required_fields if f not in formatted]
    
    if missing_fields:
        print(f"❌ 缺少字段: {missing_fields}")
    else:
        print(f"✅ 所有必要字段都存在")
    
    # 检查每个题目的必要字段
    question_required = ['number', 'type', 'question', 'options', 'correct', 'explanation']
    for i, q in enumerate(formatted['questions']):
        missing = [f for f in question_required if f not in q]
        if missing:
            print(f"❌ 第{i+1}题缺少字段: {missing}")
        else:
            print(f"✅ 第{i+1}题字段完整")
    
    print(f"\n导出数据结构预览:")
    print(f"  exam_type: {formatted.get('exam_type')}")
    print(f"  article length: {len(formatted.get('article', ''))} chars")
    print(f"  questions count: {len(formatted.get('questions', []))}")


if __name__ == "__main__":
    print("\n🚀 开始阅读理解模块测试\n")
    
    try:
        test_reading_generator()
        test_convenience_function()
        test_difficulty_levels()
        test_question_type_distribution()
        test_exporter()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
