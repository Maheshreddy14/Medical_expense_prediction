import hashlib
import streamlit as st
import re
from pymongo import MongoClient
from streamlit_option_menu import option_menu
import random
import smtplib
from email.mime.text import MIMEText
import pickle
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
import requests
import json




#Connect to MongoDB
mongo_uri = "mongodb+srv://maheswarreddyavula111:ZQabAWtPcPnWJLYi@cluster0.nzfkmcg.mongodb.net/main"
client=MongoClient(mongo_uri)
db=client['MainProject']
user_collection=db['UserCredentials']

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Streamlit UI
st.set_page_config(
    page_title="Medical Expense Prediction",
    page_icon="🧑‍⚕️",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown("""
    <style>
        /* Increase the font size for the entire page */
        body {
            font-size: 18px; /* Adjust the font size value as per your requirement */
        }
    </style>
""", unsafe_allow_html=True)



#Title
st.title('MEDICAL EXPENSE PREDICTION')

#Background image

#Navigation bar
with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu", #required
        options=["Home","Registration","Login","Dashboard","Profile","Logout"], #required
        icons=["house","clipboard2-pulse-fill","box-arrow-in-right","border-all","person-circle","box-arrow-right"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
        "container": {"padding": "0!important"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {
            "font-size": "24px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "white"
        },
        "nav-link-selected": {"background-color": "#2596be"}
    },
)
    
#Home page
def load_lottieurl(url:str):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()
def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
if selected=="Home":
    lottie_hello=load_lottieurl("https://lottie.host/6e488e55-7a4d-44db-a44a-1efc82bc0ec0/gNjTml2kRm.json")
    st_lottie(lottie_hello,key="hello",height=400)
    st.markdown("""
    ### About Us
    <div style="text-align:justify">
    Welcome to our application! We strive to provide a seamless user experience for registration and more. Our team is dedicated to building innovative 
    solutions to meet your needs.
    </div>
                
    ### Motive of this Application
                
    <div style="text-align:justify">
    The motive behind developing a machine learning model for explainable cost prediction of medical insurance can be multifaceted and beneficial for various stakeholders involved in the healthcare ecosystem. Here are some key motives and potential benefits of such an application:
    </div>
    <div style="text-align:justify">
    <h5>Transparency and Understanding:</h5> By employing machine learning techniques for cost prediction, insurers can provide transparent explanations for how they arrive at premium costs for different individuals. This transparency helps consumers understand why they are charged a certain amount and what factors contribute to their insurance costs.
    </div>
    <div style="text-align:justify">
    <h5>Fairness and Equity:</h5> Machine learning models can help insurers ensure fairness and equity in their pricing strategies by basing premiums on relevant factors such as age, medical history, lifestyle, and pre-existing conditions. This can prevent discriminatory pricing practices and ensure that individuals with similar risk profiles are charged similar premiums.
    </div>
    <div style="text-align:justify">
    <h5>Risk Management:</h5> Predictive models can help insurers better assess the risk associated with insuring a particular individual or group. By analyzing historical data and identifying patterns, insurers can more accurately predict future healthcare costs and adjust premiums accordingly, thus minimizing financial risks for both insurers and policyholders.
    </div>
    <div style="text-align:justify">
    <h5>Personalized Insurance Plans:</h5> Machine learning models enable the development of personalized insurance plans tailored to individual needs and risk profiles. By understanding the factors that influence an individual's healthcare costs, insurers can offer customized coverage options that provide adequate protection at affordable rates.
    </div>
    <div style="text-align:justify">
    <h5>Preventive Care and Health Promotion:</h5>redictive models can identify individuals at higher risk of developing certain health conditions or requiring costly medical interventions in the future. Insurers can use this information to proactively promote preventive care and wellness programs, ultimately reducing healthcare costs and improving overall health outcomes.
    <div style="text-align:justify">
    <h5>Fraud Detection:</h5> Machine learning algorithms can be used to detect fraudulent claims and activities, thereby helping insurers reduce losses associated with fraudulent behavior. By analyzing patterns in claims data, these models can identify suspicious patterns indicative of fraud, enabling timely intervention and investigation. 
    </div>
""",unsafe_allow_html=True)
    
#Registration page
# Set your email credentials
email_address = "maashared20@gmail.com"
email_password = "wkxk rite uomg bcsl"

def send_otp(email, otp):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_address, email_password)
        subject = "Your OTP"
        body = f"Your OTP is: {otp}"
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = email_address
        msg["To"] = email
        server.sendmail(email_address, email, msg.as_string())

