import requests	
from bs4 import BeautifulSoup 
from random import randrange
try:
    from Tkinter import * # python2
except ImportError: # python3
    from tkinter import *

try:
  url = "http://quotes.toscrape.com/"
  r = requests.get(url, timeout = 5)
  r.raise_for_status()

  # store quotes here
  list_of_quotes = []

  for i in range(1, 11): # no joke here, website really has only 10 pages
    url = "http://quotes.toscrape.com/page/{}".format(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser") 
    # finding all divs with class = quote
    fortune_quotes = soup.find_all("div", class_ = "quote")
  
    for f_quote in fortune_quotes:
      # get all contents 
      content = f_quote.contents
      # author is the third item in content
      author = content[3].find_all("small", class_ = "author")[0].text
      # quote is the first item in content
      quote = content[1].text
      # we want our quote to fit the paper in the background pic
      if(len(quote) < 1000):
        q = quote + "\n\n" + author.upper()
        list_of_quotes.append(q)

  # printing quotes on button click    
  def print_quote():
    random_quote = randrange(0, len(list_of_quotes))
    # label text set to quote
    label.config(text = list_of_quotes[random_quote])
    # animate button press
    button.config(state = ACTIVE, relief = SUNKEN) # let it sink in
    button.after(200, lambda: button.config(relief = RAISED, state = NORMAL)) # bring it back up
   
  # make some gui
  root = Tk()
  root.resizable(width = False, height = False) # making window to be non-resizable
  root.geometry("625x460") 
  
  heart_symbol = u'\u2765' # because we want things to be pretty
  app_title = "Fortune Cookie" + " " + heart_symbol 
  root.title(app_title)
  
  background = PhotoImage(file = "assets/bg.png")
  background_label = Label(root, image = background)
  background_label.grid(row = 0)

  button_frame = Frame(root)
  button_frame.grid() 

  label_frame = Frame(root)
  label_frame.grid(row = 0)
  
  label = Label(label_frame, 
	      text = "Get your quote of the day!",
	      background = "#DBDBDB", # color of our paper in the background pic
	      font = ("Helvetica", 8, "italic"),
	      wraplength = 200)
  label.grid() 

  button = Button(button_frame, 
		text = "Try me",
		foreground = "black", 	
		command = print_quote, 
		cursor = "heart",
		font = ("Verdana", 9))
  button.grid()

  # center the window so it doesn't pop up wherever it wants
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

# catch exceptions and write proper messages about them
except requests.HTTPError as http_err:
  print("HTTP Error" + ": " + str(http_err))
except requests.ConnectionError as con_err:
  print("Connection Error. Make sure you are connected to Internet. \nTechnical Details given below: \n")
  print(str(con_err))
except requests.Timeout as time_err:
  print("Timeout Error: ")
  print(str(time_err))
except requests.RequestException as req_err:
  print("General Error: ")
  print(str(req_err))
