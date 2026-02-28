# Contributing to Bias-Radar / 贡献指南

Thank you for your interest in contributing to Bias-Radar! This document provides guidelines for contributing to this project.

感谢你对 Bias-Radar 项目的关注！本文档提供了贡献指南。

## Project Status / 项目状态

This is currently a personal project maintained by Chance Dean (PerryLink). While contributions are welcome, please note that this is an individual effort and response times may vary.

这是一个由 Chance Dean (PerryLink) 个人维护的项目。虽然欢迎贡献，但请注意这是个人项目，响应时间可能会有所不同。

## How to Report Issues / 如何报告问题

If you find a bug or have a feature request:

如果你发现了 bug 或有功能建议：

1. **Search existing issues** - Check if the issue has already been reported

   **搜索现有问题** - 检查问题是否已被报告

2. **Create a new issue** - If not found, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem or suggestion
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Python version, OS, etc.)

   **创建新问题** - 如果没有找到，创建新问题并包含：
   - 清晰、描述性的标题
   - 问题或建议的详细描述
   - 重现步骤（针对 bug）
   - 期望行为 vs 实际行为
   - 你的环境（Python 版本、操作系统等）

## Development Environment Setup / 开发环境搭建

### Prerequisites / 前置要求

- Python 3.8 or higher / Python 3.8 或更高版本
- Git
- pip

### Setup Steps / 搭建步骤

1. **Fork and clone the repository / Fork 并克隆仓库**

```bash
git clone https://github.com/PerryLink/bias-radar.git
cd bias-radar
```

2. **Create a virtual environment / 创建虚拟环境**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies / 安装依赖**

```bash
pip install -r requirements.txt
pip install -e .
```

4. **Install development dependencies / 安装开发依赖**

```bash
pip install pytest pytest-cov
```

5. **Verify installation / 验证安装**

```bash
pytest
bias-scan run
```

## Code Standards / 代码规范

### Python Style Guide / Python 风格指南

This project follows **PEP 8** style guidelines:

本项目遵循 **PEP 8** 风格指南：

- Use 4 spaces for indentation (no tabs) / 使用 4 个空格缩进（不使用制表符）
- Maximum line length: 88 characters / 最大行长度：88 字符
- Use descriptive variable names / 使用描述性的变量名
- Add docstrings for functions and classes / 为函数和类添加文档字符串
- Use type hints where appropriate / 适当使用类型提示

### Code Quality / 代码质量

- Write clear, self-documenting code / 编写清晰、自解释的代码
- Add comments for complex logic / 为复杂逻辑添加注释
- Keep functions focused and small / 保持函数专注和简洁
- Avoid code duplication / 避免代码重复

## Testing / 测试

### Running Tests / 运行测试

```bash
# Run all tests / 运行所有测试
pytest

# Run with coverage / 运行并查看覆盖率
pytest --cov=bias_radar tests/

# Run specific test file / 运行特定测试文件
pytest tests/test_scanner.py
```

### Writing Tests / 编写测试

- Add tests for new features / 为新功能添加测试
- Ensure existing tests pass / 确保现有测试通过
- Aim for good test coverage / 追求良好的测试覆盖率
- Use descriptive test names / 使用描述性的测试名称

## Pull Request Process / Pull Request 流程

### Before Submitting / 提交前

1. **Create a feature branch / 创建功能分支**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes / 进行修改**
   - Follow code standards / 遵循代码规范
   - Add tests / 添加测试
   - Update documentation if needed / 如需要更新文档

3. **Test your changes / 测试你的修改**

```bash
pytest
```

4. **Commit your changes / 提交你的修改**

```bash
git add .
git commit -m "feat: add your feature description"
```

Use conventional commit messages:
- `feat:` for new features / 新功能
- `fix:` for bug fixes / bug 修复
- `docs:` for documentation / 文档
- `test:` for tests / 测试
- `refactor:` for refactoring / 重构
- `chore:` for maintenance / 维护

### Submitting the PR / 提交 PR

1. **Push to your fork / 推送到你的 fork**

```bash
git push origin feature/your-feature-name
```

2. **Create a Pull Request / 创建 Pull Request**
   - Go to the original repository / 访问原始仓库
   - Click "New Pull Request" / 点击 "New Pull Request"
   - Select your branch / 选择你的分支
   - Fill in the PR template with:
     - Clear description of changes / 清晰描述修改内容
     - Related issue numbers / 相关问题编号
     - Testing performed / 已执行的测试

3. **Wait for review / 等待审查**
   - Address any feedback / 处理反馈意见
   - Make requested changes / 进行要求的修改
   - Be patient - this is a personal project / 保持耐心 - 这是个人项目

## Project Structure / 项目结构

```
bias-radar/
├── src/bias_radar/      # Main package / 主包
│   ├── scanner.py       # Bias scanning logic / 偏见扫描逻辑
│   ├── visualizer.py    # Visualization / 可视化
│   └── cli.py           # CLI interface / CLI 接口
├── tests/               # Test files / 测试文件
├── docs/                # Documentation / 文档
└── requirements.txt     # Dependencies / 依赖
```

## Questions? / 有问题？

If you have questions about contributing:

如果你对贡献有疑问：

- Open an issue for discussion / 开启一个 issue 进行讨论
- Contact: novelnexusai@outlook.com
- GitHub: [@PerryLink](https://github.com/PerryLink)

## License / 许可证

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

通过贡献，你同意你的贡献将在 Apache License 2.0 下授权。

---

Thank you for contributing to making AI bias detection more accessible!

感谢你为让 AI 偏见检测更易用做出贡献！
