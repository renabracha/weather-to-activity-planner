import os
import requests
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Set up the environment variables
load_dotenv()

# Initialise the model
os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
llm = ChatGroq(model = "llama-3.3-70b-versatile")

# Access the OpenWeather API
os.environ["OPENWEATHER_API_KEY"] = os.getenv('OPENWEATHER_API_KEY')

# A lookup table for the language codes and names. OpenWeather provides weather data in these languages
language_lookup = {
  "sq": "Albanian",
  "af": "Afrikaans",
  "ar": "Arabic",
  "az": "Azerbaijani",
  "eu": "Basque",
  "be": "Belarusian",
  "bg": "Bulgarian",
  "ca": "Catalan",
  "zh_cn": "Chinese Simplified",
  "zh_tw": "Chinese Traditional",
  "zh_cn": "Simplified Chinese",
  "zh_tw": "Traditional Chinese",
  "hr": "Croatian",
  "cz": "Czech",
  "da": "Danish",
  "nl": "Dutch",
  "en": "English",
  "fi": "Finnish",
  "fr": "French",
  "gl": "Galician",
  "de": "German",
  "el": "Greek",
  "he": "Hebrew",
  "hi": "Hindi",
  "hu": "Hungarian",
  "is": "Icelandic",
  "id": "Indonesian",
  "it": "Italian",
  "ja": "Japanese",
  "kr": "Korean",
  "ku": "Kurdish",
  "la": "Latvian",
  "lt": "Lithuanian",
  "mk": "Macedonian",
  "no": "Norwegian",
  "fa": "Persian",
  "pl": "Polish",
  "pt": "Portuguese",
  "pt_br": "Brasilian Portuguese",
  "ro": "Romanian",
  "ru": "Russian",
  "sr": "Serbian",
  "sk": "Slovak",
  "sl": "Slovenian",
  "sp": "Spanish",
  "es": "Spanish",
  "sv": "Swedish",
  "se": "Swedish",
  "th": "Thai",
  "tr": "Turkish",
  "ua": "Ukrainian",
  "uk": "Ukrainian",
  "vi": "Vietnamese",
  "zu": "Zulu"
}

# Functions to check location ambiguity
def check_location_ambiguity(location):
    ambiguity_prompt = f"""Check whether there is more than one place around the world with the name {location}.
    For example, there is 'London' in the UK and in Ontario, Canada.
    Return 'yes' if the place name is ambiguous, otherwise 'no'."""
    ambiguous = llm.invoke(ambiguity_prompt).content.strip().lower()
    return "yes" in ambiguous

# Get country for a location
def get_country_for_location(location):
    get_country_prompt = f"""Find the name of the country where {location} is located.
    Return only the name of the country in English and nothing else.
    Keep the answer short."""
    country = llm.invoke(get_country_prompt).content.strip()
    return country

# Detect the language based on location and country
def detect_language(location, country):
    get_language_prompt = f"""Look at {location} and {country} and detect the language the user is using.
    Return only the name of the language in English and nothing else.
    Keep the answer short."""
    language = llm.invoke(get_language_prompt).content.strip().lower()
    return language

# Get confirmation message
def get_confirmation_message(location, country, language):
    confirmation_prompt = f"""You are given a location '{location}' and country '{country}'.
    The user is writing in {language}.

    If {language} is English, return exactly: 'Got it! You're in {location}, {country}.'

    If {language} is not English, you MUST translate the ENTIRE message into {language}.
    For example, if {language} is Japanese, translate 'Got it! You're in {location}, {country}.' completely into Japanese.
    Pay attention to the word order, following the grammar of the {language}.
    For example, if {language} is Japanese, the correct word order will be 'わかりました！あなたは日本の東京にいるのですね。'.
    DO NOT keep any English words in your response.
    DO NOT use English for any part of the response.
    Respond ONLY in {language} with proper characters, punctuation, and grammar for that language.

    Return ONLY the translated message with no explanations."""
    message = llm.invoke(confirmation_prompt).content.strip()
    return message

# Convert the language name to OpenWeather's language code
def get_language_code(language, language_lookup=language_lookup):
    # Normalise the input by converting to lowercase
    normalised_name = language.lower()

    # Search through the dictionary for matching language name
    for code, name in language_lookup.items():
        if name.lower() == normalised_name:
            return code

    # Return None if no match is found
    return None

# Get the current weather data using OpenWeather API
def get_weather_data(location, country, language_code):
    # Define the API endpoint and query parameters
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Format location and country for the 'q' parameter
    location_param = f"{location},{country}" if country else location
    params = {
        "q": location_param,
        "units": "metric",
        "lang": language_code,
        "APPID": os.environ["OPENWEATHER_API_KEY"] 
    }

    # Define the request headers with API key and host
    headers = {
        "Accept": "application/json"
    }

    # Send a GET request to the API endpoint with query parameters and headers
    response = requests.request("GET", url, headers=headers, params=params)

    # Parse the response data
    data = response.json()

    # Return the weather data
    return data

