import csv

with open('processed_circuit_breakers.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    with open('output.sql', 'w', encoding='utf-8') as outfile:
        for row in reader:
            outfile.write(
                f"""INSERT INTO main.circuit_breaker_model (type_id, manufacturer_id, order_number, description, sahkonumero, price)
SELECT t.ID, 2, '{row['order_number']}', '{row['description']}', '{row['sahkonumero']}', {row['price']}
FROM main.circuit_breaker_type t
WHERE t.curve='{row['curve']}' AND t.phases={row['phases']} AND t."In"={row['in']} AND t.Ik={row['ik']};\n"""
            )