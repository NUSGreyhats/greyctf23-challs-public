import mingus.core.notes as notes
from mingus.containers import Note, Composition, NoteContainer, Bar, Track
from mingus.midi import midi_file_out
from itertools import product

values = set()

with open('text.txt') as f:
    # Read 1 char at a time and store values
    data = f.read().lower()
    for c in data:
        values.add(c)


# Sort all symbols
values = sorted(list(values))
print(values)

mapping = {}
combi = list(product(list("CDEFGAB"), [ i for i in range(6)])) + list(product(["A#","C#","D#","F#"], [ i for i in range(2)])) + list(product(["Db","Eb","Gb","Ab","Bb"], [ i for i in range(2)]))
for i,v  in enumerate(values):
    n,c = combi[i]
    mapping[v] = Note(n, c)


# Read file mapping as notes
track = Track()


for c in data:
    track.add_notes(mapping[c], 1)


# Save as a midi file
midi_file_out.write_Track("result.mid", track)





