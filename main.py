from flask import Flask, abort, render_template, jsonify, flash, request, redirect, url_for, make_response, send_file # pyright: ignore[reportMissingImports]
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import joinedload
from datetime import datetime
import requests
import json
from time import sleep
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash # pyright: ignore[reportMissingImports]
import os
from io import BytesIO
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from functools import wraps

from database import ApiTokens, Users, Profiles, UserSkills, UserProgress, JobCatalog, JobSkillCatalog, SkillCatalog, AIAnalysis, EarlyBirdWarteliste, Lesson, db, set_job_catalog, set_skill_catalog
from api import api_bp

from ai import (
    analyze_evidence_with_ai,
    FluffelSkillsAIError,
    FluffelSkillsConfigurationError,
)

from skill_engine import build_fluffelskills_profile
from job_catalog import JOB_PROFILES

load_dotenv()

app = Flask(__name__)
MAX_PROFILE_PICTURE_BYTES = 2 * 1024 * 1024

app.secret_key = os.getenv("SECRET_KEY", "dev-key")


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['MAX_CONTENT_LENGTH'] = MAX_PROFILE_PICTURE_BYTES + 65536
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = True  # nur HTTPS

app.config['MAIL_SERVER'] = 'mail.gmx.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_ADDRESS')

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)


db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # wohin bei nicht eingeloggt


# API-System einbinden
app.register_blueprint(api_bp)


@login_manager.user_loader
def load_user(user_id):
    # Löst gleichzeitig das Problem der Legacy-Warnung und lädt das Profil direkt mit
    return db.session.get(
        Users, 
        int(user_id), 
        options=[joinedload(Users.profile)]
    )

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            return "Zugriff verweigert", 403
        return f(*args, **kwargs)
    return wrapper

@app.route("/init-db")
def init_db():
    with app.app_context():
        db.create_all()
        set_job_catalog()
        set_skill_catalog()
    return "DB erstellt!"

@app.route("/", methods=['GET', 'POST'])
def home_page():
    return render_template('homepage.html')

@app.route("/pricing")
def pricing():
    return render_template('pricing.html')

@app.route('/api/join-waitlist', methods=['POST'])
@login_required  # Schützt die Route; nur eingeloggte User dürfen darauf zugreifen
def warteliste_beitreten():
    # JSON-Daten aus dem JavaScript-Fetch abfangen
    data = request.get_json() or {}
    plan_name = data.get('plan_name', 'PRO')
    
    try:
        # Prüfen, ob der User bereits auf der Liste steht
        exists = db.session.execute(
            db.select(EarlyBirdWarteliste).filter_by(user_id=current_user.id)
        ).scalar_one_or_none()
        
        if exists:
            return jsonify({
                'status': 'success',
                'message': 'Bereits auf der Liste registriert.',
                'free_months': 1,
            }), 200
        
        # Neuen Eintrag erstellen
        neuer_eintrag = EarlyBirdWarteliste(
            user_id=current_user.id,
            plan_name=plan_name
        )
        
        db.session.add(neuer_eintrag)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Erfolgreich für {plan_name} eingetragen!',
            'free_months': 1,
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Fehler beim Eintragen in die Warteliste: {e}")
        return jsonify({'status': 'error', 'message': 'Datenbankfehler beim Eintragen.'}), 500

@app.route("/terms")
def terms():
    return "Nutzungsbedingungen"

@app.route("/privacy-policy")
def privacy_policy():
    return "Datenschutzerklärung"

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # 🔍 Datenbank check
        existing_username = Users.query.filter_by(username=username).first()
        existing_email = Users.query.filter_by(email=email).first()

        if existing_username:
            return "Dieser Benutzername ist bereits vergeben!", 400
        
        if existing_email:
            return "Diese E-Mail ist bereits registriert! Bitte versuche dich anzumelden.", 400

        # 👤 neuen User erstellen
        new_user = Users(
            username=username,
            email=email,
            pass_hash=generate_password_hash(password),
            role="user",  # Standardrolle auf "user" setzen
            verified=True,
        )
        

        db.session.add(new_user)
        db.session.commit()

        # E-Mail-Verifizierung senden
        #token = serializer.dumps(email, salt='email-confirm')
        #confirm_url = url_for('confirm_email', token=token, _external=True)
        #msg = Message('Bitte bestätige deine E-Mail-Adresse', recipients=[email])

        #msg.body = f'Bitte klicke auf den folgenden Link, um deine E-Mail-Adresse zu bestätigen: {confirm_url}'
        #mail.send(msg)

        # 🔐 Login direkt nach Registrierung
        login_user(new_user)

        return redirect(url_for('onboarding'))

    return render_template('register.html')

