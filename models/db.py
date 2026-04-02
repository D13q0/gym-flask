import pyodbc
from config import DB_CONFIG

def get_connection():
    return pyodbc.connect(
        f"DRIVER={DB_CONFIG['DRIVER']};"
        f"SERVER={DB_CONFIG['SERVER']};"
        f"DATABASE={DB_CONFIG['DATABASE']};"
        f"Trusted_Connection={DB_CONFIG['Trusted_Connection']};"
    )