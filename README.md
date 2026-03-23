# 📱 Parent Phone SOS

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![GitHub Stars](https://img.shields.io/github/stars/timorzheng/parent-phone-sos?style=social)](https://github.com/timorzheng/parent-phone-sos)

**AI-powered remote phone support for parents** 🚀

Help your parents use their phones remotely by sending them a screenshot. Our AI analyzes the problem, generates step-by-step instructions, and annotates the screenshot with red circles and arrows so they can easily follow along.

[中文版本 (Chinese)](README_CN.md)

---

## 🎯 The Problem

Your parents text you at 3 AM: "Something's wrong with my phone again!" 😰

Instead of trying to guess what they're doing over a phone call, they can now:
1. Take a screenshot
2. Describe their problem
3. Receive perfectly annotated, step-by-step instructions

## ✨ Features

- 🤖 **AI-Powered Analysis** - GPT-4o Vision or Claude to understand phone screenshots
- 📍 **Smart Annotation** - Red circles, arrows, and numbered steps overlaid on the screenshot
- 📋 **Step-by-Step Instructions** - Clear, jargon-free instructions for each step
- 🌍 **Bilingual** - English and Chinese support
- 📱 **Mobile Responsive** - Works beautifully on all devices
- 🎨 **Beautiful UI** - Modern, warm, family-friendly design
- 🚀 **Fast & Reliable** - Built with FastAPI for lightning-fast performance
- 🐳 **Docker Support** - Easy deployment with Docker
- 💾 **FAQ Database** - 30+ common phone problems with ready-made solutions
- 🔄 **Provider Fallback** - Automatically switches between OpenAI and Anthropic

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ or Docker
- OpenAI API key (or Anthropic API key)

### Option 1: Local Setup

```bash
# Clone the repository
git clone https://github.com/timorzheng/parent-phone-sos.git
cd parent-phone-sos

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Run the server
python -m uvicorn src.main:app --reload
```

Open http://localhost:8000 in your browser!

### Option 2: Docker Deployment

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Build and run with docker-compose
docker-compose up -d

# Access at http://localhost:8000
```

## 📖 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    User Screenshot                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │   AI Analysis (GPT-4o/Claude)   │
        │  - Identify UI elements          │
        │  - Generate step-by-step steps   │
        │  - Get element coordinates       │
        └───────────────┬──────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │      Image Annotation            │
        │  - Draw red circles              │
        │  - Add numbered labels           │
        │  - Draw pointing arrows          │
        └───────────────┬──────────────────┘
                        │
                        ▼
        ┌──────────────────────────────────┐
        │   Step-by-Step Instructions      │
        │   (Easy for parents to follow)  │
        └──────────────────────────────────┘
```

## 🎨 Demo

[GIF Demo coming soon - showing before/after annotated screenshots]

## 📚 API Documentation

### Endpoints

#### POST /api/analyze
Analyze a screenshot and get instructions.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@screenshot.png" \
  -F "question=How do I increase the font size?"
```

**Response:**
```json
{
  "analysis": {
    "summary": "To increase font size, open Settings and adjust display options",
    "steps": [
      {
        "step_number": 1,
        "instruction_text": "Open Settings app",
        "ui_element": "Settings icon",
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
Get all FAQ items.

```bash
curl "http://localhost:8000/api/faq/list"
```

#### GET /api/faq/{id}
Get a specific FAQ item.

```bash
curl "http://localhost:8000/api/faq/wifi"
```

#### GET /api/faq/search?q=keyword
Search FAQ by keyword.

```bash
curl "http://localhost:8000/api/faq/search?q=wifi"
```

#### GET /health
Health check endpoint.

```bash
curl "http://localhost:8000/health"
```

## ⚙️ Configuration

Edit `.env` file to customize:

```env
# AI Providers
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=your-key
PREFERRED_PROVIDER=openai

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Image
MAX_IMAGE_SIZE_MB=20
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run with coverage
pytest --cov=src
```

## 📱 Supported Platforms

- iPhone (iOS)
- Android
- WeChat
- Android Settings
- iOS Settings

## 🎓 FAQ Database Includes

- WiFi Connection
- Font Size Adjustment
- Storage Cleanup
- App Download
- Video Calls
- Screenshots
- Bluetooth Pairing
- Volume Control
- Notifications
- System Updates
- Battery Saver
- Brightness
- Airplane Mode
- Location Services
- Network Reset
- Screen Lock
- App Permissions
- Photo Deletion
- Password Reset
- Cache Clearing
- And 10+ more...

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python 3.8+
- **AI:** OpenAI GPT-4o Vision or Anthropic Claude
- **Image Processing:** Pillow (PIL)
- **Frontend:** Vanilla HTML/CSS/JavaScript
- **Deployment:** Docker, docker-compose
- **Testing:** pytest

## 📄 Project Structure

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
│   ├── main.py          # FastAPI app
│   ├── analyzer.py      # AI analysis
│   ├── annotator.py     # Image annotation
│   ├── models.py        # Data models
│   ├── prompts.py       # AI prompts
│   ├── config.py        # Configuration
│   └── faq.py          # FAQ database
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

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ to help families stay connected
- Inspired by the real frustrations of helping parents use technology
- Special thanks to all contributors

## 📧 Support

- 📬 Email: support@parentphonesos.com
- 💬 GitHub Issues: [Report a bug](https://github.com/timorzheng/parent-phone-sos/issues)
- 💡 Feature Requests: [Request a feature](https://github.com/timorzheng/parent-phone-sos/discussions)

---

<div align="center">

**Made with ❤️ to help families stay connected**

[⭐ Star on GitHub](https://github.com/timorzheng/parent-phone-sos) • [🐛 Report Bug](https://github.com/timorzheng/parent-phone-sos/issues) • [💡 Request Feature](https://github.com/timorzheng/parent-phone-sos/discussions)

</div>
