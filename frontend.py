import streamlit as st
import requests
import pandas as pd
import time

# 🔹 Page Configuration
st.set_page_config(page_title="Find It Right", page_icon="🔍", layout="wide")

# 🔹 Enhanced Styling
st.markdown("""
    <style>
        /* Main Theme Colors */
        :root {
            --primary-color: #4361ee;
            --secondary-color: #3f37c9;
            --accent-color: #4cc9f0;
            --text-color: #2b2d42;
            --card-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            --gradient-bg: linear-gradient(135deg, #4361ee, #3a0ca3);
        }
        
        /* Title and subtitle */
        .big-title {
            font-size: 70px;
            font-weight: 800;
            background: var(--gradient-bg);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-align: center;
            letter-spacing: 1px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .subtext {
            font-size: 20px;
            color: #6c757d;
            margin-top: 5px;
            text-align: center;
            font-weight: 300;
        }
        
        /* Investor Cards */
        .investor-card {
            background-color: white;
            color: var(--text-color);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: var(--card-shadow);
            transition: transform 0.3s ease;
            border-left: 5px solid var(--primary-color);
            position: relative;
        }
        
        .investor-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        }
        
        .investor-card h4 {
            color: var(--primary-color);
            font-weight: 700;
            font-size: 22px;
            margin-bottom: 12px;
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 8px;
        }
        
        .investor-card p {
            margin-bottom: 15px;
            line-height: 1.6;
        }
        
        .investor-card a {
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }
        
        .investor-card a:hover {
            color: var(--secondary-color);
            text-decoration: none;
        }
        
        /* Buttons */
        .stButton > button {
            background: var(--gradient-bg) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 10px 20px !important;
            font-weight: 600 !important;
            transition: all 0.3s !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Progress Bar */
        .stProgress > div > div > div {
            background-color: #dc3545 !important; /* Red progress bar */
            height: 10px !important;
            border-radius: 10px !important;
        }
        
        .stProgress > div > div {
            background-color: #e9ecef !important;
            border-radius: 10px !important;
        }
        
        /* Chat styling */
        .chat-message {
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 10px;
            display: inline-block;
            max-width: 70%;
        }
        
        .user-message {
            background-color: rgba(67, 97, 238, 0.1);
            float: right;
            margin-left: 30%;
        }
        
        .investor-message {
            background-color: #f0f0f0;
            float: left;
        }
        
        /* Messages and alerts */
        .success-box {
            background-color: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #28a745;
            margin: 15px 0;
        }
        
        .warning-box {
            background-color: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #ffc107;
            margin: 15px 0;
        }
        
        .error-box {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #dc3545;
            margin: 15px 0;
        }
        
        /* Domain badge */
        .domain-badge {
            display: inline-block;
            background: var(--gradient-bg);
            color: white;
            font-weight: bold;
            padding: 8px 20px;
            border-radius: 30px;
            margin-top: 10px;
            font-size: 16px;
        }
        
        /* Match badge */
        .match-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: var(--gradient-bg);
            color: white;
            font-weight: bold;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 13px;
        }
        
        /* Input fields */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            border-radius: 12px !important;
            border: 2px solid #e0e0e0 !important;
            padding: 12px !important;
        }
        
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.2) !important;
        }
        
        /* Chat interface */
        .chat-container {
            background-color: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: var(--card-shadow);
            margin-bottom: 20px;
            max-height: 400px;
            overflow-y: auto;
            border-left: 5px solid var(--primary-color);
        }
    </style>
""", unsafe_allow_html=True)

# 🔹 Helper Functions
def show_message(message, type="info"):
    """Show styled message box"""
    if type == "success":
        st.markdown(f'<div class="success-box"><b>✅ Success:</b> {message}</div>', unsafe_allow_html=True)
    elif type == "warning":
        st.markdown(f'<div class="warning-box"><b>⚠ Warning:</b> {message}</div>', unsafe_allow_html=True)
    elif type == "error":
        st.markdown(f'<div class="error-box"><b>❌ Error:</b> {message}</div>', unsafe_allow_html=True)
    else:
        st.info(message)

def format_funds(funds):
    """Format funds display"""
    try:
        funds_str = str(funds).replace(',', '').replace('$', '').strip().upper()
        if "M" in funds_str:
            return f"${float(funds_str.replace('M', '')) * 1_000_000:,.0f}"
        elif "B" in funds_str:
            return f"${float(funds_str.replace('B', '')) * 1_000_000_000:,.0f}"
        else:
            return f"${float(funds_str):,.0f}"
    except:
        return "🔸 Not Disclosed"

