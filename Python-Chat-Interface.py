from tkinter import *
import time
import re
import os
import string
import webbrowser

saved_username = ["You"]

# checks if username file exists, if not, makes one.
if not os.path.isfile("usernames.txt"):
    # doesnt exist, creates usernames.txt file
    print('"username.txt" file doesn\'t exist. Creating new file.')
    with open ("usernames.txt", 'wb') as file:
        pass
else:
    # file exists, takes all existing usernames stored in file and adds them to saved_username list
    print('"username.txt" file found.')
    with open("usernames.txt", 'r') as file:
        for line in file:
            saved_username.append(line.replace("\n", ""))
    pass


class ChatInterface(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        # sets default bg for top level windows
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 10"

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

        # username
        username = Menu(options, tearoff=0)
        options.add_cascade(label="Username", menu=username)
        username.add_command(label="Change Username", command=self.change_username)
        username.add_command(label="Default Username", command=self.default_username)
        username.add_command(label="View Username History", command=self.view_username_history)
        username.add_command(label="Clear Username History", command=self.clear_username_history)

        options.add_separator()

        # font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default", command=self.font_change_default)
        font.add_command(label="Times", command=self.font_change_times)
        font.add_command(label="System", command=self.font_change_system)
        font.add_command(label="Helvetica", command=self.font_change_helvetica)
        font.add_command(label="Fixedsys", command=self.font_change_fixedsys)

        # color theme
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Color Theme", menu=color_theme)
        color_theme.add_command(label="Default", command=self.color_theme_default)
        color_theme.add_command(label="Night", command=self.color_theme_dark)
        color_theme.add_command(label="Grey", command=self.color_theme_grey)
        color_theme.add_command(label="Blue", command=self.color_theme_dark_blue)
        color_theme.add_command(label="Pink", command=self.color_theme_pink)
        color_theme.add_command(label="Turquoise", command=self.color_theme_turquoise)
        color_theme.add_command(label="Hacker", command=self.color_theme_hacker)

        # all to default
        options.add_command(label="Default layout", command=self.default_format)

        options.add_separator()

        # default window size
        options.add_command(label="Default Window Size", command=self.default_window_size)

    # Help
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
        help_option.add_command(label="Features", command=self.features_msg)
        help_option.add_command(label="About", command=self.about_msg)
        help_option.add_command(label="Source Code", command=self.src_code_msg)

    # Chat interface
        # frame containing text box with messages and scrollbar
        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # contains messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        # self.users_message = self.entry_field.get()

        # frame containing send button and emoji button
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        # send button
        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message(None), activebackground="#FFFFFF",
                                  activeforeground="#000000")
        self.send_button.pack(side=LEFT, ipady=2)
        self.master.bind("<Return>", self.send_message_event)

        # emoticons
        self.emoji_button = Button(self.send_button_frame, text="☺", width=2, relief=GROOVE, bg='white',
                                   bd=1, command=self.emoji_options, activebackground="#FFFFFF",
                                   activeforeground="#000000")
        self.emoji_button.pack(side=RIGHT, padx=6, pady=6, ipady=2)

        self.last_sent_label(date="No messages sent.")

    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)

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
        saved = "Chat log saved to {}\n".format(new_name)

        # saves chat log file
        try:
            with open(new_name, 'w')as file:
                self.text_box.configure(state=NORMAL)
                log = self.text_box.get(1.0, END)
                file.write(log)
                self.text_box.insert(END, saved)
                self.text_box.see(END)
                self.text_box.configure(state=DISABLED)

        except UnicodeEncodeError:
            # displays error when trying to save chat with unicode. (fix in future)
            self.error_window("Unfortunately this chat can't be saved as of this \nversion "
                              "because it contains unicode characters.", type="simple_error", height='100')

    # clears chat
    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.last_sent_label(date="No messages sent.")
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

# Help functions
    def features_msg(self):
        msg_box = Toplevel()
        msg_box.configure(bg=self.tl_bg)

    def about_msg(self):
        about_message = "This is a chat interface created in " \
                        "Python by me, Jorge Soderberg. I started this " \
                        "project to help continue to grow my skills " \
                        "in python, especially with larger, more " \
                        "complex class based programs. This is my " \
                        "largest project with a UI so far. There are " \
                        "still many features I would like to add in " \
                        "the future."
        self.error_window(about_message, type="simple_error", height='140')

    def src_code_msg(self):
        webbrowser.open('https://github.com/Josode/Python-Chat-Interface')

