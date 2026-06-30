
        function togglePassword(inputId) {
            const input = document.getElementById(inputId);
            const icon = document.getElementById(inputId + '-icon');
            if (input.type === 'password') {
                input.type = 'text';
                icon.textContent = 'visibility_off';
            } else {
                input.type = 'password';
                icon.textContent = 'visibility';
            }
        }

        // Form submission micro-interaction
        const form = document.getElementById('reset-password-form');
        form.addEventListener('submit', (e) => {
            const btn = e.target.querySelector('button[type="submit"]');
            const originalText = btn.textContent;
            btn.disabled = true;
            btn.innerHTML = '<span class="flex items-center justify-center gap-2"><span class="animate-spin material-symbols-outlined">sync</span> Saving...</span>';
            
            setTimeout(() => {
                btn.innerHTML = '<span class="flex items-center justify-center gap-2"><span class="material-symbols-outlined">check_circle</span> Success</span>';
                btn.classList.replace('bg-primary-container', 'bg-tertiary-container');
                setTimeout(() => {
                    // Logic for redirect would go here
                    console.log('Redirecting to login...');
                    btn.disabled = false;
                    btn.textContent = originalText;
                    btn.classList.replace('bg-tertiary-container', 'bg-primary-container');
                }, 1500);
            }, 2000);
        });

