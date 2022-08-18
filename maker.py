import enum
from random import random
from mido import MidiFile
from midiutil import MIDIFile
from mido import Message, MidiFile, MidiTrack

class note:
    n = -1
    length = 0
    time=0
    channel = 0
    vel = 64
    def __init__(self, n, length, time,channel,vel=64):
        self.n = n
        self.length= length
        self.time = time
        self.channel = channel
        self.vel = vel
    def __str__(self):
        return f"note {self.n} length {self.length} time {self.time} channel {self.channel}"
class song:
    notes = []
    ticks_per_beat = 0
    def from_midi_track(self, track,ticks_per_beat):
        self.notes = []
        self.ticks_per_beat = ticks_per_beat
        time = 0
        for i,mid in enumerate(track):
            if "time" in dir(mid):
                time += mid.time

            if mid.type == "note_on":
                length = 0
                found = False
                for off in track[i+1:]:
                    if "time" in dir(off):
                        length += off.time
                    if off.type == "note_off" or (off.type == "note_on" and off.velocity == 0):
                    
                        if off.note == mid.note:
                            found = True
                            break
                if not found or length <= 0:
                    print("ERROR")
                                      
                self.notes.append(note(mid.note, length, time,mid.channel,mid.velocity))
           
    def create_random(self):
        length = int(random()*10000)
        time = 0
        for _ in range(length):

            self.notes.append(note(
                int(random() * 50) + 50,
                int(random() * 200)+1,
                time,
                int(random() * 3),
                int(random() * 100)
            ))
            time += int(random() * 100)+1
    def to_midi_track(self):
        tracked_notes = {}
        track = []
        prev_time = 0
        for n in self.notes:
            ks = []
            for k,v in tracked_notes.items():
                if k<n.time and k > prev_time:
                    deltatime = (v.time+v.length) - prev_time
                    prev_time = v.time+v.length
                    track.append(Message('note_off', note=v.n, velocity=0, time=deltatime))
                    ks.append(k)
                    if deltatime<0:
                        return [],False
            for k in ks:
                del tracked_notes[k]
            deltatime = n.time - prev_time
      
            track.append(Message('note_on', note=n.n, velocity=n.vel, time=deltatime))
            tracked_notes[n.time + n.length] = tracked_notes.get(n.time + n.length,n)
            tracked_notes = dict(sorted(tracked_notes.items()))
            prev_time = n.time
       
        return track,True

mid = MidiFile('queen.mid')
sng = song()


mid2 = MidiFile()
mid2.ticks_per_beat = mid.ticks_per_beat

for i,t in enumerate(mid.tracks):
    
    sng.from_midi_track(t, mid.ticks_per_beat)
    new_track , failed = sng.to_midi_track()
    mid2.tracks.append(new_track)
    a = 0
    b = 0
    
        
print(len(mid2.tracks))
mid2.save("wii2.mid")


'''

for j,n in enumerate(t):
        if n.type == "note_on" or n.type == "note_off":
            if a >= len(new_track):
                print(n)
                continue
            if n.type == "note_on":
                print(n,"|", new_track[a],"|", sng.notes[b])
                b+=1
            elif n.type == "note_off":
                print(n,"|", new_track[a])
            if not (n.note == new_track[a].note):
                pass#input()
            else:
                a+=1
    print("endtrack")
mid = MidiFile('major-scale.mid')
for i,track in enumerate(mid.tracks):
    print("Track", i)
    for m in track:
        print(m)
degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 60   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(degrees):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
'''