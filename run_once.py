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
    item_reports = []
    success_count = 0
    skip_count = 0
    item_index = 1

    for item_name, data in results.items():
        if data is None:
            print(f"[跳过] {item_name} 数据获取失败")
            skip_count += 1
            item_reports.append(f"{item_index}. {item_name}\n   状态: 获取失败")
            item_index += 1
            continue

        volume = data["volume"]
        price = data["price"]
        steamdt_volume = data.get("steamdt_volume")
        steam_volume = data.get("steam_volume")
        steamdt_price = data.get("steamdt_price")
        steam_price = data.get("steam_price")

        # 保存到数据库
        save_volume(item_name, volume, price)
        print(f"[保存] {item_name} -> 成交量: {volume}, 价格: {price}")
        success_count += 1

        # 构建每个饰品的详细报告
        lines = [f"{item_index}. {item_name}"]
        if steamdt_volume is not None:
            lines.append(f"   SteamDT成交: {steamdt_volume}")
        if steam_volume is not None:
            lines.append(f"   Steam成交: {steam_volume}")
        lines.append(f"   今日推算成交: {volume}")
        if steamdt_price is not None:
            lines.append(f"   SteamDT价格: {steamdt_price}元")
        if steam_price is not None:
            lines.append(f"   Steam价格: {steam_price}元")
        item_reports.append("\n".join(lines))
        item_index += 1

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

    # 每次运行都发送采集报告
    report_lines = []
    report_lines.append(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)")
    report_lines.append(f"成功: {success_count}  失败: {skip_count}")
    if alert_count > 0:
        report_lines.append(f"报警: {alert_count} 条 (请查看其他通知)")
    report_lines.append("")
    report_lines.append("\n\n".join(item_reports))

    report_content = "\n".join(report_lines)
    send_wechat_notification("Steam监控采集报告", report_content)
    print(f"\n[OK] 已发送采集报告到微信")
    print(f"[完成] 本次共触发 {alert_count} 条报警")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_once()
    except Exception as e:
        import traceback
        print(f"[错误] 程序异常: {e}")
        traceback.print_exc()
        sys.exit(1)
