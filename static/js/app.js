/**
 * EduPulse AI — Global Core Application State & UI Controller
 */

// Tab Navigation Switcher
function switchTab(tabId) {
    const tabs = ['youtube', 'pdf', 'roadmap', 'timer'];
    tabs.forEach(tab => {
        const navBtn = document.getElementById(`tab-btn-${tab}`);
        const section = document.getElementById(`section-${tab}`);
        if (tab === tabId) {
            navBtn?.classList.add('active-tab');
            navBtn?.classList.remove('text-slate-400');
            section?.classList.add('active-section');
            section?.classList.remove('hidden');
        } else {
            navBtn?.classList.remove('active-tab');
            navBtn?.classList.add('text-slate-400');
            section?.classList.remove('active-section');
            section?.classList.add('hidden');
        }
    });
}

// Global Loading Overlay Controls
function showLoading(message = 'Analyzing educational material...') {
    const overlay = document.getElementById('global-loading');
    const textEl = document.getElementById('loading-text');
    if (textEl) textEl.textContent = message;
    if (overlay) overlay.classList.remove('hidden');
}

function hideLoading() {
    const overlay = document.getElementById('global-loading');
    if (overlay) overlay.classList.add('hidden');
}

// Universal API Fetch Client Wrapper
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, options);
        let data;
        try {
            data = await response.json();
        } catch (e) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        if (!response.ok) {
            let errorMessage = 'API Request failed';

            if (data.detail) {
                if (typeof data.detail === 'string') {
                    errorMessage = data.detail;
                } else if (Array.isArray(data.detail)) {
                    // Extract FastAPI 422 validation field messages
                    errorMessage = data.detail
                        .map(err => `${err.loc ? err.loc.slice(1).join(' -> ') : 'Field'}: ${err.msg}`)
                        .join('\n');
                } else if (typeof data.detail === 'object') {
                    errorMessage = JSON.stringify(data.detail);
                }
            } else if (data.message) {
                errorMessage = data.message;
            }

            throw new Error(errorMessage);
        }
        return data;
    } catch (error) {
        alert(`Error:\n${error.message}`);
        throw error;
    }
}
