"""
数据库模块 - 存储和查询饰品成交量数据
"""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "volume_data.db"


def init_db():
    """初始化数据库表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS volume_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            volume INTEGER,
            price TEXT,
            recorded_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("[OK] 数据库初始化完成")


def save_volume(item_name, volume, price):
    """保存成交量数据"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO volume_log (item_name, volume, price, recorded_at) VALUES (?, ?, ?, ?)",
        (item_name, volume, price, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_yesterday_avg_volume(item_name):
    """获取昨天的平均成交量"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT AVG(volume) FROM volume_log
        WHERE item_name = ?
        AND recorded_at > datetime('now', '-1 day')
        AND recorded_at < datetime('now', '-24 hours')
    """, (item_name,))
    
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] else 0


def get_recent_volumes(item_name, hours=24):
    """获取最近N小时的成交量数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT volume, recorded_at FROM volume_log
        WHERE item_name = ?
        AND recorded_at > datetime('now', '-{} hours')
        ORDER BY recorded_at DESC
    """.format(hours), (item_name,))
    
    results = cursor.fetchall()
    conn.close()
    return results


def get_latest_volume(item_name):
    """获取最新的成交量记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT volume, price, recorded_at FROM volume_log
        WHERE item_name = ?
        ORDER BY recorded_at DESC
        LIMIT 1
    """, (item_name,))
    
    result = cursor.fetchone()
    conn.close()
    return result


def get_volume_n_minutes_ago(item_name, minutes):
    """获取 N 分钟前的成交量"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT volume, price, recorded_at FROM volume_log
        WHERE item_name = ?
        AND recorded_at > datetime('now', '-{} minutes')
        ORDER BY recorded_at ASC
        LIMIT 1
    """.format(minutes), (item_name,))
    
    result = cursor.fetchone()
    conn.close()
    return result
