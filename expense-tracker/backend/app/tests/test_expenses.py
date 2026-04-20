import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code == 200

@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/auth/register", json={
            "name": "Ayush", "email": "ayush@test.com", "password": "test1234"
        })
    assert r.status_code == 200
    assert "access_token" in r.json()

@pytest.mark.asyncio
async def test_create_expense_unauthorized():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/expenses/", json={
            "title": "Food", "amount": 200, "category": "food"
        })
    assert r.status_code == 401
