import os
import secrets
import time
from functools import wraps

from flask import Blueprint, jsonify, request, Response
import redis

import app.database as db

# Erstellt den API-Blueprint (Zentraler Präfix: /api/v1)
api_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')


def get_redis_client():
    """Create a Redis client lazily so imports do not block on a missing Redis instance."""
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        try:
            client = redis.Redis.from_url(redis_url, decode_responses=True, socket_connect_timeout=1, socket_timeout=1)
            client.ping()
            return client
        except redis.exceptions.RedisError:
            return None

    try:
        client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, socket_connect_timeout=1, socket_timeout=1)
        client.ping()
        return client
    except redis.exceptions.RedisError:
        return None


r = get_redis_client()

def require_api_token(f):
    """
    Hochentwickelter Decorator für Token-Validierung und Redis-basiertes Rate-Limiting.
    Fügt automatisch standardisierte X-RateLimit-Header an die Antwort an.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. Token aus dem Header extrahieren
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "error": "Fehlendes oder ungültiges Authorization-Format. Nutze 'Bearer <token>'"}), 401
        
        token = auth_header.split(" ")[1]
        
        # 2. Token in SQLite prüfen
        token_info = db.get_token_info(token)
        if not token_info:
            return jsonify({"success": False, "error": "Dieses API-Token existiert nicht oder ist ungültig."}), 403
            
        rate_limit, window_seconds = token_info
        
        # Standardwerte für die Header vorbereiten
        limit_header = "Infinite" if rate_limit == -1 else str(rate_limit)
        remaining_header = "Infinite"
        reset_header = "0"
        
        # 3. Rate-Limiting über Redis ausführen (nur wenn das Limit nicht unbegrenzt (-1) ist)
        if rate_limit != -1:
            redis_key = f"ratelimit:{token}"
            
            # Hole die aktuelle Anzahl an Anfragen in diesem Zeitfenster
            current_requests = r.get(redis_key)
            
            if current_requests and int(current_requests) >= rate_limit:
                # Limit überschritten! Berechne verbleibende Wartezeit
                ttl = r.ttl(redis_key)
                response = jsonify({
                    "success": False, 
                    "error": f"Rate Limit überschritten. Maximal {rate_limit} Anfragen erlaubt."
                })
                response.status_code = 429
                response.headers["X-RateLimit-Limit"] = limit_header
                response.headers["X-RateLimit-Remaining"] = "0"
                response.headers["X-RateLimit-Reset"] = str(ttl)
                response.headers["Retry-After"] = str(ttl) # Standard-HTTP-Verhalten
                return response
            
            # Nutze eine atomare Redis-Pipeline, um Race Conditions zu verhindern
            pipe = r.pipeline()
            pipe.incr(redis_key)
            # Wenn der Key brandneu ist, verpasse ihm das Ablaufdatum (window_seconds)
            if not current_requests:
                pipe.expire(redis_key, window_seconds)
            
            # Führe Pipeline aus und hole den aktuellen Zählerstand
            results = pipe.execute()
            new_count = results[0]
            
            remaining_header = str(max(0, rate_limit - new_count))
            reset_header = str(r.ttl(redis_key))
            
        # 4. Request erlauben und die passenden Header an die Response heften
        response, status_code = f(*args, **kwargs)
        
        # Falls eine rohe Flask-Response zurückgegeben wurde, in ein Objekt umwandeln
        if not isinstance(response, Response):
            response = jsonify(response)
            
        response.headers["X-RateLimit-Limit"] = limit_header
        response.headers["X-RateLimit-Remaining"] = remaining_header
        response.headers["X-RateLimit-Reset"] = reset_header
        response.status_code = status_code 
        return response

    return decorated_function


# ==========================================
# ENDPUNKTE
# ==========================================

@api_bp.route('/data', methods=['GET'])
@require_api_token
def get_secure_data():
    """Ein Beispiel-Endpunkt, der sensible Anwendungsdaten ausgibt."""
    return {
        "success": True,
        "message": "Erfolgreich autorisiert! Hier sind deine exklusiven Daten.",
        "payload": ["Wert X", "Wert Y", "Wert Z"]
    }, 200


@api_bp.route('/tokens/generate', methods=['POST'])
def generate_token():
    """
    Ein Admin-Endpunkt, um neue, benutzerdefinierte Tokens zu erstellen.
    Erwartet im JSON-Body: 'rate_limit' und 'window_seconds'.
    """
    data = request.get_json() or {}
    
    # Auslesen mit sicheren Standardwerten (-1 bedeutet unbegrenzt, Fenster 60s)
    rate_limit = data.get("rate_limit", -1)
    window_seconds = data.get("window_seconds", 60)
    
    # Generiere ein absolut sicheres, zufälliges Token im Hex-Format
    new_token = f"key_{secrets.token_hex(16)}"
    
    # In SQLite abspeichern
    success = db.insert_new_token(new_token, rate_limit, window_seconds)
    
    if success:
        return {
            "success": True,
            "message": "Neues API-Token erfolgreich registriert.",
            "token": new_token,
            "config": {
                "rate_limit": rate_limit,
                "window_seconds": window_seconds
            }
        }, 201
    else:
        return {"success": False, "error": "Fehler beim Generieren des Tokens."}, 500
