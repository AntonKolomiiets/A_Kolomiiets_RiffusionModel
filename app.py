import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'video_processing'))

import streamlit as st
from video_processing.file_handler import handle_file_upload
from video_processing.video_splitter import split_video
from video_processing.audio_generator import generate_audio, SCHEDULER_OPTIONS
from video_processing.audio_replacer import replace_audio
from video_processing.zip_creator import create_zip


def main():
    st.set_page_config(layout="wide")
    st.title("Hi Reface!")

    # Session state variables
    if "results" not in st.session_state:
        st.session_state['results'] = None
    if "prompt" not in st.session_state:
        st.session_state["prompt"] = ""
    
    # Model and clips settings
    with st.sidebar:
        st.header("Upload and Settings")
        video_file = st.file_uploader("Upload a video file", type=["mp4", "avi"])
        num_clips = st.number_input("Number of clips", min_value=1)
        prompt = st.text_input("Audio generation prompt", value=st.session_state["prompt"], key="prompt")

        with st.expander("Model Settings"):
            scheduler = st.selectbox("Scheduler", SCHEDULER_OPTIONS, index=0)
            use_20k = st.checkbox("Use 20kHz", value=False)
            guidance = st.slider("Guidance", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
            seed = st.number_input("Seed", min_value=1, max_value=1000) 
            
        clip_with_audio = st.number_input("Clip number to add audio", min_value=1)
        num_columns = st.number_input("Number of columns", min_value=3)
    
        
    # Process files
    if st.button("Process"):
        if video_file and st.session_state.prompt:
            # Upload file
            video_path = handle_file_upload(video_file)

            # Split video to clips
            clips = split_video(video_path, num_clips)

            # Generate audio file
            audio_path = generate_audio(
                prompt=st.session_state.prompt,
                scheduler=scheduler,
                use_20k=use_20k,
                guidance=guidance,
                starting_seed=seed)
           
            # Replace audio
            clips[clip_with_audio - 1] = replace_audio(clips[clip_with_audio - 1], audio_path[0])
            
            # Create Zip file
            zip_path = create_zip(clips)
            
            
            st.success("Processing complete! Download the clips below.")

            

        else:
            st.error("Please upload a video file and provide an audio prompt.")

        # Download clips as Zip folder
        with open(zip_path, "rb") as f:
                st.download_button("Download Clips", data=f, file_name="clips.zip")
            
        # Display results in columns
        st.write("### Generated Clips:")
        columns = st.columns(num_columns)
        for i, clip in enumerate(clips):
            col = columns[i % num_columns]
            col.video(clip)


if __name__ == "__main__":
    main()
