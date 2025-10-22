import pyodbc

def add_item_to_database(config):

    # 1️⃣ Connect to SQL Server
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-LNSADFU\MYSECONDSERVER;"          # or 'hostname\\SQLEXPRESS'
        "DATABASE=Cmune;"
        "UID=sa;"
        "PWD=cmune$1;"
    )

    cursor = conn.cursor()

    # 2️⃣ Check if item already exists
    check_sql = "SELECT COUNT(*) FROM dbo.Items WHERE ItemId = ?"
    cursor.execute(check_sql, (config['item_id'],))
    exists = cursor.fetchone()[0] > 0
    
    if exists:
        print(f"⚠️ Item {config['name']} (ID: {config['item_id']}) already exists, skipping...")
        cursor.close()
        conn.close()
        return

    # 3️⃣ Enable IDENTITY_INSERT to allow explicit values in identity column
    cursor.execute("SET IDENTITY_INSERT dbo.Items ON")

    # 4️⃣ Prepare the INSERT query
    sql = """
    INSERT INTO dbo.Items (
        ItemId,
        Name,
        Description,
        CreditsPerDayShop,
        PointsPerDayShop,
        TypeId,
        IsForSale,
        AmountRemainingInShop,
        IsFeatured,
        PurchaseType,
        PermanentCreditsShop,
        IsNew,
        IsPopular,
        ClassId,
        PackOneAmount,
        PackTwoAmount,
        PackThreeAmount,
        MaximumOwnableAmount,
        Enable1Day,
        Enable7Days,
        Enable30Days,
        Enable90Days,
        MaximumDurationDays,
        PermanentPointsShop,
        IsDisable,
        CustomProperties,
        IsEnabledInShop,
        CreditsPerDayUnderground,
        PermanentCreditsUnderground,
        IsEnabledInUnderground,
        AmountRemainingInUnderground,
        UsageCount
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    # 5️⃣ Define the values to insert
    values = (
        config['item_id'],                  # ItemId
        config['name'],                     # Name
        config['description'],              # Description
        1000,                               # CreditsPerDayShop
        1000,                               # PointsPerDayShop
        config['type_id'],                  # TypeId
        False,                              # IsForSale
        100000,                             # AmountRemainingInShop
        False,                              # IsFeatured
        1,                                  # PurchaseType
        100000,                             # PermanentCreditsShop
        False,                              # IsNew
        False,                              # IsPopular
        config['class_id'],                 # ClassId
        1,                                  # PackOneAmount
        0,                                  # PackTwoAmount
        0,                                  # PackThreeAmount
        1,                                  # MaximumOwnableAmount
        True,                               # Enable1Day
        True,                               # Enable7Days
        True,                               # Enable30Days
        False,                              # Enable90Days
        30,                                 # MaximumDurationDays
        100000,                             # PermanentPointsShop
        False,                              # IsDisable
        '',                                 # CustomProperties
        True,                               # IsEnabledInShop
        1000,                               # CreditsPerDayUnderground
        100000,                             # PermanentCreditsUnderground
        False,                              # IsEnabledInUnderground
        100000,                             # AmountRemainingInUnderground
        0                                   # UsageCount
    )

    # 6️⃣ Execute and commit
    cursor.execute(sql, values)
    conn.commit()

    # 7️⃣ Disable IDENTITY_INSERT after insertion
    cursor.execute("SET IDENTITY_INSERT dbo.Items OFF")

    print(f"✅ Item {config['name']} inserted successfully!")

    # 8️⃣ Clean up
    cursor.close()
    conn.close()
