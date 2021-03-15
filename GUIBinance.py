# GUIBinance.py
from tkinter import *
from tkinter import ttk

####################################

import time
from datetime import datetime, timedelta
from time import mktime
from binance.client import Client
from pprint import pprint


def ServerTime():
    time_res = client.get_server_time()
    tm = time_res['serverTime'] / 1000

    dt = datetime.fromtimestamp(mktime(time.localtime(tm)))
    # dt = dt + timedelta(hours=7) # only on colab
    dt = dt.strftime('%Y-%m-%d %H:%M:%S')  # strftime.org
    print(dt)
    return dt


API_KEY = 'KmmKN74wuPNFKUMN5FHLWyDOwNzW8U7Pbhl3HOVtb4t3olRV9JNA5O5aBCnvFtgh'
SECRET_KEY = '7WTPYuPItpWIUAyghUiErXl89tkyjJrf288iwFVE27wI0BK0K2Q6Gb2qMXkgR6WP'
client = Client(API_KEY, SECRET_KEY)

###################################


GUI = Tk()
GUI.geometry('700x500')
GUI.title('Uncle Smart Crypto by Uncle Engineer')

FONT1 = (None, 30)

# Tab

Tab = ttk.Notebook(GUI)

T1 = Frame(Tab)
T2 = Frame(Tab)
T3 = Frame(Tab)
T4 = Frame(Tab)

Tab.pack(fill=BOTH, expand=1)

# icont1 = PhotoImage(file='t1.png')
# icont2 = PhotoImage(file='t2.png')
# icont3 = PhotoImage(file='t3.png')
# icont4 = PhotoImage(file='t4.png')

# Tab.add(T1, text='Market', image=icont1, compound='left')
# Tab.add(T2, text='Sell', image=icont2, compound='left')
# Tab.add(T3, text='Buy', image=icont3, compound='left')
# Tab.add(T4, text='Balance', image=icont4, compound='left')

Tab.add(T1, text='Market', compound='left')
Tab.add(T2, text='Sell', compound='left')
Tab.add(T3, text='Buy', compound='left')
Tab.add(T4, text='Balance', compound='left')

F1 = ttk.Labelframe(T1, text='Market Price')
F1.place(x=50, y=50)

# LABEL
L1 = ttk.Label(F1, text='เหรียญ', font=FONT1)
L1.grid(row=0, column=0, padx=20)

# ENTRY COIN
v_coin = StringVar()  # เก็บข้อมูลใน gui
v_coin.set('BTCUSDT')
E1 = ttk.Entry(F1, textvariable=v_coin, font=FONT1, width=15)
E1.grid(row=0, column=1, padx=20)


# BUTTON
def CheckPrice(event=None):
    global autostate
    # print(v_coin.get())
    symbol = v_coin.get()
    try:
        tickers = client.get_ticker(symbol=symbol)
        pprint(tickers)

        lastprice = float(tickers['lastPrice'])

        if lastprice > 5000:
            text = '{} : {:,.2f} ($)'.format(symbol, lastprice)
        elif lastprice > 200:
            text = '{} : {:,.3f} ($)'.format(symbol, lastprice)
        elif lastprice > 10:
            text = '{} : {:,.5f} ($)'.format(symbol, lastprice)
        else:
            text = '{} : {:,.8f} ($)'.format(symbol, lastprice)

        v_result.set(text)
    except Exception as e:
        # print(e)
        v_result.set('---มีปัญหาในการเช็คราคา---')
        ChangeState(state=False)

    if autostate == True:
        E1.configure(state='disabled')
        Result.after(500, CheckPrice)


B1 = ttk.Button(F1, text='เช็คราคา', command=CheckPrice)
B1.grid(row=1, column=1, padx=20, pady=10, ipady=10, ipadx=20)

E1.bind('<Return>', CheckPrice)

F2 = Frame(T1)
F2.place(x=50, y=200)

v_result = StringVar()
v_result.set('------RESULT------')

Result = ttk.Label(F2, textvariable=v_result, font=(None, 35))
Result.pack()

# ---------MODE ----------
autostate = False


def ChangeState(event=None, state=None):
    global autostate
    autostate = not autostate

    if state is not None:
        autostate = state

    if autostate == True:
        v_status.set('Status: (Auto) [F1] Change to Manual')
        CheckPrice()
    else:
        E1.configure(state='enabled')
        v_status.set('Status: (Manual) [F1] Change to Auto')


GUI.bind('<F1>', ChangeState)

v_status = StringVar()
v_status.set('Status: (Manual) [F1] Change to Auto')

Status = ttk.Label(T1, textvariable=v_status)
Status.place(x=20, y=470)

# Tab2


v_sell_coin = StringVar()  # เก็บข้อมูลใน gui
v_sell_coin.set('BTCUSDT')
ET21 = ttk.Entry(T2, textvariable=v_sell_coin, font=FONT1, width=15)
ET21.pack(pady=10)

v_sell_amount = StringVar()  # เก็บข้อมูลใน gui
v_sell_amount.set('1')
ET22 = ttk.Entry(T2, textvariable=v_sell_amount, font=FONT1, width=15)
ET22.pack(pady=10)

v_sell_price = StringVar()  # เก็บข้อมูลใน gui
v_sell_price.set('54321')
ET23 = ttk.Entry(T2, textvariable=v_sell_price, font=FONT1, width=15)
ET23.pack(pady=10)

BSell = ttk.Button(T2, text='Sell')
BSell.pack(pady=50, ipadx=20, ipady=10)

GUI.mainloop()
