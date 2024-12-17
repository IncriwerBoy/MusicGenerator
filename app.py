import streamlit as st
import os
import pygame
import logging
from helper import predict, convert  # Adjust the import as necessary

# Set up logging
logging.basicConfig(level=logging.INFO)

st.title('Music Generator')

def generate_music():
    try:
        # Call the predict and convert functions
        output_notes = predict()
        output = convert(output_notes)
        
        # Save the output to a MIDI file
        midi_file_path = 'output.mid'
        with open(midi_file_path, 'wb') as f:
            f.write(output)
        
        st.success('Music generated successfully!')
        logging.info('Music generated and saved to output.mid')
    except Exception as e:
        # st.error(f"An error occurred: {e}")
        logging.error(f"An error occurred during music generation: {e}")

def play_midi(file_path):
    try:
        pygame.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        st.success('Music is playing!')
    except Exception as e:
        st.error(f"An error occurred while playing the MIDI file: {e}")
        logging.error(f"An error occurred while playing the MIDI file: {e}")

def stop_midi():
    try:
        pygame.mixer.music.stop()
        pygame.quit()
        st.success('Music stopped successfully!')
    except Exception as e:
        st.error(f"An error occurred while stopping the MIDI file: {e}")
        logging.error(f"An error occurred while stopping the MIDI file: {e}")

if st.button('Generate'):
    generate_music()

midi_file_path = 'output.mid'

if os.path.exists(midi_file_path):
    st.audio(midi_file_path)
    

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button('Play'):
            play_midi(midi_file_path)
    with col2:
        if st.button('Stop'):
            stop_midi()
    with col3:
        with open(midi_file_path, "rb") as f:
                st.download_button(label="Download", data=f, file_name="output.mid")
        
else:
    st.warning('Generate the music first to play the MIDI file.')
