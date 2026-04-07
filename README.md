# ResearchMate - 商业文章素材采集助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/yitao2027/research-mate-skill?style=social)](https://github.com/yitao2027/research-mate-skill/stargazers)

> **为商业作者打造的智能化素材采集系统** —— 系统化采集高质量案例、数据、观点和竞品动态，建立结构化素材库，让深度写作有扎实的内容基础。

## 🎯 解决什么痛点

你是否遇到过这些问题：

- ❌ 接到选题后不知道从哪里找素材，只能零散搜索
- ❌ 找到的资料质量参差不齐，难以判断可信度
- ❌ 收藏了一堆链接，写作时却找不到关键信息在哪
- ❌ 花费大量时间搜集素材，真正写作的时间却被压缩
- ❌ 文章缺乏数据支撑和案例佐证，内容显得单薄

**ResearchMate** 通过自动化采集 + 智能分类 + 质量评估，帮你把素材收集效率提升 **3-5 倍**，让你把更多精力投入到深度分析和观点提炼上。

---

## 📖 适用场景

| 场景 | 典型用户 | 使用频率 |
|------|---------|---------|
| 行业分析文章 | 科技媒体作者、行业研究员 | 每周 2-3 次 |
| 公司深度报道 | 财经记者、商业分析师 | 每周 1-2 次 |
| 竞品分析报告 | 产品经理、市场策略人员 | 每月 2-4 次 |
| 投资研究笔记 | 投资人、券商分析师 | 每日使用 |
| 自媒体商业内容 | 公众号主、知乎大 V | 每周 3-5 次 |

---

## ⚡ 快速开始

### 前置要求

- Python 3.9 或更高版本
- pip 包管理器
- 网络连接（用于访问公开信息源）

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/yitao2027/research-mate-skill.git
cd research-mate-skill

# 2. 创建虚拟环境（推荐）
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行测试
python main.py --test

# 5. 开始采集素材
python main.py --topic "新能源汽车行业" --output materials/
```

### 配置说明

复制配置文件模板并根据需要调整：

```bash
cp config.example.yaml config.yaml
```

编辑 `config.yaml`：

```yaml
# 采集源配置
sources:
  industry_reports: true      # 行业报告
  tech_media: true           # 科技媒体
  company_filings: false     # 公司公告（需额外配置 API）
  social_media: true         # 社交媒体

# 输出格式
output:
  format: markdown           # 支持 markdown/json/csv
  include_citations: true    # 是否包含引用链接
  auto_tag: true            # 自动打标签

# 质量过滤
filters:
  min_credibility_score: 0.7  # 最低可信度阈值 (0-1)
  max_age_days: 30           # 资料最大年龄（天）
  require_data_points: true  # 必须包含数据点
```

---

## 🛠️ 核心功能

### 1. 多源信息采集

支持从以下渠道自动采集素材：

#### 行业报告
- 券商研报（中信证券、中金公司、国泰君安等）
- 咨询公司报告（麦肯锡、BCG、德勤、普华永道）
- 研究机构（艾瑞咨询、易观分析、亿欧智库）

#### 科技媒体
- 36 氪、虎嗅、晚点 LatePost
- 界面新闻、澎湃新闻、财经网
- TechCrunch、Bloomberg（英文源）

#### 上市公司公告
- 财报、招股书、投资者关系材料
- 重大事项公告、董事会决议

#### 社交媒体热点
- 知乎高赞回答（商业、科技话题）
- 雪球讨论（个股、行业分析）
- 微博热搜（商业相关话题）

### 2. 智能素材分类

采集到的素材会自动分类为：

```
📊 事实数据
├─ 财务指标（营收、利润、毛利率）
├─ 市场数据（份额、规模、增长率）
├─ 运营数据（用户数、DAU、留存率）
└─ 融资数据（轮次、金额、估值）

💼 典型案例
├─ 企业转型案例
├─ 产品创新案例
├─ 营销策略案例
└─ 组织管理案例

💬 专家观点
├─ 投资人评论
├─ CEO/创始人访谈
├─ 行业分析师报告
└─ 学者研究成果

🔍 竞品动态
├─ 新品发布
├─ 融资并购
├─ 战略调整
└─ 人事变动
```

### 3. 素材质量评估

每个素材都会经过以下维度评分：

| 维度 | 权重 | 说明 |
|------|------|------|
| **来源可信度** | 40% | 基于媒体权威性、历史准确性 |
| **时效性** | 25% | 发布时间越近分数越高 |
| **数据完整性** | 20% | 是否包含具体数字、对比数据 |
| **交叉验证** | 15% | 是否有多个独立来源佐证 |

**评分示例：**
```
素材：某新能源车企 2025 年 Q4 交付量达 50 万辆
├─ 来源可信度：0.9（官方财报）
├─ 时效性：0.95（7 天前发布）
├─ 数据完整性：0.8（含同比环比数据）
├─ 交叉验证：0.7（3 家媒体报道）
└─ 综合得分：0.86 ✅ 推荐使用
```

### 4. 输出交付物

#### 结构化素材卡片（Markdown 格式）

```markdown
## 素材卡片 #001

**类型：** 事实数据 - 财务指标  
**主题：** 比亚迪 2025 年 Q4 财报  
**采集时间：** 2026-04-07 15:30  

