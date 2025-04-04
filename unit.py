import streamlit as st
import pandas as pd
import plotly.express as px
from pint import UnitRegistry
from forex_python.converter import CurrencyRates, RatesNotAvailableError

# Initialize unit registry and currency API
ureg = UnitRegistry()
currency_api = CurrencyRates()

# Function to convert units
def convert_units(value, from_unit, to_unit, category):
    try:
        if category == "Currency":
            rate_from = currency_api.get_rate(from_unit, 'USD')
            rate_to = currency_api.get_rate(to_unit, 'USD')
            return value * (rate_to / rate_from)
        elif category == "Temperature":
            if from_unit == "celsius" and to_unit == "fahrenheit":
                return (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                return (value - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                return value + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                return value - 273.15
            elif from_unit == "fahrenheit" and to_unit == "kelvin":
                return (value - 32) * 5/9 + 273.15
            elif from_unit == "kelvin" and to_unit == "fahrenheit":
                return (value - 273.15) * 9/5 + 32
        else:
            return (value * ureg(from_unit)).to(to_unit).magnitude
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Unit Converter by Duaa Raza", page_icon="🔄", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
    <style>
        body {
            background-color: #F4F4F9;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #1DB954;
            color: white;
            border-radius: 8px;
            padding: 15px;
            font-size: 16px;
            border: none;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
        }
        .stButton>button:hover {
            background-color: #1ed760;
        }
        .stSelectbox>div>div {
            background-color: #F1F1F1;
            border-radius: 8px;
            font-size: 16px;
        }
        .stTitle {
            color: #4C4C6C;
            font-size: 32px;
            font-weight: bold;
            text-align: center;
        }
        .stSubheader {
            color: #3C3C3C;
            font-size: 24px;
            margin-top: 40px;
        }
        .stDataFrame {
            margin-top: 20px;
        }
        .stMarkdown {
            color: #2E2E2E;
            font-size: 14px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Centered title with custom style
st.markdown("<h1 style='text-align: center;'>🔄 <b> Unit Converter</b></h1>", unsafe_allow_html=True)

st.write("Convert units across multiple categories with ease. Perfect for everyday conversions.")

# Category selection
try:
    currency_units = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD"]
except Exception:
    currency_units = ["USD", "EUR", "GBP", "INR"]  # Fallback values

categories = {
    "Length": ["meter", "kilometer", "mile", "yard", "foot", "inch", "centimeter", "millimeter"],
    "Weight": ["kilogram", "gram", "pound", "ounce", "milligram", "ton"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Time": ["second", "minute", "hour", "day", "week", "month", "year"],
    "Currency": currency_units,
    "Area": ["square meter", "square kilometer", "square mile", "square yard", "square foot", "acre", "hectare"],
    "Volume": ["liter", "milliliter", "cubic meter", "cubic centimeter", "gallon", "quart", "pint", "cup"],
    "Speed": ["meter/second", "kilometer/hour", "mile/hour", "foot/second", "knot"],
    "Energy": ["joule", "kilojoule", "calorie", "kilocalorie", "watt hour", "kilowatt hour"],
    "Pressure": ["pascal", "bar", "psi", "atmosphere"],
    "Data": ["bit", "byte", "kilobyte", "megabyte", "gigabyte", "terabyte"]
}

category = st.selectbox("**Select Conversion Category**", list(categories.keys()))

# Input fields
col1, col2, col3 = st.columns(3)
with col1:
    value = st.number_input("**Enter Value**", min_value=0.0, format="%.4f")
with col2:
    from_unit = st.selectbox("**From Unit**", categories[category])
with col3:
    to_unit = st.selectbox("**To Unit**", categories[category])

# Conversion logic
if st.button("**Convert**", use_container_width=True, key="convert_button"):
    result = convert_units(value, from_unit, to_unit, category)
    st.success(f"**{value} {from_unit} = {result} {to_unit}**")

    # Conversion history
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({"Value": value, "From": from_unit, "To": to_unit, "Result": result})

# Display history with a sleek design
if "history" in st.session_state and st.session_state.history:
    st.subheader("**Conversion History**")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)
    
    fig = px.bar(df, x="From", y="Result", color="To", title="Conversion Data")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><br><p style='text-align: center;'>Made with ❤️ using Streamlit | Designed by Duaa Raza ❤️</p>", unsafe_allow_html=True)
