SKILL_CATALOG = [
    # --- Programming & Development ---
    {"skill": "Python", "category": "Programming"},
    {"skill": "JavaScript", "category": "Programming"},
    {"skill": "HTML & CSS", "category": "Programming"},
    {"skill": "Basic HTML/CSS", "category": "Programming"},
    {"skill": "Python (Basics)", "category": "Programming"},
    {"skill": "Linux & Bash", "category": "Programming"},
    
    # --- Data & AI ---
    {"skill": "Statistics", "category": "Data & AI"},
    {"skill": "Machine Learning", "category": "Data & AI"},
    {"skill": "Deep Learning", "category": "Data & AI"},
    {"skill": "Model Evaluation", "category": "Data & AI"},
    {"skill": "SQL", "category": "Data & AI"},
    {"skill": "Data Visualization", "category": "Data & AI"},
    {"skill": "ETL Pipelines", "category": "Data & AI"},
    {"skill": "Big Data (Spark/Hadoop)", "category": "Data & AI"},
    {"skill": "Cloud Databases", "category": "Data & AI"},
    {"skill": "Excel / Google Sheets", "category": "Data & AI"},
    {"skill": "Tableau / PowerBI", "category": "Data & AI"},
    {"skill": "Data Interpretation", "category": "Data & AI"},
    
    # --- Engineering & Infrastructure ---
    {"skill": "Git", "category": "Engineering Tools"},
    {"skill": "Cloud Deployment", "category": "Infrastructure"},
    {"skill": "API Development", "category": "Engineering Tools"},
    {"skill": "API Consumption", "category": "Engineering Tools"},
    {"skill": "CI/CD Pipelines", "category": "Infrastructure"},
    {"skill": "Docker & Kubernetes", "category": "Infrastructure"},
    
    # --- Product, Design & Agility ---
    {"skill": "Agile Methodologies (Scrum)", "category": "Product Management"},
    {"skill": "Requirements Engineering", "category": "Product Management"},
    {"skill": "Stakeholder Management", "category": "Product Management"},
    {"skill": "Product Strategy", "category": "Product Management"},
    {"skill": "Technical Basics", "category": "Product Management"},
    {"skill": "Figma / Adobe XD", "category": "Design"},
    {"skill": "User Research", "category": "Design"},
    {"skill": "Wireframing & Prototyping", "category": "Design"},
    {"skill": "Design Systems", "category": "Design"},
    
    # --- Marketing & Quality Assurance ---
    {"skill": "SEO & SEM", "category": "Marketing"},
    {"skill": "Google Analytics", "category": "Marketing"},
    {"skill": "Copywriting", "category": "Marketing"},
    {"skill": "Social Media Ad Platforms", "category": "Marketing"},
    {"skill": "A/B Testing", "category": "Marketing"},
    {"skill": "Manual Testing", "category": "Quality Assurance"},
    {"skill": "Test Case Writing", "category": "Quality Assurance"},
    {"skill": "Bug Tracking Tools (Jira)", "category": "Quality Assurance"},
    {"skill": "Test Automation Basics", "category": "Quality Assurance"},
    {"skill": "Communication", "category": "Soft Skills"},
]

