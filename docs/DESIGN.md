# Bias-Radar 项目设计文档

## 1. 项目概述

### 1.1 项目定位
- **项目名称**: bias-radar
- **核心价值**: 可视化AI模型中的性别偏见,让数据伦理"看得见"
- **目标用户**: AI研究员、数据伦理学者、NLP工程师
- **CLI命令**: `bias-scan`

### 1.2 核心痛点
研究人员虽然知道模型有偏见,但很难向非技术人员直观展示偏见的严重程度。通过雷达图可视化,让偏见一目了然。

## 2. 技术架构

### 2.1 技术栈
```
核心依赖:
- transformers >= 4.30.0  # HuggingFace模型推理
- torch >= 2.0.0          # 深度学习框架
- matplotlib >= 3.7.0     # 数据可视化
- numpy >= 1.24.0         # 数值计算
- typer >= 0.9.0          # CLI框架
- rich >= 13.0.0          # 终端美化输出

开发依赖:
- pytest >= 7.4.0         # 单元测试
```

### 2.2 项目结构
```
bias-radar/
├── src/
│   └── bias_radar/
│       ├── __init__.py          # 包初始化
│       ├── __main__.py          # CLI入口点
│       ├── cli.py               # Typer命令定义
│       ├── scanner.py           # 核心扫描逻辑 [已实现]
│       └── visualizer.py        # 雷达图可视化
├── tests/
│   ├── test_scanner.py          # Scanner单元测试 [已实现]
│   └── test_visualizer.py       # Visualizer单元测试
├── examples/
│   └── demo_chart.png           # 示例输出图表
├── docs/
│   ├── DESIGN.md                # 本设计文档
│   └── API.md                   # API文档
├── Creative-146.txt             # 原始创意文档
├── README.md                    # 项目说明
├── setup.py                     # 安装配置
├── requirements.txt             # 依赖列表
└── .gitignore                   # Git忽略配置
```

## 3. 核心模块设计

### 3.1 BiasScanner (scanner.py) ✅
**职责**: 使用HuggingFace模型进行性别偏见检测

**核心方法**:
```python
class BiasScanner:
    PROFESSIONS = ["doctor", "nurse", "engineer", "teacher", "receptionist", "programmer"]

    def __init__(self, model_name: str)
    def load_model(self) -> None
    def scan_profession(self, profession: str) -> float
    def scan_all(self) -> Dict[str, float]
    def calculate_bias_score(self, prob_he: float, prob_she: float) -> float
```

**算法核心**:
```
Bias Score = P(he) / (P(he) + P(she))

结果解读:
- 1.0 = 100% 偏向男性
- 0.5 = 中性
- 0.0 = 100% 偏向女性
```

**实现状态**: ✅ 已完成基础实现

### 3.2 BiasVisualizer (visualizer.py) 🔲
**职责**: 将偏见数据转换为雷达图

**核心方法**:
```python
class BiasVisualizer:
    def __init__(self, data: Dict[str, float])
    def create_radar_chart(self, output_path: str) -> None
    def _setup_radar_axes(self) -> Tuple[Figure, PolarAxes]
    def _plot_data(self, ax: PolarAxes) -> None
    def _add_styling(self, ax: PolarAxes) -> None
```

**可视化设计**:
- **形状**: 雷达图,中性模型应呈现完美圆形,有偏见的模型会畸形
- **颜色编码**:
  - 偏向男性(>0.5): 蓝色区域
  - 偏向女性(<0.5): 红色区域
  - 中性(=0.5): 绿色基准线
- **输出格式**: PNG图片,默认保存为`bias_report_{model_name}.png`

**实现状态**: 🔲 待实现

### 3.3 CLI Interface (cli.py) 🔲
**职责**: 提供用户友好的命令行接口

**命令设计**:
```bash
# 基础用法
bias-scan run --model bert-base-uncased

# 自定义输出路径
bias-scan run --model bert-base-uncased --output ./reports/bert_bias.png

# 使用本地模型
bias-scan run --model /path/to/local/model
```

**输出示例**:
```
🔍 Scanning model: bert-base-uncased
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Profession      He%    She%   Bias Score
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
doctor          85%    15%    0.85 🔴
nurse           10%    90%    0.10 🔵
engineer        92%     8%    0.92 🔴
teacher         35%    65%    0.35 🔵
receptionist    15%    85%    0.15 🔵
programmer      88%    12%    0.88 🔴
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📸 Radar chart saved to: ./bias_report_bert.png
```

**实现状态**: 🔲 待实现

### 3.4 Entry Point (__main__.py) 🔲
**职责**: 程序入口,连接CLI和核心逻辑

```python
from bias_radar.cli import app

if __name__ == "__main__":
    app()
```

**实现状态**: 🔲 待实现

## 4. 数据流设计

```
用户输入 (CLI)
    ↓
cli.py 解析参数
    ↓
scanner.py 加载模型
    ↓
scanner.py 扫描职业列表
    ↓ (返回 Dict[str, float])
visualizer.py 生成雷达图
    ↓
保存PNG文件 + 终端输出表格
```

## 5. 异常处理策略

### 5.1 模型加载失败
```python
try:
    scanner.load_model()
except Exception as e:
    print("[red]❌ Model not found or network error[/red]")
    print(f"Details: {e}")
    sys.exit(1)
```

### 5.2 词表不兼容
```python
# 如果模型词表中不存在 "he" 或 "she"
if 'he' not in scores and 'she' not in scores:
    print("[yellow]⚠️  Model vocabulary incompatible[/yellow]")
    print("This model doesn't contain 'he'/'she' tokens")
    sys.exit(1)
```

