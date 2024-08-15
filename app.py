import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
meals = pd.read_csv('merged_data.csv')

st.sidebar.header('User Profile')
age = st.sidebar.number_input('Age', min_value=1, max_value=100, value=30)
gender = st.sidebar.selectbox('Gender', ['Male', 'Female'])
weight = st.sidebar.number_input('Weight (kg)', min_value=1, max_value=200, value=70)
height = st.sidebar.number_input('Height (cm)', min_value=1, max_value=250, value=175)
activity_level = st.sidebar.selectbox('Activity Level', ['Sedentary', 'Lightly active', 'Moderately active', 'Very active', 'Super active'])

def calculate_bmr(weight, height, age, gender):
    if gender == 'Male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def daily_calorie_needs(bmr, activity_level):
    activity_multipliers = {
        'Sedentary': 1.2,
        'Lightly active': 1.375,
        'Moderately active': 1.55,
        'Very active': 1.725,
        'Super active': 1.9
    }
    return bmr * activity_multipliers[activity_level]

bmr = calculate_bmr(weight, height, age, gender)
daily_calories = daily_calorie_needs(bmr, activity_level)
st.sidebar.write(f"Daily Caloric Needs: {daily_calories:.2f} kcal")

def categorize_meal(item):
    if item['Caloric Value'] > 300 and item['Protein'] > 15:
        return 'Dinner'
    elif item['Caloric Value'] > 200 and item['Protein'] > 10:
        return 'Lunch'
    elif item['Carbohydrates'] > 30:
        return 'Breakfast'
    else:
        return 'Snacks'

meals['Meal_Category'] = meals.apply(categorize_meal, axis=1)

def categorize_meal(item):
    if item['Caloric Value'] > 300 and item['Protein'] > 15:
        return 'Dinner'
    elif item['Caloric Value'] > 200 and item['Protein'] > 10:
        return 'Lunch'
    elif item['Carbohydrates'] > 30:
        return 'Breakfast'
    else:
        return 'Snacks'

meals['Meal_Category'] = meals.apply(categorize_meal, axis=1)

st.header('Meal Plan Breakdown')
category_counts = meals['Meal_Category'].value_counts()
st.bar_chart(category_counts)

st.subheader('Nutrient Breakdown')
meal_choice = st.selectbox('Choose a meal', meals['Meal_Category'].unique())
selected_meal = meals[meals['Meal_Category'] == meal_choice]
st.dataframe(selected_meal[['Food Item', 'Protein', 'Carbohydrates', 'Fat', 'Caloric Value']])

st.subheader('Nutrient Goals Tracking')
protein_goal = selected_meal['Protein'].sum() / (0.2 * daily_calories / 4) * 100
carb_goal = selected_meal['Carbohydrates'].sum() / (0.5 * daily_calories / 4) * 100
fat_goal = selected_meal['Fat'].sum() / (0.3 * daily_calories / 9) * 100

st.progress(protein_goal, text="Protein Goal")
st.progress(carb_goal, text="Carbohydrate Goal")
st.progress(fat_goal, text="Fat Goal")

st.sidebar.subheader('Meal Filters')
high_protein = st.sidebar.checkbox('High Protein')
low_carb = st.sidebar.checkbox('Low Carb')

filtered_meals = meals.copy()
if high_protein:
    filtered_meals = filtered_meals[filtered_meals['Protein'] > 20]
if low_carb:
    filtered_meals = filtered_meals[filtered_meals['Carbohydrates'] < 10]

st.subheader('Filtered Meals')
st.dataframe(filtered_meals)

st.subheader('Nutrient Intake Over Time')
nutrient_trends = filtered_meals.groupby('Date').sum()
st.line_chart(nutrient_trends[['Protein', 'Carbohydrates', 'Fat']])

st.subheader('Export Meal Plan')
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_meals)
st.download_button(
    label="Download Meal Plan as CSV",
    data=csv,
    file_name='meal_plan.csv',
    mime='text/csv',
)

