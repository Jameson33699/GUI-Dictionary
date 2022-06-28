from tkinter import *
import json
from difflib import get_close_matches
from tkinter import messagebox
import pyttsx3

# Functionality

engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)
engine.setProperty('rate', 125)


def search():
    #    word = search_bar.get()
    #    dictionary = Dictionary(word)
    #    if word in dictionary:
    #        meaning = dictionary.print_meanings()
    #        for item in meaning:
    #            text_area.insert(item)

    data = json.load(open('data.json'))
    word = search_bar.get()
    word = word.lower()
    if word in data:
        meaning = data[word]
        text_area.delete(1.0, END)
        for item in meaning:
            text_area.insert(END, u'\u2022' + item + '\n\n')
    elif len(get_close_matches(word, data.keys())) > 0:
        close_match = get_close_matches(word, data.keys())[0]
        response = messagebox.askyesno('Confirm', f'Did you mean {close_match} ?')
        if response:
            search_bar.delete(0, END)
            search_bar.insert(END, close_match)
            meaning = data[close_match]
            text_area.delete(1.0, END)
            for item in meaning:
                text_area.insert(END, u'\u2022' + item + '\n\n')
        else:
            messagebox.showerror("Word not found",
                                 "Your word search cannot be found, please double check your spelling")
            search_bar.delete(0, END)
            text_area.delete(1.0, END)

    else:
        messagebox.showerror("Word not found",
                             "Hmm that doesn't seem to be a word, you might want to check your spelling")
        search_bar.delete(0, END)
        text_area.delete(1.0, END)


def clear():
    search_bar.delete(0, END)
    text_area.delete(1.0, END)


def close():
    response = messagebox.askyesno('Close Window', 'Are you sure you want to close application?')
    if response:
        root.destroy()
    else:
        pass


def word_audio():
    engine.say(search_bar.get())
    engine.runAndWait()


def meaning_audio():
    engine.say(text_area.get(1.0, END))
    engine.runAndWait()
# GUI


root = Tk()

root.geometry('916x611+300+100')
root.title("Personal Dictionary")
root.resizable(False, False)

bg_image = PhotoImage(file='background_916x611.png')
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0)

enter_word_label = Label(root, text='Word Search', font=('castellar', 20, 'bold'), fg='black', bg='#EBE9EA')
enter_word_label.place(x=450, y=50)

search_bar = Entry(root, font=('ariel', 16, 'italic', 'bold'), justify=CENTER, bd=8, relief=GROOVE)
search_bar.place(x=440, y=100)

search_image = PhotoImage(file='srch.png')
search_button = Button(root, image=search_image, bd=0, bg='#EBE9EA', cursor='hand2', activebackground='#EBE9EA',
                       command=search)
search_button.place(x=550, y=150)

mic_image = PhotoImage(file='mic.png')
mic_button = Button(root, image=mic_image, bd=0, bg='#EBE9EA', cursor='hand2', activebackground='#EBE9EA',
                    command=word_audio)
mic_button.place(x=650, y=150)

meaning_label = Label(root, text='Definitions', font=('castellar', 20, 'bold'), fg='black', bg='#EBE9EA')
meaning_label.place(x=470, y=250)

text_area = Text(root, width=50, height=10, font=('ariel', 14, 'italic', 'bold'), bd=8, relief=GROOVE)
text_area.place(x=300, y=300)

clear_img = PhotoImage(file='delete-symbol.png')
clear_button = Button(root, image=clear_img, bd=0, bg='#EBE9EA', cursor='hand2', activebackground='#EBE9EA',
                      command=clear)
clear_button.place(x=550, y=560)

audio_img = PhotoImage(file='mic.png')
audio_button = Button(root, image=audio_img, bd=0, bg='#EBE9EA', cursor='hand2', activebackground='#EBE9EA',
                      command=meaning_audio)
audio_button.place(x=650, y=560)

exit_img = PhotoImage(file='exit.png')
exit_button = Button(root, image=exit_img, bd=0, bg='#EBE9EA', cursor='hand2', activebackground='#EBE9EA',
                     command=close)
exit_button.place(x=875, y=25)


def enter_function():
    search_button.invoke()


root.bind('<Return>', enter_function)

root.mainloop()