# 🔹 Initialize Session State
if "predicted_domains" not in st.session_state:
    st.session_state.predicted_domains = []
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = None
if "chat_investor_id" not in st.session_state:
    st.session_state.chat_investor_id = None
if "chat_investor_name" not in st.session_state:
    st.session_state.chat_investor_name = None
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False
if "view" not in st.session_state:
    st.session_state.view = "main"  # 'main' or 'chat'

# Function to handle chat button clicks
def open_chat(investor_id, investor_name):
    st.session_state.chat_investor_id = investor_id
    st.session_state.chat_investor_name = investor_name
    st.session_state.view = "chat"

# Function to go back to main view
def back_to_main():
    st.session_state.view = "main"

# 🔹 Title & Description
st.markdown('<p class="big-title"><b>🔍 Find It Right</b></p>', unsafe_allow_html=True)
st.markdown('<p class="subtext">💡 AI-powered platform to match projects with the best investors!</p>', unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# 🔹 Main App Interface
if st.session_state.view == "chat":
    # Chat Interface
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"""
            <h3 style="color: #4361ee;">
                <span style="display: inline-block; background: linear-gradient(135deg, #4361ee, #3a0ca3); 
                      color: white; border-radius: 50%; width: 32px; height: 32px; text-align: center; 
                      line-height: 32px; margin-right: 10px;">
                    {st.session_state.chat_investor_name[0].upper() if st.session_state.chat_investor_name else "?"}
                </span>
                Chat with {st.session_state.chat_investor_name}
            </h3>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("↩ Back", key="back_btn"):
            back_to_main()
    
    # Auto-refresh toggle
    st.session_state.auto_refresh = st.checkbox("🔄 Auto Refresh Chat", value=st.session_state.auto_refresh)
    
    # Fetch and display messages
    try:
        chat_response = requests.get(
            f"http://127.0.0.1:8000/get_messages/{st.session_state.chat_investor_id}",
            timeout=10
        )
        chat_response.raise_for_status()
        chat_messages = chat_response.json().get("messages", [])
    except requests.exceptions.RequestException as e:
        show_message(f"Failed to load messages: {e}", "error")
        chat_messages = []
    
    # Display chat messages
    if chat_messages:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in chat_messages:
            sender = "You" if msg["sender"] == "fundraiser" else st.session_state.chat_investor_name
            sender_icon = "👤" if msg["sender"] == "fundraiser" else "💼"
            message_class = "user-message" if msg["sender"] == "fundraiser" else "investor-message"
            
            st.markdown(f"""
                <div class="chat-message {message_class}">
                    <div><b>{sender_icon} {sender}</b></div>
                    <div>{msg['message']}</div>
                </div>
                <div style="clear: both;"></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 40px 0; color: #6c757d;">
                <div style="font-size: 48px; margin-bottom: 10px;">💬</div>
                <p>No messages yet. Start the conversation!</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Message input
    col1, col2 = st.columns([4, 1])
    with col1:
        new_message = st.text_input("Type your message", placeholder="Type your message here...")
    with col2:
        if st.button("Send", use_container_width=True):
            if new_message.strip():
                try:
                    with st.spinner("Sending..."):
                        send_response = requests.post(
                            "http://127.0.0.1:8000/send_message/",
                            json={"investor_id": st.session_state.chat_investor_id, "sender": "fundraiser", "message": new_message},
                            timeout=10
                        )
                        send_response.raise_for_status()
                        st.experimental_rerun()
                except requests.exceptions.RequestException as e:
                    show_message(f"Message sending failed: {e}", "error")
    
    # Auto refresh
    if st.session_state.auto_refresh:
        time.sleep(3)
        st.experimental_rerun()

else:
    # Main Interface
    # Project description input box with heading
    st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 16px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); 
                margin: 15px 0; border-left: 5px solid #4361ee;">
            <h3 style="margin-top: 0; color: #4361ee;">📌 Tell us about your project</h3>
            <p style="margin-bottom: 10px; color: #6c757d;">
                The more details you provide, the better we can match you with suitable investors.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    description = st.text_area("Project Description", height=150, placeholder="Describe your startup idea...")
    
    # Predict button centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Predict Domain", use_container_width=True):
            description = description.strip()
            
            if description:
                with st.spinner("🔍 Analyzing your project..."):
                    try:
                        response = requests.post(
                            "http://127.0.0.1:8000/predict/", 
                            json={"description": description}, 
                            timeout=10
                        )
                        response.raise_for_status()
                        
                        result = response.json()
                        st.session_state.predicted_domains = result.get("predicted_domains", [])
                        
                        if st.session_state.predicted_domains:
                            show_message("Prediction successful! Choose a domain below.", "success")
                        else:
                            show_message("No domains were predicted. Try providing more details.", "warning")
                    except requests.exceptions.RequestException as e:
                        show_message(f"Prediction API Request Failed: {e}", "error")
            else:
                show_message("Please enter a project description before predicting.", "warning")
    
    # Domain selection with icons
    if st.session_state.predicted_domains:
        st.markdown("""
            <h3 style="text-align: center; color: #4361ee; margin: 25px 0 15px 0;">
                🎯 Select the Best Match for Your Project
            </h3>
        """, unsafe_allow_html=True)
        
        # Domain icons dictionary
        domain_icons = {
            "Technology": "💻", "Healthcare": "🏥", "Finance": "💰", 
            "Education": "📚", "E-commerce": "🛒", "Real Estate": "🏢",
            "Food": "🍽", "Travel": "✈", "Entertainment": "🎬"
        }
        
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for i, domain in enumerate(st.session_state.predicted_domains[:3]):
            icon = domain_icons.get(domain, "🔍")
            with cols[i]:
                st.markdown(f"""
                    <div style="background-color: white; padding: 15px; border-radius: 16px; 
                          box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); text-align: center; margin-bottom: 15px;">
                        <div style="font-size: 32px; margin-bottom: 8px;">{icon}</div>
                        <div style="font-weight: 600; color: #4361ee;">{domain}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("Select", key=f"btn_{i}", use_container_width=True):
                    st.session_state.selected_domain = domain
    
    # Selected domain display
    if st.session_state.selected_domain:
        st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 16px; margin: 20px 0; text-align: center; 
                      border: 1px solid rgba(67, 97, 238, 0.2);">
                <h4 style="margin: 0; color: #4361ee;">Selected Domain</h4>
                <div class="domain-badge">{st.session_state.selected_domain}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Find investors button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
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
                            show_message(investors["message"], "warning")
                        else:
                            st.markdown("""
                                <h2 style="color: #4361ee; text-align: center; margin: 30px 0 20px 0;">
                                    📋 Top Matching Investors
                                </h2>
                            """, unsafe_allow_html=True)
                            
                            # Display investors
                            investors_df = pd.DataFrame(investors)
                            
                            if not investors_df.empty:
                                for idx, investor in investors_df.iterrows():
                                    investor_id = investor.get("investor_id", f"default_{idx}")
                                    investor_name = investor.get("investor_name", "N/A")
                                    
                                    # Calculate match percentage
                                    match_score = investor.get("match_score", 0)
                                    match_percentage = min(round((match_score / 100) * 100), 100)
                                    
                                    col1, col2, col3 = st.columns([2, 1, 1])
                                    
                                    with col1:
                                        # Format funds
                                        funds_display = format_funds(investor.get("funds_available", "N/A"))
                                        
                                        st.markdown(f"""
                                            <div class="investor-card">
                                                <div class="match-badge">{match_percentage}% Match</div>
                                                <h4>{investor_name} ({investor.get("investor_company", "N/A")})</h4>
                                                <p><b>Experience:</b> {investor.get("investor_experience(years)", "N/A")} years | 
                                                <b>Investments:</b> {investor.get("no_of_companies_invested", "N/A")}</p>
                                                <p><b>Funds Available:</b> {funds_display}</p>
                                                <p><b>Domains:</b> {investor.get("domains", "N/A")}</p>
                                                <p>
                                                    <a href='{investor.get("linkedin_url", "#")}' target='_blank'>🔗 LinkedIn</a> | 
                                                    ✉ <a href='mailto:{investor.get("email", "#")}'>{investor.get("email", "N/A")}</a>
                                                </p>
                                            </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with col2:
                                        st.progress(min(match_score / 100, 1.0))
                                    
                                    with col3:
                                        if st.button("💬 Chat", key=f"chat_{investor_id}", use_container_width=True):
                                            open_chat(investor_id, investor_name)
                            else:
                                show_message("No matching investors found.", "warning")
                    except requests.exceptions.RequestException as e:
                        show_message(f"Investor API Request Failed: {e}", "error")