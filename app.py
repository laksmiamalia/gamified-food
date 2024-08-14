import streamlit as st
import pandas as pd

merged_data = pd.read_csv('merged_data.csv')

# Define functions to categorize food items
def categorize_protein(row):
    return 'High-Protein' if row['Protein'] > 20 else 'Not High-Protein'

def categorize_carb(row):
    return 'Low-Carb' if row['Carbohydrates'] < 10 else 'Not Low-Carb'

def categorize_fat(row):
    return 'Low-Fat' if row['Fat'] < 5 else 'Not Low-Fat'

def categorize_fiber(row):
    return 'High-Fiber' if row['Dietary Fiber'] > 5 else 'Not High-Fiber'

def categorize_sugar(row):
    return 'Low-Sugar' if row['Sugars'] < 5 else 'Not Low-Sugar'

def categorize_cal(row):
    return 'Low-Cal' if row['Caloric Value'] < 100 else 'Not Low-Cal'

def categorize_chol(row):
    return 'Low-Chol' if row['Cholesterol'] < 20 else 'Not Low-Chol'

def categorize_sodium(row):
    return 'Low-Sodium' if row['Sodium'] < 10 else 'Not Low-Sodium'

def categorize_meal(row):
    if row['Caloric Value'] > 300 and row['Protein'] > 15:
        return 'Dinner'
    elif row['Caloric Value'] > 200 and row['Protein'] > 10:
        return 'Lunch'
    elif row['Carbohydrates'] > 30:
        return 'Breakfast'
    else:
        return 'Snacks'

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
    
    # Apply additional categorizations
    merged_data['Protein_Category'] = merged_data.apply(categorize_protein, axis=1)
    merged_data['Carbohydrate_Category'] = merged_data.apply(categorize_carb, axis=1)
    merged_data['Fat_Category'] = merged_data.apply(categorize_fat, axis=1)
    merged_data['Fiber_Category'] = merged_data.apply(categorize_fiber, axis=1)
    merged_data['Sugar_Category'] = merged_data.apply(categorize_sugar, axis=1)
    merged_data['Calorie_Category'] = merged_data.apply(categorize_cal, axis=1)
    merged_data['Cholesterol_Category'] = merged_data.apply(categorize_chol, axis=1)
    merged_data['Sodium_Category'] = merged_data.apply(categorize_sodium, axis=1)
    
    # Categorize meal types
    merged_data['Meal_Category'] = merged_data.apply(categorize_meal, axis=1)
    
    # Filter out non-recommended foods
    recommended_data = merged_data[merged_data['Caloric_Intake_Category'] == 'Moderate-Calorie Meal']
    
    return recommended_data

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
    # Load your dataset
    
    # Process the data
    processed_data = process_food_data(merged_data, weight_kg, height_cm, age_years, gender, activity_level)
    
    # Display menus
    st.write('Here is your personalized menu:')
    
    breakfast_menu = processed_data[processed_data['Meal_Category'] == 'Breakfast']
    lunch_menu = processed_data[processed_data['Meal_Category'] == 'Lunch']
    dinner_menu = processed_data[processed_data['Meal_Category'] == 'Dinner']
    
    st.subheader('Breakfast Menu')
    st.write(breakfast_menu)
    
    st.subheader('Lunch Menu')
    st.write(lunch_menu)
    
    st.subheader('Dinner Menu')
    st.write(dinner_menu)
