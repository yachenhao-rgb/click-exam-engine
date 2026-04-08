# -*- coding: utf-8 -*-
"""
题目质量验证模块测试脚本
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_validator():
    """测试验证器功能"""
    print("=" * 60)
    print("测试题目质量验证模块")
    print("=" * 60)
    print()
    
    # 导入验证器
    try:
        from core.question_validator import QuestionValidator
        print("✅ 成功导入 QuestionValidator")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    
    # 创建验证器实例
    try:
        validator = QuestionValidator()
        print("✅ 成功创建验证器实例")
        print(f"   - CEFR 词表加载: {len(validator.cefr_dict)} 个词")
        print(f"   - NLTK 可用: {validator.nltk_available}")
        print()
    except Exception as e:
        print(f"❌ 创建验证器失败: {e}")
        return False
    
    # 测试用例
    test_cases = [
        {
            'name': '测试1: 正常名词题',
            'data': {
                'correct_word': 'success',
                'options': ['success', 'succeed', 'successful', 'successfully'],
                'pos': 'noun',
                'context': 'Hard work and dedication lead to success in life.',
                'position': 6
            },
            'expected': {'min_score': 8, 'should_pass': True}
        },
        {
            'name': '测试2: 动词题',
            'data': {
                'correct_word': 'make',
                'options': ['make', 'take', 'get', 'give'],
                'pos': 'verb',
                'context': 'Make a decision today.',
                'position': 0
            },
            'expected': {'min_score': 8, 'should_pass': True}
        },
        {
            'name': '测试3: 形容词题',
            'data': {
                'correct_word': 'important',
                'options': ['important', 'different', 'difficult', 'interesting'],
                'pos': 'adj',
                'context': 'Education is important for everyone.',
                'position': 2
            },
            'expected': {'min_score': 8, 'should_pass': True}
        },
        {
            'name': '测试4: 挖空专有名词（应该失败）',
            'data': {
                'correct_word': 'John',
                'options': ['John', 'Mary', 'David', 'Sarah'],
                'pos': 'noun',
                'context': 'John is a good student.',
                'position': 0
            },
            'expected': {'min_score': 0, 'should_pass': False}
        },
        {
            'name': '测试5: 挖空数字（应该失败）',
            'data': {
                'correct_word': '2024',
                'options': ['2024', '2023', '2025', '2022'],
                'pos': 'noun',
                'context': 'The year is 2024.',
                'position': 3
            },
            'expected': {'min_score': 0, 'should_pass': False}
        },
        {
            'name': '测试6: 干扰项重复',
            'data': {
                'correct_word': 'happy',
                'options': ['happy', 'glad', 'glad', 'joyful'],
                'pos': 'adj',
                'context': 'She looks very happy today.',
                'position': 3
            },
            'expected': {'min_score': 5, 'should_pass': False}
        },
        {
            'name': '测试7: 干扰项与答案相同',
            'data': {
                'correct_word': 'beautiful',
                'options': ['beautiful', 'beautiful', 'wonderful', 'amazing'],
                'pos': 'adj',
                'context': 'What a beautiful day it is!',
                'position': 2
            },
            'expected': {'min_score': 5, 'should_pass': False}
        },
        {
            'name': '测试8: 干扰项词性不一致',
            'data': {
                'correct_word': 'success',
                'options': ['success', 'succeed', 'successful', 'happily'],
                'pos': 'noun',
                'context': 'Success requires hard work.',
                'position': 0
            },
            'expected': {'min_score': 6, 'should_pass': True}
        }
    ]
    
    print("开始测试...")
    print()
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"【{test_case['name']}】")
        
        try:
            # 执行验证
            result = validator.validate_question(test_case['data'])
            
            # 检查结果
            score = result['score']
            is_valid = result['is_valid']
            
            print(f"   评分: {score}/10")
            print(f"   有效: {'✅' if is_valid else '❌'}")
            
            # 检查是否通过
            if test_case['expected']['should_pass']:
                if is_valid and score >= test_case['expected']['min_score']:
                    print(f"   ✅ 测试通过")
                    passed += 1
                else:
                    print(f"   ⚠️ 预期通过，但未达到标准")
                    failed += 1
            else:
                if not is_valid or score < test_case['expected']['min_score']:
                    print(f"   ✅ 测试通过（预期失败）")
                    passed += 1
                else:
                    print(f"   ⚠️ 预期失败，但通过了")
                    failed += 1
            
            # 显示问题
            if result['issues']:
                print(f"   问题:")
                for issue in result['issues']:
                    print(f"      - {issue}")
            
            # 显示警告
            if result['warnings']:
                print(f"   警告:")
                for warning in result['warnings']:
                    print(f"      - {warning}")
            
        except Exception as e:
            print(f"   ❌ 测试出错: {e}")
            failed += 1
        
        print()
    
    # 测试批量验证
    print("=" * 60)
    print("测试批量验证")
    print("=" * 60)
    print()
    
    try:
        questions = [tc['data'] for tc in test_cases[:5]]
        batch_result = validator.validate_batch(questions)
        
        print(f"总题目数: {batch_result['total_questions']}")
        print(f"有效题目: {batch_result['valid_count']}")
        print(f"无效题目: {batch_result['invalid_count']}")
        print(f"平均得分: {batch_result['average_score']:.1f}")
        print()
        
        # 生成报告
        report = validator.generate_validation_report(batch_result)
        print("验证报告:")
        print(report)
        
    except Exception as e:
        print(f"批量验证失败: {e}")
    
    # 测试与出题引擎集成
    print()
    print("=" * 60)
    print("测试与出题引擎集成")
    print("=" * 60)
    print()
    
    try:
        from core.exam_generator import ExamGenerator
        generator = ExamGenerator()
        print("✅ 成功导入 ExamGenerator")
        
        # 生成测试题目
        test_text = """
        Success is not final, failure is not fatal. 
        It is the courage to continue that counts. 
        Education is the most powerful weapon which you can use to change the world.
        Make your dreams come true through hard work and dedication.
        A good beginning makes a good ending.
        """
        
        print("正在生成题目...")
        result = generator.generate_exam(test_text, num_blanks=5)
        
        if 'error' in result:
            print(f"❌ 生成失败: {result['error']}")
        else:
            print(f"✅ 成功生成 {result['total_blanks']} 道题目")
            print(f"   整体质量评分: {result.get('overall_score', 'N/A')}/10")
            print()
            
            # 显示每道题的质量评分
            print("各题质量评分:")
            for q in result['questions']:
                score = q.get('quality_score', 'N/A')
                is_valid = q.get('validation', {}).get('is_valid', True)
                status = '✅' if is_valid else '❌'
                print(f"   第{q['number']}题: {score}/10 {status}")
                
                # 显示问题
                if q.get('validation', {}).get('issues'):
                    for issue in q['validation']['issues']:
                        print(f"      - {issue}")
            
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 总结
    print()
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"通过: {passed}/{passed + failed}")
    print(f"失败: {failed}/{passed + failed}")
    print()
    
    if failed == 0:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查上述输出")
    
    return failed == 0

if __name__ == "__main__":
    success = test_validator()
    sys.exit(0 if success else 1)