'''@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)  # 1 Stunde gültig
    except Exception as e:
        return "Der Bestätigungslink ist ungültig oder abgelaufen.", 400

    # Modernes SQLAlchemy-Format passend zu deiner database.py
    user = db.session.execute(
        db.select(Users).filter_by(email=email)
    ).scalar_one_or_none()

    if user:
        if not user.verified:
            user.verified = True
            db.session.commit()
        
        # Der magische Trick: Den User direkt einloggen!
        login_user(user)
        
        # Optional: Eine kurze Erfolgsmeldung für das Dashboard bereitstellen
        flash("E-Mail-Adresse erfolgreich bestätigt! Willkommen an Bord.", "success")
        
        # Weiterleitung zum Dashboard, wo dein funktionierendes JavaScript wartet
        return redirect(url_for('dashboard'))
    else:
        return "Benutzer nicht gefunden.", 404'''

@app.route("/onboarding", methods=['GET', 'POST'])
@login_required
def onboarding():
    all_jobs = JobCatalog.query.all()
    all_skills = SkillCatalog.query.all()

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        b_day_str = request.form.get('birthdate')
        b_day = datetime.strptime(b_day_str, "%Y-%m-%d").date()
        goal_job = request.form.get('goal_job')
        country = request.form.get('country')
        city = request.form.get('city')
        diploma = request.form.get('diploma')
        grade = request.form.get('grade')
        job_experience = request.form.get('job_experience')
        skills = request.form.getlist('skills')
        time_to_learn = request.form.get('time_to_learn')
        visibility = request.form.get('visibility')

        if not job_experience:
            job_experience = "keine"

        # ==========================================
        # 1. JOB-PROFIL AUS DER DATENBANK LADEN
        # ==========================================
        db_job = JobCatalog.query.filter_by(titel=goal_job).first()
        
        if not db_job:
            # Sicherheits-Fallback falls der Job nicht in der DB existiert
            return f"Der ausgewählte Beruf '{goal_job}' wurde nicht im System gefunden.", 400

        # Die verknüpften Skills aus der Datenbank in ein Dictionary umwandeln
        skills_liste = []
        for s in db_job.skills:
            skills_liste.append({
                "skill": s.name,
                "target_level": s.target_level,
                "importance": s.importance
            })

        # Die finale Dictionary-Struktur für deine build_fluffelskills_profile Funktion
        job_profile_dict = {
            "title": db_job.titel,
            "required_skills": skills_liste
        }

        # ==========================================
        # 2. PROFIL ERSTELLEN ODER AKTUALISIEREN (Verhindert UNIQUE-Fehler)
        # ==========================================
        profile = Profiles.query.filter_by(user_id=current_user.id).first()
        if not profile:
            profile = Profiles(user_id=current_user.id)
            db.session.add(profile)

        # Daten zuweisen
        profile.first_name = first_name
        profile.last_name = last_name
        profile.birthdate = b_day
        profile.goal_job = goal_job
        profile.country = country
        profile.city = city
        profile.diploma = diploma
        profile.grade = float(grade) if grade else 0.0
        profile.job_experience = job_experience
        profile.time_to_learn = time_to_learn
        profile.visibility = visibility

        # Schritt A: Alte Skills des Benutzers löschen (wichtig bei Aktualisierungen)
        

        current_user.onboarded = True
        db.session.add(current_user)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"❌ DB-Fehler: {e}")
            return "Fehler beim Speichern in der Datenbank", 500

        # USER_DATA Dictionary befüllen
        USER_DATA = {
            "personal_details": {
                "first_name": first_name,
                "last_name": last_name,
                "birthdate": b_day_str,
                "country": country,
                "city": city,
            },
            "goals": [f"Become a(n) {goal_job}"],
            "desired_job": goal_job,
            "school_leaving_certificate": {
                "type": diploma,
                "grade": grade,
            },
            "studies": [],
            "work_experience": job_experience,
            "existing_skills": skills,
            "uploaded_documents": [],
            "github_data": [],
            "certificates": [],
            "skill_tests": [],
            "projects": [],
            "employer_confirmations": [],
            "learning_progress": [],
            "challenge_results": [],
        }

        try:

            ai_result = analyze_evidence_with_ai(
                personal_details=USER_DATA[
                    "personal_details"
                ],
                goals=USER_DATA[
                    "goals"
                ],
                desired_job=USER_DATA[
                    "desired_job"
                ],
                school_leaving_certificate=USER_DATA[
                    "school_leaving_certificate"
                ],
                studies=USER_DATA[
                    "studies"
                ],
                work_experience=USER_DATA[
                    "work_experience"
                ],
                existing_skills=USER_DATA[
                    "existing_skills"
                ],
                uploaded_documents=USER_DATA[
                    "uploaded_documents"
                ],
                github_data=USER_DATA[
                    "github_data"
                ],
                certificates=USER_DATA[
                    "certificates"
                ],
                skill_tests=USER_DATA[
                    "skill_tests"
                ],
                projects=USER_DATA[
                    "projects"
                ],
                employer_confirmations=USER_DATA[
                    "employer_confirmations"
                ],
                learning_progress=USER_DATA[
                    "learning_progress"
                ],
                challenge_results=USER_DATA[
                    "challenge_results"
                ],
                output_language="Deutsch",
            )

        except FluffelSkillsConfigurationError as exc:

            print("❌ Konfigurationsfehler:")
            print(exc)

            return "Unerwarteter Fehler", 500

        except FluffelSkillsAIError as exc:

            print("❌ AI-Fehler:")
            print(exc)

            return "Unerwarteter Fehler", 500

        except Exception as exc:

            print("❌ Unerwarteter Fehler:")
            print(type(exc).__name__)
            print(exc)

            return "Unerwarteter Fehler", 500
        
        print("✅ KI-Antwort erhalten.")

        # ==========================================
        # 3. DAS DEFINIERTE JOB-PROFIL ÜBERGEBEN
        # ==========================================
        final_profile = build_fluffelskills_profile(
            ai_analysis=ai_result,
            raw_data=USER_DATA,
            job_profile=job_profile_dict  # Übergabe des generierten Dictionaries
        )

        print(final_profile)

        print("✅ FluffelSkills-Profil wurde erfolgreich gebaut.")

        # ==========================================
        # 4. ERST JETZT: KI-ERGEBNISSE IN DER DB SPEICHERN
        # ==========================================
        # Falls build_fluffelskills_profile das Format ändert, nutzen wir hier 'final_profile'
        # Falls es nur ein Zwischenschritt war und das JSON in 'ai_result' steht, ändere es zurück zu 'ai_result'
        target_profile_data = final_profile 

        ai_entry = AIAnalysis.query.filter_by(user_id=current_user.id).first()
        if not ai_entry:
            ai_entry = AIAnalysis(user_id=current_user.id)
            db.session.add(ai_entry)

        try:
            # Schnelle Metriken aus der finalen Struktur ziehen
            job_match_score = target_profile_data.get('job_match', 0)
            skills_found = len(target_profile_data.get('skill_profile', {}).get('skills', []))
            missing_skills_found = len(target_profile_data.get('missing_skills', []))
            
            # Werte zuweisen
            ai_entry.job_match = job_match_score
            ai_entry.skills_count = skills_found
            ai_entry.missing_skills_count = missing_skills_found
            ai_entry.raw_analysis_data = target_profile_data  # Das komplette, fertige JSON

            UserSkills.query.filter_by(profile_id=profile.id).delete()
            skills_list = target_profile_data.get('skill_profile', {}).get('skills', [])
            
            for skill_data in skills_list:
                skill_name = skill_data.get('name')
                skill_level = skill_data.get('level')
                confidence = skill_data.get('confidence')
                skill = SkillCatalog.query.filter_by(skill_name=skill_name).first()
                if skill:
                    skill_id = skill.id
                else:
                    skill_id = None

                new_skill = UserSkills(
                    profile_id=profile.id,
                    skill_catalog_id=skill_id,
                    points=skill_level,
                    confidence=confidence
                )

                db.session.add(new_skill)
            
            db.session.commit()
            print("✅ Finales Profil erfolgreich in der Datenbank gespeichert.")

            
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ DB-Fehler beim Speichern des finalen Profils: {e}")
            # Optional: Hier entscheiden, ob trotzdem weitergeleitet wird oder ein Fehler kommt
            return "Fehler beim Speichern der Profildaten", 500
        
        return redirect(url_for('dashboard'))

    return render_template('onboarding.html', jobs=all_jobs, skills=all_skills)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        login_value = request.form.get("login")
        password = request.form.get("password")

        user = Users.query.filter(
            (Users.username == login_value) | (Users.email == login_value)
        ).first()

        if not user or not check_password_hash(user.pass_hash, password):
            return "Login fehlgeschlagen", 400

        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.onboarded:
        return redirect(url_for('onboarding'))
    if not current_user.verified:
        return "Bitte bestätige deine E-Mail-Adresse, um fortzufahren.", 403
    return render_template(
        'index.html', 
        name=current_user.username, 
        goal_job=current_user.profile.goal_job,
    )

