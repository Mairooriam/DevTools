import pandas as pd

# Path to your CSV file
CSV_FILE_PATH = "data/contactors_AC3_AND_AC1.csv"

# Path to the output SQL file
OUTPUT_SQL_FILE = "output/contactors.sql"

# Table name
TABLE_NAME = "main.contactor_type"

def generate_sql_from_csv():
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(CSV_FILE_PATH)

        # Open the output file in write mode
        with open(OUTPUT_SQL_FILE, "w") as sql_file:
            for _, row in df.iterrows():
                # Generate the SQL INSERT statement for each row (excluding ID)
                sql_statement = f"""
                INSERT INTO {TABLE_NAME} (In_ac1, In_ac3, p_ac1, p_ac3, Ik, nc_aux_count, no_aux_count, control_voltage, heat_dissipation_AC1, heat_dissipation_AC3)
                VALUES ({row['In_ac1']}, {row['In_ac3']}, {row['p_ac1']}, {row['p_ac3']}, {row['Ik']}, {row['nc_aux_count']}, {row['no_aux_count']}, '{row['control_voltage']}', {row['heat_dissipation_AC1']}, {row['heat_dissipation_AC3']});
                """
                # Write the SQL statement to the file
                sql_file.write(sql_statement.strip() + "\n")

        print(f"SQL statements successfully written to {OUTPUT_SQL_FILE}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_sql_from_csv()