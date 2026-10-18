from main import app, db
from sqlalchemy import text

with app.app_context():
    # Ersetzen Sie 'accounts' durch den genauen Namen der Tabelle
    table_name = input("Welche Tabelle möchten Sie löschen? (z.B. 'accounts', 'users', 'profiles'): ")
    sure = input(f"Bitte bestätigen Sie die Löschung der Tabelle '{table_name}' (Y/n): ").lower()
    if sure != 'y': 
        print("Löschung abgebrochen.")
        exit()
    
    print(f"Lösche Tabelle '{table_name}' via SQL...")
    # 'IF EXISTS' verhindert Fehler, falls die Tabelle bereits gelöscht wurde
    db.session.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
    db.session.commit()
    
    print(f"Tabelle '{table_name}' wurde dauerhaft entfernt.")
