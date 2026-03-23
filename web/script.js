/* Parent Phone SOS - Frontend JavaScript */

let selectedFile = null;
let currentAnalysis = null;
let isDemoMode = false;
let originalImage = null;

// Hardcoded FAQ data for offline support
const FAQ_DATA = [
  { category: "连接WiFi", category_en: "Connect to WiFi", platforms: ["iPhone", "Android"] },
  { category: "调大字体", category_en: "Increase Font Size", platforms: ["iPhone", "Android"] },
  { category: "清理内存", category_en: "Clear Memory/Storage", platforms: ["iPhone", "Android"] },
  { category: "下载安装App", category_en: "Download & Install App", platforms: ["iPhone", "Android"] },
  { category: "微信视频通话", category_en: "WeChat Video Call", platforms: ["iPhone", "Android"] },
  { category: "怎么截图", category_en: "Take a Screenshot", platforms: ["iPhone", "Android"] },
  { category: "蓝牙连接", category_en: "Bluetooth Pairing", platforms: ["iPhone", "Android"] },
  { category: "调节音量", category_en: "Adjust Volume", platforms: ["iPhone", "Android"] },
  { category: "关闭通知", category_en: "Turn Off Notifications", platforms: ["iPhone", "Android"] },
  { category: "更新系统", category_en: "System Update", platforms: ["iPhone", "Android"] },
  { category: "设置闹钟", category_en: "Set an Alarm", platforms: ["iPhone", "Android"] },
  { category: "打开手电筒", category_en: "Turn On Flashlight", platforms: ["iPhone", "Android"] },
  { category: "切换深色模式", category_en: "Switch to Dark Mode", platforms: ["iPhone", "Android"] },
  { category: "查看存储空间", category_en: "Check Storage Space", platforms: ["iPhone", "Android"] },
  { category: "设置壁纸", category_en: "Change Wallpaper", platforms: ["iPhone", "Android"] }
];

// Demo mode responses with keyword matching
const DEMO_RESPONSES = {
  "wifi": {
    summary: "Here is how to connect to WiFi on your phone",
    difficulty: "easy",
    estimated_time: 2,
    steps: [
      { instruction_text: "Open Settings app - look for the gear icon ⚙️", ui_element: "Settings icon on home screen" },
      { instruction_text: "Tap on \"WiFi\" or \"WLAN\"", ui_element: "WiFi option in settings menu" },
      { instruction_text: "Toggle WiFi ON if it is off", ui_element: "WiFi toggle switch" },
      { instruction_text: "Find your home WiFi name in the list and tap it", ui_element: "WiFi network name" },
      { instruction_text: "Enter the WiFi password and tap \"Connect\"", ui_element: "Password field and Connect button" }
    ]
  },
  "font": {
    summary: "Here is how to increase the font size on your phone",
    difficulty: "easy",
    estimated_time: 1,
    steps: [
      { instruction_text: "Open Settings app ⚙️", ui_element: "Settings icon" },
      { instruction_text: "Tap \"Display\" or \"Display & Brightness\"", ui_element: "Display option" },
      { instruction_text: "Tap \"Font Size\" or \"Text Size\"", ui_element: "Font Size option" },
      { instruction_text: "Drag the slider to the RIGHT to make text bigger", ui_element: "Size slider" }
    ]
  },
  "screenshot": {
    summary: "Here is how to take a screenshot",
    difficulty: "easy",
    estimated_time: 1,
    steps: [
      { instruction_text: "For iPhone: Press Side button + Volume Up at the same time", ui_element: "Physical buttons" },
      { instruction_text: "For Android: Press Power + Volume Down at the same time", ui_element: "Physical buttons" },
      { instruction_text: "The screenshot will flash and save to your Photos/Gallery", ui_element: "Photos app" }
    ]
  },
  "default": {
    summary: "I analyzed your screenshot and here are the steps to help",
    difficulty: "medium",
    estimated_time: 3,
    steps: [
      { instruction_text: "Look at the screenshot above - the demo shows general guidance", ui_element: "Your uploaded screenshot" },
      { instruction_text: "Start by tapping the button or menu item you need to interact with", ui_element: "First element to tap" },
      { instruction_text: "Follow the sequence of steps", ui_element: "Continue with next steps" },
      { instruction_text: "If you see a confirmation dialog, tap \"OK\" or \"Confirm\"", ui_element: "Confirmation button" }
    ]
  }
};

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const clearFileBtn = document.getElementById('clearFileBtn');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const questionInput = document.getElementById('questionInput');
const providerSelect = document.getElementById('providerSelect');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const resultsSection = document.getElementById('resultsSection');
const imageContainer = document.getElementById('imageContainer');
const annotatedImage = document.getElementById('annotatedImage');
const downloadImageBtn = document.getElementById('downloadImageBtn');
const summaryText = document.getElementById('summaryText');
const difficultyBadge = document.getElementById('difficultyBadge');
const timeBadge = document.getElementById('timeBadge');
const providerBadge = document.getElementById('providerBadge');
const stepsContainer = document.getElementById('stepsContainer');
const copyStepsBtn = document.getElementById('copyStepsBtn');
const shareText = document.getElementById('shareText');
const copyShareBtn = document.getElementById('copyShareBtn');
const faqContainer = document.getElementById('faqContainer');
const demoBanner = document.getElementById('demoBanner');
const demoModeIndicator = document.getElementById('demoModeIndicator');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkAPIAvailability();
    setupEventListeners();
    loadFAQ();
});

