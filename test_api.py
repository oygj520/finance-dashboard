import sys
sys.path.insert(0, r'E:\openclaw-projects\finance-dashboard')

from backend.main import get_dashboard_data
import json

print('=== 测试后端数据接口 ===\n')

result = get_dashboard_data()

print('返回结果:')
print(json.dumps(result, indent=2, ensure_ascii=False))

if result['success']:
    print('\n✓ 数据格式检查:')
    charts = result['charts']
    
    print(f"  分类图表 - categories: {len(charts['category']['categories'])} 项")
    print(f"  分类图表 - values: {len(charts['category']['values'])} 项")
    print(f"  月度图表 - months: {len(charts['monthly']['months'])} 项")
    print(f"  趋势图表 - months: {len(charts['trend']['months'])} 项")
    
    if len(charts['category']['categories']) > 0:
        print(f"\n  分类数据示例:")
        for i, cat in enumerate(charts['category']['categories'][:3]):
            print(f"    {cat}: ¥{charts['category']['values'][i]} ({charts['category']['percentages'][i]}%)")
else:
    print(f"\n✗ 数据获取失败：{result['error']}")
