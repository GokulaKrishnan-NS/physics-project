from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from midiutil import MIDIFile
import math

# ---------------------------
# Notes (C major scale, 2 octaves)
NOTES = {
    "C4": 60, "D4": 62, "E4": 64, "F4": 65, "G4": 67, "A4": 69, "B4": 71,
    "C5": 72, "D5": 74, "E5": 76, "F5": 77, "G5": 79, "A5": 81, "B5": 83
}

# Note durations (beats)
DURATIONS = [0.25, 0.5, 1, 2]  # sixteenth, eighth, quarter, half

# Instruments (General MIDI numbers)
INSTRUMENTS = {
    "Piano": 0,
    "Violin": 40,
    "Flute": 73,
    "Guitar": 24,
    "Trumpet": 56
}

# ---------------------------
# Quantum random number generator
def quantum_random_bit():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    job = simulator.run(compiled, shots=1)
    result = job.result()
    counts = result.get_counts()
    return int(list(counts.keys())[0])

def quantum_random_number(n):
    num_bits = math.ceil(math.log2(n))
    bits = [str(quantum_random_bit()) for _ in range(num_bits)]
    return int("".join(bits), 2) % n

# ---------------------------
# Generate base melody (used for all instruments)
def generate_base_melody(length=16):
    melody = []
    note_names = list(NOTES.keys())
    for _ in range(length):
        note = note_names[quantum_random_number(len(note_names))]
        duration = DURATIONS[quantum_random_number(len(DURATIONS))]
        melody.append((note, duration))
    return melody

# ---------------------------
# Multi-instrument MIDI generator (harmonized)
def create_midi(filename="quantum_harmony.mid", instruments=["Piano", "Violin", "Flute"], tempo=120, length=16):
    mf = MIDIFile(len(instruments))  # multiple tracks
    base_melody = generate_base_melody(length)
    note_list = list(NOTES.values())

    print("\n Generating Harmonized Quantum Music ")
    print("Base Melody:")
    for idx, (note, dur) in enumerate(base_melody, start=1):
        print(f"Note {idx}: {note}, Duration: {dur} beats")

    for i, instr in enumerate(instruments):
        channel = i
        mf.addTempo(i, 0, tempo)
        mf.addProgramChange(i, channel, INSTRUMENTS[instr], 0)

        print(f"\nInstrument: {instr}")
        time = 0
        for j, (base_note, dur) in enumerate(base_melody):
            # Create harmony: offset each instrument’s pitch by 0–4 semitones
            base_pitch = NOTES[base_note]
            harmony_offset = (i * 2) % 5  # small shift to create chord-like sound
            pitch = note_list[(note_list.index(base_pitch) + harmony_offset) % len(note_list)]

            print(f"  Playing: {base_note} (+{harmony_offset} semitones) for {dur} beats")
            mf.addNote(i, channel, pitch, time, dur, 100)
            time += dur

    with open(filename, "wb") as f:
        mf.writeFile(f)

    print(f"\n MIDI file saved as '{filename}' ({tempo} BPM)")

# ---------------------------
# Example usage
if __name__ == "__main__":
    create_midi(
        filename="quantum_harmony.mid",
        instruments=["Piano", "Flute", "Violin"],
        tempo=100,
        length=12
    )
