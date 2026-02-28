"""
CSV 导入解析模块
负责解析微信账单 CSV 文件并自动分类
"""

import csv
import re
from datetime import datetime

# 分类关键词映射
CATEGORY_KEYWORDS = {
    '餐饮': ['餐饮', '外卖', '美团', '饿了么', '肯德基', '麦当劳', '星巴克', '咖啡', '餐厅', '小吃', '奶茶', '烧烤', '火锅'],
    '交通': ['交通', '地铁', '公交', '打车', '滴滴', '出租车', '加油', '停车', '火车', '飞机', '高铁', '共享单车'],
    '购物': ['购物', '淘宝', '京东', '拼多多', '超市', '便利店', '商场', '服装', '鞋子', '化妆品', '数码', '电器'],
    '娱乐': ['娱乐', '电影', 'KTV', '游戏', '视频', '音乐', '会员', '直播', '演出', '门票'],
    '医疗': ['医疗', '医院', '药店', '药品', '体检', '诊所'],
    '教育': ['教育', '培训', '学校', '课程', '书籍', '学习'],
    '居住': ['居住', '房租', '物业', '水电', '燃气', '宽带', '装修', '家居'],
    '通讯': ['通讯', '话费', '流量', '手机', '充值'],
    '人情': ['人情', '红包', '礼物', '转账', '借款', '还款'],
    '金融': ['金融', '保险', '理财', '基金', '股票', '银行', '利息', '手续费'],
    '其他': ['其他']
}

def parse_csv(file_path):
    """
    解析微信账单 CSV 文件
    返回交易记录列表
    """
    transactions = []
    
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            # 尝试检测 CSV 格式
            sample = f.read(2048)
            f.seek(0)
            
            # 检测分隔符
            try:
                dialect = csv.Sniffer().sniff(sample)
            except csv.Error:
                dialect = csv.excel
            
            reader = csv.reader(f, dialect)
            
            # 读取表头
            headers = None
            for row in reader:
                if row and any(h in str(row[0]) for h in ['交易时间', '交易类型', '交易金额']):
                    headers = row
                    break
            
            if not headers:
                # 尝试直接解析
                f.seek(0)
                reader = csv.reader(f)
                headers = next(reader, None)
            
            if not headers:
                return {'success': False, 'error': '无法识别 CSV 格式', 'transactions': []}
            
            # 解析每一行
            for row in reader:
                if not row or len(row) < 3:
                    continue
                
                try:
                    transaction = parse_row(row, headers)
                    if transaction:
                        transactions.append(transaction)
                except Exception as e:
                    continue
    
    except Exception as e:
        return {'success': False, 'error': str(e), 'transactions': []}
    
    return {'success': True, 'error': None, 'transactions': transactions}

def parse_row(row, headers):
    """
    解析单行 CSV 数据
    """
    try:
        # 创建字段映射
        row_dict = {}
        for i, header in enumerate(headers):
            if i < len(row):
                row_dict[header.strip()] = row[i].strip() if row[i] else ''
        
        # 提取必要字段
        transaction_time = row_dict.get('交易时间', '')
        transaction_type = row_dict.get('交易类型', '')
        amount_str = row_dict.get('交易金额', '0')
        account_type = row_dict.get('账户类型', '')
        counterparty = row_dict.get('对方账号', '')
        description = row_dict.get('商品说明', '')
        
        # 如果没有商品说明，尝试从其他字段获取
        if not description and len(row) > 5:
            description = row[5] if len(row) > 5 else ''
        
        # 解析金额
        amount = parse_amount(amount_str)
        if amount == 0:
            return None
        
        # 确定收入/支出
        income_or_expense = '支出' if amount < 0 else '收入'
        amount = abs(amount) if income_or_expense == '支出' else amount
        
        # 自动分类
        category = auto_categorize(transaction_type, description, counterparty)
        
        return {
            'transaction_time': transaction_time,
            'transaction_type': transaction_type,
            'amount': amount,
            'account_type': account_type,
            'counterparty': counterparty,
            'description': description,
            'category': category,
            'income_or_expense': income_or_expense
        }
    
    except Exception as e:
        return None

def parse_amount(amount_str):
    """
    解析金额字符串
    支持格式：-25.00, +500.00, 25.00 等
    """
    try:
        # 移除空格和货币符号
        amount_str = str(amount_str).strip().replace('¥', '').replace('￥', '').replace(',', '')
        
        # 处理 + 号
        if amount_str.startswith('+'):
            amount_str = amount_str[1:]
        
        return float(amount_str)
    except:
        return 0.0

def auto_categorize(transaction_type, description, counterparty):
    """
    自动识别交易分类
    """
    text = f"{transaction_type} {description} {counterparty}".lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return category
    
    # 根据交易类型判断
    if '收入' in transaction_type or '转账' in transaction_type:
        return '人情' if '转账' in text else '金融'
    
    return '其他'

def validate_csv(file_path):
    """
    验证 CSV 文件格式
    """
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read(1024)
            return '交易时间' in content or '交易金额' in content
    except:
        return False
