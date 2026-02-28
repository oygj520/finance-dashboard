"""
Finance Dashboard - 打包脚本
使用 PyInstaller 打包成 Windows 可执行文件
"""

import os
import sys
import shutil
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
BUILD_DIR = PROJECT_ROOT / 'build'
DIST_DIR = PROJECT_ROOT / 'dist'

def clean_build():
    """清理旧的构建文件"""
    print("🧹 清理旧的构建文件...")
    
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print(f"  已删除：{BUILD_DIR}")
    
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
        print(f"  已删除：{DIST_DIR}")
    
    spec_file = PROJECT_ROOT / 'finance_dashboard.spec'
    if spec_file.exists():
        spec_file.unlink()
        print(f"  已删除：{spec_file}")

def build_exe():
    """构建可执行文件"""
    print("\n📦 开始打包...")
    
    # PyInstaller 命令
    cmd = f'''
    pyinstaller --noconfirm --onefile --windowed ^
    --name "FinanceDashboard" ^
    --add-data "frontend;frontend" ^
    --add-data "data;data" ^
    --icon="NONE" ^
    --hidden-import=eel ^
    --hidden-import=pandas ^
    backend/main.py
    '''
    
    os.system(cmd)

def post_build():
    """构建后处理"""
    print("\n✅ 打包完成！")
    
    exe_path = DIST_DIR / 'FinanceDashboard.exe'
    if exe_path.exists():
        print(f"\n📍 可执行文件位置：{exe_path}")
        print(f"📊 文件大小：{exe_path.stat().st_size / 1024 / 1024:.2f} MB")
    else:
        print("\n❌ 打包失败，未找到可执行文件")

def main():
    """主函数"""
    print("=" * 60)
    print("  Finance Dashboard - 打包工具")
    print("=" * 60)
    
    # 检查依赖
    try:
        import eel
        import pandas
        import PyInstaller
        print("\n✅ 依赖检查通过")
    except ImportError as e:
        print(f"\n❌ 缺少依赖：{e}")
        print("请先运行：pip install -r requirements.txt")
        return
    
    # 清理
    clean_build()
    
    # 构建
    build_exe()
    
    # 后处理
    post_build()
    
    print("\n" + "=" * 60)
    print("  使用说明:")
    print("  1. 运行 FinanceDashboard.exe 启动应用")
    print("  2. 点击「导入账单」上传微信账单 CSV")
    print("  3. 数据存储在 data/finance.db")
    print("=" * 60)

if __name__ == '__main__':
    main()
