import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# ---------------- TITLE ----------------
st.title("📊 Retail-Sales-Intelligence-Revenue-Optimization-Dashboard")
st.markdown("Interactive dashboard with dynamic business insights")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("Data/cleaned_sales_data.csv")
df['order_date'] = pd.to_datetime(df['order_date'])

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Select Region",
    df['region'].unique(),
    default=df['region'].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    df['category'].unique(),
    default=df['category'].unique()
)

# Apply filters
filtered_df = df[
    (df['region'].isin(region)) &
    (df['category'].isin(category))
]

# ---------------- EMPTY DATA CHECK ----------------
if filtered_df.empty:
    st.error("⚠️ No data available for selected filters. Please adjust filters.")
    st.stop()

# ---------------- KPIs ----------------
total_revenue = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
avg_order_value = filtered_df['sales'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue", f"₹{total_revenue/1e7:.2f} Cr")
col2.metric("📈 Profit", f"₹{total_profit/1e7:.2f} Cr")
col3.metric("🧾 Avg Order Value", f"₹{avg_order_value:,.0f}")

st.markdown("---")

# ---------------- MONTHLY TREND ----------------
st.subheader("📈 Monthly Sales Trend")

filtered_df['month'] = filtered_df['order_date'].dt.to_period('M').astype(str)

monthly_sales = filtered_df.groupby('month')['sales'].sum().reset_index()

fig1 = px.line(
    monthly_sales,
    x='month',
    y='sales',
    markers=True,
    title="Sales Trend Over Time"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- TOP PRODUCTS ----------------
st.subheader("🔥 Top Products")

top_products = filtered_df.groupby('product')['sales'].sum().sort_values(ascending=False).head(5).reset_index()

fig2 = px.bar(
    top_products,
    x='sales',
    y='product',
    orientation='h',
    text='sales',
    title="Top 5 Revenue Generating Products"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- REGION PERFORMANCE ----------------
st.subheader("🌍 Region Performance")

region_sales = filtered_df.groupby('region')['sales'].sum().reset_index()

fig3 = px.bar(
    region_sales,
    x='region',
    y='sales',
    text='sales',
    title="Revenue by Region"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.markdown("## 💡 Key Business Insights")

# 🔥 Top Product Insight
if not top_products.empty:
    top_product = top_products.iloc[0]['product']

    st.success(f"""
    🔥 Top Revenue Driver: **{top_product}**

    👉 This product generates the highest revenue.
    👉 Focus marketing & inventory on this product.
    """)

# 📉 Growth Insight
if len(monthly_sales) > 1:
    growth = monthly_sales['sales'].pct_change().mean()

    if growth < 0:
        st.warning("""
        ⚠️ Sales Growth is slightly declining.

        👉 Possible reasons:
        - Demand drop
        - Seasonality
        - Competition

        👉 Action: Analyze low-performing months.
        """)
    else:
        st.success("📈 Sales are growing steadily.")

# 💰 Discount Insight
avg_profit_by_discount = filtered_df.groupby('discount')['profit'].mean()

if not avg_profit_by_discount.empty:
    best_discount = avg_profit_by_discount.idxmax()

    st.info(f"""
    💰 Optimal Discount Strategy:

    👉 {best_discount}% discount gives highest average profit.

    👉 Avoid heavy discounts → reduces profitability.
    """)
