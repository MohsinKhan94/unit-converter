import streamlit as st
import pandas as pd
import numpy as np

# Set a global flag for Plotly availability
PLOTLY_AVAILABLE = False

# Set page configuration first, before any other Streamlit commands
st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    layout="wide"
)

# Try to import plotly with more detailed error handling
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
    st.success("Plotly successfully imported.")
except ImportError as e:
    st.warning(f"Plotly could not be imported: {str(e)}. Visualizations will be limited.")
except Exception as e:
    st.warning(f"Unexpected error importing plotly: {str(e)}. Visualizations will be limited.")

# Include GSAP library and custom animations
st.markdown("""
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>

<style>
    /* Base styles */
    .main {
        background-color: #f0f2f6;
        background-image: linear-gradient(135deg, #f0f2f6 0%, #e4e8f0 100%);
        transition: background-color 0.3s ease, background-image 0.3s ease;
    }
    
    /* Hide any unwanted divs */
    .element-container:empty {
        display: none !important;
    }
    
    /* Header styling with fixes */
    .app-header {
        border-bottom: 1px solid rgba(0, 105, 204, 0.2);
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        animation: fadeDown 1s ease forwards;
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
        box-shadow: 0 2px 8px rgba(0, 105, 204, 0.3);
        animation: float 3s ease-in-out infinite;
    }
    
    /* Common styles for headings */
    h1, h2, h3, h4, h5, h6 {
        color: #0066cc;
        transition: color 0.3s ease;
    }
    
    /* Cards with glassmorphism effect */
    .converter-card, .card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 105, 204, 0.1);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s, box-shadow 0.3s, background 0.3s ease, border-color 0.3s ease;
        animation: fadeUp 1s ease 0.6s forwards;
    }
    
    .converter-card:hover, .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 36px rgba(0, 105, 204, 0.15);
    }
    
    /* Result display fix */
    .result-card {
        background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0, 105, 204, 0.3);
        text-align: center;
        animation: fadeScale 1s ease 0.8s forwards;
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
    
    /* Custom Streamlit button styling */
    .stButton>button {
        background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
        color: white;
        font-weight: 500;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 105, 204, 0.3);
    }
    
    /* Category buttons styling */
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 10px;
        margin-bottom: 20px;
    }
    
    .category-button {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0, 105, 204, 0.1);
        transition: all 0.3s;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .category-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 105, 204, 0.2);
    }
    
    .category-button.selected {
        background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
        color: white;
        transform: scale(1.05);
    }
    
    .category-icon {
        font-size: 1.5rem;
        margin-bottom: 5px;
    }
    
    /* Table styling */
    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        opacity: 0;
        animation: fadeUp 1s ease 1s forwards;
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
        opacity: 0;
        animation: fadeIn 1s ease 1.2s forwards;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeScale {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes float {
        0% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0); }
    }
    
    /* Dark mode */
    .dark-mode {
        background-color: #121212 !important;
        background-image: linear-gradient(135deg, #121212 0%, #1e1e2e 100%) !important;
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
    
    .dark-mode table {
        background-color: rgba(30, 30, 46, 0.5) !important;
    }
    
    .dark-mode th {
        background: rgba(0, 0, 0, 0.3) !important;
        color: #00aaff !important;
    }
    
    .dark-mode td {
        border-bottom: 1px solid #333 !important;
        color: #ddd !important;
    }
    
    .dark-mode tr:nth-child(even) {
        background-color: rgba(0, 0, 0, 0.2) !important;
    }
</style>

<script>
    // Function to celebrate conversion with confetti
    function celebrateConversion() {
        if (typeof confetti !== 'undefined') {
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.8, x: 0.5 }
            });
        }
    }
    
    // Add click listeners to conversion buttons
    function setupEventListeners() {
        // Set up button animations and effects
        document.querySelectorAll('button').forEach(button => {
            button.addEventListener('click', function() {
                setTimeout(celebrateConversion, 500);
            });
            
            // Add hover animations
            button.addEventListener('mouseenter', () => {
                button.style.transform = 'translateY(-2px)';
                button.style.boxShadow = '0 4px 12px rgba(0, 105, 204, 0.3)';
            });
            
            button.addEventListener('mouseleave', () => {
                button.style.transform = '';
                button.style.boxShadow = '';
            });
        });
        
        // Add card tilt effects if GSAP is available
        if (typeof gsap !== 'undefined') {
            document.querySelectorAll('.card, .converter-card').forEach(card => {
                card.addEventListener('mousemove', function(e) {
                    const rect = this.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    const rotateX = (y - centerY) / 20;
                    const rotateY = (centerX - x) / 20;
                    
                    gsap.to(this, {
                        rotateX: rotateX,
                        rotateY: rotateY,
                        duration: 0.5,
                        ease: "power2.out",
                        transformPerspective: 1000,
                        transformOrigin: "center"
                    });
                });
                
                card.addEventListener('mouseleave', function() {
                    gsap.to(this, {
                        rotateX: 0,
                        rotateY: 0,
                        duration: 0.5,
                        ease: "power2.out"
                    });
                });
            });
        }
    }
    
    // Function to apply dark mode
    function applyTheme(isDark) {
        if (isDark) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    }
    
    // Run setup when document is loaded
    document.addEventListener('DOMContentLoaded', setupEventListeners);
    
    // Handle Streamlit's dynamic updates
    const observer = new MutationObserver(() => {
        setupEventListeners();
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# Custom header without using divs
st.markdown("""
<div class="app-header">
  <span class="app-title">Unit Converter</span>
  <span class="badge">Simple</span>
  <span class="badge">Elegant</span>
</div>
""", unsafe_allow_html=True)

# Conversion categories and units
categories = {
    "Length": {
        "Meter": 1,
        "Kilometer": 0.001,
        "Centimeter": 100,
        "Millimeter": 1000,
        "Micrometer": 1000000,  # 1 meter = 1,000,000 micrometers
        "Nanometer": 1000000000,  # 1 meter = 1,000,000,000 nanometers
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
        "Acre": 0.000247105,
        "Hectare": 0.0001
    },
    "Volume": {
        "Cubic Meter": 1,
        "Liter": 1000,
        "Milliliter": 1000000,
        "Gallon (US)": 264.172,
        "Quart (US)": 1056.69,
        "Pint (US)": 2113.38,
        "Cup (US)": 4226.75,
        "Fluid Ounce (US)": 33814
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
    },
    "Currency": {
        "USD": 1,
        "EUR": 0.92,
        "GBP": 0.79,
        "JPY": 149.5,
        "CAD": 1.36,
        "AUD": 1.52,
        "CNY": 7.24,
        "INR": 83.12
    }
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
def get_formula(from_unit, to_unit, category, value, result):
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

# Create a trend visualization
def create_trend_visualization(from_value, from_unit, to_unit, category):
    # Declare PLOTLY_AVAILABLE as global
    global PLOTLY_AVAILABLE
    
    # Check if units are the same
    if from_unit == to_unit:
        return None
    
    # Create a range of values around the input value
    if from_value < 0.1:
        values = np.linspace(0, 1, 10)
    elif from_value < 1:
        values = np.linspace(0, 5, 10)
    elif from_value < 10:
        values = np.linspace(0, 50, 10)
    elif from_value < 100:
        values = np.linspace(0, 500, 10)
    else:
        values = np.linspace(0, from_value * 5, 10)
    
    # Convert all values
    converted_values = []
    for val in values:
        if category == "Temperature":
            converted = convert_temperature(val, from_unit, to_unit)
        else:
            converted = convert(val, from_unit, to_unit, category, categories[category])
        converted_values.append(converted)
    
    # Create visualization based on available libraries
    if PLOTLY_AVAILABLE:
        try:
            # Create the plotly plot
            fig = px.line(
                x=values, 
                y=converted_values,
                labels={"x": f"{from_unit}", "y": f"{to_unit}"},
                title=f"Conversion Trend: {from_unit} to {to_unit}"
            )
            
            fig.update_layout(
                plot_bgcolor="white",
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.1)',
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.1)',
                ),
                title_font=dict(size=16),
                margin=dict(l=40, r=40, t=40, b=40),
            )
            
            return fig
        except Exception as e:
            st.warning(f"Error creating Plotly visualization: {str(e)}. Falling back to alternative visualization.")
            PLOTLY_AVAILABLE = False
    
    # Fallback to matplotlib if Plotly is not available
    if not PLOTLY_AVAILABLE:
        try:
            import matplotlib.pyplot as plt
            import io
            from matplotlib import rcParams
            
            # Set matplotlib style
            rcParams['font.family'] = 'sans-serif'
            rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(values, converted_values, marker='o', linestyle='-', linewidth=2, color='#0066cc')
            
            # Add labels and title
            ax.set_xlabel(from_unit)
            ax.set_ylabel(to_unit)
            ax.set_title(f"Conversion Trend: {from_unit} to {to_unit}")
            
            # Add grid
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Style improvements
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Return the matplotlib figure to streamlit
            return fig
        except Exception as e:
            st.warning(f"Error creating matplotlib visualization: {str(e)}. Visualization will be disabled.")
            return None
    
    return None

# Sidebar for settings
with st.sidebar:
    st.markdown("<h3 style='color: #1E88E5;'>Settings</h3>", unsafe_allow_html=True)
    decimal_places = st.slider("Decimal Places", 0, 10, 6)
    
    # Theme mode toggle
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    dark_mode = st.toggle("Dark Mode", st.session_state.dark_mode)
    st.session_state.dark_mode = dark_mode
    
    # Apply dark mode with a more comprehensive approach
    if dark_mode:
        st.markdown("""
        <style>
            /* Dark mode for the entire app */
            .main, .stApp, .css-ffhzg2 {
                background-color: #121212 !important;
                background-image: linear-gradient(135deg, #121212 0%, #1e1e2e 100%) !important;
                color: #f0f0f0 !important;
            }
            
            /* Dark mode for all text */
            p, span, label, .stMarkdown, .stText, div {
                color: #e0e0e0 !important;
            }
            
            /* Dark mode for headers */
            h1, h2, h3, h4, h5, h6, .stHeader, .stTitle, .stSubheader {
                color: #00aaff !important;
            }
            
            /* Dark mode for inputs - enhanced selectors */
            .stTextInput, .stNumberInput, .stDateInput, .stTimeInput, .stSelectbox {
                background-color: #2d2d3a !important;
                color: white !important;
                border-color: #444 !important;
            }
            
            /* Target the actual input elements inside Streamlit components */
            input, select, textarea, .stNumberInput input, .stTextInput input, [data-baseweb="input"] input, [data-baseweb="textarea"], 
            [data-testid="stNumberInput"] input, .stTextInput input {
                color: white !important;
                background-color: #2d2d3a !important;
                border-color: #444 !important;
            }
            
            /* Target selectbox text */
            [data-baseweb="select"] div, [data-baseweb="select"] span, [data-baseweb="select"] svg {
                color: white !important;
            }
            
            /* Target dropdown menu items */
            [role="listbox"] li, [role="option"], [data-baseweb="menu"] li, [data-baseweb="menu"] div {
                color: white !important;
                background-color: #2d2d3a !important;
            }
            
            /* Hover states for dropdown items */
            [role="listbox"] li:hover, [role="option"]:hover, [data-baseweb="menu"] li:hover {
                background-color: #444 !important;
            }
            
            /* Dark mode for sliders */
            .stSlider {
                background-color: transparent !important;
            }
            
            /* Dark mode for buttons */
            .stButton button {
                background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%) !important;
                color: white !important;
            }
            
            /* Dark mode for tables */
            .stTable, .stDataFrame {
                background-color: #1e1e2e !important;
                color: #e0e0e0 !important;
            }
            
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
            
            /* Dark mode for app header */
            .app-header {
                border-bottom-color: rgba(255, 255, 255, 0.1) !important;
            }
            
            /* Dark mode specific adjustments */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #1e1e2e !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                color: #f0f0f0 !important;
            }
            
            .stTabs [aria-selected="true"] {
                color: #00aaff !important;
            }
            
            /* Streamlit toggle */
            .st-cb, .st-bq, .st-aj, .st-c0 {
                background-color: #2d2d3a !important;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #1a1a2e !important;
                border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
            
            /* Plotly chart background */
            .js-plotly-plot {
                background-color: rgba(30, 30, 46, 0.8) !important;
            }
            
            /* Footer dark mode */
            footer {
                color: #888 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light mode reset (optional but helps avoid lingering dark styles)
        st.markdown("""
        <style>
            .main, .stApp {
                background-color: #f0f2f6 !important;
                background-image: linear-gradient(135deg, #f0f2f6 0%, #e4e8f0 100%) !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #0066cc !important;
            }
            
            p, span, label, div {
                color: #333 !important;
            }
            
            /* Reset table colors */
            table {
                background-color: white !important;
            }
            
            th {
                background: #f0f2f6 !important;
                color: #0066cc !important;
            }
            
            td {
                border-bottom: 1px solid #eee !important;
                color: #333 !important;
            }
            
            tr:nth-child(even) {
                background-color: rgba(240, 242, 246, 0.5) !important;
            }
        </style>
        """, unsafe_allow_html=True)

# Category icons
category_icons = {
    "Length": "📏",
    "Weight/Mass": "⚖️",
    "Temperature": "🌡️",
    "Area": "📐",
    "Volume": "🧪",
    "Time": "⏱️",
    "Speed": "🚀",
    "Data": "💾",
    "Currency": "💰"
}

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

# Use the selected category - use Streamlit's native heading
category = st.session_state.selected_category
st.subheader(f"Selected: {category_icons.get(category, '🔄')} {category}")

# Get units for selected category
units = list(categories[category].keys())

# Create two columns for input and output
col1, col2 = st.columns(2)

# Direct components in columns instead of HTML cards - with session state preservation
def on_value_change():
    st.session_state.category_values[category] = st.session_state.from_value
    
def on_from_unit_change():
    st.session_state.category_from_units[category] = st.session_state.from_unit
    
def on_to_unit_change():
    st.session_state.category_to_units[category] = st.session_state.to_unit

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

# Display the result directly
col2.markdown(f"""
<div style="background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%); color: white; padding: 20px; border-radius: 12px; margin: 15px 0; box-shadow: 0 4px 20px rgba(0, 105, 204, 0.3); text-align: center;">
    <div style="font-size: 1.8rem; font-weight: 600; margin-bottom: 5px;">{result:.{decimal_places}f} {to_unit}</div>
    <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; font-style: italic; margin-top: 5px;">{get_formula(from_unit, to_unit, category, from_value, result)}</div>
</div>
""", unsafe_allow_html=True)

# Enhanced visualization
st.subheader("Conversion Trend")
fig = create_trend_visualization(from_value, from_unit, to_unit, category)
if fig:
    try:
        # Check if it's a plotly figure (has 'update_layout' attribute)
        if hasattr(fig, 'update_layout'):
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Assume it's a matplotlib figure
            st.pyplot(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying visualization: {str(e)}")
        
        # Show a basic table as fallback
        st.write("Conversion values:")
        values = [0.1, 1, 10, 100]
        table_data = {"Value in " + from_unit: [], "Value in " + to_unit: []}
        for val in values:
            if category == "Temperature":
                converted = convert_temperature(val, from_unit, to_unit)
            else:
                converted = convert(val, from_unit, to_unit, category, categories[category])
            table_data["Value in " + from_unit].append(val)
            table_data["Value in " + to_unit].append(converted)
        st.table(pd.DataFrame(table_data))
else:
    # No figure was created, show table as fallback
    if from_unit != to_unit:
        st.write("Conversion values:")
        values = [0.1, 1, 10, 100]
        table_data = {"Value in " + from_unit: [], "Value in " + to_unit: []}
        for val in values:
            if category == "Temperature":
                converted = convert_temperature(val, from_unit, to_unit)
            else:
                converted = convert(val, from_unit, to_unit, category, categories[category])
            table_data["Value in " + from_unit].append(val)
            table_data["Value in " + to_unit].append(converted)
        st.table(pd.DataFrame(table_data))

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
<footer style="margin-top: 3rem; text-align: center; color: #666; font-size: 0.8rem; opacity: 0; animation: fadeIn 1s ease 1.2s forwards;">
    Simple Unit Converter - Clean, Fast, Beautiful
</footer>
""", unsafe_allow_html=True) 