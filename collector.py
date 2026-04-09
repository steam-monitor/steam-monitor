"""数据采集模块 - 从 SteamDT API 获取饰品价格和成交量数据"""
import requests
from datetime import datetime
import time

# 饰品列表配置 (使用 itemId)
# 从 https://steamdt.com/items 手动获取的探剂饰品列表
ITEMS = {
    # ========== 激流大行动 探剂 ==========
    "中队长鲁沙尔·勒库托 | 法国宪兵特勤队": "待补充",
    "指挥官黛维达·费尔南德斯（护目镜） | 海豹蛙人": "待补充",
    "指挥官弗兰克·巴鲁德（湿袜） | 海豹蛙人": "待补充",
    "遗忘者克拉斯沃特 | 游击队": "待补充",
    "克拉斯沃特（三分熟） | 游击队": "待补充",
    "薇帕姐（革新派） | 游击队": "待补充",
    "化学防害上尉 | 法国宪兵特勤队": "待补充",
    "中尉雷克斯·克里奇 | 海豹蛙人": "待补充",
    "残酷的达里尔（穷鬼） | 专业人士": "待补充",
    "精锐捕兽者索尔曼 | 游击队": "待补充",
    "亚诺（野草） | 游击队": "待补充",
    "军医少尉 | 法国宪兵特勤队": "待补充",
    "军官雅克·贝尔特朗 | 法国宪兵特勤队": "914695813570834432",
    "中尉法洛（抱树人） | 特警": "待补充",
    "上校曼戈斯·达比西 | 游击队": "待补充",
    "捕兽者 | 游击队": "待补充",
    "准尉 | 法国宪兵特勤队": "待补充",
    "D中队军官 | 新西兰特种空勤团": "待补充",
    "陆军中尉普里米罗 | 巴西第一营": "待补充",
    "丛林反抗者 | 精锐分子": "待补充",
    "捕兽者（挑衅者） | 游击队": "待补充",

    # ========== 狂牙大行动 探剂 ==========
    "指挥官 梅 '极寒' 贾米森 | 特警": "待补充",
    "残酷的达里尔爵士（迈阿密） | 专业人士": "待补充",
    "残酷的达里尔爵士（沉默） | 专业人士": "待补充",
    "残酷的达里尔爵士（头盖骨） | 专业人士": "待补充",
    "残酷的达里尔爵士（皇家） | 专业人士": "待补充",
    "残酷的达里尔爵士（聒噪） | 专业人士": "待补充",
    "第一中尉法洛 | 特警": "待补充",
    "\"两次\"麦考伊 | 战术空中管制部队装甲兵": "待补充",
    "红衫列赞 | 军刀": "待补充",
    "飞贼波兹曼 | 专业人士": "待补充",
    "老K | 专业人士": "待补充",
    "\"蓝莓\" 铅弹 | 海军水面战中心海豹部队": "808836530722177024",
    "约翰 '范·海伦' 卡斯克 | 特警": "待补充",
    "军士长炸弹森 | 特警": "待补充",
    "出逃的萨莉 | 专业人士": "待补充",
    "小凯夫 | 专业人士": "待补充",
    "化学防害专家 | 特警": "808884914023563264",  # 已有
    "生物防害专家 | 特警": "待补充",
    "德拉戈米尔 | 军刀勇士": "待补充",
    "街头士兵 | 凤凰战士": "待补充",

    # ========== 裂网大行动 探剂 ==========
    "海军上尉里克索尔 | 海军水面战中心海豹部队": "553486490",  # 已有
    "爱娃特工 | 联邦调查局（FBI）": "待补充",
    "\"医生\"罗曼诺夫 | 军刀": "待补充",
    "精英穆哈里克先生 | 精锐分子": "待补充",
    "黑狼 | 军刀": "553486487",
    "迈克·赛弗斯 | 联邦调查局（FBI）狙击手": "待补充",
    "\"两次\"麦考伊 | 美国空军战术空中管制部队": "待补充",
    "沙哈马特教授 | 精锐分子": "待补充",
    "准备就绪的列赞 | 军刀": "待补充",
    "马尔库斯·戴劳 | 联邦调查局（FBI）人质营救队": "待补充",
    "马克西姆斯 | 军刀": "待补充",
    "铅弹 | 海军水面战中心海豹部队": "待补充",
    "奥西瑞斯 | 精锐分子": "待补充",
    "弹弓 | 凤凰战士": "待补充",
    "德拉戈米尔 | 军刀": "待补充",
    "海豹突击队第六分队士兵 | 海军水面战中心海豹部队": "待补充",
    "第三特种兵连 | 德国特种部队突击队": "待补充",
    "特种兵 | 联邦调查局（FBI）特警": "待补充",
    "地面叛军 | 精锐分子": "待补充",
    "执行者 | 凤凰战士": "待补充",
    "枪手 | 凤凰战士": "待补充",
    "B中队指挥官 | 英国空军特别部队": "待补充",

    # ========== 其他饰品（保留） ==========
    "Tec-9 | 晶红石英 (崭新出厂)": "22630",
}

