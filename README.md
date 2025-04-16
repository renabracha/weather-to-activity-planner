# Weather to Activity Planner

This is a little demonstration that prompting is enough to build a Web app that provides a weather forecast and suggests what to wear, where to go and what to do in real-time in a language of your choice, with no need to build an Agent with heavy programming. 

The use of Langchain provides a structure to the code, enhancing readability with the sequencing of modular prompt templates. 

The application follows the sequence below:
1. Ask for user location.
2. Get the current weather data based on (1).  
3. Interpret the weather data.
4. Give recommendations based on (3).

The Planner pulls local weather data from OpenWeather, then prompts the LLM to suggest outfits, indoor/outdoor activities and travel plans. You can get a free API key from the OpenWeather website, which gives you access to the current weather data free of charge.


To run weather_to_activity_planner.py, do the following:

### Step 1. Place the files in a folder. 
1. Place the .py file in a local folder (e.g. C:\temp\weather_to_activity_planner).
2. Create a file called ".env" and place the GROQ API key and OpenWeather API key in the following format:
	GROQ_API_KEY = <groq_api_key>
	OPENWEATHER_API_KEY = <openweather_api_key>
3. Place the .env file in the same local folder. 

### Step 2. Install Python. 
1. In Windows, open the Command Prompt window.
2. Make sure Python is installed. In the Command Prompt window, type:
	python --version
If you get an error or "Python is not recognized", you need to install Python:
	1. Go to https://www.python.org/downloads/
	2. Download the latest Python installer for Windows
	3. Run the installer and make sure to check "Add Python to PATH" during installation

### Step 3. Set up a virtual environment. 
This keeps your project dependencies isolated:
1. In the Command Prompt window, go to the script folder. Type:
	cd c:\<path to your script folder>.
2. In the Command Prompt, create a Python virtual environment named "weather_env".
	python -m venv weather_env
3. In the Command Prompt, activate the Python virtual environment.
	weather_env\Scripts\activate

### Step 4. Install the required packages. 
1. In the Command Prompt window, type:
	pip install python-dotenv groq langchain langchain_groq streamlit

### Step 5. Run the script. 
1. In the Command Prompt window, run the Streamlit application. Type:
	streamlit run weather_to_activity_planner.py

This will start a local web server and open the application in your browser. Press the Start button to plan your day. 