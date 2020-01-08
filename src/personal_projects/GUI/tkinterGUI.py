import tkinter

window = tkinter.Tk()

window.title('Petters magiske GUI')

label = tkinter.Label(window, text='Og jeg er Petter den magiske proggern').pack()
button = tkinter.Button(window, text='please dont click this')
button.pack()
checkvariable = tkinter.IntVar()
checker = tkinter.Checkbutton(window, text='Something', variable=checkvariable
                              ).pack()
def var_states():
    print(f'State of the checker {checkvariable.get()}')

button2 = tkinter.Button(window, text='vis', command=var_states).pack()

def test():
    if checkvariable is True:
        tkinter.Label(window, text='Nå skjedde det noe').pack()
    else:
        tkinter.Label(window, text='Nei, detta gikk dårlig').pack()


tkinter.Button(window, text='Klikk på meg!!!', command=test).pack()
window.mainloop()
