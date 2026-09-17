/**
 * EduPulse AI — PDF Synthesizer Module
 */

function updatePDFFileName(input) {
    const label = document.getElementById('pdf-file-label');
    if (input.files && input.files[0]) {
        label.textContent = `Selected: ${input.files[0].name}`;
        label.classList.add('text-brand-400');
    }
}

// Drag and Drop Zone Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('pdf-drop-zone');
    if (!dropZone) return;

    dropZone.addEventListener('click', () => {
        document.getElementById('pdf-file-input').click();
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('border-brand-500', 'bg-slate-800/80');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('border-brand-500', 'bg-slate-800/80');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files[0]) {
            const input = document.getElementById('pdf-file-input');
            input.files = files;
            updatePDFFileName(input);
        }
    });
});

async function handlePDFSubmit(event) {
    event.preventDefault();
    const fileInput = document.getElementById('pdf-file-input');
    if (!fileInput.files || !fileInput.files[0]) {
        alert('Please select a PDF document first.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    showLoading('Synthesizing PDF document structure & generating notes...');

    try {
        const response = await fetch('/api/v1/pdf/synthesize', {
            method: 'POST',
            body: formData
        });

        let data;
        try {
            data = await response.json();
        } catch (e) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        if (!response.ok) {
            let errMsg = 'Failed to process PDF document.';
            if (data.detail) {
                if (typeof data.detail === 'string') {
                    errMsg = data.detail;
                } else if (Array.isArray(data.detail)) {
                    errMsg = data.detail.map(err => `${err.loc ? err.loc.slice(1).join(' -> ') : 'Field'}: ${err.msg}`).join('\n');
                } else {
                    errMsg = JSON.stringify(data.detail);
                }
            }
            throw new Error(errMsg);
        }

        renderPDFResults(data);
    } catch (err) {
        alert(`Error:\n${err.message}`);
    } finally {
        hideLoading();
    }
}

function renderPDFResults(data) {
    const container = document.getElementById('pdf-output-container');
    container.classList.remove('hidden');

    document.getElementById('pdf-stat-pages').textContent = data.page_count || 0;
    document.getElementById('pdf-stat-words').textContent = data.word_count || 0;
    document.getElementById('pdf-stat-time').textContent = `${data.estimated_reading_time_min || 0} min`;

    document.getElementById('pdf-notes-content').innerHTML = data.synthesized_notes || '<p>No content extracted.</p>';
}