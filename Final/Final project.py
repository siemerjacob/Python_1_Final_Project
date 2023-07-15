# To run the program, you need to install the following packages:
# Pandas
# Tkinter
# Requests
# BeautifulSoup (bs4)
# Folium
# Geopy

# Run the following command to install the required packages:
# pip install pandas requests beautifulsoup4 folium geopy

# Note: Tkinter is included in the standard library for Python 3.x so you dont need to install it if you have python 3.x

# To run the program, save the code in a Python file (weather_data_fetcher.py)

# You can download the image file that I uploaded and replace the line of code:
# sun_image = PhotoImage(file="C:/Users/15153/Desktop/5-Best-Free-and-Paid-Weather-APIs-2019-e1587582023501.png")
# with the path of the downloaded PNG image.
# You can do this by right-clicking the downloaded image, copying the path, and replacing the path in the code.
# Replace "C:/Users/15153/Desktop/5-Best-Free-and-Paid-Weather-APIs-2019-e1587582023501.png" with your path.
# you also need to make sure you have rons csv editor downloaded.

# You can now run the code and press the open csv button to view the csv and view database data button to view the database data.
# note make sure you can see the python console when clicking view database because it shows in the console.
# you can now run the code :)


import requests
import pandas as pd
import tkinter as tk
from tkinter import messagebox, PhotoImage
from typing import Generator
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk
import folium
from geopy.geocoders import Nominatim
import os
import sqlite3


#sqlite weather data table
def create_weather_data_table():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        temperature REAL NOT NULL,
        humidity INTEGER NOT NULL,
        pressure INTEGER NOT NULL,
        wind_speed REAL NOT NULL,
        visibility TEXT NOT NULL
    )
    """

    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

#inserting the weather data
def insert_weather_data(weather_data: pd.DataFrame) -> None:
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()

    insert_data_query = """
    INSERT INTO weather_data (location, temperature, humidity, pressure, wind_speed, visibility)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    for _, row in weather_data.iterrows():
        cursor.execute(insert_data_query, (row["Location"], row["Temperature"], row["Humidity"], row["Pressure"], row["Wind Speed"], row["Visibility"]))

    conn.commit()
    conn.close()

#view weather data
def view_weather_data():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()

    select_data_query = "SELECT * FROM weather_data"
    cursor.execute(select_data_query)
    weather_data_rows = cursor.fetchall()

    print("ID | Location       | Temperature | Humidity | Pressure | Wind Speed | Visibility")
    print("-------------------------------------------------------------------------------")
    for row in weather_data_rows:
        print(f"{row[0]:<3} | {row[1]:<15} | {row[2]:<12} | {row[3]:<8} | {row[4]:<8} | {row[5]:<10} | {row[6]}")

    conn.close()

#clear the weather data
def clear_weather_data():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()

    delete_data_query = "DELETE FROM weather_data"
    cursor.execute(delete_data_query)
    conn.commit()

    print("Weather data table has been cleared.")

    conn.close()



# Get the coordinates of the location using Geopy
def get_location_coordinates(location: str) -> tuple:
    geolocator = Nominatim(user_agent="weather_data_fetcher")
    location_data = geolocator.geocode(location)
    return location_data.latitude, location_data.longitude

# Create a map visualization using Folium
def create_map_visualization(weather_data: pd.DataFrame) -> None:
    map_ = folium.Map(location=[0, 0], zoom_start=2)

    for _, row in weather_data.iterrows():
        lat, lon = get_location_coordinates(row["Location"])
        popup_text = f"""Location: {row["Location"]}
Temperature: {row["Temperature"]}
Humidity: {row["Humidity"]}
Pressure: {row["Pressure"]}
Wind Speed: {row["Wind Speed"]}
Visibility: {row["Visibility"]}"""
        folium.Marker([lat, lon], popup=popup_text).add_to(map_)

    map_.save("weather_data_map.html")


# Save the fetched weather data to a CSV file
def save_weather_data_to_csv(weather_data: pd.DataFrame) -> None:
    file_path = "weather_data.csv"
    if os.path.exists(file_path):
        weather_data.to_csv(file_path, mode="a", header=False, index=False)
    else:
        weather_data.to_csv(file_path, index=False)

