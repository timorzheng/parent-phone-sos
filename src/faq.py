"""FAQ database for Parent Phone SOS."""

from typing import Dict, List
from src.models import FAQItem

FAQ_DATABASE: Dict[str, FAQItem] = {
    "wifi": FAQItem(
        id="wifi",
        category="连接WiFi",
        category_en="Connect to WiFi",
        steps=[
            "打开手机设置 (Open Settings)",
            "找到WiFi选项 (Find WiFi option)",
            "打开WiFi开关 (Turn on WiFi)",
            "选择你的WiFi网络 (Select your WiFi network)",
            "输入密码 (Enter password)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "font_size": FAQItem(
        id="font_size",
        category="调大字体",
        category_en="Increase Font Size",
        steps=[
            "打开手机设置 (Open Settings)",
            "进入显示设置 (Go to Display settings)",
            "找到字体大小选项 (Find Font Size option)",
            "向右滑动来增大字体 (Slide right to increase size)",
            "确认更改 (Confirm changes)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "storage": FAQItem(
        id="storage",
        category="清理内存",
        category_en="Clear Storage Space",
        steps=[
            "打开设置 (Open Settings)",
            "进入存储空间 (Go to Storage)",
            "查看占用空间最多的应用 (See what takes most space)",
            "删除不需要的应用或照片 (Delete unused apps or photos)",
            "重启手机 (Restart phone)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "download_app": FAQItem(
        id="download_app",
        category="下载应用",
        category_en="Download an App",
        steps=[
            "打开应用商店 (Open App Store/Play Store)",
            "点击搜索 (Tap Search)",
            "输入应用名称 (Type app name)",
            "点击获取或安装 (Tap Get or Install)",
            "验证身份 (Verify identity if needed)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "video_call": FAQItem(
        id="video_call",
        category="视频通话",
        category_en="Video Call on WeChat",
        steps=[
            "打开微信 (Open WeChat)",
            "找到要通话的联系人 (Find the contact)",
            "点击他们的聊天窗口 (Tap their chat)",
            "点击右上角的视频通话按钮 (Tap video call button in top right)",
            "等待对方接听 (Wait for them to answer)",
        ],
        platforms=["WeChat"],
    ),
    "screenshot": FAQItem(
        id="screenshot",
        category="截图",
        category_en="Take a Screenshot",
        steps=[
            "iPhone: 同时按下音量+按钮和侧边按钮 (Press volume+ and side button together)",
            "Android: 同时按下电源和音量-按钮 (Press power and volume- together)",
            "稍等一秒 (Wait for 1 second)",
            "截图会自动保存到图库 (Screenshot saves to gallery automatically)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "bluetooth": FAQItem(
        id="bluetooth",
        category="蓝牙配对",
        category_en="Pair Bluetooth Device",
        steps=[
            "打开设置 (Open Settings)",
            "进入蓝牙设置 (Go to Bluetooth)",
            "打开蓝牙开关 (Turn on Bluetooth)",
            "选择你的设备 (Select your device)",
            "输入配对码 (Enter pairing code if needed)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "volume": FAQItem(
        id="volume",
        category="调节音量",
        category_en="Adjust Volume",
        steps=[
            "按手机侧边的音量按钮 (Press volume buttons on the side)",
            "向上增大音量，向下减小 (Up to increase, down to decrease)",
            "屏幕上会显示音量条 (Volume bar appears on screen)",
            "调整到适合的位置 (Adjust to comfortable level)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "notifications": FAQItem(
        id="notifications",
        category="关闭通知",
        category_en="Turn Off Notifications",
        steps=[
            "打开设置 (Open Settings)",
            "进入通知设置 (Go to Notifications)",
            "选择要关闭通知的应用 (Select the app)",
            "关闭允许通知开关 (Toggle off Allow Notifications)",
            "返回完成 (Go back and done)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "system_update": FAQItem(
        id="system_update",
        category="系统更新",
        category_en="System Update",
        steps=[
            "打开设置 (Open Settings)",
            "进入关于手机 (Go to About Phone)",
            "找到系统更新选项 (Find System Update)",
            "点击检查更新 (Tap Check for Update)",
            "如有更新，点击立即更新 (If available, tap Update Now)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "battery": FAQItem(
        id="battery",
        category="省电模式",
        category_en="Enable Battery Saver",
        steps=[
            "打开设置 (Open Settings)",
            "进入电池设置 (Go to Battery)",
            "找到电池健康或省电模式 (Find Battery Health or Saver Mode)",
            "打开省电模式 (Turn on Battery Saver)",
            "确认 (Confirm)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "brightness": FAQItem(
        id="brightness",
        category="调节亮度",
        category_en="Adjust Brightness",
        steps=[
            "从屏幕顶部向下滑 (Swipe down from top of screen)",
            "在控制中心找到亮度条 (Find brightness slider)",
            "向右增亮，向左变暗 (Right to brighten, left to darken)",
            "调整到舒适的亮度 (Adjust to comfortable level)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "airplane_mode": FAQItem(
        id="airplane_mode",
        category="飞行模式",
        category_en="Enable Airplane Mode",
        steps=[
            "打开设置 (Open Settings)",
            "进入飞行模式选项 (Find Airplane Mode)",
            "打开飞行模式开关 (Turn on Airplane Mode)",
            "屏幕顶部会显示飞行模式图标 (Airplane icon appears at top)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "location": FAQItem(
        id="location",
        category="定位服务",
        category_en="Enable Location Services",
        steps=[
            "打开设置 (Open Settings)",
            "进入隐私设置 (Go to Privacy)",
            "找到位置服务 (Find Location Services)",
            "打开开关 (Turn on the switch)",
            "选择应用权限 (Choose app permissions)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "reset_network": FAQItem(
        id="reset_network",
        category="重置网络设置",
        category_en="Reset Network Settings",
        steps=[
            "打开设置 (Open Settings)",
            "进入系统设置 (Go to System)",
            "找到重置选项 (Find Reset options)",
            "选择重置网络设置 (Tap Reset Network Settings)",
            "输入密码确认 (Enter password to confirm)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "screen_lock": FAQItem(
        id="screen_lock",
        category="屏幕锁定",
        category_en="Set Screen Lock",
        steps=[
            "打开设置 (Open Settings)",
            "进入安全设置 (Go to Security)",
            "找到屏幕锁定选项 (Find Screen Lock)",
            "选择锁定方式 (Choose lock type: PIN, pattern, face, fingerprint)",
            "按提示完成设置 (Follow prompts to complete)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "app_permissions": FAQItem(
        id="app_permissions",
        category="应用权限",
        category_en="Manage App Permissions",
        steps=[
            "打开设置 (Open Settings)",
            "进入应用管理 (Go to Apps)",
            "选择一个应用 (Select an app)",
            "进入权限设置 (Go to Permissions)",
            "启用或关闭所需权限 (Enable/disable needed permissions)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "delete_photos": FAQItem(
        id="delete_photos",
        category="删除照片",
        category_en="Delete Photos",
        steps=[
            "打开照片应用 (Open Photos app)",
            "进入相册 (Go to an album)",
            "点击选择 (Tap Select)",
            "选择要删除的照片 (Choose photos to delete)",
            "点击删除并确认 (Tap Delete and confirm)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "password_reset": FAQItem(
        id="password_reset",
        category="忘记密码",
        category_en="Password Reset",
        steps=[
            "在登录屏幕上点击忘记密码 (Tap Forgot Password on login)",
            "验证身份信息 (Verify your identity)",
            "选择接收重置链接的方式 (Choose how to receive reset link)",
            "按照邮件或短信中的说明 (Follow instructions in email/SMS)",
            "设置新密码 (Set a new password)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "clear_cache": FAQItem(
        id="clear_cache",
        category="清除缓存",
        category_en="Clear App Cache",
        steps=[
            "打开设置 (Open Settings)",
            "进入应用管理 (Go to Apps)",
            "选择应用 (Select the app)",
            "点击存储 (Tap Storage)",
            "点击清除缓存 (Tap Clear Cache)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "auto_lock": FAQItem(
        id="auto_lock",
        category="自动锁屏时间",
        category_en="Auto-Lock Screen Time",
        steps=[
            "打开设置 (Open Settings)",
            "进入显示和亮度 (Go to Display & Brightness)",
            "找到自动锁屏选项 (Find Auto-Lock)",
            "选择时间间隔 (Select time interval)",
            "确认设置 (Confirm)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "keyboard_settings": FAQItem(
        id="keyboard_settings",
        category="键盘设置",
        category_en="Keyboard Settings",
        steps=[
            "打开设置 (Open Settings)",
            "进入语言和输入法 (Go to Language & Input)",
            "选择键盘设置 (Select Keyboard settings)",
            "启用或禁用自动更正 (Enable/disable autocorrect)",
            "调整键盘大小 (Adjust keyboard size)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "reset_phone": FAQItem(
        id="reset_phone",
        category="恢复出厂设置",
        category_en="Factory Reset",
        steps=[
            "备份重要数据 (Back up important data)",
            "打开设置 (Open Settings)",
            "进入系统设置 (Go to System)",
            "找到恢复出厂设置 (Find Factory Reset)",
            "确认操作 (Confirm the operation)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "hotspot": FAQItem(
        id="hotspot",
        category="个人热点",
        category_en="Personal Hotspot",
        steps=[
            "打开设置 (Open Settings)",
            "进入个人热点 (Go to Personal Hotspot)",
            "打开开关 (Turn on the switch)",
            "记下WiFi名称和密码 (Note the WiFi name and password)",
            "其他设备可以连接该WiFi (Other devices can now connect)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "accessibility": FAQItem(
        id="accessibility",
        category="辅助功能",
        category_en="Accessibility Features",
        steps=[
            "打开设置 (Open Settings)",
            "进入辅助功能 (Go to Accessibility)",
            "找到所需功能 (Find the feature you need)",
            "启用该功能 (Enable the feature)",
            "根据需要调整设置 (Adjust settings as needed)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "search_app": FAQItem(
        id="search_app",
        category="搜索应用",
        category_en="Search for an App",
        steps=[
            "进入应用商店首页 (Go to App Store home)",
            "点击下方的搜索标签 (Tap the Search tab at bottom)",
            "输入应用名称 (Type the app name)",
            "从结果中选择正确的应用 (Select the correct app from results)",
            "点击获取或查看 (Tap Get or View)",
        ],
        platforms=["iPhone", "Android"],
    ),
    "backup": FAQItem(
        id="backup",
        category="备份数据",
        category_en="Backup Your Data",
        steps=[
            "打开设置 (Open Settings)",
            "登录你的账户 (Sign in to your account)",
            "找到云同步选项 (Find Cloud Sync option)",
            "选择要备份的内容 (Select what to back up)",
            "打开自动备份 (Enable automatic backup)",
        ],
        platforms=["iPhone", "Android"],
    ),
}


def get_faq_by_id(faq_id: str) -> FAQItem | None:
    """Get a specific FAQ item by ID."""
    return FAQ_DATABASE.get(faq_id)


def get_all_faq() -> List[FAQItem]:
    """Get all FAQ items."""
    return list(FAQ_DATABASE.values())


def search_faq(keyword: str) -> List[FAQItem]:
    """Search FAQ items by keyword (category name or description)."""
    keyword_lower = keyword.lower()
    results = []
    for item in FAQ_DATABASE.values():
        if (
            keyword_lower in item.category.lower()
            or keyword_lower in item.category_en.lower()
        ):
            results.append(item)
    return results
