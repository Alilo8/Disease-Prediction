#!/usr/bin/env python

from tkinter import *
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model

data = pd.read_csv('Training new.csv')
df = pd.read_csv('disease_precaution.csv')
precaution = {}
for i, row in df.iterrows():
    precaution[row['Disease']] = [row['Symptom_precaution_0'] , row['Symptom_precaution_1'] , str(row['Symptom_precaution_2']) , str(row['Symptom_precaution_3'])]

l1 = list(data.columns[:-1])
l1.append('aaa')
l2=[]
for i in range(len(l1)-1):
    l2.append(0)

cnn_model = pickle.load(open('cnn_model.sav', 'rb'))
cnn_model = load_model('cnn_model')
labelEncoder = pickle.load(open('labelEncoder.sav', 'rb'))


def CNN():
    psymptoms = list(lb.get(0,lb_count[0]))
    index = []
    for i in psymptoms:
        if i=='aaa' or i=='Select Here':
            index.append(psymptoms.index(i))
            
    for i in range(len(index)-1,-1,-1):
        del(psymptoms[index[i]])
    
    l2 = []
    for i in range(len(l1)-1):
        l2.append(0)
        
    for k in range(len(l1)):
        for z in psymptoms:
            if(z==l1[k]):
                l2[k]=1
    
    inputtest = np.array([l2])
    inputtest = np.reshape(inputtest, (inputtest.shape[0], inputtest.shape[1], 1))
    inputtest = np.expand_dims(inputtest, axis=-1)
    predict = cnn_model.predict(inputtest)
    t1.delete("1.0", END)
    temp = predict.argmax()
    temp = labelEncoder.inverse_transform([temp])
    t1.insert(END, temp[0])
    t2.insert(END, *precaution[predict[0]])

def prediction():
    CNN()
     
# GUI stuff..............................................................................
        
root = Tk()
root.configure(background='white')

Symptom1 = StringVar()
Symptom1.set("Select Here")


Name = StringVar()


NameLb = Label(root, text="Name", fg="black", bg="silver")
NameLb.config(font=("Times",15,"bold italic"))
NameLb.grid(row=6, column=0, pady=15, sticky=W)

S1Lb = Label(root, text="Symptom", fg="black", bg="silver")
S1Lb.config(font=("Times",15,"bold italic"))
S1Lb.grid(row=7, column=0, pady=10, sticky=W)

lrLb = Label(root, text="CNN", fg="white", bg="black")
lrLb.config(font=("Times",15,"bold italic"))
lrLb.grid(row=15, column=0, pady=10,sticky=W)

ranfLb = Label(root, text="Precaution",fg="white", bg="black")
ranfLb.config(font=("Times",15,"bold italic"))
ranfLb.grid(row=17, column=0, pady=10, sticky=W)

OPTIONS = sorted(l1)

NameEn = Entry(root, textvariable=Name)
NameEn.grid(row=6, column=1)

from tkinter import ttk

S1 = ttk.Combobox(root, textvariable=Symptom1, values=OPTIONS)
S1.grid(row=7, column=1)

lb = Listbox(root)
lb_count = [0]
lb.grid(row=9, column=1 , padx=10)

def add():
    lb.insert(lb_count[0],Symptom1.get())
    lb_count[0] += 1

def delete():
    lb_count[0] -= 1
    lb.delete(lb_count[0])
    
def clear():
    lb_count[0] = 0
    lb.delete(0,'end')
    
add_btn = Button(root, text="Add", command=add,bg="White",fg="green")
add_btn.config(font=("Times",15,"bold italic"))
add_btn.grid(row=10, column=0,padx=0)

del_btn = Button(root, text="Delete", command=delete,bg="White",fg="green")
del_btn.config(font=("Times",15,"bold italic"))
del_btn.grid(row=10, column=1,padx=0)

del_btn = Button(root, text="Clear", command=clear,bg="White",fg="green")
del_btn.config(font=("Times",15,"bold italic"))
del_btn.grid(row=10, column=2,padx=0)

dst = Button(root, text="Prediction", command=prediction,bg="White",fg="green")
dst.config(font=("Times",15,"bold italic"))
dst.grid(row=8, column=2,padx=10)

t1 = Listbox(root, height=5, width=40,bg="white",fg="black")
t1.config(font=("Times",15,"bold italic"))
t1.grid(row=15, column=1, padx=10)

t2 = Text(root, height=1, width=20,bg="white",fg="black")
t2.config(font=("Times",15,"bold italic"))
t2.grid(row=17, column=1 , padx=10)


root.mainloop()

