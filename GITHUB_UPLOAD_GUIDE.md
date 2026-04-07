# 📤 GitHub 上传操作指南

**适用对象：** GitHub 新手，从未上传过项目的开发者  
**目标：** 将 ResearchMate 素材采集技能上传到你的 GitHub 账号 (@yitao2027)

---

## 🎯 方案选择

你有 **两种方式** 可以上传项目到 GitHub：

### 方案 A：使用 GitHub Desktop（推荐新手）
- ✅ 图形化界面，无需记命令
- ✅ 自动处理 Git 配置
- ✅ 可视化查看文件变化

### 方案 B：使用命令行 Git
- ✅ 更灵活，适合后续自动化
- ✅ 所有开发者必备技能
- ✅ 本指南重点讲解此方案

---

## 📋 准备工作

### Step 1: 安装 Git

**macOS:**
```bash
# 打开终端，输入以下命令安装 Xcode Command Line Tools（包含 Git）
xcode-select --install
```

**Windows:**
1. 访问 https://git-scm.com/download/win
2. 下载并运行安装程序
3. 一路 Next 即可（保持默认选项）

**验证安装:**
```bash
git --version
# 应显示类似：git version 2.42.0
```

---

## 🚀 上传流程（命令行方案）

### Step 1: 在 GitHub 上创建空仓库

1. 登录你的 GitHub 账号：https://github.com/yitao2027
2. 点击右上角 **+** → **New repository**
3. 填写以下信息：
   - **Repository name:** `research-mate`
   - **Description:** `📚 商业文章素材采集助手 - 帮助作者系统化采集高质量素材，建立结构化素材库`
   - **Public/Private:** 选择 **Public**（开源项目更容易获得 Star）
   - **Initialize this repository with:** ❌ **不要勾选**（保持空白）
4. 点击 **Create repository**

✅ 创建成功后，你会看到一个页面显示 "Quick setup" 和一行类似这样的命令：
```
git remote add origin https://github.com/yitao2027/research-mate.git
```

**保持这个页面打开，我们马上要用到它！**

---

### Step 2: 初始化本地 Git 仓库

打开终端（Terminal），进入项目目录：

```bash
cd /Users/182378252qq.com/.real/users/user-05e652c12065c87f63ac28ea21bf71f7/workspace/research-mate-skill
```

#### 2.1 初始化 Git 仓库
```bash
git init
```
你会看到：`Initialized empty Git repository in ...`

#### 2.2 配置 Git 用户信息（首次使用需要设置）
```bash
git config --global user.name "yitao2027"
git config --global user.email "你的邮箱@example.com"
```
> ⚠️ **重要：** 邮箱建议使用你 GitHub 账号绑定的邮箱，这样提交记录才会关联到你的账号

#### 2.3 查看所有文件状态
```bash
git status
```
你会看到一堆 "Untracked files"（未跟踪的文件），这是正常的。

---

### Step 3: 添加文件到暂存区

```bash
# 添加所有文件（除了 .gitignore 排除的）
git add .
```

或者分步添加（更谨慎的做法）：
```bash
git add README.md
git add main.py
git add requirements.txt
git add LICENSE
git add .gitignore
git add src/
```

再次查看状态：
```bash
git status
```
现在应该显示 "Changes to be committed"（绿色文字）

---

### Step 4: 提交到本地仓库

```bash
git commit -m "Initial commit: ResearchMate v0.1.0 - 商业文章素材采集助手"
```

> 💡 `-m` 后面的文字是提交信息（commit message），应该简洁描述这次提交的内容

你会看到类似：
```
[main (root-commit) a1b2c3d] Initial commit: ResearchMate v0.1.0
 10 files changed, 1234 insertions(+)
 create mode 100644 README.md
 create mode 100644 main.py
 ...
```

---

### Step 5: 关联远程仓库并推送

回到之前 GitHub 页面上显示的 "Quick setup" 区域，找到这行命令：

```bash
git remote add origin https://github.com/yitao2027/research-mate.git
```

复制并执行（如果 URL 不同，用你页面上显示的）：
```bash
git remote add origin https://github.com/yitao2027/research-mate.git
```

> 🔍 验证是否添加成功：`git remote -v` 应该显示 origin 的 URL

#### 推送到 GitHub

```bash
git branch -M main
git push -u origin main
```

> 💡 `-u` 参数会设置上游分支，以后直接 `git push` 即可

**首次推送可能需要认证：**
- 如果使用 HTTPS 方式，会提示输入 GitHub 用户名和密码
- **密码位置：** 不是你的 GitHub 登录密码，而是 **Personal Access Token**
- 获取 Token：GitHub Settings → Developer settings → Personal access tokens → Generate new token

**推荐使用 SSH 方式（一劳永逸）：**

1. 生成 SSH Key：
   ```bash
   ssh-keygen -t ed25519 -C "你的邮箱@example.com"
   ```
   一路回车即可

2. 查看公钥内容：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   复制显示的全部内容（以 `ssh-ed25519` 开头）

3. 添加到 GitHub：
   - 访问 https://github.com/settings/keys
   - 点击 **New SSH key**
   - Title: 随便填（如 "My MacBook Pro"）
   - Key: 粘贴刚才复制的内容
   - 点击 **Add SSH key**

