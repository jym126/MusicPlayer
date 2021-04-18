from tkinter import *
from pygame import mixer
from tkinter import filedialog
import threading

counter = 0
counterImg = 0


class MusicPlayer:

    def __init__(self, window):
        global frame
        window.title('JL Player. By Thunder')
        window.iconbitmap("auricular.ico")
        window.geometry()
        window.config(bg="blue")

        self.capa0 = Frame(window)
        self.capa0.pack(expand="1")
        self.capa0.config(bg="#c0c0c0")

        capa1 = LabelFrame(self.capa0, bg="blue")
        capa1.grid(row=1, columnspan=7)
        capa1.config(bg="#ffffff")

        # imagen de los botones
        self.openimage = PhotoImage(file="D:/Proyectos/Python/MusicPlayer/imagenes/open4.png")
        self.playimage = PhotoImage(file="D:/Proyectos/Python/MusicPlayer/imagenes/play4.png")
        self.stopimage = PhotoImage(file="D:/Proyectos/Python/MusicPlayer/imagenes/stop4.png")
        self.pauseimage = PhotoImage(file="D:/Proyectos/Python/MusicPlayer/imagenes/pause4.png")
        self.nextimage = PhotoImage(file="D:/Proyectos/Python/MusicPlayer/imagenes/forw4.png")
        self.backimage = PhotoImage(file="D:/Proyectos/Python/MusicPlayer/imagenes/rew4.png")

        # Botones de control
        self.Load = Button(capa1, text='Load', bd=1, image=self.openimage, font=('Times', 10),
                           command=lambda: self.add_many_songs())
        self.Load.grid(row=0, column=0)
        self.Play = Button(capa1, text='Play', bd=1, image=self.playimage, font=('Times', 10), command=self.play)
        self.Play.grid(row=0, column=1)
        self.Pause = Button(capa1, text='Pause', bd=1, image=self.pauseimage, font=('Times', 10), command=self.pause)
        self.Pause.grid(row=0, column=2)
        self.Stop = Button(capa1, text='Stop', bd=1, image=self.stopimage, font=('Times', 10), command=self.stop)
        self.Stop.grid(row=1, column=1)
        self.Next = Button(capa1, text='Next', bd=1, image=self.nextimage, font=('Times', 10), command=self.next)
        self.Next.grid(row=1, column=0)
        self.Back = Button(capa1, text='Back', bd=1, image=self.backimage, font=('Times', 10), command=self.back)
        self.Back.grid(row=1, column=2)

        capa2 = LabelFrame(self.capa0)
        capa2.grid(row=1, column=7)
        capa2.config()
        self.Vol = Scale(capa2, from_=1, to=0, resolution=.1, length=100, relief="raised", label="Vol",
                         command=self.volume)
        self.Vol.grid(row=0, column=2)

        # Barra de estado
        self.status_bar = Label(self.capa0, text="", bg="black", fg="white", bd=1, relief=GROOVE, anchor=E)
        self.status_bar.grid(row=2, column=8)

        # Pantalla playlist
        self.song_box = Listbox(self.capa0, width=30, height=7)
        self.song_box.grid(row=1, column=8)
        self.song_box.config(bg="black", fg="green", selectbackground="gray")

        # Menu superior
        my_menu = Menu(root)
        root.config(menu=my_menu)

        # add song menu
        add_song_menu = Menu(my_menu)
        my_menu.add_cascade(label="Añadir Canciones", menu=add_song_menu)
        add_song_menu.add_command(label="Una cancion a la Playlist", command=lambda: self.add_song())

        # add many songs to menu
        add_song_menu.add_command(label="Varias canciones a la Playlist", command=lambda: self.add_many_songs())

        # Eliminar cancion
        remove_song_menu = Menu(my_menu)
        my_menu.add_cascade(label="Eliminar canciones", menu=remove_song_menu)
        remove_song_menu.add_command(label="Elimina la canción seleccionada", command=self.delete_song)
        remove_song_menu.add_command(label="Elimina toda la lista", command=self.delete_all_songs)

        self.music_file = False
        self.playing_state = False

    def equalizer(self):
        self.equa = ""


        self.pantalla = Label(self.capa0, image=self.equa, height=100)
        self.pantalla.grid(row=0, columnspan=12)

        a = "D:/Proyectos/Python/MusicPlayer/imagenes/gif/a.gif"
        b = "D:/Proyectos/Python/MusicPlayer/imagenes/gif/b.gif"
        c = "D:/Proyectos/Python/MusicPlayer/imagenes/gif/c.gif"
        d = "D:/Proyectos/Python/MusicPlayer/imagenes/gif/d.gif"

        self.frame = (0, a, b, c, d, a, c, d, a, d, b)

        def count():
            global counterImg
            counterImg += 1
            self.equa = PhotoImage(file=self.frame[counterImg])
            self.pantalla.config(image=self.equa)
            self.pantalla.after(80, count)
            if counterImg > 9:
                counterImg = 0


        count()

    def add_song(self):

        self.song = filedialog.askopenfilename(initialdir="D:/Proyectos/Python/MusicPlayer/musica",
                                               title="Elige una canción",
                                               filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav"),))
        self.songString = "D:/Proyectos/Python/MusicPlayer/musica/"
        self.song = self.song.replace(self.songString, "")
        self.song_box.insert(END, self.song)

    def add_many_songs(self):
        self.songs = filedialog.askopenfilenames(initialdir="D:/Proyectos/Python/MusicPlayer/musica",
                                                 title="Elige una canción",
                                                 filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav"),))
        self.songString = "D:/Proyectos/Python/MusicPlayer/musica/"
        for song in self.songs:
            song = song.replace(self.songString, "")
            self.song_box.insert(END, song)

    def load(self):
        self.music_file = filedialog.askopenfilename()

    def play(self):
        global counter, counterImg
        mixer.init()
        song = self.song_box.get(ACTIVE)
        self.songString = "D:/Proyectos/Python/MusicPlayer/musica/"
        mixer.music.load(self.songString + song)
        # mixer.music.load(self.music_file)
        mixer.music.play(loops=0)
        # ver el temporizador
        counter = counterImg = 0
        self.play_time(self.status_bar)
        self.equalizer()

    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state = True
        else:
            mixer.music.unpause()
            self.playing_state = False

    def volume(self, x):
        mixer.music.set_volume(self.Vol.get())

    def next(self):
        global counter
        next_one = self.song_box.curselection()
        next_one = next_one[0] + 1
        song = self.song_box.get(next_one)
        song = song.replace(self.songString, "")
        mixer.music.load(self.songString + song)
        mixer.music.play(loops=0)

        self.song_box.select_clear(0, END)
        self.song_box.activate(next_one)
        self.song_box.select_set(next_one, last=None)

        counter = 0

    def back(self):
        global counter
        next_one = self.song_box.curselection()
        next_one = next_one[0] - 1
        song = self.song_box.get(next_one)
        song = song.replace(self.songString, "")
        mixer.music.load(self.songString + song)
        mixer.music.play(loops=0)

        self.song_box.select_clear(0, END)
        self.song_box.activate(next_one)
        self.song_box.select_set(next_one, last=None)

        counter = 0

    def stop(self):
        global counter, counterImg
        global frames
        mixer.music.stop()
        self.status_bar.config(text="")
        counter = threading.Lock
        counterImg = threading.Lock

    def delete_song(self):
        self.song_box.delete(ANCHOR)
        mixer.music.stop()

    def delete_all_songs(self):
        self.song_box.delete(0, END)
        mixer.music.stop()

    # Estado y tiempo
    def play_time(self, label):
        def count():
            global counter
            counter += 1
            label.config(text="Time lapse: " + str(counter))
            label.after(1000, count)

        count()


root = Tk()
app = MusicPlayer(root)

root.mainloop()