// Check if API is available
async function checkAPIAvailability() {
    try {
        const response = await fetch('/health', {
            method: 'GET',
            signal: AbortSignal.timeout(2000)
        });
        isDemoMode = !response.ok;
    } catch (error) {
        isDemoMode = true;
    }

    // Show demo banner if in demo mode
    if (isDemoMode && demoBanner) {
        demoBanner.style.display = 'block';
    }
}

// Event Listeners
function setupEventListeners() {
    // File upload
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    clearFileBtn.addEventListener('click', clearFile);

    // Drag and drop
    dropZone.addEventListener('dragover', handleDragOver);
    dropZone.addEventListener('dragleave', handleDragLeave);
    dropZone.addEventListener('drop', handleDrop);
    dropZone.addEventListener('click', () => fileInput.click());

    // Analysis
    analyzeBtn.addEventListener('click', analyzeScreenshot);

    // Copy buttons
    copyStepsBtn.addEventListener('click', copyStepsToClipboard);
    copyShareBtn.addEventListener('click', copyShareToClipboard);
    downloadImageBtn.addEventListener('click', downloadAnnotatedImage);
}

// File Handling
function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        selectFile(files[0]);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    dropZone.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        selectFile(files[0]);
    }
}

function selectFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file (JPEG, PNG, etc.)');
        return;
    }

    // Validate file size (20MB max)
    const maxSizeMB = 20;
    if (file.size > maxSizeMB * 1024 * 1024) {
        showError(`File is too large. Maximum size: ${maxSizeMB}MB`);
        return;
    }

    selectedFile = file;

    // Store original image for demo mode
    const reader = new FileReader();
    reader.onload = (e) => {
        originalImage = e.target.result;
    };
    reader.readAsDataURL(file);

    dropZone.style.display = 'none';
    fileInfo.style.display = 'flex';
    fileName.textContent = `✓ Selected: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    clearError();
}

function clearFile() {
    selectedFile = null;
    originalImage = null;
    fileInput.value = '';
    dropZone.style.display = 'block';
    fileInfo.style.display = 'none';
    resultsSection.style.display = 'none';
}

// Analysis
async function analyzeScreenshot() {
    // Validate inputs
    if (!selectedFile) {
        showError('Please select a screenshot first');
        return;
    }

    const question = questionInput.value.trim();
    if (!question) {
        showError('Please describe your problem');
        return;
    }

    // Show loading
    analyzeBtn.disabled = true;
    loadingIndicator.style.display = 'block';
    resultsSection.style.display = 'none';
    clearError();

    try {
        if (isDemoMode) {
            // Demo mode: generate mock response
            await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate delay
            const demoResult = generateDemoResponse(question);
            displayResults(demoResult, true);
        } else {
            // Production mode: call API
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('question', question);

            const provider = providerSelect.value;
            if (provider) {
                formData.append('provider', provider);
            }

            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Analysis failed');
            }

            const result = await response.json();
            currentAnalysis = result;
            displayResults(result, false);
        }

        resultsSection.style.display = 'block';

        // Scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }, 100);

    } catch (error) {
        console.error('Analysis error:', error);
        showError(error.message || 'Failed to analyze screenshot. Please try again.');
    } finally {
        loadingIndicator.style.display = 'none';
        analyzeBtn.disabled = false;
    }
}

// Generate demo response based on keywords
function generateDemoResponse(question) {
    const lowerQuestion = question.toLowerCase();
    let responseKey = 'default';

    // Keyword matching
    if (lowerQuestion.includes('wifi') || lowerQuestion.includes('网络')) {
        responseKey = 'wifi';
    } else if (lowerQuestion.includes('font') || lowerQuestion.includes('字体') || lowerQuestion.includes('size')) {
        responseKey = 'font';
    } else if (lowerQuestion.includes('screenshot') || lowerQuestion.includes('截图')) {
        responseKey = 'screenshot';
    }

    const response = DEMO_RESPONSES[responseKey];
    return {
        analysis: response,
        is_demo: true
    };
}

// Display Results
function displayResults(result, isDemo = false) {
    const analysis = result.analysis;

    // Summary
    summaryText.textContent = analysis.summary;

    // Metadata badges
    const diffClass = `difficulty-${analysis.difficulty}`;
    difficultyBadge.className = diffClass;
    difficultyBadge.textContent = `📊 ${analysis.difficulty.charAt(0).toUpperCase() + analysis.difficulty.slice(1)}`;

    timeBadge.className = '';
    timeBadge.textContent = `⏱️ ${analysis.estimated_time} mins`;

    if (isDemo) {
        providerBadge.className = '';
        providerBadge.textContent = `🎨 Demo Mode`;
    } else {
        providerBadge.className = '';
        providerBadge.textContent = `🤖 ${analysis.provider === 'openai' ? 'GPT-4o' : 'Claude'}`;
    }

    // Image handling
    if (isDemo && originalImage) {
        // Show original image with demo banner
        annotatedImage.src = originalImage;
        imageContainer.style.display = 'block';

        // Add demo mode indicator to image if it doesn't exist
        if (!document.getElementById('demoBanner')) {
            const demoBannerDiv = document.createElement('div');
            demoBannerDiv.className = 'demo-image-banner';
            demoBannerDiv.innerHTML = '🎨 Demo Mode - In production, this image would have red circles and arrows';
            imageContainer.insertBefore(demoBannerDiv, annotatedImage);
        }
    } else if (result.annotated_image_base64) {
        annotatedImage.src = `data:image/png;base64,${result.annotated_image_base64}`;
        imageContainer.style.display = 'block';
    } else {
        imageContainer.style.display = 'none';
    }

    // Steps
    stepsContainer.innerHTML = '';
    analysis.steps.forEach((step, index) => {
        const stepElement = createStepElement(step, index + 1);
        stepsContainer.appendChild(stepElement);
    });

    // Share text
    const shareContent = generateShareText(analysis);
    shareText.value = shareContent;
}

function createStepElement(step, stepNum) {
    const div = document.createElement('div');
    div.className = 'step';

    let coordinatesInfo = '';
    if (step.coordinates) {
        const coords = step.coordinates;
        coordinatesInfo = `\n📍 Location: (${coords.x}, ${coords.y}) Size: ${coords.width}×${coords.height}px`;
    }

    div.innerHTML = `
        <div class="step-content">
            <div class="step-number">${stepNum}</div>
            <div class="step-text">
                <div class="instruction">${escapeHtml(step.instruction_text)}</div>
                <div class="element">${escapeHtml(step.ui_element)}</div>
            </div>
        </div>
    `;

    return div;
}

// Utility Functions
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
}

function clearError() {
    errorMessage.style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function generateShareText(analysis) {
    let text = `📱 PHONE SETUP INSTRUCTIONS\n`;
    text += `━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
    text += `Goal: ${analysis.summary}\n`;
    text += `Difficulty: ${analysis.difficulty}\n`;
    text += `Time needed: ~${analysis.estimated_time} minutes\n\n`;
    text += `STEPS:\n`;
    text += `━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;

    analysis.steps.forEach((step, index) => {
        text += `STEP ${index + 1}:\n`;
        text += `${step.instruction_text}\n`;
        text += `(Tap on: ${step.ui_element})\n\n`;
    });

    text += `━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
    text += `✓ All done! Let me know if you need help.\n`;
    text += `Need more support? Visit: Parent Phone SOS`;

    return text;
}

