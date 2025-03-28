document.addEventListener('DOMContentLoaded', function() {
    // Form validation for input boxes and dropdowns
    const formButton = document.querySelector('.btn');
    const inputs = document.querySelectorAll('.input-box');
    const dropdowns = document.querySelectorAll('.dropdown-box');
    const form = document.getElementById('questionForm');

    // Form button validation
    if (formButton) {
        formButton.addEventListener('click', function(event) {
            let isValid = true;

            // Clear previous error highlights
            inputs.forEach(input => {
                input.style.border = '1px solid #ccc';
                input.style.backgroundColor = '';
            });
            dropdowns.forEach(dropdown => {
                dropdown.style.border = '1px solid #ccc';
                dropdown.style.backgroundColor = '';
            });

            // Validate input boxes
            inputs.forEach(input => {
                if (input.value.trim() === '') {
                    isValid = false;
                    input.style.border = '2px solid red';
                    input.style.backgroundColor = '#ffcccc';
                }
            });

            // Validate dropdowns
            dropdowns.forEach(dropdown => {
                if (dropdown.value === '') {
                    isValid = false;
                    dropdown.style.border = '2px solid red';
                    dropdown.style.backgroundColor = '#ffcccc';
                }
            });

            if (!isValid) {
                event.preventDefault();
                alert('Please fill out all required fields.');
            }
        });
    }

    // Image handling and tooltips
    const images = document.querySelectorAll('.segment-image');
    images.forEach((image, index) => {
        const descriptions = [
            'Parole and Probation',
            'Department of Justice',
            'Bagong Pilipinas'
        ];

        // Image click handler
        image.addEventListener('click', function() {
            alert(descriptions[index]);
        });

        // Image hover handlers
        image.addEventListener('mouseenter', function() {
            image.style.opacity = '0.8';
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.innerText = image.alt;
            tooltip.style.position = 'absolute';
            tooltip.style.top = `${image.getBoundingClientRect().top - 30}px`;
            tooltip.style.left = `${image.getBoundingClientRect().left}px`;
            tooltip.style.backgroundColor = 'black';
            tooltip.style.color = 'white';
            tooltip.style.padding = '5px 10px';
            tooltip.style.borderRadius = '5px';
            tooltip.style.fontSize = '12px';
            tooltip.style.zIndex = '1001';
            tooltip.id = `tooltip-${index}`;
            document.body.appendChild(tooltip);
        });

        image.addEventListener('mouseleave', function() {
            image.style.opacity = '1';
            const tooltip = document.getElementById(`tooltip-${index}`);
            if (tooltip) {
                tooltip.remove();
            }
        });
    });

    // Form submission handling
    if (form) {
        form.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            // Validate all questions are answered
            const questions = document.querySelectorAll('.question');
            let allAnswered = true;

            // Clear previous highlights
            questions.forEach(question => {
                question.classList.remove('highlight');
            });

            // Check each question quietly
            questions.forEach(question => {
                const options = question.querySelectorAll('input[type="radio"]');
                const isAnswered = Array.from(options).some(option => option.checked);

                if (!isAnswered) {
                    allAnswered = false;
                    question.classList.add('highlight');
                }
            });

            if (!allAnswered) {
                // Scroll to first unanswered question instead of showing alert
                const firstUnanswered = document.querySelector('.highlight');
                if (firstUnanswered) {
                    firstUnanswered.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return false;
            }

            try {
                // Format the data for Google Sheets
                const formData = new FormData(form);
                const payload = {
                    timestamp: new Date().toISOString(),
                    segment: window.location.pathname.split('/').pop()
                };
                
                formData.forEach((value, key) => {
                    payload[key] = value;
                });

                // Try to send data to Google Sheets, but don't block on failure
                try {
                    await fetch(GOOGLE_SCRIPT_URL, {
                        method: 'POST',
                        mode: 'no-cors',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: new URLSearchParams(payload).toString()
                    });
                } catch (e) {
                    // Log error silently
                    console.warn('Failed to send data to Google Sheets:', e);
                }

                // Continue to next segment regardless of Google Sheets success
                form.submit();
            } catch (error) {
                // Log error silently and try to continue
                console.error('Form submission error:', error);
                form.submit();
            }
        });
    }
});
