# Setup
- install driver ODBC Driver 17 for SQL Server, eg in Ubuntu: 

```
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
```

```
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
```

```
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

- set database string in execute_sql.py
Have a look in uber-server-4-3-8 for credentials and server ip.
```
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-LNSADFU\MYSECONDSERVER;"
    f"DATABASE={database};"
    "UID=sa;"
    "PWD=cmune$1;"
)
```

- get Python dependencies
```
poetry init
```

- execute script which fills the tables
```
poetry run python main.py
```

# Procudure
This is the last part of setting up the database.
First part is in uber-server DataAccess.Setup which creates the databases.
It includes .sql files to be executed.
Only if this is successfully finished, this must be executed, which is mainly about
the items.

