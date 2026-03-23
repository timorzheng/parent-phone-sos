/* Parent Phone SOS - Frontend JavaScript */

let selectedFile = null;
let currentAnalysis = null;

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

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadFAQ();
});

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
    dropZone.style.display = 'none';
    fileInfo.style.display = 'flex';
    fileName.textContent = `✓ Selected: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    clearError();
}

function clearFile() {
    selectedFile = null;
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

    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('question', question);

    const provider = providerSelect.value;
    if (provider) {
        formData.append('provider', provider);
    }

    // Show loading
    analyzeBtn.disabled = true;
    loadingIndicator.style.display = 'block';
    resultsSection.style.display = 'none';
    clearError();

    try {
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
        displayResults(result);
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

// Display Results
function displayResults(result) {
    const analysis = result.analysis;

    // Summary
    summaryText.textContent = analysis.summary;

    // Metadata badges
    const diffClass = `difficulty-${analysis.difficulty}`;
    difficultyBadge.className = diffClass;
    difficultyBadge.textContent = `📊 ${analysis.difficulty.charAt(0).toUpperCase() + analysis.difficulty.slice(1)}`;

    timeBadge.className = '';
    timeBadge.textContent = `⏱️ ${analysis.estimated_time} mins`;

    providerBadge.className = '';
    providerBadge.textContent = `🤖 ${analysis.provider === 'openai' ? 'GPT-4o' : 'Claude'}`;

    // Annotated image
    if (result.annotated_image_base64) {
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
    button.style.color = '#27AE60';

    setTimeout(() => {
        element.innerHTML = originalText;
        element.style.backgroundColor = '';
        element.style.color = '';
    }, 2000);
}

// FAQ
async function loadFAQ() {
    try {
        const response = await fetch('/api/faq/list');
        const data = await response.json();

        faqContainer.innerHTML = '';
        data.items.slice(0, 6).forEach(item => {
            const faqElement = createFAQElement(item);
            faqContainer.appendChild(faqElement);
        });
    } catch (error) {
        console.error('Failed to load FAQ:', error);
    }
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
