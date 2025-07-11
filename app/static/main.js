// Save and restore last prompt
const promptInput = document.getElementById('prompt');
const imageInput = document.getElementById('image');
const form = document.getElementById('analyze-form');
const outputDiv = document.getElementById('output');
const analyzingOverlay = document.getElementById('analyzing-overlay');
const tryAgainBtn = document.getElementById('try-again');
const analyzeBtn = document.getElementById('analyze-btn');
const tokenUsageContainer = document.getElementById('token-usage-container');
const imagePreviewContainer = document.getElementById('image-preview-container');
const imagePreview = document.getElementById('image-preview');

// Restore last prompt
window.addEventListener('DOMContentLoaded', () => {
  const lastPrompt = localStorage.getItem('lastPrompt');
  if (lastPrompt) {
    promptInput.value = lastPrompt;
  }
});

function resetUI() {
  imageInput.value = '';
  outputDiv.innerHTML = '';
  tokenUsageContainer.style.display = 'none';
  tokenUsageContainer.innerHTML = '';
  analyzingOverlay.style.display = 'none';
  tryAgainBtn.style.display = 'none';
  analyzeBtn.style.display = 'inline-block';
  imagePreviewContainer.style.display = 'none';
  imagePreview.src = '';
}

tryAgainBtn.onclick = () => {
  resetUI();
};

imageInput.addEventListener('change', () => {
  if (imageInput.files && imageInput.files[0]) {
    const file = imageInput.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
      imagePreviewContainer.style.display = 'flex';
    };
    reader.readAsDataURL(file);
  } else {
    imagePreviewContainer.style.display = 'none';
    imagePreview.src = '';
  }
});

form.onsubmit = async (e) => {
  e.preventDefault();
  const prompt = promptInput.value.trim();
  if (!prompt) {
    outputDiv.innerHTML = '<div id="error">Prompt is required.</div>';
    return;
  }
  localStorage.setItem('lastPrompt', prompt);
  outputDiv.innerHTML = '';
  tokenUsageContainer.style.display = 'none';
  tokenUsageContainer.innerHTML = '';
  analyzingOverlay.style.display = 'flex';
  tryAgainBtn.style.display = 'none';
  analyzeBtn.style.display = 'none';

  const formData = new FormData();
  formData.append('prompt', prompt);
  if (imageInput.files[0]) {
    formData.append('image', imageInput.files[0]);
  }

  try {
    const response = await fetch('/infer/', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    analyzingOverlay.style.display = 'none';
    tryAgainBtn.style.display = 'inline-block';
    if (response.ok) {
      outputDiv.innerHTML = `<div><strong>Analysis:</strong><br>${data.analysis.replace(/\n/g, '<br>')}</div>`;
      tokenUsageContainer.style.display = 'block';
      tokenUsageContainer.innerHTML = `<strong>Token Usage:</strong><br>${formatTokenUsage(data.token_usage)}`;
    } else {
      outputDiv.innerHTML = `<div id="error">${data.detail || 'An error occurred.'}</div>`;
    }
  } catch (err) {
    analyzingOverlay.style.display = 'none';
    tryAgainBtn.style.display = 'inline-block';
    outputDiv.innerHTML = `<div id="error">Network or server error.</div>`;
  }
};

function formatTokenUsage(tokenUsage) {
  if (!tokenUsage) return '';
  return `
    Total tokens: <strong>${tokenUsage.total_tokens}</strong><br>
    Prompt tokens: <strong>${tokenUsage.prompt_tokens}</strong><br>
    Completion tokens: <strong>${tokenUsage.completion_tokens}</strong><br>
    Total cost: <strong>$${tokenUsage.total_cost}</strong>
  `;
}