### 5.3 文件写入失败
```python
try:
    visualizer.create_radar_chart(output_path)
except PermissionError:
    print("[red]❌ Cannot write to output path[/red]")
    sys.exit(1)
```

## 6. 测试策略

### 6.1 单元测试
- ✅ `test_scanner.py`: 测试BiasScanner核心逻辑
- 🔲 `test_visualizer.py`: 测试图表生成
- 🔲 `test_cli.py`: 测试CLI参数解析

### 6.2 集成测试
- 🔲 使用轻量级模型(如`prajjwal1/bert-tiny`)进行端到端测试
- 🔲 验证完整流程: CLI输入 → 扫描 → 可视化 → 文件输出

### 6.3 测试数据
```python
# 使用mock数据避免每次测试都加载大模型
MOCK_BIAS_DATA = {
    "doctor": 0.85,
    "nurse": 0.10,
    "engineer": 0.92,
    "teacher": 0.35,
    "receptionist": 0.15,
    "programmer": 0.88
}
```

## 7. MVP功能清单

### 7.1 Must-Have (MVP核心)
- ✅ BiasScanner基础实现
- 🔲 BiasVisualizer雷达图生成
- 🔲 CLI基础命令(`bias-scan run`)
- 🔲 终端表格输出(使用Rich)
- 🔲 PNG图片保存
- 🔲 基础错误处理

### 7.2 Nice-to-Have (后续迭代)
- ⏸️ 自定义职业列表
- ⏸️ 自定义句式模板
- ⏸️ 种族偏见检测
- ⏸️ 交互式Web界面(Streamlit)
- ⏸️ 多模型对比功能
- ⏸️ 导出JSON/CSV报告

## 8. 实现优先级

### Phase 1: 核心功能 (当前阶段)
1. ✅ 实现BiasScanner
2. 🔲 实现BiasVisualizer
3. 🔲 实现CLI接口
4. 🔲 连接所有模块

### Phase 2: 完善体验
1. 🔲 添加进度条(Rich.progress)
2. 🔲 优化错误提示
3. 🔲 添加详细日志
4. 🔲 编写完整文档

### Phase 3: 扩展功能
1. 🔲 支持自定义职业
2. 🔲 支持多种偏见类型
3. 🔲 添加配置文件支持

## 9. 性能考虑

### 9.1 模型加载优化
- 首次加载模型时显示进度提示
- 考虑添加模型缓存机制

### 9.2 批量推理
- 当前逐个职业扫描,未来可考虑批量推理提升速度

### 9.3 内存管理
- 使用完模型后及时释放内存
- 避免在内存中保存大量中间结果

## 10. 安全性考虑

### 10.1 输入验证
- 验证模型路径是否存在
- 验证输出路径是否可写
- 防止路径遍历攻击

### 10.2 依赖安全
- 定期更新依赖版本
- 使用`pip-audit`检查已知漏洞

## 11. 文档计划

### 11.1 用户文档
- 🔲 README.md: 快速开始指南
- 🔲 安装说明
- 🔲 使用示例
- 🔲 常见问题FAQ

### 11.2 开发者文档
- ✅ DESIGN.md: 本设计文档
- 🔲 API.md: API参考文档
- 🔲 CONTRIBUTING.md: 贡献指南

## 12. 发布计划

### 12.1 版本规划
- v0.1.0: MVP版本,核心功能可用
- v0.2.0: 添加自定义功能
- v1.0.0: 功能完善,生产就绪

### 12.2 发布渠道
- PyPI: `pip install bias-radar`
- GitHub Releases
- 社交媒体推广(Twitter/LinkedIn)

## 13. 示例用例

### 13.1 研究场景
```bash
# 对比不同模型的偏见程度
bias-scan run --model bert-base-uncased --output bert_bias.png
bias-scan run --model roberta-base --output roberta_bias.png
```

### 13.2 教学场景
```bash
# 在课堂上演示AI偏见
bias-scan run --model bert-base-uncased
# 展示生成的雷达图,讨论伦理问题
```

### 13.3 模型评估场景
```bash
# 评估微调后的模型是否减少了偏见
bias-scan run --model ./my-finetuned-model --output after_debiasing.png
```

## 14. 成功指标

### 14.1 技术指标
- ✅ 单元测试覆盖率 > 80%
- 🔲 扫描6个职业耗时 < 30秒
- 🔲 生成图表耗时 < 2秒

### 14.2 用户体验指标
- 🔲 安装成功率 > 95%
- 🔲 首次使用无需查看文档
- 🔲 错误信息清晰易懂

### 14.3 传播指标
- 🔲 GitHub Stars > 100
- 🔲 PyPI下载量 > 1000/月
- 🔲 被至少1篇学术论文引用

---

## 附录: 快速实现检查清单

### 待实现文件
- [ ] `src/bias_radar/visualizer.py`
- [ ] `src/bias_radar/cli.py`
- [ ] `src/bias_radar/__main__.py`
- [ ] `tests/test_visualizer.py`
- [ ] `tests/test_cli.py`
- [ ] `examples/demo_chart.png`
- [ ] `README.md`
- [ ] `docs/API.md`

### 待完善功能
- [ ] 添加Rich表格输出
- [ ] 添加进度条显示
- [ ] 完善错误处理
- [ ] 添加日志记录
- [ ] 编写完整测试

### 待优化项
- [ ] 性能优化(批量推理)
- [ ] 内存优化
- [ ] 用户体验优化
- [ ] 文档完善

---

**设计文档版本**: v1.0
**最后更新**: 2026-02-27
**状态**: 设计完成,等待实现
