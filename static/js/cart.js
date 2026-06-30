
        function increment(btn) {
            let label = btn.previousElementSibling;
            let val = parseInt(label.innerText);
            label.innerText = val + 1;
        }
        
        function decrement(btn) {
            let label = btn.nextElementSibling;
            let val = parseInt(label.innerText);
            if (val > 1) {
                label.innerText = val - 1;
            }
        }

        // Simple interaction for the primary action
        document.querySelector('button.bg-primary-container').addEventListener('click', function() {
            this.innerHTML = '<span class="material-symbols-outlined animate-spin">sync</span> Loading...';
            setTimeout(() => {
                window.location.href = '#checkout';
            }, 800);
        });