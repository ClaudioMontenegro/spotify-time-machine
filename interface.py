from tkinter import *
from data_collect import DataCollect


BACKGROUND = "#232723"
GREEN_TEXT = "#62d089"
WHITE_TEXT = "#e1ece3"
FONT = "Gotham Circular"
FONT_SIZE = 12


class Interface:
    def __init__(self):

        # Window
        self.window = Tk()
        self.window.config(padx=50, pady=50, bg=BACKGROUND)
        self.window.title("Spotify Time Machine")

        # Canvas
        self.logo = PhotoImage(file="images/spotify_logo.png")
        self.canvas = Canvas(width=200, height=200, bg=BACKGROUND, highlightthickness=0)
        self.canvas.create_image(100, 100, image=self.logo)
        self.canvas.grid(row=0, column=1, columnspan=3, pady=20)

        # Labels
        self.year_lb = Label(text="Select a date to travel to: ", font=(FONT, FONT_SIZE, "bold"),
                             bg=BACKGROUND, fg=GREEN_TEXT)
        self.year_lb.grid(row=1, column=1)
        self.name_lb = Label(text="Enter the playlist's name: ", font=(FONT, FONT_SIZE, "bold"),
                             bg=BACKGROUND, fg=GREEN_TEXT)
        self.name_lb.grid(row=2, column=1)

        # Entries
        self.year_ent = Entry(width=20, bg="white", fg="grey", font=(FONT, 10))
        self.year_ent.insert(0, "YYYY-MM-DD")
        self.year_ent.bind('<FocusIn>', self.on_entry_click)
        self.year_ent.bind('<FocusOut>', lambda event: self.on_entry_leave(event))
        self.year_ent.grid(row=1, column=2)
        self.name_pl = Entry(width=20, bg="white", fg="black", font=(FONT, 10))
        self.name_pl.grid(row=2, column=2)

        # Buttons
        self.travel = PhotoImage(file="images/travel-bt.png")
        self.travel_bt = Button(image=self.travel,
                                bg=BACKGROUND,
                                border=0,
                                borderwidth=0,
                                command=self.on_click_travel)
        self.travel_bt.config(activebackground=BACKGROUND)
        self.travel_bt.grid(row=2, column=3, sticky="we", padx=10)

        self.data_collector = DataCollect(self.year_ent, self.name_pl)

        self.window.mainloop()

    def on_entry_click(self, event):
        if self.year_ent.get() == "YYYY-MM-DD":
            self.year_ent.delete(0, END)
            self.year_ent.config(fg='black')  # Change text color to black

    def on_entry_leave(self, event):
        if not self.year_ent.get():
            self.year_ent.insert(0, "YYYY-MM-DD")
            self.year_ent.config(fg='grey')  # Change text color to grey

    def on_click_travel(self):
        self.data_collector.collect_data()
        self.year_ent.delete(0, 'end')
        self.name_pl.delete(0, 'end')
        self.year_ent.bind('<FocusIn>', self.on_entry_click)
        self.year_ent.bind('<FocusOut>', lambda event: self.on_entry_leave(event))
