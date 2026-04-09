"""
Steam 饰品成交量监控系统 - 主程序
定时采集数据、存储、检测异常、触发报警
"""
import time
import sys
from datetime import datetime
from db import init_db, save_volume
from collector import monitor_items
from alert import check_volume_alert
from sweeper_alert import check_sweeper_alert
from notification import show_alert_popup, send_wechat_notification


# 配置
COLLECTION_INTERVAL = 3600  # 采集间隔（秒），3600 = 1小时


def print_banner():
    """打印启动横幅"""
    print("\n" + "="*60)
    print("Steam 饰品成交量监控系统")
    print("="*60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"采集间隔: {COLLECTION_INTERVAL / 60} 分钟")
    print(f"报警阈值: 成交量变化超过 10% 提醒, 超过 30% 特别提醒")
    print("="*60 + "\n")


def run_monitor():
    """运行监控主循环"""
    while True:
        print(f"\n{'='*60}")
        print(f"开始采集数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # 采集所有饰品的数据
        results = monitor_items()
        
        # 处理每个饰品
        for item_name, data in results.items():
            if data is None:
                continue
            
            volume = data["volume"]
            price = data["price"]
            steamdt_volume = data.get("steamdt_volume")
            steam_volume = data.get("steam_volume")
            steamdt_price = data.get("steamdt_price")
            steam_price = data.get("steam_price")
            
            # 保存数据到数据库
            save_volume(item_name, volume, price)
            print(f"[完成] 数据已保存: {item_name} -> 成交量: {volume}, 价格: {price}")
            
            # 检测扫货（10 分钟内涨 100%）
            should_sweeper_alert, sweeper_msg = check_sweeper_alert(item_name, volume)
            if should_sweeper_alert:
                print(f"[扫货报警] 疑似有人扫货！")
                send_wechat_notification("🚨【扫货报警】", sweeper_msg)
            
            # 检测报警（和昨天对比）
            should_alert, alert_msg, alert_level = check_volume_alert(item_name, volume)
            if should_alert:
                if alert_level == "critical":
                    print(f"[特别报警] 触发重要提醒！")
                else:
                    print(f"[普通提醒] 触发提醒")
                show_alert_popup(item_name, alert_msg, alert_level)
        
        print(f"\n[完成] 本次采集完成，等待 {COLLECTION_INTERVAL / 60} 分钟后下次采集...")
        print(f"[计划] 下次采集时间: {(datetime.fromtimestamp(time.time() + COLLECTION_INTERVAL)).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 等待下一次采集
        time.sleep(COLLECTION_INTERVAL)


def main():
    """主函数"""
    try:
        # 打印启动信息
        print_banner()
        
        # 初始化数据库
        print("[初始化] 正在初始化数据库...")
        init_db()
        
        # 开始监控
        print("\n[启动] 监控系统启动！\n")
        print("[提示] 按 Ctrl+C 可以停止程序\n")
        print("-" * 60)
        
        run_monitor()
        
    except KeyboardInterrupt:
        print("\n\n[停止] 程序已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n[错误] 程序异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
