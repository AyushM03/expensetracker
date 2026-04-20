from fastapi import HTTPException, status
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.schemas import RegisterRequest, LoginRequest
from datetime import datetime


async def register_user(data: RegisterRequest) -> dict:
    db = get_db()

    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = {
        "name": data.name,
        "email": data.email,
        "hashed_password": hash_password(data.password),
        "created_at": datetime.utcnow(),
        "is_active": True,
    }
    result = await db.users.insert_one(user)
    user["_id"] = str(result.inserted_id)

    token = create_access_token({"sub": str(result.inserted_id), "email": data.email})
    return {"access_token": token, "token_type": "bearer"}


async def login_user(data: LoginRequest) -> dict:
    db = get_db()

    user = await db.users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token({"sub": str(user["_id"]), "email": user["email"]})
    return {"access_token": token, "token_type": "bearer"}
