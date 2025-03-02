import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import re
import math

# Set page configuration
st.set_page_config(
    page_title="Unit Converter Pro",
    page_icon="🔄",
    layout="wide"
)

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
    }
    
    h1 {
        color: #0066cc;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        opacity: 0;
    }
    
    h2 {
        color: #0066cc;
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 1.5rem;
        opacity: 0;
    }
    
    h3 {
        color: #0066cc;
        font-size: 1.4rem;
        margin-top: 1rem;
        opacity: 0;
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
        transition: transform 0.3s, box-shadow 0.3s;
        opacity: 0;
        transform: translateY(20px);
    }
    
    .converter-card:hover, .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 36px rgba(0, 105, 204, 0.15);
    }
    
    .result-display {
        background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        font-size: 1.6rem;
        font-weight: 600;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0, 105, 204, 0.3);
        opacity: 0;
        transform: scale(0.95);
    }
    
    .formula {
        color: #666;
        font-size: 0.9rem;
        font-style: italic;
        margin-top: 5px;
        text-align: center;
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
    
    .category-selector {
        margin-bottom: 20px;
    }
    
    footer {
        margin-top: 3rem;
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        opacity: 0;
    }
    
    /* Header styling */
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(0, 105, 204, 0.2);
        opacity: 0;
        transform: translateY(-10px);
    }
    
    .logo {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0066cc 0%, #00aaff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
    }
    
    .badge {
        background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-left: 10px;
        box-shadow: 0 2px 8px rgba(0, 105, 204, 0.3);
        transition: all 0.3s ease;
    }
    
    .badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 105, 204, 0.4);
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
    
    /* Input field styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #e0e3e9;
        padding: 10px 15px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.2);
    }
    
    /* Add a subtle pattern background */
    .main:before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%230066cc' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        z-index: -1;
        pointer-events: none;
    }
    
    /* Add custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #005bb8 0%, #0088ee 100%);
    }
    
    /* Animation classes for GSAP */
    .fade-in {
        opacity: 0;
    }
    
    .slide-up {
        opacity: 0;
        transform: translateY(30px);
    }
    
    .slide-left {
        opacity: 0;
        transform: translateX(30px);
    }
    
    .scale-in {
        opacity: 0;
        transform: scale(0.9);
    }
    
    /* Pulsing effect for result */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(0, 102, 204, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Floating animation for cards */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }
    
    .float {
        animation: float 4s ease-in-out infinite;
    }
</style>

