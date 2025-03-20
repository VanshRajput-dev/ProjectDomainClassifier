import streamlit as st
import requests
import pandas as pd
import time

# 🔹 Page Configuration
st.set_page_config(page_title="Find It Right", page_icon="🔍", layout="wide")

# 🔹 Styling
st.markdown("""
    <style>
        body { background-color: #121212; } /* Dark background */
        .investor-card {
            background-color: #f7f7f7; /* Soft gray */
            color: #2c3e50; /* Darker text */
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 12px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .investor-card a { color: #1a73e8; }
        .investor-card a:hover { text-decoration: underline; }
    </style>
""", unsafe_allow_html=True)

# 🔹 Initialize Session State
if "predicted_domains" not in st.session_state:
    st.session_state.predicted_domains = []
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = None
if "chat_investor_id" not in st.session_state:
    st.session_state.chat_investor_id = None
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False

# 🔹 Title & Description
st.markdown('<p class="big-title">🔍 Find It Right</p>', unsafe_allow_html=True)
st.markdown('<p class="subtext">💡 AI-powered platform to match projects with the best investors!</p>', unsafe_allow_html=True)
st.write("---")

# 🔹 Text Input for Project Description
description = st.text_area("📌 Project Description:", height=150, placeholder="Describe your startup idea...")

# 🔹 Predict Button
if st.button("🚀 Predict Domain", use_container_width=True):
    description = description.strip()

    if description:
        with st.spinner("🔍 Analyzing your project..."):
            try:
                response = requests.post("http://127.0.0.1:8000/predict/", json={"description": description}, timeout=10)
                response.raise_for_status()

                result = response.json()
                st.session_state.predicted_domains = result.get("predicted_domains", [])

                if st.session_state.predicted_domains:
                    st.success("✅ Prediction Successful!")
                else:
                    st.warning("⚠ No domains were predicted. Try providing more details.")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Prediction API Request Failed: {e}")
    else:
        st.warning("⚠ Please enter a project description before predicting.")

# 🔹 Domain Selection Buttons
if st.session_state.predicted_domains:
    st.write("### 🎯 Select a Domain:")
    col1, col2, col3 = st.columns(3)

    for i, domain in enumerate(st.session_state.predicted_domains[:3]):  # Show only top 3 domains
        if (i == 0 and col1.button(domain, key=f"btn_{i}", use_container_width=True)) or \
           (i == 1 and col2.button(domain, key=f"btn_{i}", use_container_width=True)) or \
           (i == 2 and col3.button(domain, key=f"btn_{i}", use_container_width=True)):
            st.session_state.selected_domain = domain

# 🔹 Find Investors Button
if st.session_state.selected_domain:
    st.write(f"✅ Selected Domain: *{st.session_state.selected_domain}*")

    if st.button("🔎 Find Investors", use_container_width=True):
        with st.spinner("🔍 Finding top investors..."):
            try:
                investor_response = requests.post(
                    "http://127.0.0.1:8000/investors/",
                    json={"selected_domain": st.session_state.selected_domain},
                    timeout=50
                )
                investor_response.raise_for_status()

                investors = investor_response.json()

                if "message" in investors:
                    st.warning("⚠ " + investors["message"])
                else:
                    st.subheader("📋 Top Matching Investors")

                    # 🔹 Convert JSON to DataFrame
                    investors_df = pd.DataFrame(investors)

                    if not investors_df.empty:
                        for _, investor in investors_df.iterrows():
                            col1, col2, col3 = st.columns([2, 1, 1])

                            with col1:
                                st.markdown(f"""
                                    <div class='investor-card'>
                                    <h4>{investor.get("investor_name", "N/A")} ({investor.get("investor_company", "N/A")})</h4>
                                    <p><b>Experience:</b> {investor.get("investor_experience(years)", "N/A")} years | 
                                    <b>Investments:</b> {investor.get("no_of_companies_invested", "N/A")}</p>
                                    <p><b>Funds Available:</b> {investor.get("funds_available", "🔸 Not Disclosed")}</p>
                                    <p><a href='{investor.get("linkedin_url", "#")}' target='_blank'>🔗 LinkedIn</a> | 
                                    ✉ <a href='mailto:{investor.get("email", "#")}'>{investor.get("email", "N/A")}</a></p>
                                    </div>
                                """, unsafe_allow_html=True)

                            with col2:
                                match_score = investor.get("match_score", 0)
                                st.progress(min(1.0, match_score / 100))  # Keep progress bar valid

                            with col3:
                                investor_id = investor.get("investor_id", f"default_{_}")  # Ensure unique key
                                if investor_id:  # Only create button if investor_id is valid
                                    if st.button(f"💬 Chat", key=f"chat_{investor_id}", use_container_width=True):
                                        st.session_state.chat_investor_id = investor_id

                                    st.session_state.chat_investor_id = investor.get("investor_id")

                    else:
                        st.warning("⚠ No matching investors found.")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Investor API Request Failed: {e}")

# 🔹 Chat Section
if st.session_state.chat_investor_id:
    st.write(f"🗨 Chatting with Investor ID: *{st.session_state.chat_investor_id}*")

    # Auto-refresh toggle
    st.session_state.auto_refresh = st.checkbox("🔄 Auto Refresh Chat", value=st.session_state.auto_refresh)

    # Fetch Chat Messages
    try:
        chat_response = requests.get(
            f"http://127.0.0.1:8000/get_messages/{st.session_state.chat_investor_id}",
            timeout=10
        )
        chat_response.raise_for_status()
        chat_messages = chat_response.json().get("messages", [])
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to load messages: {e}")
        chat_messages = []

    # Display Messages
    chat_box = st.container()
    with chat_box:
        for msg in chat_messages:
            sender = "👤 You" if msg["sender"] == "fundraiser" else "💼 Investor"
            st.chat_message(sender, msg['message'])

    # Message Input
    new_message = st.text_input("💬 Type your message...")

    if st.button("Send"):
        if new_message.strip():
            try:
                send_response = requests.post(
                    "http://127.0.0.1:8000/send_message/",
                    json={"investor_id": st.session_state.chat_investor_id, "sender": "fundraiser", "message": new_message},
                    timeout=10
                )
                send_response.raise_for_status()
                st.experimental_rerun()  # Refresh chat messages
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Message sending failed: {e}")

    # Auto refresh chat messages
    if st.session_state.auto_refresh:
        time.sleep(5)
        st.experimental_rerun()