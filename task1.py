import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Titanic Data Explorer", layout="wide")

st.markdown(
    """
    <style>
        .main {
            background: #f5f7fb;
        }
        .stApp {
            color: #1f2937;
        }
        div[data-testid="stSidebar"] {
            background: #111827;
            color: white;
        }
        h1, h2, h3 {
            color: #111827;
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
        except Exception as e:
            st.error(f"Could not read the uploaded file. Error: {e}")
            return None
        return df

    default_file = Path(__file__).with_name("Titanic-Dataset.csv")
    if default_file.exists():
        return pd.read_csv(default_file)

    return None


with st.sidebar:
    st.header("Controls")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    st.caption("If no file is uploaded, the app loads the Titanic dataset from the project folder.")

st.title("Titanic Data Explorer")
st.caption("A simple dashboard for viewing a dataset and exploring a single column.")


df = load_data(uploaded_file)

if df is None:
    st.info("Please upload a CSV file to start exploring.")
    st.stop()

if df.empty:
    st.warning("The uploaded CSV is empty.")
    st.stop()

st.subheader("Dataset overview")
col1, col2, col3 = st.columns(3)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing values", int(df.isnull().sum().sum()))

st.dataframe(df.head(10), use_container_width=True)

st.subheader("Column explorer")
selected_column = st.selectbox("Choose a column", df.columns.tolist())

if pd.api.types.is_numeric_dtype(df[selected_column]):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(df[selected_column].dropna(), bins=20, color="#4f46e5", edgecolor="black")
    ax.set_title(f"Histogram: {selected_column}")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Frequency")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(fig)
else:
    counts = df[selected_column].fillna("Missing").value_counts()
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(counts.index.astype(str), counts.values, color="#f59e0b", edgecolor="black")
    ax.set_title(f"Bar chart: {selected_column}")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Count")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.3,
            str(int(height)),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)

st.subheader("Quick summary")
summary = df.describe(include="all").T
st.dataframe(summary, use_container_width=True)