let currentTab = 0; // Start bei Schritt 0 (Index-basiert)
let summe = 0;

showTab(currentTab);

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

function getRandomInt(min, max) {
  // Math.floor rundet die Zahl ab
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

async function showTab(n) {
    let tabs = document.getElementsByClassName("form-step");
    tabs[n].classList.add("active");
    // Buttons anpassen
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (tabs.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Abschließen";
    } else {
        document.getElementById("nextBtn").innerHTML = "Weiter";
        document.getElementById("nextBtn").disabled = false;
    }
    updateStepper(n);
}

async function submitForm() {
    document.getElementById('step-4').removeAttribute('hidden');
    document.getElementById('nextBtn').hidden = true;
    document.getElementById('prevBtn').hidden = true;

    progressBar = document.getElementById("progressBar");
    progressBarInner = document.getElementById("progressBarInner");
    while (summe < 100) {
        const rest = 100 - summe;
        const maxValue = Math.min(3, rest);
        const randomValue = Math.floor(Math.random() * maxValue) + 1;
        summe += randomValue;
        progressBarInner.style.width = summe + "%";
        await wait(getRandomInt(150, 350));
    }

    document.getElementById("nextBtn").disabled = true;
}
async function nextPrev(n) {
    let tabs = document.getElementsByClassName("form-step");
    // Wenn "Weiter" geklickt wird, validiere die Felder im aktuellen Schritt
    if (n == 1 && !await validateForm()) return false;
    // Verstecke aktuellen Schritt
    tabs[currentTab].classList.remove("active");
    currentTab = currentTab + n;
    // Wenn das Ende erreicht ist, Formular abschicken
    if (currentTab >= tabs.length) {
        document.getElementById("regForm").submit();
        document.getElementById("step-4").classList.add("active");
        await submitForm();
    }
    await showTab(currentTab);
}

// Verhindert das Weitergehen, wenn Pflichtfelder leer oder ungültig sind
async function validateForm() {
    let tabs = document.getElementsByClassName("form-step");
    let inputs = tabs[currentTab].getElementsByTagName("input");
    let selects = tabs[currentTab].getElementsByTagName("select");
    let valid = true;
    
    // 1. Standard-Pflichtfeld-Prüfung für Inputs
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].hasAttribute('required') && inputs[i].value == "") {
            inputs[i].classList.add("is-invalid");
            valid = false;
        } else {
            inputs[i].classList.remove("is-invalid");
        }
    }
    
    // 2. Standard-Pflichtfeld-Prüfung für Selects
    for (let i = 0; i < selects.length; i++) {
        if (selects[i].hasAttribute('required') && selects[i].value == "") {
            selects[i].classList.add("is-invalid");
            valid = false;
        } else {
            selects[i].classList.remove("is-invalid");
        }
    }

    // 3. NEU: Job-Katalog-Validierung (nur in Schritt 2 -> Index 1)
    if (currentTab === 1) { // currentTab 1 entspricht dem <div id="step-2">
        const jobInput = document.getElementById('goal_job');
        const jobList = document.getElementById('job_liste');
        
        if (jobInput && jobList) {
            // Hole alle erlaubten Titel aus der HTML-Datalist
            const validJobs = Array.from(jobList.options).map(option => option.value);
            const userInput = jobInput.value.trim();
            
            // Wenn der eingegebene Text nicht exakt mit einem Listeneintrag übereinstimmt
            if (!validJobs.includes(userInput)) {
                jobInput.classList.add("is-invalid");
                
                // Eine schöne Bootstrap-Fehlermeldung per Alert ausgeben
                alert(document.body.dataset.invalidJobMessage);
                
                jobInput.focus();
                valid = false; // Blockiert das Weitergehen!
            } else {
                jobInput.classList.remove("is-invalid");
            }
        }
    }
    
    return valid;
}
// Färbt die Kreise und Linien im Stepper blau
function updateStepper(n) {
    for (let i = 1; i <= 3; i++) {
        let indicator = document.getElementById("step-indicator-" + i);
        if (i < n + 1) {
            indicator.className = "stepper-item completed"; // Komplett blau inklusive Verbindungslinie
        } else if (i == n + 1) {
            indicator.className = "stepper-item active";    // Nur der Kreis blau
        } else {
            indicator.className = "stepper-item";           // Grau
        }
    }
}