4. 改用 SSH 地址重新关联：
   ```bash
   git remote set-url origin git@github.com:yitao2027/research-mate.git
   git push -u origin main
   ```

✅ **推送成功后，刷新 GitHub 仓库页面，你应该能看到所有文件了！**

---

## 🎨 包装优化清单

项目上传后，按以下顺序完善包装：

### 阶段一：基础完善（必做）

- [ ] **README 顶部添加徽章**（提升专业度）
  ```markdown
  ![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
  ![License](https://img.shields.io/badge/license-MIT-green.svg)
  ![Python](https://img.shields.io/badge/python-3.9+-red.svg)
  ![Stars](https://img.shields.io/github/stars/yitao2027/research-mate.svg)
  ```

- [ ] **添加截图/GIF 演示**
  - 运行程序的实际输出截图
  - 或用 LICEcap 录制一个 30 秒的使用 GIF

- [ ] **完善目录结构说明**
  - 在 README 中添加项目结构树

### 阶段二：进阶优化（选做）

- [ ] **添加 Issue 模板**
  - `.github/ISSUE_TEMPLATE/bug_report.md`
  - `.github/ISSUE_TEMPLATE/feature_request.md`

- [ ] **编写贡献指南**
  - `CONTRIBUTING.md` 说明如何参与项目

- [ ] **发布第一个 Release**
  - Releases → Draft a new release → Tag: v0.1.0

- [ ] **添加 GitHub Actions CI/CD**
  - 自动运行测试
  - 自动检查代码质量

### 阶段三：推广运营（长期）

- [ ] **分享到技术社区**
  - 知乎、掘金、V2EX、Hacker News
  - 附上 GitHub 链接

- [ ] **响应 Issues 和 PR**
  - 及时回复用户问题
  - 合并优质贡献

- [ ] **持续迭代更新**
  - 每月至少一次小版本更新
  - 保持 CHANGELOG.md 更新记录

---

## 🏆 得高分的关键因素

根据 GitHub 热门项目的经验，以下因素最影响项目热度：

### 1. **第一印象（前 3 秒决定用户是否继续看）**
- ✅ 清晰的 Logo 或 Banner 图
- ✅ 一句话价值主张（README 第一行）
- ✅ 专业的徽章展示

### 2. **文档质量（决定用户是否 Star）**
- ✅ 快速开始教程（5 分钟内能跑起来）
- ✅ 丰富的使用示例
- ✅ FAQ 常见问题解答
- ✅ API 文档完整

### 3. **项目活跃度（决定长期增长）**
- ✅ 定期 Commits（每周至少 1-2 次）
- ✅ 活跃的 Issues 讨论
- ✅ 及时的 Bug 修复
- ✅ Release 版本更新

### 4. **社区建设（决定能否破圈）**
- ✅ 明确的贡献指南
- ✅ 友好的 Issue 回复
- ✅ 认可贡献者（README 添加 Contributors 列表）
- ✅ 建立 Discord/微信群等社区

### 5. **差异化定位（决定竞争力）**
- ✅ 解决真实痛点（你的素材采集定位很好！）
- ✅ 与现有工具对比表格
- ✅ 独特的功能亮点
- ✅ 成功案例展示

---

## 📊 项目结构总览

上传完成后，你的仓库应该是这样的：

```
research-mate/
├── README.md                 # 项目主文档（最重要！）
├── main.py                   # 程序入口
├── requirements.txt          # Python 依赖
├── LICENSE                   # 开源许可证
├── .gitignore               # Git 忽略文件
├── GITHUB_UPLOAD_GUIDE.md   # 本指南
└── src/
    ├── __init__.py          # 包初始化
    ├── collector.py         # 素材采集器
    ├── classifier.py        # 智能分类器
    ├── evaluator.py         # 质量评估器
    ├── exporter.py          # 多格式导出器
    └── config.py            # 配置管理
```

---

## 🆘 常见问题

### Q1: "fatal: remote origin already exists"
**解决：** `git remote remove origin` 然后重新 `git remote add origin ...`

### Q2: "Permission denied (publickey)"
**解决：** SSH Key 没配置好，重新走一遍 Step 5 的 SSH 配置流程

### Q3: 推送时卡在 "Enumerating objects..."
**解决：** 网络问题，尝试：
- 切换网络（手机热点试试）
- 使用 `GIT_TRACE_PACKET=1 git push` 查看详细进度
- 耐心等待（大文件可能比较慢）

### Q4: 不小心提交了敏感信息（密码、Token）
**紧急处理：**
1. 立即删除远程仓库
2. 本地 `git reset --hard HEAD~1` 回退提交
3. 修改敏感信息
4. 重新上传

---

## 📞 下一步行动

1. ✅ 你现在已经完成了所有代码文件的创建
2. 📤 接下来按照本指南上传到 GitHub
3. 🎨 上传完成后，我可以帮你：
   - 设计项目 Logo（用 AI 生成）
   - 录制使用演示 GIF
   - 编写更详细的使用教程
   - 规划 v0.2.0 新功能

**有任何问题随时问我！现在就开始上传吧！** 🚀
