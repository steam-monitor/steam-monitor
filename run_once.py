"""
GitHub Actions 单次运行脚本
采集一次数据并发送报警，然后退出
"""
import os
import sys
from datetime import datetime
from db import init_db, save_volume
from collector import monitor_items
from alert import check_volume_alert
from sweeper_alert import check_sweeper_alert
from notification import send_wechat_notification

# 从环境变量读取 SendKey（GitHub Secrets）
import notification
env_key = os.environ.get("SERVERCHAN_SENDKEY")
if env_key:
    notification.SERVERCHAN_SENDKEY = env_key
    notification.SERVERCHAN_API_URL = f"https://sctapi.ftqq.com/{env_key}.send"


def run_once():
    """执行一次采集和报警检测"""
    print("=" * 60)
    print("Steam 饰品成交量监控 - GitHub Actions 单次运行")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)")
    print("=" * 60)

    # 初始化数据库
    init_db()

    # 采集所有饰品数据
    results = monitor_items()

    alert_count = 0

    for item_name, data in results.items():
        if data is None:
            print(f"[跳过] {item_name} 数据获取失败")
            continue

        volume = data["volume"]
        price = data["price"]

        # 保存到数据库
        save_volume(item_name, volume, price)
        print(f"[保存] {item_name} -> 成交量: {volume}, 价格: {price}")

        # 扫货检测
        should_sweeper, sweeper_msg = check_sweeper_alert(item_name, volume)
        if should_sweeper:
            print(f"[扫货报警] {item_name}")
            send_wechat_notification("【扫货报警】疑似有人扫货", sweeper_msg)
            alert_count += 1

        # 成交量异常检测
        should_alert, alert_msg, alert_level = check_volume_alert(item_name, volume)
        if should_alert:
            if alert_level == "critical":
                title = f"【特别重要】{item_name} 成交量异常"
            else:
                title = f"【普通提醒】{item_name} 成交量变化"
            print(f"[报警] {title}")
            send_wechat_notification(title, alert_msg)
            alert_count += 1

    print(f"\n[完成] 本次共触发 {alert_count} 条报警")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_once()
    except Exception as e:
        import traceback
        print(f"[错误] 程序异常: {e}")
        traceback.print_exc()
        sys.exit(1)
