import gradio as gr
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

def get_weather(city):
    # Initialize undetected Chrome driver    
    try:
        driver = uc.Chrome()

        # Target page
        driver.get(f"https://www.google.com/search?q=weather+in+{city}")
        time.sleep(2)  # Allow JS to render content

        # Parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract data
        weather_data = {}

        # Temperature
        temp_span = soup.find("span", {"id": "wob_tm"})
        if temp_span:
            weather_data["Temperature (°C)"] = temp_span.text.strip()

        # Precipitation
        precip_span = soup.find("span", {"id": "wob_pp"})
        if precip_span:
            weather_data["Precipitation"] = precip_span.text.strip()

        # Humidity
        humidity_span = soup.find("span", {"id": "wob_hm"})
        if humidity_span:
            weather_data["Humidity"] = humidity_span.text.strip()

        # Wind
        wind_span = soup.find("span", {"id": "wob_ws"})
        if wind_span:
            weather_data["Wind"] = wind_span.text.strip()

        # Output
        for key, value in weather_data.items():
            print(f"{key}: {value}")
        return (weather_data["Temperature (°C)"],weather_data["Precipitation"],weather_data["Humidity"],weather_data["Wind"])

    finally:
        driver.quit() 

def main():
    # Gradio Interface with multiple outputs
    demo = gr.Interface(
        fn=get_weather,
        inputs=gr.Textbox(label="Enter City Name"),
        outputs=[
        gr.Textbox(label=" Temperature (°C)"),
        gr.Textbox(label=" Precipitation"),
        gr.Textbox(label=" Humidity"),
        gr.Textbox(label=" Wind")
    ],
    title="🌦️ Simple Weather App ",
    description="Enter a city name"
)

    demo.launch(share=True)
if __name__ == "__main__":
    main()
