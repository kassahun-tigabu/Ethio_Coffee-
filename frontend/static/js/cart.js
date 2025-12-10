// Cart functionality
document.addEventListener('DOMContentLoaded', () => {
    const cartBody = document.getElementById('cart-body');
    const subtotalEl = document.getElementById('subtotal');
    const shippingEl = document.getElementById('shipping');
    const taxEl = document.getElementById('tax');
    const cartTotalEl = document.getElementById('cart-total');
    const clearCartBtn = document.getElementById('clearCart');
    const checkoutBtn = document.querySelector('.checkout-btn');
    
    let cart = JSON.parse(localStorage.getItem('ethiocoffee_cart')) || [];
    
    // Display cart items
    function displayCartItems() {
        if (cart.length === 0) {
            cartBody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center" style="padding: 3rem;">
                        <p>Your cart is empty. <a href="/products">Start shopping!</a></p>
                    </td>
                </tr>
            `;
            return;
        }
        
        cartBody.innerHTML = '';
        let subtotal = 0;
        
        cart.forEach((item, index) => {
            const itemTotal = item.price * item.quantity;
            subtotal += itemTotal;
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td data-label="Product">
                    <div class="product-cell">
                        <img src="/static/images/coffee${(index % 8) + 1}.jpg" alt="${item.name}" class="product-img">
                        <div>
                            <div class="product-name">${item.name}</div>
                            <div class="product-category">Premium Arabica</div>
                        </div>
                    </div>
                </td>
                <td data-label="Price" class="price-cell">${item.price} ETB</td>
                <td data-label="Quantity">
                    <div class="quantity-controls">
                        <button class="quantity-btn minus" data-index="${index}">-</button>
                        <input type="number" class="quantity-input" value="${item.quantity}" min="1" max="10" data-index="${index}">
                        <button class="quantity-btn plus" data-index="${index}">+</button>
                    </div>
                </td>
                <td data-label="Total" class="total-cell">${itemTotal} ETB</td>
                <td data-label="Remove">
                    <button class="remove-btn" data-index="${index}">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </td>
            `;
            
            cartBody.appendChild(row);
        });
        
        // Update totals
        const shipping = 50;
        const tax = subtotal * 0.15; // 15% tax
        const total = subtotal + shipping + tax;
        
        subtotalEl.textContent = `${subtotal} ETB`;
        shippingEl.textContent = `${shipping} ETB`;
        taxEl.textContent = `${tax.toFixed(2)} ETB`;
        cartTotalEl.textContent = `${total.toFixed(2)} ETB`;
    }
    
    // Quantity controls
    cartBody.addEventListener('click', (e) => {
        if (e.target.classList.contains('quantity-btn')) {
            const index = parseInt(e.target.getAttribute('data-index'));
            const input = cartBody.querySelector(`.quantity-input[data-index="${index}"]`);
            let quantity = parseInt(input.value);
            
            if (e.target.classList.contains('plus') && quantity < 10) {
                quantity++;
            } else if (e.target.classList.contains('minus') && quantity > 1) {
                quantity--;
            }
            
            input.value = quantity;
            cart[index].quantity = quantity;
            localStorage.setItem('ethiocoffee_cart', JSON.stringify(cart));
            displayCartItems();
        }
    });
    
    // Remove item
    cartBody.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-btn') || e.target.closest('.remove-btn')) {
            const index = parseInt(e.target.getAttribute('data-index') || 
                                 e.target.closest('.remove-btn').getAttribute('data-index'));
            cart.splice(index, 1);
            localStorage.setItem('ethiocoffee_cart', JSON.stringify(cart));
            displayCartItems();
            updateCartCount();
        }
    });
    
    // Clear cart
    if (clearCartBtn) {
        clearCartBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to clear your cart?')) {
                localStorage.removeItem('ethiocoffee_cart');
                cart = [];
                displayCartItems();
                updateCartCount();
            }
        });
    }
    
    // Checkout
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', () => {
            if (cart.length === 0) {
                alert('Your cart is empty. Add some products first!');
                return;
            }
            
            alert('Proceeding to checkout... This would redirect to payment page in a real implementation.');
            // Redirect to checkout page
            // window.location.href = '/checkout';
        });
    }
    
    // Update cart count in header
    function updateCartCount() {
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            cartCount.textContent = cart.length;
        }
    }
    
    // Initialize
    displayCartItems();
});