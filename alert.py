"""
报警检测模块 - 检测成交量异常并触发报警
"""
from db import get_yesterday_avg_volume, get_latest_volume


# 报警配置
ALERT_CONFIG = {
    "volume_normal_threshold": 0.1,   # 成交量变化超过 10% 就普通提醒（0.1 = ±10%）
    "volume_critical_threshold": 0.3, # 成交量变化超过 30% 就特别提醒（0.3 = ±30%）
}


def check_volume_alert(item_name, current_volume):
    """
    检查成交量是否异常
    返回: (是否报警, 报警信息, 报警级别)
    报警级别: "normal" = 普通, "critical" = 特别, None = 不报警
    """
    yesterday_avg = get_yesterday_avg_volume(item_name)
    
    if yesterday_avg == 0:
        print(f"[警告] {item_name}: 没有昨天的数据作为对比")
        return False, None, None
    
    change_ratio = current_volume / yesterday_avg
    change_percent = (change_ratio - 1) * 100
    
    # 成交量暴涨（超过 30%）
    if change_percent >= ALERT_CONFIG["volume_critical_threshold"] * 100:
        alert_msg = f"🚨 [特别提醒] 成交量暴涨！\n\n饰品: {item_name}\n昨日均量: {yesterday_avg:.0f}\n当前成交量: {current_volume}\n涨幅: +{change_percent:.1f}%"
        return True, alert_msg, "critical"
    
    # 成交量暴跌（超过 30%）
    elif change_percent <= -ALERT_CONFIG["volume_critical_threshold"] * 100:
        alert_msg = f"🚨 [特别提醒] 成交量暴跌！\n\n饰品: {item_name}\n昨日均量: {yesterday_avg:.0f}\n当前成交量: {current_volume}\n跌幅: {change_percent:.1f}%"
        return True, alert_msg, "critical"
    
    # 成交量上涨（超过 10%）
    elif change_percent >= ALERT_CONFIG["volume_normal_threshold"] * 100:
        alert_msg = f"⚠️ [普通提醒] 成交量上涨\n\n饰品: {item_name}\n昨日均量: {yesterday_avg:.0f}\n当前成交量: {current_volume}\n涨幅: +{change_percent:.1f}%"
        return True, alert_msg, "normal"
    
    # 成交量下跌（超过 10%）
    elif change_percent <= -ALERT_CONFIG["volume_normal_threshold"] * 100:
        alert_msg = f"⚠️ [普通提醒] 成交量下跌\n\n饰品: {item_name}\n昨日均量: {yesterday_avg:.0f}\n当前成交量: {current_volume}\n跌幅: {change_percent:.1f}%"
        return True, alert_msg, "normal"
    
    return False, None, None
