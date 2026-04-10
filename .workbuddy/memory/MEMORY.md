# Steam饰品监控项目 - 长期记忆

## 用户偏好
- 不想收到太多信息，只关注异常情况
- 需要微信实时推送（手机查看）
- 监控时间间隔：1小时采集一次

## 监控规则
### 成交量报警
- 对比昨天平均成交量
- ±10% ~ ±30%：普通提醒
- ±超过30%：特别重要提醒

### 扫货报警
- 对比10分钟前成交量
- 涨幅100%及以上：立即发送扫货报警
- 不受1小时采集间隔限制

## 微信通知配置
- 平台：Server酱 (https://sct.ftqq.com)
- SendKey: SCT333503Ty8CW1mvwhtW3ESp9vRv59kdJ
- API: https://sct.ftqq.com/{SENDKEY}.send

## 云端部署
### GitHub Actions（主部署）
- 仓库：https://github.com/steam-monitor/steam-monitor（公开）
- 工作流：.github/workflows/monitor.yml
- 运行频率：每小时整点自动触发
- 状态：已激活
- Secret名称：SERVERCHAN_KEY
- 数据持久化：actions/cache 缓存 volume_data.db
- keep-alive：.github/workflows/keep-alive.yml，每天7点推送空commit保持活跃
- 2026-04-09：改为公开仓库解决私有仓库定时任务不触发问题

### 网络加速
- 之前用奇游加速器（需付费）
- 后用SteamCommunity302免费加速（有时不稳定）
- 偶尔有502错误，重启SteamCommunity302可解决

### WorkBuddy自动化任务（备用）
- steam-3：主监控，每小时
- steam-4：扫货检测，每小时
- 状态：已激活

## 当前监控饰品
### 已激活（6个）
1. Tec-9 | 晶红石英 (崭新出厂) (itemId: 22630)
2. 化学防害专家 | 特警 (itemId: 808884914023563264)
3. 海军上尉里克索尔 | 海军水面战中心海豹部队 (itemId: 553486490)
4. "蓝莓" 铅弹 | 海军水面战中心海豹部队 (itemId: 808836530722177024)
5. 黑狼 | 军刀 (itemId: 553486487)
6. 军官雅克·贝尔特朗 | 法国宪兵特勤队 (itemId: 914695813570834432)

### 待补充itemId的探剂（57个）
其余探剂已添加到collector.py配置，monitor_items()函数会自动跳过itemId为"待补充"的项

## 技术要点
- SteamDT API需要从网页手动获取itemId
- 使用total_volume = steamdt_volume + steam_volume（今日推算成交）
- Windows命令行和WeChat通知不支持emoji，已移除所有emoji符号
- monitor_items()函数自动跳过"待补充"项

## 通知颜色（2026-04-09新增）
- 成交量上涨/暴涨：深红色 (#8B0000)
- 成交量下跌/暴跌：深绿色 (#006400)
- 扫货报警：深红色 (#8B0000)
- 使用 Server酱 Markdown 的 `<font color="">` 标签实现

## 已修复问题
1. Windows命令行emoji编码问题
2. WeChat通知emoji问题
3. 扫货检测算法逻辑错误（改为计算相对涨幅）
