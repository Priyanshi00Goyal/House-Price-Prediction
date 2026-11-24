<<<<<<< HEAD

import os
import traceback
import joblib
import pandas as pd
import streamlit as st

from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Haven | House Price Predictor",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 2. PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "train.csv"
MODEL_PATH = BASE_DIR / "models" / "house_price_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"

# =========================================================
# 3. PREMIUM STYLING
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    :root {
        --cream: #F7F5EF;
        --green: #244C3A;
        --green-light: #E4EDE5;
        --ink: #202C26;
        --muted: #727B73;
        --border: #E2E4DA;
        --gold: #C69B58;
    }

    .stApp {
        background-color: var(--cream);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--green) !important;
    }

    [data-testid="stSidebar"] {
        background-color: #EDEFE7;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--ink);
    }

    .hero {
        background: linear-gradient(125deg, #214735, #41694F);
        padding: 42px 38px;
        border-radius: 22px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white !important;
        font-size: clamp(32px, 4vw, 48px);
        margin-bottom: 12px;
    }

    .hero p {
        color: #E4ECE5;
        font-size: 16px;
        line-height: 1.8;
        max-width: 680px;
    }

    .eyebrow {
        color: #D8BD88;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .section-label {
        color: var(--muted);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .feature-card {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 22px;
        min-height: 150px;
    }

    .feature-card h3 {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 16px;
        margin-bottom: 8px;
    }

    .feature-card p {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.7;
    }

    .metric-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 20px;
        min-height: 110px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 9px;
    }

    .metric-value {
        color: var(--green);
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        font-weight: 700;
    }

    .result-card {
        background: #E4EDE5;
        border: 1px solid #CADBCD;
        border-radius: 18px;
        padding: 28px;
        margin-top: 22px;
    }

    .result-label {
        color: #496552;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 12px;
        font-weight: 700;
    }

    .result-price {
        color: #214735;
        font-family: 'Playfair Display', serif;
        font-size: clamp(32px, 4vw, 46px);
        font-weight: 700;
        margin: 10px 0;
    }

    .small-note {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.7;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background: #244C3A;
        color: white;
        border: 1px solid #244C3A;
        border-radius: 10px;
        padding: 10px 22px;
        font-weight: 600;
        min-height: 44px;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background: #183626;
        color: white;
        border-color: #183626;
    }

    div[data-testid="stForm"] {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 22px;
    }

    .footer {
        text-align: center;
        color: var(--muted);
        font-size: 12px;
        padding: 30px 0 12px;
    }

    hr {
        border-color: var(--border);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 4. LOAD MODEL, PREPROCESSOR AND DATASET
# =========================================================

@st.cache_resource
def load_artifacts():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    if not PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(
            f"Preprocessor file not found: {PREPROCESSOR_PATH}"
        )

    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    return model, preprocessor


@st.cache_data
def load_dataset():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {DATA_PATH}"
        )

    return pd.read_csv(DATA_PATH)


try:
    model, preprocessor = load_artifacts()
    dataset = load_dataset()

except Exception as error:
    st.error("The application could not load its required files.")
    st.code(f"{type(error).__name__}: {error}")
    st.info(
        "Check that data/train.csv and both model files "
        "exist in their expected folders."
    )
    st.stop()


# =========================================================
# 5. NAVIGATION
# =========================================================

PAGES = [
    "Overview",
    "Price Estimator",
    "About the Model",
]


def go_to_estimator():
    # Streamlit runs this callback before rerunning the script.
    # Therefore, changing the radio's state here is safe.
    st.session_state.page_navigation = "Price Estimator"


if "page_navigation" not in st.session_state:
    st.session_state.page_navigation = "Overview"


with st.sidebar:
    st.markdown(
        """
        <div style="padding: 12px 0 24px;">
            <div style="font-size: 30px;">⌂</div>
            <div style="font-family: 'Playfair Display', serif;
                        font-size: 27px; font-weight: 700;
                        color: #244C3A;">
                Haven
            </div>
            <div style="font-size: 11px; letter-spacing: 2px;
                        color: #727B73;">
                PROPERTY INTELLIGENCE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("##### NAVIGATION")

    page = st.radio(
        "Choose a page",
        PAGES,
        key="page_navigation",
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("##### MODEL SNAPSHOT")
    st.caption("Algorithm: Random Forest Regressor")
    st.caption("Task: House price regression")
    st.caption("Training records: 80,000")

    st.markdown("---")
    st.markdown(
        """
        <div class="small-note">
        Built with Python, Pandas, Scikit-learn and Streamlit.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 6. OVERVIEW PAGE
# =========================================================

if page == "Overview":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">SMART PROPERTY ESTIMATION</div>
            <h1>Find the value<br>behind every address.</h1>
            <p>
                Explore estimated property prices using a machine
                learning model trained on housing data. Enter property
                details to get an estimate in Indian rupees.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">THE EXPERIENCE</div>',
        unsafe_allow_html=True,
    )

    st.markdown("## Property insights, made simpler")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="feature-card">
                <div style="font-size:27px;">⌂</div>
                <h3>Property details</h3>
                <p>
                    Enter location, property type, size, age,
                    furnishing and other property characteristics.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="feature-card">
                <div style="font-size:27px;">↗</div>
                <h3>Machine learning</h3>
                <p>
                    A trained Random Forest regression model uses
                    property features to estimate a price.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="feature-card">
                <div style="font-size:27px;">₹</div>
                <h3>Price estimate</h3>
                <p>
                    Receive an estimated property value in lakhs
                    of Indian rupees.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown("### Ready to estimate a property?")

    st.button(
        "Explore the Price Estimator →",
        on_click=go_to_estimator,
        key="overview_estimator_button",
    )

    st.markdown("---")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Training dataset</div>
                <div class="metric-value">80,000</div>
                <div class="small-note">Property records</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Selected model</div>
                <div class="metric-value">Random Forest</div>
                <div class="small-note">Regression algorithm</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Model R² score</div>
                <div class="metric-value">78.50%</div>
                <div class="small-note">
                    Evaluation result on the held-out test set
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# 7. PRICE ESTIMATOR PAGE
# =========================================================

elif page == "Price Estimator":

    st.markdown(
        '<div class="section-label">PERSONALIZED ESTIMATION</div>',
        unsafe_allow_html=True,
    )

    st.title("Estimate your property's value")
    st.write(
        "Fill in the details below. The model will use these "
        "features to estimate the property's price."
    )

    # Get categories from the actual dataset so the input values
    # match the categories used during model training.
    def get_options(column):
        values = dataset[column].dropna().unique().tolist()
        return sorted(values, key=lambda value: str(value))

    city_options = get_options("City")
    locality_options = get_options("Locality_Type")
    property_options = get_options("Property_Type")
    furnishing_options = get_options("Furnishing_Status")
    parking_options = get_options("Parking")
    lift_options = get_options("Lift_Available")
    gated_options = get_options("Gated_Community")

    # Preserve the original raw feature order expected by the
    # saved preprocessing pipeline.
    expected_columns = list(preprocessor.feature_names_in_)

    with st.form("property_prediction_form"):

        st.markdown("### 01 — Location and property")

        col1, col2 = st.columns(2)

        with col1:
            city = st.selectbox("City", city_options)
            locality = st.selectbox(
                "Locality category", locality_options
            )
            property_type = st.selectbox(
                "Property type", property_options
            )
            bhk = st.number_input(
                "Number of bedrooms (BHK)",
                min_value=1,
                max_value=20,
                value=2,
                step=1,
            )
            bathrooms = st.number_input(
                "Number of bathrooms",
                min_value=1,
                max_value=20,
                value=2,
                step=1,
            )

        with col2:
            furnishing = st.selectbox(
                "Furnishing status", furnishing_options
            )
            age = st.number_input(
                "Property age (years)",
                min_value=0,
                max_value=200,
                value=5,
                step=1,
            )
            parking = st.selectbox(
                "Parking available (0 = No, 1 = Yes)",
                parking_options,
            )
            lift = st.selectbox(
                "Lift available (0 = No, 1 = Yes)",
                lift_options,
            )
            gated = st.selectbox(
                "Gated community (0 = No, 1 = Yes)",
                gated_options,
            )

        st.markdown("---")
        st.markdown("### 02 — Size and building details")

        col3, col4 = st.columns(2)

        with col3:
            super_area = st.number_input(
                "Super area (sq. ft.)",
                min_value=50.0,
                max_value=100000.0,
                value=1200.0,
                step=50.0,
            )
            carpet_area = st.number_input(
                "Carpet area (sq. ft.)",
                min_value=30.0,
                max_value=100000.0,
                value=900.0,
                step=50.0,
            )
            floor_number = st.number_input(
                "Floor number",
                min_value=0,
                max_value=200,
                value=2,
                step=1,
            )

        with col4:
            total_floors = st.number_input(
                "Total floors in building",
                min_value=1,
                max_value=200,
                value=5,
                step=1,
            )
            metro_distance = st.number_input(
                "Distance to metro (km)",
                min_value=0.0,
                max_value=500.0,
                value=2.0,
                step=0.5,
            )
            city_distance = st.number_input(
                "Distance to city centre (km)",
                min_value=0.0,
                max_value=500.0,
                value=5.0,
                step=0.5,
            )

        st.markdown("")
        submitted = st.form_submit_button(
            "Calculate Estimated Price",
            use_container_width=True,
        )

    if submitted:

        # Basic consistency checks
        if carpet_area > super_area:
            st.warning(
                "Carpet area is larger than super area. "
                "Please check the measurements."
            )

        elif floor_number > total_floors:
            st.warning(
                "The floor number cannot exceed the total "
                "number of floors."
            )

        else:
            # Build the input with the same raw feature names
            # used during model training.
            input_data = {
                "City": city,
                "Locality_Type": locality,
                "Property_Type": property_type,
                "BHK": int(bhk),
                "Bathrooms": int(bathrooms),
                "Super_Area_SqFt": float(super_area),
                "Carpet_Area_SqFt": float(carpet_area),
                "Floor_Number": int(floor_number),
                "Total_Floors": int(total_floors),
                "Age_of_Property": int(age),
                "Furnishing_Status": furnishing,
                "Parking": parking,
                "Lift_Available": lift,
                "Gated_Community": gated,
                "Distance_to_Metro_km": float(metro_distance),
                "Distance_to_City_Center_km": float(city_distance),
            }

            input_df = pd.DataFrame([input_data])

            # Match the exact raw feature names and order.
            input_df = input_df[expected_columns]

            try:
                with st.spinner(
                    "Analysing property features..."
                ):
                    # Transform the raw input before prediction.
                    transformed_input = preprocessor.transform(
                        input_df
                    )

                    prediction = float(
                        model.predict(transformed_input)[0]
                    )

                if not pd.notna(prediction):
                    raise ValueError(
                        "The model returned an invalid prediction."
                    )

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">
                            Estimated property value
                        </div>
                        <div class="result-price">
                            ₹ {prediction:,.2f} Lakhs
                        </div>
                        <div style="color:#496552; font-size:14px;">
                            Approximately ₹ {prediction * 100000:,.0f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.caption(
                    "This is a machine learning estimate, not a "
                    "verified market valuation or an offer to buy "
                    "or sell the property. Actual prices can vary."
                )

                with st.expander(
                    "View the property details used for prediction"
                ):
                    st.dataframe(
                        input_df,
                        use_container_width=True,
                        hide_index=True,
                    )

            except Exception as error:
                st.error(
                    f"Prediction failed: {type(error).__name__}"
                )
                st.code(str(error))

                with st.expander("Technical details"):
                    st.code(traceback.format_exc())


# =========================================================
# 8. ABOUT THE MODEL PAGE
# =========================================================

elif page == "About the Model":

    st.markdown(
        '<div class="section-label">BEHIND THE PREDICTION</div>',
        unsafe_allow_html=True,
    )

    st.title("About the machine learning model")

    st.write(
        "This project compares several regression algorithms "
        "for estimating residential property prices."
    )

    st.markdown("### Final model evaluation")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">R² score</div>
                <div class="metric-value">0.7850</div>
                <div class="small-note">
                    About 78.50% of target variance explained
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Mean Absolute Error</div>
                <div class="metric-value">₹33.05 L</div>
                <div class="small-note">
                    Average absolute prediction error
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Root Mean Squared Error</div>
                <div class="metric-value">₹68.99 L</div>
                <div class="small-note">
                    Penalizes larger prediction errors more heavily
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### Model comparison")

    comparison_path = BASE_DIR / "models" / "final_model_comparison.csv"

    if comparison_path.exists():
        try:
            comparison = pd.read_csv(comparison_path)

            st.dataframe(
                comparison,
                use_container_width=True,
                hide_index=True,
            )

        except Exception as error:
            st.warning(
                f"Could not read model comparison: {error}"
            )
    else:
        st.info(
            "The model comparison CSV is not available. "
            "The evaluation metrics above are from the saved "
            "final model evaluation."
        )

    st.markdown("---")
    st.markdown("### How a prediction works")

    st.markdown(
        """
        1. **Collect property details:** location, size, property type,
           furnishing, age and accessibility features.
        2. **Preprocess the input:** the saved preprocessing pipeline
           handles categorical and numerical features.
        3. **Generate a prediction:** the trained Random Forest
           Regressor estimates the price.
        4. **Display the result:** the predicted value is shown in
           lakhs of Indian rupees.
        """
    )

    st.markdown("### Important limitations")

    st.markdown(
        """
        - Predictions depend on the quality and coverage of the
          training dataset.
        - The model may not capture every local market change or
          unique property characteristic.
        - The estimate should not replace a professional property
          valuation.
        """
    )


# =========================================================
# 9. FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        HAVEN · HOUSE PRICE PREDICTION<br>
        Built with Python, Pandas, Scikit-learn and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
=======

import os
import traceback
import joblib
import pandas as pd
import streamlit as st

from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Haven | House Price Predictor",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 2. PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "train.csv"
MODEL_PATH = BASE_DIR / "models" / "house_price_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"

# =========================================================
# 3. PREMIUM STYLING
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    :root {
        --cream: #F7F5EF;
        --green: #244C3A;
        --green-light: #E4EDE5;
        --ink: #202C26;
        --muted: #727B73;
        --border: #E2E4DA;
        --gold: #C69B58;
    }

    .stApp {
        background-color: var(--cream);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--green) !important;
    }

    [data-testid="stSidebar"] {
        background-color: #EDEFE7;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--ink);
    }

    .hero {
        background: linear-gradient(125deg, #214735, #41694F);
        padding: 42px 38px;
        border-radius: 22px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white !important;
        font-size: clamp(32px, 4vw, 48px);
        margin-bottom: 12px;
    }

    .hero p {
        color: #E4ECE5;
        font-size: 16px;
        line-height: 1.8;
        max-width: 680px;
    }

    .eyebrow {
        color: #D8BD88;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .section-label {
        color: var(--muted);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .feature-card {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 22px;
        min-height: 150px;
    }

    .feature-card h3 {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 16px;
        margin-bottom: 8px;
    }

    .feature-card p {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.7;
    }

    .metric-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 20px;
        min-height: 110px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 9px;
    }

    .metric-value {
        color: var(--green);
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        font-weight: 700;
    }

    .result-card {
        background: #E4EDE5;
        border: 1px solid #CADBCD;
        border-radius: 18px;
        padding: 28px;
        margin-top: 22px;
    }

    .result-label {
        color: #496552;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 12px;
        font-weight: 700;
    }

    .result-price {
        color: #214735;
        font-family: 'Playfair Display', serif;
        font-size: clamp(32px, 4vw, 46px);
        font-weight: 700;
        margin: 10px 0;
    }

    .small-note {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.7;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background: #244C3A;
        color: white;
        border: 1px solid #244C3A;
        border-radius: 10px;
        padding: 10px 22px;
        font-weight: 600;
        min-height: 44px;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background: #183626;
        color: white;
        border-color: #183626;
    }

    div[data-testid="stForm"] {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 22px;
    }

    .footer {
        text-align: center;
        color: var(--muted);
        font-size: 12px;
        padding: 30px 0 12px;
    }

    hr {
        border-color: var(--border);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 4. LOAD MODEL, PREPROCESSOR AND DATASET
# =========================================================

@st.cache_resource
def load_artifacts():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    if not PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(
            f"Preprocessor file not found: {PREPROCESSOR_PATH}"
        )

    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    return model, preprocessor


@st.cache_data
def load_dataset():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {DATA_PATH}"
        )

    return pd.read_csv(DATA_PATH)


try:
    model, preprocessor = load_artifacts()
    dataset = load_dataset()

except Exception as error:
    st.error("The application could not load its required files.")
    st.code(f"{type(error).__name__}: {error}")
    st.info(
        "Check that data/train.csv and both model files "
        "exist in their expected folders."
    )
    st.stop()


# =========================================================
# 5. NAVIGATION
# =========================================================

PAGES = [
    "Overview",
    "Price Estimator",
    "About the Model",
]


def go_to_estimator():
    # Streamlit runs this callback before rerunning the script.
    # Therefore, changing the radio's state here is safe.
    st.session_state.page_navigation = "Price Estimator"


if "page_navigation" not in st.session_state:
    st.session_state.page_navigation = "Overview"


with st.sidebar:
    st.markdown(
        """
        <div style="padding: 12px 0 24px;">
            <div style="font-size: 30px;">⌂</div>
            <div style="font-family: 'Playfair Display', serif;
                        font-size: 27px; font-weight: 700;
                        color: #244C3A;">
                Haven
            </div>
            <div style="font-size: 11px; letter-spacing: 2px;
                        color: #727B73;">
                PROPERTY INTELLIGENCE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("##### NAVIGATION")

    page = st.radio(
        "Choose a page",
        PAGES,
        key="page_navigation",
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("##### MODEL SNAPSHOT")
    st.caption("Algorithm: Random Forest Regressor")
    st.caption("Task: House price regression")
    st.caption("Training records: 80,000")

    st.markdown("---")
    st.markdown(
        """
        <div class="small-note">
        Built with Python, Pandas, Scikit-learn and Streamlit.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 6. OVERVIEW PAGE
# =========================================================

if page == "Overview":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">SMART PROPERTY ESTIMATION</div>
            <h1>Find the value<br>behind every address.</h1>
            <p>
                Explore estimated property prices using a machine
                learning model trained on housing data. Enter property
                details to get an estimate in Indian rupees.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">THE EXPERIENCE</div>',
        unsafe_allow_html=True,
    )

    st.markdown("## Property insights, made simpler")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="feature-card">
                <div style="font-size:27px;">⌂</div>
                <h3>Property details</h3>
                <p>
                    Enter location, property type, size, age,
                    furnishing and other property characteristics.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="feature-card">
                <div style="font-size:27px;">↗</div>
                <h3>Machine learning</h3>
                <p>
                    A trained Random Forest regression model uses
                    property features to estimate a price.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="feature-card">
                <div style="font-size:27px;">₹</div>
                <h3>Price estimate</h3>
                <p>
                    Receive an estimated property value in lakhs
                    of Indian rupees.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown("### Ready to estimate a property?")

    st.button(
        "Explore the Price Estimator →",
        on_click=go_to_estimator,
        key="overview_estimator_button",
    )

    st.markdown("---")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Training dataset</div>
                <div class="metric-value">80,000</div>
                <div class="small-note">Property records</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Selected model</div>
                <div class="metric-value">Random Forest</div>
                <div class="small-note">Regression algorithm</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Model R² score</div>
                <div class="metric-value">78.50%</div>
                <div class="small-note">
                    Evaluation result on the held-out test set
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# 7. PRICE ESTIMATOR PAGE
# =========================================================

elif page == "Price Estimator":

    st.markdown(
        '<div class="section-label">PERSONALIZED ESTIMATION</div>',
        unsafe_allow_html=True,
    )

    st.title("Estimate your property's value")
    st.write(
        "Fill in the details below. The model will use these "
        "features to estimate the property's price."
    )

    # Get categories from the actual dataset so the input values
    # match the categories used during model training.
    def get_options(column):
        values = dataset[column].dropna().unique().tolist()
        return sorted(values, key=lambda value: str(value))

    city_options = get_options("City")
    locality_options = get_options("Locality_Type")
    property_options = get_options("Property_Type")
    furnishing_options = get_options("Furnishing_Status")
    parking_options = get_options("Parking")
    lift_options = get_options("Lift_Available")
    gated_options = get_options("Gated_Community")

    # Preserve the original raw feature order expected by the
    # saved preprocessing pipeline.
    expected_columns = list(preprocessor.feature_names_in_)

    with st.form("property_prediction_form"):

        st.markdown("### 01 — Location and property")

        col1, col2 = st.columns(2)

        with col1:
            city = st.selectbox("City", city_options)
            locality = st.selectbox(
                "Locality category", locality_options
            )
            property_type = st.selectbox(
                "Property type", property_options
            )
            bhk = st.number_input(
                "Number of bedrooms (BHK)",
                min_value=1,
                max_value=20,
                value=2,
                step=1,
            )
            bathrooms = st.number_input(
                "Number of bathrooms",
                min_value=1,
                max_value=20,
                value=2,
                step=1,
            )

        with col2:
            furnishing = st.selectbox(
                "Furnishing status", furnishing_options
            )
            age = st.number_input(
                "Property age (years)",
                min_value=0,
                max_value=200,
                value=5,
                step=1,
            )
            parking = st.selectbox(
                "Parking available (0 = No, 1 = Yes)",
                parking_options,
            )
            lift = st.selectbox(
                "Lift available (0 = No, 1 = Yes)",
                lift_options,
            )
            gated = st.selectbox(
                "Gated community (0 = No, 1 = Yes)",
                gated_options,
            )

        st.markdown("---")
        st.markdown("### 02 — Size and building details")

        col3, col4 = st.columns(2)

        with col3:
            super_area = st.number_input(
                "Super area (sq. ft.)",
                min_value=50.0,
                max_value=100000.0,
                value=1200.0,
                step=50.0,
            )
            carpet_area = st.number_input(
                "Carpet area (sq. ft.)",
                min_value=30.0,
                max_value=100000.0,
                value=900.0,
                step=50.0,
            )
            floor_number = st.number_input(
                "Floor number",
                min_value=0,
                max_value=200,
                value=2,
                step=1,
            )

        with col4:
            total_floors = st.number_input(
                "Total floors in building",
                min_value=1,
                max_value=200,
                value=5,
                step=1,
            )
            metro_distance = st.number_input(
                "Distance to metro (km)",
                min_value=0.0,
                max_value=500.0,
                value=2.0,
                step=0.5,
            )
            city_distance = st.number_input(
                "Distance to city centre (km)",
                min_value=0.0,
                max_value=500.0,
                value=5.0,
                step=0.5,
            )

        st.markdown("")
        submitted = st.form_submit_button(
            "Calculate Estimated Price",
            use_container_width=True,
        )

    if submitted:

        # Basic consistency checks
        if carpet_area > super_area:
            st.warning(
                "Carpet area is larger than super area. "
                "Please check the measurements."
            )

        elif floor_number > total_floors:
            st.warning(
                "The floor number cannot exceed the total "
                "number of floors."
            )

        else:
            # Build the input with the same raw feature names
            # used during model training.
            input_data = {
                "City": city,
                "Locality_Type": locality,
                "Property_Type": property_type,
                "BHK": int(bhk),
                "Bathrooms": int(bathrooms),
                "Super_Area_SqFt": float(super_area),
                "Carpet_Area_SqFt": float(carpet_area),
                "Floor_Number": int(floor_number),
                "Total_Floors": int(total_floors),
                "Age_of_Property": int(age),
                "Furnishing_Status": furnishing,
                "Parking": parking,
                "Lift_Available": lift,
                "Gated_Community": gated,
                "Distance_to_Metro_km": float(metro_distance),
                "Distance_to_City_Center_km": float(city_distance),
            }

            input_df = pd.DataFrame([input_data])

            # Match the exact raw feature names and order.
            input_df = input_df[expected_columns]

            try:
                with st.spinner(
                    "Analysing property features..."
                ):
                    # Transform the raw input before prediction.
                    transformed_input = preprocessor.transform(
                        input_df
                    )

                    prediction = float(
                        model.predict(transformed_input)[0]
                    )

                if not pd.notna(prediction):
                    raise ValueError(
                        "The model returned an invalid prediction."
                    )

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">
                            Estimated property value
                        </div>
                        <div class="result-price">
                            ₹ {prediction:,.2f} Lakhs
                        </div>
                        <div style="color:#496552; font-size:14px;">
                            Approximately ₹ {prediction * 100000:,.0f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.caption(
                    "This is a machine learning estimate, not a "
                    "verified market valuation or an offer to buy "
                    "or sell the property. Actual prices can vary."
                )

                with st.expander(
                    "View the property details used for prediction"
                ):
                    st.dataframe(
                        input_df,
                        use_container_width=True,
                        hide_index=True,
                    )

            except Exception as error:
                st.error(
                    f"Prediction failed: {type(error).__name__}"
                )
                st.code(str(error))

                with st.expander("Technical details"):
                    st.code(traceback.format_exc())


# =========================================================
# 8. ABOUT THE MODEL PAGE
# =========================================================

elif page == "About the Model":

    st.markdown(
        '<div class="section-label">BEHIND THE PREDICTION</div>',
        unsafe_allow_html=True,
    )

    st.title("About the machine learning model")

    st.write(
        "This project compares several regression algorithms "
        "for estimating residential property prices."
    )

    st.markdown("### Final model evaluation")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">R² score</div>
                <div class="metric-value">0.7850</div>
                <div class="small-note">
                    About 78.50% of target variance explained
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Mean Absolute Error</div>
                <div class="metric-value">₹33.05 L</div>
                <div class="small-note">
                    Average absolute prediction error
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Root Mean Squared Error</div>
                <div class="metric-value">₹68.99 L</div>
                <div class="small-note">
                    Penalizes larger prediction errors more heavily
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### Model comparison")

    comparison_path = BASE_DIR / "models" / "final_model_comparison.csv"

    if comparison_path.exists():
        try:
            comparison = pd.read_csv(comparison_path)

            st.dataframe(
                comparison,
                use_container_width=True,
                hide_index=True,
            )

        except Exception as error:
            st.warning(
                f"Could not read model comparison: {error}"
            )
    else:
        st.info(
            "The model comparison CSV is not available. "
            "The evaluation metrics above are from the saved "
            "final model evaluation."
        )

    st.markdown("---")
    st.markdown("### How a prediction works")

    st.markdown(
        """
        1. **Collect property details:** location, size, property type,
           furnishing, age and accessibility features.
        2. **Preprocess the input:** the saved preprocessing pipeline
           handles categorical and numerical features.
        3. **Generate a prediction:** the trained Random Forest
           Regressor estimates the price.
        4. **Display the result:** the predicted value is shown in
           lakhs of Indian rupees.
        """
    )

    st.markdown("### Important limitations")

    st.markdown(
        """
        - Predictions depend on the quality and coverage of the
          training dataset.
        - The model may not capture every local market change or
          unique property characteristic.
        - The estimate should not replace a professional property
          valuation.
        """
    )


# =========================================================
# 9. FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        HAVEN · HOUSE PRICE PREDICTION<br>
        Built with Python, Pandas, Scikit-learn and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
>>>>>>> 398e28e (Prepare House Price Prediction app for deployment)
