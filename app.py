import streamlit as st
from streamlit_folium import st_folium
import folium

def create_map(location, zoom_start=10):
    # Create the Folium map object
    m = folium.Map(location=location, zoom_start=zoom_start)
    
    # HTML content for the popup, including an audio player
    audio_html = """
    <h4>This is where you say something</h4>
     <img src="http://localhost:8000/images/test.png" alt="Girl in a jacket" width="150" height="150">
    <audio controls>
      <source src="http://localhost:8000/sound/sound.mp3" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>
    """
    
    # Custom icon (optional)
    icon = folium.Icon(color="red", icon="info-sign")
    
    # Adding a marker with the custom HTML popup
    folium.Marker(
        location, 
        popup=folium.Popup(audio_html, max_width=300), 
        icon=icon
    ).add_to(m)
    
    return m

# Streamlit app layout
st.title('Folium Map with Custom Marker and Audio in Streamlit')
st.write('This is a web app to display a Folium map with a custom marker. Click the marker to play audio.')

# Map initialization
location = [40.7128, -74.0060]  # Example location (New York City)
zoom_start = 12  # Map zoom level

# Create a folium map object with a custom marker
m = create_map(location, zoom_start)

# Display the map in the Streamlit app
st_folium(m, width=725, height=500)