### 核心内容
- 营业收入：2,150 亿元，同比增长 42%
- 净利润：185 亿元，同比增长 68%
- 毛利率：22.5%，较上年同期提升 3.2pct
- 研发投入：128 亿元，占营收比重 5.9%

### 来源信息
- 原始链接：https://example.com/byd-q4-2025-report
- 发布媒体：巨潮资讯网（官方指定披露平台）
- 发布时间：2026-03-31
- 可信度评分：0.92/1.0

### 引用建议
> "根据比亚迪 2025 年 Q4 财报显示，公司全年营业收入达 2,150 亿元，同比增长 42%，净利润 185 亿元，同比增长 68% [1]。"

### 关联素材
- #003 宁德时代同期财报对比
- #007 新能源车行业整体增速分析
```

#### 素材溯源清单（CSV 格式）

```csv
ID，类型，主题，来源 URL,采集时间，可信度，时效性，综合得分
001，财务数据，比亚迪 Q4 财报，https://...,2026-04-07,0.92,0.95,0.86
002，专家观点，李斌访谈，https://...,2026-04-06,0.85,0.88,0.79
...
```

#### 写作灵感提示

基于采集到的素材，自动生成潜在选题方向：

```
💡 基于当前素材的写作建议：

1. **对比分析类**
   - 比亚迪 vs 特斯拉：2025 年盈利能力全对比
   - 造车新势力谁先实现可持续盈利？

2. **趋势洞察类**
   - 从财报看新能源车行业三大转折点
   - 毛利率普遍提升背后的产业链重构

3. **深度案例类**
   - 比亚迪如何做到毛利率 22.5%？
   - 研发投入超百亿的技术护城河效应
```

---

## 📂 项目结构

```
research-mate-skill/
├── main.py                 # 主程序入口
├── config.example.yaml     # 配置文件模板
├── requirements.txt        # Python 依赖
├── README.md              # 项目文档
├── LICENSE                # MIT 许可证
├── .gitignore            # Git 忽略规则
│
├── src/
│   ├── __init__.py
│   ├── collector.py      # 采集器模块
│   ├── classifier.py     # 分类器模块
│   ├── evaluator.py      # 质量评估模块
│   └── exporter.py       # 导出器模块
│
├── sources/
│   ├── industry_reports.py   # 行业报告源
│   ├── tech_media.py        # 科技媒体源
│   ├── social_media.py      # 社交媒体源
│   └── base_source.py       # 源基类
│
├── templates/
│   ├── material_card.md    # 素材卡片模板
│   └── summary_report.md   # 汇总报告模板
│
├── tests/
│   ├── test_collector.py
│   ├── test_classifier.py
│   └── test_evaluator.py
│
└── materials/              # 输出目录（自动生成）
    ├── 2026-04-07_新能源汽车/
    │   ├── materials.md
    │   ├── citations.csv
    │   └── inspiration.md
    └── ...
```

---

## 🔧 高级用法

### 自定义采集源

添加新的信息源只需继承 `BaseSource` 类：

```python
from src.sources.base_source import BaseSource

class CustomSource(BaseSource):
    def fetch(self, topic: str) -> list:
        # 实现你的采集逻辑
        pass
    
    def parse(self, raw_html: str) -> dict:
        # 解析页面内容
        pass
```

### 批量采集模式

```bash
# 一次性采集多个主题
python main.py --topics-file topics.txt --output batch_materials/

# topics.txt 内容示例：
新能源汽车行业
人工智能大模型
跨境电商
```

### API 调用方式

在你的 Python 项目中直接调用：

```python
from research_mate import ResearchMate

assistant = ResearchMate(config_path="config.yaml")

# 采集素材
materials = assistant.collect("储能行业", days_back=7)

# 获取高质量素材（评分>0.8）
premium = [m for m in materials if m.score > 0.8]

# 导出为 Markdown
assistant.export(materials, format="markdown", output_dir="./output")
```

---

## 🤝 贡献指南

欢迎贡献代码、报告新的信息源或改进文档！

### 开发环境搭建

```bash
# Fork 项目后克隆到本地
git clone https://github.com/YOUR_USERNAME/research-mate-skill.git
cd research-mate-skill

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试确保一切正常
pytest tests/
```

### 提交 PR 流程

1. 在 GitHub 上 Fork 本项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 在 GitHub 上创建 Pull Request

### Issue 反馈

遇到问题或有新功能建议？请查看 [Issue 模板](.github/ISSUE_TEMPLATE/) 后提交。

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) - 详见 LICENSE 文件

---

## 🙏 致谢

感谢以下开源项目提供的技术支持：

- [Requests](https://requests.readthedocs.io/) - HTTP 请求库
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析
- [PyYAML](https://pyyaml.org/) - 配置文件解析
- [Rich](https://rich.readthedocs.io/) - 终端美化输出

---

## 📬 联系方式

- **作者：** 易涛 (@yitao2027)
- **邮箱：** [你的邮箱]
- **GitHub Issues:** [问题反馈](https://github.com/yitao2027/research-mate-skill/issues)

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star 支持！**

[回到顶部 ↑](#readme)

</div>
