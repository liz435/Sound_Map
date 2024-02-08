import streamlit as st
from streamlit_folium import st_folium
import folium
import os
from supabase import create_client, Client
from dotenv import load_dotenv


def main():
    st.title('New York City Sound Map')
    location = [40.7128, -74.0060]
    zoom_start = 12 
    m = create_map(location, zoom_start)
    st_folium(m, width=725, height=500)

    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    data = supabase.table('Sound_Map').select('location').execute()
    st.write(len(data.data))

    if st.button('idk yet'):
        pass
    if st.button('Add Content'):
        # Step 2: Display file uploaders and text input for address upon button click
        with st.form("add_content_form", clear_on_submit=True):  # Form to add content
            st.write("Please upload your content")
            uploaded_image = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
            uploaded_audio = st.file_uploader("Upload Audio", type=['mp3', 'wav'])
            address = st.text_input("Address")
            text = st.text_input("Text")
            print('smitprev')
            
            # Submit button for the form
            submitted = st.form_submit_button("Submit Content", use_container_width = True)
            if submitted:
                dataIn = supabase.table("Sound_Map").insert({"text_description":text}).execute()
                assert len(dataIn.data) > 0
                print('here')
                # Step 3: Process the uploaded files and address
                if uploaded_image is not None and uploaded_audio is not None and address:
                    st.success("Content uploaded successfully!")
                    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
                    # For audio, you might want to save it and use an audio player to play it
                    # Display the address or use it as needed
                    st.write(f"Address: {address}")
                    st.write(f"Text: {text}")
                    print(text)
                else:
                    st.error("Please upload both an image and an audio file, and enter an address.")
                    print("error")





def create_map(location, zoom_start=10):
    m = folium.Map(location=location, zoom_start=zoom_start)
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
    
    folium.Marker(
        location, 
        popup=folium.Popup(audio_html, max_width=300), 
        icon=icon
    ).add_to(m)
    return m

if __name__ == "__main__":
    main()






