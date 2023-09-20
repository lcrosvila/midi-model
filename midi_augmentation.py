import os
import random
import argparse
import pretty_midi
from copy import deepcopy

# Function to transpose notes in a MIDI file
def transpose_midi(midi, transpose_semitones):
    for instrument in midi.instruments:
        for note in instrument.notes:
            note.pitch += transpose_semitones

# Function to change tempo in a MIDI file
def change_tempo(midi, tempo_factor):
    for instrument in midi.instruments:
        for note in instrument.notes:
            note.start *= tempo_factor
            note.end *= tempo_factor

# Function to vary velocity in a MIDI file
def vary_velocity(midi, velocity_range):
    for instrument in midi.instruments:
        for note in instrument.notes:
            note.velocity = min(127, max(0, note.velocity + random.randint(-velocity_range, velocity_range)))

augmentations = {
    "transpose": transpose_midi,
    "tempo": change_tempo,
    "velocity": vary_velocity
}

# Function to apply data augmentation techniques to a MIDI file multiple times
def augment_midi_multiple_times(input_file, output_dir, num_augmentations):
    midi = pretty_midi.PrettyMIDI(input_file)
    filename = os.path.basename(input_file)
    base_name, ext = os.path.splitext(filename)

    for ii in range(num_augmentations):
        # Apply data augmentation techniques
        transpose_semitones = random.randint(-2, 2)
        tempo_factor = random.uniform(0.8, 1.2)
        velocity_range = random.randint(0, 10)

        for k, v in augmentations.items():
            augmented_midi = deepcopy(midi)  # Create a copy of the original MIDI
            augmentation_suffix = f"{k}_{ii}"
            output_file = os.path.join(output_dir, f"{base_name}_{augmentation_suffix}{ext}")
            
            v(augmented_midi, transpose_semitones) if k == "transpose" else None
            v(augmented_midi, tempo_factor) if k == "tempo" else None
            v(augmented_midi, velocity_range) if k == "velocity" else None

            augmented_midi.write(output_file)

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
