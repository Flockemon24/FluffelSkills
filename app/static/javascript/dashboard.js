document.addEventListener("DOMContentLoaded", function() {
    console.log("Wartelisten-Script wurde geladen...");
    
    const wishedPlan = localStorage.getItem('wished_plan');
    console.log("Gefundener Plan im LocalStorage:", wishedPlan);
    
    if (wishedPlan) {
        const modal = document.getElementById('earlyBirdModal');
        console.log("Modal-Element im HTML gefunden?", modal);
        
        if (modal) {
            console.log("Versuche Modal anzuzeigen...");
            modal.removeAttribute('hidden');
            modal.classList.add('active');
            // Falls du Inline-Styles nutzt, schalten wir es hier sicherheitshalber auf flex/block
            modal.style.display = 'flex'; 
        } else {
            console.error("FEHLER: Ein Plan wurde im Speicher gefunden, aber das HTML-Element mit der ID 'earlyBirdModal' fehlt auf dieser Seite!");
        }
        
        console.log("Sende API-Anfrage an Flask...");
        fetch('/api/join-waitlist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plan_name: wishedPlan })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Antwort von Flask erhalten:", data);
            localStorage.removeItem('wished_plan');
            console.log("wished_plan erfolgreich aus dem LocalStorage gelöscht.");
        })
        .catch(error => {
            console.error("Fehler beim API-Aufruf an Flask:", error);
        });
    }
});


function closeModal() {
    const modal = document.getElementById('earlyBirdModal');
    modal.classList.remove('active');
}

// Schließen, wenn man irgendwo außerhalb des Fensters hinklickt
window.onclick = function(event) {
    const modal = document.getElementById('earlyBirdModal');
    if (event.target === modal) {
        closeModal();
    }
}