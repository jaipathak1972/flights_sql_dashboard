import streamlit as st
from user_register import UserRegister
from dbhealper import create_bar_graph, create_line_graph, create_pie_chart, create_boxplot_graph

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

# Initialize UserRegister class
user_register = UserRegister()

# Initialize session state if not already done
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "Tab 1"

def set_tab(tab_name):
    st.session_state.selected_tab = tab_name

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

def main_dashboard(name):
    st.title(f'Welcome {name} to the Health Care Dashboard')
    st.write("Fetching data from heartattack database...")

    table_name = 'heartattack.heart_attack'

    st.write("Generating Bar Graph...")
    bar_fig = create_bar_graph(table_name)
    if bar_fig:
        st.plotly_chart(bar_fig, use_container_width=True)
    else:
        st.write("No data available for bar graph.")

    st.write("Generating Line Graph...")
    line_fig = create_line_graph(table_name)
    if line_fig:
        st.plotly_chart(line_fig, use_container_width=True)
    else:
        st.write("No data available for line graph.")

    st.write("Generating Pie Chart...")
    pie_fig = create_pie_chart(table_name)
    if pie_fig:
        st.plotly_chart(pie_fig, use_container_width=True)
    else:
        st.write("No data available for pie chart.")

    st.write("Generating Box Plot...")
    boxplot_fig = create_boxplot_graph(table_name)
    if boxplot_fig:
        st.plotly_chart(boxplot_fig, use_container_width=True)
    else:
        st.write("No data available for box plot.")

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
                if user_register.login_user(login_username, login_password):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.experimental_rerun()  # Refresh the app state
                else:
                    st.error("Invalid username or password.")
            else:
                st.error("Please enter a username and password.")

    with tab2:
        st.header("Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            if new_username and new_password:
                user_register.register_user(new_username, new_password)
                st.success("Registration successful!")
                st.experimental_rerun()  # Refresh the app state
            else:
                st.error("Please enter a username and password.")
