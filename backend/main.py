"""
Finance Dashboard - 个人财务仪表盘
主程序入口
使用 Eel 框架实现 Python 后端 + Web 前端
"""

import eel
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 导入后端模块
from backend.database import (
    init_db,
    add_transactions,
    add_import_history,
    get_import_history,
    get_all_transactions,
    get_summary,
    get_transaction_count
)
from backend.importer import parse_csv, validate_csv
from backend.analyzer import (
    analyze_data,
    get_category_chart_data,
    get_monthly_chart_data,
    get_trend_chart_data,
    get_recent_transactions
)

# 初始化 Eel
eel.init('frontend')

# 确保数据目录存在
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

@eel.expose
def initialize_app():
    """初始化应用"""
    init_db()
    return {
        'success': True,
        'message': '应用初始化成功',
        'transaction_count': get_transaction_count()
    }

@eel.expose
def import_csv(file_path):
    """
    导入 CSV 文件
    """
    try:
        # 验证文件
        if not os.path.exists(file_path):
            return {'success': False, 'error': '文件不存在'}
        
        if not validate_csv(file_path):
            return {'success': False, 'error': '无效的微信账单格式'}
        
        # 解析 CSV
        result = parse_csv(file_path)
        
        if not result['success']:
            return {'success': False, 'error': result['error']}
        
        transactions = result['transactions']
        
        if not transactions:
            return {'success': False, 'error': '未找到有效交易记录'}
        
        # 添加到数据库
        added_count = add_transactions(transactions)
        
        # 记录导入历史
        filename = os.path.basename(file_path)
        add_import_history(filename, added_count)
        
        return {
            'success': True,
            'message': f'成功导入 {added_count} 条记录',
            'total': len(transactions),
            'added': added_count,
            'duplicates': len(transactions) - added_count
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}

@eel.expose
def get_dashboard_data():
    """
    获取仪表盘数据
    """
    try:
        summary = get_summary()
        chart_data = {
            'category': get_category_chart_data(),
            'monthly': get_monthly_chart_data(),
            'trend': get_trend_chart_data()
        }
        recent = get_recent_transactions(10)
        total_count = get_transaction_count()
        
        return {
            'success': True,
            'summary': summary,
            'charts': chart_data,
            'recent_transactions': recent,
            'total_count': total_count
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

@eel.expose
def get_import_history():
    """
    获取导入历史记录
    """
    try:
        history = get_import_history()
        return {'success': True, 'history': history}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@eel.expose
def get_all_data():
    """
    获取所有交易数据
    """
    try:
        transactions = get_all_transactions()
        return {'success': True, 'transactions': transactions}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@eel.expose
def refresh_data():
    """
    刷新数据
    """
    return get_dashboard_data()

def main():
    """主函数"""
    # 初始化数据库
    init_db()
    
    # 获取前端目录
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    
    # 启动 Eel 应用
    print("启动 Finance Dashboard...")
    print(f"前端目录：{frontend_dir}")
    
    # 设置窗口大小
    eel.start('index.html', size=(1200, 800), port=0)

if __name__ == '__main__':
    main()
