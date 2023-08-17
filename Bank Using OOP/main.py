from datetime import date, datetime
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkcalendar import *
from PIL import ImageTk, Image

#TKINTER
root = Tk()
root.title("Curry's Bank")
root.resizable(False, False)
root.geometry('+470+300')

gold = '#9C7A00'

welcome = Frame(root, bg=gold)
sign_menu = Frame(root, bg=gold)

#SETUP
countries =('Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola',
 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia',
 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus',
 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island',
 'Brazil', 'British Indian Ocean Territory', 'Brunei', 'Bulgaria', 'Burkina Faso',
 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic',
 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros',
 'Congo', 'The Democratic Republic of the Congo', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire",
 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica',
 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea',
 'Estonia', 'Eswatini', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland',
 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon',
 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada',
 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti',
 'Heard Island and McDonald Islands', 'Vatican City', 'Honduras', 'Hong Kong',
 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland',
 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya',
 'Kiribati', "South Korea", 'North Korea', 'Kuwait', 'Kyrgyzstan',
 "Laos", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein',
 'Lithuania', 'Luxembourg', 'Macao', 'North Macedonia', 'Madagascar', 'Malawi', 'Malaysia',
 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte',
 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro',
 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands',
 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island',
 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine',
 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal',
 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy',
 'Saint Helena (Ascension and Tristan da Cunha)', 'Saint Kitts and Nevis', 'Saint Lucia',
 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines',
 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles',
 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands',
 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka',
 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Sweden', 'Switzerland',
 'Syrian Arab Republic', 'Taiwan', 'Tajikistan', 'Tanzania',
 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan',
 'Vanuatu', 'Venezuela', 'Vietnam', 'UK Virgin Islands', 'US Virgin Islands',
 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe')
customers = []
data_file = 'data.txt'
cur_name = ''

q = PrettyPrinter()

with open(data_file, 'r') as f:
    data = f.readlines()

users_index = {}

def go_home():
    global win
    try:
        win.destroy()
    except:
        pass
    mylb.set('')
    password_etr.delete(0, END)
    firstname_etr.delete(0, END)
    surname_etr.delete(0, END)
    sign_menu.pack_forget()
    welcome.pack()

def get_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def show_and_hide():
    if password_etr.cget('show') == '•':
        password_etr.config(show='')
        show_hide.config(text='Hide')
    else:
        password_etr.config(show='•')
        show_hide.config(text='Show')

#WELCOME
def go_sign_menu():
    if sign_button['text'] == 'Sign In':
        welcome.pack_forget()
        sign_menu.pack()
    else:
        signed_as['text'] = 'Not\nsigned in'
        sign_button['text'] = 'Sign In'

signed_as = Label(welcome, font='Helvetica 20 bold', bg=gold, text='Not\nsigned in')
signed_as.grid(row=0, column=0)

myimg = ImageTk.PhotoImage(Image.open("Curry's Bank.jpg").resize((640,120)))
Label(welcome, image=myimg).grid(row=0, column=1, pady=10, padx=10)

sign_button = Button(welcome, text='Sign In', font='Helvetica 20 bold', bg=gold, command=go_sign_menu)
sign_button.grid(padx=10, row=0, column=2)

#SIGN_MENU
def change_sign():
    if sign_title.cget('text') == 'Sign In':
        sign_title['text'] = 'Sign Up'
        have_acc['text'] = 'I already have\nan account'
        extras.grid(row=4, columnspan=2, pady=10)
    else:
        sign_title['text'] = 'Sign In'
        date_dis['text'] = 'Not Selected'
        mylb.set('')
        have_acc['text'] = "I don't have\nan account"
        extras.grid_forget()

def check_date(calendar):
    win.destroy()
    date_dis['text'] = calendar.get_date()

def pop_cal():
    global win
    try:
        win.destroy()
    except:
        pass

    win = Toplevel(root)
    win.title('Choose DoB')
    win['bg'] = gold
    calendar = Calendar(win, locale='en_UK', selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, font='Helvetica 20 bold',
                        background=gold, foreground='black', bordercolor='black', normalbackground=gold, showweeknumbers=False,
                        maxdate=date(datetime.now().year, datetime.now().month, datetime.now().day), weekendbackground=gold,
                        weekendforeground='black', othermonthbackground='grey', othermonthforeground='black',
                        othermonthwebackground='grey', othermonthweforeground='black', headersbackground=gold,
                        disableddaybackground = 'black', disableddayforeground = 'black')
    calendar.grid()
    grab_date = Button(win, text='Submit', width=22, font='Helvetica 25 bold', bg=gold, command=lambda: check_date(calendar))
    grab_date.grid()

def pop_message(message):
    global x
    try:
        x.destroy()
    except:
        pass
    x = Toplevel(root, bg=gold)
    x.geometry('+620+420')
    Label(x, text=message, font='Helvetica 25 bold', bg=gold).grid(padx=20, pady=20)
    cur_name = ''
    x.after(5000, x.destroy)

def enter_details_():
    global cur_name
    cur_name = f"{firstname_etr.get()} {surname_etr.get()}"
    #check if account name is registered
    if sign_title.cget('text') == 'Sign In':
        if cur_name in users_index:
            if password_etr.get() == customers[users_index[cur_name]].password:
                signed_as['text'] = f'Signed in as:\n{cur_name}'
                sign_button['text'] = 'Sign Out'
                go_home()
        else:
            pop_message('Name not registered')
    elif cur_name not in users_index:
        #check if all entries are valid
        if len(cur_name) >= 3 and len(password_etr.get()) != 0 and '/' in date_dis['text'] and mylb.get() != '':
            if cur_name.isalpha() and get_age(date(*reversed([int(i) for i in date_dis['text'].split('/')]))) >= 18:
                new_customer = BankCustomer(firstname_etr.get(), surname_etr.get(), password_etr.get(), mylb.get(), *reversed([int(i) for i in date_dis['text'].split('/')]), 0)
                customers.append(new_customer)
                data.append(f"{firstname_etr.get()},{surname_etr.get()},{password_etr.get()},{mylb.get()},{','.join(reversed([i for i in date_dis['text'].split('/')]))}\n")
                with open(data_file, 'w') as f:
                    for line in data:
                        f.write(line)
                signed_as['text'] = f'Signed in as:\n{cur_name}'
                sign_button['text'] = 'Sign Out'
                go_home()
            else:
                pop_message('   Requirements:\n'
                            '-Must be 18 or above\n'
                            '-No numbers in name')
        else:
            pop_message('Please fill out\nall fields')
    else:
        pop_message('Name already registered')

extras = Frame(sign_menu, bg=gold)

back = Button(sign_menu, text='🔙', command=go_home, font='Helvetica 30 bold', bg=gold)
back.grid(sticky=W, columnspan=2)

sign_title = Label(sign_menu, text='Sign In', font='Helvetica 50 bold', bg=gold)
sign_title.grid(row=0, columnspan=2)

have_acc = Button(sign_menu, text="I don't have\nan account", font='Helvetica 20 bold', bg=gold, command=change_sign)
have_acc.grid(row=0, columnspan=2, sticky=E)

Label(sign_menu, text='First Name', font='Helvetica 30 bold', bg=gold).grid(row=1, column=0, sticky=W)
firstname_etr = Entry(sign_menu, validatecommand=(root.register(lambda text: ' ' not in text), '%P'), validate='key', font='Helvetica 30 bold', bg=gold, width=24)
firstname_etr.grid(row=1, column=1, sticky=W)

Label(sign_menu, text='Last Name', font='Helvetica 30 bold', bg=gold).grid(row=2, column=0, sticky=W)
surname_etr = Entry(sign_menu, validatecommand=(root.register(lambda text: ' ' not in text), '%P'), validate='key', font='Helvetica 30 bold', bg=gold, width=24)
surname_etr.grid(row=2, column=1, sticky=W)

Label(sign_menu, text='Password', font='Helvetica 30 bold', bg=gold).grid(row=3, column=0, sticky=W)
password_etr = Entry(sign_menu, font='Helvetica 30 bold', bg=gold, show='•', width=20, validatecommand=(root.register(lambda text: len(text) < 25), '%P'), validate='key')
password_etr.grid(row=3, column=1, sticky=W)
show_hide = Button(sign_menu, text='Show', font='Helvetica 20 bold', bg=gold, command=show_and_hide)
show_hide.grid(row=3, column=1, sticky=E)

Label(extras, text='Choose DoB📆', font='Helvetica 30 bold', bg=gold).grid(row=0, column=0, padx=(10, 50))
date_dis = Button(extras, text='Not selected', font='Helvetica 30 bold', bg=gold, command=pop_cal)
date_dis.grid(row=1, column=0, padx=(10, 50))

Label(extras, text='Choose Country', font='Helvetica 30 bold', bg=gold).grid(row=0, column=1, padx=(0, 10))
mystyle = ttk.Style()
mystyle.theme_use('clam')
bigfont = Font(family="Helvetica",size=20, weight='bold')
root.option_add("*TCombobox*Listbox*Font", bigfont)
mystyle.configure('TCombobox', foreground='black', textsize=10, arrowsize=30, font='Helvetica 44 bold', background=gold, fieldbackground=gold, selectedbackground='black', fieldforeground=gold)
mylb = ttk.Combobox(extras, values=countries, width=20, state="readonly", style='TCombobox', font='Helvetica 20 bold')
mylb.grid(row=1, column=1)

enter_details = Button(sign_menu, command=enter_details_, text='Enter Details', font='Helvetica 30 bold', bg=gold, width=31)
enter_details.grid(row=10, columnspan=2)

#MAIN
class BankCustomer:
    def __init__(self, first_name: str, last_name: str, password: str, country: str, yearob: int, monthob: int, dayob: int, balance: float):
        self.name = (f'{first_name} {last_name}')
        self.password = password
        self.country = country
        self.balance: float = balance
        self.dob = date(int(yearob), int(monthob), int(dayob))
    def get_details(self):
        return f"""{self.name}\n
        Born {self.dob}
        {get_age(self.dob)} years old
        £{str(self.balance)}"""
    def deposit(self, amount):
        self.balance += float(amount)
    def withdraw(self, amount):
        if self.balance > amount:
            self.balance -= float(amount)

for i, line in enumerate(data):
    new_customer = BankCustomer(*line.split(','))
    customers.append(new_customer)
    users_index[f"{line.split(',')[0]} {line.split(',')[1]}"] = i

welcome.pack()
root.mainloop()