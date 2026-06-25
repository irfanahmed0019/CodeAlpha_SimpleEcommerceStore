
        // Simple scroll behavior for header
        window.addEventListener('scroll', () => {
            const header = document.querySelector('header');
            if (window.scrollY > 20) {
                header.classList.add('shadow-sm');
                header.classList.add('bg-opacity-95');
                header.classList.add('backdrop-blur-md');
            } else {
                header.classList.remove('shadow-sm');
                header.classList.remove('bg-opacity-95');
                header.classList.remove('backdrop-blur-md');
            }
        });

        // Simple button micro-interaction
        document.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', function() {
                this.classList.add('scale-95');
                setTimeout(() => this.classList.remove('scale-95'), 100);
            });
        });
 