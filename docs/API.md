# Parent Phone SOS - API Documentation

Complete API reference for Parent Phone SOS backend.

## Base URL

```
http://localhost:8000
or
https://your-domain.com
```

## Authentication

Currently, the API does not require authentication. Rate limiting is applied per IP address.

## Rate Limiting

- **Limit:** 100 requests per hour
- **Headers:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Response Format

All responses are in JSON format.

### Success Response

```json
{
  "status": "success",
  "data": {}
}
```

### Error Response

```json
{
  "detail": "Error message"
}
```

## Endpoints

### 1. Health Check

**GET /health**

Check if the service is running.

**Response:** `200 OK`
```json
{
  "status": "ok",
  "service": "Parent Phone SOS",
  "version": "0.1.0"
}
```

### 2. API Information

**GET /api/info**

Get API information and capabilities.

**Response:** `200 OK`
```json
{
  "name": "Parent Phone SOS",
  "version": "0.1.0",
  "description": "AI-powered remote phone support for parents",
  "providers": ["openai", "anthropic"],
  "max_image_size_mb": 20,
  "allowed_formats": ["jpeg", "jpg", "png", "webp"]
}
```

### 3. Analyze Screenshot

**POST /api/analyze**

Analyze a screenshot and get step-by-step instructions.

**Request Parameters:**
- `file` (required): Screenshot image file (multipart/form-data)
- `question` (required): Problem description
- `provider` (optional): AI provider ('openai' or 'anthropic')

**Example:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@screenshot.png" \
  -F "question=How do I connect to WiFi?" \
  -F "provider=openai"
```

**Response:** `200 OK`
```json
{
  "analysis": {
    "summary": "To connect to WiFi, open Settings and select WiFi",
    "steps": [
      {
        "step_number": 1,
        "instruction_text": "Open the Settings app",
        "ui_element": "Settings icon",
        "coordinates": {
          "x": 50,
          "y": 100,
          "width": 60,
          "height": 60
        }
      }
    ],
    "difficulty": "easy",
    "estimated_time": 5,
    "provider": "openai"
  },
  "annotated_image_base64": "iVBORw0KGgoAAAANS..."
}
```

**Error Responses:**

- `400 Bad Request`: Missing required fields
- `413 Payload Too Large`: File exceeds max size
- `415 Unsupported Media Type`: Invalid file format
- `500 Internal Server Error`: Analysis failed

### 4. Get FAQ List

**GET /api/faq/list**

Get all frequently asked questions.

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "wifi",
      "category": "连接WiFi",
      "category_en": "Connect to WiFi",
      "steps": [
        "打开手机设置 (Open Settings)",
        "找到WiFi选项 (Find WiFi option)",
        "打开WiFi开关 (Turn on WiFi)"
      ],
      "platforms": ["iPhone", "Android"]
    }
  ],
  "count": 30
}
```

### 5. Get Specific FAQ

**GET /api/faq/{id}**

Get a specific FAQ item by ID.

**Parameters:**
- `id` (path): FAQ item ID (e.g., 'wifi', 'font_size')

**Example:**
```bash
curl http://localhost:8000/api/faq/wifi
```

**Response:** `200 OK`
```json
{
  "id": "wifi",
  "category": "连接WiFi",
  "category_en": "Connect to WiFi",
  "steps": [
    "打开手机设置 (Open Settings)",
    "找到WiFi选项 (Find WiFi option)",
    "打开WiFi开关 (Turn on WiFi)",
    "选择你的WiFi网络 (Select your WiFi network)",
    "输入密码 (Enter password)"
  ],
  "platforms": ["iPhone", "Android"]
}
```

**Error Responses:**
- `404 Not Found`: FAQ item not found

### 6. Search FAQ

**GET /api/faq/search**

Search FAQ items by keyword.

**Query Parameters:**
- `q` (required): Search keyword (minimum 2 characters)

