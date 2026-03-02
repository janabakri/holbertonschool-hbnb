from flask_jwt_extended import get_jwt

claims = get_jwt()

if not claims.get("is_admin"):
    return {"error": "Admins only"}, 403
