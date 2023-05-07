import guitarpro


def parse_gp_sample():
    song = guitarpro.parse("input/sample.gp5")
    song


def create_gp_sample():
    song = guitarpro.Song()
    track = song.tracks[0]
    track.name = 'My first track'
    track.channel.instrument = 29  # overdrive guitar
    voice = song.tracks[0].measures[0].voices[0]
    track.useRSE = True
    for i in range(16):
        beat = guitarpro.Beat(voice)
        beat.duration = guitarpro.Duration(value=guitarpro.Duration.sixteenth)
        note = guitarpro.Note(beat)
        note.value = i % 4 + 1
        note.string = 6 - i // 4
        beat.notes.append(note)
        voice.beats.append(beat)
    guitarpro.write(song, "output/test.gp5")

if __name__ == '__main__':
    create_gp_sample()
    parse_gp_sample()

