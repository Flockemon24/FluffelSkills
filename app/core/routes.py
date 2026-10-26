from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from app.database import EarlyBirdWarteliste, db

core_bp = Blueprint("core", __name__)


@core_bp.route("/", methods=["GET", "POST"], endpoint="home_page")
def home_page():
    return render_template("homepage.html")


@core_bp.route("/pricing", endpoint="pricing")
def pricing():
    return render_template("pricing.html")


@core_bp.route("/api/join-waitlist", methods=["POST"], endpoint="warteliste_beitreten")
@login_required
def warteliste_beitreten():
    data = request.get_json() or {}
    plan_name = data.get("plan_name", "PRO")

    try:
        exists = db.session.execute(
            db.select(EarlyBirdWarteliste).filter_by(user_id=current_user.id)
        ).scalar_one_or_none()

        if exists:
            return jsonify({
                "status": "success",
                "message": "Bereits auf der Liste registriert.",
                "free_months": 1,
            }), 200

        neuer_eintrag = EarlyBirdWarteliste(
            user_id=current_user.id,
            plan_name=plan_name,
        )

        db.session.add(neuer_eintrag)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"Erfolgreich für {plan_name} eingetragen!",
            "free_months": 1,
        }), 201

    except Exception as exc:
        db.session.rollback()
        print(f"Fehler beim Eintragen in die Warteliste: {exc}")
        return jsonify({"status": "error", "message": "Datenbankfehler beim Eintragen."}), 500


@core_bp.route("/terms", endpoint="terms")
def terms():
    return "Nutzungsbedingungen"


@core_bp.route("/privacy-policy", endpoint="privacy_policy")
def privacy_policy():
    return "Datenschutzerklärung"
