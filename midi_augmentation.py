import os
import random
import mido
import argparse

# Function to transpose notes in a MIDI file
def transpose_midi(midi_file, output_file, transpose_semitones):
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on':
                msg.note += transpose_semitones
    midi_file.save(output_file)

# Function to change tempo in a MIDI file
def change_tempo(midi_file, output_file, tempo_factor):
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                msg.tempo = int(msg.tempo * tempo_factor)
    midi_file.save(output_file)

# Function to vary velocity in a MIDI file
def vary_velocity(midi_file, output_file, velocity_range):
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on':
                msg.velocity = min(127, max(0, msg.velocity + random.randint(-velocity_range, velocity_range)))
    midi_file.save(output_file)

# Function to apply data augmentation techniques to a MIDI file multiple times
def augment_midi_multiple_times(input_file, output_dir, num_augmentations):
    midi_file = mido.MidiFile(input_file)
    filename = os.path.basename(input_file)
    base_name, ext = os.path.splitext(filename)

    for i in range(num_augmentations):
        augmentation_suffix = f"augmentation_{i}"
        output_file = os.path.join(output_dir, f"{base_name}_{augmentation_suffix}{ext}")

        # Apply data augmentation techniques
        transpose_semitones = random.randint(-5, 5)
        tempo_factor = random.uniform(0.8, 1.2)
        velocity_range = random.randint(0, 10)

        transpose_midi(midi_file, output_file, transpose_semitones)
        change_tempo(midi_file, output_file, tempo_factor)
        vary_velocity(midi_file, output_file, velocity_range)

# Function to process a directory of MIDI files
def process_directory(input_dir, output_dir, num_augmentations):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".midi") or filename.endswith(".mid"):
            input_file = os.path.join(input_dir, filename)
            augment_midi_multiple_times(input_file, output_dir, num_augmentations)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MIDI Data Augmentation")
    parser.add_argument("--input_dir", required=True, help="Input directory containing MIDI files")
    parser.add_argument("--output_dir", required=True, help="Output directory to save augmented MIDI files")
    parser.add_argument("--num_augmentations", type=int, default=5, help="Number of augmentations per MIDI file")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    num_augmentations = args.num_augmentations

    process_directory(input_dir, output_dir, num_augmentations)
