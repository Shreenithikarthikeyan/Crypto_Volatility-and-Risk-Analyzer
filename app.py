import streamlit as st
import pandas as pd
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Crypto Risk Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

/* Glass Card */
.glass {
background: rgba(255,255,255,0.08);
padding:30px;
border-radius:20px;
backdrop-filter: blur(12px);
box-shadow:0 8px 32px rgba(0,0,0,0.3);
}

/* Login Button */
div.stButton > button {
background: linear-gradient(45deg,#00c6ff,#0072ff);
color:white;
border:none;
padding:10px 25px;
border-radius:10px;
font-weight:bold;
transition:0.3s;
}

div.stButton > button:hover {
transform: scale(1.05);
}

/* Hide Streamlit menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False


# ---------------- API FUNCTION ----------------
def fetch_crypto():
    url="https://api.coingecko.com/api/v3/coins/markets"
    params={
        "vs_currency":"usd",
        "order":"market_cap_desc",
        "per_page":5,
        "page":1
    }

    data=requests.get(url,params=params).json()

    df=pd.DataFrame(data)[["name","current_price","price_change_percentage_24h","total_volume"]]
    return df


# ================= LOGIN PAGE =================
if not st.session_state.login:

    col1,col2,col3 = st.columns([1,2,1])

    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.title("🚀 Crypto Risk Analyzer")
        st.subheader("Secure Login")

        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("LOGIN"):
            if username == "admin" and password == "1234":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Wrong credentials")

        st.markdown("</div>", unsafe_allow_html=True)


# ================= DASHBOARD =================
else:

    # SIDEBAR
    st.sidebar.title("⚡ Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard","Analytics"])

    st.sidebar.success("Logged in as Admin")

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()

    # -------- DASHBOARD --------
    if page == "Dashboard":

        st.title("📊 Crypto Market Dashboard")

        df = fetch_crypto()

        col1,col2,col3,col4,col5 = st.columns(5)

        for i,col in enumerate([col1,col2,col3,col4,col5]):
            with col:
                st.markdown(f"""
                <div class="glass">
                <h4>{df['name'][i]}</h4>
                <h2>${df['current_price'][i]}</h2>
                <p>24h Change: {round(df['price_change_percentage_24h'][i],2)}%</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("### 📈 Price Trend")
        st.line_chart(df["current_price"])

        st.markdown("### 📋 Live Data")
        st.dataframe(df, use_container_width=True)

    # -------- ANALYTICS PAGE --------
    elif page == "Analytics":

        st.title("📉 Risk Analytics")

        df = fetch_crypto()

        st.bar_chart(df["total_volume"])

        st.area_chart(df["price_change_percentage_24h"])

        st.success("Risk visualization ready ✅")
        from crypto_api import fetch_crypto

df = fetch_crypto()
st.dataframe(df)

