import time
import tkinter as tk
import pyglet, os
from tkinter import W, OptionMenu, ttk, messagebox
from puzzle_generator import Puzzle_Generator

pyglet.font.add_file('./assets/Lato-Black.ttf')
pyglet.font.add_file('./assets/Lato-Regular.ttf')

def validate_entry(entry, index, what, widget_dict, widget):
    print(f'Validating: {entry} {index} {what} {widget}')
    '''
    if what == '0':
        print('Deletion')
        print(type(dict(widget_dict)))
        widget_dict[widget].configure(fg='#CDC7BE')
    '''
    try:
        int(entry)
        str(entry)
        if int(index) >= 1:
            return False
        else:
            return True
    except ValueError:
        return False

class sudokuApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('300x420')
        self.title('SUDOKU')
        self.iconbitmap('./assets/sudoku_icon.ico')
        self.resizable(False, False)
        self.columnconfigure(0, weight =1)
        self.rowconfigure(1, weight=1)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Main.TButton", font=('Lato-Regular', 12), background='#6C4A4A', foreground='#D0CAB2')
        style.configure("Main.TLabel", font=('Lato-Black', 12), background='#FDF6EC', foreground='#6C4A4A')
        style.configure("Sudoku.TLabel", font=('Lato-Black', 12), background='#6C4A4A', foreground='#FDF6EC', width='100', height='100')
        style.map('TButton', background=[('active','#FDF6EC')])

        self.title = tk.Label(self, font=('Lato-Black',16), text='SUDOKU', bg='#D0CAB2', fg='#FDF6EC', pady=4)
        self.container = tk.Frame(self, bg='#FDF6EC')

        self.is_a_num = self.register(validate_entry)

        self.title.grid(sticky=tk.W + tk.E)
        self.container.grid(sticky=tk.N + tk.W + tk.E + tk.S)
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        self.frames = {}
        self.start()
    
    def start(self, resume=None):
        start_frame = tk.Frame(self.container, pady=80, bg='#FDF6EC')
        start_frame.columnconfigure(0, weight=1)
        start_frame.pack(fill='both', expand=True)
        self.frames['start'] = start_frame

        label = ttk.Label(start_frame, text='Difficulty:', style='Main.TLabel')
        label.grid(pady=10)

        difficulty = tk.StringVar()
        difficulty.set('Medium')
        dropdown = tk.OptionMenu(start_frame, difficulty, 'Easy', 'Medium', 'Hard')
        dropdown.config(font=('Lato-Black', 10), bg='#FDF6EC', fg='#6C4A4A', border=0, highlightbackground='#FDF6EC', activebackground='#D0CAB2', activeforeground='#6C4A4A', )
        dropdown.grid(row=1)

        if resume:
            resume_btn = ttk.Button(start_frame, style='Main.TButton', text='Resume', command= self.resume)
            resume_btn.grid(row=2, pady=15)

            new_game_btn = ttk.Button(start_frame, style='Main.TButton', text='New Game', command= lambda: self.game(difficulty, start_frame, game_running=True))
            new_game_btn.grid(row=3, pady=15, padx=35)
        else:
            new_game_btn = ttk.Button(start_frame, style='Main.TButton', text='New Game', command= lambda: self.game(difficulty, start_frame))
            new_game_btn.grid(row=3, pady=30, padx=35, ipadx=10, ipady=10)
        
        quit_btn = ttk.Button(start_frame, style='Main.TButton', text='Quit', command= self.destroy)
        quit_btn.grid(row=4, pady=15)

    def game(self, difficulty, frame, game_running=False):
        if game_running:
            sure = messagebox.askokcancel('There is a game already running!', 'Are you sure you want to star a new game? \n Your previous game will be lost.')
            if sure:
                pass
            else:
                return None
        puz = Puzzle_Generator(str(difficulty.get()).lower())
        frame.pack_forget()

        game_frame = tk.Frame(self.container, bg= '#FDF6EC')
        game_frame.columnconfigure(0, weight=1)
        self.frames['game'] = game_frame

        sudoku_grid = tk.Canvas(game_frame, bg='#FDF6EC', bd=0, highlightcolor='#FDF6EC', )

        puzzle_dict = self.print_puzzle(sudoku_grid, puz)
        h= sudoku_grid.winfo_reqheight()
        w= sudoku_grid.winfo_reqwidth()
        print(f'Canvas width: {w} height: {h}')
        for i in range (0, w, 84):
            sudoku_grid.create_line([(i, 0), (i, w)], tag='grid_line', fill='#6C4A4A', width=2)
        for i in range (0, h, 87):
            sudoku_grid.create_line([(0, i), (h, i)], tag='grid_line', fill='#6C4A4A', width=2)
        game_frame.pack(fill='both', expand=True)
        sudoku_grid.grid(row=0, column=0, columnspan=2, pady=24)

        buttons_label = tk.Label(game_frame, bg='#FDF6EC')
        buttons_label.grid(row=1, column=0, ipady=0, ipadx=0)

        exit_btn = ttk.Button(buttons_label, style='Main.TButton', text='Exit', command= lambda: self.back_to_start(game_frame))
        exit_btn.grid(row=0, column=0, pady =5, padx=15)

        check_btn = ttk.Button(buttons_label, style='Main.TButton', text='Check Puzzle', command= lambda: self.check_puzzle(puzzle_dict, puz))
        check_btn.grid(row=0, column=1, pady =5, padx=15)
    
    def print_puzzle(self, frame, puzzle):
        cell_dict = {}
        for row_index, row in enumerate(puzzle.puzzle):
            for cell_index, cell in enumerate(row):
                id = str(row_index)+str(cell_index)
                if cell != 0:
                    cell_dict[id] = tk.Label(frame, text=str(cell), bg= '#FDF6EC', fg='#6C4A4A', border=0, width=2, font='Lato-Regular 15', justify='center', padx=0, pady=0, )
                else:
                    cell_dict[id] = tk.Entry(frame)
                    cell_dict[id].config(bg= '#FDF6EC', fg='#CDC7BE', border=1, width=2, font='Lato-Regular 15', justify='center', insertborderwidth=0)
                    cell_dict[id].config(validatecommand=(self.is_a_num, '%S', '%i', '%d', cell_dict, id), validate='key')
        for x in cell_dict:
            cell_dict[x].grid(row=x[0], column=x[1], padx=1, pady=1)
    
        return cell_dict

    def back_to_start(self, frame):
        frame.pack_forget()
        self.start(resume=True) 

    def resume(self):
        self.frames['start'].pack_forget()
        self.frames['game'].pack()

    def check_puzzle(self, puzzle_dict, puzzle):
        checklist = []
        missing = 0
        errors = 0
        for i in range(9):
            checklist.append([0 for x in range(9)])
        for key, val in puzzle_dict.items():
            row = int(key[0])
            col = int(key[1])
            if str(val)[25] == 'l':
                checklist[row][col] = puzzle.puzzle[row][col]
            elif str(val)[25] == 'e':
                if val.get() != '':
                    attempt = int(val.get())
                    checklist[row][col] = attempt
                    #print(f'Attempt at row {row}, col {col}: {attempt} {type(attempt)}')
                    if puzzle.grid[row][col] != attempt:
                        errors += 1
                        #print(f'Failed attempt. Expected: {puzzle.grid[row][col]} {type(puzzle.grid[row][col])}')
                        val.configure(fg='#FF8080')
                    else:
                        val.configure(fg='#CDC7BE')
                        #print('All looks good..')
                else:
                    missing +=1
        if missing == 0:
            if errors == 0:
                messagebox.showinfo('PUZZLE SOLVED!', 'Congratulations you have completed the puzzle', )
            else:
                messagebox.showerror('WRONG SOLUTION', 'Sorry, there is an error in the puzzle')
        else:
            messagebox.showwarning('PUZZLE NOT SOLVED YET!', f'There are still unsolved cells in the puzzle ({missing})')

        return checklist

app = sudokuApp()
app.mainloop()