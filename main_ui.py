# To setup our streamlit application - building forms to collect personal information ,
# collecting the macro information like the number of calories , protein etc & then adding the notes and asking AI

import streamlit as st
from macro_flow_ai import get_macros
from profiles import get_notes, create_profile, get_profile
from form_submit import update_personal_info, add_note, delete_note

st.title("Personal Fitness Tool")
# To run our application - streamlit run main_ui.py -> by default runs on port 8051


# build a personal data form
@st.fragment()  # rendered separated from the rest of UI , if any of the field gets updated this doesn't force the rest of UI to Update
def personal_data_form():
    with st.form("personal_data"):
        st.header("Personal Data")

        # Now we're going to use the profile values to fill in the values in our form ,
        # so as soon as the user saves information for example , it will actually be persisted and we'll see it update in the form
        profile = (
            st.session_state.profile
        )  # now we go to all the fields and we're gonna filling these values
        name = st.text_input("Name", value=profile["general"]["name"])
        age = st.number_input(
            "Age", min_value=1, max_value=100, step=1, value=profile["general"]["age"]
        )
        weight = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            max_value=200.0,
            step=0.1,
            value=float(profile["general"]["weight"]),
        )
        height = st.number_input(
            "Height (cm)",
            min_value=0.0,
            max_value=250.0,
            step=0.1,
            value=float(profile["general"]["height"]),
        )
        genders = ["Male", "Female", "Other"]
        gender = st.radio(
            "Gender", genders, genders.index(profile["general"].get("gender", "Male"))
        )  # default to Male
        activities = (
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Extra Active",
        )
        activity_level = st.selectbox(
            "Activity Level",
            activities,
            index=activities.index(
                profile["general"].get("activity_level", "Sedentary")
            ),
        )
        personal_data_submit = st.form_submit_button("Submit")
        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner("Submitting personal data..."):
                    # save the data
                    # all we here doing is passing all the kwargs of all the updates we want to perform within this general_type of subfield of profile
                    st.session_state.profile = update_personal_info(
                        profile,
                        "general",
                        name=name,
                        weight=weight,
                        height=height,
                        gender=gender,
                        age=age,
                        activity_level=activity_level,
                    )
                    st.success("Personal data submitted successfully")
            else:
                st.warning("Please fill all the fields")


@st.fragment()
def goals_form():
    profile = st.session_state.profile
    with st.form("goals_form"):
        st.header("Goals")
        goals = st.multiselect(
            "Select your Goals",
            ["Muscle Gain", "Fat Loss", "Stay Active"],
            default=profile.get("goals", ["Muscle Gain"]),
        )
        goals_submit = st.form_submit_button("Save")
        if goals_submit:
            if goals:
                with st.spinner("Submitting goals..."):
                    st.session_state.profile = update_personal_info(
                        profile, "goals", goals=goals
                    )
                    st.success("Goals Updated")
            else:
                st.warning("Please select atleast one goal")


@st.fragment()
def macros():
    profile = st.session_state.profile
    nutrition = st.container(border=True)
    nutrition.header("Macros")
    if nutrition.button("Generate with AI"):
        result = get_macros(profile.get("general"), profile.get("goals"))
        profile["nutrition"] = result
        nutrition.success("AI has generated  the results")

    with nutrition.form("nutrition_form", border=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            calories = st.number_input(
                "Calories",
                min_value=0,
                max_value=10000,
                step=1,
                value=profile["nutrition"].get("calories", 0),
            )
        with col2:
            protein = st.number_input(
                "Protein",
                min_value=0,
                max_value=10000,
                step=1,
                value=profile["nutrition"].get("protein", 0),
            )
        with col3:
            fat = st.number_input(
                "Fat",
                min_value=0,
                max_value=10000,
                step=1,
                value=profile["nutrition"].get("fat", 0),
            )
        with col4:
            carbs = st.number_input(
                "Carbs",
                min_value=0,
                max_value=10000,
                step=1,
                value=profile["nutrition"].get("carbs", 0),
            )
        if st.form_submit_button("Save"):
            with st.spinner("Saving..."):
                st.session_state.profile = update_personal_info(
                    profile,
                    "nutrition",
                    calories=calories,
                    protein=protein,
                    fat=fat,
                    carbs=carbs,
                )
                st.success("Informatin Saved")


# function to call the personal data form
def forms():
    if "profile" not in st.session_state:
        # This is place where we can store information that can be shared between different components
        # & kind of saved within the current state or run of this application
        # if not in this state
        profile_id = 1
        profile = get_profile(profile_id)
        if not profile:
            # create a profile
            profile_id, profile = create_profile(profile_id)
        st.session_state.profile = (
            profile  # Now we will have a profile stored in our st.session_state
        )
        st.session_state.profile_id = profile_id

    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)
    personal_data_form()
    goals_form()
    macros()


if __name__ == "__main__":
    forms()
