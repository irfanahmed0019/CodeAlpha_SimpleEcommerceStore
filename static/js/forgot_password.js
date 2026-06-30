
    function handleAssistance(event) {
      event.preventDefault();
      const form = document.getElementById('assistanceForm');
      const success = document.getElementById('successMessage');
      
      // Basic UI transformation
      form.classList.add('opacity-40', 'pointer-events-none');
      success.classList.remove('hidden');
      
      // Auto-focus the success context
      success.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
