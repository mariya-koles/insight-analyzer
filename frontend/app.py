import streamlit as st
import requests
import re

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Insight Analyzer", layout="wide")

st.title("📊 Insight Analyzer")
st.markdown("Upload a CSV file to explore it and get AI-generated insights.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None


if uploaded_file is not None:
    # Display file info
    st.success(f"Uploaded file: {uploaded_file.name}")

    # Upload to backend
    with st.spinner("Uploading and analyzing..."):
        files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
        upload_response = requests.post(f"{API_URL}/upload", files=files)

        if upload_response.status_code == 200:
            st.session_state.uploaded_filename = uploaded_file.name

            # Request analysis
            analyze_response = requests.get(
                f"{API_URL}/analyze", params={"filename": uploaded_file.name}
            )

            if analyze_response.status_code == 200:
                result = analyze_response.json()

                # --- EDA Summary ---
                st.subheader("📈 EDA Summary")
                st.write("**Shape:**", result['eda']['shape'])
                st.write("**Columns:**", result['eda']['columns'])
                st.write("**Data Types:**")
                st.json(result['eda']['dtypes'])
                st.write("**Missing Values:**")
                st.json(result['eda']['missing'])
                st.write("**Statistical Summary:**")
                st.json(result['eda']['describe'])

                # --- LLM Insight ---
                st.subheader("🧠 AI Insight")

                # Clean and display initial insight
                cleaned_insight = (
                    result["insight"]
                    .replace('\xa0', ' ')
                    .replace('$', r'\$')
                    .strip()
                )
                cleaned_insight = re.sub(r'\n{3,}', '\n\n', cleaned_insight)
                st.markdown(cleaned_insight)

                # Regenerate button
                if st.button("🔁 Regenerate Insight"):
                    with st.spinner("Re-generating insight..."):
                        retry_response = requests.get(
                            f"{API_URL}/analyze", params={"filename": st.session_state.uploaded_filename}
                        )

                        if retry_response.status_code == 200:
                            retry_result = retry_response.json()

                            cleaned_retry_insight = (
                                retry_result["insight"]
                                .replace('\xa0', ' ')
                                .replace('$', r'\$')
                                .strip()
                            )
                            cleaned_retry_insight = re.sub(r'\n{3,}', '\n\n', cleaned_retry_insight)

                            st.markdown("#### 🔄 Refreshed Insight")
                            st.markdown(cleaned_retry_insight)
                        else:
                            st.error("Failed to regenerate insight.")
            else:
                st.error(f"Analysis failed: {analyze_response.text}")
        else:
            st.error(f"Upload failed: {upload_response.text}")