@app.route("/roadmap")
@login_required
def roadmap():
    user_id = current_user.id 
    all_skills = SkillCatalog.query.all()

    # Abfragen, welche Lektionen der User schon geschafft hat
    completed_lessons = [p.lesson_id for p in UserProgress.query.filter_by(user_id=user_id).all()]
    
    return render_template('roadmaps.html', skills=all_skills, completed=completed_lessons)

@app.route("/profile")
@login_required
def profile():
    profile_data = current_user.profile
    if profile_data is None:
        return redirect(url_for('onboarding'))

    showcase = []
    analysis = AIAnalysis.query.filter_by(user_id=current_user.id).first()
    if analysis and isinstance(analysis.raw_analysis_data, dict):
        saved_showcase = analysis.raw_analysis_data.get('public_showcase', [])
        if isinstance(saved_showcase, list):
            showcase = [item for item in saved_showcase if isinstance(item, str)]

    selected_skills = []
    for item in profile_data.skills:
        skill = SkillCatalog.query.filter_by(id=item.skill_catalog_id).first()
        selected_skills.append(skill.skill_name)

    return render_template(
        'profile.html',
        profile=profile_data,
        account=current_user,
        skill_catalog=SkillCatalog.query.order_by(SkillCatalog.categorie, SkillCatalog.skill_name).all(),
        selected_skills=selected_skills,
        showcase_text='\n'.join(showcase),
        profile_url=url_for('public_profile', username=current_user.username, _external=True),
    )


