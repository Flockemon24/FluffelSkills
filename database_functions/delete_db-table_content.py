from run import app, db, Users, Profiles

db_to_delete = input("Welche Datenbank möchten Sie löschen?\n(1) Users\n(2) Profiles\nBitte geben Sie die Zahl ein: ")
sure = input(f"Bitte bestätigen Sie die Löschung der Datenbank '{db_to_delete}' (Y/n): ").lower()
if sure != 'y':
    print("Löschung abgebrochen.")
    exit()

with app.app_context():
    if db_to_delete == "1" and sure == 'y':
        print("Lösche Users-Datenbank...")
        db.session.query(Users).delete()
        print("Users-Datenbank erfolgreich gelöscht.")
    elif db_to_delete == "2" and sure == 'y':
        print("Lösche Profiles-Datenbank...")
        db.session.query(Profiles).delete()
        print("Profiles-Datenbank erfolgreich gelöscht.")

    db.session.commit()