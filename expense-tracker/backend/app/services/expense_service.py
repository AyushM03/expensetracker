from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from app.core.database import get_db
from app.core.redis import cache_get, cache_set, cache_delete
from app.schemas.schemas import ExpenseCreate, ExpenseUpdate


def expense_to_dict(exp: dict) -> dict:
    exp["id"] = str(exp.pop("_id"))
    return exp


async def create_expense(user_id: str, data: ExpenseCreate) -> dict:
    db = get_db()
    doc = {
        "user_id": user_id,
        "title": data.title,
        "amount": data.amount,
        "category": data.category.value if hasattr(data.category, "value") else data.category,
        "note": data.note,
        "date": data.date or datetime.utcnow(),
        "created_at": datetime.utcnow(),
    }
    result = await db.expenses.insert_one(doc)
    doc["_id"] = result.inserted_id
    # Invalidate summary cache on new expense
    await cache_delete(f"summary:{user_id}")
    return expense_to_dict(doc)


async def get_expenses(
    user_id: str,
    category: str = None,
    skip: int = 0,
    limit: int = 10,
) -> list:
    db = get_db()
    query = {"user_id": user_id}
    if category:
        query["category"] = category

    cursor = db.expenses.find(query).sort("date", -1).skip(skip).limit(limit)
    expenses = await cursor.to_list(length=limit)
    return [expense_to_dict(e) for e in expenses]


async def get_expense_by_id(user_id: str, expense_id: str) -> dict:
    db = get_db()
    exp = await db.expenses.find_one(
        {"_id": ObjectId(expense_id), "user_id": user_id}
    )
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense_to_dict(exp)


async def update_expense(user_id: str, expense_id: str, data: ExpenseUpdate) -> dict:
    db = get_db()
    updates = {k: v for k, v in data.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="Nothing to update")

    result = await db.expenses.find_one_and_update(
        {"_id": ObjectId(expense_id), "user_id": user_id},
        {"$set": updates},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Expense not found")
    await cache_delete(f"summary:{user_id}")
    return expense_to_dict(result)


async def delete_expense(user_id: str, expense_id: str):
    db = get_db()
    result = await db.expenses.delete_one(
        {"_id": ObjectId(expense_id), "user_id": user_id}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    await cache_delete(f"summary:{user_id}")
    return {"message": "Expense deleted"}


async def get_monthly_summary(user_id: str, month: str) -> dict:
    """month format: YYYY-MM e.g. 2026-04"""
    cache_key = f"summary:{user_id}:{month}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    db = get_db()
    year, mon = map(int, month.split("-"))
    start = datetime(year, mon, 1)
    end = datetime(year, mon + 1, 1) if mon < 12 else datetime(year + 1, 1, 1)

    pipeline = [
        {"$match": {"user_id": user_id, "date": {"$gte": start, "$lt": end}}},
        {"$group": {
            "_id": "$category",
            "total": {"$sum": "$amount"},
            "count": {"$sum": 1},
        }},
    ]
    results = await db.expenses.aggregate(pipeline).to_list(length=100)

    by_category = {r["_id"]: r["total"] for r in results}
    total = sum(by_category.values())
    count = sum(r["count"] for r in results)

    summary = {
        "month": month,
        "total": total,
        "by_category": by_category,
        "count": count,
    }
    await cache_set(cache_key, summary, expire=300)
    return summary
