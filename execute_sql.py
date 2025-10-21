import pyodbc

# 1️⃣ Connect to SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-LNSADFU\MYSECONDSERVER;"          # or 'hostname\\SQLEXPRESS'
    "DATABASE=Cmune;"
    "UID=sa;"
    "PWD=cmune$1;"
)

cursor = conn.cursor()

# 2️⃣ Prepare the INSERT query
sql = """
INSERT INTO dbo.Items (
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
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
config = {}
config['name'] = ""
config['description'] = ""
config['type_id'] = 0
config['class_id'] = 0
# config['permanent_points'] = 0
# config['permanent_credits'] = 0
# config['points_per_day'] = 0
# config['credits_per_day'] = 0


# 3️⃣ Define the values to insert
values = (
    'Sword of Dawn',                    # Name
    'A rare sword imbued with light.',  # Description
    1000,                               # CreditsPerDayShop
    1000,                               # PointsPerDayShop
    2,                                  # TypeId
    False,                              # IsForSale
    100000,                             # AmountRemainingInShop
    False,                              # IsFeatured
    1,                                  # PurchaseType
    100000,                             # PermanentCreditsShop
    False,                              # IsNew
    False,                              # IsPopular
    3,                                  # ClassId
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

# 4️⃣ Execute and commit
cursor.execute(sql, values)
conn.commit()

print("✅ Item inserted successfully!")

# 5️⃣ Clean up
cursor.close()
conn.close()
