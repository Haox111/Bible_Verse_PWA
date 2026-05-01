# 每日靈糧 · Daily Verse

每日推送圣经经文的 PWA，和合本繁体中文，托管于 GitHub Pages，无需后端。

**访问地址**：https://haox111.github.io/Bible_Verse_PWA/

---

## 功能

- 每日经文：GitHub Actions 每天 9:00 AM PST 自动随机挑选一节经文
- 分类浏览：按钮切换今日 / 旧约 / 新约 / 福音书 / 随机
- 邮件发送：将当前经文发送到任意邮箱（EmailJS）
- PWA：支持添加到手机桌面

---

## 项目结构

```
├── index.html
├── style.css
├── app.js
├── config.js                # EmailJS 公钥配置
├── manifest.json
├── service-worker.js
├── data/
│   ├── chiun.json           # 和合本全文（~7MB，懒加载）
│   ├── book_meta.json       # 66卷书名及分类
│   └── today.json           # 当日经文（每日自动更新）
├── scripts/
│   └── pick_verse.py
├── tests/
│   └── test_pick_verse.py
└── .github/workflows/
    └── daily.yml
```

---

## 本地运行

```bash
git clone https://github.com/Haox111/Bible_Verse_PWA.git
cd Bible_Verse_PWA
python -m http.server 8080
# 访问 http://localhost:8080
```

直接双击 `index.html` 会因 CORS 无法加载数据，请通过本地服务器访问。

---

## EmailJS 配置

1. 注册 [EmailJS](https://www.emailjs.com/)，连接 Gmail
2. 创建模板，变量：`{{to_email}}`、`{{verse_text}}`、`{{verse_ref}}`
3. 填入 `config.js`：

```js
const EMAILJS_CONFIG = {
  publicKey:  'your_public_key',
  serviceId:  'your_service_id',
  templateId: 'your_template_id',
};
```

---

## 数据来源

圣经数据来自 [scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases)，和合本繁体中文，66卷，31104节。
