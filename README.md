# Steam 饰品成交量监控系统

自动监控 CS2/CSGO 饰品成交量，发现异常时触发桌面弹窗提醒。

---

## 功能特性

✅ **自动采集** - 每小时从 Steam 官方 API 获取数据  
✅ **数据存储** - 所有数据存储在本地 SQLite 数据库  
✅ **智能报警** - 成交量比昨天涨 50% 自动报警  
✅ **桌面弹窗** - 异常时弹出窗口提醒  
✅ **多饰品支持** - 可轻松添加更多监控目标  

---

## 安装依赖

```bash
pip install requests
```

---

## 使用方法

### 1. 启动监控

```bash
python main.py
```

### 2. 停止监控

按 `Ctrl + C` 停止程序

---

## 配置说明

### 修改监控饰品

编辑 `collector.py` 文件，在 `ITEMS` 字典中添加或修改饰品：

```python
ITEMS = {
    "Tec-9 | 晶红石英 (Minimal Wear)": "Tec-9%20%7C%20Crystal%20Magenta%20(Minimal%20Wear)",
    "AK-47 | 红线 (久经沙场)": "AK-47%20%7C%20Redline%20(Field-Tested)",
    # 添加更多饰品...
}
```

### 修改报警阈值

编辑 `alert.py` 文件：

```python
ALERT_CONFIG = {
    "volume_increase_threshold": 1.5,  # 涨 50% 报警
    "volume_decrease_threshold": 0.5,  # 跌 50% 报警
}
```

### 修改采集间隔

编辑 `main.py` 文件：

```python
COLLECTION_INTERVAL = 3600  # 3600 秒 = 1小时
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `main.py` | 主程序，定时采集和监控 |
| `collector.py` | 数据采集模块，调用 Steam API |
| `db.py` | 数据库模块，存储数据 |
| `alert.py` | 报警检测模块 |
| `notification.py` | 桌面弹窗提醒模块 |
| `volume_data.db` | 本地数据库（自动生成） |

---

## 注意事项

- **首次运行需要积累数据**：程序需要至少运行 24 小时才能对比昨天的成交量
- **Steam API 限制**：请合理设置采集间隔，避免频繁请求
- **程序需要一直运行**：保持程序运行才能持续监控

---

## 查看历史数据

可以使用 SQLite 客户端查看 `volume_data.db` 文件，或运行：

```python
from db import get_recent_volumes
data = get_recent_volumes("Tec-9 | 晶红石英 (Minimal Wear)", hours=24)
print(data)
```

---

## 常见问题

**Q: 为什么第一次运行没有报警？**  
A: 报警需要对比昨天的数据，首次运行没有历史数据参考。

**Q: 如何获取饰品名称？**  
A: 在 Steam 市场搜索饰品，URL 中的 `market_hash_name` 参数就是饰品名称。

**Q: 可以监控多件饰品吗？**  
A: 可以，在 `collector.py` 中的 `ITEMS` 字典添加更多饰品即可。
