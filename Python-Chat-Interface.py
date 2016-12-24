from tkinter import *
import time
import os

saved_username = ["you"]


class ChatInterface(Frame):

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
        font.add_command(label="Fixedsys", command=self.font_change_fixedsys)

        # color theme
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Color Theme", menu=color_theme)
        color_theme.add_command(label="Default", command=self.color_theme_default)
        color_theme.add_command(label="Night", command=self.color_theme_dark)
        color_theme.add_command(label="Dark Blue", command=self.color_theme_dark_blue)
        color_theme.add_command(label="Hacker", command=self.color_theme_hacker)

        # all to default
        options.add_command(label="Default layout", command=self.default_format)

        options.add_separator()

        # change username
        options.add_command(label="Change Username", command=self.change_username)

    # Help
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
        help_option.add_command(label="Features", command=self.features_msg)
        help_option.add_command(label="About", command=self.about_msg)
        help_option.add_command(label="Source Code", command=self.src_code_msg)

        # sets default bg for top level windows
        self.top_level_bg = "#EEEEEE"
        self.top_level_fg = "#000000"
        self.font = "Verdana 10"

    # Chat interface
        # frame containing text box with messages and scrollbar
        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # displays messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.master, bd=0)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(side=BOTTOM, fill=X, padx=6, pady=6)
        # self.users_message = self.entry_field.get()

        # frame containing send button and emoji button
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(side=BOTTOM, fill=BOTH)

        # send button
        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message(None), activebackground="#FFFFFF",
                                  activeforeground="#000000")
        self.send_button.pack(side=LEFT)
        self.master.bind("<Return>", self.send_message_event)

        # emoticons
        self.emoji_button = Button(self.send_button_frame, text="☺", width=2, relief=GROOVE, bg='white',
                                   bd=1, command=self.emoji_options, activebackground="#FFFFFF",
                                   activeforeground="#000000")
        self.emoji_button.pack(side=RIGHT, padx=6, pady=6)

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
            save_error = Toplevel(bg=self.top_level_bg)

            def close():
                save_error.destroy()

            error_frame = Frame(save_error, bd=10, background=self.top_level_bg)
            error_frame.pack()
            error_message = Label(error_frame, text="Unfortunately this chat can't be\n saved because it "
                                                    "contains\n unicode characters.", font='Verdana 10',
                                  bg=self.top_level_bg, fg=self.top_level_fg, activebackground=self.top_level_bg,
                                  activeforeground=self.top_level_fg)
            error_message.pack()

            okay = Button(error_frame, text="Okay", font='Verdana 10', command=close, bg=self.top_level_bg,
                          fg=self.top_level_fg, activebackground=self.top_level_bg, activeforeground=self.top_level_fg)
            okay.pack(side=BOTTOM)

    # clears chat
    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

# Help functions
    def features_msg(self):
        msg_box = Toplevel()
        msg_box.configure(bg=self.top_level_bg)

    def about_msg(self):
        msg_box = Toplevel()
        msg_box.configure(bg=self.top_level_bg)

    def src_code_msg(self):
        msg_box = Toplevel()
        msg_box.configure(bg=self.top_level_bg)

# Send Message

    # allows "enter" key for sending msg
    def send_message_event(self, event):
        user_name = saved_username[-1]
        self.send_message(user_name)

    # formats user input for displaying using most recently set username
    # TO DO: add "username changed to (name)" message and enter key event
    def send_message(self, username):
        if username is None:
            username = saved_username[-1]
        # username length limiter (limits to 20 characters or less)
        if len(username) > 20:
            # creates top level window with error message
            self.change_username_window.destroy()
            self.too_long = Toplevel()
            self.too_long.focus_set()
            self.too_long.grab_set()

            # gets main window width and height to position change username window
            half_root_width = root.winfo_x()
            half_root_height = root.winfo_y() + 60
            placement = '400x70' + '+' + str(int(half_root_width)) + '+' + str(int(half_root_height))
            self.too_long.geometry(placement)

            too_long_frame = Frame(self.too_long, bd=10, bg=self.top_level_bg)
            too_long_frame.pack()
            error_label = Label(too_long_frame, text="Your username must be 20 characters or less.", font=self.font,
                                bg=self.top_level_bg, fg=self.top_level_fg)
            error_label.pack()
            okay_button = Button(too_long_frame, relief=GROOVE, bd=1, text="Okay", font=self.font, bg=self.top_level_bg,
                                 fg=self.top_level_fg, activebackground=self.top_level_bg,
                                 activeforeground=self.top_level_fg, command=self.close_too_long_window)
            okay_button.pack()

        user_input = self.entry_field.get()

        if username != "you":
            self.close_username_window()
        # adds username to list and makes current username most recently added on list
        saved_username.append(username)
        # joins username with message and formats to being readable
        username = saved_username[-1] + ": "
        message = (username, user_input, '\n')
        readable_msg = ''.join(message)
        readable_msg.strip('{')
        readable_msg.strip('}')

        # clears entry field, passes formatted msg to send_message_you
        if user_input != '':
            self.entry_field.delete(0, END)
            self.send_message_you(readable_msg)

    # inserts user input into text box
    def send_message_you(self, message):
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, message)
        self.text_box.see(END)
        self.text_box.configure(state=DISABLED)

