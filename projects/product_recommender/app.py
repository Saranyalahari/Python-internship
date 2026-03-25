import streamlit as st
import pandas as pd
from recommender import hybrid_recommend

# Load products
products = pd.read_csv("data/products.csv")

st.title("🛒 Product Recommendation System")

product_list = products['name'].tolist()

selected_product = st.selectbox("Select a Product", product_list)

if st.button("Recommend"):
    recommendations = hybrid_recommend(selected_product)

    if len(recommendations) == 0:
        st.write("No recommendations found.")
    else:
        st.subheader("Recommended Products")

        for _, row in recommendations.iterrows():
            st.image(row['image'], width=100)
            st.write(f"**{row['name']}**")
            st.write(row['description'])
            st.write("---")

        # Export to CSV
        recommendations.to_csv("recommended_products.csv", index=False)
        st.success("Recommendations saved to CSV!")