async function copyStepsToClipboard() {
    if (!currentAnalysis) return;

    const text = generateShareText(currentAnalysis.analysis);
    try {
        await navigator.clipboard.writeText(text);
        showNotification(copyStepsBtn, 'Copied to clipboard!');
    } catch (error) {
        showError('Failed to copy to clipboard');
    }
}

async function copyShareToClipboard() {
    const text = shareText.value;
    try {
        await navigator.clipboard.writeText(text);
        showNotification(copyShareBtn, 'Copied for sharing!');
    } catch (error) {
        showError('Failed to copy to clipboard');
    }
}

function downloadAnnotatedImage() {
    if (!currentAnalysis || !currentAnalysis.annotated_image_base64) {
        showError('No image available');
        return;
    }

    const link = document.createElement('a');
    link.href = `data:image/png;base64,${currentAnalysis.annotated_image_base64}`;
    link.download = `phone-sos-${new Date().getTime()}.png`;
    link.click();

    showNotification(downloadImageBtn, 'Image downloaded!');
}

function showNotification(element, message) {
    const originalText = element.innerHTML;
    element.textContent = message;
    element.style.backgroundColor = '#D5F4E6';
    element.style.color = '#27AE60';

    setTimeout(() => {
        element.innerHTML = originalText;
        element.style.backgroundColor = '';
        element.style.color = '';
    }, 2000);
}