# Open the csv file
def open_csv_file():
    csv_file_path = "weather_data.csv"
    if os.path.exists(csv_file_path):
        if os.name == 'nt':  # For Windows
            os.startfile(csv_file_path)
        elif os.name == 'posix':  # For Linux and macOS
            os.system(f"open {csv_file_path}")
        else:
            messagebox.showerror("Error", f"Unsupported operating system: {os.name}")
    else:
        messagebox.showerror("Error", f"The CSV file does not exist: {csv_file_path}")

# Clear the csv file
def clear_csv_file():
    csv_file_path = "weather_data.csv"
    if os.path.exists(csv_file_path):
        with open(csv_file_path, "w") as file:
            file.write("")  # Empty the file
        messagebox.showinfo("Success", "CSV file cleared successfully.")
    else:
        messagebox.showerror("Error", f"The CSV file does not exist: {csv_file_path}")


# Fetch weather data for a given location using OpenWeatherMap API
def fetch_weather_data(location: str, api_key: str) -> dict:
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    return response.json()

# Fetch additional weather data like visibility
def fetch_additional_weather_data(location: str) -> dict:
    base_url = f"https://www.timeanddate.com/weather/{location}/ext"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    qfacts = soup.find('div', {'id': 'qfacts'})

    visibility = "N/A"
    if qfacts:
        try:
            visibility = qfacts.find_all('p')[-1].text.split()[-2]
        except IndexError:
            pass

    return {"Visibility": visibility}

# Process and clean the fetched weather data using Pandas
def process_weather_data(data: dict, additional_data: dict) -> pd.DataFrame:
    weather_data = {
        "Location": data["name"],
        "Temperature": data["main"]["temp"],
        "Humidity": data["main"]["humidity"],
        "Pressure": data["main"]["pressure"],
        "Wind Speed": data["wind"]["speed"],
        "Visibility": additional_data["Visibility"],
    }
    return pd.DataFrame(weather_data, index=[0])

# Fetch weather data and additional data, and process the data
def fetch_and_process_data(location: str, api_key: str) -> pd.DataFrame:
    raw_weather_data = fetch_weather_data(location, api_key)
    additional_weather_data = fetch_additional_weather_data(location)
    processed_weather_data = process_weather_data(raw_weather_data, additional_weather_data)
    return processed_weather_data

# Fetch and process weather data in chunks
def weather_data_generator(locations: list, api_key: str, chunk_size: int = 1) -> Generator[pd.DataFrame, None, None]:
    with ThreadPoolExecutor() as executor:
        weather_data_chunk = list(executor.map(fetch_and_process_data, locations, [api_key]*len(locations)))

        for index, weather_data in enumerate(weather_data_chunk, start=1):
            yield weather_data

            if index % chunk_size == 0:
                weather_data_chunk = weather_data_chunk[chunk_size:]

    if weather_data_chunk:
        weather_data_chunk = weather_data_chunk

# Submit form function
def submit_form(*args):
    try:
        locations = entry_locations.get().split(', ')
        temp_unit = temperature_units_var.get()
        chunk_size = 2
        weather_data_list = []

        create_weather_data_table()

        for chunk in weather_data_generator(locations, api_key, chunk_size):
            weather_data_list.append(chunk)

        combined_weather_data = pd.concat(weather_data_list, ignore_index=True)

        if temp_unit == "Fahrenheit":
            combined_weather_data["Temperature"] = combined_weather_data["Temperature"].apply(lambda x: x * 9/5 + 32)

        display_weather_data(combined_weather_data)
        save_weather_data_to_csv(combined_weather_data)  # Call the function to save the data to a CSV file
        create_map_visualization(combined_weather_data)  # Call the function to create the map visualization
        insert_weather_data(combined_weather_data)  # Call the function to insert the data into the SQLite database

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



