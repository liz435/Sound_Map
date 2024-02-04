import streamlit as st
from streamlit_folium import st_folium
import folium


def create_map(location, zoom_start=10):
    # Create the Folium map object
    m = folium.Map(location=location, zoom_start=zoom_start)
    
    # HTML content for the popup, including an audio player
    audio_html = """
    <h4 style = "font-family: EB Garamon">The forecast said the sun had ended its residency 
in forbearance. A shock in the spine of wind woke you 
from a mandatory hibernation. You had blue bangs and insisted to stay soft like an egg yolk. 
Sorrow is making its way into your fist, yet winter decides to stay longer in this shared mist.</h4>
     <img src="http://localhost:8001/images/test.png" alt="Girl in a jacket" width="150" height="150" style="margin-left:75px ">
    <audio controls>
      <source src="http://localhost:8001/sound/sound.mp3" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>
    """
    icon = folium.Icon(color="red", icon="info-sign")
    
    # Adding a marker with the custom HTML popup
    folium.Marker(
        location, 
        popup=folium.Popup(audio_html, max_width=300), 
        icon=icon
    ).add_to(m)

    return m

# Streamlit app layout
st.title('New York City Sound Map')
# st.write('This is a web app to display a Folium map with a custom marker. Click the marker to play audio.')

# Map initialization
location = [40.7128, -74.0060]  # Example location (New York City)
zoom_start = 12  # Map zoom level

# Create a folium map object with a custom marker
m = create_map(location, zoom_start)

# Display the map in the Streamlit app
st_folium(m, width=725, height=500)
