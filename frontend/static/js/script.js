// script.js

// Mobile menu toggle
const menuBtn = document.querySelector('.menu-btn');
const navLinks = document.querySelector('.nav-links');

if(menuBtn) {
    menuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });
}

// Cart functionality (basic example)
let cart = [];

function addToCart(productName, price) {
    cart.push({ name: productName, price: price });
    updateCartUI();
}

function updateCartUI() {
    const cartContainer = document.querySelector('.cart-items');
    if(!cartContainer) return;

    cartContainer.innerHTML = '';
    cart.forEach(item => {
        const div = document.createElement('div');
        div.className = 'cart-item';
        div.innerHTML = `${item.name} - $${item.price}`;
        cartContainer.appendChild(div);
    });

    const total = cart.reduce((sum, item) => sum + item.price, 0);
    const totalDiv = document.querySelector('.cart-total');
    if(totalDiv) totalDiv.innerHTML = `Total: $${total}`;
}

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Optional: Alert when contact form submitted
const contactForm = document.getElementById('contact-form');
if(contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert("Thank you! Your message has been sent.");
        contactForm.reset();
    });
}
