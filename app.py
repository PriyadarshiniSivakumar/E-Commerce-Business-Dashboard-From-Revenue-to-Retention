import streamlit as st
import pandas as pd
import plotly.express as px


file_path = "ecommerce_reports.xlsx"   
all_data = pd.read_excel(file_path, sheet_name="AllData")
retention_data = pd.read_excel(file_path, sheet_name="Retention")

all_data["FirstPurchase"] = pd.to_datetime(all_data["FirstPurchase"], errors="coerce")
all_data["LastPurchase"] = pd.to_datetime(all_data["LastPurchase"], errors="coerce")

all_data["Ratings"] = pd.to_numeric(all_data["Ratings"], errors="coerce").fillna(0)

st.title("📊 E-commerce Customer Dashboard")

customer_id = st.text_input("🔍 Enter Customer ID:", "")

if customer_id:
    try:
        customer_id = int(customer_id)
        customer_info = all_data[all_data["Customer_ID"] == customer_id]

        if not customer_info.empty:
            st.subheader(f"Customer Profile: {customer_info.iloc[0]['Name']}")
            st.write(customer_info[["Customer_ID", "Name", "Email", "City", "State", "Country", "Customer_Type"]])

          
            purchase_count = customer_info.shape[0]
            avg_rating = customer_info["Ratings"].mean()

            if purchase_count > 5:
                segment = "🔁 Loyal Customer"
            else:
                segment = "🆕 New / Low Engagement"

            
            col1, col2 = st.columns(2)
            col1.metric("Purchases", purchase_count)
            col2.metric("Avg Rating", f"{avg_rating:.1f}")
            st.success(f"Customer Segment: {segment}")

            
            st.subheader("📆 Customer Purchase Timeline")

            if "LastPurchase" in customer_info.columns:
              
                timeline = customer_info.sort_values("LastPurchase")
                fig_timeline = px.line(
                    timeline,
                    x="LastPurchase",
                    y=timeline.index, 
                    markers=True,
                    title="Purchases Over Time"
                )
                st.plotly_chart(fig_timeline, use_container_width=True)

            st.subheader("⭐ Ratings Trend")
            fig_ratings = px.scatter(
                customer_info.sort_values("LastPurchase"),
                x="LastPurchase",
                y="Ratings",
                color="Ratings",
                title="Ratings Across Purchases"
            )
            st.plotly_chart(fig_ratings, use_container_width=True)

            st.subheader("🛍️ Category-Wise Purchases")
            fig_category = px.pie(
                customer_info,
                names="Product_Category",
                title="Purchases by Product Category"
            )
            st.plotly_chart(fig_category, use_container_width=True)

        else:
            st.warning("❌ Customer ID not found!")

    except ValueError:
        st.error("Please enter a valid numeric Customer ID.")

st.subheader("📈 Category Retention Performance")
fig = px.bar(
    retention_data.melt(id_vars="Product_Category", var_name="Status", value_name="Count"),
    x="Product_Category", y="Count", color="Status", barmode="group",
    title="Retention by Product Category"
)
st.plotly_chart(fig, use_container_width=True)
