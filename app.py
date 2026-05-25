import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(layout="wide")

# Custom padding
st.markdown(
    """
    <style>
    div.block-container {
        padding-top: 1rem;
    }

    .title-text {
        font-weight: bold;
        padding: 5px;
        border-radius: 6px;
        text-align: center;
        font-size: 40px;
        color: #111;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Reading the Excel file
df = pd.read_excel("Adidas.xlsx", header=4)

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Open image
image = Image.open('adidas-logo.jpeg')

# Top section
col1, col2 = st.columns([0.1, 0.9])

with col1:
    st.image(image, width=100)

with col2:
    html_title = """
    <h1 class="title-text">
        Adidas Interactive Sales Dashboard
    </h1>
    """
    st.markdown(html_title, unsafe_allow_html=True)

# Date and chart section
col3, col4, col5 = st.columns([0.2, 0.6, 0.2])

with col3:
    box_date = datetime.datetime.now().strftime("%d %B %Y")

    st.markdown(f"""
    ### Last Updated
    {box_date}
    """)

with col4:

    # Bar chart
    fig = px.bar(
        df,
        x="Retailer",
        y="Units Sold",
        labels={"Units Sold": "Units Sold"},
        title="Units Sold by Retailer",
        hover_data=["Units Sold"],
        template="plotly_white",
        height=500,
        color="Retailer"
    )

    st.plotly_chart(fig, use_container_width=True)

# Bottom section
_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])

with view1:
    expander = st.expander("Retailer Wise Sales")

    data = df[["Retailer", "Units Sold"]].groupby(by="Retailer").sum()

expander.dataframe(data)

with dwn1:
    st.download_button(
        "Get Data",
        data=data.to_csv().encode("utf-8"),
        file_name="RetailerSales.csv",
        mime="text/csv"
    )

# Convert Invoice Date column into datetime
df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])

# Create Month-Year column
df["Month_Year"] = df["Invoice Date"].dt.strftime("%b'%y")

# Group data
result = df.groupby(by="Month_Year")["Units Sold"].sum().reset_index()

with col5:

    fig1 = px.line(
        result,
        x="Month_Year",
        y="Units Sold",
        title="Units Sold Over Time",
        template="plotly_white"
    )

    st.plotly_chart(fig1, use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)

with dwn2:
    st.download_button(
        "Get Data",
        data=result.to_csv().encode("utf-8"),
        file_name="Monthly Sales.csv",
        mime="text/csv"
    )
    st.divider()
# Group the data state-wise
result1 = df.groupby(by="State")[["Units Sold"]].sum().reset_index()

# Create figure
fig3 = go.Figure()

# Add bar chart
fig3.add_trace(
    go.Bar(
        x=result1["State"],
        y=result1["Units Sold"],
        name="Units Sold"
    )
)

# Add line chart
fig3.add_trace(
    go.Scatter(
        x=result1["State"],
        y=result1["Units Sold"],
        mode="lines+markers",
        name="Units Sold Trend",
        yaxis="y2"
    )
)

# Update layout
fig3.update_layout(
    title="Units Sold by State",

    # X-axis title
    xaxis=dict(title="State"),

    # Primary Y-axis
    yaxis=dict(
        title="Units Sold",
        showgrid=False
    ),

    # Secondary Y-axis
    yaxis2=dict(
        title="Units Sold Trend",
        overlaying="y",
        side="right"
    ),

    template="plotly_white",

    legend=dict(x=1, y=1)
)

# Create column layout
_, col6 = st.columns([0.1, 1])

# Display chart
with col6:
    st.plotly_chart(fig3, use_container_width=True)

 # Create columns layout
_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])

# View data inside expander
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)

# Download CSV file
with dwn3:
    st.download_button(
        "Get Data",
        data=result1.to_csv().encode("utf-8"),
        file_name="Sales_by_UnitsSold.csv",
        mime="text/csv"
    )

# Add divider line
st.divider()
# Create column layout
_, col7 = st.columns([0.1, 1])

# Group the data by Region and City
treemap = df[["Region", "City", "Units Sold"]].groupby(
    by=["Region", "City"]
)["Units Sold"].sum().reset_index()

# Function to format sales values
def format_sales(value):
    if value >= 1000:
        return '{:.2f} K'.format(value / 1000)

    return str(value)

# Create formatted column
treemap["Units Sold (Formatted)"] = treemap["Units Sold"].apply(format_sales)

# Create treemap chart
fig4 = px.treemap(
    treemap,

    # Treemap hierarchy
    path=["Region", "City"],

    # Values for chart
    values="Units Sold",

    # Hover information
    hover_name="Units Sold (Formatted)",
    hover_data=["Units Sold (Formatted)"],

    # Chart styling
    color="City",
    height=700,
    width=600
)

# Show labels and values inside treemap
fig4.update_traces(textinfo="label+value")

# Display chart
with col7:
    st.subheader(":point_right: Units Sold by Region and City in Treemap")

    st.plotly_chart(fig4, use_container_width=True)

    # Create columns layout
_, view4, dwn4 = st.columns([0.5, 0.45, 0.45])

# View data section
with view4:

    # Group data by Region and City
    result2 = df[["Region", "City", "Units Sold"]].groupby(
        by=["Region", "City"]
    )["Units Sold"].sum().reset_index()

    # Create expander
    expander = st.expander("View Data for Units Sold by Region and City")

    # Display data
    expander.write(result2)

# Download section
with dwn4:

    st.download_button(
        "Get Data",
        data=result2.to_csv(index=False).encode("utf-8"),
        file_name="Sales_by_Region.csv",
        mime="text/csv"
    )

    # Create columns layout
_, view5, dwn5 = st.columns([0.5, 0.45, 0.45])

# View raw data section
with view5:

    # Create expander
    expander = st.expander("View Sales Raw Data")

    # Display dataframe
    expander.write(df)

# Download raw data section
with dwn5:

    st.download_button(
        "Get Raw Data",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="SalesRawData.csv",
        mime="text/csv"
    )

# Add divider line
st.divider()