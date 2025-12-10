from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.models.schemas import UserCreate, Token
from src.services.auth import verify_password, get_password_hash, create_access_token
from src.db import get_db

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate, db=Depends(get_db)):
    """Create user with username, email, password (psycopg)"""
    try:
        async with db.cursor() as cur:
            await cur.execute(
                "SELECT COUNT(*) FROM users WHERE email = %s",
                (user.email,),
            )
            row = await cur.fetchone()
            existing = row[0] if row else 0

            if existing > 0:
                raise HTTPException(status_code=400, detail="Email already registered!")

            hashed_password = get_password_hash(user.password)

            await cur.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
                """,
                (user.username, user.email, hashed_password),
            )

        return {
            "message": "✅ User created!",
            "login": f"Email: {user.email}, use your chosen password to login.",
        }

    except Exception as e:
        print("❌ SIGNUP ERROR:", e)
        raise HTTPException(status_code=500, detail=f"Signup failed: {e}")

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute(
            "SELECT username, email, password FROM users WHERE email = %s",
            (form_data.username,) # form_data.username is the email from the form
        )
        row = await cur.fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="❌ Wrong email/password")

    username, email, hashed_password = row
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=401, detail="❌ Wrong email/password")

    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}