# creates top level window with error message
    def error_window(self, error_msg, type="simple_error", height='100', button_msg="Okay"):
        # try's to destroy change username window if its an error with username content
        try:
            self.change_username_window.destroy()
        except AttributeError:
            pass

        # makes top level with placement relative to root and specified error msg
        self.error_window_tl = Toplevel(bg=self.tl_bg)
        self.error_window_tl.focus_set()
        self.error_window_tl.grab_set()

        # gets main window width and height to position change username window
        half_root_width = root.winfo_x()
        half_root_height = root.winfo_y() + 60
        placement = '400x' + str(height) + '+' + str(int(half_root_width)) + '+' + str(int(half_root_height))
        self.error_window_tl.geometry(placement)

        too_long_frame = Frame(self.error_window_tl, bd=5, bg=self.tl_bg)
        too_long_frame.pack()

        self.error_scrollbar = Scrollbar(too_long_frame, bd=0)
        self.error_scrollbar.pack(fill=Y, side=RIGHT)

        error_text = Text(too_long_frame, font=self.font, bg=self.tl_bg, fg=self.tl_fg, wrap=WORD, relief=FLAT,
                          height=round(int(height)/30), yscrollcommand=self.error_scrollbar.set)
        error_text.pack(pady=6, padx=6)
        error_text.insert(INSERT, error_msg)
        error_text.configure(state=DISABLED)
        self.error_scrollbar.config(command=self.text_box.yview)

        button_frame = Frame(too_long_frame, width=12)
        button_frame.pack()

        okay_button = Button(button_frame, relief=GROOVE, bd=1, text=button_msg, font=self.font, bg=self.tl_bg,
                             fg=self.tl_fg, activebackground=self.tl_bg, width=5, height=1,
                             activeforeground=self.tl_fg, command=lambda: self.close_error_window(type))
        okay_button.pack(side=LEFT, padx=5)

        if type == "username_history_error":
            cancel_button = Button(button_frame, relief=GROOVE, bd=1, text="Cancel", font=self.font, bg=self.tl_bg,
                             fg=self.tl_fg, activebackground=self.tl_bg, width=5, height=1,
                             activeforeground=self.tl_fg, command=lambda: self.close_error_window("simple_error"))
            cancel_button.pack(side=RIGHT, padx=5)

