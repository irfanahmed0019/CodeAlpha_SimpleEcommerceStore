
    // Simple micro-interactions for form feedback
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
      input.addEventListener('focus', () => {
        input.parentElement.querySelector('label').classList.add('text-primary');
      });
      input.addEventListener('blur', () => {
        input.parentElement.querySelector('label').classList.remove('text-primary');
      });
    });