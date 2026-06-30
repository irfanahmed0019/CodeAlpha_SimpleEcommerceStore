
        // Simple micro-interaction for hover states on sidebar
        document.querySelectorAll('aside nav a').forEach(link => {
            link.addEventListener('mouseenter', () => {
                if (!link.classList.contains('bg-primary-container')) {
                    link.style.transform = 'translateX(4px)';
                }
            });
            link.addEventListener('mouseleave', () => {
                link.style.transform = 'translateX(0)';
            });
        });
const methods = document.querySelectorAll('input[name="payment_method"]');
const cardForm = document.getElementById("card-form");

function togglePayment() {

    const selected = document.querySelector(
        'input[name="payment_method"]:checked'
    ).value;

    if (selected === "card") {

        cardForm.style.display = "block";

    } else {

        cardForm.style.display = "none";

    }

}

methods.forEach(method => {

    method.addEventListener("change", togglePayment);

});

togglePayment();