<script>
    // Initialize GSAP animations
    function initGSAP() {
        // Check if GSAP is loaded
        if (typeof gsap !== 'undefined') {
            // Register ScrollTrigger plugin
            gsap.registerPlugin(ScrollTrigger);
            
            // Get animation speed factor if available
            const speedFactor = window.animationSpeedFactor || 1;
            
            // Animation for header
            gsap.to('.header', {
                opacity: 1,
                y: 0,
                duration: 1 * speedFactor,
                ease: "power3.out"
            });
            
            // Animate headings
            gsap.to('h1, h2, h3', {
                opacity: 1,
                duration: 0.8 * speedFactor,
                stagger: 0.2 * speedFactor,
                ease: "power2.out",
                scrollTrigger: {
                    trigger: 'h1, h2, h3',
                    start: "top 90%"
                }
            });
            
            // Animate cards with 3D rotation effect
            gsap.utils.toArray('.card, .converter-card').forEach(card => {
                // Create a tilt effect on mouse move for cards
                card.addEventListener('mousemove', function(e) {
                    const rect = this.getBoundingClientRect();
                    const x = e.clientX - rect.left; // x position within the element
                    const y = e.clientY - rect.top; // y position within the element
                    
                    // Calculate rotation based on mouse position
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    const rotateX = (y - centerY) / 20;
                    const rotateY = (centerX - x) / 20;
                    
                    // Apply the rotation
                    gsap.to(this, {
                        rotateX: rotateX,
                        rotateY: rotateY,
                        duration: 0.5,
                        ease: "power2.out",
                        transformPerspective: 1000,
                        transformOrigin: "center"
                    });
                });
                
                // Reset rotation when mouse leaves
                card.addEventListener('mouseleave', function() {
                    gsap.to(this, {
                        rotateX: 0,
                        rotateY: 0,
                        duration: 0.5,
                        ease: "power2.out"
                    });
                });
                
                // Animate cards on scroll
                gsap.fromTo(card,
                    {
                        y: 50,
                        opacity: 0
                    },
                    {
                        y: 0,
                        opacity: 1,
                        duration: 0.8 * speedFactor,
                        ease: "back.out(1.7)",
                        scrollTrigger: {
                            trigger: card,
                            start: "top 90%"
                        }
                    }
                );
            });
            
            // Animate result with attention-grabbing effect
            gsap.utils.toArray('.result-display').forEach(result => {
                // Initial animation
                gsap.fromTo(result,
                    {
                        scale: 0.8,
                        opacity: 0
                    },
                    {
                        scale: 1,
                        opacity: 1,
                        duration: 0.8 * speedFactor,
                        ease: "elastic.out(1, 0.5)",
                        scrollTrigger: {
                            trigger: result,
                            start: "top 90%"
                        },
                        onComplete: function() {
                            // Add a subtle pulse animation
                            gsap.to(result, {
                                boxShadow: '0 8px 32px rgba(0, 105, 204, 0.4)',
                                duration: 1.5 * speedFactor,
                                repeat: -1,
                                yoyo: true,
                                ease: "sine.inOut"
                            });
                        }
                    }
                );
            });
            
            // Animate buttons with hover effects
            gsap.utils.toArray('button').forEach(button => {
                button.addEventListener('mouseenter', () => {
                    gsap.to(button, {
                        scale: 1.05,
                        duration: 0.3 * speedFactor,
                        ease: "power1.out"
                    });
                });
                
                button.addEventListener('mouseleave', () => {
                    gsap.to(button, {
                        scale: 1,
                        duration: 0.3 * speedFactor,
                        ease: "power1.out"
                    });
                });
                
                // Add click effect
                button.addEventListener('click', () => {
                    gsap.timeline()
                        .to(button, {
                            scale: 0.95,
                            duration: 0.1 * speedFactor
                        })
                        .to(button, {
                            scale: 1,
                            duration: 0.3 * speedFactor,
                            ease: "back.out(2)"
                        });
                });
            });
            
            // Add floating animation to badges
            gsap.utils.toArray('.badge').forEach(badge => {
                gsap.to(badge, {
                    y: -5,
                    duration: 2 * speedFactor,
                    repeat: -1,
                    yoyo: true,
                    ease: "sine.inOut"
                });
            });
            
            // Staggered animation for table rows
            gsap.utils.toArray('tr').forEach((row, index) => {
                gsap.fromTo(row,
                    {
                        opacity: 0,
                        x: -20
                    },
                    {
                        opacity: 1,
                        x: 0,
                        duration: 0.5 * speedFactor,
                        delay: index * 0.05 * speedFactor,
                        ease: "power1.out",
                        scrollTrigger: {
                            trigger: row,
                            start: "top 95%"
                        }
                    }
                );
            });
            
            // Footer animation
            gsap.to('footer', {
                opacity: 1,
                duration: 1 * speedFactor,
                delay: 0.5 * speedFactor,
                scrollTrigger: {
                    trigger: 'footer',
                    start: "top 95%"
                }
            });
        } else {
            // If GSAP is not loaded yet, try again in 100ms
            setTimeout(initGSAP, 100);
        }
    }
    
    // Function to celebrate conversion with confetti
    function celebrateConversion() {
        if (typeof confetti !== 'undefined') {
            // Shoot confetti from the middle bottom
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.8, x: 0.5 }
            });
            
            // If there's a result display, add special animation
            const resultDisplays = document.querySelectorAll('.result-display');
            if (resultDisplays.length > 0 && typeof gsap !== 'undefined') {
                resultDisplays.forEach(display => {
                    // Create a celebratory animation
                    gsap.timeline()
                        .to(display, {
                            scale: 1.1,
                            boxShadow: '0 0 30px rgba(0, 150, 255, 0.8)',
                            duration: 0.3,
                            ease: "back.out(2)"
                        })
                        .to(display, {
                            scale: 1,
                            boxShadow: '0 8px 32px rgba(0, 105, 204, 0.3)',
                            duration: 0.5,
                            ease: "elastic.out(1, 0.3)"
                        });
                });
            }
        }
    }
    
    // Add click listeners to conversion buttons
    function setupConversionButtons() {
        // Listen for button clicks that might be conversion actions
        document.querySelectorAll('button').forEach(button => {
            button.addEventListener('click', function() {
                // Filter out some buttons that shouldn't trigger confetti
                const buttonText = button.innerText.toLowerCase();
                if (buttonText.includes('clear') || buttonText.includes('reset') || buttonText.includes('remove')) {
                    return;
                }
                
                // Give time for Streamlit to update the UI, then celebrate
                setTimeout(celebrateConversion, 500);
            });
        });
    }
    
    // Run animations when document is ready or Streamlit is fully loaded
    document.addEventListener('DOMContentLoaded', function() {
        initGSAP();
        setupConversionButtons();
    });
    
    // Also handle Streamlit's dynamic updates
    const observer = new MutationObserver(() => {
        initGSAP();
        setupConversionButtons();
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# App header with animated badges
st.markdown("""
<div class="header">
    <div class="logo">Unit Converter Pro 
        <span class="badge">Business</span> 
        <span class="badge">Education</span>
        <span class="badge">NEW</span>
    </div>
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
            return f"{value}°C × (9/5) + 32 = {result:.6g}°F"
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return f"{value}°C + 273.15 = {result:.6g}K"
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return f"({value}°F - 32) × (5/9) = {result:.6g}°C"
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return f"({value}°F - 32) × (5/9) + 273.15 = {result:.6g}K"
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return f"{value}K - 273.15 = {result:.6g}°C"
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return f"({value}K - 273.15) × (9/5) + 32 = {result:.6g}°F"
        else:
            return "Same unit, no conversion needed"
    else:
        if from_unit == to_unit:
            return "Same unit, no conversion needed"
        else:
            conversion_dict = categories[category]
            factor = conversion_dict[from_unit]/conversion_dict[to_unit]
            return f"{value} {from_unit} × {1/factor:.6g} = {result:.6g} {to_unit}"

# Scientific calculator function
def scientific_calculator(expression):
    """
    A simple scientific calculator that evaluates mathematical expressions
    """
    # Replace scientific notation
    expression = expression.replace('^', '**')
    expression = expression.replace('×', '*')
    expression = expression.replace('÷', '/')
    
    # Add support for common math functions
    safe_dict = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'log': math.log10,
        'ln': math.log,
        'exp': math.exp,
        'pi': math.pi,
        'e': math.e,
        'abs': abs,
        'pow': pow,
        'round': round
    }
    
    try:
        # Evaluate the expression in a safe environment
        return eval(expression, {"__builtins__": {}}, safe_dict)
    except Exception as e:
        return f"Error: {str(e)}"

# Function to generate enhanced visualizations
def create_enhanced_visualization(from_value, from_unit, to_unit, category):
    """Create an enhanced visualization comparing values in two units"""
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
    
    # Create a Plotly figure with two y-axes
    fig = px.line(
        x=values, 
        y=converted_values,
        labels={"x": f"{from_unit}", "y": f"{to_unit}"},
        title=f"Conversion Relationship: {from_unit} to {to_unit}"
    )
    
    # Enhance the plot with better styling
    fig.update_layout(
        plot_bgcolor="rgba(240, 242, 246, 0.8)",
        paper_bgcolor="rgba(240, 242, 246, 0.3)",
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="#333"
        ),
        title=dict(
            font=dict(
                family="Arial, sans-serif",
                size=20,
                color="#0066cc"
            )
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.1)',
            gridwidth=1,
            zeroline=True,
            zerolinecolor='rgba(0, 0, 0, 0.2)',
            zerolinewidth=1,
            title_font=dict(size=16)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.1)',
            gridwidth=1,
            zeroline=True,
            zerolinecolor='rgba(0, 0, 0, 0.2)',
            zerolinewidth=1,
            title_font=dict(size=16)
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified"
    )
    
    # Change the line appearance
    fig.update_traces(
        line=dict(width=3, color='#0066cc'),
        mode='lines+markers',
        marker=dict(size=8, color='#0066cc', line=dict(width=2, color='white'))
    )
    
    # Add points at specific value
    fig.add_scatter(
        x=[from_value],
        y=[convert(from_value, from_unit, to_unit, category, categories[category]) if category != "Temperature" 
           else convert_temperature(from_value, from_unit, to_unit)],
        mode='markers',
        marker=dict(size=12, color='#ff3b30', line=dict(width=2, color='white')),
        name=f"Current Value: {from_value} {from_unit}"
    )
    
    return fig

# Function to create a trend visualization
def create_trend_visualization(from_value, from_unit, to_unit, category):
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
    
    # Create the plot
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

# Function to save to history
def save_to_history(category, from_value, from_unit, to_value, to_unit):
    if 'conversion_history' not in st.session_state:
        st.session_state.conversion_history = []
    
    st.session_state.conversion_history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "from_value": from_value,
        "from_unit": from_unit,
        "to_value": to_value,
        "to_unit": to_unit
    })

# Function to export history to CSV
def export_history_to_csv():
    if 'conversion_history' in st.session_state and st.session_state.conversion_history:
        df = pd.DataFrame(st.session_state.conversion_history)
        return df.to_csv(index=False).encode('utf-8')
    return None

# Define business use cases
business_use_cases = {
    "Length": [
        "Construction and architecture - measuring building dimensions",
        "Logistics - calculating shipping container space",
        "Manufacturing - product specifications and quality control"
    ],
    "Weight/Mass": [
        "Shipping and freight - calculating shipping costs",
        "Manufacturing - material requirements and inventory management",
        "Food industry - recipe scaling and portion control"
    ],
    "Temperature": [
        "Food safety - monitoring storage temperatures",
        "Manufacturing - process control and quality assurance",
        "HVAC - building climate control systems"
    ],
    "Area": [
        "Real estate - property valuation and space planning",
        "Agriculture - crop yield estimation and land management",
        "Construction - material estimation (flooring, roofing, etc.)"
    ],
    "Volume": [
        "Chemical industry - mixing solutions and compounds",
        "Beverage industry - production and packaging",
        "Oil and gas - storage and transportation"
    ],
    "Time": [
        "Project management - scheduling and resource allocation",
        "Logistics - delivery timeframes and planning",
        "Manufacturing - production cycle optimization"
    ],
    "Speed": [
        "Transportation - delivery scheduling and route planning",
        "Manufacturing - production line optimization",
        "Telecommunications - data transfer rates"
    ],
    "Data": [
        "IT infrastructure - storage planning and management",
        "Telecommunications - bandwidth allocation",
        "Cloud services - pricing and capacity planning"
    ],
    "Currency": [
        "International trade - pricing and cost analysis",
        "Financial services - investment and portfolio management",
        "Travel industry - pricing and currency exchange services"
    ]
}

# Define student tips
student_tips = {
    "Length": "Remember that the meter is the base unit of length in the metric system. Most scientific calculations use metric units.",
    "Weight/Mass": "Mass is a measure of the amount of matter, while weight is the force of gravity on an object. On Earth, we often use these terms interchangeably.",
    "Temperature": "The Kelvin scale has no negative values and is used in scientific calculations. 0 Kelvin is absolute zero, the lowest possible temperature.",
    "Area": "Area is a two-dimensional measurement. When converting between units, remember that the conversion factor must be squared.",
    "Volume": "Volume is a three-dimensional measurement. When converting between units, the conversion factor must be cubed.",
    "Time": "Time is the only measurement unit that uses the same base across all systems (seconds, minutes, hours).",
    "Speed": "Speed is a derived unit, calculated as distance divided by time. Pay attention to both components when converting.",
    "Data": "Digital data uses binary (base-2) prefixes: 1 Kilobyte = 1024 Bytes, not 1000 Bytes as in the metric system.",
    "Currency": "Currency conversion rates fluctuate constantly based on global markets. These are approximate values for educational purposes."
}

# Main app layout
with st.sidebar:
    st.markdown("<h3 style='color: #1E88E5;'>ProConvert Tools</h3>", unsafe_allow_html=True)
    
    # Mode selection
    app_mode = st.radio(
        "Select Mode",
        ["Standard Converter", "Batch Conversion", "For Students"]
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Settings
    st.markdown("<h4>Settings</h4>", unsafe_allow_html=True)
    decimal_places = st.slider("Decimal Places", 0, 10, 6)
    
    # Theme settings
    st.markdown("<h4>Theme Settings</h4>", unsafe_allow_html=True)
    theme_mode = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    animation_speed = st.select_slider("Animation Speed", options=["Slow", "Normal", "Fast"])
    
    # Apply theme settings with JavaScript
    theme_js = f"""
    <script>
        function applyTheme() {{
            const theme = "{theme_mode}";
            const body = document.body;
            
            if (theme === "Dark" || (theme === "Auto" && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
                // Add dark mode styles
                const darkStyles = `
                    .main {{
                        background-color: #121212 !important;
                        background-image: linear-gradient(135deg, #121212 0%, #1e1e2e 100%) !important;
                    }}
                    
                    h1, h2, h3, h4, h5, h6 {{
                        color: #00aaff !important;
                    }}
                    
                    p, span, div {{
                        color: #f0f0f0 !important;
                    }}
                    
                    .converter-card, .card {{
                        background: rgba(30, 30, 46, 0.7) !important;
                        border: 1px solid rgba(255, 255, 255, 0.1) !important;
                    }}
                    
                    .stButton>button {{
                        background: linear-gradient(135deg, #0099ff 0%, #00ccff 100%) !important;
                    }}
                    
                    table {{
                        background-color: rgba(30, 30, 46, 0.5) !important;
                    }}
                    
                    th {{
                        background: rgba(0, 0, 0, 0.3) !important;
                        color: #00aaff !important;
                    }}
                    
                    td {{
                        border-bottom: 1px solid #333 !important;
                        color: #ddd !important;
                    }}
                    
                    tr:nth-child(even) {{
                        background-color: rgba(0, 0, 0, 0.2) !important;
                    }}
                `;
                
                // Add or update the style element
                let styleEl = document.getElementById('dark-theme-style');
                if (!styleEl) {{
                    styleEl = document.createElement('style');
                    styleEl.id = 'dark-theme-style';
                    document.head.appendChild(styleEl);
                }}
                styleEl.textContent = darkStyles;
                
            }} else {{
                // Remove dark mode styles if they exist
                const styleEl = document.getElementById('dark-theme-style');
                if (styleEl) styleEl.remove();
            }}
        }}
        
        // Apply animation speed
        function applyAnimationSpeed() {{
            const speed = "{animation_speed}";
            let speedFactor = 1;
            
            if (speed === "Fast") speedFactor = 0.6;
            else if (speed === "Slow") speedFactor = 1.5;
            
            // Add a style tag to set a CSS variable for animation duration
            let styleEl = document.getElementById('animation-speed-style');
            if (!styleEl) {{
                styleEl = document.createElement('style');
                styleEl.id = 'animation-speed-style';
                document.head.appendChild(styleEl);
            }}
            
            styleEl.textContent = `
                :root {{
                    --animation-speed-factor: ${{speedFactor}};
                }}
            `;
            
            // Update GSAP animations if it's available
            if (typeof gsap !== 'undefined') {{
                // This will be used by GSAP animations to adjust their duration
                window.animationSpeedFactor = speedFactor;
            }}
        }}
        
        // Run the functions
        function updateTheme() {{
            applyTheme();
            applyAnimationSpeed();
        }}
        
        // Apply theme immediately and whenever the DOM changes
        updateTheme();
        const observer = new MutationObserver(() => {{
            updateTheme();
        }});
        
        observer.observe(document.body, {{ childList: true, subtree: true }});
        
        // Also update when the page has fully loaded
        window.addEventListener('load', updateTheme);
    </script>
    """
    st.markdown(theme_js, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # History section
    st.markdown("<h4>Conversion History</h4>", unsafe_allow_html=True)
    
    if 'conversion_history' in st.session_state and st.session_state.conversion_history:
        if st.button("Clear History"):
            st.session_state.conversion_history = []
            st.experimental_rerun()
        
        csv = export_history_to_csv()
        if csv is not None:
            st.download_button(
                label="Export to CSV",
                data=csv,
                file_name="conversion_history.csv",
                mime="text/csv",
            )
    else:
        st.write("No conversion history yet.")

# Standard Converter Mode
if app_mode == "Standard Converter":
    st.markdown("<h2 class='slide-up'>Standard Unit Converter</h2>", unsafe_allow_html=True)
    
    # Floating action button for quick help
    st.markdown("""
    <div class="fab-container">
        <button class="fab" id="helpButton">
            <span>?</span>
        </button>
    </div>
    
    <div class="help-tooltip" id="helpTooltip">
        <div class="tooltip-content">
            <h4>Quick Tips</h4>
            <ul>
                <li>Choose a category and units to convert between</li>
                <li>View the conversion formula below the result</li>
                <li>Explore the trend graph to see how values scale</li>
                <li>Check the reference table for common conversions</li>
            </ul>
            <button class="close-tooltip">×</button>
        </div>
    </div>
    
    <script>
        // Set up the help button functionality
        function setupHelpButton() {
            const helpButton = document.getElementById('helpButton');
            const helpTooltip = document.getElementById('helpTooltip');
            const closeTooltip = document.querySelector('.close-tooltip');
            
            if (helpButton && helpTooltip && closeTooltip) {
                helpButton.addEventListener('click', () => {
                    helpTooltip.classList.toggle('active');
                    
                    // Animate tooltip with GSAP if available
                    if (typeof gsap !== 'undefined') {
                        if (helpTooltip.classList.contains('active')) {
                            gsap.fromTo(helpTooltip, 
                                {opacity: 0, scale: 0.8, y: 20},
                                {opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "back.out(1.7)"}
                            );
                        }
                    }
                });
                
                closeTooltip.addEventListener('click', () => {
                    helpTooltip.classList.remove('active');
                });
            } else {
                // Try again if elements aren't ready
                setTimeout(setupHelpButton, 500);
            }
        }
        
        // Run setup when DOM is loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setupHelpButton);
        } else {
            setupHelpButton();
        }
    </script>
    
    <style>
        .fab-container {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 999;
        }
        
        .fab {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
            color: white;
            border: none;
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.4);
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .fab:hover {
            transform: scale(1.1) rotate(10deg);
            box-shadow: 0 6px 16px rgba(0, 102, 204, 0.6);
        }
        
        .help-tooltip {
            position: fixed;
            bottom: 100px;
            right: 30px;
            width: 300px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
            z-index: 998;
            opacity: 0;
            visibility: hidden;
            transform: translateY(20px);
            transition: all 0.3s;
        }
        
        .help-tooltip.active {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }
        
        .tooltip-content {
            padding: 20px;
        }
        
        .tooltip-content h4 {
            margin-top: 0;
            color: #0066cc;
        }
        
        .tooltip-content ul {
            padding-left: 20px;
            margin-bottom: 15px;
        }
        
        .close-tooltip {
            position: absolute;
            top: 10px;
            right: 10px;
            background: none;
            border: none;
            font-size: 18px;
            cursor: pointer;
            color: #666;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Interactive category selection with cards
    st.markdown("<div class='category-selector slide-up'>", unsafe_allow_html=True)
    
    # Display categories as interactive cards
    category_cols = st.columns(4)
    
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
    
    # Create a session state for selected category if it doesn't exist
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = list(categories.keys())[0]
    
    # Display category cards
    for i, (col, category) in enumerate(zip(category_cols, list(categories.keys())[:4])):
        with col:
            is_selected = st.session_state.selected_category == category
            selected_class = "selected" if is_selected else ""
            st.markdown(f"""
            <div class="category-card {selected_class}" id="category-{i}" onclick="selectCategory('{category}')">
                <div class="category-icon">{category_icons.get(category, '🔄')}</div>
                <div class="category-name">{category}</div>
            </div>
            """, unsafe_allow_html=True)
    
    category_cols = st.columns(4)
    for i, (col, category) in enumerate(zip(category_cols, list(categories.keys())[4:8])):
        with col:
            is_selected = st.session_state.selected_category == category
            selected_class = "selected" if is_selected else ""
            st.markdown(f"""
            <div class="category-card {selected_class}" id="category-{i+4}" onclick="selectCategory('{category}')">
                <div class="category-icon">{category_icons.get(category, '🔄')}</div>
                <div class="category-name">{category}</div>
            </div>
            """, unsafe_allow_html=True)
    
    category_cols = st.columns(4)
    if len(categories.keys()) > 8:
        for i, (col, category) in enumerate(zip(category_cols, list(categories.keys())[8:])):
            with col:
                is_selected = st.session_state.selected_category == category
                selected_class = "selected" if is_selected else ""
                st.markdown(f"""
                <div class="category-card {selected_class}" id="category-{i+8}" onclick="selectCategory('{category}')">
                    <div class="category-icon">{category_icons.get(category, '🔄')}</div>
                    <div class="category-name">{category}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # JavaScript for category selection
    st.markdown("""
    <script>
        function selectCategory(category) {
            // Use Streamlit's setComponentValue to update
            if (window.Streamlit) {
                window.Streamlit.setComponentValue(category);
            }
            
            // Update visual state immediately for better UX
            document.querySelectorAll('.category-card').forEach(card => {
                card.classList.remove('selected');
            });
            
            // Find the card that matches the category and select it
            document.querySelectorAll('.category-card').forEach(card => {
                if (card.querySelector('.category-name').innerText === category) {
                    card.classList.add('selected');
                    
                    // Add animation with GSAP if available
                    if (typeof gsap !== 'undefined') {
                        gsap.to(card, {
                            scale: 1.05,
                            boxShadow: '0 12px 32px rgba(0, 105, 204, 0.25)',
                            duration: 0.3,
                            ease: "back.out(1.5)"
                        });
                        
                        gsap.to(card.querySelector('.category-icon'), {
                            scale: 1.2,
                            duration: 0.4,
                            ease: "elastic.out(1, 0.5)"
                        });
                    }
                }
            });
        }
        
        // Add hover animations to category cards
        function addCategoryCardAnimations() {
            if (typeof gsap !== 'undefined') {
                document.querySelectorAll('.category-card:not(.selected)').forEach(card => {
                    card.addEventListener('mouseenter', () => {
                        gsap.to(card, {
                            y: -5,
                            boxShadow: '0 10px 20px rgba(0, 105, 204, 0.2)',
                            duration: 0.3,
                            ease: "power2.out"
                        });
                        
                        gsap.to(card.querySelector('.category-icon'), {
                            scale: 1.1,
                            duration: 0.3,
                            ease: "back.out(1.5)"
                        });
                    });
                    
                    card.addEventListener('mouseleave', () => {
                        gsap.to(card, {
                            y: 0,
                            boxShadow: '0 4px 10px rgba(0, 105, 204, 0.1)',
                            duration: 0.3,
                            ease: "power2.out"
                        });
                        
                        gsap.to(card.querySelector('.category-icon'), {
                            scale: 1,
                            duration: 0.3,
                            ease: "power2.out"
                        });
                    });
                });
            }
        }
        
        // Add mutation observer to handle Streamlit's dynamic updates
        const catObserver = new MutationObserver(() => {
            addCategoryCardAnimations();
        });
        
        catObserver.observe(document.body, { childList: true, subtree: true });
        
        // Run once on load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', addCategoryCardAnimations);
        } else {
            addCategoryCardAnimations();
        }
    </script>
    
    <style>
        .category-selector {
            margin-bottom: 30px;
        }
        
        .category-card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            margin-bottom: 15px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0, 105, 204, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .category-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 105, 204, 0.2);
        }
        
        .category-card.selected {
            background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
            color: white;
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(0, 105, 204, 0.3);
        }
        
        .category-icon {
            font-size: 2rem;
            margin-bottom: 8px;
        }
        
        .category-name {
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Use the selected category
    category = st.selectbox("Select category", list(categories.keys()), key="category_select", label_visibility="collapsed")
    st.session_state.selected_category = category
    
    # Get units for selected category
    units = list(categories[category].keys())
    
    # Add a tab layout for additional features
    converter_tabs = st.tabs(["Basic Converter", "Scientific Calculator", "Unit Comparison"])
    
    with converter_tabs[0]:
        # Move existing converter code here
        # Create two columns for input and output
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            from_value = st.number_input("Value", value=1.0, format=f"%.{decimal_places}f")
            from_unit = st.selectbox("From", units)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            to_unit = st.selectbox("To", units, index=1 if len(units) > 1 else 0)
            
            # Calculate the result
            if category == "Temperature":
                result = convert_temperature(from_value, from_unit, to_unit)
            else:
                result = convert(from_value, from_unit, to_unit, category, categories[category])
            
            # Save to history
            save_to_history(category, from_value, from_unit, result, to_unit)
            
            # Display the result
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-value'>{result:.{decimal_places}g} {to_unit}</div>", unsafe_allow_html=True)
            
            # Display the formula
            formula = get_formula(from_unit, to_unit, category, from_value, result)
            st.markdown(f"<div class='formula'>{formula}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Enhanced visualization
        st.markdown("<h3>Conversion Relationship</h3>", unsafe_allow_html=True)
        fig = create_enhanced_visualization(from_value, from_unit, to_unit, category)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Quick conversion table
        st.markdown("<h3>Quick Reference Table</h3>", unsafe_allow_html=True)
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
                table_data["To"].append(f"{converted:.{decimal_places}g} {to_unit}")
            
            st.table(pd.DataFrame(table_data))
        else:
            st.write("Select different units to see conversion table")
        
        # Business use cases
        if category in business_use_cases:
            st.markdown("<h3>Business Applications</h3>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("Common business use cases for this conversion type:")
            for use_case in business_use_cases[category]:
                st.markdown(f"- {use_case}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with converter_tabs[1]:
        st.markdown("<h3>Scientific Calculator</h3>", unsafe_allow_html=True)
        st.markdown("<p>Use this calculator for complex calculations before converting units</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <style>
            .calculator-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 8px;
                max-width: 400px;
                margin-bottom: 20px;
            }
            
            .calculator-button {
                background: linear-gradient(135deg, #f0f2f6 0%, #e4e8f0 100%);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                text-align: center;
                transition: all 0.2s;
                cursor: pointer;
            }
            
            .calculator-button:hover {
                background: linear-gradient(135deg, #e4e8f0 0%, #d8dce4 100%);
                transform: translateY(-2px);
            }
            
            .calculator-button.operator {
                background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
                color: white;
            }
            
            .calculator-button.function {
                background: linear-gradient(135deg, #4a4a4a 0%, #6a6a6a 100%);
                color: white;
            }
            
            .calculator-button.equals {
                background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
                color: white;
                grid-column: span 2;
            }
            
            .calculator-screen {
                grid-column: span 4;
                background-color: white;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 15px;
                font-size: 20px;
                text-align: right;
                margin-bottom: 10px;
                min-height: 30px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        calc_col1, calc_col2 = st.columns([2, 1])
        
        with calc_col1:
            calc_expression = st.text_input("Enter a mathematical expression", 
                                           placeholder="e.g., 2 + 2 or sin(30) or sqrt(16)")
            
            if calc_expression:
                calc_result = scientific_calculator(calc_expression)
                st.markdown(f"""
                <div class='result-card' style='margin-top: 15px;'>
                    <div class='result-value'>{calc_result}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Add the result to the converter if it's a number
                if isinstance(calc_result, (int, float)):
                    if st.button("Use this result in converter"):
                        st.session_state['calculator_result'] = calc_result
                        st.experimental_rerun()
        
        with calc_col2:
            st.markdown("<p>Examples:</p>", unsafe_allow_html=True)
            st.markdown("""
            - Basic: `2 + 3 * 4`
            - Trig: `sin(30) * 2`
            - Powers: `2^3 + 4^2`
            - Roots: `sqrt(16) + sqrt(9)`
            - Constants: `pi * 2` or `e^2`
            """)
    
    with converter_tabs[2]:
        st.markdown("<h3>Unit Comparison</h3>", unsafe_allow_html=True)
        st.markdown("<p>Compare multiple units side by side</p>", unsafe_allow_html=True)
        
        # Allow selecting multiple units to compare
        comparison_units = st.multiselect("Select units to compare", units, 
                                         default=[units[0], units[1] if len(units) > 1 else units[0]])
        
        if len(comparison_units) > 0:
            comparison_value = st.number_input("Reference value", value=1.0, format=f"%.{decimal_places}f", key="compare_value")
            
            # Create comparison table
            compare_data = {}
            
            # First column is the reference unit
            reference_unit = comparison_units[0]
            
            # Generate data for all selected units
            for unit in comparison_units:
                values = []
                for base_val in [0.1, 0.5, 1, 5, 10, 50, 100]:
                    # Convert from reference unit to current unit
                    if category == "Temperature":
                        if reference_unit == unit:
                            result = base_val
                        else:
                            result = convert_temperature(base_val, reference_unit, unit)
                    else:
                        if reference_unit == unit:
                            result = base_val
                        else:
                            result = convert(base_val, reference_unit, unit, category, categories[category])
                    values.append(f"{result:.{decimal_places}g}")
                
                compare_data[f"{unit}"] = values
            
            # Create a DataFrame for the comparison table
            compare_df = pd.DataFrame(compare_data, index=[f"{val} {reference_unit}" for val in [0.1, 0.5, 1, 5, 10, 50, 100]])
            
            # Display the comparison table
            st.markdown("<div class='comparison-table'>", unsafe_allow_html=True)
            st.dataframe(compare_df)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Create a bar chart comparing the selected value across units
            comparison_results = []
            for unit in comparison_units:
                if category == "Temperature":
                    if reference_unit == unit:
                        result = comparison_value
                    else:
                        result = convert_temperature(comparison_value, reference_unit, unit)
                else:
                    if reference_unit == unit:
                        result = comparison_value
                    else:
                        result = convert(comparison_value, reference_unit, unit, category, categories[category])
                comparison_results.append(result)
            
            # Create a bar chart
            comparison_fig = px.bar(
                x=comparison_units,
                y=comparison_results,
                labels={"x": "Unit", "y": "Equivalent Value"},
                title=f"Comparison of {comparison_value} {reference_unit} across different units",
                color_discrete_sequence=['#0066cc']
            )
            
            comparison_fig.update_layout(
                plot_bgcolor="rgba(240, 242, 246, 0.8)",
                paper_bgcolor="rgba(240, 242, 246, 0.3)",
                font=dict(
                    family="Arial, sans-serif",
                    size=14,
                    color="#333"
                ),
                xaxis=dict(title="Unit"),
                yaxis=dict(title="Equivalent Value")
            )
            
            st.plotly_chart(comparison_fig, use_container_width=True)

# Batch Conversion Mode
elif app_mode == "Batch Conversion":
    st.markdown("<h2>Batch Conversion Tool</h2>", unsafe_allow_html=True)
    st.markdown("<p>Convert multiple values at once - perfect for data processing and analysis.</p>", unsafe_allow_html=True)
    
    # Category selection
    category = st.selectbox("Select category", list(categories.keys()))
    
    # Get units for selected category
    units = list(categories[category].keys())
    
    col1, col2 = st.columns(2)
    
    with col1:
        from_unit = st.selectbox("From Unit", units)
    
    with col2:
        to_unit = st.selectbox("To Unit", units, index=1 if len(units) > 1 else 0)
    
    # Create a text area for manual entry
    values_input = st.text_area(
        "Enter values (one per line):",
        height=200,
        help="Enter one value per line. Example:\n1\n2\n3.5\n10.5"
    )
    
    if st.button("Convert Values"):
        if values_input:
            try:
                # Parse input values
                input_values = []
                for line in values_input.strip().split('\n'):
                    if line.strip():
                        input_values.append(float(line.strip()))
                
                # Convert values
                converted_values = []
                for val in input_values:
                    if category == "Temperature":
                        converted = convert_temperature(val, from_unit, to_unit)
                    else:
                        converted = convert(val, from_unit, to_unit, category, categories[category])
                    converted_values.append(converted)
                
                # Create results dataframe
                results_df = pd.DataFrame({
                    f"Value ({from_unit})": input_values,
                    f"Converted ({to_unit})": converted_values
                })
                
                # Display results
                st.markdown("<h3>Conversion Results</h3>", unsafe_allow_html=True)
                st.dataframe(results_df)
                
                # Add download button for results
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="batch_conversion_results.csv",
                    mime="text/csv",
                )
                
                # Save the first conversion to history
                if input_values:
                    save_to_history(category, input_values[0], from_unit, converted_values[0], to_unit)
                
            except ValueError:
                st.error("Please enter valid numeric values, one per line.")
        else:
            st.warning("Please enter values to convert.")

# Student Mode
elif app_mode == "For Students":
    st.markdown("<h2>Student Learning Mode</h2>", unsafe_allow_html=True)
    st.markdown("<p>Learn about unit conversions with helpful explanations and examples.</p>", unsafe_allow_html=True)
    
    # Category selection
    category = st.selectbox("Select category to learn about", list(categories.keys()))
    
    # Display educational content
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>Understanding {category} Conversions</h3>", unsafe_allow_html=True)
    
    # Display tip for students
    if category in student_tips:
        st.info(student_tips[category])
    
    # Get units for selected category
    units = list(categories[category].keys())
    
    # Create two columns for input and output
    col1, col2 = st.columns(2)
    
    with col1:
        from_value = st.number_input("Value", value=1.0, format=f"%.{decimal_places}f")
        from_unit = st.selectbox("From", units)
    
    with col2:
        to_unit = st.selectbox("To", units, index=1 if len(units) > 1 else 0)
        
        # Calculate the result
        if category == "Temperature":
            result = convert_temperature(from_value, from_unit, to_unit)
        else:
            result = convert(from_value, from_unit, to_unit, category, categories[category])
        
        # Display the result
        st.markdown(f"<h3>{result:.{decimal_places}g} {to_unit}</h3>", unsafe_allow_html=True)
    
    # Display the formula
    st.markdown("<h4>Conversion Formula:</h4>", unsafe_allow_html=True)
    formula = get_formula(from_unit, to_unit, category, from_value, result)
    st.markdown(f"<p>{formula}</p>", unsafe_allow_html=True)
    
    # Show step-by-step calculation
    st.markdown("<h4>Step-by-Step Calculation:</h4>", unsafe_allow_html=True)
    
    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            st.markdown(f"1. Multiply {from_value} by 9/5: {from_value * 9/5}")
            st.markdown(f"2. Add 32: {from_value * 9/5} + 32 = {result}")
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            st.markdown(f"1. Add 273.15 to {from_value}: {from_value} + 273.15 = {result}")
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            st.markdown(f"1. Subtract 32 from {from_value}: {from_value} - 32 = {from_value - 32}")
            st.markdown(f"2. Multiply by 5/9: ({from_value} - 32) × 5/9 = {result}")
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            st.markdown(f"1. Subtract 32 from {from_value}: {from_value} - 32 = {from_value - 32}")
            st.markdown(f"2. Multiply by 5/9: ({from_value} - 32) × 5/9 = {(from_value - 32) * 5/9}")
            st.markdown(f"3. Add 273.15: ({from_value} - 32) × 5/9 + 273.15 = {result}")
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            st.markdown(f"1. Subtract 273.15 from {from_value}: {from_value} - 273.15 = {result}")
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            st.markdown(f"1. Subtract 273.15 from {from_value}: {from_value} - 273.15 = {from_value - 273.15}")
            st.markdown(f"2. Multiply by 9/5: ({from_value} - 273.15) × 9/5 = {(from_value - 273.15) * 9/5}")
            st.markdown(f"3. Add 32: ({from_value} - 273.15) × 9/5 + 32 = {result}")
    else:
        if from_unit == to_unit:
            st.markdown("No conversion needed for same units.")
        else:
            conversion_dict = categories[category]
            # Convert to base unit
            base_value = from_value / conversion_dict[from_unit]
            st.markdown(f"1. Convert {from_value} {from_unit} to the base unit: {from_value} ÷ {conversion_dict[from_unit]} = {base_value} {list(conversion_dict.keys())[0]}")
            
            # Convert from base unit to target unit
            st.markdown(f"2. Convert from base unit to {to_unit}: {base_value} × {conversion_dict[to_unit]} = {result} {to_unit}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Practice problems
    st.markdown("<h3>Practice Problems</h3>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    if 'practice_problems' not in st.session_state:
        # Generate practice problems
        st.session_state.practice_problems = []
        
        for i in range(3):
            if category == "Temperature":
                problem_value = np.random.randint(1, 100)
                from_idx = np.random.randint(0, len(units))
                to_idx = (from_idx + 1 + np.random.randint(0, len(units) - 1)) % len(units)
            else:
                problem_value = np.random.randint(1, 100)
                from_idx = np.random.randint(0, len(units))
                to_idx = (from_idx + 1 + np.random.randint(0, len(units) - 1)) % len(units)
            
            problem_from_unit = units[from_idx]
            problem_to_unit = units[to_idx]
            
            if category == "Temperature":
                answer = convert_temperature(problem_value, problem_from_unit, problem_to_unit)
            else:
                answer = convert(problem_value, problem_from_unit, problem_to_unit, category, categories[category])
            
            st.session_state.practice_problems.append({
                "value": problem_value,
                "from_unit": problem_from_unit,
                "to_unit": problem_to_unit,
                "answer": answer
            })
    
    # Display practice problems
    for i, problem in enumerate(st.session_state.practice_problems):
        st.markdown(f"**Problem {i+1}:** Convert {problem['value']} {problem['from_unit']} to {problem['to_unit']}")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_answer = st.number_input(f"Your answer for Problem {i+1}", format=f"%.{decimal_places}f")

# Custom footer with animation
st.markdown("""
<footer>
    <p>Unit Converter Pro - Created with ❤️ | © 2023 All Rights Reserved</p>
    <p>Powered by advanced conversion algorithms and animated with GSAP</p>
</footer>
""", unsafe_allow_html=True)




