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
- SendKey: SCT333503TicKpEmfPpjTQP1g630uctuou
- API: https://sct.ftqq.com/{SENDKEY}.send

## 云端部署
- 平台：WorkBuddy自动化任务
- 任务名称：Steam饰品监控
- 运行频率：每小时
- 状态：已激活

## 当前监控饰品
### 已激活（5个）
1. Tec-9 | 晶红石英 (崭新出厂)
2. 化学防害专家 | 特警 (itemId: 808884914023563264)
3. 海军上尉里克索尔 | 海军水面战中心海豹部队 (itemId: 553486490)
4. "蓝莓" 铅弹 | 海军水面战中心海豹部队 (itemId: 808836530722177024)
5. 黑狼 | 军刀 (itemId: 553486487)

### 待补充itemId的探剂（58个）
其余探剂已添加到collector.py配置，monitor_items()函数会自动跳过itemId为"待补充"的项

## 技术要点
- SteamDT API需要从网页手动获取itemId
- 使用total_volume = steamdt_volume + steam_volume（今日推算成交）
- Windows命令行和WeChat通知不支持emoji，已移除所有emoji符号
- monitor_items()函数自动跳过"待补充"项

## 已修复问题
1. Windows命令行emoji编码问题
2. WeChat通知emoji问题
3. 扫货检测算法逻辑错误（改为计算相对涨幅）