def _profile_picture_mimetype(image_data):
    if image_data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    if image_data.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'
    if image_data[:6] in (b'GIF87a', b'GIF89a'):
        return 'image/gif'
    if len(image_data) >= 12 and image_data[:4] == b'RIFF' and image_data[8:12] == b'WEBP':
        return 'image/webp'
    return None


def _profile_is_visible(user):
    if user.profile is None:
        return False
    return user.profile.visibility == 'public' or (
        current_user.is_authenticated and current_user.get_id() == str(user.id)
    )


def _public_profile_data(user):
    profile_data = user.profile
    analysis = AIAnalysis.query.filter_by(user_id=user.id).first()
    raw_data = analysis.raw_analysis_data if analysis and isinstance(analysis.raw_analysis_data, dict) else {}
    skill_profile = raw_data.get('skill_profile', {})
    analyzed_skills = skill_profile.get('skills', []) if isinstance(skill_profile, dict) else []
    levels = {
        item.get('name'): item.get('level', 0)
        for item in analyzed_skills
        if isinstance(item, dict) and isinstance(item.get('name'), str)
    }
    selected_names = sorted({item.skill for item in profile_data.skills}, key=str.casefold)
    skill_catalog = SkillCatalog.query.filter(SkillCatalog.skill_name.in_(selected_names)).all() if selected_names else []
    catalog_by_name = {item.skill_name: item for item in skill_catalog}
    completed_ids = {
        item.lesson_id
        for item in UserProgress.query.filter_by(user_id=user.id).all()
    }

    skills = []
    for skill_name in selected_names:
        catalog_item = catalog_by_name.get(skill_name)
        lessons = catalog_item.lessons if catalog_item else []
        completed = sum(lesson.id in completed_ids for lesson in lessons)
        level = levels.get(skill_name, 0)
        level = max(0, min(100, int(round(level)))) if isinstance(level, (int, float)) else 0
        skills.append({
            'name': skill_name,
            'category': catalog_item.categorie if catalog_item else 'Skill',
            'level': level,
            'completed_lessons': completed,
            'total_lessons': len(lessons),
            'lesson_progress': round(completed * 100 / len(lessons)) if lessons else 0,
        })

    selected_names_set = set(selected_names)
    graph_edges = []
    graph_data = raw_data.get('skill_graph', {})
    if isinstance(graph_data, dict):
        for edge in graph_data.get('edges', []):
            if not isinstance(edge, dict):
                continue
            from_skill = edge.get('from_skill')
            to_skill = edge.get('to_skill')
            if from_skill in selected_names_set and to_skill in selected_names_set:
                graph_edges.append({'from_skill': from_skill, 'to_skill': to_skill})

    showcase = raw_data.get('public_showcase', [])
    if not isinstance(showcase, list):
        showcase = []
    showcase = [item for item in showcase if isinstance(item, str)]

    return {
        'user': user,
        'profile': profile_data,
        'skills': skills,
        'skill_points': sum(skill['level'] for skill in skills),
        'completed_lesson_count': sum(skill['completed_lessons'] for skill in skills),
        'showcase': showcase,
        'graph': {
            'nodes': [
                {'skill': skill['name'], 'category': skill['category'], 'level': skill['level']}
                for skill in skills
            ],
            'edges': graph_edges,
        },
        'avatar_url': url_for('profile_avatar', username=user.username),
    }


