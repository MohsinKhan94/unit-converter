import streamlit as st

st.title("Plotly Import Test")

try:
    import plotly
    st.success(f"✅ Plotly base package imported successfully. Version: {plotly.__version__}")
except Exception as e:
    st.error(f"❌ Failed to import plotly: {str(e)}")

try:
    import plotly.express as px
    st.success(f"✅ Plotly Express imported successfully.")
    
    # Create a simple plot to verify functionality
    import pandas as pd
    import numpy as np
    
    # Sample data
    df = pd.DataFrame({
        'x': range(10),
        'y': np.random.randn(10)
    })
    
    # Create and display plot
    fig = px.line(df, x='x', y='y', title='Test Plot')
    st.plotly_chart(fig)
    
except Exception as e:
    st.error(f"❌ Failed to import plotly.express: {str(e)}")

st.write("If you see this message, the app is running even if some imports failed.") 