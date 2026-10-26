from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.ai import (
    FluffelSkillsAIError,
    FluffelSkillsConfigurationError,
    analyze_evidence_with_ai,
)
from app.database import AIAnalysis, JobCatalog, Profiles, SkillCatalog, UserSkills, Users, db
from app.skill_engine import build_fluffelskills_profile

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"], endpoint="register")
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password") or ""

        if not username or not email or not password:
            return "Bitte f?lle alle Felder korrekt aus.", 400

        if len(username) > 100 or len(email) > 150 or len(password) < 8:
            return "Bitte pr?fe Benutzername, E-Mail und Passwort. Das Passwort muss mindestens 8 Zeichen lang sein.", 400

        existing_username = Users.query.filter_by(username=username).first()
        existing_email = Users.query.filter_by(email=email).first()

        if existing_username:
            return "Dieser Benutzername ist bereits vergeben!", 400

        if existing_email:
            return "Diese E-Mail ist bereits registriert! Bitte versuche dich anzumelden.", 400

        new_user = Users(
            username=username,
            email=email,
            pass_hash=generate_password_hash(password),
            role="user",
            verified=True,
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("auth.onboarding"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "POST":
        login_value = (request.form.get("login") or "").strip()
        password = request.form.get("password") or ""

        if not login_value or not password:
            return "Bitte gib Benutzername/E-Mail und Passwort ein.", 400

        user = Users.query.filter(
            (Users.username == login_value) | (Users.email == login_value)
        ).first()

        if not user or not check_password_hash(user.pass_hash, password):
            return "Login fehlgeschlagen", 400

        login_user(user)
        return redirect(url_for("dashboard.dashboard"))

    return render_template("auth/login.html")


@auth_bp.route("/onboarding", methods=["GET", "POST"], endpoint="onboarding")
@login_required
def onboarding():
    all_jobs = JobCatalog.query.all()
    all_skills = SkillCatalog.query.all()

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        b_day_str = request.form.get("birthdate")
        b_day = datetime.strptime(b_day_str, "%Y-%m-%d").date()
        goal_job = request.form.get("goal_job")
        country = request.form.get("country")
        city = request.form.get("city")
        diploma = request.form.get("diploma")
        grade = request.form.get("grade")
        job_experience = request.form.get("job_experience")
        skills = request.form.getlist("skills")
        time_to_learn = request.form.get("time_to_learn")
        visibility = request.form.get("visibility")

        if not job_experience:
            job_experience = "keine"

        db_job = JobCatalog.query.filter_by(titel=goal_job).first()
        if not db_job:
            return f"Der ausgew?hlte Beruf '{goal_job}' wurde nicht im System gefunden.", 400

        skills_liste = []
        for skill in db_job.skills:
            skills_liste.append({
                "skill": skill.name,
                "target_level": skill.target_level,
                "importance": skill.importance,
            })

        job_profile_dict = {
            "title": db_job.titel,
            "required_skills": skills_liste,
        }

        profile = Profiles.query.filter_by(user_id=current_user.id).first()
        if not profile:
            profile = Profiles(user_id=current_user.id)
            db.session.add(profile)

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

        db.session.add(current_user)

        try:
            db.session.commit()
        except Exception as exc:
            db.session.rollback()
            print(f"? DB-Fehler: {exc}")
            return "Fehler beim Speichern in der Datenbank", 500

        user_data = {
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
                personal_details=user_data["personal_details"],
                goals=user_data["goals"],
                desired_job=user_data["desired_job"],
                school_leaving_certificate=user_data["school_leaving_certificate"],
                studies=user_data["studies"],
                work_experience=user_data["work_experience"],
                existing_skills=user_data["existing_skills"],
                uploaded_documents=user_data["uploaded_documents"],
                github_data=user_data["github_data"],
                certificates=user_data["certificates"],
                skill_tests=user_data["skill_tests"],
                projects=user_data["projects"],
                employer_confirmations=user_data["employer_confirmations"],
                learning_progress=user_data["learning_progress"],
                challenge_results=user_data["challenge_results"],
                output_language="Deutsch",
            )
        except FluffelSkillsConfigurationError as exc:
            print("? Konfigurationsfehler:")
            print(exc)
            return "Unerwarteter Fehler", 500
        except FluffelSkillsAIError as exc:
            print("? AI-Fehler:")
            print(exc)
            return "Unerwarteter Fehler", 500
        except Exception as exc:
            print("? Unerwarteter Fehler:")
            print(type(exc).__name__)
            print(exc)
            return "Unerwarteter Fehler", 500

        final_profile = build_fluffelskills_profile(
            ai_analysis=ai_result,
            raw_data=user_data,
            job_profile=job_profile_dict,
        )

        ai_entry = AIAnalysis.query.filter_by(user_id=current_user.id).first()
        if not ai_entry:
            ai_entry = AIAnalysis(user_id=current_user.id)
            db.session.add(ai_entry)

        try:
            job_match_score = final_profile.get("job_match", 0)
            skills_found = len(final_profile.get("skill_profile", {}).get("skills", []))
            missing_skills_found = len(final_profile.get("missing_skills", []))

            ai_entry.job_match = job_match_score
            ai_entry.skills_count = skills_found
            ai_entry.missing_skills_count = missing_skills_found
            ai_entry.raw_analysis_data = final_profile

            UserSkills.query.filter_by(profile_id=profile.id).delete()
            skills_list = final_profile.get("skill_profile", {}).get("skills", [])

            for skill_data in skills_list:
                skill_name = skill_data.get("name")
                skill_level = skill_data.get("level")
                confidence = skill_data.get("confidence")
                skill = SkillCatalog.query.filter_by(skill_name=skill_name).first()
                skill_id = skill.id if skill else None

                new_skill = UserSkills(
                    profile_id=profile.id,
                    skill_catalog_id=skill_id,
                    points=skill_level,
                    confidence=confidence,
                )
                db.session.add(new_skill)

            db.session.commit()
        except Exception as exc:
            db.session.rollback()
            print(f"? DB-Fehler beim Speichern des finalen Profils: {exc}")
            return "Fehler beim Speichern der Profildaten", 500

        current_user.onboarded = True
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for("dashboard.dashboard"))

    return render_template("auth/onboarding.html", jobs=all_jobs, skills=all_skills)


@auth_bp.route("/logout", endpoint="logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
