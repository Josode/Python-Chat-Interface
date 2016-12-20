from tkinter import *
import time
import os


class PersonalAssistantGUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)
# Menu bar

    # File
        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file)
        file.add_command(label="Save Chat Log", command=self.save_chat)
        file.add_command(label="Clear Chat", command=self.clear_chat)
        file.add_separator()
        file.add_command(label="Exit", command=self.client_exit)

    # Options
        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options)

        # font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default", command=self.font_change_default)
        font.add_command(label="Times", command=self.font_change_times)
        font.add_command(label="System", command=self.font_change_system)
        font.add_command(label="Helvetica", command=self.font_change_helvetica)

        # color theme
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Color Theme", menu=color_theme)
        color_theme.add_command(label="Default", command=self.color_theme_default)
        color_theme.add_command(label="Night", command=self.color_theme_dark)
        color_theme.add_command(label="Dark Blue", command=self.color_theme_dark_blue)
        color_theme.add_command(label="Hacker", command=self.color_theme_hacker)

        # all to default
        options.add_command(label="Default layout", command=self.default_format)

    # Help
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
        help_option.add_command(label="Features", command=self.features_msg)
        help_option.add_command(label="About", command=self.about_msg)
        help_option.add_command(label="Source Code", command=self.src_code_msg)

        # sets default bg for help windows
        self.help_window_color = "#EEEEEE"
        self.font = "Verdana"

    # Chat interface
        # frame containing text box with messages and scrollbar
        self.text_frame = Frame(self.master, bd=8)
        self.text_frame.pack(fill=BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=BOTH, side=RIGHT)

        # displays messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=5, pady=5, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE)
        # text_box.insert(INSERT, "Testing")
        self.text_box.pack(fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.master, bd=8)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=BOTH)
        # self.users_message = self.entry_field.get()

        # frame containing send button
        self.send_button_frame = Frame(self.master, bd=5)
        self.send_button_frame.pack(side=RIGHT, fill=BOTH)

        # send button
        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=self.send_message)
        self.send_button.pack(fill=BOTH)
        self.master.bind("<Return>", self.send_message_event)

# File functions
    def client_exit(self):
        exit()

    def save_chat(self):
        # creates unique name for chat log file
        time_file = str(time.strftime('%X %x'))
        remove = ":/ "
        for var in remove:
            time_file = time_file.replace(var, "_")

        # gets current directory of program. creates "logs" folder to store chat logs.
        path = os.getcwd() + "\\logs\\"
        new_name = path + "log_" + time_file
        saved = "Chat log saved to {}".format(new_name)

        # saves chat log file
        self.text_box.configure(state=NORMAL)
        log = self.text_box.get(1.0, END)
        with open(new_name, 'w')as file:
            file.write(log)
            self.text_box.insert(INSERT, saved)
            self.text_box.see(END)
        self.text_box.configure(state=DISABLED)

    # clears chat
    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.text_box.delete(1.0, END)
        self.text_box.see(END)
        self.text_box.config(state=DISABLED)

# Help functions
    def features_msg(self):
        msg_box = Toplevel()
        msg_box.configure(bg=self.help_window_color)

    def about_msg(self):
        msg_box = Toplevel()
        msg_box.configure(bg=self.help_window_color)

    def src_code_msg(self):
        msg_box = Toplevel()
        msg_box.configure(bg=self.help_window_color)

    # inserts user input into text box
    def send_message_you(self, message):
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(INSERT, message)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)

    # allows "enter" key for sending msg
    def send_message_event(self, event):
        self.send_message()

    # formats user input for displaying
    def send_message(self):
        you = "You: "

        user_input = self.entry_field.get()
        message = (you , user_input, '\n')
        readable_msg = ''.join(message)
        readable_msg.strip('{')
        readable_msg.strip('}')
        self.entry_field.delete(0, END)

        if user_input != '':
            self.send_message_you(readable_msg)

# Font options
    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana"

    def font_change_times(self):
        self.text_box.config(font="Times")
        self.entry_field.config(font="Times")
        self.font = "Times"

    def font_change_system(self):
        self.text_box.config(font="System")
        self.entry_field.config(font="System")
        self.font = "System"

    def font_change_helvetica(self):
        self.text_box.config(font="helvetica 10")
        self.entry_field.config(font="helvetica 10")
        self.font = "helvetica"

# Color theme options
    # Default
    def color_theme_default(self):
        self.master.config(bg="#EEEEEE")
        self.text_frame.config(bg="#EEEEEE")
        self.entry_frame.config(bg="#EEEEEE")
        self.text_box.config(bg="#FFFFFF", fg="#000000")
        self.entry_field.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#EEEEEE")
        self.send_button.config(bg="#EEEEEE", fg="#000000")

        self.help_window_color = "#FFFFFF"

    # Dark Blue
    def color_theme_dark_blue(self):
        self.master.config(bg="#081B2D")
        self.text_frame.config(bg="#081B2D")
        self.text_box.config(bg="#13283C", fg="#FFFFFF")
        self.entry_frame.config(bg="#081B2D")
        self.entry_field.config(bg="#13283C", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#081B2D")
        self.send_button.config(bg="#13283C", fg="#FFFFFF", activebackground="#13283C", activeforeground="#FFFFFF")

        self.help_window_color = "#13283C"

    # Night
    def color_theme_dark(self):
        self.master.config(bg="#2E2E2E")
        self.text_frame.config(bg="#2E2E2E")
        self.text_box.config(bg="#171717", fg="#FFFFFF")
        self.entry_frame.config(bg="#2E2E2E")
        self.entry_field.config(bg="#171717", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#2E2E2E")
        self.send_button.config(bg="#171717", fg="#FFFFFF")

        self.help_window_color = "#171717"

    # Hacker
    def color_theme_hacker(self):
        self.master.config(bg="#0F0F0F")
        self.text_frame.config(bg="#0F0F0F")
        self.entry_frame.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#33FF33")
        self.entry_field.config(bg="#0F0F0F", fg="#33FF33", insertbackground="#33FF33")
        self.send_button_frame.config(bg="#0F0F0F")
        self.send_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")

        self.help_window_color = "#0F0F0F"

    # Default font and color theme
    def default_format(self):
        self.font_change_default()
        self.color_theme_default()


root = Tk()
root.geometry()
root.title("Chat GUI")

a = PersonalAssistantGUI(root)

root.mainloop()
