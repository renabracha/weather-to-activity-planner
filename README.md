# Weather to Activity Planner

## Acknowledgment
I would like to thank the following individuals and organisations that made this project possible. 
* Groq for providing me free access to their API key and thereby allowing me to gain hands-on experience in making API calls without having to constantly worry about token limits.
* OpenWeather for providing me access to their current weather data through a free API key. I appreciated the API instructions were clear, concise and yet in a friendly tone. The implementation was smooth and I started pulling the weather data right away. 

## Abstract
The project showcases how well-crafted prompting is sufficient to build a Web app that pulls current weather data for the user's location, provides a weather forecast and suggests what to wear, where to go and what to do in real-time in a language of your choice, with no need to build an Agent with heavy programming.
<br>
Langchain provides a structure to the code, enhancing readability with the sequencing of modular prompt templates. 
<br>
The application follows the sequence below:
1. Ask for user location.
2. Get the current weather data based on (1).  
3. Interpret the weather data.
4. Give recommendations based on (3).

## Challenges
I wanted the Planner to communicate in the user's language, regardless of where they are. Devising a prompt that convinces Groq to switch from English 
to the language the user is using took some doing. Groq receives three clues to figure out the language: 1) the user's location (city), 2) country 
(after disambiguation due to a city of the same name, like 'London', existing in multiple countries), and 3) the writing system the user uses to enter 
their location. It correctly identifies the clues every time, but only a long-winded and repetitive prompt did the job. It just goes to show what seems 
obvious to one is clearly not obvious to another.

What started off as a Langchain sequencing demonstration in a .ipynb file on Google Colab morphed into an unrecognisable beast when it came to packaging it as a 
streamlit Web app in a .py file. Unlike some previous streamlit apps I worked on, this one was convoluted so much so that all the functions had to be 
re-written as streamlit functions with a lot of help from Claude. 

# Installation
To run weather_to_activity_planner.py, do the following:

### Step 1. Place the files in a folder. 
1. Place the `.py` file in a local folder (e.g. `C:\temp\weather_to_activity_planner`).
2. Create a file called `.env` and place the GROQ API key in the following format:
	`GROQ_API_KEY = <groq_api_key>`
  `OPENWEATHER_API_KEY = <openweather_api_key>`
3. Place the `.env` file in the same local folder. 

### Step 2. Install Python. 
1. In Windows, open the Command Prompt window.
2. Make sure Python is installed. In the Command Prompt window, type:
	`python --version`
If you get an error or "Python is not recognized", you need to install Python:
	1. Go to `https://www.python.org/downloads/`.
	2. Download the latest Python installer for Windows
	3. Run the installer and make sure to check `Add Python to PATH` during installation

### Step 3. Set up a virtual environment. 
This keeps your project dependencies isolated:
1. In the Command Prompt window, go to the script folder. Type:<br>
	`cd C:\<path to your script folder>`
2. In the Command Prompt, create a Python virtual environment named `weather_env`.<br>
	`python -m venv weather_env`
3. In the Command Prompt, activate the Python virtual environment.<br>
	`weather_env\Scripts\activate`
4. Install the required dependencies.<br>
  `pip install -r requirements.txt`

### Step 4. Install the required packages. 
1. In the Command Prompt window, type:<br>
	`pip install python-dotenv groq langchain langchain_groq streamlit`

### Step 5. Run the script. 
1. In the Command Prompt window, run the Streamlit application. Type:<br>
	`streamlit run weather_to_activity_planner.py`
<br>
<br>
This will start a local web server and open the application in your browser. Press the Analyse button to view the results. 

## Web app in action
### English
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/0_enter_location_en.jpg?raw=true)
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/1_enter_country_en.jpg?raw=true)
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/2_forecast_recommendations_en.jpg?raw=true)

### Japanese
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/0_enter_location_ja.jpg?raw=true)
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/1_enter_country_ja.jpg?raw=true)
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/2_forecast_recommendations_ja.jpg?raw=true)

### Spanish
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/0_enter_location_es.jpg?raw=true)
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/1_enter_country_es.jpg?raw=true)
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/2_forecast_recommendations_es.jpg?raw=true)

### Hebrew
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/0_enter_location_he.jpg?raw=true)
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/1_enter_country_he.jpg?raw=true)
![Alt text for screen reader](https://github.com/renabracha/weather-to-activity-planner/blob/main/2_forecast_recommendations_he.jpg?raw=true)