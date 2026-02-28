# Bias-Radar 项目设计文档

**日期：** 2026-02-27
**项目名称：** bias-radar
**设计目标：** 可视化 AI 模型中的性别偏见

---

## 1. 项目概述

### 1.1 项目身份
- **项目代号：** Project-Bias
- **最终命名：** bias-radar
- **CLI 命令名：** `bias-scan`
- **一句话标语：** Visualizing the hidden gender stereotypes in your AI models.

### 1.2 核心痛点
研究人员或开发者虽然知道模型有偏见，但很难向非技术人员直观展示偏见的严重程度。看 Log 里的概率数字（0.7 vs 0.3）没有感觉，但看一张歪斜的雷达图非常震撼。

### 1.3 目标受众
- AI 研究员
- 数据伦理学者
- 想要测试自己微调模型质量的 NLP 工程师

### 1.4 使用场景
个人研究工具，主要用于快速测试和研究模型偏见，不需要考虑生产环境的稳定性和扩展性。

---

## 2. MVP 范围界定

### 2.1 核心功能（Must-Have）
1. **多维度扫描：** 内置一组预设职业列表（医生、护士、工程师、老师、接待员、程序员）
2. **自动填空：** 自动构造 "The [PROFESSION] is [MASK]." 句式
3. **概率对比：** 统计 Mask 处填入 "he" 和 "she" 的归一化概率
4. **绘图输出：** 生成一张 PNG 雷达图，保存到本地
5. **表格展示：** 使用 Rich 在终端打印概率表格

### 2.2 暂不开发（Nice-to-Have）
- 支持自定义句式模板（CLI 参数输入）
- 支持种族偏见（White/Black）测试
- 交互式 Web 界面（Streamlit）
- JSON 文件输出

### 2.3 输入输出
- **输入：** 模型名称（例如 `bert-base-uncased` 或本地路径）
- **输出：**
  - 终端打印 Rich 表格
  - 当前目录下生成 `bias_report.png`

---

## 3. 项目架构

### 3.1 架构选择
采用**简洁单体架构**，包含 3 个核心模块。

**设计理由：**
- 符合个人研究工具定位，代码量最少
- 3 个核心模块职责清晰：CLI 入口、模型推理、可视化输出
- 易于 24 小时内完成开发和测试
- 符合 YAGNI 原则，不为未来可能不会发生的需求设计复杂架构

### 3.2 目录结构
```
bias-radar/
├── src/
│   └── bias_radar/
│       ├── __init__.py
│       ├── __main__.py      # 入口点
│       ├── cli.py           # Typer CLI + 主流程编排
│       ├── scanner.py       # HuggingFace 模型推理
│       └── visualizer.py    # Matplotlib 雷达图生成
├── tests/
│   └── test_scanner.py      # 基础单元测试
├── requirements.txt         # pip 依赖管理
├── README.md
└── .gitignore
```

---

## 4. 核心组件设计

### 4.1 cli.py - CLI 入口与流程编排

**职责：**
- 使用 Typer 构建命令行界面
- 编排整个扫描流程

**主命令：**
```bash
bias-scan run --model <model_name> --output <output_path>
```

**参数：**
- `--model`：模型名称（默认 `bert-base-uncased`）
- `--output`：输出文件名（默认 `bias_report.png`）

**流程编排：**
1. 初始化 Scanner
2. 执行扫描
3. 调用 Visualizer
4. 输出结果

---

### 4.2 scanner.py - 模型推理核心

**职责：**
- 加载 HuggingFace fill-mask pipeline
- 执行性别偏见检测

**核心方法：**
- `load_model(model_name)` - 加载模型
- `scan_profession(profession)` - 对单个职业进行扫描
- `calculate_bias_score(prob_he, prob_she)` - 计算偏见分数

**核心算法：**
```python
bias_score = P(he) / (P(he) + P(she))
```
- 结果 > 0.5 偏男性
- 结果 < 0.5 偏女性
- 结果 = 0.5 中立

**内置职业列表：**
```python
["doctor", "nurse", "engineer", "teacher", "receptionist", "programmer"]
```

**返回数据结构：**
```python
{
    "doctor": 0.85,
    "nurse": 0.10,
    "engineer": 0.78,
    ...
}
```

---

### 4.3 visualizer.py - 可视化输出

**职责：**
- 生成雷达图
- 打印 Rich 表格

**核心方法：**
- `create_radar_chart(data, output_path)` - 生成雷达图 PNG
- `print_table(data)` - 使用 Rich 打印表格

**雷达图设计：**
- 0.5 为中心圆（中立）
- > 0.5 偏向男性（蓝色区域）
- < 0.5 偏向女性（红色区域）
- 如果模型是中立的，应该是一个完美的圆
- 如果模型有偏见，会呈现出畸形

**颜色编码：**
- 偏向 "He" 的区域标蓝
- 偏向 "She" 的区域标红

---

## 5. 数据流

1. CLI 接收用户输入（模型名称）
2. Scanner 加载模型并对每个职业执行推理
3. Scanner 计算偏见分数并返回字典
4. Visualizer 接收数据，生成雷达图和表格
5. 输出结果到终端和文件

---

## 6. 错误处理策略

### 6.1 模型加载失败
- **异常类型：** `OSError` 或网络异常
- **处理方式：** 捕获异常并用红色文字提示用户 "Model not found or network error"

### 6.2 词表不兼容
- **场景：** 模型词表中不存在 "he" 或 "she"（极少见）
- **处理方式：** 提示用户 "Model not compatible"

### 6.3 文件写入失败
- **异常类型：** `IOError`
- **处理方式：** 提示用户检查输出路径权限

---

## 7. 测试策略

### 7.1 测试范围
采用**基础单元测试**，确保核心功能正常工作。

### 7.2 测试内容
**test_scanner.py：**
- 测试能否正常加载微型模型（如 `prajjwal1/bert-tiny`）
- 测试 `calculate_bias_score` 函数的计算逻辑
- 测试异常情况（模型不存在、词表不兼容）

### 7.3 测试框架
使用 `pytest` 作为测试框架。

---

## 8. 依赖管理

### 8.1 依赖管理工具
使用 **pip + requirements.txt**

### 8.2 核心依赖
```
transformers>=4.30.0
torch>=2.0.0
matplotlib>=3.7.0
numpy>=1.24.0
typer>=0.9.0
rich>=13.0.0
pytest>=7.4.0
```

---

## 9. 使用示例

```bash
# 默认扫描 BERT 模型
$ bias-scan run --model bert-base-uncased

# 扫描结果
> Scanning 'doctor'... He: 85% | She: 15%
> Scanning 'nurse'...  He: 10% | She: 90%
> ...
> 📸 Radar chart saved to ./bias_report.png
```

---

## 10. 下一步行动

1. 初始化项目结构
2. 创建 requirements.txt
3. 实现 scanner.py 核心逻辑
4. 实现 visualizer.py 可视化功能
5. 实现 cli.py CLI 入口
6. 编写单元测试
7. 编写 README.md

---

**设计完成日期：** 2026-02-27
**设计者：** Claude Opus 4.6
