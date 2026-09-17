/**
 * EduPulse AI — Study Roadmap Planner Module
 */

async function handleRoadmapSubmit(event) {
    event.preventDefault();

    const subject = document.getElementById('roadmap-subject')?.value.trim();
    const days = parseInt(document.getElementById('roadmap-days')?.value, 10);
    const hours = parseFloat(document.getElementById('roadmap-hours')?.value);

    if (!subject || isNaN(days) || isNaN(hours)) {
        alert('Please fill out all roadmap fields with valid numbers.');
        return;
    }

    showLoading('Generating personalized study roadmap...');

    try {
        const data = await apiRequest('/api/v1/roadmap/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                subject_title: subject,
                horizon_days: days,
                daily_hours: hours
            })
        });

        renderRoadmapResults(data);
    } catch (err) {
        console.error('Roadmap Generation Error:', err);
    } finally {
        hideLoading();
    }
}

function renderRoadmapResults(data) {
    const container = document.getElementById('roadmap-output-container');
    if (!container) return;

    container.classList.remove('hidden');

    const titleEl = document.getElementById('roadmap-title');
    if (titleEl) {
        titleEl.textContent = `${data.subject} (${data.duration_days} Days Plan)`;
    }

    const timelineContainer = document.getElementById('roadmap-timeline');
    if (timelineContainer && Array.isArray(data.schedule)) {
        timelineContainer.innerHTML = data.schedule.map(item => `
            <div class="p-4 bg-slate-800/60 border border-slate-700/50 rounded-xl">
                <div class="flex justify-between items-center mb-1">
                    <span class="font-semibold text-brand-400">Day ${item.day}</span>
                    <span class="text-xs text-slate-400">${item.hours} hrs</span>
                </div>
                <p class="text-slate-200 text-sm">${item.topic}</p>
            </div>
        `).join('');
    }
}