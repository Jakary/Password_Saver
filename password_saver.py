import sqlite3,hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial

class login(Tk):
	def __init__(self):
		super(). __init__()
		self.geometry("700X500")
		self.resizable(False,False)
	def Label(self):
		self.backgroundImage=PhotoImage(file="bg.jpg")
		self.backgroundImageLabel




if __name__ ==" __main__":
	Login=login()
	Login.Label()
	Login.mainloop()




#datbase code
with sqlite3.connect("password_vault.db")as db:
	cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")

#Create popup
def popUp(text):
	answer = simpledialog.askstring("input string", text)
	
	return answer

#initiate window
window = Tk()
window.title("Password Vault")

def hashPassword(input):
	hash = hashlib.md5(input)
	hash = hash.hexdigest()

	return hash


def firstScreen():
	window.geometry("400x400")

	lbl=Label(window,text="create your password")
	lbl.config(anchor=CENTER)
	lbl.pack()


	text = Entry(window, width=20 )
	text.pack()
	text.focus()


	lbl1=Label(window, text="re enter your password")
	lbl1.pack()

	text1 = Entry(window, width=20)
	text1.pack()
	text1.focus()

	lbl2 = Label(window)
	lbl2.pack()

	def savePassword():
		if text.get() == text1.get():
			hashedPassword = hashPassword(text.get().encode('utf-8'))

			insert_password = """INSERT INTO masterpassword(password)
			VALUES(?)"""
			cursor.execute(insert_password, [(hashedPassword)])
			db.commit()

			passwordVault()
		else:
			lbl2.config(text="password does not match")

	button = Button(window,text="Save", command=savePassword)
	button.pack()

def loginScreen():
	window.geometry("500x700")
#text output
	lbl=Label(window,text="enter password")
	lbl.config(anchor=CENTER)
	lbl.pack()

# text entry
	text = Entry(window, width=20 ,show="*")
	text.pack()
	text.focus()

# wrong password
	lbl1=Label(window)
	lbl1.pack()
	def getMasterPassword():
		checkHashedPassword =  hashPassword(text.get().encode('utf-8'))
		cursor.execute("SELECT * FROM masterpassword WHERE id=1 AND password = ?",[(checkHashedPassword)])
		print(checkHashedPassword)
		return cursor.fetchall()

	def checkPassword():
		match = getMasterPassword()

		print(match)
		

		if match:
			passwordVault()
		else:
			text.delete(0,'end')
			lbl.config(text="Wrong Password")


	button = Button(window,text="submit", command=checkPassword)
	button.pack(pady=10)

def passwordVault():
	for widget in window.winfo_children():
		widget.destroy()

	def addEntry():
		text1= "Website"
		text2 = "Username"
		text3 = "Password"

		website = popUp(text1)
		username = popUp(text2)
		pasword = popUp(text3)

		insert_fields = """INSERT INTO vault(website,username,password) 
		VALUES(?, ?, ?)"""

		cursor.execute(insert_fields, (website,username,pasword))
		db.commit()

		passwordVault()

	def removeEntry(input):
		cursor.execute("DELETE FROM vault WHERE id = ?",(input,))
		db.commit()

		passwordVault()

	window.geometry("700x350")

	lbl = Label(window, text="passwordVault")
	lbl.grid(column=1)

	button = Button(window, text="+", command=addEntry)
	button.grid(column=1,pady=10)

	lbl = Label(window,text="website")
	lbl.grid(row=2, column=0,padx=80)
	lbl = Label(window,text="username")
	lbl.grid(row=2, column=1,padx=80)
	lbl = Label(window,text="password")
	lbl.grid(row=2, column=2,padx=80)

	cursor.execute("SELECT * FROM vault")
	if(cursor.fetchall() != None):
		i = 0
		while TRUE:
			cursor.execute("SELECT * FROM vault")
			array = cursor.fetchall()


			lbl1 = Label(window, text=(array[i][1]))
			lbl1.grid(column=0, row= i+3)
			lbl1 = Label(window, text=(array[i][2]))
			lbl1.grid(column=1, row= i+3)
			lbl1 = Label(window, text=(array[i][3]))
			lbl1.grid(column=2, row= i+3)

			button=Button(window, text="delete", command=partial(removeEntry,array[i][0]))
			button.grid(column=3, row=i+3, pady=10)

			i = i+1

			cursor.execute("SELECT * FROM vault")
			if (len(cursor.fetchall()) <=i):
				break




cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
	loginScreen()
else:
	firstScreen()
window.mainloop() 