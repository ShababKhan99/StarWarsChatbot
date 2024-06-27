from tkinter import *
from customtkinter import *
import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

PRI_COLOR = ("#4a4d32", "#cacdb2")
SEC_COLOR = ("#9abc9e", "#436547")
ACC_COLOR = ("#5f9174", "#6ea083")
BG_COLOR = ("#f4f5ef", "#0f100a")
TEXT_COLOR = ("#1a1c12", "#ebede3")

options = [
    str("Darth Maul"),
    str("Obi Wan Kenobi"),
    str("Master Yoda"),
    str("Anakin Skywalker"),
    str("Boba Fett"),
]

chat_log = [{"role": "system",
            "content": "You are Darth Maul, speaking to the user through a Sith Holocron. You must act accordingly."}]


class App:
    def __init__(self):
        super().__init__()
        set_appearance_mode("system")
        self.window = CTk()
        self.window.geometry("950x750")
        self.FONT = CTkFont(family="Helvetica", size=14)
        self.FONT_BOLD = CTkFont(family="Helvetica", size=14, weight='bold')

        self.bot_select = StringVar()
        self.bot_select.set(options[0])
        self.theme_switch_var = StringVar(value="off")
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Star Wars Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.geometry("950x750")

        self.window.columnconfigure((0, 1, 2), weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=15)
        self.window.rowconfigure(2, weight=1)

        # Header
        head_label = CTkLabel(
            self.window,
            fg_color="transparent",
            text_color=TEXT_COLOR,
            text="Welcome to the Star Wars Chatbot",
            font=self.FONT_BOLD
        )
        head_label.grid(row=0, column=1, pady=10, sticky="new")

        # Bot Select Combo box
        self.drop_down = CTkComboBox(
            self.window,
            variable=self.bot_select,
            values=options,
            fg_color=ACC_COLOR,
            dropdown_fg_color=ACC_COLOR,
            border_color=SEC_COLOR,
            button_color=SEC_COLOR,
            command=self._selected
        )
        self.drop_down.grid(row=0, column=2, pady=15, padx=25, sticky="ne")

        # Light/Dark Mode switch
        self.theme_switch = CTkSwitch(
            self.window,
            text="",
            command=self.switch_event,
            variable=self.theme_switch_var,
            onvalue="on",
            offvalue="off",
            progress_color="#5f9174"
        )
        self.theme_switch.grid(row=0, column=0, padx=25, pady=10, sticky="nw")

        # Text box
        self.text_box = CTkTextbox(
            self.window,
            width=910,
            height=2,
            corner_radius=10,
            border_spacing=5,
            font=self.FONT,
            fg_color=BG_COLOR,
            text_color=TEXT_COLOR,
            scrollbar_button_color=ACC_COLOR,
            activate_scrollbars=TRUE,
            wrap='word',
            state=DISABLED,
        )
        self.text_box.configure(cursor="arrow")
        self.text_box.grid(row=1, column=0, columnspan=3, sticky="ns")

        bottom_label = CTkLabel(
            self.window,
            text=""
        )
        bottom_label.grid(row=2, column=0, columnspan=3, sticky="ns")
        bottom_label.rowconfigure(0, weight=1)
        bottom_label.columnconfigure((0, 1), weight=10)
        bottom_label.columnconfigure(2, weight=3)

        # Message Entry
        self.message_entry = CTkEntry(
            bottom_label,
            width=810,
            height=110,
            corner_radius=10,
            fg_color=PRI_COLOR,
            text_color=SEC_COLOR,
            font=self.FONT
        )
        self.message_entry.grid(
            row=0, column=0, columnspan=2, pady=8, sticky="nw")
        self.message_entry.focus()
        self.message_entry.bind("<Return>", self._on_enter_pressed)

        # Send Button
        self.send_button = CTkButton(
            bottom_label,
            height=110,
            width=100,
            text="GO",
            font=self.FONT,
            text_color=PRI_COLOR,
            fg_color=SEC_COLOR,
            command=lambda: self._on_enter_pressed(None)
        )
        self.send_button.grid(row=0, column=2, pady=8, sticky="ne")

    def switch_event(self):
        if self.theme_switch_var.get() == "on":
            set_appearance_mode("light")
        elif self.theme_switch_var.get() == "off":
            set_appearance_mode("dark")
        else:
            print("incorrect")
            print(self.theme_switch_var)

    def _selected(self, event):
        self.text_box.configure(state=NORMAL)
        self.text_box.delete('1.0', 'end')
        self.text_box.configure(state=DISABLED)
        self.change_bot(self.bot_select.get())

    def _on_enter_pressed(self, event):
        msg = self.message_entry.get()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.message_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, msg1)
        self.text_box.configure(state=DISABLED)

        self.message_entry.delete(0, END)
        msg2 = f"{self.bot_select.get()}: {self.get_response(msg)}\n\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, msg2)
        self.text_box.configure(state=DISABLED)

        self.text_box.see(END)

    def change_bot(self, text):
        if text == options[0]:
            chat_log.clear()
            chat_log.append({"role": "system",
                            "content": "You are Darth Maul, speaking to the user through a Sith Holocron. You must act accordingly."})
        elif text == options[1]:
            chat_log.clear()
            chat_log.append({"role": "system",
                            "content": "You are Obi Wan Kenobi, speaking to the user through a Jedi Holocron. You must act accordingly."})
        elif text == options[2]:
            chat_log.clear()
            chat_log.append({"role": "system",
                            "content": "You are Master Yoda, speaking to the user through a Jedi Holocron. You must act accordingly."})
        elif text == options[3]:
            chat_log.clear()
            chat_log.append({"role": "system",
                            "content": "You are Anakin Skywalker, but after he was redeemed by Luke Skywalker, and freed of the dark side. You are speaking to the user through a Jedi Holocron. You must act accordingly."})
        elif text == options[4]:
            chat_log.clear()
            chat_log.append({"role": "system",
                            "content": "You are Boba Fett, speaking to the user through an network connection and computer. You must act accordingly."})
        else:
            print(f"Incorrect choice. {text} is not in choices")

    def get_response(self, text):
        chat_log.append({"role": "user", "content": text})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_log,
        )
        assistant_response = response.choices[0].message.content
        assistant_response = assistant_response.strip('\n').strip()
        chat_log.append({"role": "assistant", "content": assistant_response})

        return assistant_response


class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self.bot_select = StringVar()
        self.bot_select.set(options[0])
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Star Wars Character chats")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=950, height=750, bg=PRI_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome To A Star Wars Chatbot", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # divider
        line = Label(self.window, width=450, bg=PRI_COLOR)
        line.place(relwidth=1, rely=0.07, relheight=0.12)

        # text widget
        self.text_box = Text(self.window, width=20, height=2,
                             bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=15, pady=5)
        self.text_box.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_box.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_box)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_box.yview)

        # bottom label
        bottom_label = Label(self.window, bg=PRI_COLOR, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # bot choice dropdown
        self.drop = OptionMenu(
            bottom_label, self.bot_select, *options, command=self._selected)
        self.drop.place(relwidth=1)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50",
                               fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06,
                             rely=0.035, relx=0.11)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Send",
                             font=FONT_BOLD, width=20, bg=PRI_COLOR, command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.035, relheight=0.06, relwidth=0.22)


if __name__ == "__main__":
    app = App()
    app.run()
