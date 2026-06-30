
        // Micro-interactions
        document.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                // Potential hover effects via JS if needed
            });
        });

        // Simple sticky header effect
        window.addEventListener('scroll', () => {
            const header = document.querySelector('header');
            if (window.scrollY > 50) {
                header.classList.add('py-2');
                header.classList.remove('h-20');
                header.classList.add('h-16');
            } else {
                header.classList.remove('py-2');
                header.classList.add('h-20');
                header.classList.remove('h-16');
            }
        });
