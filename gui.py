from tkinter import *
from tkinter.ttk import *
import pyrebase
import json
from collections import namedtuple

def displayData(eventObject):
    i = 0
    loc_index = 0
    for fld in field_list:
        if fld == "locations":
            loc_index = i
        else:
            setText(entry[i], json_restaurants[combo.get()]._asdict().get(fld))
        i = i + 1
        
    getLocations(None, loc_index)
        
def getLocations(eventObject, index):
    locations = []
    x = json_restaurants[combo.get()]._asdict().get("locations")
    try:
        i = 0
        for loc in x:
            data = {"address":loc.address, "latitude":loc.latitude, "longitude":loc.longitude, "phone":loc.phone}
            locations.append({i:data})
            i = i + 1
    except TypeError:
        locations.append("")
        
    entry[index]["values"] = locations
    entry[index].current(0)

def setText(entry_parm, text):
    entry_parm.delete(0,END)
    try:
        entry_parm.insert(0,text)
    except TclError:
        entry_parm.insert(0,"")
    return

def setWindow(window, title, geo):
    window.title(title)
    window.geometry(geo)
    
def getCombo(frame, state, values, action, side, width):
    combo = Combobox(frame, state=state, values=values, width=width)
    combo.bind("<<ComboboxSelected>>", action)
    combo.current(0)
    combo.pack(side=side)
    return combo

def getButton(frame, text, side, command):
    btn = Button(frame, text=text, command=command)
    btn.pack(side=side)
    return btn
    
    
def addData():
    data = {field_list[0]:entry[0].get(), field_list[1]:entry[1].get(), field_list[2]:entry[2].get(), field_list[3]:entry[3].get(),field_list[4]:entry[4].get(),field_list[5]:entry[5].get(),field_list[6]:entry[6].get()}
    #field_list[0]:entry[0].get(), field_list[1]:entry[1].get(), field_list[2]:entry[2].get(), field_list[3]:entry[3].get(),field_list[4]:entry[4].get(),field_list[5]:entry[5].get(),field_list[6]:entry[6].get()
    #i = 0 
    #for fld in field_list:
     #   tup = namedtuple(field_list[i], entry[i].get())
      #  data.append(tup)
      #  i = i + 1
    db.child("restaurants").child("markets").child("cookeville").child(combo.get()).update(data)
    
config = {
     }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
#authenticate a user
user = auth.sign_in_with_email_and_password("testeraccount@nhfd.fd", "testerman")
db = firebase.database()
all_restaurants = db.child("restaurants").child("markets").child("cookeville").get(user['idToken'])
restaurant_key_list = []
field_list = []
frame = []
label = []
entry = []
json_restaurants = {}

window = Tk()
setWindow(window,"Menu Entry","800x300")
topFrame = Frame(window)

for k in all_restaurants.each():
    #get the restaurant keys
    restaurant_key_list.append(k.key())
    #create restaurant json object
    x = json.loads(json.dumps(k.val()), object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))
    json_restaurants[k.key()] = x
    
#    
for k in all_restaurants.val().get(restaurant_key_list[0]).keys():
    field_list.append(k)

bottomFrame = Frame(window)
btn = getButton(topFrame, "Add Data", LEFT, addData)
combo = getCombo(topFrame, 'readonly', restaurant_key_list, displayData, RIGHT, 20)

i = 0
for fld in field_list:
    frame.append(Frame(bottomFrame))
    
    if fld == "locations":
        entry.append(getCombo(frame[i], "normal", restaurant_key_list, None, RIGHT, 68))
    else:
        entry.append(Entry(frame[i], width=70))
        entry[i].pack(side=RIGHT)
        
    label.append(Label(frame[i], text=fld + ": ", anchor=W))
    label[i].pack(side=LEFT)
    frame[i].pack(fill=BOTH)
    i = i+1
    
topFrame.pack(fill=X)
bottomFrame.pack(fill=BOTH)
displayData(None)
window.mainloop()