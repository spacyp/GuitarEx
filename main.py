import guitarpro
import random


def create_gp_sample():
    song = guitarpro.Song()
    track = song.tracks[0]
    track.name = 'Exercise Track'
    track.channel.instrument = 29  # overdrive guitar
    track.useRSE = True

    note_generator = generate_notes()

    #remove default measure
    song.measureHeaders = []
    track.measures = []

    finished = False
    while not finished:
        song.newMeasure()
        measure = track.measures[-1]
        voice = measure.voices[0]
        measure_is_full = False
        fullness = 0.0
        while not measure_is_full:
            try:
                note_data = next(note_generator)
            except StopIteration:
                finished = True
                break
            beat = guitarpro.Beat(voice, duration=guitarpro.Duration(value=note_data.get("duration")))
            note = guitarpro.Note(beat, value=note_data.get("fret"), string=note_data.get("string"))
            beat.notes.append(note)
            voice.beats.append(beat)
            fullness += 1/note_data.get("duration")
            if fullness >= 0.99:
                measure_is_full = True

    guitarpro.write(song, "output/test.gp5")


def generate_randomized_shape():
    return random.sample([1, 2, 3, 4], 4)


def generate_notes():
    fret_shape = generate_randomized_shape()
    print(f"using {fret_shape}")
    for string in range(6, 0, -1):
        for fret in fret_shape:
            yield {"string": string, "fret": fret, "duration": 16}
    for string in range(1, 7):
        for fret in reversed(fret_shape):
            yield {"string": string, "fret": fret, "duration": 16}


if __name__ == '__main__':
    create_gp_sample()
