document.addEventListener('DOMContentLoaded', () => {
    // Use the completedSteps passed from Flask
    completedSteps.forEach(stepNumber => {
        document.getElementById(`step${stepNumber}`).classList.add('completed');
    });

    // Add click event listeners to each step
    document.querySelectorAll('.step').forEach((step, index) => {
        step.addEventListener('click', () => {
            if (completedSteps.includes(index + 1)) {
                // Navigate to the respective section page (e.g., `/section1`)
                window.location.href = `/page${index + 1}`;
            } else {
                alert('Please complete the previous sections first.');
            }
        });
    });
});
