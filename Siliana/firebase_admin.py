import json
import os
from typing import Any, Dict

import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials


def _init_firebase_app() -> None:
    # Reuse default app if already initialized
    if firebase_admin._apps:
        return

    service_account_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
    service_account_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH", "").strip()

    if service_account_json:
        cred_obj = json.loads(service_account_json)
        cred = credentials.Certificate(cred_obj)
    elif service_account_path:
        cred = credentials.Certificate(service_account_path)
    else:
        raise RuntimeError(
            "Firebase Admin credentials not configured. Set FIREBASE_SERVICE_ACCOUNT_JSON "
            "or FIREBASE_SERVICE_ACCOUNT_PATH."
        )

    firebase_admin.initialize_app(cred)


def verify_firebase_id_token(id_token: str) -> Dict[str, Any]:
    """Verify a Firebase Authentication ID token and return decoded claims."""
    _init_firebase_app()
    return firebase_auth.verify_id_token(id_token)
