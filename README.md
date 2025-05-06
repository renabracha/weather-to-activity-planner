# Weather to Activity Planner

## Acknowledgment
I would like to thank the following individuals and organisations that made this project possible. 
* Groq for providing me free access to their API key and thereby allowing me to gain hands-on experience in making API calls without having to constantly worry about token limits.
* OpenWeather for providing me access to their current weather data through a free API key. I appreciated the API instructions were clear, concise and yet in a friendly tone. The implementation was smooth and I started pulling the weather data right away. 

## Abstract
This project demonstrates how effective prompt engineering alone can power a fully functional web app that retrieves real-time weather data based on the user's location, interprets it, and offers personalized suggestions - including what to wear, where to go, and what to do - all in the user's preferred language. No complex agent design or heavy programming is required.
<br><br>
The application follows this sequence:
1. Prompt the user to enter their location.
2. Retrieve current weather data based on the input.
3. Analyze and interpret the weather information.
4. Provide personalized activity, clothing, and destination recommendations.

## Development Notes
* **LangChain** adds structure and modularity to the code by sequencing prompt templates for weather analysis, recommendation generation, and localization.
* Some place names are inherently ambiguous — for example, “London” could refer to the capital of the UK or a city in Canada. The model leverages its pre-trained geographic knowledge to detect such cases and prompts the user for clarification when necessary.
* Despite the constraints of a free-tier weather API (limited data), the model produces meaningful interpretations. It supplements minimal weather data with creative, practical suggestions for indoor/outdoor activities, tourist spots, and weather-appropriate outfits - drawing on the model's general knowledge.

## Challenges
* A key goal was for the Planner to communicate in the user's language, no matter their location. Achieving this required crafting a detailed and somewhat repetitive prompt to encourage Groq to switch from English. The model is guided by three cues:
  1. The user's entered location (e.g., city).
  2. The disambiguated country name.
  3. The writing system (script) used when entering the location.

  While Groq correctly interprets the clues every time, it took significant prompt tuning to achieve the desired multilingual output. What feels obvious to humans often needs to be spelled out for LLMs.

* What began as a LangChain sequencing demo in a Jupyter Notebook on Google Colab evolved into a significantly more complex Streamlit app. Unlike earlier projects, packaging this logic into a `.py` script required rewriting nearly every function using Streamlit’s interactive UI patterns - with substantial help from Claude to restructure the logic for a web-based workflow.

## Installation
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

### Step 4. Run the script. 
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