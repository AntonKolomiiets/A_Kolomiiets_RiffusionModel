import typing as T
import os

from riffusion.spectrogram_params import SpectrogramParams
from riffusion.streamlit import util as streamlit_util



DEFAULT_CHECKPOINT = "riffusion/riffusion-model-v1"
SCHEDULER_OPTIONS = [
    "DPMSolverMultistepScheduler",
    "PNDMScheduler",
    "DDIMScheduler",
    "LMSDiscreteScheduler",
    "EulerDiscreteScheduler",
    "EulerAncestralDiscreteScheduler",
]

def generate_audio(
    prompt: str,
    scheduler: str,  # Replace with appropriate scheduler option
    use_20k: bool,
    guidance: float, # was 7.0
    starting_seed: int,
    width: int = 512, #vas int = 512
    negative_prompt: str = "",
    num_clips: int = 1,
    num_inference_steps: int = 30, #default 30
    extension: str = "mp3",
    device: str = "cpu",
    checkpoint: str = DEFAULT_CHECKPOINT, 
) -> T.List[str]:
    
    if not prompt:
        print("Enter a prompt")
        return

    if use_20k:
        params = SpectrogramParams(
            min_frequency=10,
            max_frequency=20000,
            sample_rate=44100,
            stereo=True,
        )
    else:
        params = SpectrogramParams(
            min_frequency=0,
            max_frequency=10000,
            stereo=False,
        )
    file_paths = []
    seed = starting_seed
    for i in range(1, num_clips + 1):
        print(f"Generating clip {i} / {num_clips} - Seed {seed}")

        image = streamlit_util.run_txt2img(
            prompt=prompt,
            num_inference_steps=num_inference_steps,
            guidance=guidance,
            negative_prompt=negative_prompt,
            seed=seed,
            width=width,
            height=512,
            checkpoint=checkpoint,
            device=device,
            scheduler=scheduler,
        )

        segment = streamlit_util.audio_segment_from_spectrogram_image(
            image=image,
            params=params,
            device=device,
        )


        file_path = streamlit_util.save_audio_to_file(
            segment, name=f"{prompt.replace(' ', '_')}_{seed}", extension=extension
        )
        file_paths.append(file_path)


        seed += 1
        os.system('afplay /System/Library/Sounds/Glass.aiff')
        os.system('afplay /System/Library/Sounds/Glass.aiff')

    return file_paths


