from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from midiutil import MIDIFile
import math

# -------------------------
# Step 1: Quantum Random Number Generator
# -------------------------
def quantum_random_bit():
    qc = QuantumCircuit(1, 1)
    qc.h(0)                 # put qubit into superposition
    qc.measure(0, 0)

    simulator = Aer.get_backend("aer_simulator")
    qc_compiled = transpile(qc, simulator)   
    result = simulator.run(qc_compiled, shots=1).result()
    counts = result.get_counts()
    return int(list(counts.keys())[0])  # returns 0 or 1

def quantum_random_number(max_value=10):
    """Generate random integer in [0, max_value-1]"""
    num_bits = math.ceil(math.log2(max_value))
    bits = [quantum_random_bit() for _ in range(num_bits)]
    value = int("".join(map(str, bits)), 2)
    return value % max_value

# -------------------------
# Step 2: Map Numbers -> Notes
# -------------------------
# Two octaves of C major (you can extend later to 88 keys)
NOTES = [
    "C4","D4","E4","F4","G4","A4","B4",
    "C5","D5","E5","F5","G5","A5","B5"
]

def generate_melody(length=16):
    melody = []
    for i in range(length):
        note = NOTES[quantum_random_number(len(NOTES))]
        melody.append(note)
        print(f"Note {i+1}: {note}")   #  show each note
    return melody

# -------------------------
# Step 3: Save Melody as MIDI
# -------------------------
NOTE_MAPPING = {
    "C4": 60, "D4": 62, "E4": 64, "F4": 65, "G4": 67, "A4": 69, "B4": 71,
    "C5": 72, "D5": 74, "E5": 76, "F5": 77, "G5": 79, "A5": 81, "B5": 83
}

def save_melody(melody, filename="quantum_melody.mid"):
    midi = MIDIFile(1)  
    track = 0
    time = 0
    midi.addTrackName(track, time, "Quantum Melody")
    midi.addTempo(track, time, 120)  # 120 BPM

    for note in melody:
        pitch = NOTE_MAPPING[note]
        midi.addNote(track, channel=0, pitch=pitch,
                     time=time, duration=1, volume=100)
        time += 1

    with open(filename, "wb") as f:
        midi.writeFile(f)

    print(f"\n MIDI file saved as {filename}")

# -------------------------
# Step 4: Run Everything
# -------------------------
if __name__ == "__main__":
    melody = generate_melody(length=16)   # 16 notes melody
    print("\nFinal Melody:", melody)
    save_melody(melody)
