from tkinter import *
from customtkinter import *
import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

BG_GRAY = "#ABB2B9"
BG_COLOR = "#56445D"
TEXT_COLOR = "#C8C6AF"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

options = [
    str("Darth Maul"),
    str("Obi Wan Kenobi"),
    str("Master Yoda"),
    str("Anakin Skywalker"),
    str("Boba Fett"),
]

chat_log = []


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
        self.window.configure(width=470, height=750, bg=BG_GRAY)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome To A Star Wars Chatbot", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.12)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2,
                                bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=15, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
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
                             font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.035, relheight=0.06, relwidth=0.22)

    def _selected(self, event):
        self.text_widget.configure(state=NORMAL)
        self.text_widget.delete('1.0', 'end')
        self.text_widget.configure(state=DISABLED)
        self.change_bot(self.bot_select.get())

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        self.msg_entry.delete(0, END)
        msg2 = f"{self.bot_select.get()}: {self.get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)

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
            print(text.lower().replace(" ", "").strip())
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


if __name__ == "__main__":
    app = ChatApplication()
    app.run()
