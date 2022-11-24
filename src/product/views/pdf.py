from pathlib import Path
from os import path

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

FILEPATH = Path(__file__).resolve().parent

data = {
    "id": 1,
    "customer": {
        "id_birth": "000000/0000",
        "full_name": "a a",
        "personal_id": "0000000000",
        "personal_id_expiration_date": "2023-01-01",
        "residence": "Cejl 111",
        "nationality": "CZ",
        "birthplace": "Brno",
        "sex": "M",
    },
    "sell_price": 111,
    "status": "LOAN",
    "rate_frequency": "WEEK",
    "rate_times": 4,
    "rate": "2.2",
    "product_name": "tel",
    "buy_price": 1000,
    "quantity": 1,
    "inventory_id": 0,
    "date_create": "2022-10-01T14:31:31.018000Z",
    "date_extend": "2022-10-01T14:31:31.018000Z",
    "date_end": None,
    "user": 1,
    "interest": [
        {"from": "2022-10-04", "to": "2022-10-11", "price": 1025},
        {"from": "2022-10-11", "to": "2022-10-18", "price": 1050},
        {"from": "2022-10-18", "to": "2022-10-25", "price": 1070},
        {"from": "2022-10-25", "to": "2022-11-01", "price": 1095},
    ],
}


def generate_pdf():
    p = canvas.Canvas(path.join(FILEPATH, "foo.pdf"), pagesize=letter)
    p.drawString(100, 100, "Hello world.")
    p.showPage()
    p.save()


if __name__ == "__main__":
    generate_pdf()
