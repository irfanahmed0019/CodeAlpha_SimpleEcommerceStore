
        // Simple micro-interaction for payment method selection
        const paymentMethods = document.querySelectorAll('input[name="payment_method"]');
        paymentMethods.forEach(method => {
            method.addEventListener('change', (e) => {
                // Remove active styling from all
                document.querySelectorAll('input[name="payment_method"]').forEach(input => {
                    input.closest('label').classList.remove('border-primary', 'bg-surface-container-lowest');
                    input.closest('label').classList.add('border-outline-variant', 'bg-surface-container-low');
                    
                    // Hide credit card details if not selected
                    const cardDetails = input.closest('label').querySelector('.animate-in');
                    if (cardDetails) cardDetails.classList.add('hidden');
                });
                
                // Add active styling to current
                const label = e.target.closest('label');
                label.classList.add('border-primary', 'bg-surface-container-lowest');
                label.classList.remove('border-outline-variant', 'bg-surface-container-low');
                
                // Show details if card
                const cardDetails = label.querySelector('.animate-in');
                if (cardDetails) cardDetails.classList.remove('hidden');
            });
        });