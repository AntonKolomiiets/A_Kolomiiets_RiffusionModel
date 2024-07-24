# Hello again Reface!

This is a Streamlit application that uses Riffusion model. This project allows users to upload videos, generate audio from text prompts, and replace the audio in the video clips.

## Extra

The Riffusion model is a good approach for audio generation, but it needs extensive prompt engineering and, in addition, more thorough post-processing to achieve decent-sounding clips. Here is a Streamlit app that uses a different model, which sounds better in my opinion: ["link"](https://github.com/AntonKolomiiets/A_Kolomiiets_StableAudio). I did not combine the two to avoid creating bloat in the Streamlit code, so it is cleaner and more readable. Also, the two apps have slightly different approaches to part selection, as this one does not have custom duration selection.

## Installation

To run the application locally, clone the repo from GitHub with `git clone`, install dependencies with `pip install -r requirements.txt` and run with `streamlit run app.py`