@app.route('/u/<username>')
def public_profile(username):
    user = Users.query.filter_by(username=username).first_or_404()
    if not _profile_is_visible(user):
        abort(404)
    return render_template('public_profile.html', **_public_profile_data(user))


@app.route('/u/<username>/avatar')
def profile_avatar(username):
    user = Users.query.filter_by(username=username).first_or_404()
    if not _profile_is_visible(user) or not user.profile.profile_pic:
        abort(404)
    image_data = user.profile.profile_pic
    mimetype = _profile_picture_mimetype(image_data)
    if not mimetype:
        abort(404)
    response = send_file(BytesIO(image_data), mimetype=mimetype, max_age=0)
    response.cache_control.private = True
    response.cache_control.no_store = True
    return response


@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    account = current_user._get_current_object()
    profile_data = account.profile
    if profile_data is None:
        return redirect(url_for('onboarding'))

    username = request.form.get('username', '').strip()
    if not username or len(username) > 100:
        flash('Bitte gib einen gültigen Benutzernamen ein.', 'error')
        return redirect(url_for('profile'))
    username_taken = Users.query.filter_by(username=username).first()
    if username_taken and username_taken.id != account.id:
        flash('Dieser Benutzername ist bereits vergeben.', 'error')
        return redirect(url_for('profile'))

    showcase = [line.strip() for line in request.form.get('showcase', '').splitlines() if line.strip()]
    if len(showcase) > 12 or any(len(item) > 200 for item in showcase):
        flash('Nutze höchstens 12 Projekte oder Nachweise mit maximal 200 Zeichen pro Eintrag.', 'error')
        return redirect(url_for('profile'))

    uploaded_picture = request.files.get('profile_pic')
    picture_data = None
    if uploaded_picture and uploaded_picture.filename:
        picture_data = uploaded_picture.stream.read(MAX_PROFILE_PICTURE_BYTES + 1)
        if len(picture_data) > MAX_PROFILE_PICTURE_BYTES:
            flash('Das Profilbild darf höchstens 2 MB groß sein.', 'error')
            return redirect(url_for('profile'))
        if not _profile_picture_mimetype(picture_data):
            flash('Bitte lade ein PNG-, JPEG-, GIF- oder WebP-Bild hoch.', 'error')
            return redirect(url_for('profile'))

    account.username = username
    profile_data.first_name = request.form.get('first_name', '').strip()[:100] or profile_data.first_name
    profile_data.last_name = request.form.get('last_name', '').strip()[:100] or profile_data.last_name
    profile_data.goal_job = request.form.get('goal_job', '').strip()[:100] or profile_data.goal_job
    profile_data.job_experience = request.form.get('bio', '').strip()[:3000] or None
    profile_data.time_to_learn = request.form.get('time_to_learn', '').strip()[:50] or None
    visibility = request.form.get('visibility')
    if visibility in {'private', 'public'}:
        profile_data.visibility = visibility

    if request.form.get('remove_profile_pic') == 'on':
        profile_data.profile_pic = None
    elif picture_data is not None:
        profile_data.profile_pic = picture_data

    valid_skills = {item.skill_name for item in SkillCatalog.query.all()}
    selected_skills = list(dict.fromkeys(
        skill for skill in request.form.getlist('skills') if skill in valid_skills
    ))
    selected_skills_names = []
    
    for skill_name in selected_skills:
        skill = SkillCatalog.query.filter_by(skill_name=skill_name).first()
        selected_skills_names.append(skill.id)

    profile_data.skills = [UserSkills(skill_catalog_id=skill) for skill in selected_skills_names]

    analysis = AIAnalysis.query.filter_by(user_id=account.id).first()
    if not analysis:
        analysis = AIAnalysis(user_id=account.id, raw_analysis_data={})
        db.session.add(analysis)
    raw_data = dict(analysis.raw_analysis_data) if isinstance(analysis.raw_analysis_data, dict) else {}
    raw_data['public_showcase'] = showcase
    analysis.raw_analysis_data = raw_data

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Deine Änderungen konnten nicht gespeichert werden.', 'error')
        return redirect(url_for('profile'))

    flash('Dein Profil wurde gespeichert.', 'success')
    return redirect(url_for('profile'))


