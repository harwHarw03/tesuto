import requests
import argparse
import json
import os
import subprocess

def read_text(input_text):
    if os.path.isfile(input_text):
        with open(input_text, 'r', encoding='utf-8') as f:
            return f.read()
    return input_text

def synthesize(text_input, speaker, output_file, play_audio):
    text = read_text(text_input)

    query_url = f"http://localhost:50021/audio_query"
    params = {"text": text, "speaker": speaker}
    print("[*] Sending audio query...")
    response = requests.post(query_url, params=params)
    if response.status_code != 200:
        print("[-] Failed to get audio query")
        print(response.text)
        return

    query_data = response.json()

    synth_url = f"http://localhost:50021/synthesis?speaker={speaker}"
    headers = {"Content-Type": "application/json"}
    print("[*] Synthesizing audio...")
    response = requests.post(synth_url, headers=headers, data=json.dumps(query_data))
    if response.status_code != 200:
        print("[-] Failed to synthesize audio")
        print(response.text)
        return

    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"[+] Audio saved to {output_file}")

    if play_audio:
        print(f"[*] Playing audio with aplay...")
        subprocess.run(["aplay", output_file])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text-to-speech using VoiceVox API")
    parser.add_argument("text_input", type=str, help="Text to synthesize or path to a text file")
    parser.add_argument("--speaker", type=int, default=7, help="Speaker ID (default: 7)")
    parser.add_argument("--output", type=str, default="audio.wav", help="Output WAV file (default: audio.wav)")
    parser.add_argument("--play", action="store_true", help="Play the audio after generation using aplay")
    args = parser.parse_args()

    synthesize(args.text_input, args.speaker, args.output, args.play)
