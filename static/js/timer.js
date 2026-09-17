/**
 * EduPulse AI — Focus Pomodoro Timer Module
 */

let timerInterval = null;
let totalSeconds = 25 * 60;
let remainingSeconds = 25 * 60;
let isRunning = false;

function updateTimerDisplay() {
    const minutes = Math.floor(remainingSeconds / 60);
    const seconds = remainingSeconds % 60;
    const display = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    
    document.getElementById('timer-display').textContent = display;

    // Update SVG Progress Ring Offset
    const ring = document.getElementById('timer-progress-ring');
    if (ring) {
        const totalDash = 276.46;
        const offset = totalDash - (remainingSeconds / totalSeconds) * totalDash;
        ring.style.strokeDashoffset = offset;
    }
}

function toggleTimer() {
    if (isRunning) {
        pauseTimer();
    } else {
        startTimer();
    }
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;

    const btnText = document.getElementById('timer-btn-text');
    const btnIcon = document.getElementById('timer-btn-icon');
    if (btnText) btnText.textContent = 'Pause Focus';
    if (btnIcon) btnIcon.className = 'fa-solid fa-pause';

    timerInterval = setInterval(() => {
        if (remainingSeconds > 0) {
            remainingSeconds--;
            updateTimerDisplay();
        } else {
            pauseTimer();
            alert('Focus Session Completed! Take a short break to recharge.');
            resetTimer();
        }
    }, 1000);
}

function pauseTimer() {
    isRunning = false;
    clearInterval(timerInterval);

    const btnText = document.getElementById('timer-btn-text');
    const btnIcon = document.getElementById('timer-btn-icon');
    if (btnText) btnText.textContent = 'Resume Focus';
    if (btnIcon) btnIcon.className = 'fa-solid fa-play';
}

function resetTimer() {
    pauseTimer();
    remainingSeconds = 25 * 60;
    totalSeconds = 25 * 60;

    const btnText = document.getElementById('timer-btn-text');
    const btnIcon = document.getElementById('timer-btn-icon');
    if (btnText) btnText.textContent = 'Start Focus';
    if (btnIcon) btnIcon.className = 'fa-solid fa-play';

    updateTimerDisplay();
}

// Initialize Timer State
document.addEventListener('DOMContentLoaded', () => {
    updateTimerDisplay();
});