_LESSONS_BY_SKILL = {

    # =========================================================
    # 1. PYTHON — 10 Fragen
    # =========================================================
    "Python": [
        (
            "Variable erstellen",
            "Variablen werden in Python mit '=' erstellt. Ein Datentyp muss normalerweise nicht angegeben werden. Beispiel: 'grade = 'A''",
            "Erstelle die Variable 'age' und speichere den Wert 13 darin.",
            "age = 13"
        ),
        (
            "String speichern",
            "Texte werden in Python normalerweise in einfachen oder doppelten Anführungszeichen gespeichert.",
            "Erstelle die Variable 'name' und speichere darin den Text 'John'.",
            "name = 'John'"
        ),
        (
            "Liste erstellen",
            "Listen speichern mehrere Werte. Sie werden mit eckigen Klammern erstellt. Beispiel: 'numbers = [1, 2, 2, 3]'",
            "Definiere die Liste 'cars' mit den Einträgen 'Ford', 'BMW' und 'Tesla'.",
            "cars = ['Ford', 'BMW', 'Tesla']"
        ),
        (
            "Auf Listenelement zugreifen",
            "Python verwendet bei Listen einen nullbasierten Index. Das erste Element hat also den Index 0. Man schreibt also für den dritten Listeneintrag: 'list[2]'",
            "Greife auf das zweite Element der Liste 'cars' zu.",
            "cars[1]"
        ),
        (
            "if-Bedingung",
            "Mit if kann Code nur ausgeführt werden, wenn eine Bedingung wahr ist. Man schreibt: 'if number == 2:'",
            "Schreibe eine if-Bedingung, die prüft, ob 'age' mindestens 18 ist.",
            "if age >= 18:"
        ),
        (
            "for-Schleife",
            "Mit einer for-Schleife kannst du alle Elemente einer Liste nacheinander verarbeiten. Man schreibt zum Beispiel: 'for number in numbers:'",
            "Schreibe eine for-Schleife, die jedes Element aus 'cars' in der Variable 'car' durchläuft.",
            "for car in cars:"
        ),
        (
            "Funktion definieren",
            "Eigene Funktionen werden mit 'def' definiert. Dahinter schreibt man den Namen der Funktion und Klammern. Beispiel: 'def test():'",
            "Erstelle eine Funktion 'greet', die den Text 'Hello!' ausgibt.",
            "def greet():"
        ),
        (
            "Funktion mit Parameter",
            "Funktionen können Parameter erhalten, die beim Aufruf übergeben werden. Diese schreibt man in die Klammern hinter dem Funktionsnamen.",
            "Erstelle eine Funktion 'greet', die den Parameter 'name' erhält.",
            "def greet(name):"
        ),
        (
            "Dictionary erstellen",
            "Dictionaries speichern Daten als Schlüssel-Wert-Paare. Man schreibt sie in geschweifte Klammern. zwischen Schlüssel und Wert schreibt man einen Doppelpunkt, zwischen zwei verschiedene Paare ein Komma. Beispiel: 'product = {'name': 'Ice', 'price': '20'}'",
            "Erstelle ein Dictionary 'user' mit dem Namen 'John' und dem Alter 13.",
            "user = {'name': 'John', 'age': 13}"
        ),
        (
            "Liste erweitern",
            "Mit .append() kannst du ein neues Element am Ende einer Liste hinzufügen. Beispiel: numbers.append(4)",
            "Füge 'Audi' am Ende der Liste 'cars' hinzu.",
            "cars.append('Audi')"
        )
    ],


    # =========================================================
    # 2. JAVASCRIPT — 10 Fragen
    # =========================================================
    "JavaScript": [
        (
            "Variable erstellen",
            "Variablen werden in Python mit '=' erstellt. Ein Datentyp muss normalerweise nicht angegeben werden. Beispiel: 'grade = 'A''",
            "Erstelle die Variable 'age' und speichere den Wert 13 darin.",
            "age = 13"
        ),
        (
            "String speichern",
            "Texte werden in Python normalerweise in einfachen oder doppelten Anführungszeichen gespeichert.",
            "Erstelle die Variable 'name' und speichere darin den Text 'John'.",
            "name = 'John'"
        ),
        (
            "Liste erstellen",
            "Listen speichern mehrere Werte. Sie werden mit eckigen Klammern erstellt. Beispiel: 'numbers = [1, 2, 2, 3]'",
            "Definiere die Liste 'cars' mit den Einträgen 'Ford', 'BMW' und 'Tesla'.",
            "cars = ['Ford', 'BMW', 'Tesla']"
        ),
        (
            "Auf Listenelement zugreifen",
            "Python verwendet bei Listen einen nullbasierten Index. Das erste Element hat also den Index 0. Man schreibt also für den dritten Listeneintrag: 'list[2]'",
            "Greife auf das zweite Element der Liste 'cars' zu.",
            "cars[1]"
        ),
        (
            "if-Bedingung",
            "Mit if kann Code nur ausgeführt werden, wenn eine Bedingung wahr ist. Man schreibt: 'if number == 2:'",
            "Schreibe eine if-Bedingung, die prüft, ob 'age' mindestens 18 ist.",
            "if age >= 18:"
        ),
        (
            "for-Schleife",
            "Mit einer for-Schleife kannst du alle Elemente einer Liste nacheinander verarbeiten. Man schreibt zum Beispiel: 'for number in numbers:'",
            "Schreibe eine for-Schleife, die jedes Element aus 'cars' in der Variable 'car' durchläuft.",
            "for car in cars:"
        ),
        (
            "Funktion definieren",
            "Eigene Funktionen werden mit 'def' definiert. Dahinter schreibt man den Namen der Funktion und Klammern. Beispiel: 'def test():'",
            "Erstelle eine Funktion 'greet', die den Text 'Hello!' ausgibt.",
            "def greet():"
        ),
        (
            "Funktion mit Parameter",
            "Funktionen können Parameter erhalten, die beim Aufruf übergeben werden. Diese schreibt man in die Klammern hinter dem Funktionsnamen.",
            "Erstelle eine Funktion 'greet', die den Parameter 'name' erhält.",
            "def greet(name):"
        ),
        (
            "Dictionary erstellen",
            "Dictionaries speichern Daten als Schlüssel-Wert-Paare. Man schreibt sie in geschweifte Klammern. zwischen Schlüssel und Wert schreibt man einen Doppelpunkt, zwischen zwei verschiedene Paare ein Komma. Beispiel: 'product = {'name': 'Ice', 'price': '20'}'",
            "Erstelle ein Dictionary 'user' mit dem Namen 'John' und dem Alter 13.",
            "user = {'name': 'John', 'age': 13}"
        ),
        (
            "Liste erweitern",
            "Mit .append() kannst du ein neues Element am Ende einer Liste hinzufügen. Beispiel: numbers.append(4)",
            "Füge 'Audi' am Ende der Liste 'cars' hinzu.",
            "cars.append('Audi')"
        )
    ],


    # =========================================================
    # 3. HTML & CSS — 10 Fragen
    # =========================================================
    "HTML & CSS": [
        (
            "Überschrift erstellen",
            "Das HTML-Element h1 wird für die wichtigste Überschrift einer Seite verwendet.",
            "Erstelle eine h1-Überschrift mit dem Text 'FluffelSkills'.",
            "<h1>FluffelSkills</h1>"
        ),
        (
            "Absatz erstellen",
            "Mit dem p-Element werden Textabsätze erstellt.",
            "Erstelle einen Absatz mit dem Text 'Welcome to FluffelSkills'.",
            "<p>Welcome to FluffelSkills</p>"
        ),
        (
            "Link erstellen",
            "Mit dem a-Element können Links erstellt werden. Die Zieladresse steht im href-Attribut.",
            "Erstelle einen Link zu https://fluffelskills.pythonanywhere.com/ mit dem Text 'FluffelSkills'.",
            '<a href="https://fluffelskills.pythonanywhere.com/">FluffelSkills</a>'
        ),
        (
            "Bild einfügen",
            "Das img-Element bindet ein Bild ein. Das src-Attribut enthält den Pfad zur Datei.",
            "Füge das Bild 'logo.png' ein.",
            '<img src="logo.png" alt="Logo">'
        ),
        (
            "Button erstellen",
            "Mit dem button-Element kannst du einen anklickbaren Button erstellen.",
            "Erstelle einen Button mit dem Text 'Start'.",
            '<button>Start</button>'
        ),
        (
            "Textfarbe ändern",
            "Mit der CSS-Eigenschaft color kannst du die Textfarbe festlegen.",
            "Setze die Textfarbe eines Elements auf blau.",
            "color: blue;"
        ),
        (
            "Hintergrundfarbe ändern",
            "Mit background-color wird die Hintergrundfarbe eines Elements festgelegt.",
            "Setze die Hintergrundfarbe eines Elements auf schwarz.",
            "background-color: black;"
        ),
        (
            "Klasse definieren",
            "Mit einem Punkt wird in CSS ein Klassen-Selektor angesprochen.",
            "Schreibe einen CSS-Selektor für die Klasse 'card'.",
            ".card { }"
        ),
        (
            "Flexbox aktivieren",
            "display: flex aktiviert das Flexbox-Layout.",
            "Aktiviere Flexbox für ein Element.",
            "display: flex;"
        ),
        (
            "Abstand festlegen",
            "margin erzeugt Außenabstand, padding erzeugt Innenabstand.",
            "Setze für ein Element einen Innenabstand von 20 Pixeln.",
            "padding: 20px;"
        )
    ],


    # =========================================================
    # 4. SQL — 10 Fragen
    # =========================================================
    "SQL": [
        (
            "Daten mit SELECT abfragen",
            "SELECT wird verwendet, um Daten aus einer Tabelle abzurufen.",
            "Lies die Spalte 'name' aus der Tabelle 'clients' aus.",
            "SELECT name FROM clients;"
        ),
        (
            "Alle Spalten auswählen",
            "Mit * werden alle Spalten einer Tabelle ausgewählt.",
            "Gib alle Spalten der Tabelle 'users' aus.",
            "SELECT * FROM users;"
        ),
        (
            "Mit WHERE filtern",
            "WHERE filtert Datensätze nach einer Bedingung.",
            "Gib alle Benutzer aus der Tabelle 'users' aus, deren Alter 18 ist.",
            "SELECT * FROM users WHERE age = 18;"
        ),
        (
            "Datensatz hinzufügen",
            "INSERT INTO fügt neue Datensätze in eine Tabelle ein.",
            "Füge einen Benutzer namens 'Florian' mit dem Alter 13 in die Tabelle 'users' ein.",
            "INSERT INTO users (name, age) VALUES ('Florian', 13);"
        ),
        (
            "Datensatz ändern",
            "UPDATE verändert vorhandene Datensätze.",
            "Setze das Alter des Benutzers 'Florian' auf 14.",
            "UPDATE users SET age = 14 WHERE name = 'Florian';"
        ),
        (
            "Datensatz löschen",
            "DELETE löscht Datensätze aus einer Tabelle.",
            "Lösche den Benutzer 'Florian' aus der Tabelle 'users'.",
            "DELETE FROM users WHERE name = 'Florian';"
        ),
        (
            "Sortieren",
            "ORDER BY sortiert die Ergebnisse einer Abfrage.",
            "Gib alle Benutzer aus und sortiere sie nach dem Alter aufsteigend.",
            "SELECT * FROM users ORDER BY age ASC;"
        ),
        (
            "Anzahl zählen",
            "COUNT() zählt die Anzahl der Datensätze oder Werte.",
            "Zähle die Anzahl aller Benutzer in der Tabelle 'users'.",
            "SELECT COUNT(*) FROM users;"
        ),
        (
            "Tabellen verbinden",
            "JOIN verbindet Datensätze aus mehreren Tabellen über gemeinsame Werte.",
            "Verbinde 'users' und 'orders' über die Spalte 'user_id'.",
            "SELECT * FROM users JOIN orders ON users.id = orders.user_id;"
        ),
        (
            "Gruppieren",
            "GROUP BY fasst Datensätze mit gleichen Werten zusammen.",
            "Zähle, wie viele Benutzer es pro Land gibt.",
            "SELECT country, COUNT(*) FROM users GROUP BY country;"
        )
    ],


    # =========================================================
    # 5. GIT — 10 Fragen
    # =========================================================
    "Git": [
        (
            "Repository klonen",
            "git clone kopiert ein bestehendes Repository auf den eigenen Computer.",
            "Klone das Repository 'Flask-Dashboard' vom GitHub-Benutzer 'John123'.",
            "git clone https://github.com/John123/Flask-Dashboard.git"
        ),
        (
            "Repository initialisieren",
            "git init erstellt in einem Ordner ein neues Git-Repository.",
            "Initialisiere im aktuellen Ordner ein neues Git-Repository.",
            "git init"
        ),
        (
            "Status anzeigen",
            "git status zeigt, welche Dateien geändert oder noch nicht versioniert wurden.",
            "Zeige den aktuellen Status des Repositorys an.",
            "git status"
        ),
        (
            "Datei zur Staging Area hinzufügen",
            "git add merkt Änderungen für den nächsten Commit vor.",
            "Füge die Datei 'app.py' zur Staging Area hinzu.",
            "git add app.py"
        ),
        (
            "Alle Änderungen hinzufügen",
            "git add . fügt alle Änderungen im aktuellen Verzeichnis zur Staging Area hinzu.",
            "Füge alle aktuellen Änderungen zur Staging Area hinzu.",
            "git add ."
        ),
        (
            "Commit erstellen",
            "Ein Commit speichert einen bestimmten Stand des Projekts.",
            "Erstelle einen Commit mit der Nachricht 'Initial version'.",
            "git commit -m 'Initial version'"
        ),
        (
            "Änderungen pushen",
            "git push lädt lokale Commits auf das Remote-Repository hoch.",
            "Lade den aktuellen main-Branch zum Remote-Repository 'origin' hoch.",
            "git push origin main"
        ),
        (
            "Änderungen holen",
            "git pull lädt Änderungen vom Remote-Repository herunter und integriert sie.",
            "Hole die Änderungen des main-Branches von 'origin'.",
            "git pull origin main"
        ),
        (
            "Branch erstellen",
            "Branches ermöglichen getrennte Entwicklungszweige.",
            "Erstelle einen neuen Branch namens 'feature-login'.",
            "git branch feature-login"
        ),
        (
            "Branch wechseln",
            "git switch wechselt auf einen anderen Branch.",
            "Wechsle zum Branch 'feature-login'.",
            "git switch feature-login"
        )
    ],


    # =========================================================
    # 6. LINUX & BASH — 7 Fragen
    # =========================================================
    "Linux & Bash": [
        (
            "Aktuellen Ordner anzeigen",
            "pwd zeigt den vollständigen Pfad des aktuellen Arbeitsverzeichnisses.",
            "Zeige den aktuellen Arbeitsordner an.",
            "pwd"
        ),
        (
            "Dateien anzeigen",
            "ls listet Dateien und Ordner im aktuellen Verzeichnis auf.",
            "Zeige alle Dateien und Ordner im aktuellen Verzeichnis an.",
            "ls"
        ),
        (
            "Ordner wechseln",
            "cd wechselt das aktuelle Arbeitsverzeichnis.",
            "Wechsle in den Ordner 'projects'.",
            "cd projects"
        ),
        (
            "Ordner erstellen",
            "mkdir erstellt einen neuen Ordner.",
            "Erstelle einen Ordner namens 'FluffelSkills'.",
            "mkdir FluffelSkills"
        ),
        (
            "Datei kopieren",
            "cp kopiert Dateien oder Ordner.",
            "Kopiere die Datei 'app.py' nach 'backup.py'.",
            "cp app.py backup.py"
        ),
        (
            "Datei umbenennen",
            "mv kann unter Linux auch zum Umbenennen von Dateien verwendet werden.",
            "Benenne 'old.py' in 'new.py' um.",
            "mv old.py new.py"
        ),
        (
            "Datei löschen",
            "rm löscht Dateien.",
            "Lösche die Datei 'test.txt'.",
            "rm test.txt"
        )
    ],


    # =========================================================
    # 7. API DEVELOPMENT — 7 Fragen
    # =========================================================
    "API Development": [
        (
            "Flask-API starten",
            "Flask kann verwendet werden, um schnell eine Web-API zu erstellen.",
            "Erstelle eine minimale Flask-App-Definition.",
            "app = Flask(__name__)"
        ),
        (
            "GET-Route erstellen",
            "Mit einer GET-Route kannst du Daten über eine URL bereitstellen.",
            "Erstelle eine Flask-Route '/api/status', die auf GET-Anfragen reagiert.",
            "@app.route('/api/status', methods=['GET'])"
        ),
        (
            "JSON zurückgeben",
            "jsonify erzeugt eine JSON-Antwort für Flask.",
            "Gib aus einer Flask-Route das JSON {'status': 'ok'} zurück.",
            "return jsonify({'status': 'ok'})"
        ),
        (
            "POST-Route erstellen",
            "POST wird typischerweise verwendet, um Daten an eine API zu senden.",
            "Erstelle eine Flask-Route '/api/users', die POST-Anfragen akzeptiert.",
            "@app.route('/api/users', methods=['POST'])"
        ),
        (
            "Request-Daten lesen",
            "request.json enthält JSON-Daten, die mit einer POST-Anfrage übertragen wurden.",
            "Lies die JSON-Daten einer Anfrage in der Variable 'data' aus.",
            "data = request.json"
        ),
        (
            "HTTP-Statuscode setzen",
            "Mit einer Statusnummer kann eine API das Ergebnis einer Anfrage genauer kennzeichnen.",
            "Gib aus einer Flask-Route eine JSON-Antwort mit dem Statuscode 201 zurück.",
            "return jsonify({'created': True}), 201"
        ),
        (
            "URL-Parameter",
            "URL-Parameter können direkt in einer Route definiert und als Funktionsparameter gelesen werden.",
            "Erstelle eine Flask-Route '/api/users/<id>', die die Benutzer-ID als Parameter erhält.",
            "@app.route('/api/users/<id>')"
        )
    ],


    # =========================================================
    # 8. API CONSUMPTION — 7 Fragen
    # =========================================================
    "API Consumption": [
        (
            "GET-Anfrage senden",
            "Mit der requests-Bibliothek kann Python HTTP-Anfragen an APIs senden.",
            "Sende eine GET-Anfrage an 'https://api.example.com/users'.",
            "response = requests.get('https://api.example.com/users')"
        ),
        (
            "JSON auslesen",
            "response.json() wandelt die JSON-Antwort einer API in Python-Daten um.",
            "Lies die JSON-Antwort der Variable 'response' aus.",
            "data = response.json()"
        ),
        (
            "POST-Anfrage senden",
            "Mit requests.post() kannst du Daten an eine API senden.",
            "Sende den JSON-Inhalt {'name': 'Florian'} per POST an '/users'.",
            "response = requests.post('https://api.example.com/users', json={'name': 'Florian'})"
        ),
        (
            "Authorization Header",
            "Viele APIs benötigen einen Token im Authorization-Header.",
            "Sende den Token 'abc123' als Bearer Token mit einer Anfrage.",
            "headers = {'Authorization': 'Bearer abc123'}"
        ),
        (
            "Query-Parameter",
            "Query-Parameter werden häufig verwendet, um API-Ergebnisse zu filtern oder zu verändern.",
            "Rufe '/users' mit dem Parameter 'limit=10' auf.",
            "response = requests.get('https://api.example.com/users', params={'limit': 10})"
        ),
        (
            "Statuscode prüfen",
            "response.status_code enthält den HTTP-Statuscode der Antwort.",
            "Prüfe, ob die API den Statuscode 200 zurückgegeben hat.",
            "if response.status_code == 200:"
        ),
        (
            "Timeout setzen",
            "Ein Timeout verhindert, dass ein Programm unbegrenzt auf eine API wartet.",
            "Sende eine GET-Anfrage mit einem Timeout von 5 Sekunden.",
            "response = requests.get('https://api.example.com/users', timeout=5)"
        )
    ],


    # =========================================================
    # 9. MACHINE LEARNING — 7 Fragen
    # =========================================================
    "Machine Learning": [
        (
            "Daten aufteilen",
            "Für Machine Learning werden Daten häufig in Trainings- und Testdaten aufgeteilt.",
            "Teile X und y mit train_test_split in Trainings- und Testdaten auf.",
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)"
        ),
        (
            "Modell erstellen",
            "Scikit-learn bietet viele fertige Machine-Learning-Modelle.",
            "Erstelle einen RandomForestClassifier.",
            "model = RandomForestClassifier()"
        ),
        (
            "Modell trainieren",
            "fit() trainiert ein Machine-Learning-Modell mit den Trainingsdaten.",
            "Trainiere das Modell mit X_train und y_train.",
            "model.fit(X_train, y_train)"
        ),
        (
            "Vorhersage erstellen",
            "predict() verwendet ein trainiertes Modell, um neue Werte vorherzusagen.",
            "Erstelle Vorhersagen für X_test.",
            "predictions = model.predict(X_test)"
        ),
        (
            "Features skalieren",
            "StandardScaler bringt numerische Features ungefähr auf eine einheitliche Skala.",
            "Erstelle einen StandardScaler.",
            "scaler = StandardScaler()"
        ),
        (
            "Modell speichern",
            "Mit joblib kann ein trainiertes Scikit-learn-Modell gespeichert werden.",
            "Speichere das Modell als 'model.pkl'.",
            "joblib.dump(model, 'model.pkl')"
        ),
        (
            "Modell laden",
            "Ein gespeichertes Modell kann später wieder geladen werden.",
            "Lade das Modell aus 'model.pkl'.",
            "model = joblib.load('model.pkl')"
        )
    ],


    # =========================================================
    # 10. STATISTICS — 7 Fragen
    # =========================================================
    "Statistics": [
        (
            "Mittelwert berechnen",
            "Der Mittelwert ist die Summe aller Werte geteilt durch ihre Anzahl.",
            "Berechne mit NumPy den Mittelwert des Arrays 'values'.",
            "mean = np.mean(values)"
        ),
        (
            "Median berechnen",
            "Der Median ist der mittlere Wert einer sortierten Datenmenge.",
            "Berechne den Median des Arrays 'values'.",
            "median = np.median(values)"
        ),
        (
            "Standardabweichung berechnen",
            "Die Standardabweichung misst, wie stark die Werte um den Mittelwert streuen.",
            "Berechne die Standardabweichung von 'values'.",
            "std = np.std(values)"
        ),
        (
            "Varianz berechnen",
            "Die Varianz ist das Quadrat der Standardabweichung.",
            "Berechne die Varianz von 'values'.",
            "variance = np.var(values)"
        ),
        (
            "Korrelation berechnen",
            "Die Pearson-Korrelation beschreibt den linearen Zusammenhang zwischen zwei Variablen.",
            "Berechne mit NumPy die Korrelationsmatrix für 'x' und 'y'.",
            "correlation = np.corrcoef(x, y)"
        ),
        (
            "Zufällige Stichprobe",
            "Eine zufällige Stichprobe kann verwendet werden, um einen Teil einer größeren Datenmenge auszuwählen.",
            "Wähle mit NumPy zufällig 10 Elemente aus dem Array 'values' aus.",
            "sample = np.random.choice(values, 10)"
        ),
        (
            "Quantil berechnen",
            "Ein Quantil beschreibt einen bestimmten Punkt in einer Verteilung.",
            "Berechne das 75%-Quantil von 'values'.",
            "q75 = np.percentile(values, 75)"
        )
    ],


    # =========================================================
    # 11. DATA VISUALIZATION — 7 Fragen
    # =========================================================
    "Data Visualization": [
        (
            "Balkendiagramm",
            "Mit matplotlib kannst du Daten als Balkendiagramm darstellen.",
            "Erstelle ein Balkendiagramm mit den Kategorien 'Python' und 'JavaScript' und den Werten 90 und 70.",
            "plt.bar(['Python', 'JavaScript'], [90, 70])"
        ),
        (
            "Liniendiagramm",
            "Liniendiagramme eignen sich besonders für zeitliche Entwicklungen.",
            "Erstelle ein Liniendiagramm aus den Werten in 'sales'.",
            "plt.plot(sales)"
        ),
        (
            "Streudiagramm",
            "Ein Scatterplot zeigt den Zusammenhang zwischen zwei numerischen Variablen.",
            "Erstelle einen Scatterplot aus 'x' und 'y'.",
            "plt.scatter(x, y)"
        ),
        (
            "Diagrammtitel",
            "Mit plt.title() kannst du einem Diagramm einen Titel geben.",
            "Setze den Titel des aktuellen Diagramms auf 'Skills'.",
            "plt.title('Skills')"
        ),
        (
            "X-Achse beschriften",
            "Mit plt.xlabel() wird die Beschriftung der X-Achse gesetzt.",
            "Beschrifte die X-Achse mit 'Skill'.",
            "plt.xlabel('Skill')"
        ),
        (
            "Diagramm anzeigen",
            "plt.show() zeigt das aktuelle matplotlib-Diagramm an.",
            "Zeige das aktuelle Diagramm an.",
            "plt.show()"
        ),
        (
            "Histogramm",
            "Ein Histogramm zeigt die Verteilung numerischer Werte.",
            "Erstelle ein Histogramm aus den Daten in 'ages'.",
            "plt.hist(ages)"
        )
    ],


    # =========================================================
    # 12. EXCEL / GOOGLE SHEETS — 7 Fragen
    # =========================================================
    "Excel / Google Sheets": [
        (
            "SUMME",
            "SUM addiert mehrere Zellen oder Werte.",
            "Addiere die Werte aus A1 bis A10.",
            "=SUM(A1:A10)"
        ),
        (
            "Durchschnitt",
            "AVERAGE berechnet den Mittelwert eines Zellbereichs.",
            "Berechne den Durchschnitt der Werte aus B1 bis B10.",
            "=AVERAGE(B1:B10)"
        ),
        (
            "WENN",
            "IF prüft eine Bedingung und gibt abhängig vom Ergebnis unterschiedliche Werte zurück.",
            "Gib 'Bestanden' aus, wenn A1 mindestens 50 ist, sonst 'Nicht bestanden'.",
            '=IF(A1>=50,"Bestanden","Nicht bestanden")'
        ),
        (
            "MAXIMUM",
            "MAX gibt den größten Wert aus einem Bereich zurück.",
            "Finde den größten Wert aus C1 bis C20.",
            "=MAX(C1:C20)"
        ),
        (
            "MINIMUM",
            "MIN gibt den kleinsten Wert aus einem Bereich zurück.",
            "Finde den kleinsten Wert aus C1 bis C20.",
            "=MIN(C1:C20)"
        ),
        (
            "ZÄHLENWENN",
            "COUNTIF zählt Zellen, die ein bestimmtes Kriterium erfüllen.",
            "Zähle in A1:A100, wie oft der Wert 'Python' vorkommt.",
            '=COUNTIF(A1:A100,"Python")'
        ),
        (
            "SVERWEIS / XLOOKUP",
            "XLOOKUP kann anhand eines Suchwerts den passenden Wert aus einem anderen Bereich zurückgeben.",
            "Suche den Wert aus A2 in D2:D20 und gib den passenden Wert aus E2:E20 zurück.",
            "=XLOOKUP(A2,D2:D20,E2:E20)"
        )
    ],


    # =========================================================
    # 13. ETL PIPELINES — 7 Fragen
    # =========================================================
    "ETL Pipelines": [
        (
            "CSV laden",
            "Pandas kann CSV-Dateien in einen DataFrame laden.",
            "Lade die Datei 'users.csv' in einen DataFrame namens 'df'.",
            "df = pd.read_csv('users.csv')"
        ),
        (
            "Spalte auswählen",
            "Mit dem Spaltennamen kann eine einzelne DataFrame-Spalte ausgewählt werden.",
            "Wähle die Spalte 'age' aus dem DataFrame 'df' aus.",
            "ages = df['age']"
        ),
        (
            "Zeilen filtern",
            "Mit booleschen Bedingungen können bestimmte Zeilen eines DataFrames ausgewählt werden.",
            "Erstelle einen neuen DataFrame mit allen Benutzern, die mindestens 18 Jahre alt sind.",
            "adults = df[df['age'] >= 18]"
        ),
        (
            "Fehlende Werte entfernen",
            "dropna() entfernt Zeilen mit fehlenden Werten.",
            "Entferne alle Zeilen mit fehlenden Werten aus 'df'.",
            "df = df.dropna()"
        ),
        (
            "Spalte umbenennen",
            "rename() kann Spaltennamen ändern.",
            "Benenne die Spalte 'name' in 'username' um.",
            "df = df.rename(columns={'name': 'username'})"
        ),
        (
            "CSV speichern",
            "to_csv() speichert einen DataFrame als CSV-Datei.",
            "Speichere den DataFrame 'df' als 'clean_users.csv' ohne Index.",
            "df.to_csv('clean_users.csv', index=False)"
        ),
        (
            "Daten zusammenführen",
            "merge() verbindet DataFrames anhand gemeinsamer Spalten.",
            "Verbinde die DataFrames 'users' und 'orders' über die Spalte 'user_id'.",
            "result = users.merge(orders, on='user_id')"
        )
    ],


    # =========================================================
    # 14. DEEP LEARNING — 5 Fragen
    # =========================================================
    "Deep Learning": [
        (
            "Neuronales Netzwerk",
            "In PyTorch können neuronale Netze mit nn.Module und Layern aufgebaut werden.",
            "Erstelle einen linearen Layer mit 10 Eingaben und 5 Ausgaben.",
            "layer = nn.Linear(10, 5)"
        ),
        (
            "Loss Function",
            "Eine Loss Function misst, wie stark die Vorhersage eines Modells vom Zielwert abweicht.",
            "Erstelle eine Cross-Entropy-Loss-Funktion für eine Klassifikation.",
            "loss_fn = nn.CrossEntropyLoss()"
        ),
        (
            "Optimizer",
            "Ein Optimizer verändert die Modellparameter anhand der berechneten Gradienten.",
            "Erstelle einen Adam-Optimizer für die Parameter von 'model' mit einer Lernrate von 0.001.",
            "optimizer = torch.optim.Adam(model.parameters(), lr=0.001)"
        ),
        (
            "Gradienten zurücksetzen",
            "Vor einem neuen Trainingsschritt müssen die alten Gradienten normalerweise zurückgesetzt werden.",
            "Setze die Gradienten des Optimizers zurück.",
            "optimizer.zero_grad()"
        ),
        (
            "Backpropagation",
            "backward() berechnet die Gradienten des Loss bezüglich der Modellparameter.",
            "Führe Backpropagation für die Variable 'loss' aus.",
            "loss.backward()"
        )
    ],


    # =========================================================
    # 15. MODEL EVALUATION — 5 Fragen
    # =========================================================
    "Model Evaluation": [
        (
            "Accuracy berechnen",
            "Accuracy beschreibt den Anteil der korrekten Vorhersagen.",
            "Berechne die Accuracy aus 'y_test' und 'predictions'.",
            "accuracy = accuracy_score(y_test, predictions)"
        ),
        (
            "Confusion Matrix",
            "Eine Confusion Matrix zeigt, wie häufig die verschiedenen Klassen korrekt oder falsch vorhergesagt wurden.",
            "Erstelle eine Confusion Matrix für 'y_test' und 'predictions'.",
            "cm = confusion_matrix(y_test, predictions)"
        ),
        (
            "Precision",
            "Precision beschreibt, wie viele der als positiv vorhergesagten Fälle tatsächlich positiv sind.",
            "Berechne die Precision für 'y_test' und 'predictions'.",
            "precision = precision_score(y_test, predictions)"
        ),
        (
            "Recall",
            "Recall beschreibt, wie viele der tatsächlich positiven Fälle gefunden wurden.",
            "Berechne den Recall für 'y_test' und 'predictions'.",
            "recall = recall_score(y_test, predictions)"
        ),
        (
            "F1-Score",
            "Der F1-Score kombiniert Precision und Recall.",
            "Berechne den F1-Score für 'y_test' und 'predictions'.",
            "f1 = f1_score(y_test, predictions)"
        )
    ],


    # =========================================================
    # 16. CI/CD PIPELINES — 5 Fragen
    # =========================================================
    "CI/CD Pipelines": [
        (
            "Workflow auslösen",
            "GitHub Actions Workflows können beispielsweise bei einem Push gestartet werden.",
            "Schreibe die YAML-Zeile, mit der ein Workflow bei jedem Push ausgelöst wird.",
            "push:"
        ),
        (
            "Checkout Action",
            "Die Checkout Action lädt den Repository-Code in einen GitHub-Actions-Runner.",
            "Verwende die aktuelle Checkout-v4-Action.",
            "uses: actions/checkout@v4"
        ),
        (
            "Python einrichten",
            "GitHub Actions kann Python über eine offizielle Action bereitstellen.",
            "Richte Python 3.13 mit der offiziellen Setup-Python-Action ein.",
            "uses: actions/setup-python@v5"
        ),
        (
            "Tests ausführen",
            "run führt einen Shell-Befehl innerhalb eines GitHub-Actions-Schritts aus.",
            "Führe mit GitHub Actions die Python-Tests mit pytest aus.",
            "run: pytest"
        ),
        (
            "Abhängigkeiten installieren",
            "pip installiert Python-Pakete aus einer requirements.txt-Datei.",
            "Installiere die Abhängigkeiten aus 'requirements.txt' in einem CI-Workflow.",
            "run: pip install -r requirements.txt"
        )
    ],


    # =========================================================
    # 17. DOCKER & KUBERNETES — 5 Fragen
    # =========================================================
    "Docker & Kubernetes": [
        (
            "Python-Image auswählen",
            "Die FROM-Anweisung legt das Basis-Image eines Docker Images fest.",
            "Verwende Python 3.13 als Basis-Image.",
            "FROM python:3.13"
        ),
        (
            "Docker Image bauen",
            "docker build erstellt ein Docker Image aus einem Dockerfile.",
            "Baue das aktuelle Docker-Projekt als Image mit dem Namen 'fluffelskills'.",
            "docker build -t fluffelskills ."
        ),
        (
            "Container starten",
            "docker run erstellt und startet einen Container aus einem Image.",
            "Starte das Image 'fluffelskills' und verbinde Port 8000 des Hosts mit Port 8000 im Container.",
            "docker run -p 8000:8000 fluffelskills"
        ),
        (
            "Kubernetes Deployment erstellen",
            "Ein Kubernetes Deployment verwaltet Pods und stellt die gewünschte Anzahl von Instanzen bereit.",
            "Erstelle ein Deployment aus der Datei 'deployment.yaml'.",
            "kubectl apply -f deployment.yaml"
        ),
        (
            "Kubernetes Pods anzeigen",
            "kubectl get pods zeigt die aktuell laufenden Pods an.",
            "Zeige alle Pods im aktuellen Kubernetes-Kontext an.",
            "kubectl get pods"
        )
    ],


    # =========================================================
    # 18. CLOUD DEPLOYMENT — 5 Fragen
    # =========================================================
    "Cloud Deployment": [
        (
            "Server auf allen Interfaces",
            "0.0.0.0 sorgt dafür, dass eine Webanwendung nicht nur auf localhost lauscht.",
            "Starte eine Flask-Anwendung auf Port 8000 und mache sie über alle Netzwerkinterfaces erreichbar.",
            "app.run(host='0.0.0.0', port=8000)"
        ),
        (
            "Gunicorn starten",
            "Gunicorn ist ein verbreiteter WSGI-Server für Python-Webanwendungen.",
            "Starte die Flask-Anwendung 'app' mit Gunicorn auf Port 8000.",
            "gunicorn app:app --bind 0.0.0.0:8000"
        ),
        (
            "Umgebungsvariable setzen",
            "Environment Variables speichern Konfigurationen außerhalb des Quellcodes.",
            "Setze unter Linux die Variable 'API_KEY' auf 'abc123'.",
            "export API_KEY='abc123'"
        ),
        (
            "HTTPS-Port",
            "HTTPS verwendet standardmäßig Port 443.",
            "Welche Portfreigabe würdest du für HTTPS konfigurieren?",
            "443"
        ),
        (
            "DNS-Test",
            "nslookup kann prüfen, welche IP-Adresse zu einem Domainnamen gehört.",
            "Prüfe über die Shell, auf welche IP-Adresse 'example.com' zeigt.",
            "nslookup example.com"
        )
    ],


    # =========================================================
    # 19. BIG DATA (SPARK/HADOOP) — 5 Fragen
    # =========================================================
    "Big Data (Spark/Hadoop)": [
        (
            "SparkSession erstellen",
            "Eine SparkSession ist der Einstiegspunkt für die Arbeit mit Apache Spark.",
            "Erstelle eine SparkSession namens 'spark'.",
            "spark = SparkSession.builder.appName('MyApp').getOrCreate()"
        ),
        (
            "CSV mit Spark laden",
            "Spark kann große CSV-Dateien als DataFrame einlesen.",
            "Lade die Datei 'users.csv' als Spark DataFrame.",
            "df = spark.read.csv('users.csv', header=True, inferSchema=True)"
        ),
        (
            "Spalte auswählen",
            "select() wählt bestimmte Spalten eines Spark DataFrames aus.",
            "Wähle die Spalten 'name' und 'age' aus 'df' aus.",
            "df.select('name', 'age')"
        ),
        (
            "Daten filtern",
            "filter() oder where() kann Datensätze anhand einer Bedingung filtern.",
            "Filtere alle Benutzer heraus, die mindestens 18 Jahre alt sind.",
            "df.filter(df.age >= 18)"
        ),
        (
            "DataFrame anzeigen",
            "show() gibt die ersten Zeilen eines Spark DataFrames aus.",
            "Zeige die ersten 20 Zeilen von 'df' an.",
            "df.show(20)"
        )
    ],


    # =========================================================
    # 20. CLOUD DATABASES — 5 Fragen
    # =========================================================
    "Cloud Databases": [
        (
            "PostgreSQL verbinden",
            "SQLAlchemy kann verwendet werden, um eine Verbindung zu einer PostgreSQL-Datenbank aufzubauen.",
            "Erstelle eine SQLAlchemy-Engine für eine PostgreSQL-Datenbank unter localhost:5432 mit der Datenbank 'app'.",
            "engine = create_engine('postgresql+psycopg://user:password@localhost:5432/app')"
        ),
        (
            "SQL ausführen",
            "Mit einer Datenbankverbindung können SQL-Anweisungen direkt ausgeführt werden.",
            "Führe über eine SQLAlchemy-Connection den Befehl 'SELECT * FROM users' aus.",
            "result = connection.execute(text('SELECT * FROM users'))"
        ),
        (
            "Transaktion speichern",
            "commit() bestätigt Änderungen innerhalb einer Transaktion.",
            "Bestätige eine Datenbanktransaktion.",
            "connection.commit()"
        ),
        (
            "Datenbank-URL aus Environment Variable",
            "Datenbankzugänge sollten nicht fest im Quellcode gespeichert werden.",
            "Lies die Datenbank-URL aus der Environment Variable 'DATABASE_URL'.",
            "database_url = os.getenv('DATABASE_URL')"
        ),
        (
            "Verbindung schließen",
            "Datenbankverbindungen sollten nach ihrer Verwendung geschlossen werden.",
            "Schließe die Variable 'connection'.",
            "connection.close()"
        )
    ]
}