def generate_otp():
    otp = ""
    for _ in range(6):
        otp += str(random.randint(0, 9))
    return otp
def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
        return False
    return True
if selected=="Registration":
    #Background image
    background_image = """
        <style>
        [data-testid="stAppViewContainer"] > .main {
            background-image: url("https://img.freepik.com/free-photo/top-view-stethoscope_23-2148519789.jpg?size=626&ext=jpg&ga=GA1.1.1395880969.1709856000&semt=ais");
            background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
            background-position: center;  
            background-repeat: no-repeat;
        }
        </style>
        """
    st.markdown(background_image, unsafe_allow_html=True)
    st.subheader(f"{selected} Page")
    st.write("##### Please fill out the registration form below:")
    name = st.text_input("###### Name")
    email = st.text_input("###### Email")
    password = st.text_input("###### Password", type="password")
    confirm_password = st.text_input("###### Confirm Password", type="password")
    submit_button=st.button('Register')
    if submit_button:
        if not validate_email(email):
            st.error('Invalid email format. lease enter a valid email.')
        elif user_collection.find_one({'email':email}):
            st.error('Email already in use. Please choose a different email.')
        elif user_collection.find_one({'username':name}):
            st.error('Username already exists. Please enter different username.')
        elif len(name)<4:
            st.error('Username must be atleast 4 characters long.')
        elif len(password)<8:
            st.error('Password must be atleast 8 characters long.')
        elif password!=confirm_password:
            st.error('Passwords do not match. Please try again.')
        else:  
        # Insert user details into MongoDB
            hashed_password = hash_password(password)
            user_data = {"username":name,"email": email, "password": hashed_password}
            user_collection.insert_one(user_data)
            st.success("Registration successful. Please login.")
    st.markdown("Already have an account? Go to Login")

#Login page
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False
if selected=="Login":
    #Background image
    background_image= """
        <style>
        [data-testid="stAppViewContainer"] > .main {
            background-image: url("https://img.freepik.com/free-photo/top-view-stethoscope_23-2148519789.jpg?size=626&ext=jpg&ga=GA1.1.1395880969.1709856000&semt=ais");
            background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
            background-position: center;  
            background-repeat: no-repeat;
        }
        </style>
        """
    st.markdown(background_image, unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["##### Login", "##### Verification"])
    with tab1:
        username = st.text_input("###### Username")
        password = st.text_input("###### Password", type="password")
        hashed_password = hash_password(password)
        user = user_collection.find_one({"username": username, "password": hashed_password})

        if "otp" not in st.session_state:
                    st.session_state.otp=''
        if st.button("Send OTP"):
            if user:
                otp=generate_otp()
                st.session_state.otp= otp
                send_otp(user["email"],otp)
                if "entered_otp" not in st.session_state:      
                    st.session_state.entered_otp=""           
            else:
               st.error('Invalid username or password!')
    with tab2:
        entered_otp = st.text_input("###### Enter OTP")
        st.session_state.entered_otp = entered_otp
                
        if st.button("Login"):
            if st.session_state.entered_otp == st.session_state.otp:
                st.success("OTP is verified!")
                st.session_state.logged_in = True
                st.session_state.user=username
                st.success("Logged in as {}".format(user["username"]))
            
            else:
                st.error("Please enter correct OTP!")

