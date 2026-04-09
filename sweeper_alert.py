"""扫货监控模块 - 检测短时间内成交量暴涨"""
from db import get_volume_n_minutes_ago
from notification import send_wechat_notification


# 扫货配置
SWEEPER_CONFIG = {
    "check_interval_minutes": 10,  # 每 10 分钟检查一次
    "volume_increase_threshold": 1.0,  # 10 分钟内涨 100% 就报警（1.0 = +100%）
}


def check_sweeper_alert(item_name, current_volume):
    """
    检测是否有人扫货
    返回: (是否报警, 报警信息)
    """
    # 获取 10 分钟前的成交量
    prev_data = get_volume_n_minutes_ago(item_name, SWEEPER_CONFIG["check_interval_minutes"])
    
    if not prev_data:
        # 没有 10 分钟前的数据，无法对比
        return False, None
    
    prev_volume = prev_data[0]
    
    if prev_volume == 0:
        # 10 分钟前没有数据
        return False, None
    
    # 计算涨幅
    increase_ratio = (current_volume - prev_volume) / prev_volume
    increase_percent = increase_ratio * 100
    
    # 10 分钟内涨 100% = 疑似扫货
    if increase_ratio >= SWEEPER_CONFIG["volume_increase_threshold"]:
        alert_msg = f"🚨 【扫货报警】疑似有人扫货！\n\n饰品: {item_name}\n10分钟前成交量: {prev_volume}\n当前成交量: {current_volume}\n涨幅: +{increase_percent:.1f}%\n\n⚠️ 可能有人大量囤货，请关注价格变化！"
        return True, alert_msg
    
    return False, None
