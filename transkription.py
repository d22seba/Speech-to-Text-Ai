import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import sounddevice as sd
import numpy as np
import webrtcvad
from aiprompt import *
from tts import *

model_name = "openai/whisper-small"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)

vad = webrtcvad.Vad(2) 

def frame_generator(frame_duration_ms, audio, sample_rate):
    n = int(sample_rate * frame_duration_ms / 1000)  
    offset = 0
    while offset + n <= len(audio):
        yield audio[offset:offset + n]
        offset += n

def is_speech(audio_chunk, sample_rate=16000):
    pcm_data = (audio_chunk * 32768).astype(np.int16).tobytes()
    return vad.is_speech(pcm_data, sample_rate)

def wait_for_speech(fs=16000):
    print("🎙️ Warte auf Sprache...")
    while True:
        audio = sd.rec(int(0.5 * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()
        audio = audio.squeeze()
        frames = list(frame_generator(20, audio, fs))
        if any(is_speech(frame, sample_rate=fs) for frame in frames):
            print("🎤 Sprache erkannt! Aufnahme beginnt...")
            break

def record_audio(duration=5, fs=16000):
    print(f"🎙️ Aufnahme für {duration} Sekunden...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    return audio.squeeze()

def transcribe_audio(audio_data, fs=16000):
    inputs = processor(audio_data, sampling_rate=fs, return_tensors="pt")
    forced_ids = processor.get_decoder_prompt_ids(language="german", task="transcribe")
    generated_ids = model.generate(inputs.input_features, forced_decoder_ids=forced_ids)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return text

if __name__ == "__main__":
    # wait_for_speech()
    # audio = record_audio(duration=5)
    # print("🧠 Transkribiere...")
    # text = transcribe_audio(audio)
    text = "sag mir wie es dir heute so geht"
    print("text:",text)
    output = ollama_run(text)
    print(output)
