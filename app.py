import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Sales Dashboard")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    """Load sales data from CSV file"""
    df = pd.read_csv('lesson-setup/data/sales.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
    return df

try:
    df = load_data()

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Sales", f"${df['Sales'].sum():,.2f}")

    with col2:
        st.metric("Total Orders", f"{len(df):,}")

    with col3:
        st.metric("Total Products", f"{df['Product ID'].nunique():,}")

    with col4:
        st.metric("Avg Order Value", f"${df['Sales'].mean():,.2f}")

    st.markdown("---")

    # Display sample data
    st.subheader("📋 Sales Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # Simple visualization
    st.markdown("---")
    st.subheader("📈 Sales by Category")

    category_sales = df.groupby('Category')['Sales'].sum().reset_index()
    fig = px.bar(
        category_sales,
        x='Category',
        y='Sales',
        title='Total Sales by Category',
        labels={'Sales': 'Sales Amount ($)', 'Category': 'Category'},
        color='Category'
    )
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("❌ Error: lesson-setup/data/sales.csv not found. Please ensure the file exists in the data directory.")
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")

# Footer
st.markdown("---")
st.caption("Sales Dashboard - Built with Streamlit")
