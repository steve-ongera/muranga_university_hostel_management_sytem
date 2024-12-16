// Mobile Menu Toggle
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// Smooth Scrolling for Anchor Links
const scrollLinks = document.querySelectorAll('a[href^="#"]');

scrollLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);

        window.scrollTo({
            top: targetElement.offsetTop - 50, // Adjust for header height
            behavior: 'smooth'
        });
    });
});

// Form Validation (Example: Simple Email Validation)
const form = document.querySelector('form');
const emailInput = document.querySelector('input[type="email"]');

form.addEventListener('submit', function(e) {
    if (!validateEmail(emailInput.value)) {
        alert('Please enter a valid email address.');
        e.preventDefault();
    }
});

function validateEmail(email) {
    const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return regex.test(email);
}

// Example: Hide the alert message after a few seconds
setTimeout(function() {
    const alertMessage = document.querySelector('.alert');
    if (alertMessage) {
        alertMessage.style.display = 'none';
    }
}, 5000); // Hide after 5 seconds
