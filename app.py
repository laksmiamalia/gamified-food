import streamlit as st
import pandas as pd

# Include the functions from above here
def calculate_caloric_needs(weight_kg, height_cm, age_years, gender, activity_level):
    if gender == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161

    activity_multipliers = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'super active': 1.9
    }

    return bmr * activity_multipliers.get(activity_level, 1.2)

def categorize_caloric_intake(row, user_daily_calories):
    if row['Caloric Value'] < 0.2 * user_daily_calories:
        return 'Low-Calorie Meal'
    elif row['Caloric Value'] < 0.4 * user_daily_calories:
        return 'Moderate-Calorie Meal'
    else:
        return 'High-Calorie Meal'

def process_food_data(merged_data, weight_kg, height_cm, age_years, gender, activity_level):
    user_daily_calories = calculate_caloric_needs(weight_kg, height_cm, age_years, gender, activity_level)
    merged_data['User_Calorie_Needs'] = user_daily_calories
    merged_data['Caloric_Intake_Category'] = merged_data.apply(lambda x: categorize_caloric_intake(x, user_daily_calories), axis=1)
    return merged_data

# Streamlit user form
st.title('Personalized Nutrition Plan')

st.header('Enter Your Information')

# User inputs
weight_kg = st.number_input('Weight (kg)', min_value=30.0, max_value=200.0, value=70.0)
height_cm = st.number_input('Height (cm)', min_value=140.0, max_value=220.0, value=170.0)
age_years = st.number_input('Age (years)', min_value=18, max_value=100, value=30)
gender = st.selectbox('Gender', ['male', 'female'])
activity_level = st.selectbox('Activity Level', ['sedentary', 'lightly active', 'moderately active', 'very active', 'super active'])

if st.button('Generate Nutrition Plan'):
    # Assume you have loaded your dataset into 'merged_data'
    merged_data = pd.read_csv('your_data.csv')
    processed_data = process_food_data(merged_data, weight_kg, height_cm, age_years, gender, activity_level)
    
    st.write('Here is your personalized data:')
    st.write(processed_data.head())  # Display the processed data (or relevant parts)
