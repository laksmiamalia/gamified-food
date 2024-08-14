import streamlit as st
import pandas as pd

# Load your dataset into 'merged_data'
merged_data = pd.read_csv('merged_data.csv')

# Define functions to categorize food items
def categorize_protein(row):
    if row['Protein'] > 20:
        return 'High-Protein'
    else:
        return 'Not High-Protein'

def categorize_carb(row):
    if row['Carbohydrates'] < 10:
        return 'Low-Carb'
    else:
        return 'Not Low-Carb'

def categorize_fat(row):
    if row['Fat'] < 5:
        return 'Low-Fat'
    else:
        return 'Not Low-Fat'

def categorize_fiber(row):
    if row['Dietary Fiber'] > 5:
        return 'High-Fiber'
    else:
        return 'Not High-Fiber'

def categorize_sugar(row):
    if row['Sugars'] < 5:
        return 'Low-Sugar'
    else:
        return 'Not Low-Sugar'

def categorize_cal(row):
    if row['Caloric Value'] < 100:
        return 'Low-Cal'
    else:
        return 'Not Low-Cal'

def categorize_chol(row):
    if row['Cholesterol'] < 20:
        return 'Low-Chol'
    else:
        return 'Not Low-Chol'

def categorize_sodium(row):
    if row['Sodium'] < 10:
        return 'Low-Sodium'
    else:
        return 'Not Low-Sodium'

# Apply the functions to the DataFrame
def apply_categorization(merged_data):
    merged_data['Protein_Category'] = merged_data.apply(categorize_protein, axis=1)
    merged_data['Carbohydrate_Category'] = merged_data.apply(categorize_carb, axis=1)
    merged_data['Fat_Category'] = merged_data.apply(categorize_fat, axis=1)
    merged_data['Fiber_Category'] = merged_data.apply(categorize_fiber, axis=1)
    merged_data['Sugar_Category'] = merged_data.apply(categorize_sugar, axis=1)
    merged_data['Calorie_Category'] = merged_data.apply(categorize_cal, axis=1)
    merged_data['Cholesterol_Category'] = merged_data.apply(categorize_chol, axis=1)
    merged_data['Sodium_Category'] = merged_data.apply(categorize_sodium, axis=1)
    return merged_data

def categorize_meal(item):
    if item['Caloric Value'] > 300 and item['Protein'] > 15:
        return 'Dinner'
    elif item['Caloric Value'] > 200 and item['Protein'] > 10:
        return 'Lunch'
    elif item['Carbohydrates'] > 30:
        return 'Breakfast'
    else:
        return 'Snack'

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
    merged_data = apply_categorization(merged_data)
    merged_data['Meal_Category'] = merged_data.apply(categorize_meal, axis=1)
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
    processed_data = process_food_data(merged_data, weight_kg, height_cm, age_years, gender, activity_level)
    
    st.write('Here is your personalized data:')
    st.write(processed_data.head())  # Display the processed data (or relevant parts)
