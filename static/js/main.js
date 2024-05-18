document.addEventListener('DOMContentLoaded', function() {
    const startTrainingButton = document.getElementById('start-training');
    const progressBar = document.getElementById('progress-bar');
    const uploadForm = document.getElementById('upload-form');

    if (startTrainingButton) {
        startTrainingButton.addEventListener('click', function() {
            // Prevent form submission
            event.preventDefault();
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

        document.getElementById('cancel-training').addEventListener('click', function() {
            event.preventDefault();
            clearInterval(interval);
            progressBar.style.width = '0%';
            progressBar.setAttribute('aria-valuenow', 0);
            startTrainingButton.disabled = false;
        });
    }
});
