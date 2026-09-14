import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Titanic Data Explorer", layout="wide")

st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"], .main {
            background-color: black;
            color: white;
        }
        [data-testid="stSidebar"] {
            background-color: black;
            color: white;
        }
        .stApp {
            color: white;
        }
        h1, h2, h3, p, div, label, span {
            color: white !important;
        }
        .stDataFrame, .stTable, .stMetric {
            background-color: black;
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception:
            st.error("Please upload a valid CSV file.")
            return None

    default_file = Path(__file__).with_name("Titanic-Dataset.csv")
    if default_file.exists():
        return pd.read_csv(default_file)

    return None


st.sidebar.header("Upload")
uploaded_file = st.sidebar.file_uploader("CSV file", type=["csv"])

st.title("Titanic Data Viewer")


df = load_data(uploaded_file)

if df is None:
    st.stop()

if df.empty:
    st.warning("The file is empty.")
    st.stop()

st.subheader("Data")
st.dataframe(df.head(10), use_container_width=True)

selected_column = st.selectbox("Select column", df.columns.tolist())

if pd.api.types.is_numeric_dtype(df[selected_column]):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df[selected_column].dropna(), bins=20, color="white", edgecolor="black")
    ax.set_title(f"Histogram of {selected_column}")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Count")
    st.pyplot(fig)
else:
    counts = df[selected_column].fillna("Missing").value_counts()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(counts.index.astype(str), counts.values, color="white", edgecolor="black")
    ax.set_title(f"Bar chart of {selected_column}")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)

st.subheader("Summary")
st.dataframe(df.describe(include="all").T, use_container_width=True)