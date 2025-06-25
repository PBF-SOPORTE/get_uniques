import streamlit as st
import os
from file_utils import (
    list_supported_files,
    is_excel_file,
    get_excel_sheets,
    load_file,
    clean_and_export_all_sheets
)

INPUT_DIR = "input"
st.title("📂 File Viewer - CSV & Excel")

if not os.path.exists(INPUT_DIR):
    st.warning(f"The folder '{INPUT_DIR}' does not exist.")
else:
    files = list_supported_files(INPUT_DIR)

    if not files:
        st.info("No CSV or Excel files found.")
    else:
        selected_file = st.selectbox("Select a file to view:", files)

        if selected_file:
            filepath = os.path.join(INPUT_DIR, selected_file)

            sheet_name = None
            if is_excel_file(selected_file):
                sheet_names = get_excel_sheets(filepath)
                if sheet_names:
                    sheet_name = st.selectbox("Select a sheet to preview:", sheet_names)

            try:
                df, stats = load_file(filepath, sheet_name=sheet_name)
                st.success(f"Loaded: {selected_file} ({sheet_name if sheet_name else 'CSV'})")

                # Show file stats
                st.subheader("📊 File Statistics")
                for key, value in stats.items():
                    st.write(f"**{key}:** {value}")

                st.subheader("📄 Data Preview")
                st.dataframe(df)

                # Optional: Download all cleaned sheets
                if is_excel_file(selected_file):
                    st.subheader("⬇️ Export Cleaned Sheets")
                    output_buffer = clean_and_export_all_sheets(filepath)
                    st.download_button(
                        label="Download Cleaned Excel File",
                        data=output_buffer,
                        file_name=f"cleaned_{selected_file}",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            except Exception as e:
                st.error(f"Error reading file: {e}")
