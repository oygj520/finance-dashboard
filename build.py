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
    print("[CLEAN] 清理旧的构建文件...")
    
    if BUILD_DIR.exists():
        try:
            shutil.rmtree(BUILD_DIR)
            print(f"  已删除：{BUILD_DIR}")
        except Exception as e:
            print(f"  警告：无法删除 {BUILD_DIR} - {e}")
    
    if DIST_DIR.exists():
        try:
            shutil.rmtree(DIST_DIR)
            print(f"  已删除：{DIST_DIR}")
        except Exception as e:
            print(f"  警告：无法删除 {DIST_DIR} - {e}")
    
    spec_file = PROJECT_ROOT / 'FinanceDashboard.spec'
    if spec_file.exists():
        try:
            spec_file.unlink()
            print(f"  已删除：{spec_file}")
        except Exception as e:
            print(f"  警告：无法删除 {spec_file} - {e}")

def build_exe():
    """构建可执行文件"""
    print("\n[BUILD] 开始打包...")
    
    # 使用 subprocess 运行 PyInstaller
    import subprocess
    
    python_exe = sys.executable
    args = [
        python_exe, '-m', 'PyInstaller',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--name', 'FinanceDashboard',
        '--add-data', 'frontend;frontend',
        '--add-data', 'data;data',
        '--icon=NONE',
        '--hidden-import=eel',
        '--hidden-import=bottle',
        '--hidden-import=bottle_websocket',
        '--hidden-import=gevent',
        '--hidden-import=geventwebsocket',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=setuptools',
        '--hidden-import=pkg_resources',
        '--collect-all', 'eel',
        '--collect-all', 'bottle',
        '--collect-all', 'setuptools',
        'backend/main.py'
    ]
    
    subprocess.run(args, cwd=PROJECT_ROOT)

def post_build():
    """构建后处理"""
    print("\n[SUCCESS] 打包完成！")
    
    exe_path = DIST_DIR / 'FinanceDashboard.exe'
    if exe_path.exists():
        print(f"\n[INFO] 可执行文件位置：{exe_path}")
        print(f"[INFO] 文件大小：{exe_path.stat().st_size / 1024 / 1024:.2f} MB")
    else:
        print("\n[ERROR] 打包失败，未找到可执行文件")

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
        print("\n[OK] 依赖检查通过")
    except ImportError as e:
        print(f"\n[ERROR] 缺少依赖：{e}")
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
