import streamlit as st
import mysql.connector
import bcrypt

# Define custom CSS
css = """
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    color: #333;
}
header {
    background-color: #007bff;
    color: white;
    padding: 10px 0;
    text-align: center;
}
.stButton button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
}
.stButton button:hover {
    background-color: #0056b3;
}
.stTextInput input {
    border-radius: 5px;
    padding: 10px;
    border: 1px solid #ccc;
    width: 100%;
    box-sizing: border-box;
}
.stAlert {
    border-radius: 5px;
}
.st-af.st-ag.st-ah.st-ai.st-aj.st-ak.st-al.st-am.st-an.st-ao.st-ap.st-aq.st-ar {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px; /* Adjust spacing from the top */
}

/* Style the buttons to ensure uniformity and alignment */
.st-as.st-at.st-au.st-av.st-aw.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9.st-ba.st-bb.st-bc.st-bd.st-be.st-bf.st-bg.st-bh.st-bi.st-bj.st-bk.st-bl.st-bm.st-bn.st-bo.st-bp.st-bq.st-br.st-bs.st-bt.st-bu.st-bv.st-bw.st-bx.st-by.st-bz.st-c0 {
    margin: 0 10px; /* Space between buttons */
    border-radius: 5px;
}

/* Center the tab content */
.st-emotion-cache-sh2krr.e1nzilvr5 {
    text-align: center;
}
[data-testid="stVerticalBlockBorderWrapper"]{
    background-color: purple;
    margin : 20px;
    padding : 20px;
}

</style>
"""

# Apply the custom CSS
st.markdown(css, unsafe_allow_html=True)

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'jaipathak2005',
    'host': 'localhost',
    'database': 'user_auth'
}

def create_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return None

# Register user function
def register_user(username, password):
    conn = create_connection()
    if conn is None:
        return
    cursor = conn.cursor()

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        # Insert the user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
        conn.commit()
        st.success("User registered successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Login user function
def login_user(username, password):
    conn = create_connection()
    if conn is None:
        return
    cursor = conn.cursor()

    try:
        # Retrieve the user from the database
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password!")
    finally:
        cursor.close()
        conn.close()

# Initialize session state if not already done
def main_dashboard(name):
    st.title(f'Welcome {name} to the Health Care Dashboard')
    st.write("Here is your dashboard content...")


if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "Tab 1"
    
def set_tab(tab_name):
    st.session_state.selected_tab = tab_name

# Initialize session state if not already done
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# UI Logic
if st.session_state.logged_in:
    main_dashboard(st.session_state.username)
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()
else:
    # Tabs to select between Login and Register
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.header("Login")
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_username and login_password:
                login_user(login_username, login_password)
                st.experimental_rerun()  # Refresh the app state
            else:
                st.error("Please enter a username and password.")

    with tab2:
        st.header("Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            if new_username and new_password:
                register_user(new_username, new_password)
                st.experimental_rerun()  # Refresh the app state


            else:
                st.error("Please enter a username and password.")
