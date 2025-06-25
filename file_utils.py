import os
import pandas as pd
from io import BytesIO

SUPPORTED_EXTENSIONS = [".csv", ".xls", ".xlsx"]

def list_supported_files(directory):
    if not os.path.exists(directory):
        return []
    return [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ]

def is_excel_file(filename):
    return filename.endswith((".xls", ".xlsx"))

def get_excel_sheets(filepath):
    try:
        return pd.ExcelFile(filepath).sheet_names
    except Exception:
        return []

def load_file(filepath, sheet_name=None):
    """Load one sheet or CSV file and remove duplicate rows."""
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath, header=0)
    else:
        df = pd.read_excel(filepath, sheet_name=sheet_name, header=0)

    original_rows = len(df)
    df = df.drop_duplicates()
    stats = {
        "Total rows": original_rows,
        "Duplicate rows removed": original_rows - len(df),
        "Final rows": len(df),
        "Columns": df.shape[1]
    }
    return df, stats

def clean_and_export_all_sheets(filepath):
    """Clean all sheets in an Excel file and return a downloadable Excel buffer."""
    excel_file = pd.ExcelFile(filepath)
    sheet_names = excel_file.sheet_names

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet in sheet_names:
            df = pd.read_excel(filepath, sheet_name=sheet, header=0)
            df_cleaned = df.drop_duplicates()
            df_cleaned.to_excel(writer, sheet_name=sheet, index=False)
    output.seek(0)
    return output
