import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1), key="analytics_start_date")

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5), key="analytics_end_date")

    if st.button("Get Analytics", key="analytics_button"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analytics/", json=payload)
        if response.status_code == 200:
            try:
                response_json = response.json()
            except requests.exceptions.JSONDecodeError:
                st.error("Failed to decode JSON response from server.")
                st.text(f"Raw response: {response.text}")
                return
        else:
            st.error(f"Request failed with status code {response.status_code}")
            st.text(f"Response: {response.text}")
            return
        data = {
            "Category": list(response_json.keys()),
            "Total": [response_json[category]["total"] for category in response_json],
            "Percentage": [response_json[category]["percentage"] for category in response_json]
        }
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Percentage", ascending=False)
        st.title("Expense Breakdown By Category")
        st.bar_chart(data=df_sorted.set_index("Category")['Percentage'], width=0, height=0, use_container_width=True)
        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)
        st.table(df_sorted)