**Example:**
```bash
curl "http://localhost:8000/api/faq/search?q=bluetooth"
```

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "bluetooth",
      "category": "蓝牙配对",
      "category_en": "Pair Bluetooth Device",
      "steps": [
        "打开设置 (Open Settings)",
        "进入蓝牙设置 (Go to Bluetooth)",
        "打开蓝牙开关 (Turn on Bluetooth)",
        "选择你的设备 (Select your device)",
        "输入配对码 (Enter pairing code if needed)"
      ],
      "platforms": ["iPhone", "Android"]
    }
  ],
  "count": 1
}
```

**Error Responses:**
- `400 Bad Request`: Search query too short

## Data Models

### AnalysisResult

```json
{
  "summary": "string - Brief description of the solution",
  "steps": [
    {
      "step_number": "integer - Step number (1-indexed)",
      "instruction_text": "string - What the user should do",
      "ui_element": "string - Name of the UI element",
      "coordinates": {
        "x": "integer - X coordinate in pixels",
        "y": "integer - Y coordinate in pixels",
        "width": "integer - Width in pixels",
        "height": "integer - Height in pixels"
      }
    }
  ],
  "difficulty": "string - 'easy', 'medium', or 'hard'",
  "estimated_time": "integer - Time in minutes",
  "provider": "string - 'openai' or 'anthropic'"
}
```

### FAQItem

```json
{
  "id": "string - Unique identifier",
  "category": "string - Category name in Chinese",
  "category_en": "string - Category name in English",
  "steps": ["string - Solution steps"],
  "platforms": ["string - Applicable platforms"]
}
```

## Examples

### Example 1: Analyze WiFi Connection Issue

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@wifi-settings.png" \
  -F "question=I can't find the WiFi settings on my phone"
```

**Response:**
```json
{
  "analysis": {
    "summary": "To find WiFi settings, open the Settings app",
    "steps": [
      {
        "step_number": 1,
        "instruction_text": "Tap on the Settings app on your home screen",
        "ui_element": "Settings icon",
        "coordinates": {"x": 300, "y": 600, "width": 80, "height": 80}
      },
      {
        "step_number": 2,
        "instruction_text": "Tap on WiFi",
        "ui_element": "WiFi option",
        "coordinates": {"x": 100, "y": 150, "width": 200, "height": 50}
      }
    ],
    "difficulty": "easy",
    "estimated_time": 2,
    "provider": "openai"
  },
  "annotated_image_base64": "..."
}
```

### Example 2: Get All FAQ Items

**Request:**
```bash
curl http://localhost:8000/api/faq/list
```

**Response:**
```json
{
  "items": [
    {
      "id": "wifi",
      "category": "连接WiFi",
      "category_en": "Connect to WiFi",
      "steps": [...],
      "platforms": ["iPhone", "Android"]
    },
    {
      "id": "font_size",
      "category": "调大字体",
      "category_en": "Increase Font Size",
      "steps": [...],
      "platforms": ["iPhone", "Android"]
    }
  ],
  "count": 30
}
```

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request succeeded |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource not found |
| 413 | Payload Too Large - File too large |
| 415 | Unsupported Media Type - Invalid file format |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)

**Maximum file size:** 20 MB

## Error Handling

Always check the HTTP status code:

```javascript
fetch('/api/analyze', {
  method: 'POST',
  body: formData
})
.then(response => {
  if (!response.ok) {
    return response.json().then(error => {
      throw new Error(error.detail);
    });
  }
  return response.json();
})
.catch(error => {
  console.error('Error:', error.message);
});
```

## Rate Limiting

Requests are limited to 100 per hour per IP address. When limit is exceeded, you'll receive a `429 Too Many Requests` response.

## CORS

CORS is enabled for all origins. You can call the API from frontend JavaScript without issues.

## Timeout

API requests have a 60-second timeout for image analysis.

## Best Practices

1. **Compression:** Compress images before upload to improve performance
2. **Question Quality:** Write clear, specific questions for better results
3. **Error Handling:** Always handle errors gracefully in your client
4. **Caching:** Consider caching FAQ responses on the client side
5. **Testing:** Use `/api/health` to verify connectivity

## Support

For issues or questions about the API, please open an issue on GitHub:
https://github.com/yourusername/parent-phone-sos/issues
