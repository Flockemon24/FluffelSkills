let yearly = false;
const pricingLabels = document.body.dataset;
function toggleBilling() {
    yearly = !yearly;
    const toggle =
        document.getElementById(
            "billingToggle"
        );
    const proPrice =
        document.getElementById(
            "proPrice"
        );
    const futurePrice =
        document.getElementById(
            "futurePrice"
        );
    const proAnnual =
        document.getElementById(
            "proAnnual"
        );
    const futureAnnual =
        document.getElementById(
            "futureAnnual"
        );
    if (yearly) {
        toggle.classList.add(
            "yearly"
        );
        toggle.setAttribute("aria-pressed", "true");
        proPrice.innerHTML =
            '99 € <span>/ ' + pricingLabels.yearLabel + '</span>';
        futurePrice.innerHTML =
            '199 € <span>/ ' + pricingLabels.yearLabel + '</span>';
        proAnnual.textContent =
            pricingLabels.proMonthlyAnnual;
        futureAnnual.textContent =
            pricingLabels.futureMonthlyAnnual;
    } else {
        toggle.classList.remove(
            "yearly"
        );
        toggle.setAttribute("aria-pressed", "false");
        proPrice.innerHTML =
            '9,99 € <span>/ ' + pricingLabels.monthLabel + '</span>';
        futurePrice.innerHTML =
            '19,99 € <span>/ ' + pricingLabels.monthLabel + '</span>';
        proAnnual.textContent =
            pricingLabels.monthlyAnnual;
        futureAnnual.textContent =
            pricingLabels.futureAnnual;
    }
}
/* =====================================================
   KEYBOARD SUPPORT
===================================================== */
document
    .getElementById("billingToggle")
    .addEventListener(
        "keydown",
        function(event) {
            if (
                event.key === "Enter" ||
                event.key === " "
            ) {
                event.preventDefault();
                toggleBilling();
            }
        }
    );


function openModal(event, planName) {
    if (event) event.preventDefault(); 
    
    // Wir nutzen jetzt localStorage statt sessionStorage
    localStorage.setItem('wished_plan', planName);
    
    // Weiterleitung zur Registrierung
    window.location.href = "/register";
}

