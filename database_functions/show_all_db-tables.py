from run import app, db

with app.app_context():
    db.metadata.reflect(bind=db.engine)
    print("Existierende Tabellen in der Datenbank:")
    print(db.metadata.tables.keys())
