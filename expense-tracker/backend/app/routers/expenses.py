from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.routers.deps import get_current_user
from app.schemas.schemas import ExpenseCreate, ExpenseUpdate
from app.services import expense_service, ai_service

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", status_code=201)
async def create(data: ExpenseCreate, user=Depends(get_current_user)):
    return await expense_service.create_expense(user["id"], data)


@router.get("/")
async def list_expenses(
    category: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    user=Depends(get_current_user),
):
    return await expense_service.get_expenses(user["id"], category, skip, limit)


@router.get("/summary/{month}")
async def monthly_summary(month: str, user=Depends(get_current_user)):
    """month format: YYYY-MM example: 2026-04"""
    return await expense_service.get_monthly_summary(user["id"], month)


@router.get("/ai-advice/{month}")
async def ai_advice(
    month: str,
    question: Optional[str] = None,
    user=Depends(get_current_user),
):
    summary = await expense_service.get_monthly_summary(user["id"], month)
    advice = ai_service.get_ai_advice(summary, question)
    return {"month": month, "advice": advice}


@router.get("/{expense_id}")
async def get_one(expense_id: str, user=Depends(get_current_user)):
    return await expense_service.get_expense_by_id(user["id"], expense_id)


@router.put("/{expense_id}")
async def update(expense_id: str, data: ExpenseUpdate, user=Depends(get_current_user)):
    return await expense_service.update_expense(user["id"], expense_id, data)


@router.delete("/{expense_id}")
async def delete(expense_id: str, user=Depends(get_current_user)):
    return await expense_service.delete_expense(user["id"], expense_id)
