document.addEventListener('DOMContentLoaded', () => {
    // --- Elements ---
    const topicInput = document.getElementById('topic-input');
    const submitBtn = document.getElementById('submit-btn');
    const levelBtns = document.querySelectorAll('.level-btn');
    
    // Result sections
    const emptyState = document.getElementById('empty-state');
    const explanationContainer = document.getElementById('explanation-container');
    const resultText = document.getElementById('result-text');
    const explanationLevelText = document.getElementById('explanation-level-text');
    const copyBtn = document.getElementById('copy-btn');
    
    // History Drawer
    const historyDrawer = document.getElementById('history-drawer');
    const historyOverlay = document.getElementById('history-overlay');
    const openHistoryBtn = document.getElementById('open-history-btn');
    const closeHistoryBtn = document.getElementById('close-history-btn');
    const historyList = document.getElementById('history-list');
    const emptyHistoryMsg = document.getElementById('empty-history-msg');

    // --- State ---
    let currentLevel = 'Age 5';
    let isSubmitting = false;

    // --- LocalStorage ---
    const loadHistory = () => {
        const history = JSON.parse(localStorage.getItem('eli5_history') || '[]');
        return history;
    };

    const saveToHistory = (item) => {
        let history = loadHistory();
        history.unshift(item);
        // Keep only last 10
        if (history.length > 10) history = history.slice(0, 10);
        localStorage.setItem('eli5_history', JSON.stringify(history));
        renderHistory();
    };

    // --- UI Interactions ---
    
    // Level selection toggle
    levelBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Remove active classes
            levelBtns.forEach(b => {
                b.classList.remove('active-level');
                b.classList.add('text-on-surface-variant', 'hover:bg-surface-container');
            });
            // Add to clicked
            e.target.classList.add('active-level');
            e.target.classList.remove('text-on-surface-variant', 'hover:bg-surface-container');
            currentLevel = e.target.dataset.level;
        });
    });

    // History Toggle
    const toggleHistory = () => {
        if (historyDrawer.classList.contains('translate-x-full')) {
            // Open
            historyDrawer.classList.remove('translate-x-full');
            historyOverlay.classList.remove('hidden');
            setTimeout(() => historyOverlay.style.opacity = '1', 10); // Trigger transition
            renderHistory();
        } else {
            // Close
            historyDrawer.classList.add('translate-x-full');
            historyOverlay.style.opacity = '0';
            setTimeout(() => historyOverlay.classList.add('hidden'), 300);
        }
    };

    openHistoryBtn.addEventListener('click', toggleHistory);
    closeHistoryBtn.addEventListener('click', toggleHistory);
    historyOverlay.addEventListener('click', toggleHistory);

    // --- Core Logic ---

    const renderHistory = () => {
        const history = loadHistory();
        historyList.innerHTML = '';
        
        if (history.length === 0) {
            emptyHistoryMsg.style.display = 'block';
            historyList.appendChild(emptyHistoryMsg);
            return;
        }

        history.forEach(entry => {
            const div = document.createElement('div');
            div.className = "bg-surface p-4 rounded-lg cursor-pointer hover:bg-surface-container-low transition border border-surface-container group";
            div.innerHTML = `
                <div class="text-xs font-bold text-primary mb-1 uppercase tracking-wider">${entry.level}</div>
                <div class="font-bold text-on-surface line-clamp-2">${entry.topic}</div>
                <div class="text-xs text-on-surface-variant mt-2">${entry.timestamp || ''}</div>
            `;
            div.addEventListener('click', () => {
                topicInput.value = entry.topic;
                showExplanation(entry.explanation, entry.level);
                toggleHistory(); // Close drawer
            });
            historyList.appendChild(div);
        });
    };

    const setBtnLoading = (loading) => {
        isSubmitting = loading;
        if (loading) {
            submitBtn.innerHTML = `
                <span class="material-symbols-outlined animate-spin" style="font-variation-settings: 'FILL' 1;">sync</span>
                <span>Brainsplaining...</span>
            `;
            submitBtn.classList.add('opacity-80', 'cursor-not-allowed', 'scale-[0.98]');
        } else {
            submitBtn.innerHTML = `
                <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">psychology</span>
                <span>Brainsplain It!</span>
            `;
            submitBtn.classList.remove('opacity-80', 'cursor-not-allowed', 'scale-[0.98]');
        }
    };

    const showExplanation = (text, level) => {
        emptyState.classList.add('hidden');
        explanationContainer.classList.remove('hidden');
        
        // Remove animation class to re-trigger it
        explanationContainer.classList.remove('animate-fade-in');
        void explanationContainer.offsetWidth; // trigger reflow
        explanationContainer.classList.add('animate-fade-in');

        resultText.textContent = text;
        explanationLevelText.textContent = level;
    };

    const showError = (msg) => {
        emptyState.classList.add('hidden');
        explanationContainer.classList.remove('hidden');
        resultText.innerHTML = `<span class="text-error font-bold">${msg}</span>`;
        explanationLevelText.textContent = 'Error';
    };

    // Submitting for explanation
    submitBtn.addEventListener('click', async () => {
        const topic = topicInput.value.trim();
        if (!topic || isSubmitting) return;

        setBtnLoading(true);

        try {
            const res = await fetch('http://localhost:5000/api/explain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic, level: currentLevel })
            });

            const data = await res.json();
            
            if (!res.ok) {
                showError(data.error || 'Something went wrong.');
            } else {
                showExplanation(data.explanation, currentLevel);
                
                // Save to history
                saveToHistory({
                    topic,
                    level: currentLevel,
                    explanation: data.explanation,
                    timestamp: new Date().toLocaleDateString()
                });
            }
        } catch (error) {
            console.error('Fetch error:', error);
            showError('Could not connect to the Brainsplain server. Is it running?');
        } finally {
            setBtnLoading(false);
        }
    });

    // Copy to clipboard
    copyBtn.addEventListener('click', () => {
        const text = resultText.textContent;
        navigator.clipboard.writeText(text).then(() => {
            const originalHTML = copyBtn.innerHTML;
            copyBtn.innerHTML = `<span class="material-symbols-outlined text-[18px]">check</span> Copied!`;
            setTimeout(() => copyBtn.innerHTML = originalHTML, 2000);
        });
    });

    // Initialize UI
    renderHistory();
});
