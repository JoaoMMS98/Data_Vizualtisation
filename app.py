import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px


# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("health_fitness_dataset.csv")  # Ensure correct dataset path

    # Convert gender values for better readability
    df["gender"] = df["gender"].map({"F": "Female", "M": "Male"})

    return df


df = load_data()


# Define the navigation menu
def streamlit_menu():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Explore Data"],
        icons=["house", "bar-chart-line"],
        menu_icon="menu-button-wide",
        default_index=0,
        orientation="horizontal",
    )
    return selected


selected = streamlit_menu()

# Home Page - Group Presentation
if selected == "Home":
    st.title("Health & Fitness Data Analysis")

    # Team Members Section
    st.subheader("Project Team")

    team_members = [
        ("Afonso Gamito", "20240752"),
        ("Gonçalo Pacheco", "20240695"),
        ("Gonçalo Varanda", "20240691"),
        ("Hassan Bhatti", "20241023"),
        ("João Sampaio", "20240748"),
    ]

    # Display all team members inside a single styled box
    team_html = "<div style='border: 1px solid #ddd; border-radius: 10px; padding: 10px; background-color: #f9f9f9; text-align: center; font-size: 16px;'>"
    for name, student_id in team_members:
        team_html += f"<strong>{name}</strong> - Nº {student_id} <br>"
    team_html += "</div>"

    st.markdown(team_html, unsafe_allow_html=True)

    # Project Description
    st.markdown("""
    ## **Health & Fitness Data Visualization**

    Welcome to the **Health & Fitness Data Explorer**! This interactive tool helps analyze how different exercise intensities impact calorie burn across various activities.
    ### **About the Project**
    This project aims to analyze the relationship between **gender, exercise intensity, and calories burned**, utilizing clear and engaging visualizations. Through an intuitive interface, users can dynamically explore key patterns and trends to utilize for their own personal goals.

    ### **How to Use the Application**
    - **Filter by Gender**: Compare activity trends for Male or Female participants.
    - **Choose Exercise Intensity**: Analyze calorie burn for Low, Medium, and High intensity workouts.
    - **Visualize the Results**: Interactive charts reveal key patterns in exercise performance.
    """)

# Explore Data Page - Interactive Visualizations
if selected == "Explore Data":
    st.title("Explore Health & Fitness Data")

    # User Input for Gender and Intensity
    gender = st.radio("Select Gender", options=["Male", "Female"])
    intensity = st.radio("Select Intensity Level", options=["Low", "Medium", "High"])

    st.subheader(f"Data Insights for {gender}")

    # Filter Data Based on User Selection
    filtered_df = df[(df["gender"] == gender) & (df["intensity"] == intensity)]

    if not filtered_df.empty:
        # Display Average Calories Burned
        avg_calories = filtered_df["calories_burned"].mean()
        st.metric(label="Average Calories Burned", value=f"{avg_calories:.2f} kcal")

        # Plot Calories Distribution (Now includes activity names)
        fig = px.histogram(
            filtered_df,
            x="calories_burned",
            color_discrete_sequence=["#636EFA"],
            nbins=20,
            title="Calories Burned Distribution by Activity",
            labels={"calories_burned": "Calories Burned"},
        )
        st.plotly_chart(fig)

        # Scatter Plot of Duration vs. Calories Burned (Now includes activity names)
        fig_scatter = px.scatter(
            filtered_df,
            x="duration_minutes",
            y="calories_burned",
            color="activity_type",
            title=f"Duration vs Calories Burned for {gender}",
            labels={
                "duration_minutes": "Duration (Minutes)",
                "calories_burned": "Calories Burned",
                "activity_type": "Activity",
            },
        )
        st.plotly_chart(fig_scatter)

    else:
        st.warning("No data matches your selection. Try adjusting the filters.")
