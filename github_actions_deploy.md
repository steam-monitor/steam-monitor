# GitHub Actions 部署指南

把 Steam 饰品监控部署到 GitHub Actions 上，电脑关机也能每小时自动运行并发送微信通知。

---

## 第一步：创建 GitHub 仓库

1. 打开 https://github.com，登录账号（没有账号先注册，免费）
2. 点击右上角的 **+** → **New repository**
3. 填写仓库名，例如 `steam-monitor`
4. 选择 **Private**（私有，保护你的 SendKey）
5. 点击 **Create repository**

---

## 第二步：上传项目代码

在你的电脑上打开命令行（PowerShell），执行：

```powershell
cd "C:\Users\Dell\WorkBuddy\20260403184545"

# 初始化 git
git init
git add .
git commit -m "初始化 Steam 监控项目"

# 连接到你的 GitHub 仓库（把 YOUR_USERNAME 换成你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/steam-monitor.git
git branch -M main
git push -u origin main
```

---

## 第三步：添加 Secrets（保护 SendKey）

1. 打开你的 GitHub 仓库页面
2. 点击 **Settings** → 左侧找 **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 填写：
   - Name: `SERVERCHAN_SENDKEY`
   - Value: `SCT333503TicKpEmfPpjTQP1g630uctuou`
5. 点击 **Add secret**

---

## 第四步：添加 .gitignore 文件

防止数据库文件被上传（数据库用缓存管理）：

```
volume_data.db
__pycache__/
*.pyc
```

---

## 第五步：启用 Actions 并测试

1. 打开仓库页面，点击 **Actions** 标签
2. 你会看到 **Steam 饰品监控** 这个 workflow
3. 点击 **Run workflow** → **Run workflow** 手动触发一次
4. 等待约 1 分钟，看是否运行成功
5. 如果成功，微信就会收到通知（如果有异常的话）

---

## 运行频率说明

- 自动每小时运行一次（整点运行）
- GitHub Actions 免费额度：每月 2000 分钟（每次约 2 分钟，每月用约 60 * 2 = 120 分钟，绰绰有余）

---

## 常见问题

**Q：数据库数据会丢失吗？**
A：不会。GitHub Actions 用 cache 存储数据库文件，每次运行会先恢复上次的数据库，运行完再保存。

**Q：代码有变化怎么更新？**
A：在本地修改代码后，执行：
```powershell
git add .
git commit -m "更新配置"
git push
```

**Q：怎么查看运行日志？**
A：打开 GitHub 仓库 → Actions → 点击最近一次运行 → 点击 `monitor` 任务即可查看。

---

## 总结

部署完成后，就算你的电脑关机，GitHub 的服务器也会每小时自动运行监控，检测到异常就立即发微信通知你！
