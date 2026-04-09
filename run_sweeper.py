"""
扫货检测独立脚本 - 每10分钟运行一次
只做数据采集 + 扫货检测，不发送常规报告
"""
import os
import sys
from datetime import datetime
from db import init_db, save_volume
from collector import monitor_items
from sweeper_alert import check_sweeper_alert
from notification import send_wechat_notification

# 从环境变量读取 SendKey
import notification
env_key = os.environ.get("SERVERCHAN_SENDKEY")
if env_key:
    notification.SERVERCHAN_SENDKEY = env_key
    notification.SERVERCHAN_API_URL = f"https://sctapi.ftqq.com/{env_key}.send"


def run_sweeper_check():
    """执行一次扫货检测"""
    print("=" * 60)
    print("Steam 扫货检测 - 独立运行")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 初始化数据库
    init_db()

    # 采集所有饰品数据
    results = monitor_items()

    alert_count = 0

    for item_name, data in results.items():
        if data is None:
            continue

        volume = data["volume"]

        # 保存到数据库（保证数据连续性）
        save_volume(item_name, volume, data["price"])

        # 扫货检测
        should_sweeper, sweeper_msg = check_sweeper_alert(item_name, volume)
        if should_sweeper:
            print(f"[扫货报警] {item_name}")
            send_wechat_notification("【扫货报警】疑似有人扫货", sweeper_msg)
            alert_count += 1

    if alert_count == 0:
        print(f"[正常] 未检测到扫货行为")

    print(f"[完成] 本次检测完成，触发 {alert_count} 条扫货报警")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_sweeper_check()
    except Exception as e:
        import traceback
        print(f"[错误] 程序异常: {e}")
        traceback.print_exc()
        sys.exit(1)
