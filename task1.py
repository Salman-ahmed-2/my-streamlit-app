import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Exploratory Data Analysis Interface", layout="wide")

# ---------------- Sidebar: Dataset Controls ----------------
st.sidebar.header("Dataset Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV File for Analysis", type=["csv"])

st.title("Exploratory Data Analysis Interface")

if uploaded_file is not None:
    # Validate that the uploaded file is a correctly formatted CSV
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error("The uploaded file is empty. Please upload a valid CSV.")
            st.stop()
    except Exception as e:
        st.error(f"Could not read the uploaded file as a CSV. Error: {e}")
        st.stop()

    # ---------------- Dataset Preview & Metadata ----------------
    st.subheader("Dataset Preview & Metadata")

    st.write("First 5 Rows:")
    st.dataframe(df.head())

    st.write("Shape:", df.shape)

    st.write("Column Data Types:")
    dtypes_df = df.dtypes.astype(str).reset_index()
    dtypes_df.columns = ["Column", "Data Type"]
    st.dataframe(dtypes_df)

    st.write("Missing Values per Column:")
    missing_df = pd.DataFrame({
        "Missing Count": df.isnull().sum(),
        "Missing %": (df.isnull().sum() / len(df) * 100).round(2)
    })
    st.dataframe(missing_df)

    st.write("Basic Statistical Summary (Numerical Attributes):")
    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        summary = numeric_df.describe().loc[["mean", "50%", "min", "max"]]
        summary = summary.rename(index={"50%": "median"})
        st.dataframe(summary)
    else:
        st.info("No numerical columns found in this dataset.")

    # ---------------- Sidebar: Attribute Selection ----------------
    st.sidebar.header("Attribute Selection")
    selected_column = st.sidebar.selectbox("Select Attribute for Visualization", df.columns)

    # ---------------- Visualization Module ----------------
    st.subheader("Visualization")

    if pd.api.types.is_numeric_dtype(df[selected_column]):
        # Numerical -> Histogram
        fig, ax = plt.subplots()
        ax.hist(df[selected_column].dropna(), bins=20, color="skyblue", edgecolor="black")
        ax.set_title(f"Histogram of {selected_column}")
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:
        # Categorical -> Bar chart with frequency counts + percentage
        counts = df[selected_column].value_counts()
        percentages = (counts / counts.sum() * 100).round(2)

        fig, ax = plt.subplots()
        bars = ax.bar(counts.index.astype(str), counts.values, color="salmon", edgecolor="black")
        ax.set_title(f"Bar Chart of {selected_column}")
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency Count")
        plt.xticks(rotation=45, ha="right")

        for bar, pct in zip(bars, percentages):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    f"{pct}%", ha="center", va="bottom", fontsize=8)

        st.pyplot(fig)

else:
    st.info("Please upload a CSV file from the sidebar to begin analysis. "
            "(Use the titanic.csv dataset to test this app.)")