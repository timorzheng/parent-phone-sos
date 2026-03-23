# 📱 爸妈手机急救站

[![Python 版本](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![GitHub Stars](https://img.shields.io/github/stars/timorzheng/parent-phone-sos?style=social)](https://github.com/timorzheng/parent-phone-sos)

**AI 驱动的父母手机远程支持** 🚀

帮助你的父母通过发送截图来远程使用他们的手机。我们的 AI 分析问题，生成分步说明，并在截图上用红圈和箭头标注，这样他们就可以轻松跟随。

[English Version](README.md)

---

## 🎯 问题

你的父母在凌晨 3 点给你发短信："我的手机又出问题了！" 😰

现在，他们可以：
1. 截一张屏幕图
2. 描述他们的问题
3. 收到完美标注的分步说明

## ✨ 功能特性

- 🤖 **AI 分析** - 使用 GPT-4o Vision 或 Claude 理解手机截图
- 📍 **智能标注** - 在截图上绘制红圈、箭头和步骤编号
- 📋 **分步说明** - 每一步都清晰、易于理解
- 🌍 **双语支持** - 英文和中文
- 📱 **响应式设计** - 在所有设备上完美呈现
- 🎨 **美观界面** - 现代、温暖、家庭友好的设计
- 🚀 **高效可靠** - 使用 FastAPI 构建以实现闪电般的性能
- 🐳 **Docker 支持** - 轻松部署
- 💾 **常见问题库** - 30+ 个常见手机问题及解决方案
- 🔄 **提供者自动切换** - 在 OpenAI 和 Anthropic 之间自动切换

## 🚀 快速开始

### 前置条件
- Python 3.8+ 或 Docker
- OpenAI API 密钥（或 Anthropic API 密钥）

### 方式 1: 本地设置

```bash
# 克隆仓库
git clone https://github.com/timorzheng/parent-phone-sos.git
cd parent-phone-sos

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件
cp .env.example .env
# 编辑 .env 并添加你的 API 密钥

# 运行服务器
python -m uvicorn src.main:app --reload
```

在浏览器中打开 http://localhost:8000！

### 方式 2: Docker 部署

```bash
# 复制并配置环境
cp .env.example .env
# 编辑 .env 填入你的 API 密钥

# 使用 docker-compose 构建和运行
docker-compose up -d

# 访问 http://localhost:8000
```

## 📖 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                    用户手机截图                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │   AI 分析 (GPT-4o/Claude)       │
        │  - 识别 UI 元素                  │
        │  - 生成分步说明                  │
        │  - 获取元素坐标                  │
        └───────────────┬──────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │      图像标注                    │
        │  - 绘制红圈                      │
        │  - 添加编号标签                  │
        │  - 绘制指向箭头                  │
        └───────────────┬──────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │   分步说明                       │
        │   (父母易于跟随)                │
        └──────────────────────────────────┘
```

## 🎨 演示

[演示 GIF 即将推出 - 显示标注前后的对比]

## 📚 API 文档

### 端点

#### POST /api/analyze
分析截图并获取说明。

**请求:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@screenshot.png" \
  -F "question=怎样增大字体?"
```

**响应:**
```json
{
  "analysis": {
    "summary": "要增大字体，请打开设置并调整显示选项",
    "steps": [
      {
        "step_number": 1,
        "instruction_text": "打开设置应用",
        "ui_element": "设置图标",
        "coordinates": {"x": 100, "y": 200, "width": 50, "height": 50}
      }
    ],
    "difficulty": "easy",
    "estimated_time": 5,
    "provider": "openai"
  },
  "annotated_image_base64": "iVBORw0KGgoAAAANS..."
}
```

#### GET /api/faq/list
获取所有常见问题。

```bash
curl "http://localhost:8000/api/faq/list"
```

#### GET /api/faq/{id}
获取特定的常见问题。

```bash
curl "http://localhost:8000/api/faq/wifi"
```

#### GET /api/faq/search?q=关键词
按关键词搜索常见问题。

```bash
curl "http://localhost:8000/api/faq/search?q=wifi"
```

#### GET /health
健康检查端点。

```bash
curl "http://localhost:8000/health"
```

## ⚙️ 配置

编辑 `.env` 文件进行自定义：

```env
# AI 提供商
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=your-key
PREFERRED_PROVIDER=openai

# 服务器
HOST=0.0.0.0
PORT=8000
DEBUG=False

# 图像
MAX_IMAGE_SIZE_MB=20
```

## 🧪 测试

运行测试套件：

```bash
# 安装测试依赖
pip install pytest pytest-asyncio

# 运行所有测试
pytest

# 运行覆盖率测试
pytest --cov=src
```

## 📱 支持的平台

- iPhone (iOS)
- Android
- 微信
- Android 设置
- iOS 设置

## 🎓 常见问题库包括

- WiFi 连接
- 字体大小调整
- 存储空间清理
- 应用下载
- 视频通话
- 截图
- 蓝牙配对
- 音量控制
- 通知设置
- 系统更新
- 电池省电
- 亮度调节
- 飞行模式
- 位置服务
- 网络重置
- 屏幕锁定
- 应用权限
- 照片删除
- 密码重置
- 缓存清理
- 还有 10+ 个...

## 🛠️ 技术栈

- **后端:** FastAPI, Python 3.8+
- **AI:** OpenAI GPT-4o Vision 或 Anthropic Claude
- **图像处理:** Pillow (PIL)
- **前端:** 原生 HTML/CSS/JavaScript
- **部署:** Docker, docker-compose
- **测试:** pytest

## 📄 项目结构

```
parent-phone-sos/
├── README.md
├── README_CN.md
├── LICENSE
├── .env.example
├── requirements.txt
├── setup.py
├── Dockerfile
├── docker-compose.yml
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI 应用
│   ├── analyzer.py      # AI 分析
│   ├── annotator.py     # 图像标注
│   ├── models.py        # 数据模型
│   ├── prompts.py       # AI 提示词
│   ├── config.py        # 配置
│   └── faq.py          # 常见问题库
├── web/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
│   ├── test_analyzer.py
│   ├── test_annotator.py
│   └── test_api.py
└── docs/
    ├── API.md
    └── CONTRIBUTING.md
```

## 🤝 贡献

我们欢迎贡献！请参阅 [CONTRIBUTING.md](docs/CONTRIBUTING.md) 获取指南。

1. Fork 这个仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m '添加牛逼功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 用 ❤️ 构建以帮助家庭保持连接
- 受真实的父母技术使用困扰启发
- 特别感谢所有贡献者

## 📧 支持

- 📬 邮件: support@parentphonesos.com
- 💬 GitHub Issues: [报告错误](https://github.com/timorzheng/parent-phone-sos/issues)
- 💡 功能请求: [请求功能](https://github.com/timorzheng/parent-phone-sos/discussions)

---

<div align="center">

**用 ❤️ 构建以帮助家庭保持连接**

[⭐ 在 GitHub 上标星](https://github.com/timorzheng/parent-phone-sos) • [🐛 报告错误](https://github.com/timorzheng/parent-phone-sos/issues) • [💡 请求功能](https://github.com/timorzheng/parent-phone-sos/discussions)

</div>
