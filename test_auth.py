#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试用户认证功能"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试导入"""
    print('1. 测试依赖导入...')
    from flask import Flask
    from flask_login import LoginManager
    print('   Flask 和 Flask-Login 导入成功')

def test_models():
    """测试模型"""
    print('2. 测试用户模型...')
    from models.user import User, UserHistory
    
    # 测试用户创建
    success, msg, user = User.create('data/knowledge_base.db', 'testuser', 'test@test.com', 'password123')
    print(f'   创建用户: {success}, {msg}')
    
    # 测试密码验证
    if user:
        print(f'   密码验证: {user.check_password("password123")}')
        print(f'   错误密码: {user.check_password("wrong")}')
        
        # 获取用户
        fetched = User.get_by_username('data/knowledge_base.db', 'testuser')
        print(f'   获取用户: {fetched is not None}')
        
        # 测试历史记录
        UserHistory.create(
            'data/knowledge_base.db',
            user.id,
            'test-task-001',
            'cloze',
            'medium',
            10,
            'Test text content...'
        )
        history = UserHistory.get_by_user('data/knowledge_base.db', user.id)
        print(f'   历史记录: {len(history)} 条')
        
        # 清理测试用户
        import sqlite3
        conn = sqlite3.connect('data/knowledge_base.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', ('testuser',))
        conn.commit()
        conn.close()
        print('   清理测试用户完成')

def test_app():
    """测试应用创建"""
    print('3. 测试Flask应用...')
    from app import app
    print(f'   应用创建成功，路由数量: {len(app.url_map._rules)}')

if __name__ == '__main__':
    print('=' * 50)
    print('开始测试用户认证功能')
    print('=' * 50)
    
    try:
        test_imports()
        test_models()
        test_app()
        print('=' * 50)
        print('所有测试通过!')
        print('=' * 50)
    except Exception as e:
        print(f'测试失败: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
