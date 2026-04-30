# 每日圣经经文 PWA 设计文档

**日期：** 2026-04-30  
**状态：** 已批准

---

## 目标

构建一个可安装到手机桌面的 PWA 网页，每天自动更新一段圣经经文，用户可按书卷分类浏览经文，并可选择将当前经文发送到自己的邮箱。无需账号，无需订阅，打开即用。

---

## 架构

纯静态网站，托管在 GitHub Pages。GitHub Actions 负责每日更新经文数据文件。无后端服务器。

```
bible-verse-pwa/               # GitHub 仓库根目录
├── data/
│   ├── verses.json            # 全量经文库（~300 条）
│   └── today.json             # 当日经文（Actions 每天更新）
├── index.html                 # PWA 主页面
├── style.css                  # 羊皮纸暖色样式
├── app.js                     # 前端逻辑
├── manifest.json              # PWA 安装配置
├── service-worker.js          # 离线缓存支持
└── .github/workflows/
    └── daily.yml              # 每天 9AM PST 更新 today.json
```

---

## 经文数据

### 来源

手工整理三个版本，存入仓库内的 JSON 文件，不依赖第三方 API：

- **和合本（CUV）**：公版，可自由使用
- **新译和合本（RCUV）**：精选合理使用范围内的经文
- **NIV**：精选合理使用范围内的经文

### 数量

约 300 条精选经文，按分类分布：
- 旧约（`old_testament`）：约 100 条
- 新约非福音书（`new_testament`）：约 100 条
- 福音书（`gospels`）：约 100 条

### 数据格式

```json
{
  "id": "jhn-3-16",
  "book_zh": "约翰福音",
  "book_en": "John",
  "chapter": 3,
  "verse": 16,
  "category": "gospels",
  "cuv": "神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至灭亡，反得永生。",
  "rcuv": "神爱世人，甚至将他的独生子赐给他们，使所有信他的人不致灭亡，反得永生。",
  "niv": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life."
}
```

---

## 每日更新机制

GitHub Actions（`.github/workflows/daily.yml`）配置 cron：`0 17 * * *`（UTC 17:00 = PST 09:00）。

每次运行：
1. 从 `verses.json` 随机选一条经文
2. 写入 `data/today.json`
3. 提交并推送到仓库
4. GitHub Pages 自动部署新文件

前端启动时 `fetch('data/today.json')` 获取当日经文。

---

## PWA 界面

### 视觉风格

羊皮纸暖色系：
- 背景：`#f0e6d6`
- 卡片：`linear-gradient(#fdf8f0, #f7efe2)`，左侧 `5px` 棕色边框
- 主色：`#8b5e3c`，文字 `#3d2b1f`
- 字体：Georgia（衬线），适合经文阅读

### 经文卡片布局

```
┌─────────────────────────────┐
│       每日灵粮 · 日期        │
│  ┌───────────────────────┐  │
│  │  [和合本][新译][NIV]   │  │  ← 版本切换 tab
│  │  「经文正文...」        │  │
│  │ - - - - - - - - - - - │  │
│  │  NIV                  │  │
│  │  "Verse text..."      │  │
│  │  — 约翰福音 3:16       │  │
│  │  [ 发送到我的邮箱 ]    │  │
│  └───────────────────────┘  │
│  [ 旧约 ][ 新约 ][ 福音书 ][ 随机 ] │
└─────────────────────────────┘
```

卡片顶部有版本切换 tab（**和合本 / 新译和合本 / NIV**），点击切换中文译本，NIV 始终显示在下方。默认显示和合本 + NIV。

### 底部导航

四个按钮：**旧约 / 新约 / 福音书 / 随机**

点击任意按钮 → 从对应 `category` 中随机取一条经文 → 更新卡片内容（纯前端，不刷新页面）。

### 发送到邮箱

点击"发送到我的邮箱"按钮：
1. 弹出输入框，用户填写邮箱地址
2. 调用 EmailJS SDK，发送当前经文的 HTML 邮件
3. 邮件样式与网页卡片保持一致（羊皮纸风格）
4. 发送成功显示提示，失败显示错误信息

### PWA 配置

- `manifest.json`：应用名称、图标、主题色（`#8b5e3c`）、`display: standalone`
- `service-worker.js`：缓存 `verses.json` 和静态资源，支持离线查看上次加载的经文
- 手机浏览器打开后提示"添加到主屏幕"

---

## 邮件样式

EmailJS 模板使用 HTML 邮件，样式与 PWA 卡片一致：
- 羊皮纸背景色
- 和合本在上（正文大字），NIV 在下（斜体小字）
- 章节标注：`约翰福音 3:16 / John 3:16`
- 页脚：发送时间

---

## 一次性配置步骤（用户操作）

1. 在 GitHub 创建新仓库，Settings → Pages → 选 `main` 分支部署
2. 注册 [EmailJS](https://emailjs.com) 免费账号，创建 Email Service（连接 Gmail）和 Email Template
3. 在 GitHub 仓库 Settings → Secrets 添加：
   - `EMAILJS_SERVICE_ID`
   - `EMAILJS_TEMPLATE_ID`  
   - `EMAILJS_PUBLIC_KEY`
4. 推送代码后，Actions 自动运行，GitHub Pages 自动部署

---

## 约束与边界

- **不包含**：用户账号、订阅列表、推送通知、后端服务器
- **费用**：完全免费（GitHub Pages 免费，EmailJS 免费 200 封/月）
- **浏览器支持**：现代手机浏览器（Chrome/Safari for iOS & Android）
- **经文版权**：仅收录公版（和合本）及合理使用范围内的经文片段