# enter emoticons
    def emoji_options(self):
        self.selection = Toplevel(bg=self.top_level_bg, )
        self.selection.bind("<Return>", self.send_message_event)
        selection_frame = Frame(self.selection, bd=4, bg=self.top_level_bg)
        selection_frame.grid()
        self.selection.focus_set()
        self.selection.grab_set()

        close_frame = Frame(self.selection)
        close_frame.grid(sticky=S)
        close_button = Button(close_frame, text="Close", font="Verdana 9", relief=GROOVE, bg=self.top_level_bg,
                              fg=self.top_level_fg, activebackground=self.top_level_bg,
                              activeforeground=self.top_level_fg, command=self.close_emoji)
        close_button.grid(sticky=S)

        root_width = root.winfo_width()
        root_height = root.winfo_height()
        root_pos_x = root.winfo_x()
        root_pos_y = root.winfo_y()
        selection_width_x = self.selection.winfo_reqwidth()
        selection_height_y = self.selection.winfo_reqheight()

        position = '180x320' + '+' + str(root_pos_x+root_width) + '+' + str(root_pos_y)
        self.selection.geometry(position)
        self.selection.minsize(180, 320)
        self.selection.maxsize(180, 320)

        emoticon_1 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="☺",
                            activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("☺"), relief=GROOVE, bd=0)
        emoticon_1.grid(column=1, row=0, ipadx=5, ipady=5)
        emoticon_2 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="☻",
                            activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("☻"), relief=GROOVE, bd=0)
        emoticon_2.grid(column=2, row=0, ipadx=5, ipady=5)
        emoticon_3 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="☹",
                            activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("☹"), relief=GROOVE, bd=0)
        emoticon_3.grid(column=3, row=0, ipadx=5, ipady=5)
        emoticon_4 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="♡",
                            activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("♡"), relief=GROOVE, bd=0)
        emoticon_4.grid(column=4, row=0, ipadx=5, ipady=5)

        emoticon_5 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="♥",
                            activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("♥"), relief=GROOVE, bd=0)
        emoticon_5.grid(column=1, row=1, ipadx=5, ipady=5)
        emoticon_6 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="♪",
                            activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("♪"), relief=GROOVE, bd=0)
        emoticon_6.grid(column=2, row=1, ipadx=5, ipady=5)
        emoticon_7 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="❀",
                            activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("❀"), relief=GROOVE, bd=0)
        emoticon_7.grid(column=3, row=1, ipadx=5, ipady=5)
        emoticon_8 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="❁",
                            activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("❁"), relief=GROOVE, bd=0)
        emoticon_8.grid(column=4, row=1, ipadx=5, ipady=5)

        emoticon_9 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="✼",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                            font='Verdana 14', command=lambda: self.send_emoji("✼"), relief=GROOVE, bd=0)
        emoticon_9.grid(column=1, row=2, ipadx=5, ipady=5)
        emoticon_10 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="☀",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☀"), relief=GROOVE, bd=0)
        emoticon_10.grid(column=2, row=2, ipadx=5, ipady=5)
        emoticon_11 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="✌",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✌"), relief=GROOVE, bd=0)
        emoticon_11.grid(column=3, row=2, ipadx=5, ipady=5)
        emoticon_12 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="✊",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✊"), relief=GROOVE, bd=0)
        emoticon_12.grid(column=4, row=2, ipadx=5, ipady=5)

        emoticon_13 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="✋",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✋"), relief=GROOVE, bd=0)
        emoticon_13.grid(column=1, row=3, ipadx=5, ipady=5)
        emoticon_14 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="☃",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☃"), relief=GROOVE, bd=0)
        emoticon_14.grid(column=2, row=3, ipadx=5, ipady=5)
        emoticon_15 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="❄",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❄"), relief=GROOVE, bd=0)
        emoticon_15.grid(column=3, row=3, ipadx=5, ipady=5)
        emoticon_16 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="☕",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☕"), relief=GROOVE, bd=0)
        emoticon_16.grid(column=4, row=3, ipadx=5, ipady=5)

        emoticon_17 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="☂",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("☂"), relief=GROOVE, bd=0)
        emoticon_17.grid(column=1, row=4, ipadx=5, ipady=5)
        emoticon_18 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="★",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("★"), relief=GROOVE, bd=0)
        emoticon_18.grid(column=2, row=4, ipadx=5, ipady=5)
        emoticon_19 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="❎",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❎"), relief=GROOVE, bd=0)
        emoticon_19.grid(column=3, row=4, ipadx=5, ipady=5)
        emoticon_20 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="❓",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❓"), relief=GROOVE, bd=0)
        emoticon_20.grid(column=4, row=4, ipadx=5, ipady=5)

        emoticon_21 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="❗",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("❗"), relief=GROOVE, bd=0)
        emoticon_21.grid(column=1, row=5, ipadx=5, ipady=5)
        emoticon_22 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="✔",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✔"), relief=GROOVE, bd=0)
        emoticon_22.grid(column=2, row=5, ipadx=5, ipady=5)
        emoticon_23 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="✏",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✏"), relief=GROOVE, bd=0)
        emoticon_23.grid(column=3, row=5, ipadx=5, ipady=5)
        emoticon_24 = Button(selection_frame, bg=self.top_level_bg, fg=self.top_level_fg, text="✨",
                             activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                             font='Verdana 14', command=lambda: self.send_emoji("✨"), relief=GROOVE, bd=0)
        emoticon_24.grid(column=4, row=5, ipadx=5, ipady=5)

    def send_emoji(self, emoticon):
        self.entry_field.insert(END, emoticon)
        self.close_emoji()

    def close_emoji(self):
        self.selection.destroy()


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

        self.top_level_bg = "#FFFFFF"
        self.top_level_fg = "#000000"

    # Dark Blue
    def color_theme_dark_blue(self):
        self.master.config(bg="#081B2D")
        self.text_frame.config(bg="#081B2D")
        self.text_box.config(bg="#13283C", fg="#FFFFFF")
        self.entry_frame.config(bg="#081B2D")
        self.entry_field.config(bg="#13283C", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#081B2D")
        self.send_button.config(bg="#13283C", fg="#FFFFFF", activebackground="#13283C", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#13283C", fg="#FFFFFF", activebackground="#13283C", activeforeground="#FFFFFF")

        self.top_level_bg = "#13283C"
        self.top_level_fg = "#FFFFFF"

    # Night
    def color_theme_dark(self):
        self.master.config(bg="#2E2E2E")
        self.text_frame.config(bg="#2E2E2E")
        self.text_box.config(bg="#171717", fg="#FFFFFF")
        self.entry_frame.config(bg="#2E2E2E")
        self.entry_field.config(bg="#171717", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#2E2E2E")
        self.send_button.config(bg="#171717", fg="#FFFFFF", activebackground="#171717", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#171717", fg="#FFFFFF", activebackground="#171717", activeforeground="#FFFFFF")

        self.top_level_bg = "#171717"
        self.top_level_fg = "#FFFFFF"

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

        self.top_level_bg = "#0F0F0F"
        self.top_level_fg = "#33FF33"

    # Default font and color theme
    def default_format(self):
        self.font_change_default()
        self.color_theme_default()

# Change Username
    def change_username(self):
        self.change_username_window = Toplevel()
        self.change_username_window.configure(bg=self.top_level_bg)
        self.change_username_window.focus_set()
        self.change_username_window.grab_set()

        # gets main window width and height to position change username window
        half_root_width = root.winfo_x()+100
        half_root_height = root.winfo_y()+60
        placement = '180x70' + '+' + str(int(half_root_width)) + '+' + str(int(half_root_height))
        self.change_username_window.geometry(placement)

        # frame for entry field
        enter_username_frame = Frame(self.change_username_window, bg=self.top_level_bg)
        enter_username_frame.pack(pady=5)

        entry = Entry(enter_username_frame, width=22, bg=self.top_level_bg, fg=self.top_level_fg, bd=1,
                      insertbackground=self.top_level_fg)
        entry.pack(pady=3, padx=10)

        # Frame for Change button and cancel button
        buttons_frame = Frame(self.change_username_window, bg=self.top_level_bg)
        buttons_frame.pack()

        change_button = Button(buttons_frame, relief=GROOVE, text="Change", width=8, bg=self.top_level_bg, bd=1,
                        fg=self.top_level_fg, activebackground=self.top_level_bg, activeforeground=self.top_level_fg,
                        command=lambda: self.send_message(username=entry.get()))
        change_button.pack(side=LEFT, padx=4, pady=3)

        cancel_button = Button(buttons_frame, relief=GROOVE, text="Cancel", width=8, bg=self.top_level_bg, bd=1,
                               fg=self.top_level_fg, command=self.close_username_window,
                               activebackground=self.top_level_bg, activeforeground=self.top_level_fg)
        cancel_button.pack(side=RIGHT, padx=4, pady=3)

    #closes change username window
    def close_username_window(self):
        self.change_username_window.destroy()

    # closes "username too long" error message and re-open's change username window
    def close_too_long_window(self):
        self.too_long.destroy()
        self.change_username()

root = Tk()
root.title("Chat GUI")
root.minsize(250,200)
root.geometry('400x300')

a = ChatInterface(root)

root.mainloop()
