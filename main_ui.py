# To setup our streamlit application - building forms to collect personal information ,
# collecting the macro information like the number of calories , protein etc & then adding the notes and asking AI

import streamlit as st

st.title("Personal Fitness Tool")
# To run our application - streamlit run main_ui.py -> by default runs on port 8051

# build a personal data form
@st.fragment() # rendered separated from the rest of UI , if any of the field gets updated this doesn't force the rest of UI to Update
def personal_data_form():
    with st.form("personal_data"):
        st.header("Personal Data")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100,step=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=200.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, step=0.1)
        gender = st.radio("Gender", ["Male", "Female","Other"])
        activities = (
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Extra Active",
        )
        activity_level = st.selectbox("Activity Level", activities)
        personal_data_submit = st.form_submit_button("Submit")
        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
               with st.spinner("Submitting personal data..."):
                   # save the data
                st.success("Personal data submitted successfully")
            else:
                st.warning("Please fill all the fields")

# function to call the personal data form            
def forms():
    personal_data_form()            

if __name__ == "__main__":
    forms()