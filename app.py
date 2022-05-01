import tkinter
from tkinter.font import BOLD
from turtle import color

win = tkinter.Tk()
win.geometry('300x400')

title = tkinter.Label(win, text='SUDOKU', bg='#D0CAB2', fg='#FDF6EC', pady=5, )
main = tkinter.Label(win, text='   ',bg='#DED9C4')
grid = tkinter.Label(main, text='grid',bg='#D0CAB2')

def button_press():
    print('Button pressed!')
new_game_button = tkinter.Button(main, text='New Game', bg='#D0CAB2', fg='#FDF6EC', border=0, padx=10, pady=5, command=button_press)

cell_ids = []
for i in range (0,9):
    for j in range(0,9):
        id = str(i)+str(j)
        cell_ids.append(id)
cell_dict = {}
for x in cell_ids:
    cell_dict[x] = tkinter.Entry(grid, bg= '#FDF6EC', border=1, width=2, font='helvetica 15')
print(cell_dict)

title.pack(fill=tkinter.X)
main.pack(fill=tkinter.BOTH, expand=True)
grid.pack()
new_game_button.pack(side='bottom')
for x in cell_dict:
    cell_dict[x].grid(row=x[0], column=x[1])

win.mainloop()