// FAQ
function loadFAQ() {
    // First try to load from API
    if (!isDemoMode) {
        fetch('/api/faq/list')
            .then(response => response.json())
            .then(data => {
                faqContainer.innerHTML = '';
                data.items.slice(0, 6).forEach(item => {
                    const faqElement = createFAQElement(item);
                    faqContainer.appendChild(faqElement);
                });
            })
            .catch(error => {
                console.error('Failed to load FAQ from API, using hardcoded data:', error);
                loadHardcodedFAQ();
            });
    } else {
        // In demo mode, use hardcoded FAQ
        loadHardcodedFAQ();
    }
}

function loadHardcodedFAQ() {
    faqContainer.innerHTML = '';
    FAQ_DATA.slice(0, 6).forEach(item => {
        const faqElement = createFAQElement(item);
        faqContainer.appendChild(faqElement);
    });
}

function createFAQElement(item) {
    const div = document.createElement('div');
    div.className = 'faq-item';

    const platformsText = item.platforms.join(', ');

    div.innerHTML = `
        <div class="faq-title">${escapeHtml(item.category)}</div>
        <div class="faq-category">${escapeHtml(item.category_en)}</div>
        <div class="faq-platforms">${escapeHtml(platformsText)}</div>
    `;

    div.addEventListener('click', () => {
        questionInput.value = item.category_en;
        showNotification(div, 'Added to question!');
        setTimeout(() => {
            questionInput.scrollIntoView({ behavior: 'smooth' });
        }, 500);
    });

    return div;
}
