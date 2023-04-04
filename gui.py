import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
from statemachine import StateMachine

statemachine = StateMachine()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.countMsg = 0
        self.logs = []
        # root window
        self.height = "500"
        self.width = "900"
        self.hHeader = str(int(int(self.height)*0.15))
        self.hInfo = str(int(int(self.height)*0.1))
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
        btn = ttk.Button(frame, text='Upload File', command= lambda : self.open_file())
        btn.place(x=750, y=20)

        self.info = tk.Frame(self, width=self.width, height=self.hInfo)
        self.info.grid(row=1, column=0)
        labTextCurState = ttk.Label(self.info, text='Estado atual: ', font=("arial", 12), foreground="#000")
        labTextCurState.place(x=10, y=10)
        self.labCurState = ttk.Label(self.info, text='q0', font=("arial", 12, 'bold'), foreground="#5F8D4E")
        self.labCurState.place(x=110, y=10)

        self.successfull = ttk.Label(self.info, text='Movimento permitido', font=("arial", 12, 'bold'), foreground="#5F8D4E")
        self.successfull.place(x=680, y=10)

        
        self.body = tk.Frame(self, width=self.width, height=str(int(self.height) - int(self.hHeader) - int(self.hInfo)))
        self.body.grid(row=2, column=0)
        
        
        self.bind('<Return>', self.readMsg)

        scroll_bar = tk.Scrollbar(self.body)
  
        scroll_bar.pack( side = tk.RIGHT,
                        fill = tk.Y )
        
        self.listbox = tk.Listbox(self.body, 
                        yscrollcommand = scroll_bar.set, width='100', height='19')
    
        
        self.listbox.pack( side = tk.LEFT, fill = tk.BOTH )
        
        scroll_bar.config( command = self.listbox.yview )

    def readMsg(self, event):
        log = statemachine.execute(self.word.get())

        if log['cur_state'] != 'q0':
            self.successfull.place_forget()
        else:
            self.successfull.place(x=680, y=10)

        self.displayInfo(log)
        self.word.delete(0,tk.END)

    def open_file(self):
        file_path = askopenfile(mode='r', filetypes=[('Text Files', '*txt')])
        if file_path is not None:
            statemachine.reset()
            self.listbox.delete(0,tk.END)
            for row in file_path:
                log = statemachine.execute(row.replace('\n', ''))
                self.displayInfo(log)
            
            if log['cur_state'] != 'q0':
                self.listbox.insert(tk.END, '[###] Estado atual não é final')
                self.listbox.itemconfig(self.countMsg, foreground='red')
    
    def displayInfo(self, log):
        text = f"[{log['old_state']} -> {log['dest_state']}] {log['text']}"
        color = "#000" if log['error'] == 0 else "#DF2E38"
        self.listbox.insert(tk.END, text)
        self.listbox.itemconfig(self.countMsg, foreground=color)
        self.countMsg += 1
        self.labCurState.config(text = log['cur_state'])
        self.word.config(text = '')