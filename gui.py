import tkinter as tk
from tkinter import ttk
from statemachine import StateMachine

statemachine = StateMachine()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.column = 20
        self.logs = []
        # root window
        self.height = "500"
        self.width = "900"
        self.hHeader = str(int(int(self.height)*0.15))
        self.scroll = None

        self.title('Sistema Bancário - Linguagens Formais')
        self.geometry(f'{self.width}x{self.height}')
        self.maxsize(self.width, self.height)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.bg_color = "#191825"

        frame = tk.Frame(self, bg=self.bg_color, width=self.width, height=self.hHeader)
        frame.grid(row=0, column=0)
        label = ttk.Label(frame, text='Sistema Bancário', background=self.bg_color, font=("arial", 25, 'bold'), foreground="#FFF")
        label.place(x=10, y=15)
        self.word = ttk.Entry(frame)
        self.word.place(x=550, y=25)
        btn = ttk.Button(frame, text='Show')
        btn.place(x=750, y=20)


        self.body = tk.Frame(self, width=self.width, height=str(int(self.height) - int(self.hHeader)))
        self.body.grid(row=1, column=0)
        labTextCurState = ttk.Label(self.body, text='Estado atual: ', font=("arial", 12), foreground="#000")
        labTextCurState.place(x=10, y=10)
        labCurState = ttk.Label(self.body, text='q0', font=("arial", 12, 'bold'), foreground="#5F8D4E")
        labCurState.place(x=110, y=10)
        
        self.bind('<Return>', self.readMsg)
        self.scroll = tk.Scrollbar(self.body, orient='vertical')
        self.scroll.place(relx=1, rely=0, relheight=1, anchor='ne')
        # self.body.configure(yscrollcommand=self.scroll.set)

    def readMsg(self, event):
        log = statemachine.execute(self.word.get())
        self.column += 20
        # if self.column > 400 and self.scroll is None:
        self.logs.append(ttk.Label(self.body, text=log, font=("arial", 12), foreground="#000"))
        self.logs[len(self.logs) - 1].place(x=10, y=self.column)
