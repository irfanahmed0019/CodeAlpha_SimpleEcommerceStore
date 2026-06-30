
        // Simple Interaction logic for focus
        const emailInput = document.getElementById('email');
        emailInput.addEventListener('focus', () => {
            emailInput.parentElement.querySelector('label').classList.add('text-primary');
        });
        emailInput.addEventListener('blur', () => {
            emailInput.parentElement.querySelector('label').classList.remove('text-primary');
        });

        // Toggle Dark Mode purely for demonstration if user prefers system theme
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            // document.documentElement.classList.add('dark');
            // Keeping light as per prompt instruction, but system ready
        }
