#/bin/bash






















curl -X 'POST' 'http://localhost:8000/product/' \
  -H 'accept: application/json' \
  -H 'Origin: **http://localhost:3000**' \
  -H 'Content-Type: application/json' \
  -d '{
  "user": 1,
  "status": "LOAN",
  "full_name": "a b",
  "residence": "Cejl 2",
  "sex": "M",
  "nationality": "CZ",
  "personal_id": "0000000000",
  "personal_id_expiration_date": "29/09/2022",
  "birthplace": "Brno",
  "id_birth": "000000/0100",
  "interest_rate_or_quantity": 3,
  "inventory_id": 3,
  "product_name": "3",
  "buy_price": 3,
  "sell_price": 5
}'
