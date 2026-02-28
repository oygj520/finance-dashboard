# 💰 Finance Dashboard - 个人财务仪表盘

一个轻量级的个人财务管理桌面应用，支持导入微信账单 CSV 文件，自动生成可视化图表分析。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ 功能特性

### 📥 账单导入
- 支持拖拽上传微信账单 CSV 文件
- 自动解析 CSV 格式
- 智能数据去重（避免重复导入）
- 导入历史记录查看

### 📊 数据统计
- 按分类统计（餐饮、交通、购物、娱乐等）
- 按月/年汇总
- 收入 vs 支出对比
- 自动识别交易类型并分类

### 📈 图表展示
- 🥧 饼图：分类支出占比
- 📊 柱状图：月度支出趋势
- 📉 折线图：收入/支出对比趋势
- 📋 今日/本月/本年概览卡片

---

## 🚀 快速开始

### 方法一：直接运行（开发模式）

1. **安装 Python 3.8+**
   ```bash
   # 验证 Python 版本
   python --version
   ```

2. **安装依赖**
   ```bash
   cd E:\openclaw-projects\finance-dashboard
   pip install -r requirements.txt
   ```

3. **运行应用**
   ```bash
   python backend/main.py
   ```

4. **访问应用**
   - 应用会自动打开浏览器窗口
   - 或访问 http://localhost:端口

### 方法二：打包成 EXE（生产模式）

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **打包应用**
   ```bash
   python build.py
   ```

3. **运行可执行文件**
   ```
   dist/FinanceDashboard.exe
   ```

---

## 📁 项目结构

```
finance-dashboard/
├── backend/
│   ├── main.py          # 主程序入口（Eel 应用）
│   ├── importer.py      # CSV 导入解析模块
│   ├── analyzer.py      # 数据统计分析模块
│   └── database.py      # SQLite 数据库操作模块
├── frontend/
│   ├── index.html       # 主页面
│   ├── css/
│   │   └── style.css    # 样式文件
│   └── js/
│       └── app.js       # Vue 3 应用
├── data/
│   └── finance.db       # SQLite 数据库（自动生成）
├── build.py             # 打包脚本
├── requirements.txt     # Python 依赖
└── README.md            # 本文件
```

---

## 📝 使用说明

### 导入微信账单

1. **导出微信账单**
   - 打开微信 → 我 → 服务 → 钱包 → 账单
   - 点击右上角「常见问题」→「下载账单」
   - 选择「用于个人对账」
   - 选择时间范围，输入邮箱
   - 微信会将 CSV 文件发送到你的邮箱

2. **导入到应用**
   - 点击应用右上角「📥 导入账单」
   - 拖拽 CSV 文件到上传区域，或点击选择文件
   - 等待导入完成

3. **查看数据**
   - 概览卡片显示今日/本月/本年收支
   - 图表区展示分类占比和趋势
   - 底部显示最近交易记录

### 数据管理

- **数据存储位置**: `data/finance.db`
- **数据格式**: SQLite 数据库
- **数据安全**: 所有数据本地存储，不上传云端
- **数据备份**: 定期备份 `data/finance.db` 文件

---

## 🔧 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 后端 | Python 3.8+ | 核心逻辑 |
| 前端框架 | Vue 3 | 响应式 UI |
| 图表库 | ECharts 5 | 数据可视化 |
| Web 框架 | Eel | Python + Web 桥接 |
| 数据库 | SQLite | 本地存储 |
| 数据处理 | Pandas | CSV 解析 |
| 打包工具 | PyInstaller | EXE 打包 |

---

## 📋 微信 CSV 格式参考

```csv
交易时间，交易类型，交易金额，账户类型，对方账号，商品说明
2026-02-28 14:30:00，消费，-25.00，零钱，美团外卖，餐饮
2026-02-28 10:15:00，收入，+500.00，零钱，转账，工资
```

应用支持自动识别以下分类关键词：
- 🍔 餐饮：外卖、美团、饿了么、肯德基、麦当劳等
- 🚗 交通：地铁、公交、打车、滴滴、加油等
- 🛒 购物：淘宝、京东、超市、便利店等
- 🎬 娱乐：电影、KTV、游戏、视频会员等
- 🏥 医疗：医院、药店、药品等
- 📚 教育：培训、学校、课程、书籍等
- 🏠 居住：房租、物业、水电、燃气等
- 📱 通讯：话费、流量、手机充值等
- 🧧 人情：红包、礼物、转账等
- 💰 金融：保险、理财、基金、银行等

---

## ⚠️ 注意事项

1. **首次运行**: 首次运行会自动创建数据库文件
2. **数据去重**: 相同时间、金额、描述的交易会自动去重
3. **文件格式**: 仅支持微信账单 CSV 格式
4. **编码格式**: 支持 UTF-8 和 UTF-8-sig 编码
5. **数据备份**: 建议定期备份 `data/finance.db` 文件

---

## 🛠️ 常见问题

### Q: 导入失败怎么办？
A: 检查 CSV 文件格式是否正确，确保是微信导出的账单格式。

### Q: 分类不准确怎么办？
A: 可以在 `backend/importer.py` 中的 `CATEGORY_KEYWORDS` 添加更多关键词。

### Q: 如何清空所有数据？
A: 删除 `data/finance.db` 文件，重启应用会自动创建新数据库。

### Q: 打包后文件太大？
A: PyInstaller 打包会包含 Python 运行时，文件较大是正常的。可以使用 UPX 压缩。

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [ECharts](https://echarts.apache.org/) - 强大的可视化图表库
- [Eel](https://github.com/ChrisKnott/Eel) - Python 桌面应用框架
- [PyInstaller](https://www.pyinstaller.org/) - Python 打包工具

---

**开发时间**: 2026 年  
**版本**: 1.0.0 (第一期)
