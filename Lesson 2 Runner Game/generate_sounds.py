import math
import struct
import wave
import os

def generate_wav(filename, duration, sample_rate, wave_func):
    """Generate a wave file."""
    print(f"Generating {filename}...")
    num_samples = int(duration * sample_rate)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2) # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            value = wave_func(t, i, num_samples)
            # Clip the value
            value = max(-1.0, min(1.0, value))
            # Convert to 16-bit PCM
            packed_value = struct.pack('h', int(value * 32767.0))
            wav_file.writeframes(packed_value)

# 1. Jump Sound (ascending pitch)
def jump_wave(t, i, num_samples):
    freq = 300 + (t * 800) # Starts at 300Hz, goes up
    # Envelope to fade out
    envelope = 1.0 - (t / 0.3)
    if envelope < 0: envelope = 0
    return math.sin(2.0 * math.pi * freq * t) * envelope * 0.5

# 2. Powerup Sound (arpeggio / quick blips)
def powerup_wave(t, i, num_samples):
    freq = 600 if (int(t * 10) % 2 == 0) else 900
    freq += t * 1000
    envelope = 1.0 - (t / 0.5)
    return math.sin(2.0 * math.pi * freq * t) * envelope * 0.5

# 3. Crash Sound (noise + descending pitch)
def crash_wave(t, i, num_samples):
    # pseudo noise
    noise = (i * 12345 % 100) / 50.0 - 1.0
    freq = 200 - (t * 300)
    if freq < 20: freq = 20
    tone = math.sin(2.0 * math.pi * freq * t)
    envelope = 1.0 - (t / 0.6)
    if envelope < 0: envelope = 0
    return (noise * 0.3 + tone * 0.7) * envelope * 0.6

# 4. Background Music (simple repetitive synth loop)
def music_wave(t, i, num_samples):
    # 120 BPM = 2 beats per second, 0.5s per beat
    beat = t % 0.5
    measure = int(t / 0.5) % 4
    
    # Bassline
    bass_freq = 110 if measure % 2 == 0 else 82.41 # A2 or E2
    bass = math.sin(2.0 * math.pi * bass_freq * t)
    
    # Hi-hat on the off-beat
    hat = 0
    if beat > 0.25 and beat < 0.3:
        hat = (i * 12345 % 100) / 50.0 - 1.0
    
    # Melody
    melody = 0
    if measure == 0 and beat < 0.2:
        melody = math.sin(2.0 * math.pi * 440 * t)
    elif measure == 1 and beat < 0.2:
        melody = math.sin(2.0 * math.pi * 554.37 * t)
        
    return (bass * 0.4 + hat * 0.1 + melody * 0.3) * 0.5

if __name__ == "__main__":
    generate_wav("jump.wav", 0.3, 44100, jump_wave)
    generate_wav("powerup.wav", 0.5, 44100, powerup_wave)
    generate_wav("crash.wav", 0.6, 44100, crash_wave)
    generate_wav("music.wav", 8.0, 44100, music_wave) # 8 second loop
    print("Done generating sounds!")
