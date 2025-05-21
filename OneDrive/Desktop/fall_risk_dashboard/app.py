import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Fall Risk Prediction", layout="wide")
st.title("Fall Risk Prediction Dashboard")
st.markdown("Upload real patient data to analyze fall risk and generate personalized recommendations.")

# 📌 تعليمات البيانات
st.markdown("#### Required Data Format")
st.info("""
Upload a CSV or Excel file with the following columns:

| Column             | Description                                     |
|--------------------|-------------------------------------------------|
| Patient_ID         | Unique patient identifier                      |
| Age                | Patient's age in years                         |
| Mobility_Score     | 1 (low mobility) to 5 (full mobility)          |
| Medications_Count  | Number of medications taken                    |
| History_of_Falls   | 1 = yes, 0 = no                                |
| Fall_Risk          | 1 = high risk, 0 = low risk (actual label)     |

- `Fall_Risk` is required to train and evaluate the model.
""")

uploaded_file = st.file_uploader("Upload your patient data", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.markdown("### Preview")
    st.dataframe(df.head(), use_container_width=True)

    features = df.drop(columns=["Patient_ID", "Fall_Risk"])
    labels = df["Fall_Risk"]

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    df["Prediction"] = model.predict(features)
    df["Risk_Level"] = df["Prediction"].map({0: "Low", 1: "High"})

    accuracy = model.score(X_test, y_test)
    st.metric("Model Accuracy", f"{accuracy * 100:.2f}%")

    # 📊 Feature Importance Table
    st.write("### Feature Importance")
    importance_df = pd.DataFrame({
        "Feature": features.columns,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    st.dataframe(
        importance_df.style.format({"Importance": "{:.4f}"})
        .set_table_styles([
            {'selector': 'thead th', 'props': [('font-size', '12px')]},
            {'selector': 'td', 'props': [('font-size', '11px')]}
        ])
    )

    # 🖼️ الرسمات جنب بعض
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Fall Risk Distribution")
        risk_counts = df["Risk_Level"].value_counts()
        fig1, ax1 = plt.subplots(figsize=(2.5, 2.5))
        ax1.bar(risk_counts.index, risk_counts.values, width=0.4, color="#1f77b4")
        ax1.set_ylabel("Patients", fontsize=8)
        ax1.set_xlabel("Risk Level", fontsize=8)
        ax1.tick_params(axis='both', labelsize=8)
        ax1.set_title("")
        st.pyplot(fig1)

    with col2:
        st.write("#### Feature Importance Chart")
        fig2, ax2 = plt.subplots(figsize=(2.5, 2.5))
        ax2.barh(importance_df["Feature"], importance_df["Importance"], color="#2ca02c", height=0.4)
        ax2.set_xlabel("Importance", fontsize=8)
        ax2.tick_params(axis='y', labelsize=8)
        plt.tight_layout()
        st.pyplot(fig2)

    # 📄 توصيات
    st.write("### Patient Recommendations")

    def get_recommendation(risk):
        return "High risk: apply fall prevention protocol." if risk == "High" else "Low risk: routine monitoring."

    df["Recommendation"] = df["Risk_Level"].apply(get_recommendation)

    st.dataframe(df[["Patient_ID", "Risk_Level", "Recommendation"]], use_container_width=True)

    # ⬇️ تحميل النتائج
    st.write("### Download Results")
    output = df[["Patient_ID", "Age", "Mobility_Score", "Medications_Count", "History_of_Falls", "Risk_Level", "Recommendation"]]
    csv = output.to_csv(index=False).encode("utf-8")
    st.download_button("Download as CSV", data=csv, file_name="fall_risk_predictions.csv", mime="text/csv")
