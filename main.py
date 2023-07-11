import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from PIL import ImageTk, Image


#######################################################
# This program reads patterns and responses from      #
# intents.json file. It reads User Input from Chatbot #
# UI and matches it with the patterns read from json  #
# file. After calculating the probabilities of each   #
# pattern, if probability is > 80% for a pattern, it  #
# fetches a random response associated with the       #
# respective pattern.                                 #
#######################################################

bot_name = 'BOT'

# If there is a change to intents.json, set it to True. It will retrain the model.
retrain = False

with open("intents.json") as file:
    data = json.load(file)

if not retrain:
    try:

        with open("data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)
    except:
        print("Could not open data.pickle")
else:

    words = []
    labels = []
    docs_pattern = []
    docs_tag = []


    # tokenize every pattern in intents key so that it can be used for comparing  later
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_pattern.append(wrds)
            docs_tag.append(intent["tag"])

        # check if tag exists in labels; if not, add it.
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    #
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_pattern):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        # compare the two lists words and wrds
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_tag[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    # store generated pattern probability inside data.pickle
    # once training is complete, we can directly read this file without going through the training process again
    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)


# ai model
tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

# Once all the neurals are interconnected, then we teach the model.
model = tflearn.DNN(net)
if not retrain:
    try:
        model.load("model.tflearn1")
    except:
        print("Could not find model")
else:
    model.fit(training, output, n_epoch=2000, batch_size=8, show_metric=True)
    model.save("model.tflearn1")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def get_response(msg):
        results = model.predict([bag_of_words(msg, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        if results[results_index] > 0.8:

            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

                    return random.choice(responses)
        else:
            return "I do not understand :("





##############################################################
#                  CHAT BOT USER INTERFACE                   #
##############################################################

root = Tk()
root.geometry("410x510")
root['bg'] = 'black'
root.resizable(0, 0)

# create main menu
main_menu = Menu(root)

#create sub nenu
file_menu = Menu(root)
main_menu.add_command(label='Quit', command=root.quit)
root.config(menu=main_menu)



canvas = Canvas(root, height=700, width=800)
canvas.pack()

# 1 logo frame <- first pg
frame = tk.Frame(root, bg="white")
frame.place(relwidth=1, relheight=1)

photo = ImageTk.PhotoImage(file="logo.png")
photo_label = tk.Label(frame, image=photo, bg='white')  # making the image into a label
photo_label.place(x=1, y=-2)


w = tk.Label(root,
             text='Hello!',
             bg='white',
             fg='black',
             font=('Times', 14)
             )
w.place(relx=0.44, rely=0.60)

r = tk.Label(root,
             text='I\'m Querry!',
             bg='white',
             fg='black',
             font=('Times New Roman', 14),
             justify='center'
             )
r.place(relx=0.38, rely=0.65)

# frame1 stuff
chatWindow = Text(root, bg='#edede9', width=50, height=8, padx=15, pady=5)
chatWindow.configure(cursor='arrow', state=DISABLED)

scrollbar = Scrollbar(chatWindow)
scrollbar.configure(command=chatWindow.yview)


def on_enter_pressed(event):
    msg = messageWindow.get()


messageWindow_label = tk.Label(root, width=30, height=4)
messageWindow = tk.Entry(root, bg='#d6ccc2')
messageWindow.focus()
messageWindow.bind("<Return>", on_enter_pressed)




def send(msg, sender):
    if not msg:
        return

    send = f"{sender}:  {msg}"
    # send = '{}: {}'.format(sender, msg)
    chatWindow.configure(state=NORMAL)
    chatWindow.insert(END, '\n' + send)
    chatWindow.configure(state=DISABLED)
    messageWindow.delete(0, END)

    receive = f"{bot_name}:  {get_response(msg)}\n"
    # receive = '{}: {}'.format(bot_name, chat())
    chatWindow.configure(state=NORMAL)
    chatWindow.insert(END, '\n' + receive)
    chatWindow.configure(state=DISABLED)

    chatWindow.see(END)


def on_enter(event):
    msg = messageWindow.get()
    send(msg, "YOU")


button = tk.Button(frame, text='Send', bg='white', fg='black',
                   height=5, width=12, font=('Courier', 16, 'bold'), command=lambda : on_enter(None))


def frame1():
    global b1
    b1.destroy()
    photo_label.destroy()

    chatWindow.place(x=6, y=6, height=385, width=390)

    scrollbar.place(relheight=1, relx=1)

    messageWindow_label.place(x=7, y=400, height=88, width=260)
    messageWindow.place(x=7, y=400, height=88, width=260)

    button.place(x=273, y=400, height=88, width=120)


def frame2():
    with open('instructions.txt', r) as file1:
        for text in f.readlines():
            for word in text.split():
                print(word)


b1 = tk.Button(frame, text='Let\'s Chat!', bg='white', fg='black', font=('Courier', 16, 'bold'), border=3, command=frame1)
b1.place(relx=0.30,
         rely=0.80)

b2 = tk.Button(frame, text="Instructions", bg = 'white', fg='black', font=("Courier", 16, 'bold'), border=3, command=frame2)
root.mainloop()