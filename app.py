import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('best_random_forest_model.pkl')

# Sidebar menu
st.sidebar.title("🚢 Titanic Survival Prediction App")
menu = st.sidebar.radio("🧭 Navigation", ["🏠 Home", "📝 Individual Prediction", "📊 Batch Prediction", "ℹ️ About the App"])

# Style for larger fonts and bold text
st.markdown("""
    <style>
    .big-font {
        font-size:24px !important;
        font-weight: bold;
    }
    .sub-title {
        font-size:20px !important;
        font-weight: bold;
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

if menu == "🏠 Home":
    st.markdown("<h1 style='text-align: center;'>Welcome to the Titanic Survival Prediction App 🚢</h1>", unsafe_allow_html=True)
    st.markdown("<h1 class='big-font>🌟 Welcome to the Titanic Survival Prediction App 🌟</h1>", unsafe_allow_html=True)
    st.write("🚢 **Explore the Titanic disaster through data-driven insights!**")
    st.write("📝 **This web application predicts whether a passenger would have survived or not based on various features such as Pclass, Sex, Age, Fare, and more.**")
    st.write("🔍 **Get instant predictions for individual passengers or upload a CSV file for batch processing.**")
    st.write("📊 **Visualize how different features influence survival chances and learn about the Titanic dataset.**")
    st.write("🎯 Whether you're a student, researcher, Titanic enthusiast, or just curious, this app makes exploring Titanic data interactive and fun!")
    st.write("👉 **Navigate through the menu on the left to get started.**")
    st.write("🛠️ **Enjoy analyzing and predicting!**")
    
elif menu == "ℹ️ About the App":
    st.markdown("<h2 style='text-align: center;'>ℹ️ About the Titanic Survival Prediction App</h2>", unsafe_allow_html=True)
    st.write("""
        🚢 **Welcome to the Titanic Survival Prediction App!** This innovative tool leverages machine learning to analyze passenger data and predict their chances of survival during the tragic sinking of the Titanic.
        
        🔍 **How does it work?**  
        The app uses a trained **Random Forest Classifier** — a powerful ensemble learning method — to evaluate various passenger features such as Pclass, Sex, Age, Fare, and more. Depending on these inputs, it provides an instant prediction of whether a passenger would likely have survived or not.

        🎯 **Key Features:**  
        - Easy-to-use interface for both individual and batch predictions.  
        - Supports multiple input formats for flexible usage.  
        - Visual summaries and download options for your prediction data.

        📚 **Educational & Fun:**  
        Whether you're a student studying, a Titanic enthusiast, or just curious, this app offers a great way to learn how different factors influence survival outcomes. Experiment with various data points to see how predictions change!

        🌟 **Why use this app?**  
        - Quick, accurate predictions based on historical data.  
        - Improve your understanding of feature importance in machine learning models.  
        - Share your insights by downloading the prediction results.

        🧑‍💻 **Built with love and machine learning!**  
        The app is built with Python, Streamlit for web deployment, and scikit-learn for modeling — making it accessible, interactive, and fun to explore!

        💬 **Have questions or suggestions?**  
        Feel free to reach out or explore more Titanic history and data analysis. Happy exploring! 🚀
        """)

elif menu == "📝 Individual Prediction":
    st.markdown("<h2 style='text-align: center;'>🧍‍♂️ Individual Prediction</h2>", unsafe_allow_html=True)
    Pclass = st.selectbox("🛳️ Passenger Class (Pclass)", options=[1, 2, 3], index=0)
    sex_str = st.selectbox("🧑 Sex", options=["male", "female"])
    Sex = 1 if sex_str == "male" else 0
    Age = st.number_input("🎂 Age", min_value=0.0, max_value=100.0, step=0.5, value=30.0)
    SibSp = st.number_input("👨‍👩‍👧 Siblings/Spouses Aboard (SibSp)", min_value=0, max_value=10, value=0)
    Parch = st.number_input("🧓 Parents/Children Aboard (Parch)", min_value=0, max_value=10, value=0)
    Fare = st.number_input("💰 Ticket Fare", min_value=0.0, max_value=500.0, step=0.5, value=20.0)
    # Hidden Embarked with default value
    Embarked = 0  # default to 'S'

    if st.button("🚀 Predict"):
        input_df = pd.DataFrame([{
            'Pclass': Pclass,
            'Sex': Sex,
            'Age': Age,
            'SibSp': SibSp,
            'Parch': Parch,
            'Fare': Fare,
            'Embarked': Embarked
        }])
        pred = model.predict(input_df)[0]
        result_text = "🎉 Survived" if pred == 1 else "💥 Did not survive"
        st.success(f"📝 Prediction: **{result_text}**")

elif menu == "📊 Batch Prediction":
    st.markdown("<h2 style='text-align: center;'>🌐 Batch Prediction</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📁 Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error("🚫 The uploaded CSV file is empty. Please upload a valid file.")
        else:
            # Check required columns
            required_cols = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                st.error(f"❗ Missing columns: {', '.join(missing_cols)}")
            else:
                # Encode categorical variables
                df['Sex'] = df['Sex'].map({'male': 1, 'female': 0}).fillna(0)
                df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2}).fillna(0)

                # Identify rows with complete data
                complete_mask = df[required_cols].notnull().all(axis=1)

                # Separate complete and incomplete data
                df_complete = df[complete_mask].copy()
                df_incomplete = df[~complete_mask].copy()

                # Impute missing values in incomplete data with better strategies if needed
                # For simplicity, fill with median or default
                for col in ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']:
                    if df_incomplete[col].isnull().any():
                        median_value = df_incomplete[col].median()
                        df_incomplete[col].fillna(median_value, inplace=True)

                # Make predictions only on complete data
                predictions_complete = model.predict(df_complete[required_cols])
                df_complete['🎯 Survival Status'] = ['🎉 Survived' if p == 1 else '💥 Did not survive' for p in predictions_complete]
                df_complete['🔢 Survival Code'] = predictions_complete

                # For incomplete data, optionally predict after imputation or leave as is
                # Here, we predict after filling missing values
                if not df_incomplete.empty:
                    predictions_incomplete = model.predict(df_incomplete[required_cols])
                    df_incomplete['🎯 Survival Status'] = ['🎉 Survived' if p == 1 else '💥 Did not survive' for p in predictions_incomplete]
                    df_incomplete['🔢 Survival Code'] = predictions_incomplete

                # Combine results
                output_df = pd.concat([df_complete, df_incomplete], axis=0).sort_index()

                # Select output columns
                output_df = output_df[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', '🎯 Survival Status', '🔢 Survival Code']]

                # Download predictions
                csv_bytes = output_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 Download Predictions CSV",
                    data=csv_bytes,
                    file_name="predictions_output.csv",
                    mime="text/csv"
                )
                st.success(f"✅ Prediction completed for {len(df)} rows. Note: Predictions on incomplete data are based on imputed values.")