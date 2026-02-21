import csv

with open('yourfile.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(f"""INSERT INTO main.circuit_breaker_model (type_id, manufacturer_id, order_number, model, sahkonumero, price)
SELECT t.ID, 2, '{row['order_number']}', '{row['description']}', '{row['sahkonumero']}', {row['price']}
FROM main.circuit_breaker_type t
WHERE t.curve='{row['curve']}' AND t.phases={row['phases']} AND t."In"={row['in']} AND t.Ik={row['ik']};""")