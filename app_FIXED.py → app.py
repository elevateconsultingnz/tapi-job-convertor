
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Tapi ➤ Tradify CSV Convertor", layout="centered", page_icon="📄")

# Add branding banner
st.image("logo.jpg", use_container_width=True)

st.title("📄 Tapi ➤ Tradify Work Order 'CSV File' Job Convertor")

st.markdown("""
**Upload your Tapi job CSV or XLSX file below.**  
We'll convert the column names and strip out unneeded columns so it's ready for import into Tradify.
""")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Corrected column mapping based on actual headers from your file
    column_map = {
        "description": "Description",
        "job_number": "Reference",
        "company": "Customer",
        "head_tenant_name": "Site Contact",
        "head_tenant_mobile_phone": "Site Contact Mobile",
        "full_address": "Job Address",
        "city": "City"
    }

    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df = df.rename(columns=column_map)
    final_columns = list(column_map.values())
    df = df[[col for col in final_columns if col in df.columns]]

    st.success("✅ File processed. Preview below:")
    st.dataframe(df.head())

    output = io.StringIO()
    df.to_csv(output, index=False)
    st.download_button("⬇️ Download Converted CSV", data=output.getvalue(), file_name="converted_jobs.csv", mime="text/csv")
else:
    st.info("Upload a CSV or XLSX file to get started.")
