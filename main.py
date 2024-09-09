import tkinter as tk
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from tkinter import messagebox
from geopy.geocoders import Nominatim
from key import key  # Import your API key from 'key.py'
import requests


# Initialize the main window
root = tk.Tk()
root.geometry("600x600")
root.title("Phone Number Tracking and City Finder")

# Title Label
label1 = tk.Label(root, text="PHONE NUMBER TRACKING   &   CITY   FINDER .. by ( sajjo )")
label1.pack()

def get_phone_number_info():
    num = number.get("1.0", tk.END).strip()
    
    try:
        num1 = phonenumbers.parse(num)
        location = geocoder.description_for_number(num1, "en")
        service_provider = carrier.name_for_number(num1, "en")
        
        ocg = OpenCageGeocode(key)
        query = str(location)
        results = ocg.geocode(query)

        if location and results:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
        else:
            lat = "Not Found"
            lng = "Not Found"
        
        owner_name, owner_cnic = get_sim_owner_details(num)
        
        result.delete("1.0", tk.END)
        result.insert(tk.END, f"Country/Region of this Number: {location}\n")
        result.insert(tk.END, f"Service Provider of this Number: {service_provider}\n")
        result.insert(tk.END, f"Latitude: {lat}\n")
        result.insert(tk.END, f"Longitude: {lng}\n")
        result.insert(tk.END, f"Owner Name: {owner_name}\n")
        result.insert(tk.END, f"Owner CNIC: {owner_cnic}\n")
    
    except phonenumbers.NumberParseException:
        messagebox.showerror("Error", "Invalid phone number format.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_city_from_coordinates():
    try:
        lat_str = latitude_entry.get().strip()
        lon_str = longitude_entry.get().strip()

        if not lat_str or not lon_str:
            raise ValueError("Latitude and Longitude cannot be empty.")
        
        lat = float(lat_str)
        lon = float(lon_str)
        
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse((lat, lon), language='en')
        
        if location:
            city_location = location.address
        else:
            city_location = "Location not found."
        
        result.delete("1.0", tk.END)
        result.insert(tk.END, f"City Location: {city_location}\n")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_sim_owner_details(phone_number):
    try:
        api_url = f"https://api.siminfo.com/v1/getSimDetails?phone_number={phone_number}"
        headers = {
            'Authorization': 'Bearer YOUR_REAL_API_KEY'
        }
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            owner_name = data.get('owner_name', 'Not Available')
            owner_cnic = data.get('owner_cnic', 'Not Available')
        else:
            owner_name = "Not Available"
            owner_cnic = "Not Available"
    
    except Exception as e:
        owner_name = "Error"
        owner_cnic = str(e)
    
    return owner_name, owner_cnic

number = tk.Text(root, height=1, width=30)
number.pack(pady=10)

latitude_entry = tk.Entry(root, width=30)
latitude_entry.pack(pady=5)
latitude_entry.insert(0, "Latitude")

longitude_entry = tk.Entry(root, width=30)
longitude_entry.pack(pady=5)
longitude_entry.insert(0, "Longitude")

phone_search_button = tk.Button(root, text="Search Phone Number", command=get_phone_number_info)
phone_search_button.pack(pady=10)

location_search_button = tk.Button(root, text="Find City FROM Coordinates", command=get_city_from_coordinates)
location_search_button.pack(pady=10)

result = tk.Text(root, height=10, width=80)
result.pack(pady=10)

root.mainloop()
