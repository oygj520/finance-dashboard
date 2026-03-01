/**
 * Finance Dashboard - Vue 3 应用
 */

const { createApp, ref, reactive, onMounted, nextTick } = Vue;

createApp({
    setup() {
        // 响应式数据
        const loading = ref(true);
        const showImportModal = ref(false);
        const isDragOver = ref(false);
        const importStatus = ref(null);
        const importHistory = ref([]);
        
        const summary = reactive({
            today: { income: 0, expense: 0 },
            month: { income: 0, expense: 0 },
            year: { income: 0, expense: 0 }
        });
        
        const charts = reactive({
            category: { categories: [], values: [], percentages: [] },
            monthly: { months: [], income: [], expense: [] },
            trend: { months: [], income: [], expense: [], balance: [] }
        });
        
        const recent_transactions = ref([]);
        const total_count = ref(0);
        
        // 图表实例
        let categoryChart = null;
        let monthlyChart = null;
        let trendChart = null;
        
        // 图表 DOM 引用
        const categoryChartRef = ref(null);
        const monthlyChartRef = ref(null);
        const trendChartRef = ref(null);
        
        // 初始化应用
        async function initApp() {
            try {
                const result = await eel.initialize_app()();
                console.log('应用初始化:', result);
                await loadDashboardData();
                await loadImportHistory();
            } catch (error) {
                console.error('初始化失败:', error);
            } finally {
                loading.value = false;
            }
        }
        
        // 加载仪表盘数据
        async function loadDashboardData() {
            try {
                console.log('开始加载仪表盘数据...');
                const result = await eel.get_dashboard_data()();
                
                if (result.success) {
                    console.log('数据加载成功:', result);
                    // 更新概览数据
                    summary.today.income = result.summary.today.income;
                    summary.today.expense = result.summary.today.expense;
                    summary.month.income = result.summary.month.income;
                    summary.month.expense = result.summary.month.expense;
                    summary.year.income = result.summary.year.income;
                    summary.year.expense = result.summary.year.expense;
                    
                    // 更新图表数据
                    Object.assign(charts.category, result.charts.category);
                    Object.assign(charts.monthly, result.charts.monthly);
                    Object.assign(charts.trend, result.charts.trend);
                    
                    console.log('图表数据:', charts);
                    
                    // 更新最近交易
                    recent_transactions.value = result.recent_transactions;
                    total_count.value = result.total_count;
                    
                    // 渲染图表
                    await nextTick();
                    console.log('准备渲染图表...');
                    renderCharts();
                } else {
                    console.error('数据加载失败:', result.error);
                }
            } catch (error) {
                console.error('加载数据异常:', error);
            }
        }
        
        // 加载导入历史
        async function loadImportHistory() {
            try {
                const result = await eel.get_import_history()();
                if (result.success) {
                    importHistory.value = result.history;
                }
            } catch (error) {
                console.error('加载导入历史失败:', error);
            }
        }
        
        // 渲染图表
        function renderCharts() {
            renderCategoryChart();
            renderMonthlyChart();
            renderTrendChart();
        }
        
        // 渲染分类饼图
        function renderCategoryChart() {
            console.log('renderCategoryChart:', categoryChartRef.value ? 'DOM 存在' : 'DOM 不存在');
            if (!categoryChartRef.value) {
                console.error('categoryChartRef DOM 元素不存在');
                return;
            }
            
            if (categoryChart) {
                categoryChart.dispose();
            }
            
            categoryChart = echarts.init(categoryChartRef.value);
            
            const data = charts.category.categories.map((category, index) => ({
                value: charts.category.values[index],
                name: category
            }));
            
            const option = {
                tooltip: {
                    trigger: 'item',
                    formatter: '{b}: ¥{c} ({d}%)'
                },
                legend: {
                    orient: 'vertical',
                    right: 10,
                    top: 'center'
                },
                series: [
                    {
                        type: 'pie',
                        radius: ['40%', '70%'],
                        center: ['35%', '50%'],
                        data: data,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        label: {
                            formatter: '{b}: {d}%'
                        }
                    }
                ]
            };
            
            categoryChart.setOption(option);
        }
        
        // 渲染月度柱状图
        function renderMonthlyChart() {
            console.log('renderMonthlyChart:', monthlyChartRef.value ? 'DOM 存在' : 'DOM 不存在');
            if (!monthlyChartRef.value) {
                console.error('monthlyChartRef DOM 元素不存在');
                return;
            }
            
            if (monthlyChart) {
                monthlyChart.dispose();
            }
            
            monthlyChart = echarts.init(monthlyChartRef.value);
            
            const option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                legend: {
                    data: ['收入', '支出']
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: charts.monthly.months
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '收入',
                        type: 'bar',
                        data: charts.monthly.income,
                        itemStyle: {
                            color: '#10b981'
                        }
                    },
                    {
                        name: '支出',
                        type: 'bar',
                        data: charts.monthly.expense,
                        itemStyle: {
                            color: '#ef4444'
                        }
                    }
                ]
            };
            
            monthlyChart.setOption(option);
        }
        
        // 渲染趋势折线图
        function renderTrendChart() {
            console.log('renderTrendChart:', trendChartRef.value ? 'DOM 存在' : 'DOM 不存在');
            if (!trendChartRef.value) {
                console.error('trendChartRef DOM 元素不存在');
                return;
            }
            
            if (trendChart) {
                trendChart.dispose();
            }
            
            trendChart = echarts.init(trendChartRef.value);
            
            const option = {
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['收入', '支出', '结余']
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: charts.trend.months
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '收入',
                        type: 'line',
                        data: charts.trend.income,
                        smooth: true,
                        itemStyle: {
                            color: '#10b981'
                        },
                        areaStyle: {
                            color: 'rgba(16, 185, 129, 0.1)'
                        }
                    },
                    {
                        name: '支出',
                        type: 'line',
                        data: charts.trend.expense,
                        smooth: true,
                        itemStyle: {
                            color: '#ef4444'
                        },
                        areaStyle: {
                            color: 'rgba(239, 68, 68, 0.1)'
                        }
                    },
                    {
                        name: '结余',
                        type: 'line',
                        data: charts.trend.balance,
                        smooth: true,
                        itemStyle: {
                            color: '#667eea'
                        }
                    }
                ]
            };
            
            trendChart.setOption(option);
        }
        
        // 刷新数据
        async function refreshData() {
            loading.value = true;
            await loadDashboardData();
            loading.value = false;
        }
        
        // 处理文件拖拽
        function handleDrop(e) {
            isDragOver.value = false;
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFile(files[0]);
            }
        }
        
        // 处理文件选择
        function handleFileSelect(e) {
            const files = e.target.files;
            if (files.length > 0) {
                handleFile(files[0]);
            }
        }
        
        // 处理文件导入
        async function handleFile(file) {
            if (!file.name.endsWith('.csv')) {
                importStatus.value = {
                    type: 'error',
                    message: '请选择 CSV 文件'
                };
                return;
            }
            
            loading.value = true;
            importStatus.value = null;
            
            try {
                // 由于 Eel 限制，需要通过后端读取文件
                // 这里使用文件路径（在实际应用中需要调整）
                const result = await eel.import_csv(file.path)();
                
                if (result.success) {
                    importStatus.value = {
                        type: 'success',
                        message: result.message + ` (重复：${result.duplicates} 条)`
                    };
                    await loadDashboardData();
                    await loadImportHistory();
                } else {
                    importStatus.value = {
                        type: 'error',
                        message: result.error
                    };
                }
            } catch (error) {
                importStatus.value = {
                    type: 'error',
                    message: '导入失败：' + error.message
                };
            } finally {
                loading.value = false;
            }
        }
        
        // 窗口大小变化时重新渲染图表
        function handleResize() {
            if (categoryChart) categoryChart.resize();
            if (monthlyChart) monthlyChart.resize();
            if (trendChart) trendChart.resize();
        }
        
        // 生命周期
        onMounted(() => {
            console.log('Vue 应用已挂载');
            console.log('DOM 元素检查:');
            console.log('  categoryChartRef:', categoryChartRef.value);
            console.log('  monthlyChartRef:', monthlyChartRef.value);
            console.log('  trendChartRef:', trendChartRef.value);
            
            initApp();
            window.addEventListener('resize', handleResize);
        });
        
        return {
            loading,
            showImportModal,
            isDragOver,
            importStatus,
            importHistory,
            summary,
            recent_transactions,
            total_count,
            categoryChartRef,
            monthlyChartRef,
            trendChartRef,
            refreshData,
            handleDrop,
            handleFileSelect,
            Math: Math
        };
    }
}).mount('#app');
