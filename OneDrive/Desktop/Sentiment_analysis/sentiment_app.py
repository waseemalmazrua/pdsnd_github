import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="Sentiment Analyzer", layout="centered")

st.title("Sentiment Analysis App with VADER")
st.write("Upload a CSV or Excel file with a column containing text data (e.g., reviews, comments, etc.)")

# رفع الملف - يقبل csv أو xlsx
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format.")
        st.stop()

    st.subheader("Preview of your data:")
    st.dataframe(df.head())

    # اختيار العمود النصي
    text_column = st.selectbox("Select the column with text:", df.columns)

    # تحليل المشاعر باستخدام VADER
    analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(text):
        score = analyzer.polarity_scores(str(text))["compound"]
        if score >= 0.05:
            return "Positive"
        elif score <= -0.05:
            return "Negative"
        else:
            return "Neutral"

    if st.button("Run Sentiment Analysis"):
        df["Sentiment"] = df[text_column].apply(analyze_sentiment)
        st.success("Sentiment analysis complete!")
        st.subheader("Results:")
        st.dataframe(df)

        # رسم بياني
        sentiment_counts = df["Sentiment"].value_counts()
        st.subheader("Sentiment Distribution:")
        st.bar_chart(sentiment_counts)

        # تحميل النتيجة
        result_csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Results as CSV",
            result_csv,
            "sentiment_results.csv",
            "text/csv"
        )

# توقيع شخصي
st.markdown(
    """
    <div style='text-align: right; font-size: 12px; color: gray; padding-top: 30px;'>
        Made by: <b>Waseem Almazrua</b> |
        <a href='https://www.linkedin.com/in/waseemalmazrua' target='_blank' style='color: gray; text-decoration: none;'>
            LinkedIn
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
