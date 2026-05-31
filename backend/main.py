from fastapi import FastAPI
from api.user import router as user_router
from api.budget import router as user_budget
from api.income import router as user_income
from api.category import router as user_category
from api.subscription import router as user_subscription
from api.expense import router as user_expense
import uvicorn

app = FastAPI()


@app.get("/health")
def health_check():
    return {"statut": "ok",
            "message": "Spendless API is running",
            "database": "connected",
            "version": "1.0.0"}


app.include_router(user_router)
app.include_router(user_budget)
app.include_router(user_income)
app.include_router(user_category)
app.include_router(user_subscription)
app.include_router(user_expense)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
