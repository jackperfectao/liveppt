**简体中文** | [English](README_EN.md)

<div align="center">

# LivePPT

**把 Markdown / Word / PowerPoint 变成可点击、可翻页、可分享的 HTML 演示页。**

[![License](https://img.shields.io/badge/License-MIT%20%2B%20Additional%20Terms-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/jackperfectao/LivePPT?style=social)](https://github.com/jackperfectao/LivePPT/stargazers)

![LivePPT Demo Preview](assets/demo.gif)

</div>

---

## LivePPT 是什么

LivePPT 不是传统 PPT 工具，也不是单纯的文档模板。

它更像一个"演示页生成器"：
- 输入 **Markdown / Word / PowerPoint / README**
- 一条命令生成 HTML
- 结果可以直接打开、翻页、演示、分享

一句话：**先把内容变成结果，再逐步升级成更高级的演示体验。**

## 生成的 HTML 长什么样

- 单文件 HTML，无外部依赖，双击即可在浏览器打开
- 支持键盘导航（← → 翻页，Home/End 跳转）
- 支持点击圆点导航和顶部进度条
- 支持移动端响应式布局
- 内置 4 种预设主题风格，一行命令切换

## 适合谁

- 想把项目 README 讲得更清楚的开源作者
- 想快速做产品发布页 / 路演页 / 课程讲义的人
- 不想从零写前端，但又不满足于静态文档的人
- 有现成 Word 或 PPT，想快速转为可交互网页演示的人

## 30 秒快速开始

```bash
git clone https://github.com/jackperfectao/liveppt.git
cd liveppt
make install-deps
make validate
```

---

## 完整用户指南

### 支持的文件格式

LivePPT 支持 **5 种输入格式**，全部输出为 HTML：

| 输入格式 | Make 命令 | 说明 |
|---------|-----------|------|
| Markdown (.md) | `make render-html` | 已有 Markdown 直接转 |
| Word (.docx) | `make convert-docx` | Word 文档转 |
| PowerPoint (.pptx) | `make convert-pptx` | PPT 演示转 |
| README.md | `make build-from-readme` | README 清洗后转 |
| 无内容 | `make build-showcase` | 自动生成 + 渲染 |

### 1. Markdown (.md) → HTML

把已有的 Markdown 文件（如项目计划、讲义）直接转为演示页。

```bash
# Make 命令（推荐）
make render-html \
  PLAN=path/to/your-file.md \
  OUTPUT=dist/output.html \
  STYLE=neo-luxury \
  BRAND="My Brand"

# 直接 Python 调用
python3 scripts/render_plan_to_html.py \
  path/to/your-file.md \
  --output dist/output.html \
  --theme neo-luxury \
  --brand "My Brand" \
  --subtitle "自定义副标题"
```

**Markdown 格式要求：**

```markdown
# 演示标题

- 目标受众：受众描述
- 主风格：风格名称

封面介绍段落...

## 第一节标题

正文段落...

- 任务：具体任务
- 交付：交付物

## 第二节标题

- 要点一
- 要点二

## KPI

- 成果一
- 成果二
```

**解析规则：**
- `# H1` = 封面标题
- `## H2` = 每张幻灯片
- `- key：value` = 标签芯片（任务/交付/目标受众等关键字被识别为标签）
- `- item` = 要点列表
- 纯文本 = 正文段落
- `## KPI` = 总结页（带绿色对勾样式）

### 2. Word (.docx) → HTML

把 Word 文档（如商业计划书、产品需求文档、会议纪要）转为演示页。

```bash
# Make 命令（推荐）
make convert-docx \
  DOCX_INPUT=path/to/document.docx \
  OUTPUT=dist/output.html \
  STYLE=cyber-pulse \
  BRAND="My Brand"

# 直接 Python 调用
python3 scripts/convert_from_docx.py \
  path/to/document.docx \
  --output dist/output.html \
  --theme cyber-pulse \
  --brand "My Brand" \
  --subtitle "自定义副标题"
```

**Word 格式映射：**

| Word 元素 | 转换结果 |
|-----------|---------|
| 首个一级标题（Heading 1） | 演示封面标题 `#` |
| 二级标题（Heading 2） | 幻灯片边界 `##` |
| 三级标题（Heading 3） | 幻灯片内子节 `###` |
| 项目符号列表（List Bullet） | 要点列表 `- item` |
| 编号列表（List Number） | 要点列表 `- item` |
| 普通段落 | 幻灯片正文 |
| 文档属性（标题/作者/主题） | 封面元数据标签 |

**自动处理：**
- 无标题文档 → 以文件名作为封面标题
- 表格内容 → 暂跳过（会记录日志）
- 中英混合 → 自动保持 utf-8 编码

### 3. PowerPoint (.pptx) → HTML

把现有 PowerPoint 演示文件转为 LivePPT HTML 演示页。

```bash
# Make 命令（推荐）
make convert-pptx \
  PPTX_INPUT=path/to/presentation.pptx \
  OUTPUT=dist/output.html \
  STYLE=minimal-editorial \
  BRAND="My Brand"

# 直接 Python 调用
python3 scripts/convert_from_pptx.py \
  path/to/presentation.pptx \
  --output dist/output.html \
  --theme minimal-editorial \
  --brand "My Brand" \
  --subtitle "自定义副标题"
```

**PPT 格式映射：**

| PPT 元素 | 转换结果 |
|---------|---------|
| 首张标题幻灯片 | 演示封面 `#` + 副标题 |
| 幻灯片标题（标题占位符） | 幻灯片 `##` |
| 正文文本框内容 | 要点列表 `- item` |
| 演讲者备注 | 引用块 `> 备注内容` |
| 表格 | 管道分隔行 |

**自动处理：**
- 无标题幻灯片 → 自动命名为 `## 第 N 页`
- 图片和图表 → 暂跳过（会记录日志）
- 空白幻灯片 → 自动跳过

### 4. README.md → HTML（带清洗）

把 GitHub 项目的 README 转为演示页，自动清理徽章、代码块等无关内容。

```bash
# Make 命令（推荐）
make build-from-readme \
  README_INPUT=path/to/README.md \
  OUTPUT=dist/output.html \
  STYLE=prism-command \
  BRAND="My Brand"

# 直接 Python 调用
python3 scripts/build_from_readme.py \
  path/to/README.md \
  --output dist/output.html \
  --theme prism-command \
  --brand "My Brand"
```

**自动清洗内容：**
- 删除 GitHub 徽章（badge）图片链接
- 删除 `<div>` HTML 嵌入块
- 删除 fenced code blocks 代码块
- 删除 `assets/` 下的图片引用
- 重命名特定标题（如 "LivePPT 是什么" → "这个项目能做什么"）
- 保留 H1、H2 和正文内容

### 5. 从零生成内容 + HTML

还没有任何内容时，让 LivePPT 自动生成计划草稿并渲染为 HTML。

```bash
# Make 命令（一键到位）
make build-showcase \
  PROJECT="AI 产品发布网页演示" \
  AUDIENCE="技术决策者" \
  STYLE=neo-luxury \
  BRAND="LivePPT" \
  PLAN=plans/showcase.md \
  OUTPUT=dist/index.html

# 分步执行（先出 Markdown，编辑后再渲染）
python3 scripts/generate_showcase_plan.py \
  --project "AI 产品发布网页演示" \
  --audience "技术决策者" \
  --style "neo-luxury" \
  --output plans/showcase.md

# 编辑 plans/showcase.md 修改内容...

python3 scripts/render_plan_to_html.py \
  plans/showcase.md \
  --output dist/index.html \
  --theme neo-luxury \
  --brand "LivePPT"
```

---

## 主题风格

| 主题 | 风格描述 | 适用场景 |
|------|---------|---------|
| `neo-luxury` | 暖色奶油底 + 金棕点缀，高级感 | 企业发布、产品路演 |
| `cyber-pulse` | 深蓝底 + 蓝绿亮色，科技感 | AI 产品、技术发布会 |
| `minimal-editorial` | 纯白底 + 黑色强调色，编辑感 | 课程讲义、作品集 |
| `prism-command` | 深海军蓝 + 亮蓝，控制室风格 | B2B 架构演示 |

## 命令速查表

```bash
# 安装依赖
make install-deps

# 校验项目完整性
make validate

# Markdown → HTML
make render-html PLAN=input.md OUTPUT=dist/out.html STYLE=neo-luxury

# Word → HTML
make convert-docx DOCX_INPUT=input.docx OUTPUT=dist/out.html STYLE=cyber-pulse

# PowerPoint → HTML
make convert-pptx PPTX_INPUT=input.pptx OUTPUT=dist/out.html STYLE=minimal-editorial

# README → HTML（带清洗）
make build-from-readme README_INPUT=README.md OUTPUT=dist/out.html STYLE=prism-command

# 生成内容 + HTML（一步到位）
make build-showcase PROJECT="项目名" AUDIENCE="受众" STYLE=neo-luxury

# 查看帮助
make help
```

## 使用场景

- **开源项目发布**：把更新日志讲成 6-10 屏故事
- **B 端售前演示**：同一内容切不同视觉风格
- **课程讲义**：把知识点按节奏拆成页面
- **产品介绍**：比 README 更有观看路径，比传统 PPT 更轻
- **文档转换**：把 Word 商业计划书、PPT 路演稿快速转为网页

## 项目架构

```
LivePPT/
├── src/                    # 核心模块（v0.2 新增）
│   ├── core/               # 解析引擎与数据模型
│   │   ├── parser.py       # Markdown 解析函数
│   │   ├── deck.py         # 幻灯片数据模型
│   │   └── themes.py       # 主题预设
│   ├── render/             # 渲染层
│   │   ├── html_template.py # HTML 模板
│   │   └── render_plan.py   # CLI 编排
│   ├── converters/         # 文档转换器
│   │   ├── base.py          # 转换器基类
│   │   ├── docx_converter.py # Word → Markdown
│   │   └── pptx_converter.py # PPT → Markdown
│   └── cli/                # CLI 入口
│       ├── convert_docx.py   # .docx → HTML 管线
│       ├── convert_pptx.py   # .pptx → HTML 管线
│       ├── build_from_readme.py
│       ├── build_showcase.py
│       └── clean_markdown.py
├── scripts/                # 向后兼容的包装脚本
├── requirements.txt        # Python 依赖
├── Makefile                # CLI 命令入口
└── examples/               # 示例文件
```

## 当前边界

当前这版已经能解决：
- Markdown / README / Word / PPT 直接出 HTML
- 快速得到一个可演示、可分享的结果
- 同一份内容切换不同主题风格

当前还没完全解决：
- 图片和表格的完整保留与渲染
- 复杂布局自动识别（Word/PPT 中的高级排版）
- 一键导出完整静态站资源包
- 更细粒度的页面模板系统

所以现阶段更适合把它理解成：
**"把内容快速变成演示页"的 MVP**，而不是最终形态的全自动发布会引擎。

## 路线图

- `v0.1.x`：工作流、脚本、文档和 CI 稳定（已完成）
- `v0.2.x`：Word/PPT 导入、模块化架构、主题系统增强（当前版本）
- `v0.3.x`：图片处理增强、更多模板生态、完整静态站导出

详情见 [ROADMAP.md](ROADMAP.md)。

## 开源文档

- [SKILL.md](SKILL.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CHANGELOG.md](CHANGELOG.md)
- [ROADMAP.md](ROADMAP.md)

## License

`MIT + Additional Terms`（附加条款）

- 中文条款：[LICENSE](LICENSE)
- 英文条款：[LICENSE_EN.md](LICENSE_EN.md)

---

如果这个项目对你有帮助，欢迎点一个 **Star**，或提一个 Issue 告诉我你最想要的模板能力。
