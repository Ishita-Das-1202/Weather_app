# import gradio as gr
# import requests
# from bs4 import BeautifulSoup

# def get_weather(city):
#     try:
#         # Fetch weather data from wttr.in
#         # url = f"https://wttr.in/{city}?format=3"
#         find =f"Weather in {city}now"
#         url =f"https://www.google.com/search?q={find}"
#         response = requests.get(url)

#         # Basic validation
#         if response.status_code == 200:
#             return response.text
#         else:
#             return "Could not fetch weather data. Please try again."
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Gradio Interface
# demo = gr.Interface(
#     fn=get_weather,
#     inputs=gr.Textbox(label="Enter City Name"),
#     outputs=gr.Textbox(label="Weather Info"),
#     title="🌦️ Simple Weather App",
#     description="Enter a city name"
# )

# # Launch the app
# demo.launch(share=True)


import gradio as gr
import requests
from bs4 import BeautifulSoup
import random

# Random user agent to mimic a real browser
headers = {
    "User-Agent": f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

def get_weather(city):
    try:
        query = f"weather in {city}"
        url = f"https://www.google.com/search?q={query}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # print(soup)

            # Extracting elements
            location = soup.select_one("span#BBwThe")
            time_val = soup.select_one("div#wob_dts.wob_dts")
            status = soup.select_one("span#wob_dcp.wob_dcp")
            temp = soup.select_one("span#wob_tm.wob_t.q8U8x")

            if location and time_val and status and temp:
                return (
                    location.text,
                    time_val.text,
                    f"{temp.text} °C",
                    status.text
                )
            else:
                return ("N/A", "N/A", "N/A", "Could not extract weather details.")
        else:
            return ("N/A", "N/A", "N/A", "Failed to retrieve data from Google.")
    except Exception as e:
        return ("Error", "Error", "Error", str(e))

# Gradio Interface with multiple outputs
demo = gr.Interface(
    fn=get_weather,
    inputs=gr.Textbox(label="Enter City Name"),
    outputs=[
        gr.Textbox(label="📍 Location"),
        gr.Textbox(label="🕒 Time"),
        gr.Textbox(label="🌡️ Temperature"),
        gr.Textbox(label="🌤️ Condition")
    ],
    title="🌦️ Simple Weather App",
    description="Enter a city name to get real-time weather (via Google scraping)"
)

demo.launch(share=True)