# Send Message

    # allows user to hit enter instead of button to change username
    def change_username_main_event(self, event):
        saved_username.append(self.username_entry.get())
        self.change_username_main(username=saved_username[-1])

        # gets passed username from input

    def change_username_main(self, username, default=False):

        # takes saved_username list and writes all usernames into text file
        def write_usernames():
            with open('usernames.txt', 'w') as filer:
                for item in saved_username:
                    filer.write(item + "\n")

        # ensures username contains only letters and numbers
        found = False
        for char in username:
            if char in string.punctuation:
                found = True

        if found is True:
            saved_username.remove(username)
            self.error_window("Your username must contain only letters and numbers.", type="username_error",
                              height='100')
        # username length limiter (limits to 20 characters or less and greater than 1 character)
        elif len(username) > 20:
            saved_username.remove(username)
            self.error_window("Your username must be 20 characters or less.", type="username_error", height='100')

        elif len(username) < 2:
            saved_username.remove(username)
            self.error_window("Your username must be 2 characters or more.", type="username_error", height='100')

        # detects if user entered already current username
        elif len(saved_username) >= 2 and username == saved_username[-2]:
            self.error_window("That is already your current username!", type="username_error", height='100')

        # used to detect when user wants default username.
        else:
            # closes change username window, adds username to list, and displays notification
            self.close_username_window()
            write_usernames()
            self.send_message_insert("Username changed to " + '"' + username + '".')

    # allows "enter" key for sending msg
    def send_message_event(self, event):
        user_name = saved_username[-1]
        self.send_message(user_name)

    # joins username with message into publishable format
    def send_message(self, username):

        user_input = self.entry_field.get()

        username = saved_username[-1] + ": "
        message = (username, user_input)
        readable_msg = ''.join(message)
        readable_msg.strip('{')
        readable_msg.strip('}')

        # clears entry field, passes formatted msg to send_message_insert
        if user_input != '':
            self.entry_field.delete(0, END)
            self.send_message_insert(readable_msg)

    # inserts user input into text box
    def send_message_insert(self, message):
        # tries to close emoji window if its open. If not, passes
        try:
            self.close_emoji()

        except AttributeError:
            pass

        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, message + '\n')
        self.last_sent_label(str(time.strftime( "Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
        self.text_box.see(END)
        self.text_box.configure(state=DISABLED)

    # closes change username window
    def close_username_window(self):
        self.change_username_window.destroy()

    # decides type of error when i create an error window ( re-open change username window or not)
    def close_error_window(self, type):
        if type == "username_error":
            self.error_window_tl.destroy()
            self.change_username()
        elif type == "simple_error":
            self.error_window_tl.destroy()
        elif type == "username_history_error":
            self.error_window_tl.destroy()
            self.clear_username_history_confirmed()
        else:
            print("Ya dingus jorge, you gave an unknown error type.")

# enter emoticons
    def emoji_options(self):
        # makes top level window positioned to the right and at the bottom of root window
        self.emoji_selection_window = Toplevel(bg=self.tl_bg, )
        self.emoji_selection_window.bind("<Return>", self.send_message_event)
        selection_frame = Frame(self.emoji_selection_window, bd=4, bg=self.tl_bg)
        selection_frame.grid()
        self.emoji_selection_window.focus_set()
        self.emoji_selection_window.grab_set()

        close_frame = Frame(self.emoji_selection_window)
        close_frame.grid(sticky=S)
        close_button = Button(close_frame, text="Close", font="Verdana 9", relief=GROOVE, bg=self.tl_bg,
                              fg=self.tl_fg, activebackground=self.tl_bg,
                              activeforeground=self.tl_fg, command=self.close_emoji)
        close_button.grid(sticky=S)

        root_width = root.winfo_width()
        root_pos_x = root.winfo_x()
        root_pos_y = root.winfo_y()
        selection_width_x = self.emoji_selection_window.winfo_reqwidth()
        selection_height_y = self.emoji_selection_window.winfo_reqheight()

        position = '180x320' + '+' + str(root_pos_x+root_width) + '+' + str(root_pos_y)
        self.emoji_selection_window.geometry(position)
        self.emoji_selection_window.minsize(180, 320)
        self.emoji_selection_window.maxsize(180, 320)

        emoticon_1 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☺",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("☺"), relief=GROOVE, bd=0)
        emoticon_1.grid(column=1, row=0, ipadx=5, ipady=5)
        emoticon_2 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☻",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("☻"), relief=GROOVE, bd=0)
        emoticon_2.grid(column=2, row=0, ipadx=5, ipady=5)
        emoticon_3 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☹",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("☹"), relief=GROOVE, bd=0)
        emoticon_3.grid(column=3, row=0, ipadx=5, ipady=5)
        emoticon_4 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="♡",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("♡"), relief=GROOVE, bd=0)
        emoticon_4.grid(column=4, row=0, ipadx=5, ipady=5)

        emoticon_5 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="♥",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("♥"), relief=GROOVE, bd=0)
        emoticon_5.grid(column=1, row=1, ipadx=5, ipady=5)
        emoticon_6 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="♪",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("♪"), relief=GROOVE, bd=0)
        emoticon_6.grid(column=2, row=1, ipadx=5, ipady=5)
        emoticon_7 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❀",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("❀"), relief=GROOVE, bd=0)
        emoticon_7.grid(column=3, row=1, ipadx=5, ipady=5)
        emoticon_8 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❁",
                            activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("❁"), relief=GROOVE, bd=0)
        emoticon_8.grid(column=4, row=1, ipadx=5, ipady=5)

        emoticon_9 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✼",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("✼"), relief=GROOVE, bd=0)
        emoticon_9.grid(column=1, row=2, ipadx=5, ipady=5)
        emoticon_10 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☀",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☀"), relief=GROOVE, bd=0)
        emoticon_10.grid(column=2, row=2, ipadx=5, ipady=5)
        emoticon_11 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✌",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✌"), relief=GROOVE, bd=0)
        emoticon_11.grid(column=3, row=2, ipadx=5, ipady=5)
        emoticon_12 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✊",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✊"), relief=GROOVE, bd=0)
        emoticon_12.grid(column=4, row=2, ipadx=5, ipady=5)

        emoticon_13 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✋",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✋"), relief=GROOVE, bd=0)
        emoticon_13.grid(column=1, row=3, ipadx=5, ipady=5)
        emoticon_14 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☃",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☃"), relief=GROOVE, bd=0)
        emoticon_14.grid(column=2, row=3, ipadx=5, ipady=5)
        emoticon_15 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❄",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❄"), relief=GROOVE, bd=0)
        emoticon_15.grid(column=3, row=3, ipadx=5, ipady=5)
        emoticon_16 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☕",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☕"), relief=GROOVE, bd=0)
        emoticon_16.grid(column=4, row=3, ipadx=5, ipady=5)

        emoticon_17 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="☂",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☂"), relief=GROOVE, bd=0)
        emoticon_17.grid(column=1, row=4, ipadx=5, ipady=5)
        emoticon_18 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="★",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("★"), relief=GROOVE, bd=0)
        emoticon_18.grid(column=2, row=4, ipadx=5, ipady=5)
        emoticon_19 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❎",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❎"), relief=GROOVE, bd=0)
        emoticon_19.grid(column=3, row=4, ipadx=5, ipady=5)
        emoticon_20 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❓",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❓"), relief=GROOVE, bd=0)
        emoticon_20.grid(column=4, row=4, ipadx=5, ipady=5)

        emoticon_21 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="❗",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❗"), relief=GROOVE, bd=0)
        emoticon_21.grid(column=1, row=5, ipadx=5, ipady=5)
        emoticon_22 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✔",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✔"), relief=GROOVE, bd=0)
        emoticon_22.grid(column=2, row=5, ipadx=5, ipady=5)
        emoticon_23 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✏",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✏"), relief=GROOVE, bd=0)
        emoticon_23.grid(column=3, row=5, ipadx=5, ipady=5)
        emoticon_24 = Button(selection_frame, bg=self.tl_bg, fg=self.tl_fg, text="✨",
                             activebackground=self.tl_bg, activeforeground=self.tl_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✨"), relief=GROOVE, bd=0)
        emoticon_24.grid(column=4, row=5, ipadx=5, ipady=5)

    def send_emoji(self, emoticon):
        self.entry_field.insert(END, emoticon)
        # following line would close emoji toplevel windwo, only allowing 1 emoji per opening of window
        # self.close_emoji()

    def close_emoji(self):
        self.emoji_selection_window.destroy()


# Font options
    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

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
        self.font = "helvetica 10"

    def font_change_fixedsys(self):
        self.text_box.config(font="fixedsys")
        self.entry_field.config(font="fixedsys")
        self.font = "fixedsys"

# Color theme options
    # Default
    def color_theme_default(self):
        self.master.config(bg="#EEEEEE")
        self.text_frame.config(bg="#EEEEEE")
        self.entry_frame.config(bg="#EEEEEE")
        self.text_box.config(bg="#FFFFFF", fg="#000000")
        self.entry_field.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#EEEEEE")
        self.send_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.emoji_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.sent_label.config(bg="#EEEEEE", fg="#000000")

        self.tl_bg = "#FFFFFF"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"

    # Dark
    def color_theme_dark(self):
        self.master.config(bg="#2a2b2d")
        self.text_frame.config(bg="#2a2b2d")
        self.text_box.config(bg="#212121", fg="#FFFFFF")
        self.entry_frame.config(bg="#2a2b2d")
        self.entry_field.config(bg="#212121", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#2a2b2d")
        self.send_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#2a2b2d", fg="#FFFFFF")

        self.tl_bg = "#212121"
        self.tl_bg2 = "#2a2b2d"
        self.tl_fg = "#FFFFFF"

    # Grey
    def color_theme_grey(self):
        self.master.config(bg="#444444")
        self.text_frame.config(bg="#444444")
        self.text_box.config(bg="#4f4f4f", fg="#ffffff")
        self.entry_frame.config(bg="#444444")
        self.entry_field.config(bg="#4f4f4f", fg="#ffffff", insertbackground="#ffffff")
        self.send_button_frame.config(bg="#444444")
        self.send_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        self.emoji_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        self.sent_label.config(bg="#444444", fg="#ffffff")

        self.tl_bg = "#4f4f4f"
        self.tl_bg2 = "#444444"
        self.tl_fg = "#ffffff"

    # Blue
    def color_theme_dark_blue(self):
        self.master.config(bg="#263b54")
        self.text_frame.config(bg="#263b54")
        self.text_box.config(bg="#1c2e44", fg="#FFFFFF")
        self.entry_frame.config(bg="#263b54")
        self.entry_field.config(bg="#1c2e44", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#263b54")
        self.send_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#263b54", fg="#FFFFFF")

        self.tl_bg = "#1c2e44"
        self.tl_bg2 = "#263b54"
        self.tl_fg = "#FFFFFF"

    # Pink
    def color_theme_pink(self):
        self.master.config(bg="#ffc1f2")
        self.text_frame.config(bg="#ffc1f2")
        self.text_box.config(bg="#ffe8fa", fg="#000000")
        self.entry_frame.config(bg="#ffc1f2")
        self.entry_field.config(bg="#ffe8fa", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#ffc1f2")
        self.send_button.config(bg="#ffe8fa", fg="#000000", activebackground="#ffe8fa", activeforeground="#000000")
        self.emoji_button.config(bg="#ffe8fa", fg="#000000", activebackground="#ffe8fa", activeforeground="#000000")
        self.sent_label.config(bg="#ffc1f2", fg="#000000")

        self.tl_bg = "#ffe8fa"
        self.tl_bg2 = "#ffc1f2"
        self.tl_fg = "#000000"

    # Turquoise
    def color_theme_turquoise(self):
        self.master.config(bg="#003333")
        self.text_frame.config(bg="#003333")
        self.text_box.config(bg="#669999", fg="#FFFFFF")
        self.entry_frame.config(bg="#003333")
        self.entry_field.config(bg="#669999", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#003333")
        self.send_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#003333", fg="#FFFFFF")

        self.tl_bg = "#669999"
        self.tl_bg2 = "#003333"
        self.tl_fg = "#FFFFFF"

    # Hacker
    def color_theme_hacker(self):
        self.master.config(bg="#0F0F0F")
        self.text_frame.config(bg="#0F0F0F")
        self.entry_frame.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#33FF33")
        self.entry_field.config(bg="#0F0F0F", fg="#33FF33", insertbackground="#33FF33")
        self.send_button_frame.config(bg="#0F0F0F")
        self.send_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#0F0F0F", fg="#33FF33")

        self.tl_bg = "#0F0F0F"
        self.tl_bg2 = "#0F0F0F"
        self.tl_fg = "#33FF33"

    # Default font and color theme
    def default_format(self):
        self.font_change_default()
        self.color_theme_default()

# Change Username
    def change_username(self):
        self.change_username_window = Toplevel()
        self.change_username_window.bind("<Return>", self.change_username_main_event)
        self.change_username_window.configure(bg=self.tl_bg)
        self.change_username_window.focus_set()
        self.change_username_window.grab_set()

        # gets main window width and height to position change username window
        half_root_width = root.winfo_x()+100
        half_root_height = root.winfo_y()+60
        placement = '180x70' + '+' + str(int(half_root_width)) + '+' + str(int(half_root_height))
        self.change_username_window.geometry(placement)

        # frame for entry field
        enter_username_frame = Frame(self.change_username_window, bg=self.tl_bg)
        enter_username_frame.pack(pady=5)

        self.username_entry = Entry(enter_username_frame, width=22, bg=self.tl_bg, fg=self.tl_fg, bd=1,
                      insertbackground=self.tl_fg)
        self.username_entry.pack(pady=3, padx=10)

        # Frame for Change button and cancel button
        buttons_frame = Frame(self.change_username_window, bg=self.tl_bg)
        buttons_frame.pack()

        change_button = Button(buttons_frame, relief=GROOVE, text="Change", width=8, bg=self.tl_bg, bd=1,
                        fg=self.tl_fg, activebackground=self.tl_bg, activeforeground=self.tl_fg,
                        command=lambda: self.change_username_main(self.username_entry.get()))
        change_button.pack(side=LEFT, padx=4, pady=3)

        cancel_button = Button(buttons_frame, relief=GROOVE, text="Cancel", width=8, bg=self.tl_bg, bd=1,
                               fg=self.tl_fg, command=self.close_username_window,
                               activebackground=self.tl_bg, activeforeground=self.tl_fg)
        cancel_button.pack(side=RIGHT, padx=4, pady=3)

# Use default username ("You")
    def default_username(self):
        saved_username.append("You")
        self.send_message_insert("Username changed to default.")

# promps user to Clear username history (deletes usernames.txt file and clears saved_username list)
    def clear_username_history(self):
        self.error_window(error_msg="Are you sure you want to clear your username history?\n", button_msg="Clear",
                          type="username_history_error", height="120")

    def clear_username_history_confirmed(self):
         os.remove("usernames.txt")
         saved_username.clear()
         saved_username.append("You")

         self.send_message_insert("Username history cleared.")

# opens window showing username history (possible temp feature)
    def view_username_history(self):
        with open("usernames.txt", 'r') as usernames:
            view_usernames = str(usernames.readlines())

        view_usernames = re.sub("[\[\]']", "", view_usernames)
        view_usernames = view_usernames.replace("\\n", "")

        self.error_window(error_msg="Username History: \n\n" + view_usernames, type="simple_error",
                          button_msg="Close", height='150')

# Default Window Size
    def default_window_size(self):
        root.geometry('400x300')

        # scrolls to very bottom of textbox
        def see_end():
            self.text_box.configure(state=NORMAL)
            self.text_box.see(END)
            self.text_box.configure(state=DISABLED)
        root.after(10, see_end)

root = Tk()
root.title("Chat GUI")
root.minsize(400,200)
root.geometry('400x300')

a = ChatInterface(root)

root.mainloop()
