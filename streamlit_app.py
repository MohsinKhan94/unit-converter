import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration - first Streamlit command
st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    layout="wide"
)

# Include CSS for styling
st.markdown("""
<style>
    /* Base styles */
    .main {
        background-color: #f0f2f6;
        transition: background-color 0.3s ease;
    }
    
    /* Header styling */
    .app-header {
        border-bottom: 1px solid rgba(0, 105, 204, 0.2);
        margin-bottom: 2rem;
        padding-bottom: 1rem;
    }
    
    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0066cc 0%, #00aaff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .badge {
        background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-left: 10px;
        display: inline-block;
    }
    
    /* Common styles for headings */
    h1, h2, h3, h4, h5, h6 {
        color: #0066cc;
        transition: color 0.3s ease;
    }
    
    /* Cards */
    .converter-card, .card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 105, 204, 0.1);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    /* Result display */
    .result-card {
        background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0, 105, 204, 0.3);
        text-align: center;
        display: block;
        clear: both;
    }
    
    .result-value {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .formula {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        font-style: italic;
        margin-top: 5px;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
        color: white;
        font-weight: 500;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    /* Table styling */
    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    
    th {
        background: linear-gradient(135deg, #f0f2f6 0%, #e4e8f0 100%);
        color: #0066cc;
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
    }
    
    td {
        padding: 10px 15px;
        border-bottom: 1px solid #eee;
    }
    
    tr:last-child td {
        border-bottom: none;
    }
    
    tr:nth-child(even) {
        background-color: rgba(240, 242, 246, 0.5);
    }
    
    /* Footer */
    footer {
        margin-top: 3rem;
        text-align: center;
        color: #666;
        font-size: 0.8rem;
    }
    
    /* Dark mode */
    .dark-mode {
        background-color: #121212 !important;
    }
    
    .dark-mode h1, .dark-mode h2, .dark-mode h3 {
        color: #00aaff !important;
    }
    
    .dark-mode p, .dark-mode span, .dark-mode div {
        color: #f0f0f0 !important;
    }
    
    .dark-mode .card, .dark-mode .converter-card {
        background: rgba(30, 30, 46, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom header
st.markdown("""
<div class="app-header">
  <span class="app-title">Unit Converter</span>
  <span class="badge">Simple</span>
  <span class="badge">Reliable</span>
</div>
""", unsafe_allow_html=True)

# Conversion categories and units
categories = {
    "Length": {
        "Meter": 1,
        "Kilometer": 0.001,
        "Centimeter": 100,
        "Millimeter": 1000,
        "Mile": 0.000621371,
        "Yard": 1.09361,
        "Foot": 3.28084,
        "Inch": 39.3701
    },
    "Weight/Mass": {
        "Kilogram": 1,
        "Gram": 1000,
        "Milligram": 1000000,
        "Metric Ton": 0.001,
        "Pound": 2.20462,
        "Ounce": 35.274
    },
    "Temperature": {
        "Celsius": "base",
        "Fahrenheit": "derived",
        "Kelvin": "derived"
    },
    "Area": {
        "Square Meter": 1,
        "Square Kilometer": 0.000001,
        "Square Centimeter": 10000,
        "Square Mile": 3.861e-7,
        "Square Yard": 1.19599,
        "Square Foot": 10.7639,
        "Acre": 0.000247105
    },
    "Volume": {
        "Cubic Meter": 1,
        "Liter": 1000,
        "Milliliter": 1000000,
        "Gallon (US)": 264.172,
        "Quart (US)": 1056.69,
        "Pint (US)": 2113.38,
        "Cup (US)": 4226.75
    },
    "Time": {
        "Second": 1,
        "Millisecond": 1000,
        "Minute": 1/60,
        "Hour": 1/3600,
        "Day": 1/86400,
        "Week": 1/604800,
        "Month (30 days)": 1/2592000,
        "Year (365 days)": 1/31536000
    },
    "Speed": {
        "Meter per second": 1,
        "Kilometer per hour": 3.6,
        "Mile per hour": 2.23694,
        "Foot per second": 3.28084,
        "Knot": 1.94384
    },
    "Data": {
        "Byte": 1,
        "Kilobyte": 1/1024,
        "Megabyte": 1/(1024**2),
        "Gigabyte": 1/(1024**3),
        "Terabyte": 1/(1024**4)
    }
}

# Category icons
category_icons = {
    "Length": "📏",
    "Weight/Mass": "⚖️",
    "Temperature": "🌡️",
    "Area": "📐",
    "Volume": "🧪",
    "Time": "⏱️",
    "Speed": "🚀",
    "Data": "💾"
}

# Temperature conversion functions
def convert_temperature(value, from_unit, to_unit):
    # Convert to Celsius first (our base unit for temperature)
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:  # Already Celsius
        celsius = value
    
    # Convert from Celsius to target unit
    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return (celsius * 9/5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15

# Function to perform conversion
def convert(value, from_unit, to_unit, category, conversion_dict):
    if from_unit == to_unit:
        return value
    
    # Special case for temperature
    if category == "Temperature":
        return convert_temperature(value, from_unit, to_unit)
    
    # For direct conversion dictionaries
    # Convert to base unit first, then to target unit
    base_value = value / conversion_dict[from_unit]
    return base_value * conversion_dict[to_unit]

# Get conversion formula
def get_formula(from_unit, to_unit, category, value, result, decimal_places):
    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return f"{value}°C × (9/5) + 32 = {result:.{decimal_places}f}°F"
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return f"{value}°C + 273.15 = {result:.{decimal_places}f}K"
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return f"({value}°F - 32) × (5/9) = {result:.{decimal_places}f}°C"
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return f"({value}°F - 32) × (5/9) + 273.15 = {result:.{decimal_places}f}K"
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return f"{value}K - 273.15 = {result:.{decimal_places}f}°C"
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return f"({value}K - 273.15) × (9/5) + 32 = {result:.{decimal_places}f}°F"
        else:
            return "Same unit, no conversion needed"
    else:
        if from_unit == to_unit:
            return "Same unit, no conversion needed"
        else:
            conversion_dict = categories[category]
            factor = conversion_dict[from_unit]/conversion_dict[to_unit]
            return f"{value} {from_unit} × {1/factor:.{decimal_places}f} = {result:.{decimal_places}f} {to_unit}"

# Sidebar for settings
with st.sidebar:
    st.markdown("<h3 style='color: #1E88E5;'>Settings</h3>", unsafe_allow_html=True)
    decimal_places = st.slider("Decimal Places", 0, 10, 6)
    
    # Theme mode toggle
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    dark_mode = st.toggle("Dark Mode", st.session_state.dark_mode)
    st.session_state.dark_mode = dark_mode
    
    # Apply dark mode
    if dark_mode:
        st.markdown("""
        <style>
            /* Dark mode styles */
            .main, .stApp {
                background-color: #121212 !important;
            }
            
            p, span, label, div {
                color: #e0e0e0 !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #00aaff !important;
            }
            
            /* Dark mode for tables */
            table {
                background-color: rgba(30, 30, 46, 0.8) !important;
            }
            
            th {
                background: rgba(0, 0, 0, 0.3) !important;
                color: #00aaff !important;
            }
            
            td {
                border-bottom: 1px solid #333 !important;
                color: #ddd !important;
            }
            
            tr:nth-child(even) {
                background-color: rgba(0, 0, 0, 0.2) !important;
            }
        </style>
        """, unsafe_allow_html=True)

# Use columns to display categories in a grid
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

# Initialize selected category if not set
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = list(categories.keys())[0]

# Initialize dictionaries to store values for each category if not set
if 'category_values' not in st.session_state:
    st.session_state.category_values = {cat: 1.0 for cat in categories.keys()}
if 'category_from_units' not in st.session_state:
    st.session_state.category_from_units = {cat: list(categories[cat].keys())[0] for cat in categories.keys()}
if 'category_to_units' not in st.session_state:
    st.session_state.category_to_units = {cat: list(categories[cat].keys())[1] if len(list(categories[cat].keys())) > 1 else list(categories[cat].keys())[0] for cat in categories.keys()}

# Distribute categories across columns
for i, category in enumerate(categories.keys()):
    with cols[i % 3]:
        selected = st.button(
            f"{category_icons.get(category, '🔄')} {category}", 
            key=f"cat_{category}", 
            use_container_width=True
        )
        if selected:
            st.session_state.selected_category = category

# Use the selected category
category = st.session_state.selected_category
st.subheader(f"Selected: {category_icons.get(category, '🔄')} {category}")

# Get units for selected category
units = list(categories[category].keys())

# Create two columns for input and output
col1, col2 = st.columns(2)

# Define callback functions
def on_value_change():
    st.session_state.category_values[category] = st.session_state.from_value
    
def on_from_unit_change():
    st.session_state.category_from_units[category] = st.session_state.from_unit
    
def on_to_unit_change():
    st.session_state.category_to_units[category] = st.session_state.to_unit

# Input fields
from_value = col1.number_input("Value", 
                              value=st.session_state.category_values[category], 
                              format=f"%.{decimal_places}f", 
                              key="from_value",
                              on_change=on_value_change)

from_unit = col1.selectbox("From", 
                          units, 
                          index=units.index(st.session_state.category_from_units[category]) if st.session_state.category_from_units[category] in units else 0,
                          key="from_unit",
                          on_change=on_from_unit_change)

to_unit = col2.selectbox("To", 
                        units, 
                        index=units.index(st.session_state.category_to_units[category]) if st.session_state.category_to_units[category] in units else (1 if len(units) > 1 else 0),
                        key="to_unit",
                        on_change=on_to_unit_change)

# Calculate the result
if category == "Temperature":
    result = convert_temperature(from_value, from_unit, to_unit)
else:
    result = convert(from_value, from_unit, to_unit, category, categories[category])

# Display the result
col2.markdown(f"""
<div style="background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%); color: white; padding: 20px; border-radius: 12px; margin: 15px 0; box-shadow: 0 4px 20px rgba(0, 105, 204, 0.3); text-align: center;">
    <div style="font-size: 1.8rem; font-weight: 600; margin-bottom: 5px;">{result:.{decimal_places}f} {to_unit}</div>
    <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; font-style: italic; margin-top: 5px;">{get_formula(from_unit, to_unit, category, from_value, result, decimal_places)}</div>
</div>
""", unsafe_allow_html=True)

# Quick conversion table
st.subheader("Quick Reference Table")
if from_unit != to_unit:
    values = [0.1, 0.5, 1, 5, 10, 50, 100]
    if category == "Temperature" and (from_unit == "Kelvin" or to_unit == "Kelvin"):
        # Adjust values for temperature to be more meaningful
        if from_unit == "Kelvin" or to_unit == "Kelvin":
            values = [0, 10, 20, 30, 100, 200, 273.15, 373.15]
    
    table_data = {"From": [], "To": []}
    
    for val in values:
        if category == "Temperature":
            converted = convert_temperature(val, from_unit, to_unit)
        else:
            converted = convert(val, from_unit, to_unit, category, categories[category])
        
        table_data["From"].append(f"{val} {from_unit}")
        table_data["To"].append(f"{converted:.{decimal_places}f} {to_unit}")
    
    st.table(pd.DataFrame(table_data))

# Footer
st.markdown("""
<footer>
    Unit Converter - Simple, Fast, Reliable
</footer>
""", unsafe_allow_html=True) 