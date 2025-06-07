from fastapi import FastAPI, UploadFile, File, Request, Depends
from parser import extract_transactions
from firebase_config import db
from auth import authenticate_user
import os
import uuid
from datetime import datetime

app = FastAPI()

@app.post("/parse")
async def parse_pdf(
    file: UploadFile = File(...),
    uid: str = Depends(authenticate_user)  # ✅ use dependency injection here
):
    temp_path = f"/tmp/{uuid.uuid4()}.pdf"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    transactions = extract_transactions(temp_path)
    os.remove(temp_path)

    for tx in transactions:
        doc_data = {
            "amount": str(tx["amount"]),
            "createdAt": datetime.utcnow(),
            "name": tx["description"],
            "currency": "RON",
        }
        category = "income" if tx["category"] == "income" else "otherExpenses"
        db.collection(f"users/{uid}/{category}").add(doc_data)

    return {"success": True, "transactions": transactions}
