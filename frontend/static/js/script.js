// Mobile Menu Toggle
const menuToggle = document.getElementById('menuToggle');
const mainNav = document.getElementById('mainNav');

if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', () => {
        mainNav.classList.toggle('active');
        menuToggle.classList.toggle('active');
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!mainNav.contains(e.target) && !menuToggle.contains(e.target)) {
            mainNav.classList.remove('active');
            menuToggle.classList.remove('active');
        }
    });
}

// Header scroll effect
const header = document.querySelector('.header');
if (header) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

// Horizontal scroll for products
const scrollWrapper = document.querySelector('.scroll-wrapper');
const scrollPrev = document.querySelector('.scroll-btn.prev');
const scrollNext = document.querySelector('.scroll-btn.next');

if (scrollWrapper && scrollPrev && scrollNext) {
    scrollPrev.addEventListener('click', () => {
        scrollWrapper.scrollBy({
            left: -300,
            behavior: 'smooth'
        });
    });
    
    scrollNext.addEventListener('click', () => {
        scrollWrapper.scrollBy({
            left: 300,
            behavior: 'smooth'
        });
    });
}

// Add to cart functionality
const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
const cartCount = document.querySelector('.cart-count');

addToCartButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        const productName = button.getAttribute('data-name');
        const productPrice = button.getAttribute('data-price');
        
        // Update cart count
        let currentCount = parseInt(cartCount.textContent) || 0;
        cartCount.textContent = currentCount + 1;
        
        // Add to cart logic here (you can use localStorage or backend)
        addToCart(productName, productPrice);
        
        // Visual feedback
        button.innerHTML = '<i class="fas fa-check"></i> Added!';
        button.style.background = '#006B3F';
        
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-cart-plus"></i> Add to Cart';
            button.style.background = '';
        }, 1500);
    });
});

function addToCart(name, price) {
    // This is where you'd implement actual cart logic
    console.log(`Added to cart: ${name} - ${price} ETB`);
    
    // For now, just store in localStorage
    let cart = JSON.parse(localStorage.getItem('ethiocoffee_cart')) || [];
    cart.push({ name, price: parseInt(price), quantity: 1 });
    localStorage.setItem('ethiocoffee_cart', JSON.stringify(cart));
}

// Form submission
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        // Add your form submission logic here
        alert('Thank you for your message! We will get back to you soon.');
        contactForm.reset();
    });
}

// Initialize cart count on page load
document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('ethiocoffee_cart')) || [];
    if (cartCount) {
        cartCount.textContent = cart.length;
    }
});