# Display the weather data
def display_weather_data(weather_data: pd.DataFrame):
    text_result.delete(1.0, tk.END)

    # Format the header row
    header = "{:<15} {:<15} {:<10} {:<10} {:<12} {:<10}".format("Location", "Temperature", "Humidity", "Pressure",
                                                                "Wind Speed", "Visibility")
    text_result.insert(tk.END, header + "\n", "header")

    # Add a horizontal separator
    text_result.insert(tk.END, "-" * len(header) + "\n", "separator")

    # Format the data rows
    for index, row in weather_data.iterrows():
        formatted_row = "{:<15} {:<15.1f} {:<10} {:<10} {:<12} {:<10}".format(row["Location"], row["Temperature"],
                                                                              row["Humidity"], row["Pressure"],
                                                                              row["Wind Speed"], row["Visibility"])
        if index % 2 == 0:
            text_result.insert(tk.END, formatted_row + "\n", "evenrow")
        else:
            text_result.insert(tk.END, formatted_row + "\n", "oddrow")


# Main function to execute the script
def main():
    global entry_locations, text_result, temperature_units_var

    # Create the main window
    root = tk.Tk()
    root.title("Weather Data Fetcher")

    # Load image
    sun_image = PhotoImage(file=r"C:\Users\15153\Desktop\5-Best-Free-and-Paid-Weather-APIs-2019-e1587582023501.png")
    sun_image = sun_image.subsample(2, 2)
    sun_label = tk.Label(root, image=sun_image)
    sun_label.grid(row=0, column=0, columnspan=2)

    # Create and add widgets to the window
    label_title = tk.Label(root, text="Weather Data Fetcher", font=("Segoe UI", 18, "bold"))
    label_title.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    label_locations = tk.Label(root, text="Enter locations (comma-separated):", font=("Segoe UI", 12))
    label_locations.grid(row=2, column=0, padx=10, pady=5, sticky="E")

    entry_locations = tk.Entry(root, width=40)
    entry_locations.grid(row=2, column=1, padx=10, pady=5)

    label_temp_units = tk.Label(root, text="Temperature Units:", font=("Segoe UI", 12))
    label_temp_units.grid(row=3, column=0, padx=10, pady=5, sticky="E")

    temperature_units_var = tk.StringVar(root)
    temperature_units_var.set("Celsius")
    temperature_units_dropdown = ttk.Combobox(root, textvariable=temperature_units_var,
                                              values=["Celsius", "Fahrenheit"], state="readonly", width=10)
    temperature_units_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="W")
    temperature_units_var.trace("w", submit_form)

    button_open_map = tk.Button(root, text="Open Map Visualization", command=lambda: os.system("weather_data_map.html"), font=("Segoe UI", 12))
    button_open_map.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
    button_view_data = tk.Button(root, text="View Database Data", command=view_weather_data, font=("Segoe UI", 12))
    button_view_data.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
    button_clear_data = tk.Button(root, text="Clear Database Data", command=clear_weather_data, font=("Segoe UI", 12))
    button_clear_data.grid(row=9, column=0, columnspan=2, padx=10, pady=5)
    button_open_csv = tk.Button(root, text="Open CSV File", command=open_csv_file, font=("Segoe UI", 12))
    button_open_csv.grid(row=10, column=0, columnspan=2, padx=10, pady=5)
    button_clear_csv = tk.Button(root, text="Clear CSV File", command=clear_csv_file, font=("Segoe UI", 12))
    button_clear_csv.grid(row=9, column=1, padx=10, pady=5)
    button_submit = tk.Button(root, text="Fetch Weather Data", command=submit_form, font=("Segoe UI", 12))
    button_submit.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    label_result = tk.Label(root, text="Weather Data:", font=("Segoe UI", 12))
    label_result.grid(row=5, column=0, padx=10, pady=5, sticky="NW")

    text_result = tk.Text(root, wrap=tk.WORD, width=80, height=20, font=("Consolas", 10))
    text_result.grid(row=6, column=0,columnspan=2, padx=10, pady=5)
    text_result.tag_configure("evenrow", background="#f2f2f2", font=("Consolas", 10)) # Configure tag for even rows
    text_result.tag_configure("oddrow", background="#ffffff", font=("Consolas", 10)) # Configure tag for odd rows
    text_result.tag_configure("header", background="#3a3a3a", foreground="#ffffff", font=("Consolas", 10, "bold"))  # Configure tag for header row
    text_result.tag_configure("separator", background="#ffffff", font=("Consolas", 10, "bold"))  # Configure tag for separator

    # Start the GUI event loop
    root.mainloop()


api_key = "73ee727f8152667918c6f0f7f5ddfc0a"

if __name__ == "__main__":
    main()
