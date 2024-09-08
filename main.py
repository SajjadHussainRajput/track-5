import tkinter as tk
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from tkinter import messagebox
from geopy.geocoders import Nominatim
from key import key  # Import your API key from 'key.py'
import requests  # Add this for API requests


# Initialize the main window
root = tk.Tk()
root.geometry("600x600")
root.title("Phone Number Tracking and City Finder")

# Title Label
label1 = tk.Label(root, text="PHONE NUMBER TRACKING   &   CITY   FINDER .. by ( sajjo )")
label1.pack()

def get_phone_number_info():
    # Get the phone number from the Text widget
    num = number.get("1.0", tk.END).strip()
    
    try:
        # Parse the phone number
        num1 = phonenumbers.parse(num)
        
        # Get location and carrier details
        location = geocoder.description_for_number(num1, "en")
        service_provider = carrier.name_for_number(num1, "en")
        
        # Use OpenCageGeocode API to get coordinates
        ocg = OpenCageGeocode(key)
        query = str(location)
        results = ocg.geocode(query)

        if results:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
        else:
            lat = "Not Found"
            lng = "Not Found"
        
        # Get SIM owner details (name and CNIC)
        owner_name, owner_cnic = get_sim_owner_details(num)  # Fetch owner details from hypothetical API
        
        # Clear previous results
        result.delete("1.0", tk.END)
        
        # Insert new results
        result.insert(tk.END, f"Country/Region of this Number: {location}\n")
        result.insert(tk.END, f"Service Provider of this Number: {service_provider}\n")
        result.insert(tk.END, f"Latitude: {lat}\n")
        result.insert(tk.END, f"Longitude: {lng}\n")
        result.insert(tk.END, f"Owner Name: {owner_name}\n")  # Display owner name
        result.insert(tk.END, f"Owner CNIC: {owner_cnic}\n")  # Display owner CNIC
    
    except phonenumbers.NumberParseException:
        messagebox.showerror("Error", "Invalid phone number format.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_city_from_coordinates():
    try:
        # Get latitude and longitude from Text widgets
        lat = float(latitude_entry.get())
        lon = float(longitude_entry.get())
        
        # Initialize Nominatim API
        geolocator = Nominatim(user_agent="geoapiExercises")
        
        # Perform reverse geocoding
        location = geolocator.reverse((lat, lon), language='en')
        
        if location:
            city_location = location.address
        else:
            city_location = "Location not found."
        
        # Clear previous results
        result.delete("1.0", tk.END)
        
        # Insert new results
        result.insert(tk.END, f"City Location: {city_location}\n")
    except ValueError:
        messagebox.showerror("Error", "Invalid coordinates format. Please enter numeric values.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to get SIM owner details using a hypothetical API
def get_sim_owner_details(phone_number):
    """
    This function connects to a telecom API to get the SIM owner's details, including real name and CNIC.
    You will need to replace this with actual API logic when the API is available.
    """
    try:
        # Hypothetical URL for the telecom API
        api_url = f"https://api.siminfo.com/v1/getSimDetails?phone_number={phone_number}"
        headers = {
            'Authorization': 'Bearer YOUR_API_KEY_HERE'  # Replace with your API key
        }
        
        # Make the API request
        response = requests.get(api_url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
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

# Input Text widget for phone number
number = tk.Text(root, height=1, width=30)
number.pack(pady=10)

# Latitude and Longitude input fields
latitude_entry = tk.Entry(root, width=30)
latitude_entry.pack(pady=5)
latitude_entry.insert(0, "Latitude")

longitude_entry = tk.Entry(root, width=30)
longitude_entry.pack(pady=5)
longitude_entry.insert(0, "Longitude")

# Search Buttons
phone_search_button = tk.Button(root, text="Search Phone Number", command=get_phone_number_info)
phone_search_button.pack(pady=10)

location_search_button = tk.Button(root, text="Find City FROM Coordinates", command=get_city_from_coordinates)
location_search_button.pack(pady=10)

# Result Text widget
result = tk.Text(root, height=10, width=80)
result.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
