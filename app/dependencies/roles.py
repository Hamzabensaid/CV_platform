from fastapi import Depends, HTTPException, status
from app.models.user_model import UserOut
from app.core.auth import get_current_user

def require_roles(*allowed_roles: str):
    """
    Dependency to restrict access to certain roles.
    Example: Depends(require_roles("admin", "recruiter"))
    """
    def role_checker(current_user: UserOut = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return current_user
    return role_checker
