import streamlit as st
import requests
import re
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io


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
    st.session_state.data = uploaded_file.read()
    st.success(f"Uploaded file: {uploaded_file.name}")

    # Upload to backend
    with st.spinner("Uploading and analyzing..."):
        files = {"file": (uploaded_file.name, io.BytesIO(st.session_state.data), "text/csv")}
        upload_response = requests.post(f"{API_URL}/upload", files=files)

        if upload_response.status_code == 200:
            st.session_state.uploaded_filename = uploaded_file.name

            # Request analysis
            analyze_response = requests.get(
                f"{API_URL}/analyze", params={"filename": uploaded_file.name}
            )

            if analyze_response.status_code == 200:
                result = analyze_response.json()

                # --- EDA ---
                tab1, tab2, tab3 = st.tabs(["📈 EDA Summary", "📊 Univariate Analysis", "📉 Multivariate Analysis"])

                with tab1:
                    st.subheader("📈 EDA Summary")
                    # Combine EDA results into one table
                    eda_df = pd.DataFrame({
                        "Column": result['eda']['columns'],
                        "Data Type": [result['eda']['dtypes'].get(col, '-') for col in result['eda']['columns']],
                        "Missing Values": [result['eda']['missing'].get(col, '-') for col in result['eda']['columns']]
                    })

                    st.markdown("#### 📋 Overview")
                    st.dataframe(eda_df, use_container_width=True)

                    # Display shape separately in a friendly way
                    shape = result['eda']['shape']
                    st.markdown(f"**Shape:** {shape[0]} rows × {shape[1]} columns")

                    # --- Statistical Summary ---
                    st.markdown("#### 📊 Statistical Summary")
                    # Convert describe to DataFrame and transpose
                    describe_df = pd.DataFrame(result['eda']['describe']).T

                    # Drop ID-like columns
                    describe_df = describe_df.drop(
                        index=[col for col in describe_df.index if "id" in col.lower()],
                        errors="ignore"
                    )
                    st.dataframe(describe_df, use_container_width=True)

                with tab2:
                    st.subheader("📊 Univariate Analysis")
                    df = pd.read_csv(io.BytesIO(st.session_state.data))


                    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                    numeric_cols = [col for col in numeric_cols if col.lower() not in ["order_id", "customer_id"]]
                    for col in numeric_cols:
                        fig, ax = plt.subplots(figsize=(3, 1))
                        sns.histplot(df[col].dropna(), kde=True, ax=ax)
                        pretty_col = col.replace('_', ' ').title()
                        ax.set_title(f"Distribution of {pretty_col}")
                        st.pyplot(fig, clear_figure=True, use_container_width=False)

                    for col in numeric_cols:
                        fig, ax = plt.subplots(figsize=(5, 3))
                        sns.boxplot(df[col].dropna(), ax=ax)
                        pretty_col = col.replace('_', ' ').title()
                        ax.set_title(f"Distribution of {pretty_col}")
                        st.pyplot(fig, clear_figure=True, use_container_width=False)


                with tab3:
                    st.subheader("📉 Multivariate Analysis")
                    df = pd.read_csv(io.BytesIO(st.session_state.data))
                    if len(numeric_cols) >= 2:
                        fig, ax = plt.subplots(figsize=(3, 1))
                        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
                        ax.set_title("Correlation Matrix")
                        st.pyplot(fig, clear_figure=True, use_container_width=False)


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
