from io import BytesIO

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required, logout_user
from werkzeug.security import check_password_hash

from app.database import (
    AIAnalysis,
    ApiTokens,
    EarlyBirdWarteliste,
    Lesson,
    Profiles,
    SkillCatalog,
    UserProgress,
    UserSkills,
    Users,
    db,
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET", "POST"], endpoint="dashboard")
@login_required
def dashboard():
    if not current_user.onboarded:
        return redirect(url_for("auth.onboarding"))
    if not current_user.verified:
        return "Bitte best?tige deine E-Mail-Adresse, um fortzufahren.", 403
    return render_template("dashboard/dashboard.html", name=current_user.username, goal_job=current_user.profile.goal_job)


@dashboard_bp.route("/roadmap", endpoint="roadmap")
@login_required
def roadmap():
    user_id = current_user.id
    all_skills = SkillCatalog.query.all()
    completed_lessons = [p.lesson_id for p in UserProgress.query.filter_by(user_id=user_id).all()]
    return render_template("dashboard/roadmaps.html", skills=all_skills, completed=completed_lessons)


@dashboard_bp.route("/profile", endpoint="profile")
@login_required
def profile():
    profile_data = current_user.profile
    if profile_data is None:
        return redirect(url_for("auth.onboarding"))

    showcase = []
    analysis = AIAnalysis.query.filter_by(user_id=current_user.id).first()
    if analysis and isinstance(analysis.raw_analysis_data, dict):
        saved_showcase = analysis.raw_analysis_data.get("public_showcase", [])
        if isinstance(saved_showcase, list):
            showcase = [item for item in saved_showcase if isinstance(item, str)]

    selected_skills = []
    for item in profile_data.skills:
        skill = SkillCatalog.query.filter_by(id=item.skill_catalog_id).first()
        selected_skills.append(skill.skill_name)

    return render_template(
        "dashboard/profile.html",
        profile=profile_data,
        account=current_user,
        skill_catalog=SkillCatalog.query.order_by(SkillCatalog.categorie, SkillCatalog.skill_name).all(),
        selected_skills=selected_skills,
        showcase_text="\n".join(showcase),
        profile_url=url_for("dashboard.public_profile", username=current_user.username, _external=True),
    )


def _profile_picture_mimetype(image_data):
    if image_data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if image_data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if image_data[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if len(image_data) >= 12 and image_data[:4] == b"RIFF" and image_data[8:12] == b"WEBP":
        return "image/webp"
    return None


def _profile_is_visible(user):
    if user.profile is None:
        return False
    return user.profile.visibility == "public" or (
        current_user.is_authenticated and current_user.get_id() == str(user.id)
    )


def _public_profile_data(user):
    profile_data = user.profile
    analysis = AIAnalysis.query.filter_by(user_id=user.id).first()
    raw_data = analysis.raw_analysis_data if analysis and isinstance(analysis.raw_analysis_data, dict) else {}
    skill_profile = raw_data.get("skill_profile", {})
    analyzed_skills = skill_profile.get("skills", []) if isinstance(skill_profile, dict) else []
    levels = {
        item.get("name"): item.get("level", 0)
        for item in analyzed_skills
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    selected_names = sorted({item.skill_catalog.skill_name for item in profile_data.skills}, key=str.casefold)
    skill_catalog = SkillCatalog.query.filter(SkillCatalog.skill_name.in_(selected_names)).all() if selected_names else []
    catalog_by_name = {item.skill_name: item for item in skill_catalog}
    completed_ids = {item.lesson_id for item in UserProgress.query.filter_by(user_id=user.id).all()}

    skills = []
    for skill_name in selected_names:
        catalog_item = catalog_by_name.get(skill_name)
        lessons = catalog_item.lessons if catalog_item else []
        completed = sum(lesson.id in completed_ids for lesson in lessons)
        level = levels.get(skill_name, 0)
        level = max(0, min(100, int(round(level)))) if isinstance(level, (int, float)) else 0
        skills.append({
            "name": skill_name,
            "category": catalog_item.categorie if catalog_item else "Skill",
            "level": level,
            "completed_lessons": completed,
            "total_lessons": len(lessons),
            "lesson_progress": round(completed * 100 / len(lessons)) if lessons else 0,
        })

    selected_names_set = set(selected_names)
    graph_edges = []
    graph_data = raw_data.get("skill_graph", {})
    if isinstance(graph_data, dict):
        for edge in graph_data.get("edges", []):
            if not isinstance(edge, dict):
                continue
            from_skill = edge.get("from_skill")
            to_skill = edge.get("to_skill")
            if from_skill in selected_names_set and to_skill in selected_names_set:
                graph_edges.append({"from_skill": from_skill, "to_skill": to_skill})

    showcase = raw_data.get("public_showcase", [])
    if not isinstance(showcase, list):
        showcase = []
    showcase = [item for item in showcase if isinstance(item, str)]

    return {
        "user": user,
        "profile": profile_data,
        "skills": skills,
        "skill_points": sum(skill["level"] for skill in skills),
        "completed_lesson_count": sum(skill["completed_lessons"] for skill in skills),
        "showcase": showcase,
        "graph": {
            "nodes": [
                {"skill": skill["name"], "category": skill["category"], "level": skill["level"]}
                for skill in skills
            ],
            "edges": graph_edges,
        },
        "avatar_url": url_for("dashboard.profile_avatar", username=user.username),
    }


@dashboard_bp.route("/u/<username>", endpoint="public_profile")
def public_profile(username):
    user = Users.query.filter_by(username=username).first_or_404()
    if not _profile_is_visible(user):
        abort(404)
    return render_template("dashboard/public_profile.html", **_public_profile_data(user))


@dashboard_bp.route("/u/<username>/avatar", endpoint="profile_avatar")
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


@dashboard_bp.route("/profile/update", methods=["POST"], endpoint="update_profile")
@login_required
def update_profile():
    account = current_user._get_current_object()
    profile_data = account.profile
    if profile_data is None:
        return redirect(url_for("auth.onboarding"))

    username = request.form.get("username", "").strip()
    if not username or len(username) > 100:
        flash("Bitte gib einen g?ltigen Benutzernamen ein.", "error")
        return redirect(url_for("dashboard.profile"))
    username_taken = Users.query.filter_by(username=username).first()
    if username_taken and username_taken.id != account.id:
        flash("Dieser Benutzername ist bereits vergeben.", "error")
        return redirect(url_for("dashboard.profile"))

    showcase = [line.strip() for line in request.form.get("showcase", "").splitlines() if line.strip()]
    if len(showcase) > 12 or any(len(item) > 200 for item in showcase):
        flash("Nutze h?chstens 12 Projekte oder Nachweise mit maximal 200 Zeichen pro Eintrag.", "error")
        return redirect(url_for("dashboard.profile"))

    uploaded_picture = request.files.get("profile_pic")
    picture_data = None
    max_bytes = current_app.config.get("MAX_PROFILE_PICTURE_BYTES", 2 * 1024 * 1024)
    if uploaded_picture and uploaded_picture.filename:
        picture_data = uploaded_picture.stream.read(max_bytes + 1)
        if len(picture_data) > max_bytes:
            flash("Das Profilbild darf h?chstens 2 MB gro? sein.", "error")
            return redirect(url_for("dashboard.profile"))
        if not _profile_picture_mimetype(picture_data):
            flash("Bitte lade ein PNG-, JPEG-, GIF- oder WebP-Bild hoch.", "error")
            return redirect(url_for("dashboard.profile"))

    account.username = username
    profile_data.first_name = request.form.get("first_name", "").strip()[:100] or profile_data.first_name
    profile_data.last_name = request.form.get("last_name", "").strip()[:100] or profile_data.last_name
    profile_data.goal_job = request.form.get("goal_job", "").strip()[:100] or profile_data.goal_job
    profile_data.job_experience = request.form.get("bio", "").strip()[:3000] or None
    profile_data.time_to_learn = request.form.get("time_to_learn", "").strip()[:50] or None
    visibility = request.form.get("visibility")
    if visibility in {"private", "public"}:
        profile_data.visibility = visibility

    if request.form.get("remove_profile_pic") == "on":
        profile_data.profile_pic = None
    elif picture_data is not None:
        profile_data.profile_pic = picture_data

    valid_skills = {item.skill_name for item in SkillCatalog.query.all()}
    selected_skills = list(dict.fromkeys(skill for skill in request.form.getlist("skills") if skill in valid_skills))
    selected_skills_names = []
    for skill_name in selected_skills:
        skill = SkillCatalog.query.filter_by(skill_name=skill_name).first()
        if skill:
            selected_skills_names.append(skill.id)

    profile_data.skills = [UserSkills(skill_catalog_id=skill_id) for skill_id in selected_skills_names]

    analysis = AIAnalysis.query.filter_by(user_id=account.id).first()
    if not analysis:
        analysis = AIAnalysis(user_id=account.id, raw_analysis_data={})
        db.session.add(analysis)
    raw_data = dict(analysis.raw_analysis_data) if isinstance(analysis.raw_analysis_data, dict) else {}
    raw_data["public_showcase"] = showcase
    analysis.raw_analysis_data = raw_data

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash("Deine ?nderungen konnten nicht gespeichert werden.", "error")
        return redirect(url_for("dashboard.profile"))

    flash("Dein Profil wurde gespeichert.", "success")
    return redirect(url_for("dashboard.profile"))


@dashboard_bp.route("/profile/delete", methods=["POST"], endpoint="delete_account")
@login_required
def delete_account():
    account = current_user._get_current_object()
    if not check_password_hash(account.pass_hash, request.form.get("password", "")):
        flash("Das Passwort ist falsch. Dein Konto wurde nicht gel?scht.", "error")
        return redirect(url_for("dashboard.profile"))
    if request.form.get("confirm_delete") != "yes":
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
    flash("Dein Konto wurde gel?scht.", "success")
    return redirect(url_for("core.home_page"))


@dashboard_bp.route("/lesson/<int:lesson_id>", endpoint="view_lesson")
@login_required
def view_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    answer = lesson.correct_answer.lower()
    print(answer)
    return render_template("dashboard/lesson.html", lesson=lesson, id=lesson_id, answer=answer)


@dashboard_bp.route("/lesson/<int:lesson_id>/submit", endpoint="submit_lesson")
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
    return redirect(url_for("dashboard.roadmap"))
