"""
数据统计分析模块
负责财务数据的统计和分析
"""

from datetime import datetime
from backend.database import (
    get_category_stats,
    get_monthly_stats,
    get_summary,
    get_all_transactions,
    get_transaction_count
)

def analyze_data():
    """
    执行完整的数据分析
    返回分析结果
    """
    # 获取概览数据
    summary = get_summary()
    
    # 获取分类统计
    category_stats = get_category_stats()
    
    # 获取月度统计
    monthly_stats = get_monthly_stats()
    
    # 获取交易总数
    total_count = get_transaction_count()
    
    # 计算总收入和总支出
    total_income = summary['year']['income']
    total_expense = summary['year']['expense']
    
    # 计算结余
    balance = total_income - total_expense
    
    # 计算月度平均支出
    avg_monthly_expense = total_expense / 12 if total_expense > 0 else 0
    
    return {
        'summary': summary,
        'category_stats': category_stats,
        'monthly_stats': monthly_stats,
        'total_count': total_count,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'avg_monthly_expense': avg_monthly_expense
    }

def get_category_chart_data():
    """
    获取饼图数据（分类支出占比）
    """
    category_stats = get_category_stats()
    
    chart_data = {
        'categories': [],
        'values': [],
        'percentages': []
    }
    
    total = sum(item['total'] for item in category_stats)
    
    for item in category_stats:
        chart_data['categories'].append(item['category'])
        chart_data['values'].append(round(item['total'], 2))
        percentage = round((item['total'] / total * 100), 2) if total > 0 else 0
        chart_data['percentages'].append(percentage)
    
    return chart_data

def get_monthly_chart_data():
    """
    获取柱状图数据（月度支出趋势）
    """
    monthly_stats = get_monthly_stats()
    
    chart_data = {
        'months': [],
        'income': [],
        'expense': []
    }
    
    for item in monthly_stats:
        chart_data['months'].append(item['month'])
        chart_data['income'].append(round(item['income'], 2))
        chart_data['expense'].append(round(item['expense'], 2))
    
    return chart_data

def get_trend_chart_data():
    """
    获取折线图数据（收入/支出对比趋势）
    """
    monthly_stats = get_monthly_stats()
    
    chart_data = {
        'months': [],
        'income': [],
        'expense': [],
        'balance': []
    }
    
    for item in monthly_stats:
        chart_data['months'].append(item['month'])
        chart_data['income'].append(round(item['income'], 2))
        chart_data['expense'].append(round(item['expense'], 2))
        chart_data['balance'].append(round(item['income'] - item['expense'], 2))
    
    return chart_data

def get_recent_transactions(limit=10):
    """
    获取最近的交易记录
    """
    all_transactions = get_all_transactions()
    return all_transactions[:limit]

def get_statistics_by_date_range(start_date, end_date):
    """
    获取指定日期范围的统计数据
    """
    category_stats = get_category_stats(start_date, end_date)
    
    total_income = 0
    total_expense = 0
    transaction_count = 0
    
    for item in category_stats:
        total_expense += item['total']
        transaction_count += item['count']
    
    return {
        'start_date': start_date,
        'end_date': end_date,
        'total_income': total_income,
        'total_expense': round(total_expense, 2),
        'transaction_count': transaction_count,
        'category_stats': category_stats
    }
