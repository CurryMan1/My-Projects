from customtkinter import *
from CTkListbox import *
from pygame import *
import os, math, datetime, random

root = CTk()
root.title('Audio Player')
root.iconbitmap('Wineass-Ios7-Redesign-Music.ico')
root.resizable(False, False)
last_song = False
buttons_frame = CTkFrame(root)
timestamp = -1
mycounter = 1
songs = []

mixer.init()
mixer.music.set_volume(0.5)
songs_list = os.listdir('C:/Users/user/PycharmProjects/Music Player/Songs')
for song in songs_list:
    songs.append(song)

def update():
    global mycounter, timestamp, last_song
    mycounter += 1
    if (time_elapsed.cget('text') != audio_len.cget('text') or audio_len.cget('text') == '0:00:00') and pause_play.cget('text') == '⏸️':
        timestamp += 1
        time_elapsed.configure(text=str(datetime.timedelta(seconds=round(timestamp))))
        time_bar.set(timestamp)
    if mixer.music.get_busy() == False:
        if pause_play.cget('text') != '▶️':
            if songs.index(song_box.get())+1 == len(songs):
                last_song = True
                return None
            elif songs.index(song_box.get())+1 != len(songs):
                next_track()
                root.after(1000, lambda: update())
                return None
    root.after(1000, lambda: update())

def change_song(audio):
    global timestamp, last_song
    timestamp = -1
    audio_len.configure(text=str(datetime.timedelta(seconds = round(mixer.Sound(f'C:/Users/user/PycharmProjects/Music Player/Songs/{audio}').get_length()))))
    mixer.music.load(f'C:/Users/user/PycharmProjects/Music Player/Songs/{audio}')
    mixer.music.play()
    pause_play.configure(text='⏸️')
    if pause_play.cget('state') == 'disabled':
        pause_play.configure(state='normal')
        next_song.configure(state='normal')
        prev_song.configure(state='normal')
    time_bar.configure(state='normal', to=round(mixer.Sound(f'C:/Users/user/PycharmProjects/Music Player/Songs/{audio}').get_length()))
    time_bar.set(0)
    if mycounter == 1 or last_song:
        last_song = False
        update()

def play_pause(x = None):
    if pause_play.cget('text') == '▶️':
        mixer.music.unpause()
        pause_play.configure(text='⏸️')
    elif pause_play.cget('text') == '⏸️':
        mixer.music.pause()
        pause_play.configure(text='▶️')
def change_time(time):
    global timestamp
    time_elapsed.configure(text=str(datetime.timedelta(seconds=round(time))))
    timestamp = time
    if mixer.music.get_busy() == False:
        mixer.music.play(start=time)
        update()
    else:
        mixer.music.play(start=time)
    pause_play.configure(text='⏸️')

def next_track(x=0):
    song_box.select(songs.index(song_box.get()) + 1)
    time_elapsed.configure(text='0:00:00')

def prev_track(x=0):
    song_box.select(songs.index(song_box.get()) - 1)
    time_elapsed.configure(text='0:00:00')

def set_vol(vol):
    mixer.music.set_volume(vol)

def show_info(x=0):
    window = CTkToplevel(root)
    window.title('Information')
    CTkLabel(window, text='This audio app was made with CustomTKinter GUI and the\nPygame sound system by Hardhik Vittanala.', font=(None, 30)).grid(pady=10, padx=10)

song_box = CTkListbox(root, width=500, command=change_song)
song_box.grid(row=0, column=0)

for song in songs:
    song_box.insert(songs.index(song), song)

pause_play = CTkButton(buttons_frame, text='⏸️', font=('Callibri', 30), width=50, height=50, command=play_pause, state='disabled')
pause_play.grid(row=0, column=2)
next_song = CTkButton(buttons_frame, text='⏭️', font=('Callibri', 30), width=50, height=50, command=next_track, state='disabled')
next_song.grid(row=0, column=3)
prev_song = CTkButton(buttons_frame, text='⏮️', font=('Callibri', 30), width=50, height=50, command=prev_track, state='disabled')
prev_song.grid(row=0, column=1)

time_bar = CTkSlider(buttons_frame, from_=0, to=0, state='disabled', command=change_time)
time_bar.grid(row=1, column=1, columnspan=3)

time_elapsed = CTkLabel(buttons_frame, text='0:00:00')
time_elapsed.grid(row=1, column=0)

audio_len = CTkLabel(buttons_frame, text='0:00:00')
audio_len.grid(row=1, column=4)

buttons_frame.grid(row=1)

volume = CTkSlider(buttons_frame, from_=0, to=1, command=set_vol, orientation=VERTICAL, height=50)
volume.grid(row=0, column=4)

info = CTkLabel(buttons_frame, text='ⓘ', font=('Callibri', 20), width=30, height=37)
info.grid(row=0, column=0)

info.bind('<Button-1>', show_info)

root.bind('<space>', play_pause)
root.bind('<Left>', prev_track)
root.bind('<Right>', next_track)

root.mainloop()