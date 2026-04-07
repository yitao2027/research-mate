# ResearchMate - 测试指南

本文档说明如何运行和维护 ResearchMate 的测试套件。

---

## 📋 目录

- [快速开始](#快速开始)
- [运行测试](#运行测试)
- [测试覆盖率](#测试覆盖率)
- [编写新测试](#编写新测试)
- [持续集成](#持续集成)

---

## 🚀 快速开始

### 安装测试依赖

```bash
# 确保已安装开发依赖
pip install -r requirements.txt
```

requirements.txt 中已包含测试所需的 pytest 和 pytest-cov。

### 验证安装

```bash
# 检查 pytest 版本
pytest --version

# 应该显示 pytest 7.x.x
```

---

## ▶️ 运行测试

### 运行全部测试

```bash
# 在项目根目录执行
pytest
```

这将自动发现并运行 `tests/` 目录下的所有测试文件。

### 详细输出模式

```bash
# 显示每个测试的执行详情
pytest -v

# 或更详细的输出
pytest -vv
```

### 运行特定测试文件

```bash
# 只运行分类器测试
pytest tests/test_classifier.py

# 只运行评估器测试
pytest tests/test_evaluator.py

# 只运行导出器测试
pytest tests/test_exporter.py

# 只运行采集源测试
pytest tests/test_sources.py
```

### 运行特定测试用例

```bash
# 运行分类器的某个测试方法
pytest tests/test_classifier.py::TestMaterialClassifier::test_classify_financial_data

# 运行多个指定测试
pytest tests/test_classifier.py::TestMaterialClassifier::test_classify_financial_data tests/test_evaluator.py::TestQualityEvaluator::test_high_credibility_source
```

### 运行匹配模式的测试

```bash
# 运行所有名称包含 "classify" 的测试
pytest -k classify

# 运行所有名称包含 "export" 的测试
pytest -k export

# 排除某些测试
pytest -k "not slow"
```

---

## 📊 测试覆盖率

### 生成覆盖率报告

```bash
# 运行测试并生成覆盖率数据
pytest --cov=src --cov-report=html

# 在浏览器中查看 HTML 报告
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov\\index.html  # Windows
```

### 终端覆盖率报告

```bash
# 在终端显示覆盖率摘要
pytest --cov=src --cov-report=term-missing
```

### 覆盖率目标

项目目标是保持 **80% 以上**的代码覆盖率。可以在 `pytest.ini` 中配置失败阈值：

```ini
[pytest]
addopts = --cov=src --cov-fail-under=80
```

---

## ✍️ 编写新测试

### 测试文件命名

- 文件名必须以 `test_` 开头，如 `test_classifier.py`
- 放在 `tests/` 目录下

### 测试类命名

- 测试类以 `Test` 开头，如 `TestMaterialClassifier`
- 继承自 `unittest.TestCase` 或使用普通类

### 测试函数命名

- 测试函数以 `test_` 开头，如 `test_classify_financial_data`
- 使用描述性的名称，说明测试的场景

### 测试模板

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 XXX 模块
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from module_name import ClassName


class TestClassName:
    """测试类"""
    
    def setup_method(self):
        """每个测试前的准备工作（pytest 风格）"""
        self.obj = ClassName()
    
    def test_normal_case(self):
        """测试正常情况"""
        result = self.obj.some_method(input_data)
        assert result == expected_value
    
    def test_edge_case(self):
        """测试边界情况"""
        # ...
    
    def test_error_handling(self):
        """测试错误处理"""
        with pytest.raises(SomeException):
            self.obj.some_method(invalid_input)
```

### 使用 pytest.fixture

```python
import pytest

@pytest.fixture
def sample_material():
    """提供测试用的素材样本"""
    return {
        'title': '测试标题',
        'content': '测试内容',
        'source': '测试来源'
    }

def test_with_fixture(sample_material):
    """使用 fixture 的测试"""
    result = classifier.classify(sample_material)
    assert result['category'] is not None
```

---

## 🔧 调试测试

### 打印调试信息

```bash
# 显示 print 输出
pytest -s

# 或在测试失败时显示本地变量
pytest -l
```

### 逐行调试

```bash
# 使用 pdb 调试
pytest --pdb

# 或在代码中添加断点
import pdb; pdb.set_trace()
```

### 失败后进入调试器

```bash
# 测试失败时自动进入 pdb
pytest --pdb --tb=short
```

---

## 🏗️ 持续集成

### GitHub Actions 配置示例

创建 `.github/workflows/tests.yml`：

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 📝 最佳实践

1. **保持测试独立**：每个测试应该独立运行，不依赖其他测试的状态
2. **使用 Mock**：对于网络请求、文件 IO 等外部依赖，使用 mock 避免真实调用
3. **测试边界条件**：不仅要测试正常情况，还要测试空值、异常值、极端情况
4. **有意义的断言**：断言应该清晰表达预期结果，避免过于复杂的断言逻辑
5. **定期审查测试**：随着代码演进，及时更新或删除过时的测试

---

## 🐛 常见问题

### Q: 测试导入失败怎么办？

A: 确保在测试文件中正确添加了 src 目录到 Python 路径：

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
```

### Q: 如何跳过某些测试？

A: 使用 `@pytest.mark.skip`：

```python
@pytest.mark.skip(reason="暂未实现")
def test_future_feature():
    pass
```

### Q: 测试运行太慢怎么办？

A: 
- 使用 `-x` 在第一次失败时停止
- 使用 `-q` 减少输出
- 并行运行测试：`pytest-xdist` 插件

```bash
pip install pytest-xdist
pytest -n auto  # 自动使用所有 CPU 核心
```

---

## 📞 获取帮助

遇到问题？
- 查看 [pytest 官方文档](https://docs.pytest.org/)
- 提交 [GitHub Issue](https://github.com/yitao2027/research-mate-skill/issues)
- 联系维护者：易涛 (@yitao2027)

---

**最后更新：** 2026-04-07  
**维护者：** ResearchMate Team
