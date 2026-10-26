import os

from app import _get_bool_env, create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=_get_bool_env("FLASK_DEBUG", False))
