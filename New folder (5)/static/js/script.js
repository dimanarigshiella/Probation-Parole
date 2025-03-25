document.addEventListener('DOMContentLoaded', function () {
    const formButton = document.querySelector('.btn'); // Select the button
    const inputs = document.querySelectorAll('.input-box'); // Select all input boxes
    const dropdowns = document.querySelectorAll('.dropdown-box'); // Select all dropdowns

    formButton.addEventListener('click', function (event) {
        let isValid = true; // Flag to track if the form is valid

        // Clear previous error highlights
        inputs.forEach(input => {
            input.style.border = '1px solid #ccc'; // Reset border
            input.style.backgroundColor = ''; // Reset background color
        });
        dropdowns.forEach(dropdown => {
            dropdown.style.border = '1px solid #ccc'; // Reset border
            dropdown.style.backgroundColor = ''; // Reset background color
        });

        // Validate input boxes
        inputs.forEach(input => {
            if (input.value.trim() === '') {
                isValid = false;
                input.style.border = '2px solid red'; // Highlight the input box
                input.style.backgroundColor = '#ffcccc'; // Add light red background
            }
        });

        // Validate dropdowns
        dropdowns.forEach(dropdown => {
            if (dropdown.value === '') {
                isValid = false;
                dropdown.style.border = '2px solid red'; // Highlight the dropdown
                dropdown.style.backgroundColor = '#ffcccc'; // Add light red background
            }
        });

        // If the form is invalid, show an error message and prevent submission
        if (!isValid) {
            event.preventDefault(); // Prevent the default button action
            alert('Please fill out all required fields.'); // Show error message
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Select all images in the segment
    const images = document.querySelectorAll('.segment-image');

    // Add click behavior to each image
    images.forEach((image, index) => {
        image.addEventListener('click', function () {
            const descriptions = [
                'Parole and Probation',
                'Department of Justice',
                'Bagong Pilipinas'
            ];
            alert(descriptions[index]); // Show an alert with the description
        });

        // Add hover behavior to change opacity and show tooltip
        image.addEventListener('mouseenter', function () {
            image.style.opacity = '0.8'; // Reduce opacity on hover
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.innerText = image.alt; // Use the alt text as the tooltip
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

        // Remove tooltip and reset opacity on mouse leave
        image.addEventListener('mouseleave', function () {
            image.style.opacity = '1'; // Reset opacity
            const tooltip = document.getElementById(`tooltip-${index}`);
            if (tooltip) {
                tooltip.remove(); // Remove the tooltip
            }
        });
    });
});
