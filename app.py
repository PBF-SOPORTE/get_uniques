import streamlit as st
import os
from file_utils import list_supported_files, load_file

# Constants
INPUT_DIR = "input"

# UI - Title
st.title("📂 File Viewer - CSV & Excel")

# Check for directory
if not os.path.exists(INPUT_DIR):
    st.warning(f"The folder '{INPUT_DIR}' does not exist. Please create it and add some files.")
else:
    # Get list of files
    files = list_supported_files(INPUT_DIR)

    if not files:
        st.info("No CSV or Excel files found in the 'input' folder.")
    else:
        # File selection dropdown
        selected_file = st.selectbox("Select a file to view:", files)

        if selected_file:
            filepath = os.path.join(INPUT_DIR, selected_file)
            try:
                df = load_file(filepath)
                st.success(f"Successfully loaded: {selected_file}")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error reading file: {e}")
