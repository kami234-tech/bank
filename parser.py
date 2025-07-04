import fitz  # PyMuPDF
import re
from datetime import datetime

def extract_transactions(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = "".join([page.get_text() for page in doc])
        lines = text.split("\n")
        transactions = []

        for i, line in enumerate(lines):
            try:
                match = re.match(r"(\d{2}-\d{2}-\d{4} \d{2}:\d{2})", line)
                if not match:
                    continue

                date_str = match.group(1)
                amount_block = " ".join(lines[i:i+6])

                amount_match = re.search(
                    r"Suma (?:platita|retrasa|primita|incasata) ([\d,.]+) RON",
                    amount_block, re.IGNORECASE
                )
                income_match = re.search(
                    r"(Transfer primit|Suma primita|Incasare)",
                    amount_block, re.IGNORECASE
                )

                # Determine category & description
                if income_match:
                    category = "income"
                    description = "Incasare 💰"
                elif "Retragere numerar" in amount_block or "Suma retrasa" in amount_block:
                    category = "expense"
                    description = "Retragere 💸"
                else:
                    category = "expense"
                    location_match = re.search(
                        r"Locatie: (.+?)(?:\.|\sData_Ora:|\sSuma)",
                        amount_block
                    )
                    description = location_match.group(1).strip() if location_match else "Tranzactie"

                if amount_match:
                    amount = float(amount_match.group(1).replace(",", "."))
                    date = datetime.strptime(date_str, "%d-%m-%Y %H:%M").strftime("%Y-%m-%d %H:%M")

                    transactions.append({
                        "amount": amount,
                        "date": date,
                        "description": description,
                        "category": category
                    })
            except Exception as line_error:
                print(f"❌ Line {i} parse error: {line_error}")
                continue  # Skip this line but keep going

        print(f"✅ Parsed {len(transactions)} transactions.")
        return transactions

    except Exception as e:
        print(f"❌ Failed to extract transactions: {e}")
        return []
