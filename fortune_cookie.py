import requests
from bs4 import BeautifulSoup 
from random import randrange
try:
    from Tkinter import * #python2
except ImportError: #python3
    from tkinter import *
   
url = "http://quotes.toscrape.com/"
r = requests.get(url)

#store quotes here
list_of_quotes = []

for i in range(1, 11): #no joke here, website really has only 10 pages
  url = "http://quotes.toscrape.com/page/{}".format(i)
  r = requests.get(url)
  soup = BeautifulSoup(r.content, "lxml") #using lxml will speed things up
  #finding all divs with class = quote
  fortune_quotes = soup.find_all("div", class_ = "quote")
  
  for f_quote in fortune_quotes:
    # author is the third item in contents
    author = f_quote.contents[3].find_all("small", class_ = "author")[0].text
    # quote is the first item in contents 
    quote = f_quote.contents[1].text
    q = quote + " \n" + author.upper()
    list_of_quotes.append(q)
 
# printing quotes on button click    
def print_quote():
  random_quote = randrange(0, len(list_of_quotes))
  # label text set to quote
  label.config(text = list_of_quotes[random_quote])
  # animate button press
  button.config(state = ACTIVE, relief = SUNKEN) #let it sink in
  button.after(200, lambda: button.config(relief = RAISED, state = NORMAL)) #bring it back up
   
#make some gui
root = Tk()
app_title = "Fortune Cookie" + " " + u'\u2765' #heart symbol because we want things to be pretty

root.title(app_title)
root.geometry("530x385")

background = PhotoImage(file = "background.png")
background_label = Label(root, image = background)
background_label.grid(row = 0, column = 0)

button_frame = Frame(root)
button_frame.grid() 

label_frame = Frame(root)
label_frame.grid(row = 0)

label = Label(label_frame, 
	      text = "Get your quote of the day!",
	      background = "misty rose", 
	      font = ("Courier", 10, "italic"),
	      wraplength = 500,
	      compound = "top",
	      relief = RIDGE)

label.grid() 

button = Button(button_frame, 
		text = "Try me",
		background = "LightPink1",
		foreground = "black", 
		command = print_quote, 
		cursor = "heart",
		font = ("Verdana", 9))

button.grid()

#center the window so it doesn't pop up wherever it wants
def center_window():
  root.withdraw()
  root.update_idletasks()  
  width = root.winfo_screenwidth()
  reqwidth = root.winfo_reqwidth()
  height = root.winfo_screenheight()
  reqheight = root.winfo_reqheight()
  x = (width - reqwidth) / 2
  y = (height - reqheight) / 2
  root.geometry("+%d+%d" % (x, y))
  root.deiconify()

center_window()  
root.mainloop()