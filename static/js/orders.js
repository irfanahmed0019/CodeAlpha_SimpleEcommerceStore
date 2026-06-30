        // Micro-interaction for filter buttons
        const filterButtons = document.querySelectorAll('.flex.gap-stack-lg button');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                filterButtons.forEach(b => {
                    b.classList.remove('text-primary-container', 'border-primary-container');
                    b.classList.add('text-on-surface-variant', 'border-transparent');
                });
                btn.classList.add('text-primary-container', 'border-primary-container');
                btn.classList.remove('text-on-surface-variant', 'border-transparent');
            });
        });