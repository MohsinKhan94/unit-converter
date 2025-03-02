import plotly.express as px
import plotly
import pandas as pd
import numpy as np

# Print versions
print(f"Plotly version: {plotly.__version__}")
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")

# Create a simple plot
df = pd.DataFrame({
    'x': np.arange(10),
    'y': np.random.randn(10)
})

fig = px.line(df, x='x', y='y', title='Test Plot')
print("Successfully created a plot!")

# Try to save the plot to HTML to verify it works
fig.write_html("test_plot.html")
print("Successfully saved plot to HTML!") 