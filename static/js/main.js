document.addEventListener('DOMContentLoaded', function() {
    const startTrainingButton = document.getElementById('startTraining');
    const progressBar = document.getElementById('progressBar');

    if (startTrainingButton) {
        startTrainingButton.addEventListener('click', function() {
            startTrainingButton.disabled = true;
            progressBar.style.width = '0%';
            progressBar.setAttribute('aria-valuenow', 0);
            let progress = 0;
            const interval = setInterval(function() {
                if (progress >= 100) {
                    clearInterval(interval);
                    startTrainingButton.disabled = false;
                } else {
                    progress += 10; // Simulate training progress
                    progressBar.style.width = `${progress}%`;
                    progressBar.setAttribute('aria-valuenow', progress);
                }
            }, 1000);
        });
    }
});
