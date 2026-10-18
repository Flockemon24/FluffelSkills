const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirm_password");
const errorMessage = document.getElementById("error_message");
const submitBtn = document.getElementById("submit_btn");
const strengthBar = document.getElementById("strength-bar");
// Funktion 1: Passwort sichtbar/unsichtbar machen
function togglePasswordVisibility(fieldId, eyeIcon) {
    const field = document.getElementById(fieldId);
    if (field.type === "password") {
        field.type = "text";
        eyeIcon.classList.remove("bi-eye-slash");
        eyeIcon.classList.add("bi-eye");
    } else {
        field.type = "password";
        eyeIcon.classList.remove("bi-eye");
        eyeIcon.classList.add("bi-eye-slash");
    }
}
// Funktion 2: Passwort-Stärke live berechnen
function checkPasswordStrength(val) {
    if (val.length === 0) {
        strengthBar.style.width = "0%";
        strengthBar.style.backgroundColor = "#e0e0e0";
        return;
    }
    
    let points = 0;
    if (val.length >= 8) points++;
    if (/[0-9]/.test(val)) points++; 
    if (/[A-Z]/.test(val)) points++; 
    if (/[^A-Za-z0-9]/.test(val)) points++; 
    if (val.length < 8) {
        strengthBar.style.width = "30%";
        strengthBar.style.backgroundColor = "#dc3545"; // Rot (Zu kurz)
    } else if (points <= 2) {
        strengthBar.style.width = "60%";
        strengthBar.style.backgroundColor = "#ffc107"; // Orange (Mittel)
    } else {
        strengthBar.style.width = "100%";
        strengthBar.style.backgroundColor = "#198754"; // Grün (Stark)
    }
}
// Funktion 3: Validierung & Button-Sperre
function validateForm() {
    const passVal = password.value;
    const confirmVal = confirmPassword.value;
    
    // Stärkemesser aktualisieren
    checkPasswordStrength(passVal);
    const isTooShort = passVal.length < 8;
    const isNotMatching = passVal !== confirmVal;
    // Logik-Korrektur: Fehler anzeigen und Button sperren
    if (isTooShort || isNotMatching) {
        submitBtn.disabled = true;
        
        if (passVal.length > 0 || confirmVal !== "") {
            errorMessage.style.display = "block";
            if (isTooShort) {
                errorMessage.textContent = document.body.dataset.passwordTooShort;
            } else {
                errorMessage.textContent = document.body.dataset.passwordMismatch;
            }
        } else {
            errorMessage.style.display = "none";
        }
    } else {
        errorMessage.style.display = "none";
        submitBtn.disabled = false;
    }
}
// Event-Listener für Echtzeit-Prüfung beim Tippen
password.addEventListener("input", validateForm);
confirmPassword.addEventListener("input", validateForm);