@app.route('/profile/delete', methods=['POST'])
@login_required
def delete_account():
    account = current_user._get_current_object()
    if not check_password_hash(account.pass_hash, request.form.get('password', '')):
        flash('Das Passwort ist falsch. Dein Konto wurde nicht gelöscht.', 'error')
        return redirect(url_for('profile'))
    if request.form.get('confirm_delete') != 'yes':
        abort(400)

    user_id = account.id
    profile_id = current_user.profile.id
    UserProgress.query.filter_by(user_id=user_id).delete(synchronize_session=False)
    ApiTokens.query.filter_by(user_id=user_id).delete(synchronize_session=False)
    AIAnalysis.query.filter_by(user_id=user_id).delete(synchronize_session=False)
    EarlyBirdWarteliste.query.filter_by(user_id=user_id).delete(synchronize_session=False)
    Profiles.query.filter_by(user_id=user_id).delete(synchronize_session=False)
    UserSkills.query.filter_by(profile_id=profile_id).delete(synchronize_session=False)
    Users.query.filter_by(id=user_id).delete(synchronize_session=False)
    if account.profile:
        db.session.delete(account.profile)
    db.session.delete(account)
    db.session.commit()
    logout_user()
    flash('Dein Konto wurde gelöscht.', 'success')
    return redirect(url_for('home_page'))

@app.route('/lesson/<int:lesson_id>')
@login_required
def view_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    answer = lesson.correct_answer.lower()
    print(answer)
    return render_template('lesson.html', lesson=lesson, id=lesson_id, answer=answer)

@app.route('/lesson/<int:lesson_id>/submit')
@login_required
def submit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    user_id = current_user.id
    
    already_done = UserProgress.query.filter_by(user_id=user_id, lesson_id=lesson.id).first()
    if not already_done:
        progress = UserProgress(user_id=user_id, lesson_id=lesson.id)
        db.session.add(progress)
        db.session.commit()
    print("Correct answer")
    return redirect(url_for('roadmap'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

'''@app.route("/clear", methods=['POST']) # Nur POST erlauben
@login_required
@admin_required
def clear_accounts():
    try:
        db.session.query(Users).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Fehler: {e}")
    
    # Leitet den Nutzer nach dem Löschen sofort zurück zur Startseite
    return redirect(url_for('dashboard', name='user'))'''

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)