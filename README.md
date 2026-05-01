# 每日靈糧 · Daily Verse

每日推送圣经经文的 PWA，和合本繁体中文，托管于 GitHub Pages，无需后端。

**访问地址**：https://haox111.github.io/Bible_Verse_PWA/

---

## 功能

- 每日经文：GitHub Actions 每天 9:00 AM PST 自动随机挑选一节经文
- 分类浏览：按钮切换今日 / 旧约 / 新约 / 福音书 / 詩篇 / 箴言 / 随机
- 邮件发送：将当前经文发送到任意邮箱（EmailJS）
- PWA：支持添加到手机桌面

---

## 更新日志

### 2026-04-30
- 整体视觉风格重设计，羊皮纸暖色调
- 卡片字体加大，桌面端响应式适配
- App 图标更新为十字架
- 分类按钮新增「詩篇」和「箴言」，现支持：今日 / 旧约 / 新约 / 福音书 / 詩篇 / 箴言 / 随机

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

## 安装到设备

### 手机（iOS）

1. 用 Safari 打开网址
2. 点底部分享按钮（方块加箭头）
3. 选「添加到主屏幕」
4. 点右上角「添加」

### 手机（Android）

1. 用 Chrome 打开网址
2. 点右上角菜单（三个点）
3. 选「添加到主屏幕」或「安装应用」

### 电脑（Chrome）

1. 用 Chrome 打开网址
2. 点地址栏右侧的安装图标（电脑屏幕加箭头）
3. 点「安装」
4. 桌面会出现快捷方式，点击直接打开，无地址栏

---

## 数据来源

圣经数据来自 [scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases)，和合本繁体中文，66卷，31104节。
