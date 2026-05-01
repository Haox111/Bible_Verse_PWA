# 每日靈糧 · Daily Verse

一个每日推送圣经经文的 Progressive Web App（PWA），采用和合本繁体中文版，托管于 GitHub Pages，无需后端。

🌐 **访问地址**：[https://haox111.github.io/Bible_Verse_PWA/](https://haox111.github.io/Bible_Verse_PWA/)

---

## 功能特色

- 📖 **每日经文**：GitHub Actions 每天早上 9:00 AM PST 自动从全本和合本中随机挑选一节经文
- 🔀 **分类浏览**：点击按钮可随机切换「今日 / 旧约 / 新约 / 福音书 / 随机」经文
- 📧 **邮件发送**：可将当前经文发送到任意邮箱（由 EmailJS 驱动）
- 📱 **PWA 安装**：支持添加到手机桌面，像原生 App 一样使用
- ⚡ **纯静态**：无服务器、无数据库、完全免费部署

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 托管 | GitHub Pages |
| 经文数据 | 和合本 chiun.json（[scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases)） |
| 每日更新 | GitHub Actions（cron `0 17 * * *`） |
| 邮件发送 | [EmailJS](https://www.emailjs.com/)（免费，200封/月） |
| 离线缓存 | Service Worker（Cache-first 策略） |

---

## 项目结构

```
├── index.html               # 主页面
├── style.css                # 羊皮纸暖色主题样式
├── app.js                   # 核心逻辑（加载经文、分类切换、发送邮件）
├── config.js                # EmailJS 配置（公钥，可放心提交）
├── manifest.json            # PWA 清单
├── service-worker.js        # 离线缓存 Service Worker
├── data/
│   ├── chiun.json           # 和合本全文（~7MB，按需懒加载）
│   ├── book_meta.json       # 66卷书的中英文名及分类信息
│   └── today.json           # 当日经文（由 GitHub Actions 每日更新）
├── scripts/
│   └── pick_verse.py        # 随机选经文脚本（加权随机，正比于章节数）
├── tests/
│   └── test_pick_verse.py   # pytest 测试（6项）
└── .github/workflows/
    └── daily.yml            # 每日自动更新 workflow
```

---

## 本地运行

```bash
# 克隆项目
git clone https://github.com/Haox111/Bible_Verse_PWA.git
cd Bible_Verse_PWA

# 启动本地服务器（需要 Python 3）
python -m http.server 8080

# 访问 http://localhost:8080
```

> ⚠️ 直接双击 `index.html` 会因浏览器 CORS 策略无法加载 JSON 数据，请务必通过本地服务器访问。

---

## EmailJS 配置

1. 注册 [EmailJS](https://www.emailjs.com/) 账号，连接你的 Gmail
2. 创建邮件模板，变量使用：
   - `{{to_email}}` — 收件人
   - `{{verse_text}}` — 经文内容
   - `{{verse_ref}}` — 书卷章节
3. 将你的凭据填入 `config.js`：

```js
const EMAILJS_CONFIG = {
  publicKey:  'your_public_key',
  serviceId:  'your_service_id',
  templateId: 'your_template_id',
};
```

---

## GitHub Actions 每日更新

`.github/workflows/daily.yml` 在每天 UTC 17:00（即 PST 09:00）自动运行：

1. 读取 `data/chiun.json` 和 `data/book_meta.json`
2. 按章节数加权随机选取一节经文
3. 写入 `data/today.json`
4. 提交并推送，GitHub Pages 自动部署

也可以在 GitHub Actions 页面手动触发（`workflow_dispatch`）。

---

## 数据来源

圣经数据使用 [scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases) 提供的开源和合本（ChiUn），繁体中文，共 66 卷、31104 节。
