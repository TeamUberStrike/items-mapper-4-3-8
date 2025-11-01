import pyodbc

def add_item_to_database(table_name, database, values, use_identity_insert=True):

    # 1️⃣ Connect to SQL Server
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-LNSADFU\MYSECONDSERVER;"          # or 'hostname\\SQLEXPRESS'
        f"DATABASE={database};"
        "UID=sa;"
        "PWD=cmune$1;"
    )

    cursor = conn.cursor()

    # 2️⃣ Check if item already exists
    check_sql = f"SELECT COUNT(*) FROM {table_name} WHERE ItemId = ?"
    cursor.execute(check_sql, (values['ItemId'],))
    exists = cursor.fetchone()[0] > 0
    
    if exists:
        item_name = values.get('Name', 'Unknown')
        print(f"⚠️ Item {item_name} (ID: {values['ItemId']}) already exists in {table_name}, skipping...")
        cursor.close()
        conn.close()
        return

    # 3️⃣ Enable IDENTITY_INSERT to allow explicit values in identity column (only if needed)
    if use_identity_insert:
        cursor.execute(f"SET IDENTITY_INSERT {table_name} ON")

    # 4️⃣ Prepare the INSERT query dynamically
    columns = list(values.keys())
    placeholders = ', '.join(['?'] * len(columns))
    columns_str = ', '.join(columns)
    
    sql = f"""
    INSERT INTO {table_name} (
        {columns_str}
    )
    VALUES ({placeholders})
    """

    # 5️⃣ Get the values in the same order as columns
    insert_values = tuple(values[col] for col in columns)

    # 6️⃣ Execute and commit
    cursor.execute(sql, insert_values)
    conn.commit()

    # 7️⃣ Disable IDENTITY_INSERT after insertion (only if it was enabled)
    if use_identity_insert:
        cursor.execute(f"SET IDENTITY_INSERT {table_name} OFF")

    print(f"✅ Item ID {values['ItemId']} inserted successfully into {table_name}!")

    # 8️⃣ Clean up
    cursor.close()
    conn.close()
