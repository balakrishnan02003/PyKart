// Main JavaScript file for PyKart

// Cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.btn-add-cart, .btn-add-cart-large');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            const productSlug = this.getAttribute('data-product-slug');
            
            // Get quantity if on product detail page
            let quantity = 1;
            const quantityInput = document.getElementById('quantity');
            if (quantityInput) {
                quantity = parseInt(quantityInput.value) || 1;
            }
            
            // Disable button to prevent double clicks
            this.disabled = true;
            const originalText = this.textContent;
            this.textContent = 'Adding...';
            
            // Create form data
            const formData = new FormData();
            formData.append('quantity', quantity);
            const csrfToken = getCookie('csrftoken');
            if (csrfToken) {
                formData.append('csrfmiddlewaretoken', csrfToken);
            }
            
            // Send AJAX request
            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update cart count
                    updateCartCount(data.cart_count);
                    
                    // Show success message
                    showMessage(data.message, 'success');
                    
                    // Re-enable button
                    this.disabled = false;
                    this.textContent = originalText;
                } else {
                    // Handle error
                    showMessage(data.message || 'Error adding to cart', 'error');
                    this.disabled = false;
                    this.textContent = originalText;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback: redirect to cart page
                window.location.href = `/cart/add/${productId}/?quantity=${quantity}`;
            });
        });
    });
    
    // Update cart count on page load
    updateCartCount();
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to update cart count
function updateCartCount(count) {
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        if (count !== undefined) {
            cartCount.textContent = count;
        } else {
            // Fetch current count
            fetch('/cart/count/')
                .then(response => response.json())
                .then(data => {
                    cartCount.textContent = data.count;
                })
                .catch(error => {
                    console.error('Error fetching cart count:', error);
                });
        }
    }
}

// Function to show messages
function showMessage(message, type) {
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type === 'success' ? 'success' : 'error'}`;
    messageDiv.textContent = message;
    
    // Insert at the top of main content
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        // Check if messages container exists
        let messagesContainer = document.querySelector('.messages');
        if (!messagesContainer) {
            messagesContainer = document.createElement('div');
            messagesContainer.className = 'messages';
            mainContent.insertBefore(messagesContainer, mainContent.firstChild);
        }
        messagesContainer.appendChild(messageDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
            if (messagesContainer.children.length === 0) {
                messagesContainer.remove();
            }
        }, 5000);
    }
}