# Define prompts and prompt templates
interpret_weather_prompt = PromptTemplate(
    input_variables=["weather_data","language"],
    template = """Tell me the weather now, based on the information in {weather_data}.
    Include information about:
    * the current temperature with high and low
    * feels_like temperature
    * atmospheric pressure
    * humidity
    * visibility
    * wind speed and direction

    To predict the likelihood of rain, focus on the following data to make the prediction:
    * 'weather id'
    * 'description'
    * 'humidity'
    * 'clouds'

    Provide only the weather forecast with no preamble.
    Instead of presenting the information in a dry factual manner of bullet points, concatenate all the information into a couple of naturally flowing sentences in a friendly tone.
    Give the weather forecast in {language}.
    """
)

suggestion_prompt = PromptTemplate(
    input_variables=["weather_interpretation", "language"],
    template = """Based on {weather_interpretation}, make suggestions on:
    * how to dress
    * stay indoors or enjoy going out
    * where to visit
    * what activities to do
    * whether or not to take an umbrella if rain is expected

    Instead of presenting the information in a dry factual manner of bullet points, concatenate all the information into a couple of naturally flowing sentences in a friendly tone.
    Do not repeat what is already mentioned in {weather_interpretation} but rather, add to it.
    Give the suggestions in {language}.
    """
)

# Chain the prompts
def weather_to_activity_planner_chain(weather_data, language):
    """Get the user location, get the weather data, interpret the weather data, and make recommendations.

    Args:
        weather_data (dict): Weather data from OpenWeather API.
        language (str): The language in which to respond.

    Returns:
        str: A summary of the current weather and recommendations on outfit and activity.
    """
    weather_interpretation = (interpret_weather_prompt | llm).invoke({"weather_data": weather_data, "language": language}).content
    suggestions = (suggestion_prompt | llm).invoke({"weather_interpretation": weather_interpretation, "language": language}).content
    return weather_interpretation, suggestions

# Streamlit UI
st.title('Weather-to-Activity Planner with Prompt Engineering')

# Welcome message
st.markdown("""
Hey there! 👋 I'm your Weather-to-Activity Planner.  
Think of me as your personal guide to the day —  
I'll let you know what the weather's like,  
suggest what to wear, and even give you fun ideas for what to do and where to go!  
Just tell me where you are right now, and we'll get started. 🌤️✨  
Oh, and you can ask me in any language you'd like. 🌍
""")

# Create session state to store variables
if 'step' not in st.session_state:
    st.session_state.step = 'location'
if 'location' not in st.session_state:
    st.session_state.location = None
if 'country' not in st.session_state:
    st.session_state.country = None
if 'is_ambiguous' not in st.session_state:
    st.session_state.is_ambiguous = False
if 'language' not in st.session_state:
    st.session_state.language = None
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None
if 'weather_interpretation' not in st.session_state:
    st.session_state.weather_interpretation = None
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = None

# Step 1: Get location
if st.session_state.step == 'location':
    location_input = st.text_input("Your location:", key="location_input")
    if st.button("Next", key="location_button"):
        if location_input:
            st.session_state.location = location_input
            with st.spinner('Checking location...'):
                st.session_state.is_ambiguous = check_location_ambiguity(location_input)
            st.session_state.step = 'country'
            st.rerun()

# Step 2: Get country (if needed)
elif st.session_state.step == 'country':
    if st.session_state.is_ambiguous:
        country_input = st.text_input(f"There are multiple locations with that name. Could you let me know which country {st.session_state.location} is in?", key="country_input")
        if st.button("Next", key="country_button"):
            if country_input:
                st.session_state.country = country_input
                st.session_state.step = 'process'
                st.rerun()
    else:
        with st.spinner('Detecting country...'):
            st.session_state.country = get_country_for_location(st.session_state.location)
            st.session_state.step = 'process'
            st.rerun()

# Step 3: Process all data and show results
elif st.session_state.step == 'process':
    # Validate that we have all required data
    if not (st.session_state.location and st.session_state.country):
        st.session_state.step = 'location'
        st.rerun()
    try:
        # Detect language
        with st.spinner('Detecting language...'):
            st.session_state.language = detect_language(st.session_state.location, st.session_state.country)
            
        # Get and display confirmation message
        with st.spinner('Confirming location...'):
            confirmation = get_confirmation_message(st.session_state.location, st.session_state.country, st.session_state.language)
            st.success(confirmation)
        
        # Get weather data
        with st.spinner('Getting the weather data...'):
            language_code = get_language_code(st.session_state.language)
            st.session_state.weather_data = get_weather_data(st.session_state.location, st.session_state.country, language_code)
            st.success('Successfully retrieved weather data')
        
        # Generate suggestions
        with st.spinner('Putting together some suggestions...'):
            st.session_state.weather_interpretation, st.session_state.suggestions = weather_to_activity_planner_chain(st.session_state.weather_data, st.session_state.language)
            
        # Display results    
        st.subheader("Current Weather")
        st.markdown(st.session_state.weather_interpretation)
        
        st.subheader("Recommendations")
        st.markdown(st.session_state.suggestions)
        st.success('Have a great day!')
        
        # Reset button
        if st.button("Start over", key="reset_button"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.session_state.step = 'location'  # Set initial step explicitly
            st.rerun()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.button("Try again", key="error_button"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()