# SteamDT API 接口
STEAMDT_API_URL = "https://api.steamdt.com/item/trade/v1/overview/today"

# 请求头（模拟浏览器）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://steamdt.com/",
    "Origin": "https://steamdt.com",
}


def fetch_steamdt_data(item_id):
    """从 SteamDT API 获取今日成交量数据"""
    timestamp = int(time.time() * 1000)  # 毫秒时间戳
    url = f"{STEAMDT_API_URL}?timestamp={timestamp}&itemId={item_id}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)

        if resp.status_code != 200:
            print(f"[错误] API 请求失败，状态码: {resp.status_code}")
            return None

        # 解析 JSON
        data = resp.json()

        if data.get("success"):
            return data.get("data")
        else:
            print(f"[错误] API 返回错误: {data.get('errorMsg', '未知错误')}")
            return None

    except Exception as e:
        print(f"[错误] 请求异常: {e}")
        return None


def extract_volume_and_price(data):
    """从 SteamDT 数据中提取成交量和价格"""
    if not data or not isinstance(data, dict):
        return None, None

    # SteamDT 返回的数据结构:
    # overview: SteamDT 平台数据
    # steamOverview: Steam 官方数据

    # 获取三个数据
    steamdt_volume = None
    steam_volume = None
    total_volume = None

    # 1. 获取 SteamDT 平台数据
    overview = data.get("overview")
    if overview and isinstance(overview, dict):
        steamdt_volume = overview.get("transactionCount")

    # 2. 获取 Steam 官方数据
    steam_overview = data.get("steamOverview")
    if steam_overview and isinstance(steam_overview, dict):
        steam_volume = steam_overview.get("transactionCount")

    # 3. 计算合计值（今日推算成交）
    if steamdt_volume is not None and steam_volume is not None:
        total_volume = steamdt_volume + steam_volume

    # 优先使用合计值（网页上显示的"今日推算成交"）
    if total_volume is not None:
        price = steam_overview.get("avgPrice") if steam_overview else None
        return total_volume, price

    # 如果合计值不存在，使用 Steam 官方数据
    if steam_volume is not None:
        price = steam_overview.get("avgPrice") if steam_overview else None
        return steam_volume, price

    # 最后使用 SteamDT 数据
    if steamdt_volume is not None:
        price = overview.get("avgPrice") if overview else None
        return steamdt_volume, price

    return None, None


def monitor_items():
    """监控所有饰品，返回最新的成交量数据"""
    results = {}

    for display_name, item_id in ITEMS.items():
        # 跳过待补充itemId的饰品
        if item_id == "待补充":
            print(f"[跳过] {display_name} - itemId 待补充")
            continue

        print(f"\n[采集中] {display_name} (itemId: {item_id})")

        data = fetch_steamdt_data(item_id)
        if data:
            # 提取三个成交量和两个价格
            steamdt_volume = None
            steam_volume = None
            total_volume = None
            steamdt_price = None
            steam_price = None

            # 获取 SteamDT 平台数据（包括价格）
            overview = data.get("overview")
            if overview and isinstance(overview, dict):
                steamdt_volume = overview.get("transactionCount")
                steamdt_price = overview.get("avgPrice")  # SteamDT 平台价格

            # 获取 Steam 官方数据（包括价格）
            steam_overview = data.get("steamOverview")
            if steam_overview and isinstance(steam_overview, dict):
                steam_volume = steam_overview.get("transactionCount")
                steam_price = steam_overview.get("avgPrice")  # Steam 官方价格

            # 计算合计值
            if steamdt_volume is not None and steam_volume is not None:
                total_volume = steamdt_volume + steam_volume

            # 显示所有成交量和价格数据
            print(f"[SteamDT] 成交: {steamdt_volume}, 价格: {steamdt_price}")
            print(f"[Steam] 成交: {steam_volume}, 价格: {steam_price}")
            print(f"[合计] 今日推算成交: {total_volume}")

            # 使用合计值作为主要监控数据
            main_volume = total_volume if total_volume is not None else (steam_volume if steam_volume is not None else steamdt_volume)

            if main_volume is not None:
                print(f"[完成] 监控成交量: {main_volume}, 价格: {steamdt_price}")
                results[display_name] = {
                    "volume": int(main_volume),
                    "price": steamdt_price,  # 使用 SteamDT 价格
                    "steamdt_price": steamdt_price,
                    "steam_price": steam_price,
                    "steamdt_volume": steamdt_volume,
                    "steam_volume": steam_volume,
                    "total_volume": total_volume
                }
            else:
                print(f"[警告] 未能从响应中提取成交量数据")
                print(f"   原始数据: {data}")
                results[display_name] = None
        else:
            print(f"[失败] 数据获取失败")
            results[display_name] = None

    return results


if __name__ == "__main__":
    # 测试代码
    print("=== 测试 SteamDT API ===")
    results = monitor_items()
    print("\n=== 测试结果 ===")
    for name, data in results.items():
        if data:
            print(f"{name}: 成交量={data['volume']}, 价格={data['price']}")
        else:
            print(f"{name}: 获取失败")