_LESSON_CONTEXT = {
    "Python": "Python führt Anweisungen von oben nach unten aus. Einrückungen markieren Blöcke, etwa den Inhalt einer Bedingung oder Schleife; Namen und Satzzeichen müssen konsistent geschrieben sein.",
    "JavaScript": "JavaScript unterscheidet zwischen Variablendeklarationen, Funktionsaufrufen und Codeblöcken. Bei Namen ist die Groß- und Kleinschreibung relevant; geschweifte Klammern begrenzen Blöcke.",
    "HTML & CSS": "HTML beschreibt die Struktur einer Seite mit Elementen und Attributen. CSS wählt diese Elemente über Selektoren aus und verändert ihr Aussehen mit Eigenschaften und Werten.",
    "SQL": "SQL beschreibt, welche Daten aus Tabellen gelesen oder verändert werden. Tabellen- und Spaltennamen müssen stimmen; die Reihenfolge der Klauseln bestimmt, wie gefiltert, sortiert oder gruppiert wird.",
    "Git": "Git verwaltet Änderungen in mehreren Schritten: Arbeitsverzeichnis, Staging-Bereich, Commit und Remote. Wähle den Befehl passend zum gewünschten Schritt und prüfe, auf welchem Branch du arbeitest.",
    "Linux & Bash": "Shell-Befehle bestehen aus einem Kommando sowie optionalen Argumenten und Optionen. Sie wirken im aktuellen Verzeichnis; Anführungszeichen schützen Leerzeichen und Sonderzeichen.",
    "API Development": "Eine HTTP-API verbindet einen Pfad und eine Methode mit einer Funktion. Die Antwort enthält einen Statuscode und oft JSON; der Status sollte zur Art des Ergebnisses passen.",
    "API Consumption": "Bei einer HTTP-Anfrage bestimmen Methode, URL, Header und gegebenenfalls der Body, was gesendet wird. Prüfe den Statuscode und behandle Zeitüberschreitungen, bevor du Antwortdaten weiterverwendest.",
    "Machine Learning": "Ein typischer ML-Ablauf trennt Eingabemerkmale und Zielwerte, trainiert ein Modell und prüft es auf zuvor zurückgehaltenen Daten. Testdaten dürfen nicht in das Training einfließen.",
    "Statistics": "Statistische Kennzahlen fassen Beobachtungen zusammen, beantworten aber unterschiedliche Fragen. Achte auf Ausreißer, Einheiten und die passende Interpretation; eine Korrelation beweist keine Ursache.",
    "Data Visualization": "Ein Diagramm übersetzt Daten in visuelle Formen. Wähle den Diagrammtyp passend zum Vergleich, Verlauf oder zur Verteilung und beschrifte Achsen so, dass Werte eindeutig lesbar sind.",
    "Excel / Google Sheets": "Tabellenformeln beginnen mit einem Gleichheitszeichen und können einzelne Zellen, Bereiche oder Funktionen kombinieren. Kontrolliere Zellbereiche und Bedingungen, damit die Formel genau die gewünschten Werte verarbeitet.",
    "ETL Pipelines": "ETL steht für Extrahieren, Transformieren und Laden. Prüfe Datentypen, fehlende Werte und Spaltennamen bei jedem Schritt, damit die bereinigten Daten anschließend konsistent weiterverwendet werden können.",
    "Deep Learning": "Ein neuronales Netz verarbeitet Tensoren durch mehrere Layer. Die Loss-Funktion misst den Vorhersagefehler; Gradienten und Optimizer nutzen diesen Fehler, um Modellparameter schrittweise anzupassen.",
    "Model Evaluation": "Evaluationsmetriken vergleichen Vorhersagen mit den bekannten Zielwerten. Accuracy, Precision und Recall beleuchten verschiedene Fehlerarten; wähle die Kennzahl passend zu Klassenverteilung und Anwendungsfall.",
    "CI/CD Pipelines": "Ein CI/CD-Workflow wird durch ein Ereignis gestartet und führt Jobs aus einzelnen Schritten aus. Actions richten die Umgebung ein; Run-Schritte führen Befehle wie Installation und Tests aus.",
    "Docker & Kubernetes": "Ein Docker-Image ist die Vorlage für einen Container; Docker-Befehle bauen und starten diese Umgebung. Kubernetes verwaltet anschließend Anwendungen und Pods anhand deklarierter Ressourcen.",
    "Cloud Deployment": "Beim Deployment müssen Anwendung, Netzwerk und Konfiguration zusammenpassen. Bind-Adresse und Port steuern die Erreichbarkeit; Zugangsdaten gehören in Umgebungsvariablen statt in den Quellcode.",
    "Big Data (Spark/Hadoop)": "Spark verarbeitet DataFrames verteilt über viele Datenpartitionen. Transformationen beschreiben Verarbeitungsschritte, während Aktionen Ergebnisse berechnen oder ausgeben.",
    "Cloud Databases": "Datenbankzugriffe bestehen aus Verbindung, Abfrage und gegebenenfalls einer Transaktion. Verwende Konfiguration aus der Umgebung, bestätige Änderungen bewusst und schließe nicht mehr benötigte Verbindungen.",
    "Figma / Adobe XD": "Komponenten sind wiederverwendbare Designbausteine. Änderungen an der Hauptkomponente können Instanzen aktualisieren; so bleiben wiederkehrende UI-Elemente konsistent.",
}

for skill_entry in SKILL_CATALOG:
    skill_name = skill_entry["skill"]
    lessons = _LESSONS_BY_SKILL.get(skill_name, skill_entry.get("lessons", []))
    context = _LESSON_CONTEXT.get(skill_name)

    if context:
        expanded_lessons = []
        for title, content, question, answer in lessons:
            content = content.rstrip()
            if content and content[-1] not in ".!?":
                content += "."
            expanded_lessons.append((title, f"{content} {context}", question, answer))
        skill_entry["lessons"] = expanded_lessons
    else:
        skill_entry["lessons"] = lessons

del _LESSONS_BY_SKILL
del _LESSON_CONTEXT