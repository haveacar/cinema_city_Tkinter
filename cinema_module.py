import pathlib
import sys
from tkinter import *
import datetime
from tkinter import messagebox
from tkinter.ttk import Combobox, Style
import json

if __name__ == '__main__':
    sys.exit()
CONFIG_FILE = pathlib.Path(__file__).parent.joinpath('config.json')


class Cinama(Tk):
    """
        Cinema Class
        """

    def __init__(self) -> None:
        super().__init__()

        self.hall_boxes = []
        self.lbl_num_list = []
        self.order = 0
        self.index_order = ""
        self.film_name = "WONDER WOMEN - 19:00"
        self.blue_zone_price = 60
        self.green_zone_price = 90

        # validation numer
        self.vcmd = (self.register(self.validate), '%P')

        # frames
        self.top_frame = Frame(bg='#1E90FF')
        self.top_frame.grid(column=0, row=0)
        self.hall_frame = Frame(bg='#1E90FF')
        self.hall_frame.grid(column=0, row=1)
        self.pay_frame = Frame(bg='#1E90FF', padx=5)
        self.pay_frame.grid(column=1, row=1)
        self.botton_frame = Frame(bg='#1E90FF')
        self.botton_frame.grid(column=0, row=2, pady=10)

        # Display set up
        self.title("Cinema City")
        self.geometry("1000x1200+10+100")
        self.config(bg='#1E90FF')

        # pay_frame
        self.name_cinema = Label(self.pay_frame, text=self.film_name, font=('Comic Sans MS', 30, "bold"), fg='#1E90FF',
                                 bg='yellow')
        self.name_cinema.pack(anchor=S, pady=5)

        Label(self.pay_frame, text="Price:", font=('Comic Sans MS', 25, "bold"), fg='white', bg='#1E90FF').pack(
            anchor=S, pady=5)
        self.green_zone = Label(self.pay_frame, text=f"Green Zone - {self.green_zone_price} NIS",
                                font=('Comic Sans MS', 25), bg="green", fg='white')
        self.green_zone.pack(anchor=W, pady=5)

        self.blue_zone = Label(self.pay_frame, text=f"Blue Zone - {self.blue_zone_price} NIS",
                               font=('Comic Sans MS', 25), bg="#0000FF", fg='white')
        self.blue_zone.pack(anchor=W, pady=5)

        # order labels

        self.ord_l = Label(self.pay_frame, text="Telephone:", font=('Comic Sans MS', 15), fg='white', bg='#1E90FF')
        self.ord_l.pack(anchor=W, pady=5)
        self.ord_tel_entry = Entry(self.pay_frame, validate='key', validatecommand=self.vcmd)
        self.ord_tel_entry.pack(anchor=W, pady=5)

        # order
        self.order_label = Label(self.pay_frame, text=f"Order: 0", font=('Comic Sans MS', 15), fg='white', bg='#1E90FF')
        self.order_label.pack(anchor=W, pady=5)
        self.places_label = Label(self.pay_frame, text=f"Place: 0", font=('Comic Sans MS', 15), fg='white',
                                  bg='#1E90FF')
        self.places_label.pack(anchor=W, pady=5)
        self.bth_buy = Button(self.pay_frame, text="Sell", height=3, width=8, command=self.sell_push)
        self.bth_buy.pack(anchor=W, pady=5)

    def start(self) -> None:
        """Start func displays Labels, read config file, generate combo Box """

        # date now
        time_l = datetime.date.today()
        # top buttons
        Label(self.top_frame, text=time_l, font=('Comic Sans MS', 15, "bold"), fg='white', bg='#1E90FF').pack(side=LEFT,
                                                                                                              pady=5,
                                                                                                              anchor=W)
        Button(self.top_frame, text="New Order", height=3, width=5, activeforeground="green",
               command=self.new_order).pack(side=LEFT)
        Button(self.top_frame, text="SET UP", height=3, width=5, activeforeground="green",
               command=self.set_up).pack(side=LEFT)

        Label(self.botton_frame, text="©Daniel Govnir", font=('Comic Sans MS', 10, "bold"), fg='white',
              bg='#1E90FF').pack(side=LEFT,
                                 pady=5, anchor=W)

        try:
            with open(CONFIG_FILE) as f:
                halls_from_file = json.load(f)

        except:
            messagebox.showwarning("Information window", "Not found config file")

        def get_hall_selection(e) -> None:
            """
            :param e: e.widget
            """
            for h in halls_from_file:
                if h.get('name') == halls_combo.get():
                    self.rows = int(h.get("rows"))
                    self.places = int(h.get("places"))
                    self.hall_name = h.get("name")

            if self.hall_boxes != 0: self.remove_hall()

            self.create_hall()

        hall_names = [hall.get("name") for hall in halls_from_file]
        combo_style = Style()
        combo_style.configure('combo1.TCombobox')
        hall_names.insert(0, "Select hall from dropdown list")
        halls_combo = Combobox(
            self.top_frame,
            values=hall_names,
            width=30,
            height=10,
            font=("Times New Roman", 15), style="combo1.TCombobox")
        halls_combo.bind("<<ComboboxSelected>>", get_hall_selection)
        halls_combo.set(value=hall_names[0])
        halls_combo.pack(side=LEFT)

        self.mainloop()

    def create_hall(self) -> None:
        """ Generate check buttons on frame"""

        for i in range(self.rows):
            row = []
            if i in list(range(3, 7)):
                back_grn = "green"
            else:
                back_grn = "#0000FF"
            for j in range(self.places):
                btn = Checkbutton(master=self.hall_frame,

                                  indicatoron=0,
                                  text=j + 1,
                                  padx=3,
                                  pady=3,
                                  height=3,
                                  width=5,
                                  activebackground='red',
                                  disabledforeground="yellow",
                                  selectcolor="yellow",
                                  background=back_grn,
                                  foreground="white",
                                  font=('Comic Sans MS', 11, 'bold'),
                                  command=lambda row=i, col=j: self.check_button_click(row, col))

                lbl_num = Label(master=self.hall_frame, text=i + 1, height=3, width=5, bg='#000080')
                btn.grid(column=j, row=i)
                lbl_num.grid(row=i, column=11)
                row.append(btn)
                self.lbl_num_list.append(lbl_num)
            self.hall_boxes.append(row)

    def remove_hall(self) -> None:
        """Func cleans lists, remove buttons"""
        # del check buttons
        for row in self.hall_boxes:
            for chk_btn in row: chk_btn.destroy()

        # del number labels
        for next_label in self.lbl_num_list:   next_label.destroy()

        # del lists, values
        self.hall_boxes = []
        self.lbl_num_list = []
        self.order = 0
        self.index_order = ""
        self.order_label.config(text=f"Order: {self.order} NIS")
        self.places_label.config(text=f"Places: {self.index_order}")

    def check_button_click(self, r, c) -> None:
        """Func checks click, cost, price, checkbutton click"""

        self.hall_boxes[r][c].config(state="disabled")
        if self.hall_boxes[r][c].cget("background") == 'green':
            price_v = self.green_zone_price
        else:
            price_v = self.blue_zone_price
        index = f"{r + 1}:{c + 1}"

        self.calculate_order(price_v, index)

        # print(self.hall_boxes[r][c].cget('variable'))

    def calculate_order(self, price, index_btn_check) -> None:
        self.index_order += index_btn_check + ", "
        self.order += price
        self.order_label.config(text=f"Order: {self.order} NIS")
        self.places_label.config(text=f"Places: {self.index_order}")

    def sell_push(self):

        telephone = 0

        telephone = self.ord_tel_entry.get()
        print(telephone)
        print(self.order)
        print(self.index_order)

    def validate(self, new_value) -> str | int:
        """
        telephone validation function
        :param new_value: string Entry()
        :return: "" or int
        """
        return new_value == "" or new_value.isnumeric()

    def new_order(self) -> None:
        """
        func clean variables
        """
        self.order = 0
        self.index_order = ""
        self.order_label.config(text=f"Order: {self.order} NIS")
        self.places_label.config(text=f"Places: {self.index_order}")

    def set_up(self) -> None:
        """
        create Top_level windows, Labels, Buttons
        """

        def set_up_text(w_entry, label_out, text=''):
            """
            func get and set up widgets

            :param w_entry: widget Entry
            :param label_out: widget Label
            :param text: str
            """
            text_g = w_entry.get()
            if len(text) > 1:  # to change price ticket
                label_out.config(text=f'{text} {text_g} NIS')
                # blue zone
                if text.split(" ")[0] == "Blue":
                    self.blue_zone_price = int(text_g)
                # green zone
                else:
                    self.green_zone_price = int(text_g)

            else:  # to change name film
                label_out.config(text=text_g)

        # create window
        set_up_window = Toplevel(background="green")
        set_up_window.title("Admin Page")
        set_up_window.geometry("500x200")
        set_up_window.attributes('-topmost', 1)

        # set up film name
        Label(set_up_window, text='Change Film Name').grid(column=0, row=0)
        change_film_entry = Entry(set_up_window)
        change_film_entry.grid(column=1, row=0)
        Button(set_up_window, text='Set up', command=lambda: set_up_text(change_film_entry, self.name_cinema)).grid(
            column=2, row=0)

        # set up blue zone price
        Label(set_up_window, text='Change Blue Zone price').grid(column=0, row=1)
        change_blue_entry = Entry(set_up_window, validate='key', validatecommand=self.vcmd)
        change_blue_entry.grid(column=1, row=1)
        Button(set_up_window, text='Set up',
               command=lambda: set_up_text(change_blue_entry, self.blue_zone, text="Blue Zone - ")).grid(column=2,
                                                                                                         row=1)

        # set up Green zone price
        Label(set_up_window, text='Change Green Zone price').grid(column=0, row=2)
        change_green_entry = Entry(set_up_window, validate='key', validatecommand=self.vcmd)
        change_green_entry.grid(column=1, row=2)
        Button(set_up_window, text='Set up',
               command=lambda: set_up_text(change_green_entry, self.green_zone, text="Green Zone - ")).grid(column=2,
                                                                                                            row=2)
