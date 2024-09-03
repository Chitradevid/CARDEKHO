import streamlit as st
import pandas as pd
import joblib

# Load the trained model and encoders
model = joblib.load('cd_model.pkl')  
oem_mapping = joblib.load('oem_mapping.pkl')
fuel_mapping = joblib.load('fuel_mapping.pkl')
   

# Define the app layout
st.title('Car Price Prediction')
st.write('Enter the car features in the sidebar to get a price prediction.')


# Display an image
st.image('c5.png', use_column_width=False, width=600)  


def get_user_input():

    gear_box = st.sidebar.slider('Gear Box', min_value=4, max_value=8, step=1)
    kerb_weight = st.sidebar.slider('Kerb Weight',min_value=670, max_value=2200, step=5 )
    max_power = st.sidebar.slider('Max Power',min_value=40, max_value=235, step=5 )
    engine_displacement = st.sidebar.slider('Engine Displacement', min_value=10, max_value=2800, step=5 )
    model_year = st.sidebar.slider('Model Year',min_value=1995, max_value=2023, step=1 )
    oem = st.sidebar.selectbox('Brand', options=oem_mapping.keys())
    transmission = st.sidebar.selectbox('Transmission', options=['Manual', 'Automatic'])
    ft = st.sidebar.selectbox('Fuel Type', options=fuel_mapping.keys())
    km = st.sidebar.slider('KM', min_value=0, max_value=25000, step=10 )
    torque = st.sidebar.slider('Torque', min_value=7, max_value=500, step=2 )
    wheel_size = st.sidebar.slider('Wheel Size', min_value=12, max_value=19, step=1 )
    
    # Create a DataFrame from the inputs
    data = pd.DataFrame({
        'Gear Box': [gear_box],
        'Kerb Weight': [kerb_weight],
        'Max Power': [max_power],
        'Engine Displacement': [engine_displacement],
        'modelYear': [model_year],
        'oem': [oem],
        'Transmission': [transmission],
        'ft': [ft],
        'km': [km],
        'Torque': [torque],
        'Wheel Size': [wheel_size]
    })
    
    return data

# Get user input
user_input = get_user_input()

# Add a submit button
if st.sidebar.button('Predict Price'):
    # Encode categorical features using mappings
    user_input['ft'] = user_input['ft'].map(fuel_mapping)
    user_input['Transmission'] = user_input['Transmission'].map({'Manual': 0, 'Automatic': 1})
    user_input['oem'] = user_input['oem'].map(oem_mapping)

    # Predict the price
    prediction = model.predict(user_input)

    # Display the prediction with Indian Rupee symbol
    st.write(f'Estimated Price: ₹{prediction[0]:,.2f}')
