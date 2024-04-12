import streamlit as st
from streamlit_folium import st_folium
import folium
import os
import uuid
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
import re

def main():
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    
    zoom_start = 12
    location = [40.7128, -74.0060]  
    m = folium.Map(location=location, zoom_start=zoom_start)
    

    add_markers(supabase, m)
    st.title('New York City Garbage Map')
    st_folium(m, width=725, height=500)
    handle_content_upload(supabase)

def add_markers(supabase, map_obj):
    data = supabase.table("Sound_Map").select("id, location, text_description, audio_url, image_url").execute().data
    if not data:
        st.error("No data found")
        return

    for entry in data:
        audio_url = entry['audio_url']
        image_url = entry['image_url']  
        if 'location' in entry and entry['location']:
            location = entry['location']
            text_description = entry.get('text_description', 'No description available')
            create_marker(map_obj, location, text_description, audio_url, image_url)

def create_marker(map_obj, location, text_description, audio_url, image_url):
    audio_html = f"""
    <h4 style = "font-family: EB Garamon">{text_description}</h4>
    <img src="{image_url}" style="transform:rotate(90deg); margin-top:20px; margin-left:20px;" alt="Image" width="250" height="200" >
    <audio controls>
        <source src="{audio_url}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    """
    icon = folium.Icon(color="red", icon="info-sign")
    folium.Marker(
        location,
        popup=folium.Popup(audio_html, max_width=300),
        icon=icon
    ).add_to(map_obj)


def handle_content_upload(supabase):
    if st.button('Add Content'):
        st.session_state['add_content'] = True 

    if st.session_state.get('add_content', False):
        with st.form("add_content_form", clear_on_submit=True):
            st.write("Please upload your content")
            uploaded_image = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
            uploaded_audio = st.file_uploader("Upload Audio", type=['mp3', 'wav'])
            latitude = st.text_input("Latitude", value="40.7128")
            longitude = st.text_input("Longitude", value="-74.0060")
            text = st.text_input("Text")
            submitted = st.form_submit_button("Submit Content")
            if submitted:
                process_submission(supabase, uploaded_image, uploaded_audio, latitude, longitude, text)

def process_submission(supabase, uploaded_image, uploaded_audio, latitude, longitude, text):
        
        if uploaded_image is None:
            image_url = None
        else: 
            image_url = upload_file_to_storage(supabase, uploaded_image, "Sound_Map_Image")

        if uploaded_audio is None:
            audio_url = None
        else:
            audio_url = upload_file_to_storage(supabase, uploaded_audio, "Sound_Map")
        
        if text and longitude and latitude:
            location = [float(latitude), float(longitude)]
            insert_entry(supabase, text, location, image_url, audio_url)
            st.success("Content uploaded successfully!")
        else:
            st.error("Failed to upload files.")
def sanitize_filename(filename):
    sanitized = re.sub(r'\s+', '_', filename)
    sanitized = re.sub(r'[^\w.-]', '', sanitized)
    return sanitized

def upload_file_to_storage(supabase, file, bucket_name):
    if file is None:
        return None

    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    original_file_name = file.name
    sanitized_file_name = sanitize_filename(original_file_name)
    extension = os.path.splitext(sanitized_file_name)[1]
    new_file_name = f"{timestamp}_{unique_id}{extension}"
    file_bytes = file.getvalue()
    
    response = supabase.storage.from_(bucket_name).upload(new_file_name, file_bytes)
    

    if response.status_code != 200:

        error_message = response.json().get('message', 'Unknown error')
        st.error(f"Failed to upload file: {error_message}")
        return None
    else:
   
        supabase_url = os.getenv("SUPABASE_URL").rstrip("/")
        file_url = f"{supabase_url}/storage/v1/object/public/{bucket_name}/{new_file_name}"
        return file_url


def insert_entry(supabase, text, location, image_url, audio_url):
    response = supabase.table("Sound_Map").insert({
        "text_description": text,
        "location": location,
        "image_url": image_url,
        "audio_url": audio_url
    }).execute()
    

    if hasattr(response, 'error') and response.error:

        st.error(f"An error occurred while inserting the data: {response.error.message}")
    elif hasattr(response, 'data') and response.data:

        st.success("Data inserted successfully")
    else:

        st.error("Failed to insert data due to an unexpected issue.")


# Main execution
if __name__ == "__main__":
    main()
