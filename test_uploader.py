# -*- coding: utf-8 -*-
"""
文件上传功能测试脚本
"""

import os
import sys

# 测试OCR功能（需要安装pytesseract和Pillow）
def test_ocr():
    """测试图片OCR识别"""
    print("=" * 50)
    print("测试图片OCR识别")
    print("=" * 50)
    
    try:
        from PIL import Image
        import pytesseract
        
        # 检查Tesseract是否可用
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✓ Tesseract版本: {version}")
        except Exception as e:
            print(f"✗ Tesseract未正确安装: {e}")
            print("  提示：请安装Tesseract OCR引擎")
            return False
        
        # 测试简单图像识别
        print("\n正在测试OCR功能...")
        
        # 创建一个简单的测试图片
        from PIL import Image, ImageDraw, ImageFont
        
        test_img = Image.new('RGB', (300, 50), color='white')
        draw = ImageDraw.Draw(test_img)
        draw.text((10, 10), "Hello World Test", fill='black')
        
        # 保存测试图片
        test_path = 'test_ocr.png'
        test_img.save(test_path)
        
        # 识别
        text = pytesseract.image_to_string(test_img)
        print(f"✓ OCR识别成功: '{text.strip()}'")
        
        # 清理测试文件
        os.remove(test_path)
        
        return True
        
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("  提示：请运行: pip install pytesseract Pillow")
        return False
    except Exception as e:
        print(f"✗ OCR测试失败: {e}")
        return False


# 测试PDF解析功能
def test_pdf():
    """测试PDF文本提取"""
    print("\n" + "=" * 50)
    print("测试PDF文本解析")
    print("=" * 50)
    
    try:
        import pdfplumber
        print("✓ pdfplumber已安装")
        
        # 检查是否有测试PDF
        test_pdf = 'test.pdf'
        if os.path.exists(test_pdf):
            with pdfplumber.open(test_pdf) as pdf:
                print(f"✓ PDF页数: {len(pdf.pages)}")
        else:
            print("✓ pdfplumber可用（无测试PDF，跳过实际解析）")
        
        return True
        
    except ImportError:
        print("✗ pdfplumber未安装")
        print("  提示：请运行: pip install pdfplumber")
        return False
    except Exception as e:
        print(f"✗ PDF测试失败: {e}")
        return False


# 测试DOCX解析功能
def test_docx():
    """测试DOCX文本提取"""
    print("\n" + "=" * 50)
    print("测试DOCX文本解析")
    print("=" * 50)
    
    try:
        from docx import Document
        print("✓ python-docx已安装")
        return True
        
    except ImportError:
        print("✗ python-docx未安装")
        print("  提示：请运行: pip install python-docx")
        return False
    except Exception as e:
        print(f"✗ DOCX测试失败: {e}")
        return False


# 测试上传模块
def test_uploader_module():
    """测试uploader模块"""
    print("\n" + "=" * 50)
    print("测试uploader模块")
    print("=" * 50)
    
    try:
        from core.uploader import clean_text, validate_file, get_file_info
        print("✓ uploader模块导入成功")
        
        # 测试clean_text函数
        dirty_text = "  Hello   World  \n\n\n  Test  "
        clean = clean_text(dirty_text)
        assert "Hello World" in clean and "Test" in clean
        print("✓ clean_text函数正常")
        
        return True
        
    except ImportError as e:
        print(f"✗ uploader模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"✗ uploader测试失败: {e}")
        return False


# 测试Flask API
def test_flask_api():
    """测试Flask应用启动"""
    print("\n" + "=" * 50)
    print("测试Flask应用")
    print("=" * 50)
    
    try:
        from app import app
        print("✓ Flask应用加载成功")
        print(f"  上传API路由: /api/upload/image, /api/upload/file")
        
        # 检查路由是否存在
        rules = [str(rule) for rule in app.url_map.iter_rules()]
        if '/api/upload/image' in rules:
            print("✓ /api/upload/image 路由已注册")
        if '/api/upload/file' in rules:
            print("✓ /api/upload/file 路由已注册")
        
        return True
        
    except ImportError as e:
        print(f"✗ Flask应用加载失败: {e}")
        return False
    except Exception as e:
        print(f"✗ Flask测试失败: {e}")
        return False


# 主函数
def main():
    print("\n" + "=" * 60)
    print("  文件上传功能测试")
    print("=" * 60 + "\n")
    
    results = {
        'OCR识别': test_ocr(),
        'PDF解析': test_pdf(),
        'DOCX解析': test_docx(),
        'uploader模块': test_uploader_module(),
        'Flask应用': test_flask_api(),
    }
    
    print("\n" + "=" * 60)
    print("  测试结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results.items():
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "-" * 60)
    if all_passed:
        print("  🎉 所有测试通过！")
    else:
        print("  ⚠️  部分测试失败，请安装缺失的依赖")
    print("-" * 60 + "\n")


if __name__ == '__main__':
    main()
