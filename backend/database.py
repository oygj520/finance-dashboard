"""
SQLite 数据库操作模块
负责财务数据的存储和查询
"""

import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'finance.db')

def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 创建交易记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_time TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            account_type TEXT,
            counterparty TEXT,
            description TEXT,
            category TEXT,
            income_or_expense TEXT NOT NULL,
            imported_at TEXT NOT NULL,
            UNIQUE(transaction_time, amount, description)
        )
    ''')
    
    # 创建导入历史表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS import_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            import_time TEXT NOT NULL,
            record_count INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_transaction(transaction):
    """添加单条交易记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO transactions 
            (transaction_time, transaction_type, amount, account_type, counterparty, description, category, income_or_expense, imported_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction['transaction_time'],
            transaction['transaction_type'],
            transaction['amount'],
            transaction.get('account_type', ''),
            transaction.get('counterparty', ''),
            transaction.get('description', ''),
            transaction.get('category', '未分类'),
            transaction['income_or_expense'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def add_transactions(transactions):
    """批量添加交易记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    added_count = 0
    for transaction in transactions:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO transactions 
                (transaction_time, transaction_type, amount, account_type, counterparty, description, category, income_or_expense, imported_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                transaction['transaction_time'],
                transaction['transaction_type'],
                transaction['amount'],
                transaction.get('account_type', ''),
                transaction.get('counterparty', ''),
                transaction.get('description', ''),
                transaction.get('category', '未分类'),
                transaction['income_or_expense'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            if cursor.rowcount > 0:
                added_count += 1
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    return added_count

def add_import_history(filename, record_count):
    """添加导入历史记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO import_history (filename, import_time, record_count)
        VALUES (?, ?, ?)
    ''', (filename, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), record_count))
    
    conn.commit()
    conn.close()

def get_import_history():
    """获取导入历史记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT filename, import_time, record_count 
        FROM import_history 
        ORDER BY import_time DESC
        LIMIT 50
    ''')
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def get_all_transactions():
    """获取所有交易记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM transactions ORDER BY transaction_time DESC')
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def get_transactions_by_month(year_month):
    """获取指定月份的交易记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM transactions 
        WHERE transaction_time LIKE ?
        ORDER BY transaction_time DESC
    ''', (f'{year_month}%',))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def get_category_stats(start_date=None, end_date=None):
    """获取分类统计"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT category, SUM(amount) as total, COUNT(*) as count
        FROM transactions 
        WHERE income_or_expense = '支出'
    '''
    params = []
    
    if start_date and end_date:
        query += ' AND transaction_time BETWEEN ? AND ?'
        params.extend([start_date, end_date])
    
    query += ' GROUP BY category ORDER BY total DESC'
    
    cursor.execute(query, params)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def get_monthly_stats(year=None):
    """获取月度统计"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            strftime('%Y-%m', transaction_time) as month,
            SUM(CASE WHEN income_or_expense = '收入' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN income_or_expense = '支出' THEN ABS(amount) ELSE 0 END) as expense
        FROM transactions
    '''
    params = []
    
    if year:
        query += " WHERE strftime('%Y', transaction_time) = ?"
        params.append(str(year))
    
    query += ' GROUP BY month ORDER BY month'
    
    cursor.execute(query, params)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def get_summary():
    """获取概览数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    this_month = datetime.now().strftime('%Y-%m')
    this_year = datetime.now().strftime('%Y')
    
    # 今日统计
    cursor.execute('''
        SELECT 
            SUM(CASE WHEN income_or_expense = '收入' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN income_or_expense = '支出' THEN ABS(amount) ELSE 0 END) as expense
        FROM transactions 
        WHERE transaction_time LIKE ?
    ''', (f'{today}%',))
    today_stats = dict(cursor.fetchone())
    
    # 本月统计
    cursor.execute('''
        SELECT 
            SUM(CASE WHEN income_or_expense = '收入' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN income_or_expense = '支出' THEN ABS(amount) ELSE 0 END) as expense
        FROM transactions 
        WHERE transaction_time LIKE ?
    ''', (f'{this_month}%',))
    month_stats = dict(cursor.fetchone())
    
    # 本年统计
    cursor.execute('''
        SELECT 
            SUM(CASE WHEN income_or_expense = '收入' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN income_or_expense = '支出' THEN ABS(amount) ELSE 0 END) as expense
        FROM transactions 
        WHERE transaction_time LIKE ?
    ''', (f'{this_year}%',))
    year_stats = dict(cursor.fetchone())
    
    conn.close()
    
    return {
        'today': {
            'income': today_stats.get('income', 0) or 0,
            'expense': today_stats.get('expense', 0) or 0
        },
        'month': {
            'income': month_stats.get('income', 0) or 0,
            'expense': month_stats.get('expense', 0) or 0
        },
        'year': {
            'income': year_stats.get('income', 0) or 0,
            'expense': year_stats.get('expense', 0) or 0
        }
    }

def get_transaction_count():
    """获取交易记录总数"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM transactions')
    result = cursor.fetchone()
    conn.close()
    
    return result['count'] if result else 0
