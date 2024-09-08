import streamlit as st
import main
import utils
from experience_mappings import travel_experiences

# First row of input fields
col1, col2, col3, col4 = st.columns(4)

with col1:
    city = st.text_input("Destination City")
with col2:
    start_date = st.date_input("Start date")
    start_date_str = start_date.strftime("%Y-%m-%d")
with col3:
    end_date = st.date_input("End date")
    end_date_str = end_date.strftime("%Y-%m-%d")
with col4:
    traveling_options = ["Friend", "Family", "Couple", "Solo", "Group"]
    people = st.radio("Who are you traveling with?", traveling_options)

questionnaire = ""

q_1 = "What type of travel experience are you hoping to create or remember?"
# Travel Experience Type
st.header(q_1)
experience_types = [
    "Cultural Immersion",
    "Adventure Travel",
    "Relaxation and Wellness",
    "Historical Exploration",
    "Nature and Wildlife",
    "Urban Exploration",
    "Culinary Travel",
    "Volunteering",
    "Luxury Travel",
    "Road Trips",
]

selected_experiences = st.multiselect(
    "Select the types of travel experiences you're interested in:", experience_types
)

selected_experiences = "\n".join(
    [
        experience + "\n" + travel_experiences[experience]
        for experience in selected_experiences
    ]
)

questionnaire += q_1 + "\n" + selected_experiences + "\n"

q_2 = "Do you prefer active or relaxed travel experiences?"
# Travel Preferences
st.header(q_2)
travel_preferences = [
    "Mostly active and adventurous",
    "Mostly relaxed and laid-back",
    "A mix of both active and relaxed",
    "Other (please specify)",
]

selected_preference = st.selectbox("Select your preference:", travel_preferences)
questionnaire += q_2 + "\n" + selected_preference + "\n"


q_3 = "Are there any health or accessibility needs we should consider?"
# Health or Accessibility Needs
st.header(q_3)
health_needs = [
    "No specific needs",
    "Need assistance with mobility",
    "Require special dietary considerations",
    "Have a medical condition that needs attention",
]

selected_health_needs = st.selectbox(
    "Select any health or accessibility needs:", health_needs
)

questionnaire += q_3 + "\n" + selected_health_needs + "\n"

if (
    "travel_keywords" not in st.session_state
    or "questionnaire" not in st.session_state
    and questionnaire != st.session_state.questionnaire
):
    st.session_state.travel_keywords = main.get_preferences(questionnaire)
    st.session_state.questionnaire = questionnaire

selected_preferences = st.multiselect(
    "Select your travel preferences:", st.session_state.travel_keywords
)

# Submit button and processing
if st.button("Submit"):
    with st.spinner("Generating itinerary..."):
        itinerary = main.get_itinerary(
            city,
            [start_date_str, end_date_str],
            people,
            "\n".join(selected_preferences),
            questionnaire,
        )
        st.success("Itinerary generated successfully!")
        st.markdown(utils.json_to_markdown(itinerary))

    with st.spinner("Generating map..."):
        map_ = main.get_map(itinerary, city)
        st.pydeck_chart(map_)

    with st.spinner("Generating food recommendations ..."):
        food_recommendations = main.get_food_recommendations_(city)
        st.write(food_recommendations)

    with st.spinner("Generating video ..."):
        try:
            filepath = main.generate_video(itinerary, city)
            st.video(filepath)
        except Exception as e:
            print(e)
