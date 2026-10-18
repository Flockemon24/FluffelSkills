from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from job_catalog import JOB_PROFILES
from skill_catalog import SKILL_CATALOG

# Zentrales SQLAlchemy-Objekt initialisieren
db = SQLAlchemy()

# ==========================================
# MODELLE (DATENBANK-STRUKTUR)
# ==========================================

class ApiTokens(db.Model):
    __tablename__ = 'api_tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    rate_limit = db.Column(db.Integer, nullable=False, default=-1)      
    window_seconds = db.Column(db.Integer, nullable=False, default=60)  


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user") 
    onboarded = db.Column(db.Boolean, default=False)
    plan = db.Column(db.String(50), default="free") # free, pro oder future
    
    # KORREKTUR: Zeitzonenbewusstes Default-Datum ohne () übergeben!
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    verified = db.Column(db.Boolean, default=False)

    # OPTIMIERUNG: 1:1 Beziehung zum Profil (uselist=False macht es zu einer One-to-One Beziehung)
    profile = db.relationship('Profiles', backref='user', uselist=False, cascade="all, delete-orphan")
    tokens = db.relationship('ApiTokens', backref='user', lazy=True)


class Profiles(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True) # unique=True für echte 1:1 Beziehung
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.LargeBinary, nullable=True)
    birthdate = db.Column(db.Date, nullable=False)
    goal_job = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    diploma = db.Column(db.String(100), nullable=True)
    grade = db.Column(db.Float, nullable=False)
    job_experience = db.Column(db.Text, nullable=True)
    skills = db.relationship('UserSkills', backref='profile', lazy=True, cascade="all, delete-orphan")
    time_to_learn = db.Column(db.String(50), nullable=True)
    visibility = db.Column(db.String(20), default="private")
    

class UserSkills(db.Model):
    __tablename__ = 'user_skills'

    id = db.Column(db.Integer, primary_key=True)

    profile_id = db.Column(
        db.Integer,
        db.ForeignKey('profiles.id'),
        nullable=False
    )
    skill_catalog_id = db.Column(
        db.Integer,
        db.ForeignKey('skill_catalog.id'),
        nullable=False
    )
    # Aktueller Skill-Level
    points = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    # Wie sicher ist FluffelSkills bei diesem Wert?
    confidence = db.Column(
        db.Float,
        nullable=False,
        default=0
    )
    last_activity = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    skill_catalog = db.relationship(
        'SkillCatalog',
        backref='user_skills'
    )
    _table_args__ = (
        db.UniqueConstraint(
            'profile_id',
            'skill_catalog_id',
            name='unique_user_skill'
        ),
    )


# Zwischentabelle für den Lernfortschritt der User
class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    lesson_id = db.Column(
        db.Integer,
        db.ForeignKey('lessons.id'),
        nullable=False
    )

    attempts = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    completed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    __table_args__ = (
        db.UniqueConstraint(
            'user_id',
            'lesson_id',
            name='unique_user_lesson'
        ),
    )


class AIAnalysis(db.Model):
    __tablename__ = 'ai_analyses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # --- Schnellzugriff-Spalten (Übersicht) ---
    job_match = db.Column(db.Integer, nullable=False, default=0)
    skills_count = db.Column(db.Integer, nullable=False, default=0)
    missing_skills_count = db.Column(db.Integer, nullable=False, default=0)
    
    # --- Das komplette JSON als Backup & für Details ---
    raw_analysis_data = db.Column(db.JSON, nullable=False) 
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Beziehung zum User
    user = db.relationship('Users', backref=db.backref('ai_analysis', uselist=False))



class JobCatalog(db.Model):
    __tablename__ = 'jobs_catalog'
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(100), nullable=False, unique=True)
    
    skills = db.relationship('JobSkillCatalog', backref='job', lazy=True, cascade="all, delete-orphan")


class JobSkillCatalog(db.Model):
    __tablename__ = 'job_skills_catalog'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs_catalog.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    target_level = db.Column(db.Integer, nullable=False) 
    importance = db.Column(db.Integer, nullable=False)


class SkillCatalog(db.Model):
    __tablename__ = 'skill_catalog'
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), unique=True, nullable=False)
    categorie = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # BEZIEHUNG ZU DEN LEKTIONEN:
    lessons = db.relationship('Lesson', backref='skill_catalog', lazy=True, cascade="all, delete-orphan")


