"""
通知模块 - 支持桌面弹窗和微信推送
"""
from tkinter import messagebox
import threading
import requests

# Server酱配置
SERVERCHAN_SENDKEY = "SCT333503Ty8CW1mvwhtW3ESp9vRv59kdJ"
SERVERCHAN_API_URL = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"


def show_popup(title, message):
    """
    显示桌面弹窗提醒
    注意：需要在主线程之外调用，否则会阻塞
    """
    def _show():
        try:
            # 隐藏主窗口
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            
            # 显示消息框
            messagebox.showwarning(title, message)
            
            # 销毁窗口
            root.destroy()
        except Exception as e:
            print(f"❌ 弹窗显示失败: {e}")
    
    # 在新线程中显示弹窗，避免阻塞主程序
    thread = threading.Thread(target=_show)
    thread.daemon = True
    thread.start()


def send_wechat_notification(title, content):
    """
    通过 Server酱发送微信通知
    """
    try:
        data = {
            "title": title,
            "desp": content
        }
        resp = requests.post(SERVERCHAN_API_URL, json=data, timeout=10)
        
        if resp.status_code == 200:
            result = resp.json()
            if result.get("code") == 0:
                print("[OK] 微信通知发送成功")
                return True
            else:
                print(f"[FAIL] 微信通知发送失败: {result.get('message')}")
                return False
        else:
            print(f"[FAIL] 微信通知请求失败，状态码: {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"[ERROR] 微信通知发送异常: {e}")
        return False


def show_alert_popup(item_name, alert_msg, alert_level="normal"):
    """
    显示报警弹窗（桌面 + 微信推送）
    alert_level: "normal" = 普通提醒, "critical" = 特别提醒
    """
    if alert_level == "critical":
        title = f"🔴【特别重要】{item_name} 成交量异常"
    else:
        title = f"⚠️【普通提醒】{item_name} 成交量变化"
    
    # 控制台打印
    print(f"\n{'='*50}")
    print(title)
    print(alert_msg)
    print(f"{'='*50}\n")
    
    # 桌面弹窗
    show_popup(title, alert_msg)
    
    # 微信推送（只在报警时推送）
    send_wechat_notification(title, alert_msg)


def send_data_update_notification(item_name, volume, price, steamdt_volume, steam_volume, steamdt_price, steam_price):
    """
    发送数据更新通知（每次采集后推送）
    """
    title = f"📊 {item_name} 数据更新"
    
    content = f"""
🔔 数据采集完成

📊 SteamDT 平台
- 成交量: {steamdt_volume}
- 价格: ¥{steamdt_price}

📈 Steam 官方
- 成交量: {steam_volume}
- 价格: ¥{steam_price}

💰 今日推算成交: {volume}

---
⏰ 采集时间: {datetime_now_str()}
    """.strip()
    
    send_wechat_notification(title, content)


def datetime_now_str():
    """获取当前时间的字符串表示"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
