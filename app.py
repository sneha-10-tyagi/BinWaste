import streamlit as st
import serial
import time
import joblib
import numpy as np

# First page layout
def first_page():
    st.title("Welcome to the Smart Dustbin System")

    # If the user is not logged in, show the login button
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        if st.sidebar.button("Login"):
            st.session_state.login_button_clicked = True  # Show the login form when clicked
    else:
        st.write("You are logged in as admin!")

    # "About" and "Query" buttons
    about_button = st.sidebar.button("About")
    query_button = st.sidebar.button("Query")

    if about_button:
        st.write("Welcome to the Smart Dustbin Project — an innovative solution for smarter waste management. Our system helps authorities proactively manage bin fill levels. Residents can easily report issues through the platform, promoting cleaner neighborhoods. By combining technology and community efforts, we aim to build greener, healthier cities. Join us in making waste management smarter and more sustainable!.")

    if query_button:
        show_query_form()

    # Show login page if login button was clicked
    if st.session_state.get('login_button_clicked', False) and 'logged_in' not in st.session_state:
        login()

# Admin login
def login():
    st.title("Admin Login")
    
    # Define session state variables for username and password
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'password' not in st.session_state:
        st.session_state.password = ''
    
    username = st.text_input("Username", value=st.session_state.username)
    password = st.text_input("Password", type='password', value=st.session_state.password)

    # Check if username or password is entered and validate login
    if username and password:
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True  # Set logged_in status to True
            st.session_state.username = username  # Persist username
            st.session_state.password = password  # Persist password
            st.success("Login Successful!")
            admin_dashboard()
        else:
            st.error("Invalid username or password")

# Query form
def show_query_form():
    st.title("Submit Your Query")

    # Get form data and persist it in session state
    if 'name' not in st.session_state:
        st.session_state.name = ''
    if 'address' not in st.session_state:
        st.session_state.address = ''
    if 'email' not in st.session_state:
        st.session_state.email = ''
    if 'contact' not in st.session_state:
        st.session_state.contact = ''
    if 'feedback_type' not in st.session_state:
        st.session_state.feedback_type = "Complaint"  # Set default value if not set

    name = st.text_input("Name", value=st.session_state.name)
    address = st.text_input("Address", value=st.session_state.address)
    email = st.text_input("Gmail", value=st.session_state.email)
    contact = st.text_input("Contact", value=st.session_state.contact)

    # Set the default value for feedback_type if it's empty
    feedback_type = st.selectbox("Feedback Type", ["Complaint", "Request"], index=["Complaint", "Request"].index(st.session_state.feedback_type))

    # Submit button to handle query submission
    if st.button("Submit"):
        st.session_state.name = name
        st.session_state.address = address
        st.session_state.email = email
        st.session_state.contact = contact
        st.session_state.feedback_type = feedback_type
        st.write(f"Name: {name}")
        st.write(f"Address: {address}")
        st.write(f"Email: {email}")
        st.write(f"Contact: {contact}")
        st.write(f"Feedback Type: {feedback_type}")
        st.success("Your query has been submitted!")

# Admin Dashboard
def admin_dashboard():
    st.title("Admin Dashboard")

    if st.session_state.get('logged_in', False):

        # Create two separate sections for Alert and Warning messages
        alert_message_placeholder = st.empty()  # Placeholder for Alert message
        warning_message_placeholder = st.empty()  # Placeholder for Warning message

        # Message button (for form submissions)
        message_button = st.button("Messages")
        if message_button:
            st.write("Displaying all form submissions...")

        # Prediction button (for ML updates)
        prediction_button = st.button("Predictions")
        if prediction_button:
            st.write("Displaying live ML model predictions...")

        # Loop to continuously read data and update the dashboard
        while True:
            try:
                # Wait for Arduino data to stabilize
                time.sleep(2)  # Wait for 2 seconds before reading data again

                # Read data from Arduino (distance and fill percentage)
                distance, fill_percent, status = read_from_arduino()

                # Print the received data for debugging
                st.write(f"Received data: Distance: {distance} cm, Fill: {fill_percent}%")

                # Update the respective section based on the Arduino status
                if status == "Alert":
                    # Show the ALERT message in the Alert section
                    alert_message_placeholder.warning("ALERT: Dustbin is FULL!")
                    # Clear the Warning section
                    warning_message_placeholder.empty()

                elif status == "Warning":
                    # Show the WARNING message in the Warning section
                    warning_message_placeholder.warning("WARNING: Dustbin is nearing full capacity.")
                    # Clear the Alert section
                    alert_message_placeholder.empty()

                else:
                    # If the status is "Normal", clear both sections
                    alert_message_placeholder.empty()
                    warning_message_placeholder.empty()

            except Exception as e:
                st.error(f"Error reading from Arduino: {str(e)}")
                break  # Stop the loop if there is an error



# Function to read data from Arduino
def read_from_arduino():
    port = "/dev/tty.usbserial-11430"  # Replace with the correct port
    try:
        ser = serial.Serial(port, 9600)
        time.sleep(2)  # Wait for Arduino to initialize

        # Read data from Arduino
        data = ser.readline().decode().strip()
        # Example data: "Distance: 36.96 cm, Fill: 85.0%"
        print("Received data:", data)
        
        # Parse data
        if "Distance" in data and "Fill" in data:
            distance_str, fill_str = data.split(", ")
            distance = float(distance_str.split(": ")[1].replace(" cm", ""))
            fill_percent = float(fill_str.split(": ")[1].replace("%", ""))
            
            # Determine status
            if fill_percent > 85.0:
                status = "Alert"
            elif 74.0 <= fill_percent <= 85.0:
                status = "Warning"
            else:
                status = "Normal"
            
            return distance, fill_percent, status
        else:
            raise ValueError("Invalid data received from Arduino")
    except Exception as e:
        st.error(f"Error reading from Arduino: {str(e)}")
        return None, None, "Error"

# Load the model
def load_model(model_path='smart_dustbin_rf_model.pkl'):
    """
    This function loads the trained RandomForest model from the given file path.
    :param model_path: str: The path where the model is saved.
    :return: The loaded model
    """
    model = joblib.load(model_path)
    return model

# Predict dustbin status based on user input
def predict_dustbin_status():
    st.write("Enter the distance of the dustbin from the sensor (in cm):")
    distance_input = st.number_input("Distance (cm)", min_value=0, max_value=100, value=50)

    # Load the model
    model = load_model('smart_dustbin_rf_model.pkl')  # Adjust path if needed

    # Prepare input data for prediction
    input_data = np.array([[distance_input]])  # Input needs to be in a 2D array shape

    # Make prediction
    status_prediction = model.predict(input_data)
    
    # Map prediction to status
    status_mapping = {0: 'Alert', 1: 'Normal', 2: 'Warning'}
    predicted_status = status_mapping[status_prediction[0]]

    st.write(f"Predicted status for distance {distance_input} cm: {predicted_status}")

if __name__ == "__main__":
    first_page()
