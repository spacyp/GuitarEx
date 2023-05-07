import guitarpro
import random


def create_gp_sample(gen):
    song = guitarpro.Song()
    track = song.tracks[0]
    track.name = 'Exercise Track'
    track.channel.instrument = 29  # overdrive guitar
    track.useRSE = True

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
                note_data = next(gen)
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




def generate_chromatic_four_note_shape():
    fret_shape = random.sample([1, 2, 3, 4], 4)
    print(f"using {fret_shape}")
    for string in range(6, 0, -1):
        for fret in fret_shape:
            yield {"string": string, "fret": fret, "duration": 16}
    for string in range(1, 7):
        for fret in reversed(fret_shape):
            yield {"string": string, "fret": fret, "duration": 16}

FRET_OFFSET = [24, 19, 15, 10, 5, 0]
MAX_FRET = 24

#default parameters generate d minor pentatonic
def get_frets_for_scale(scale = [3, 2, 2, 3, 2], effective_start_pos=10):
    frets = []
    for string in range(6):
        # get a start value value from -12..-1
        start_pos = ((effective_start_pos - FRET_OFFSET[string]) % 12) - 12
        fret_number_for_scale = start_pos
        scale_idx = 0
        frets_for_string = set()
        while fret_number_for_scale <= MAX_FRET:
            if fret_number_for_scale >= 0:
                frets_for_string.add(fret_number_for_scale)
            fret_number_for_scale += scale[scale_idx % len(scale)]
            scale_idx += 1
        frets.append(frets_for_string)

    return frets


def generate_scale_exercise(start_fret=5, start_string=5, max_fret_down_on_string_change=1):
    relevant_notes = get_frets_for_scale()
    last_note = start_fret-1
    for string in range(start_string, 0, -1):
        for position in [0, 1]:
            note_found = False
            while not note_found:
                last_note += 1
                if last_note in relevant_notes[string-1]:
                    note_found = True
            if position == 0:
                start_fret = last_note
            yield {"string": string, "fret": last_note, "duration": 16}

        # low and high position done, go to next string and reset to low position
        last_note = start_fret-1-max_fret_down_on_string_change


def generate_groups(group_size=3, gen=generate_scale_exercise()):
    all_notes = list(gen)
    next_note_idx = 0
    note_count = 0
    while next_note_idx < len(all_notes):

        # 0 1 2  1 2 3  2 3 4
        # for i in range(group_size):

        yield all_notes[next_note_idx]
        next_note_idx += 1
        note_count += 1
        if note_count % group_size == 0:
            next_note_idx -= group_size-1





if __name__ == '__main__':
    gen_chromatic = generate_chromatic_four_note_shape()
    gen_scale = generate_scale_exercise()
    gen_group = generate_groups()
    create_gp_sample(gen_group)