#Dashboard
if selected=="Dashboard":
    background_image= """
        <style>
        [data-testid="stAppViewContainer"] > .main {
            background-image: url("https://img.freepik.com/free-photo/top-view-stethoscope_23-2148519789.jpg?size=626&ext=jpg&ga=GA1.1.1395880969.1709856000&semt=ais");
            background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
            background-position: center;  
            background-repeat: no-repeat;
        }
        </style>
        """
    st.markdown(background_image, unsafe_allow_html=True)
    st.subheader(f"{selected}")
    if st.session_state.logged_in:
        loaded_model=pickle.load(open('C:/Users/chandra shekar reddy/Medical_Expense_prediction/MainProject/train_model.sav','rb'))
        #creating a function for prediction
        def expense_prediction(input_data):
           #changing the input data to numpy array
           input_data_as_numpy_array=np.array(input_data)
           #reshape the data as we are predicting for one instance
           input_data_reshaped=input_data_as_numpy_array.reshape(1,-1)
           prediction=loaded_model.predict(input_data_reshaped)
           return prediction
        def main():
            age = st.number_input("###### Please enter your age", min_value=0, max_value=150, step=1)
            Diabetes = st.selectbox("###### Do you have Diabetes?", ("Yes", "No"))
            Diabetes= 1 if Diabetes == "Yes" else 0
            BP = st.selectbox("###### Is there any Blood pressure problems?", ("Yes", "No"))
            BP= 1 if BP == "Yes" else 0
            Transplants = st.selectbox("###### Is there any Transplants?", ("Yes", "No"))
            Transplants= 1 if Transplants == "Yes" else 0
            Chronic = st.selectbox("###### Is there any Chronic Diseases?", ("Yes", "No"))
            Chronic= 1 if Chronic == "Yes" else 0
            height = st.number_input("###### Please enter your height (in centimeters)", min_value=0.0)
            weight = st.number_input("###### Please enter your weight (in centimeters)", min_value=0.0)
            Allergies = st.selectbox("###### Is there any Known Allergies?", ("Yes", "No"))
            Allergies= 1 if Chronic == "Yes" else 0
            Cancer = st.selectbox("###### Is there any History of Cancer in your family?", ("Yes", "No"))
            Cancer= 1 if Chronic == "Yes" else 0
            num_major_surgeries = st.number_input("###### Please enter the number of major surgeries", min_value=0)
            diagnosis=''
            if st.button("Predict"):
                diagnosis=expense_prediction([age,Diabetes,BP,Transplants,Chronic,height,weight,Allergies,Cancer,num_major_surgeries])
                st.write('###### The predicted premium price is ',int(diagnosis))
                st.success('Successfully predicted the Premium Price')
        if __name__ == '__main__':
            main()
    else:
        st.markdown("""
        ### You are not logged in!""") 
    
#Profile
if selected == "Profile":
    #Background image
    background_image= """
        <style>
        [data-testid="stAppViewContainer"] > .main {
            background-image: url("https://img.freepik.com/free-photo/top-view-stethoscope_23-2148519789.jpg?size=626&ext=jpg&ga=GA1.1.1395880969.1709856000&semt=ais");
            background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
            background-position: center;  
            background-repeat: no-repeat;
        }
        </style>
        """
    st.markdown(background_image, unsafe_allow_html=True)
    st.subheader(f"{selected}")
    if st.session_state.logged_in:
        def get_user_details(username):
            user = user_collection.find_one({'username': username})
            return user
        username = st.session_state.user
        user = get_user_details(username)
        if user:
            photo =("https://pic.onlinewebfonts.com/thumbnails/icons_534267.svg")
            col1, col2 = st.columns([1, 2])
            col2.image(photo, width=200)

            col3, col4 =st.columns([1,3])

            col4.write(f"#### Name: {user['username']}")
            col4.write(f"#### Email: {user['email']}")

            
            if st.button('update_info'):
                new_name = col4.text_input('#### Enter new name', user['username'])
                new_email = col4.text_input('#### Enter new email', user['email'])

                if col4.button('Update'):
                    if new_name or new_email:
                        # Update user data in MongoDB
                        result = user_collection.update_one(
                            {'username': username},
                            {'$set': {'username': new_name, 'email': new_email}}
                        )
                        if result.modified_count > 0:
                            col1.success('User information updated successfully!')
                        else:
                            col1.warning('Failed to update user information.')
                    else:
                        col1.warning('Please provide both new name and email.')
        else:
            st.warning('User not found!')
    else:
        st.markdown("""
        ### You are not logged in!""")
#Logout
if selected=='Logout':
    #Background image
    background_image= """
        <style>
        [data-testid="stAppViewContainer"] > .main {
            background-image: url("https://img.freepik.com/free-photo/top-view-stethoscope_23-2148519789.jpg?size=626&ext=jpg&ga=GA1.1.1395880969.1709856000&semt=ais");
            background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
            background-position: center;  
            background-repeat: no-repeat;
        }
        </style>
        """
    st.markdown(background_image, unsafe_allow_html=True)
    if st.session_state.logged_in:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.success("Logged out successfully!")
    else:
        st.markdown("""
        ### You are not logged in!""")


    
