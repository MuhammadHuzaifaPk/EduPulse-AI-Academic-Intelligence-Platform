/**
 * EduPulse AI — YouTube Intelligence Module
 */

async function handleYouTubeSubmit(event) {
    if (event) event.preventDefault();

    const inputEl = document.getElementById('yt-url-input');
    const urlValue = inputEl ? inputEl.value.trim() : '';

    if (!urlValue) {
        alert('Please paste a YouTube video URL first.');
        return;
    }

    if (typeof showLoading === 'function') {
        showLoading('Extracting YouTube transcript & generating executive summary...');
    }

    try {
        const response = await fetch('/api/v1/youtube/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ url: urlValue })
        });

        const data = await response.json();

        if (!response.ok) {
            let detailMsg = 'Failed to summarize YouTube video.';
            if (data.detail) {
                detailMsg = typeof data.detail === 'string' 
                    ? data.detail 
                    : JSON.stringify(data.detail);
            }
            throw new Error(detailMsg);
        }

        renderYouTubeResults(data);
    } catch (err) {
        console.error('YouTube Processing Error:', err);
        alert(`Error:\n${err.message}`);
    } finally {
        if (typeof hideLoading === 'function') {
            hideLoading();
        }
    }
}

function renderYouTubeResults(data) {
    // 1. Reveal output container
    const container = document.getElementById('yt-output-container');
    if (container) {
        container.classList.remove('hidden');
    }

    // 2. Executive Summary
    const summaryEl = document.getElementById('yt-executive-summary');
    if (summaryEl) {
        summaryEl.innerHTML = data.summary || 'Summary generated successfully.';
    }

    // 3. Key Takeaways
    const takeawaysEl = document.getElementById('yt-takeaways-list');
    if (takeawaysEl && Array.isArray(data.takeaways)) {
        takeawaysEl.innerHTML = data.takeaways
            .map(item => `
                <li class="flex items-start space-x-2">
                    <i class="fa-solid fa-circle-check text-emerald-400 mt-0.5 shrink-0"></i>
                    <span>${item}</span>
                </li>
            `).join('');
    }

    // 4. Core Terminology
    const conceptsEl = document.getElementById('yt-concepts-container');
    if (conceptsEl && Array.isArray(data.concepts)) {
        conceptsEl.innerHTML = data.concepts
            .map(c => `
                <div class="p-3 bg-slate-900/70 rounded-xl border border-slate-800">
                    <span class="font-semibold text-indigo-300 block text-xs uppercase tracking-wider mb-1">${c.term}</span>
                    <p class="text-xs text-slate-400 leading-relaxed">${c.definition}</p>
                </div>
            `).join('');
    }

    // 5. Comprehensive Structured Notes
    const notesEl = document.getElementById('yt-notes-content');
    if (notesEl) {
        notesEl.innerHTML = data.notes || '<p class="text-slate-400">No structured notes available.</p>';
    }

    // 6. Interactive Quiz Module (Render all 4 questions)
    const quizEl = document.getElementById('yt-quiz-container');
    if (quizEl && Array.isArray(data.quiz)) {
        quizEl.innerHTML = `
            <div class="mb-4 flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-2">
                <span>Total Questions: <strong>${data.quiz.length}</strong></span>
                <span>Click an option to test your understanding</span>
            </div>
            <div class="space-y-4">
                ${data.quiz.map((q, idx) => `
                    <div class="p-4 bg-slate-900/60 rounded-xl border border-slate-800/80 space-y-3">
                        <p class="font-medium text-slate-200 text-sm flex items-start">
                            <span class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-brand-500/20 text-brand-400 text-xs font-bold mr-2 shrink-0">${idx + 1}</span>
                            <span>${q.question}</span>
                        </p>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pl-7">
                            ${q.options.map(opt => `
                                <button onclick="checkQuizAnswer(this, '${opt.replace(/'/g, "\\'")}', '${q.answer.replace(/'/g, "\\'")}')" 
                                        class="px-3.5 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 text-xs text-slate-300 text-left transition-all border border-slate-700/50 flex items-center justify-between group">
                                    <span>${opt}</span>
                                    <i class="fa-regular fa-circle text-slate-500 group-hover:text-slate-300 ml-2 shrink-0"></i>
                                </button>
                            `).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

function checkQuizAnswer(buttonEl, selectedOption, correctAnswer) {
    const parentContainer = buttonEl.parentElement;
    const allButtons = parentContainer.querySelectorAll('button');

    allButtons.forEach(btn => {
        btn.disabled = true;
        btn.classList.remove('bg-slate-800/80', 'hover:bg-slate-700/80');
        
        const btnText = btn.querySelector('span').innerText.trim();
        const icon = btn.querySelector('i');

        if (btnText === correctAnswer) {
            btn.classList.add('bg-emerald-600/30', 'border-emerald-500', 'text-emerald-300');
            if (icon) icon.className = 'fa-solid fa-circle-check text-emerald-400 ml-2 shrink-0';
        } else if (btn === buttonEl && selectedOption !== correctAnswer) {
            btn.classList.add('bg-red-600/30', 'border-red-500', 'text-red-300');
            if (icon) icon.className = 'fa-solid fa-circle-xmark text-red-400 ml-2 shrink-0';
        } else {
            btn.classList.add('opacity-50');
        }
    });
}