class EarlyBirdWarteliste(db.Model):
    __tablename__ = 'early_bird_warteliste'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    plan_name = db.Column(db.String(50), nullable=False, default="PRO")
    eingetragen_am = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    
    # JETZT KORREKT: Gekoppelt an den allgemeinen SkillCatalog
    skill_catalog_id = db.Column(db.Integer, db.ForeignKey('skill_catalog.id'), nullable=False)
    
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)         # Der Lerntext
    question = db.Column(db.Text, nullable=False)        # Die Testfrage
    correct_answer = db.Column(db.String(100), nullable=False) # Die richtige Antwort
    order_index = db.Column(db.Integer, nullable=False)  # Reihenfolge (1, 2, 3...)
    difficulty = db.Column(db.Integer, nullable=False, default=1)


class SkillEvidence(db.Model):
    __tablename__ = 'skill_evidence'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey('skill_catalog.id'),
        nullable=False
    )

    source_type = db.Column(
        db.String(50),
        nullable=False
    )

    source_id = db.Column(
        db.Integer,
        nullable=True
    )

    points_gained = db.Column(
        db.Float,
        default=0
    )

    confidence_gained = db.Column(
        db.Float,
        default=0
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )



def set_job_catalog():
    # Datenbank befüllen, wenn sie noch leer ist
    if not JobCatalog.query.first():
        for job_key, job_data in JOB_PROFILES.items():
            # 1. Haupt-Job erstellen
            neuer_job = JobCatalog(titel=job_data["title"])
            db.session.add(neuer_job)
            db.session.flush() # Holt die ID des neuen Jobs, ohne die Transaktion zu beenden
            
            # 2. Die verschachtelten Skills für diesen Job erstellen
            for skill_data in job_data["required_skills"]:
                neuer_skill = JobSkillCatalog(
                    job_id=neuer_job.id,
                    name=skill_data["skill"],
                    target_level=skill_data["target_level"],
                    importance=skill_data["importance"]
                )
                db.session.add(neuer_skill)
       
        db.session.commit()
        print("Job-Profile erfolgreich in die SQLite-Datenbank importiert!")

def set_skill_catalog():
    # Datenbank befüllen, wenn sie noch leer ist
    if not SkillCatalog.query.first():
        for skill_data in SKILL_CATALOG:
            # 1. Skill anlegen
            new_skill = SkillCatalog(
                skill_name=skill_data["skill"],
                categorie=skill_data["category"]
                # description lassen wir leer/bzw. wird None, da in deiner Liste nicht enthalten
            )
            db.session.add(new_skill)
            db.session.flush()  # Generiert die ID für 'neuer_skill', beendet aber die Transaktion noch nicht
            
            # 2. Prüfen, ob Lektionen für diesen Skill im Array definiert sind
            if "lessons" in skill_data:
                for index, (title, content, question, answer) in enumerate(skill_data["lessons"], start=1):
                    new_lesson = Lesson(
                        skill_catalog_id=new_skill.id, # Verknüpfung über die eben generierte ID
                        title=title,
                        content=content,
                        question=question,
                        correct_answer=answer,
                        order_index=index
                    )
                    db.session.add(new_lesson)
            
        db.session.commit()
        print("Skill-Katalog und Beispieldaten erfolgreich in die SQLite-Datenbank importiert!")

# ==========================================
# HILFSFUNKTIONEN FÜR DIE API
# ==========================================

def get_token_info(token_string):
    # Modernes SQLAlchemy 3.x/2.x Abfrage-Format (Zukunftssicher)
    token_entry = db.session.execute(
        db.select(ApiTokens).filter_by(token=token_string)
    ).scalar_one_or_none()
    
    if token_entry:
        return token_entry.rate_limit, token_entry.window_seconds
    return None


def insert_new_token(token_string, rate_limit, window_seconds):
    try:
        new_token = ApiTokens(
            token=token_string, 
            rate_limit=rate_limit, 
            window_seconds=window_seconds
        )
        db.session.add(new_token)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


def seed_demo_tokens():
    demo_tokens = [
        ("token_premium", -1, 60),
        ("token_standard", 5, 60),
        ("token_basic", 2, 60)
    ]
    
    for token, limit, window in demo_tokens:
        # Auch hier zukunftssicheres select() verwendet
        exists = db.session.execute(
            db.select(ApiTokens).filter_by(token=token)
        ).scalar_one_or_none()
        
        if not exists:
            db.session.add(ApiTokens(token=token, rate_limit=limit, window_seconds=window))
            
    db.session.commit()
