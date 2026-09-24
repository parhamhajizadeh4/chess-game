import tkinter as tk
import random
import time
from copy import deepcopy


# =====================================================
# WINDOW
# =====================================================

window = tk.Tk()
window.title("Chess")
window.geometry("800x600")
window.configure(bg="#202124")

content_frame = tk.Frame(
    window,
    bg="#202124"
)
content_frame.pack(
    fill="both",
    expand=True
)

welcome_label = None
current_game = None


# =====================================================
# PLAYER
# =====================================================

player_plan = "Free Plan"

SHOP_PLANS = {
    "Plus": 160,
    "PRO": 500,
    "Premium": 700
}

selected_shop_plan = None


# =====================================================
# CHESS DATA
# =====================================================

SYMBOLS = {
    ("white", "king"): "\u2654",
    ("white", "queen"): "\u2655",
    ("white", "rook"): "\u2656",
    ("white", "bishop"): "\u2657",
    ("white", "knight"): "\u2658",
    ("white", "pawn"): "\u2659",

    ("black", "king"): "\u265A",
    ("black", "queen"): "\u265B",
    ("black", "rook"): "\u265C",
    ("black", "bishop"): "\u265D",
    ("black", "knight"): "\u265E",
    ("black", "pawn"): "\u265F"
}


PIECE_VALUES = {
    "pawn": 100,
    "knight": 320,
    "bishop": 330,
    "rook": 500,
    "queen": 900,
    "king": 20000
}


# =====================================================
# BOT PROGRESS
# =====================================================

completed_levels = set()
current_level_unlocked = 1


def is_level_unlocked(level):
    return level <= current_level_unlocked


def complete_level(level):
    global current_level_unlocked

    completed_levels.add(level)

    if level == current_level_unlocked:
        if level < 10:
            current_level_unlocked += 1


# =====================================================
# START POSITION
# =====================================================

def starting_position():

    return {
        (0, 0): ("black", "rook"),
        (0, 1): ("black", "knight"),
        (0, 2): ("black", "bishop"),
        (0, 3): ("black", "queen"),
        (0, 4): ("black", "king"),
        (0, 5): ("black", "bishop"),
        (0, 6): ("black", "knight"),
        (0, 7): ("black", "rook"),

        (1, 0): ("black", "pawn"),
        (1, 1): ("black", "pawn"),
        (1, 2): ("black", "pawn"),
        (1, 3): ("black", "pawn"),
        (1, 4): ("black", "pawn"),
        (1, 5): ("black", "pawn"),
        (1, 6): ("black", "pawn"),
        (1, 7): ("black", "pawn"),

        (6, 0): ("white", "pawn"),
        (6, 1): ("white", "pawn"),
        (6, 2): ("white", "pawn"),
        (6, 3): ("white", "pawn"),
        (6, 4): ("white", "pawn"),
        (6, 5): ("white", "pawn"),
        (6, 6): ("white", "pawn"),
        (6, 7): ("white", "pawn"),

        (7, 0): ("white", "rook"),
        (7, 1): ("white", "knight"),
        (7, 2): ("white", "bishop"),
        (7, 3): ("white", "queen"),
        (7, 4): ("white", "king"),
        (7, 5): ("white", "bishop"),
        (7, 6): ("white", "knight"),
        (7, 7): ("white", "rook")
    }


# =====================================================
# MAIN PAGE
# =====================================================

def show_main_page():

    global welcome_label

    for widget in content_frame.winfo_children():
        widget.destroy()

    welcome_label = tk.Label(
        content_frame,
        text="",
        font=("Arial", 28, "bold"),
        bg="#202124",
        fg="white"
    )

    welcome_label.pack(pady=100)

    text = "Welcome to Chess! \u265F"

    def type_text(index=0):

        if welcome_label is None:
            return

        if not welcome_label.winfo_exists():
            return

        welcome_label.config(
            text=text[:index]
        )

        if index <= len(text):
            window.after(
                70,
                type_text,
                index + 1
            )

    type_text()


def hide_welcome():

    global welcome_label

    if welcome_label is not None:

        try:
            welcome_label.destroy()
        except:
            pass

        welcome_label = None


# =====================================================
# ACTIVE MENU
# =====================================================

def set_active(active_button):

    buttons = [
        profile,
        chat,
        game,
        top_players,
        shop
    ]

    for button in buttons:

        button.config(
            font=("Arial", 12),
            fg="black"
        )

    active_button.config(
        font=("Arial", 12, "bold"),
        fg="#7C4DFF"
    )


# =====================================================
# GAME MENU
# =====================================================

def close_game_menu():
    game_menu.place_forget()


def open_game():

    hide_welcome()
    close_game_menu()
    set_active(game)

    # Hide Profile / Sign Up / other current pages when entering Game.
    for widget in content_frame.winfo_children():
        widget.destroy()

    if game_menu.winfo_ismapped():
        game_menu.place_forget()
    else:
        game_menu.place(
            relx=0.5,
            rely=0.42,
            anchor="center"
        )


# =====================================================
# OTHER MENUS
# =====================================================

def open_profile():

    hide_welcome()
    close_game_menu()

    for widget in content_frame.winfo_children():
        widget.destroy()

    set_active(profile)
    show_profile_page()


# =====================================================
# PROFILE / ACCOUNT
# =====================================================

profile_data = {
    "logged_in": False,
    "name": "",
    "age": "",
    "bio": "",
    "level": "",
    "contact": "",
    "picture": None
}

verification_attempts = 0
verification_code = None
verification_timer_job = None
verification_seconds = 0
signup_picture_label = None


def clear_profile_page():
    for widget in content_frame.winfo_children():
        widget.destroy()


def show_profile_page():

    clear_profile_page()

    frame = tk.Frame(
        content_frame,
        bg="#202124"
    )
    frame.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        frame,
        text="Profile",
        font=("Arial", 25, "bold"),
        bg="#202124",
        fg="white"
    ).pack(pady=(35, 12))

    avatar = tk.Label(
        frame,
        text=profile_data["picture"] if profile_data["picture"] else "👤",
        font=("Arial", 48),
        width=4,
        height=2,
        bg="#303134",
        fg="white",
        relief="solid",
        bd=1
    )
    avatar.pack(pady=8)

    if profile_data["logged_in"]:
        name = profile_data["name"] or "User"
        tk.Label(
            frame,
            text=name,
            font=("Arial", 17, "bold"),
            bg="#202124",
            fg="white"
        ).pack(pady=5)

        buttons = tk.Frame(frame, bg="#202124")
        buttons.pack(pady=12)

        tk.Button(
            buttons,
            text="Profile Details",
            font=("Arial", 12, "bold"),
            width=16,
            command=show_profile_details
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Log Out",
            font=("Arial", 12, "bold"),
            width=12,
            command=logout_user
        ).pack(side="left", padx=5)

    else:
        buttons = tk.Frame(frame, bg="#202124")
        buttons.pack(pady=14)

        tk.Button(
            buttons,
            text="Login",
            font=("Arial", 12, "bold"),
            width=13,
            command=show_login_page
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Sign Up",
            font=("Arial", 12, "bold"),
            width=13,
            command=show_signup_step_one
        ).pack(side="left", padx=5)

        tk.Label(
            frame,
            text="You can play without an account, but some features are limited.",
            font=("Arial", 10),
            bg="#202124",
            fg="#BDBDBD",
            wraplength=520
        ).pack(pady=8)


def profile_back():
    show_profile_page()


def profile_picture_choice():
    choice = tk.Toplevel(window)
    choice.title("Profile Picture")
    choice.configure(bg="#202124")
    choice.transient(window)
    choice.grab_set()

    tk.Label(
        choice,
        text="Choose a profile picture",
        font=("Arial", 15, "bold"),
        bg="#202124",
        fg="white"
    ).pack(pady=12)

    ready = ["👤", "♟", "♞", "♜", "♛", "♚"]
    row = tk.Frame(choice, bg="#202124")
    row.pack(padx=15, pady=8)

    for picture in ready:
        tk.Button(
            row,
            text=picture,
            font=("Arial", 28),
            width=3,
            command=lambda p=picture: choose_profile_picture(p, choice)
        ).pack(side="left", padx=4)

    tk.Button(
        choice,
        text="Upload Image",
        font=("Arial", 11, "bold"),
        command=lambda: upload_profile_picture(choice)
    ).pack(pady=10)


def choose_profile_picture(picture, window_to_close):
    profile_data["picture"] = picture
    window_to_close.destroy()
    if signup_picture_label is not None and signup_picture_label.winfo_exists():
        signup_picture_label.config(text=picture)


def upload_profile_picture(window_to_close):
    from tkinter import filedialog
    path = filedialog.askopenfilename(
        title="Choose Profile Picture",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif"),
            ("All files", "*.*")
        ]
    )

    if path:
        # The actual image file is selected now.
        # Image rendering can be connected with Pillow later.
        profile_data["picture"] = "📷"
        window_to_close.destroy()
        if signup_picture_label is not None and signup_picture_label.winfo_exists():
            signup_picture_label.config(text="📷")


def show_signup_step_one():
    global signup_picture_label

    clear_profile_page()

    frame = tk.Frame(content_frame, bg="#202124")
    frame.pack(fill="both", expand=True)

    tk.Button(
        frame,
        text="Back",
        font=("Arial", 11, "bold"),
        command=show_profile_page
    ).place(x=20, y=15)

    tk.Label(
        frame,
        text="Create Account",
        font=("Arial", 23, "bold"),
        bg="#202124",
        fg="white"
    ).pack(pady=(35, 8))

    tk.Label(
        frame,
        text="Step 1 of 2",
        font=("Arial", 10),
        bg="#202124",
        fg="#BDBDBD"
    ).pack(pady=2)

    form = tk.Frame(frame, bg="#202124")
    form.pack(pady=10)

    picture_frame = tk.Frame(form, bg="#202124")
    picture_frame.grid(row=0, column=0, columnspan=2, pady=5)

    signup_picture_label = tk.Label(
        picture_frame,
        text=profile_data["picture"] if profile_data["picture"] else "👤",
        font=("Arial", 32),
        width=4,
        height=1,
        bg="#303134",
        fg="white"
    )
    signup_picture_label.pack(side="left", padx=5)

    tk.Button(
        picture_frame,
        text="Choose Picture *",
        font=("Arial", 10, "bold"),
        command=profile_picture_choice
    ).pack(side="left", padx=5)

    tk.Label(
        form,
        text="Name and Family Name *",
        font=("Arial", 10, "bold"),
        bg="#202124",
        fg="white"
    ).grid(row=1, column=0, sticky="e", padx=5, pady=5)

    name_entry = tk.Entry(form, width=27, font=("Arial", 11))
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(
        form,
        text="Age",
        font=("Arial", 10, "bold"),
        bg="#202124",
        fg="white"
    ).grid(row=2, column=0, sticky="e", padx=5, pady=5)

    age_entry = tk.Spinbox(
        form,
        from_=7,
        to=53,
        width=25,
        font=("Arial", 11)
    )
    age_entry.delete(0, "end")
    age_entry.insert(0, "7")
    age_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(
        form,
        text="Bio",
        font=("Arial", 10, "bold"),
        bg="#202124",
        fg="white"
    ).grid(row=3, column=0, sticky="ne", padx=5, pady=5)

    bio_entry = tk.Text(form, width=27, height=3, font=("Arial", 10))
    bio_entry.grid(row=3, column=1, padx=5, pady=5)

    if player_plan == "Free Plan":
        bio_entry.config(state="disabled")
        bio_note = "Bio is available for paid plans."
    else:
        bio_note = ""

    tk.Label(
        form,
        text=bio_note,
        font=("Arial", 8),
        bg="#202124",
        fg="#FFB74D"
    ).grid(row=4, column=1, sticky="w", padx=5)

    tk.Label(
        form,
        text="Game Level *",
        font=("Arial", 10, "bold"),
        bg="#202124",
        fg="white"
    ).grid(row=5, column=0, sticky="e", padx=5, pady=5)

    level_var = tk.StringVar(value="")
    level_menu = tk.OptionMenu(
        form,
        level_var,
        "Beginner",
        "Basic",
        "Intermediate",
        "Professional",
        "Superstar"
    )
    level_menu.config(width=22, font=("Arial", 10))
    level_menu.grid(row=5, column=1, sticky="w", padx=5, pady=5)

    error_label = tk.Label(
        frame,
        text="",
        font=("Arial", 9),
        bg="#202124",
        fg="#EF5350",
        wraplength=500
    )
    error_label.pack(pady=4)

    def next_step():
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        level = level_var.get().strip()

        if not profile_data["picture"]:
            error_label.config(text="Profile picture is required.")
            return

        if len(name) <= 6:
            error_label.config(text="Name and family name must contain more than 6 letters.")
            return

        if not all(("A" <= char <= "Z") or ("a" <= char <= "z") or ("0" <= char <= "9") or char == " " for char in name):
            error_label.config(text="Only English letters, numbers, and spaces are allowed.")
            return

        try:
            age_number = int(age)
        except ValueError:
            error_label.config(text="Please enter a valid age.")
            return

        if age_number < 7 or age_number > 53:
            error_label.config(text="Age must be between 7 and 53.")
            return

        if not level:
            error_label.config(text="Game level is required.")
            return

        profile_data["name"] = name
        profile_data["age"] = str(age_number)
        profile_data["level"] = level
        profile_data["bio"] = bio_entry.get("1.0", "end").strip() if player_plan != "Free Plan" else ""

        show_signup_step_two()

    tk.Button(
        frame,
        text="Next",
        font=("Arial", 12, "bold"),
        width=15,
        command=next_step
    ).pack(pady=5)


def show_signup_step_two():
    clear_profile_page()

    frame = tk.Frame(content_frame, bg="#202124")
    frame.pack(fill="both", expand=True)

    tk.Button(
        frame,
        text="Back",
        font=("Arial", 11, "bold"),
        command=show_signup_step_one
    ).place(x=20, y=15)

    tk.Label(
        frame,
        text="Verify Account",
        font=("Arial", 23, "bold"),
        bg="#202124",
        fg="white"
    ).pack(pady=(35, 8))

    tk.Label(
        frame,
        text="Step 2 of 2",
        font=("Arial", 10),
        bg="#202124",
        fg="#BDBDBD"
    ).pack(pady=2)

    form = tk.Frame(frame, bg="#202124")
    form.pack(pady=18)

    tk.Label(
        form,
        text="Phone Number or Email *",
        font=("Arial", 10, "bold"),
        bg="#202124",
        fg="white"
    ).grid(row=0, column=0, padx=5, pady=7)

    contact_entry = tk.Entry(form, width=28, font=("Arial", 11))
    contact_entry.grid(row=0, column=1, padx=5, pady=7)

    tk.Label(
        form,
        text="Verification Code *",
        font=("Arial", 10, "bold"),
        bg="#202124",
        fg="white"
    ).grid(row=1, column=0, padx=5, pady=7)

    code_entry = tk.Entry(form, width=28, font=("Arial", 11), show="•")
    code_entry.grid(row=1, column=1, padx=5, pady=7)

    send_button = tk.Button(
        form,
        text="Send Code",
        font=("Arial", 10, "bold"),
        command=lambda: send_verification_code(contact_entry, send_button, timer_label, error_label)
    )
    send_button.grid(row=1, column=2, padx=5, pady=7)

    timer_label = tk.Label(
        form,
        text="",
        font=("Arial", 9),
        bg="#202124",
        fg="#FFB74D"
    )
    timer_label.grid(row=2, column=1, columnspan=2, sticky="w", padx=5)

    error_label = tk.Label(
        frame,
        text="",
        font=("Arial", 9),
        bg="#202124",
        fg="#EF5350",
        wraplength=520
    )
    error_label.pack(pady=5)

    def finish_signup():
        if not contact_entry.get().strip():
            error_label.config(text="Phone number or email is required.")
            return

        if not code_entry.get().strip():
            error_label.config(text="Verification code is required.")
            return

        if verification_code is None:
            error_label.config(text="Please request a verification code first.")
            return

        if code_entry.get().strip() != verification_code:
            error_label.config(text="Invalid verification code.")
            return

        profile_data["contact"] = contact_entry.get().strip()
        profile_data["logged_in"] = True
        error_label.config(text="Account created successfully.", fg="#66BB6A")
        frame.after(700, show_profile_page)

    vip_var = tk.BooleanVar(value=False)

    vip_frame = tk.Frame(frame, bg="#202124")
    vip_frame.pack(pady=(2, 4))

    vip_check = tk.Checkbutton(
        vip_frame,
        text="Do you want to create a VIP account?",
        variable=vip_var,
        font=("Arial", 10, "bold"),
        bg="#202124",
        fg="white",
        activebackground="#202124",
        activeforeground="white",
        selectcolor="#303134"
    )
    vip_check.pack()

    vip_payment_label = tk.Label(
        frame,
        text="",
        font=("Arial", 9, "bold"),
        bg="#202124",
        fg="#FFD54F"
    )
    vip_payment_label.pack(pady=2)

    def update_vip_payment():
        if vip_var.get():
            vip_payment_label.config(text="VIP account: Pay 50 shillings to create your account.")
        else:
            vip_payment_label.config(text="")

    vip_var.trace_add("write", lambda *args: update_vip_payment())

    tk.Button(
        frame,
        text="Create Account",
        font=("Arial", 12, "bold"),
        width=18,
        command=finish_signup
    ).pack(pady=8)

    tk.Label(
        frame,
        text="SMS/email delivery will be connected when the real verification service is added.",
        font=("Arial", 8),
        bg="#202124",
        fg="#BDBDBD",
        wraplength=520
    ).pack(pady=5)


def send_verification_code(contact_entry, send_button, timer_label, error_label):
    global verification_attempts
    global verification_code
    global verification_seconds
    global verification_timer_job

    contact = contact_entry.get().strip()

    if not contact:
        error_label.config(text="Phone number or email is required.")
        return

    if verification_seconds > 0:
        return

    if verification_attempts >= 4:
        error_label.config(text="You cannot request another code for 24 hours.")
        send_button.config(state="disabled")
        return

    verification_attempts += 1
    verification_code = str(random.randint(100000, 999999))

    # Temporary local verification for development.
    # Real SMS/email delivery will be connected later.
    print("Verification code:", verification_code)

    error_label.config(
        text="Verification code sent.",
        fg="#66BB6A"
    )

    if verification_attempts == 1:
        verification_seconds = 0
        send_button.grid_remove()
        timer_label.config(text="Code sent.")
    elif verification_attempts == 2:
        start_verification_timer(60, send_button, timer_label)
    elif verification_attempts == 3:
        start_verification_timer(180, send_button, timer_label)
    elif verification_attempts == 4:
        start_verification_timer(300, send_button, timer_label)


def start_verification_timer(seconds, send_button, timer_label):
    global verification_seconds
    global verification_timer_job

    verification_seconds = seconds
    send_button.grid_remove()

    def tick():
        global verification_seconds
        global verification_timer_job

        minutes = verification_seconds // 60
        seconds_left = verification_seconds % 60

        timer_label.config(
            text=f"You can request another code in {minutes:02d}:{seconds_left:02d}"
        )

        if verification_seconds > 0:
            verification_seconds -= 1
            verification_timer_job = window.after(1000, tick)
        else:
            timer_label.config(text="You can request another code now.")
            send_button.grid()
            verification_timer_job = None

    tick()


def show_login_page():
    clear_profile_page()

    frame = tk.Frame(content_frame, bg="#202124")
    frame.pack(fill="both", expand=True)

    tk.Button(
        frame,
        text="Back",
        font=("Arial", 11, "bold"),
        command=show_profile_page
    ).place(x=20, y=15)

    tk.Label(
        frame,
        text="Login",
        font=("Arial", 24, "bold"),
        bg="#202124",
        fg="white"
    ).pack(pady=(55, 20))

    form = tk.Frame(frame, bg="#202124")
    form.pack()

    tk.Label(
        form,
        text="Phone Number or Email *",
        font=("Arial", 10, "bold"),
        bg="#202124",
        fg="white"
    ).grid(row=0, column=0, padx=5, pady=7)

    contact_entry = tk.Entry(form, width=28, font=("Arial", 11))
    contact_entry.grid(row=0, column=1, padx=5, pady=7)

    send_button = tk.Button(
        form,
        text="Send Code",
        font=("Arial", 10, "bold"),
        command=lambda: send_verification_code(contact_entry, send_button, timer_label, error_label)
    )
    send_button.grid(row=0, column=2, padx=5, pady=7)

    tk.Label(
        form,
        text="Verification Code *",
        font=("Arial", 10, "bold"),
        bg="#202124",
        fg="white"
    ).grid(row=1, column=0, padx=5, pady=7)

    code_entry = tk.Entry(form, width=28, font=("Arial", 11), show="•")
    code_entry.grid(row=1, column=1, padx=5, pady=7)

    timer_label = tk.Label(
        form,
        text="",
        font=("Arial", 9),
        bg="#202124",
        fg="#FFB74D"
    )
    timer_label.grid(row=2, column=1, sticky="w", padx=5)

    error_label = tk.Label(
        frame,
        text="",
        font=("Arial", 9),
        bg="#202124",
        fg="#EF5350"
    )
    error_label.pack(pady=8)

    def login():
        if not contact_entry.get().strip():
            error_label.config(text="Phone number or email is required.")
            return
        if not code_entry.get().strip():
            error_label.config(text="Verification code is required.")
            return
        if verification_code is None:
            error_label.config(text="Please request a verification code first.")
            return
        if code_entry.get().strip() != verification_code:
            error_label.config(text="Invalid verification code.")
            return

        profile_data["contact"] = contact_entry.get().strip()
        profile_data["logged_in"] = True
        error_label.config(text="Login successful.", fg="#66BB6A")
        frame.after(700, show_profile_page)

    tk.Button(
        frame,
        text="Login",
        font=("Arial", 12, "bold"),
        width=16,
        command=login
    ).pack(pady=5)


def show_profile_details():
    clear_profile_page()

    frame = tk.Frame(content_frame, bg="#202124")
    frame.pack(fill="both", expand=True)

    tk.Button(
        frame,
        text="Back",
        font=("Arial", 11, "bold"),
        command=show_profile_page
    ).place(x=20, y=15)

    tk.Label(
        frame,
        text="Profile Details",
        font=("Arial", 24, "bold"),
        bg="#202124",
        fg="white"
    ).pack(pady=(45, 20))

    details = (
        f"Name: {profile_data['name']}\n"
        f"Age: {profile_data['age']}\n"
        f"Game Level: {profile_data['level']}\n"
        f"Bio: {profile_data['bio'] or 'No bio'}\n"
        f"Plan: {player_plan}"
    )

    tk.Label(
        frame,
        text=details,
        font=("Arial", 13),
        bg="#202124",
        fg="white",
        justify="left"
    ).pack(pady=10)


def logout_user():
    global verification_code
    global verification_attempts
    global verification_seconds

    profile_data["logged_in"] = False
    profile_data["name"] = ""
    profile_data["age"] = ""
    profile_data["bio"] = ""
    profile_data["level"] = ""
    profile_data["contact"] = ""
    profile_data["picture"] = None
    verification_code = None
    verification_attempts = 0
    verification_seconds = 0

    show_profile_page()


# =====================================================
# CHAT
# =====================================================

chat_contacts = [
    "Chess Bot",
    "Chess Player",
    "Guest Player"
]

chat_messages = {
    "Chess Bot": [
        ("Chess Bot", "Welcome to Chess Chat!")
    ],
    "Chess Player": [
        ("Chess Player", "Hello! Ready to play?")
    ],
    "Guest Player": []
}

selected_chat = "Chess Bot"


def refresh_chat_messages(message_box):

    message_box.config(state="normal")
    message_box.delete("1.0", "end")

    for sender, message in chat_messages.get(selected_chat, []):
        message_box.insert(
            "end",
            f"{sender}:\n{message}\n\n"
        )

    message_box.config(state="disabled")
    message_box.see("end")


def select_chat(name, message_box, chat_list_frame):

    global selected_chat
    selected_chat = name

    for widget in chat_list_frame.winfo_children():
        if isinstance(widget, tk.Button):
            if widget.cget("text") == name:
                widget.config(
                    bg="#7C4DFF",
                    fg="white"
                )
            else:
                widget.config(
                    bg="#303134",
                    fg="white"
                )

    refresh_chat_messages(message_box)


def send_chat_message(entry, message_box):

    text = entry.get().strip()

    if not text:
        return

    chat_messages.setdefault(
        selected_chat,
        []
    ).append(("You", text))

    entry.delete(0, "end")
    refresh_chat_messages(message_box)


def filter_chat_list(search_var, chat_list_frame, message_box):

    query = search_var.get().strip().lower()

    for widget in chat_list_frame.winfo_children():
        widget.destroy()

    visible = [
        name for name in chat_contacts
        if query in name.lower()
    ]

    for name in visible:
        button = tk.Button(
            chat_list_frame,
            text=name,
            font=("Arial", 11, "bold"),
            anchor="w",
            bg=("#7C4DFF" if name == selected_chat else "#303134"),
            fg="white",
            relief="flat",
            padx=10,
            command=lambda n=name: select_chat(
                n,
                message_box,
                chat_list_frame
            )
        )
        button.pack(
            fill="x",
            pady=3
        )

    if not visible:
        tk.Label(
            chat_list_frame,
            text="No users found",
            font=("Arial", 10),
            bg="#202124",
            fg="#BDBDBD"
        ).pack(pady=10)


def show_chat_page():

    clear_profile_page()

    frame = tk.Frame(
        content_frame,
        bg="#202124"
    )
    frame.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=12
    )

    tk.Label(
        frame,
        text="Chat",
        font=("Arial", 25, "bold"),
        bg="#202124",
        fg="white"
    ).pack(pady=(8, 12))

    main = tk.Frame(
        frame,
        bg="#202124"
    )
    main.pack(
        fill="both",
        expand=True
    )

    left = tk.Frame(
        main,
        bg="#252525",
        width=210
    )
    left.pack(
        side="left",
        fill="y",
        padx=(0, 8)
    )
    left.pack_propagate(False)

    right = tk.Frame(
        main,
        bg="#252525"
    )
    right.pack(
        side="left",
        fill="both",
        expand=True
    )

    tk.Label(
        left,
        text="Conversations",
        font=("Arial", 13, "bold"),
        bg="#252525",
        fg="white"
    ).pack(pady=(10, 7))

    search_var = tk.StringVar()
    search_entry = tk.Entry(
        left,
        textvariable=search_var,
        font=("Arial", 10)
    )
    search_entry.pack(
        fill="x",
        padx=8,
        pady=(0, 8)
    )
    search_entry.insert(0, "")

    chat_list_frame = tk.Frame(
        left,
        bg="#252525"
    )
    chat_list_frame.pack(
        fill="both",
        expand=True,
        padx=8
    )

    tk.Label(
        right,
        text=selected_chat,
        font=("Arial", 15, "bold"),
        bg="#252525",
        fg="white"
    ).pack(
        anchor="w",
        padx=12,
        pady=10
    )

    message_box = tk.Text(
        right,
        font=("Arial", 11),
        bg="#303134",
        fg="white",
        insertbackground="white",
        wrap="word",
        state="disabled",
        relief="flat"
    )
    message_box.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=(0, 8)
    )

    send_frame = tk.Frame(
        right,
        bg="#252525"
    )
    send_frame.pack(
        fill="x",
        padx=10,
        pady=(0, 10)
    )

    message_entry = tk.Entry(
        send_frame,
        font=("Arial", 11)
    )
    message_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=7
    )

    tk.Button(
        send_frame,
        text="Send",
        font=("Arial", 10, "bold"),
        command=lambda: send_chat_message(
            message_entry,
            message_box
        )
    ).pack(
        side="left",
        padx=(6, 0),
        ipady=4
    )

    message_entry.bind(
        "<Return>",
        lambda event: send_chat_message(
            message_entry,
            message_box
        )
    )

    search_var.trace_add(
        "write",
        lambda *args: filter_chat_list(
            search_var,
            chat_list_frame,
            message_box
        )
    )

    # Remove the search placeholder when the user clicks it.
    search_entry.bind(
        "<FocusIn>",
        lambda event: (
            search_entry.delete(0, "end")
            if search_entry.get() == "Search..."
            else None
        )
    )

    filter_chat_list(
        search_var,
        chat_list_frame,
        message_box
    )
    refresh_chat_messages(message_box)


def open_chat():

    hide_welcome()
    close_game_menu()

    for widget in content_frame.winfo_children():
        widget.destroy()

    set_active(chat)
    show_chat_page()


def open_top_players():

    hide_welcome()
    close_game_menu()

    for widget in content_frame.winfo_children():
        widget.destroy()

    set_active(top_players)


def open_shop():

    hide_welcome()
    close_game_menu()

    for widget in content_frame.winfo_children():
        widget.destroy()

    set_active(shop)
    show_shop_page()


# =====================================================
# SHOP / SUBSCRIPTIONS
# =====================================================

def show_shop_page():

    global selected_shop_plan

    clear_profile_page()

    frame = tk.Frame(content_frame, bg="#202124")
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="Shop",
        font=("Arial", 26, "bold"),
        bg="#202124",
        fg="white"
    ).pack(pady=(35, 8))

    tk.Label(
        frame,
        text="Special Accounts & Subscriptions",
        font=("Arial", 11),
        bg="#202124",
        fg="#BDBDBD"
    ).pack(pady=(0, 18))

    cards = tk.Frame(frame, bg="#202124")
    cards.pack(pady=5)

    for plan_name, price in SHOP_PLANS.items():
        card = tk.Frame(
            cards,
            bg="#303134",
            bd=1,
            relief="solid",
            width=190,
            height=135
        )
        card.pack(side="left", padx=7)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=plan_name,
            font=("Arial", 17, "bold"),
            bg="#303134",
            fg="white"
        ).pack(pady=(12, 3))

        tk.Label(
            card,
            text=f"{price} KSh",
            font=("Arial", 14, "bold"),
            bg="#303134",
            fg="#FFD54F"
        ).pack(pady=2)

        tk.Button(
            card,
            text="Buy",
            font=("Arial", 10, "bold"),
            width=12,
            command=lambda n=plan_name, p=price: select_shop_plan(n, p)
        ).pack(pady=9)

    current_text = (
        f"Current plan: {player_plan}"
        if player_plan != "Free Plan"
        else "Current plan: Free Plan"
    )

    current_label = tk.Label(
        frame,
        text=current_text,
        font=("Arial", 11, "bold"),
        bg="#202124",
        fg="#66BB6A"
    )
    current_label.pack(pady=18)

    tk.Label(
        frame,
        text="Prices are in Kenyan Shillings (KSh).",
        font=("Arial", 9),
        bg="#202124",
        fg="#BDBDBD"
    ).pack(pady=2)

    tk.Label(
        frame,
        text="M-PESA payment will be connected through Safaricom Daraja when the backend is ready.",
        font=("Arial", 8),
        bg="#202124",
        fg="#BDBDBD",
        wraplength=600
    ).pack(pady=8)


def select_shop_plan(plan_name, price):

    global selected_shop_plan
    selected_shop_plan = plan_name

    box = tk.Toplevel(window)
    box.title("Purchase")
    box.configure(bg="#202124")
    box.transient(window)
    box.grab_set()

    tk.Label(
        box,
        text=f"{plan_name} - {price} KSh",
        font=("Arial", 18, "bold"),
        bg="#202124",
        fg="white"
    ).pack(padx=30, pady=(20, 8))

    tk.Label(
        box,
        text="Pay with M-PESA",
        font=("Arial", 12, "bold"),
        bg="#202124",
        fg="#66BB6A"
    ).pack(pady=5)

    tk.Label(
        box,
        text="Real payment is not activated yet.\nA secure backend and Safaricom Daraja credentials are required.",
        font=("Arial", 9),
        bg="#202124",
        fg="#BDBDBD",
        justify="center"
    ).pack(pady=8)

    tk.Button(
        box,
        text="Close",
        font=("Arial", 11, "bold"),
        width=12,
        command=box.destroy
    ).pack(pady=(5, 18))


# =====================================================
# CHESS
# =====================================================

class ChessGame:

    def __init__(
        self,
        parent,
        bot=False,
        level=1
    ):

        self.parent = parent
        self.bot = bot
        self.level = level

        self.pieces = starting_position()
        self.turn = "white"
        self.selected = None
        self.en_passant = None

        self.moved = {
            "white_king": False,
            "black_king": False,
            "white_rook_left": False,
            "white_rook_right": False,
            "black_rook_left": False,
            "black_rook_right": False
        }

        self.captured = {
            "white": [],
            "black": []
        }

        self.history = []
        self.game_over = False
        self.bot_job = None

        self.build_screen()
        self.refresh()

    # =================================================
    # SCREEN
    # =================================================

    def build_screen(self):

        self.game_area = tk.Frame(
            self.parent,
            bg="#202124"
        )

        self.game_area.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        tk.Button(
            self.game_area,
            text="Back",
            font=("Arial", 11, "bold"),
            command=back_from_chess
        ).place(
            x=0,
            y=0
        )

        # Canvas board.
        # This prevents columns from changing size.

        self.canvas = tk.Canvas(
            self.game_area,
            width=480,
            height=480,
            bg="#202124",
            highlightthickness=0
        )

        self.canvas.place(
            relx=0.39,
            rely=0.52,
            anchor="center"
        )

        self.canvas.bind(
            "<Button-1>",
            self.canvas_click
        )

        self.info = tk.Frame(
            self.game_area,
            bg="#202124"
        )

        self.info.place(
            relx=0.86,
            rely=0.50,
            anchor="center"
        )

        self.status = tk.Label(
            self.info,
            text="White's turn",
            font=("Arial", 13, "bold"),
            bg="#202124",
            fg="white",
            wraplength=150
        )

        self.status.pack(
            pady=10
        )

        self.black_captured = tk.Label(
            self.info,
            text="Black:\n-",
            font=("Arial", 12),
            bg="#202124",
            fg="white",
            justify="left"
        )

        self.black_captured.pack(
            pady=10
        )

        self.white_captured = tk.Label(
            self.info,
            text="White:\n-",
            font=("Arial", 12),
            bg="#202124",
            fg="white",
            justify="left"
        )

        self.white_captured.pack(
            pady=10
        )

        self.undo_button = tk.Button(
            self.info,
            text="Undo",
            font=("Arial", 11, "bold"),
            width=12,
            command=self.undo
        )

        self.undo_button.pack(
            pady=5
        )

        tk.Button(
            self.info,
            text="Restart",
            font=("Arial", 11, "bold"),
            width=12,
            command=self.restart_confirm
        ).pack(
            pady=5
        )

    # =================================================
    # BASIC HELPERS
    # =================================================

    def enemy(self, color):

        if color == "white":
            return "black"

        return "white"


    def inside(self, position):

        row, col = position

        return (
            0 <= row < 8
            and
            0 <= col < 8
        )


    def king_position(self, color, state):

        for position, piece in state.items():

            if piece == (color, "king"):
                return position

        return None

    # =================================================
    # ATTACKS
    # =================================================

    def attacked(
        self,
        position,
        by_color,
        state
    ):

        row, col = position

        for start, piece in state.items():

            color, kind = piece

            if color != by_color:
                continue

            r, c = start

            dr = row - r
            dc = col - c

            if kind == "pawn":

                direction = -1 if color == "white" else 1

                if (
                    dr == direction
                    and
                    abs(dc) == 1
                ):
                    return True

            elif kind == "knight":

                if (
                    abs(dr),
                    abs(dc)
                ) in [
                    (1, 2),
                    (2, 1)
                ]:
                    return True

            elif kind == "king":

                if max(
                    abs(dr),
                    abs(dc)
                ) == 1:
                    return True

            elif kind in [
                "rook",
                "bishop",
                "queen"
            ]:

                straight = (
                    dr == 0
                    or
                    dc == 0
                )

                diagonal = (
                    abs(dr) == abs(dc)
                )

                if kind == "rook" and not straight:
                    continue

                if kind == "bishop" and not diagonal:
                    continue

                if kind == "queen" and not (
                    straight or diagonal
                ):
                    continue

                step_r = 0

                if dr > 0:
                    step_r = 1

                elif dr < 0:
                    step_r = -1

                step_c = 0

                if dc > 0:
                    step_c = 1

                elif dc < 0:
                    step_c = -1

                rr = r + step_r
                cc = c + step_c

                blocked = False

                while (
                    rr,
                    cc
                ) != (
                    row,
                    col
                ):

                    if (
                        rr,
                        cc
                    ) in state:

                        blocked = True
                        break

                    rr += step_r
                    cc += step_c

                if not blocked:
                    return True

        return False


    def in_check(
        self,
        color,
        state
    ):

        king = self.king_position(
            color,
            state
        )

        if king is None:
            return True

        return self.attacked(
            king,
            self.enemy(color),
            state
        )

    # =================================================
    # RAW MOVES
    # =================================================

    def raw_moves(
        self,
        start,
        color,
        state
    ):

        if start not in state:
            return []

        piece_color, kind = state[start]

        if piece_color != color:
            return []

        row, col = start
        moves = []

        # PAWN

        if kind == "pawn":

            direction = (
                -1
                if color == "white"
                else 1
            )

            start_row = (
                6
                if color == "white"
                else 1
            )

            one = (
                row + direction,
                col
            )

            if (
                self.inside(one)
                and
                one not in state
            ):

                moves.append(one)

                two = (
                    row + direction * 2,
                    col
                )

                if (
                    row == start_row
                    and
                    two not in state
                ):
                    moves.append(two)

            for dc in [-1, 1]:

                target = (
                    row + direction,
                    col + dc
                )

                if not self.inside(target):
                    continue

                if target in state:

                    if state[target][0] != color:

                        if state[target][1] != "king":
                            moves.append(target)

                elif target == self.en_passant:

                    moves.append(target)

        # KNIGHT

        elif kind == "knight":

            jumps = [
                (-2, -1),
                (-2, 1),
                (-1, -2),
                (-1, 2),
                (1, -2),
                (1, 2),
                (2, -1),
                (2, 1)
            ]

            for dr, dc in jumps:

                target = (
                    row + dr,
                    col + dc
                )

                if not self.inside(target):
                    continue

                if target not in state:

                    moves.append(target)

                elif state[target][0] != color:

                    if state[target][1] != "king":
                        moves.append(target)

        # KING

        elif kind == "king":

            for dr in [-1, 0, 1]:

                for dc in [-1, 0, 1]:

                    if dr == 0 and dc == 0:
                        continue

                    target = (
                        row + dr,
                        col + dc
                    )

                    if not self.inside(target):
                        continue

                    if target not in state:

                        moves.append(target)

                    elif state[target][0] != color:

                        if state[target][1] != "king":
                            moves.append(target)

            # CASTLING

            if not self.in_check(
                color,
                state
            ):

                if color == "white":

                    if (
                        not self.moved["white_king"]
                        and
                        not self.moved["white_rook_right"]
                        and
                        state.get((7, 7))
                        ==
                        ("white", "rook")
                        and
                        (7, 5) not in state
                        and
                        (7, 6) not in state
                        and
                        not self.attacked(
                            (7, 5),
                            "black",
                            state
                        )
                        and
                        not self.attacked(
                            (7, 6),
                            "black",
                            state
                        )
                    ):

                        moves.append((7, 6))

                    if (
                        not self.moved["white_king"]
                        and
                        not self.moved["white_rook_left"]
                        and
                        state.get((7, 0))
                        ==
                        ("white", "rook")
                        and
                        (7, 1) not in state
                        and
                        (7, 2) not in state
                        and
                        (7, 3) not in state
                        and
                        not self.attacked(
                            (7, 2),
                            "black",
                            state
                        )
                        and
                        not self.attacked(
                            (7, 3),
                            "black",
                            state
                        )
                    ):

                        moves.append((7, 2))

                else:

                    if (
                        not self.moved["black_king"]
                        and
                        not self.moved["black_rook_right"]
                        and
                        state.get((0, 7))
                        ==
                        ("black", "rook")
                        and
                        (0, 5) not in state
                        and
                        (0, 6) not in state
                        and
                        not self.attacked(
                            (0, 5),
                            "white",
                            state
                        )
                        and
                        not self.attacked(
                            (0, 6),
                            "white",
                            state
                        )
                    ):

                        moves.append((0, 6))

                    if (
                        not self.moved["black_king"]
                        and
                        not self.moved["black_rook_left"]
                        and
                        state.get((0, 0))
                        ==
                        ("black", "rook")
                        and
                        (0, 1) not in state
                        and
                        (0, 2) not in state
                        and
                        (0, 3) not in state
                        and
                        not self.attacked(
                            (0, 2),
                            "white",
                            state
                        )
                        and
                        not self.attacked(
                            (0, 3),
                            "white",
                            state
                        )
                    ):

                        moves.append((0, 2))

        # ROOK / BISHOP / QUEEN

        elif kind in [
            "rook",
            "bishop",
            "queen"
        ]:

            directions = []

            if kind in [
                "rook",
                "queen"
            ]:

                directions += [
                    (-1, 0),
                    (1, 0),
                    (0, -1),
                    (0, 1)
                ]

            if kind in [
                "bishop",
                "queen"
            ]:

                directions += [
                    (-1, -1),
                    (-1, 1),
                    (1, -1),
                    (1, 1)
                ]

            for dr, dc in directions:

                rr = row + dr
                cc = col + dc

                while self.inside(
                    (rr, cc)
                ):

                    target = (
                        rr,
                        cc
                    )

                    if target not in state:

                        moves.append(target)

                    else:

                        if state[target][0] != color:

                            if state[target][1] != "king":
                                moves.append(target)

                        break

                    rr += dr
                    cc += dc

        return moves

    # =================================================
    # LEGAL MOVES
    # =================================================

    def legal_moves(
        self,
        start,
        color
    ):

        result = []

        for target in self.raw_moves(
            start,
            color,
            self.pieces
        ):

            test = dict(
                self.pieces
            )

            moving = test.pop(
                start
            )

            if (
                moving[1] == "pawn"
                and
                target == self.en_passant
                and
                target not in test
            ):

                captured_row = (
                    target[0]
                    +
                    (
                        1
                        if color == "white"
                        else -1
                    )
                )

                test.pop(
                    (
                        captured_row,
                        target[1]
                    ),
                    None
                )

            else:

                test.pop(
                    target,
                    None
                )

            test[target] = moving

            # Castle rook

            if (
                moving[1] == "king"
                and
                abs(
                    target[1]
                    -
                    start[1]
                ) == 2
            ):

                if target[1] == 6:

                    rook_start = (
                        start[0],
                        7
                    )

                    rook_end = (
                        start[0],
                        5
                    )

                else:

                    rook_start = (
                        start[0],
                        0
                    )

                    rook_end = (
                        start[0],
                        3
                    )

                rook = test.pop(
                    rook_start,
                    None
                )

                if rook:
                    test[rook_end] = rook

            king = self.king_position(
                color,
                test
            )

            if king is None:
                continue

            if not self.attacked(
                king,
                self.enemy(color),
                test
            ):

                result.append(target)

        return result


    def all_legal_moves(
        self,
        color
    ):

        result = []

        for position, piece in list(
            self.pieces.items()
        ):

            if piece[0] != color:
                continue

            for target in self.legal_moves(
                position,
                color
            ):

                result.append(
                    (
                        position,
                        target
                    )
                )

        return result

    # =================================================
    # BOT EVALUATION
    # =================================================

    def evaluate_position(
        self,
        state
    ):

        score = 0

        for position, piece in state.items():

            color, kind = piece

            value = PIECE_VALUES[kind]

            if color == "black":
                score += value
            else:
                score -= value

            row, col = position

            center = (
                3.5
                -
                (
                    abs(3.5 - row)
                    +
                    abs(3.5 - col)
                )
            )

            if center > 0:

                if color == "black":
                    score += center * 5
                else:
                    score -= center * 5

            if kind == "pawn":

                advancement = (
                    row
                    if color == "black"
                    else
                    7 - row
                )

                if color == "black":
                    score += advancement * 3
                else:
                    score -= advancement * 3

        if self.in_check(
            "white",
            state
        ):
            score += 40

        if self.in_check(
            "black",
            state
        ):
            score -= 40

        return score

    # =================================================
    # SEARCH MOVE
    # =================================================

    def search_move(
        self,
        state,
        moved,
        en_passant,
        start,
        target
    ):

        new_state = dict(state)
        new_moved = dict(moved)

        moving = new_state.pop(start)

        color, kind = moving

        captured = None

        if (
            kind == "pawn"
            and
            target == en_passant
            and
            target not in new_state
        ):

            captured_row = (
                target[0]
                +
                (
                    1
                    if color == "white"
                    else -1
                )
            )

            captured = new_state.pop(
                (
                    captured_row,
                    target[1]
                ),
                None
            )

        else:

            captured = new_state.pop(
                target,
                None
            )

        new_state[target] = moving

        if (
            kind == "king"
            and
            abs(
                target[1]
                -
                start[1]
            ) == 2
        ):

            if target[1] == 6:

                rook_start = (
                    start[0],
                    7
                )

                rook_end = (
                    start[0],
                    5
                )

            else:

                rook_start = (
                    start[0],
                    0
                )

                rook_end = (
                    start[0],
                    3
                )

            rook = new_state.pop(
                rook_start,
                None
            )

            if rook:
                new_state[rook_end] = rook

        if kind == "king":

            new_moved[
                color + "_king"
            ] = True

        if kind == "rook":

            if color == "white":

                if start == (7, 0):
                    new_moved[
                        "white_rook_left"
                    ] = True

                if start == (7, 7):
                    new_moved[
                        "white_rook_right"
                    ] = True

            else:

                if start == (0, 0):
                    new_moved[
                        "black_rook_left"
                    ] = True

                if start == (0, 7):
                    new_moved[
                        "black_rook_right"
                    ] = True

        if captured == ("white", "rook"):

            if target == (7, 0):
                new_moved[
                    "white_rook_left"
                ] = True

            if target == (7, 7):
                new_moved[
                    "white_rook_right"
                ] = True

        if captured == ("black", "rook"):

            if target == (0, 0):
                new_moved[
                    "black_rook_left"
                ] = True

            if target == (0, 7):
                new_moved[
                    "black_rook_right"
                ] = True

        new_ep = None

        if (
            kind == "pawn"
            and
            abs(
                target[0]
                -
                start[0]
            ) == 2
        ):

            new_ep = (
                (
                    start[0]
                    +
                    target[0]
                ) // 2,
                start[1]
            )

        promotion_row = (
            0
            if color == "white"
            else 7
        )

        if (
            kind == "pawn"
            and
            target[0] == promotion_row
        ):

            new_state[target] = (
                color,
                "queen"
            )

        return (
            new_state,
            new_moved,
            new_ep
        )

    # =================================================
    # SEARCH LEGAL MOVES
    # =================================================

    def search_legal_moves(
        self,
        state,
        moved,
        en_passant,
        color
    ):

        old_pieces = self.pieces
        old_moved = self.moved
        old_ep = self.en_passant

        try:

            self.pieces = state
            self.moved = moved
            self.en_passant = en_passant

            return self.all_legal_moves(
                color
            )

        finally:

            self.pieces = old_pieces
            self.moved = old_moved
            self.en_passant = old_ep

    # =================================================
    # MOVE ORDER
    # =================================================

    def move_order_score(
        self,
        state,
        move
    ):

        start, target = move

        score = 0

        moving = state.get(start)
        captured = state.get(target)

        if captured:

            score += (
                PIECE_VALUES[
                    captured[1]
                ]
                *
                10
            )

        if moving:

            if moving[1] == "pawn":

                if target[0] in [0, 7]:
                    score += 8000

        if (
            target[0] in [3, 4]
            and
            target[1] in [3, 4]
        ):

            score += 50

        return score

    # =================================================
    # MINIMAX
    # =================================================

    def minimax(
        self,
        state,
        moved,
        en_passant,
        turn,
        depth,
        alpha,
        beta,
        start_time,
        time_limit
    ):

        if (
            time.time()
            -
            start_time
        ) > time_limit:

            raise TimeoutError

        moves = self.search_legal_moves(
            state,
            moved,
            en_passant,
            turn
        )

        if not moves:

            if self.in_check(
                turn,
                state
            ):

                if turn == "black":
                    return -1000000 + depth

                return 1000000 - depth

            return 0

        if depth == 0:

            return self.evaluate_position(
                state
            )

        moves.sort(
            key=lambda move:
            self.move_order_score(
                state,
                move
            ),
            reverse=True
        )

        if turn == "black":

            best = -10000000

            for start, target in moves:

                (
                    new_state,
                    new_moved,
                    new_ep
                ) = self.search_move(
                    state,
                    moved,
                    en_passant,
                    start,
                    target
                )

                value = self.minimax(
                    new_state,
                    new_moved,
                    new_ep,
                    "white",
                    depth - 1,
                    alpha,
                    beta,
                    start_time,
                    time_limit
                )

                best = max(
                    best,
                    value
                )

                alpha = max(
                    alpha,
                    best
                )

                if beta <= alpha:
                    break

            return best

        best = 10000000

        for start, target in moves:

            (
                new_state,
                new_moved,
                new_ep
            ) = self.search_move(
                state,
                moved,
                en_passant,
                start,
                target
            )

            value = self.minimax(
                new_state,
                new_moved,
                new_ep,
                "black",
                depth - 1,
                alpha,
                beta,
                start_time,
                time_limit
            )

            best = min(
                best,
                value
            )

            beta = min(
                beta,
                best
            )

            if beta <= alpha:
                break

        return best

    # =================================================
    # BEST MOVE
    # =================================================

    def find_best_move(
        self,
        moves,
        max_depth,
        time_limit
    ):

        start_time = time.time()

        best_move = random.choice(
            moves
        )

        for depth in range(
            1,
            max_depth + 1
        ):

            current_best = None
            current_score = -10000000

            try:

                ordered = sorted(
                    moves,
                    key=lambda move:
                    self.move_order_score(
                        self.pieces,
                        move
                    ),
                    reverse=True
                )

                for start, target in ordered:

                    (
                        new_state,
                        new_moved,
                        new_ep
                    ) = self.search_move(
                        self.pieces,
                        self.moved,
                        self.en_passant,
                        start,
                        target
                    )

                    score = self.minimax(
                        new_state,
                        new_moved,
                        new_ep,
                        "white",
                        depth - 1,
                        -10000000,
                        10000000,
                        start_time,
                        time_limit
                    )

                    if score > current_score:

                        current_score = score

                        current_best = (
                            start,
                            target
                        )

                if current_best is not None:
                    best_move = current_best

            except TimeoutError:

                break

        return best_move

    # =================================================
    # BOT MOVE
    # =================================================

    def bot_move(self):

        if (
            self.game_over
            or
            self.turn != "black"
        ):
            return

        self.bot_job = None

        moves = self.all_legal_moves(
            "black"
        )

        if not moves:
            return

        # Level 1

        if self.level == 1:

            move = random.choice(
                moves
            )

            self.make_move(
                move[0],
                move[1]
            )

            return

        # Level 2

        if self.level == 2:

            captures = [
                move
                for move in moves
                if move[1] in self.pieces
            ]

            if (
                captures
                and
                random.random() < 0.30
            ):

                move = random.choice(
                    captures
                )

            else:

                move = random.choice(
                    moves
                )

            self.make_move(
                move[0],
                move[1]
            )

            return

        # Level 3 and 4

        if self.level <= 4:

            best = []
            best_score = -100000

            for start, target in moves:

                score = random.randint(
                    0,
                    20
                )

                if target in self.pieces:

                    score += (
                        PIECE_VALUES[
                            self.pieces[
                                target
                            ][1]
                        ]
                        *
                        0.15
                    )

                if (
                    target[0] in [3, 4]
                    and
                    target[1] in [3, 4]
                ):

                    score += 35

                if score > best_score:

                    best_score = score
                    best = [
                        (
                            start,
                            target
                        )
                    ]

                elif score == best_score:

                    best.append(
                        (
                            start,
                            target
                        )
                    )

            move = random.choice(
                best
            )

            self.make_move(
                move[0],
                move[1]
            )

            return

        # Level 5 and 6

        if self.level <= 6:

            move = self.find_best_move(
                moves,
                2,
                0.8
            )

            self.make_move(
                move[0],
                move[1]
            )

            return

        # Level 7 to 9

        if self.level <= 9:

            move = self.find_best_move(
                moves,
                3,
                1.2
            )

            self.make_move(
                move[0],
                move[1]
            )

            return

        # Level 10

        move = self.find_best_move(
            moves,
            4,
            2.5
        )

        self.make_move(
            move[0],
            move[1]
        )

    # =================================================
    # DRAW BOARD
    # =================================================

    def refresh(self):

        self.canvas.delete(
            "all"
        )

        square = 60

        legal = []

        if self.selected is not None:

            legal = self.legal_moves(
                self.selected,
                self.turn
            )

        for row in range(8):

            for col in range(8):

                x1 = col * square
                y1 = row * square
                x2 = x1 + square
                y2 = y1 + square

                color = (
                    "#F0D9B5"
                    if
                    (row + col) % 2 == 0
                    else
                    "#B58863"
                )

                if self.selected == (
                    row,
                    col
                ):

                    color = "#FFD54F"

                elif (
                    row,
                    col
                ) in legal:

                    color = "#81C784"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline=color
                )

                position = (
                    row,
                    col
                )

                if position in self.pieces:

                    piece = self.pieces[
                        position
                    ]

                    self.canvas.create_text(
                        x1 + 30,
                        y1 + 31,
                        text=SYMBOLS[piece],
                        font=("Arial", 34)
                    )

        self.update_captured()

        if (
            self.history
            and
            not self.game_over
        ):

            self.undo_button.config(
                state="normal"
            )

        else:

            self.undo_button.config(
                state="disabled"
            )

    # =================================================
    # CANVAS CLICK
    # =================================================

    def canvas_click(self, event):

        if self.game_over:
            return

        if (
            self.bot
            and
            self.turn == "black"
        ):
            return

        col = event.x // 60
        row = event.y // 60

        if not self.inside(
            (row, col)
        ):
            return

        self.click(
            row,
            col
        )

    # =================================================
    # CAPTURED
    # =================================================

    def update_captured(self):

        black_text = " ".join(
            SYMBOLS[p]
            for p in self.captured[
                "black"
            ]
        )

        white_text = " ".join(
            SYMBOLS[p]
            for p in self.captured[
                "white"
            ]
        )

        if not black_text:
            black_text = "-"

        if not white_text:
            white_text = "-"

        self.black_captured.config(
            text="Black:\n" + black_text
        )

        self.white_captured.config(
            text="White:\n" + white_text
        )

    # =================================================
    # HISTORY
    # =================================================

    def save_history(self):

        self.history.append({
            "pieces": dict(
                self.pieces
            ),
            "turn": self.turn,
            "moved": dict(
                self.moved
            ),
            "en_passant": self.en_passant,
            "captured": deepcopy(
                self.captured
            )
        })


    def undo(self):

        if (
            not self.history
            or
            self.game_over
        ):
            return

        state = self.history.pop()

        self.pieces = dict(
            state["pieces"]
        )

        self.turn = state["turn"]

        self.moved = dict(
            state["moved"]
        )

        self.en_passant = (
            state["en_passant"]
        )

        self.captured = deepcopy(
            state["captured"]
        )

        self.selected = None

        self.refresh()

        if self.turn == "white":
            self.status.config(
                text="White's turn"
            )
        else:
            self.status.config(
                text="Black's turn"
            )

    # =================================================
    # MAKE MOVE
    # =================================================

    def make_move(
        self,
        start,
        target
    ):

        if start not in self.pieces:
            return

        self.save_history()

        color, kind = self.pieces[
            start
        ]

        captured = None

        # En passant

        if (
            kind == "pawn"
            and
            target == self.en_passant
            and
            target not in self.pieces
        ):

            captured_row = (
                target[0]
                +
                (
                    1
                    if color == "white"
                    else -1
                )
            )

            captured = self.pieces.pop(
                (
                    captured_row,
                    target[1]
                ),
                None
            )

            if captured:

                self.captured[
                    color
                ].append(
                    captured
                )

        normal_capture = self.pieces.pop(
            target,
            None
        )

        if normal_capture:

            captured = normal_capture

            self.captured[
                color
            ].append(
                normal_capture
            )

        self.pieces.pop(
            start
        )

        self.pieces[
            target
        ] = (
            color,
            kind
        )

        # King

        if kind == "king":

            self.moved[
                color + "_king"
            ] = True

            if abs(
                target[1]
                -
                start[1]
            ) == 2:

                if target[1] == 6:

                    rook_start = (
                        start[0],
                        7
                    )

                    rook_end = (
                        start[0],
                        5
                    )

                else:

                    rook_start = (
                        start[0],
                        0
                    )

                    rook_end = (
                        start[0],
                        3
                    )

                rook = self.pieces.pop(
                    rook_start,
                    None
                )

                if rook:

                    self.pieces[
                        rook_end
                    ] = rook

        # Rook

        if kind == "rook":

            if color == "white":

                if start == (7, 0):
                    self.moved[
                        "white_rook_left"
                    ] = True

                if start == (7, 7):
                    self.moved[
                        "white_rook_right"
                    ] = True

            else:

                if start == (0, 0):
                    self.moved[
                        "black_rook_left"
                    ] = True

                if start == (0, 7):
                    self.moved[
                        "black_rook_right"
                    ] = True

        # Captured rook

        if captured == (
            "white",
            "rook"
        ):

            if target == (7, 0):
                self.moved[
                    "white_rook_left"
                ] = True

            if target == (7, 7):
                self.moved[
                    "white_rook_right"
                ] = True

        if captured == (
            "black",
            "rook"
        ):

            if target == (0, 0):
                self.moved[
                    "black_rook_left"
                ] = True

            if target == (0, 7):
                self.moved[
                    "black_rook_right"
                ] = True

        # En passant square

        self.en_passant = None

        if (
            kind == "pawn"
            and
            abs(
                target[0]
                -
                start[0]
            ) == 2
        ):

            self.en_passant = (
                (
                    start[0]
                    +
                    target[0]
                ) // 2,
                start[1]
            )

        # Promotion

        promotion_row = (
            0
            if color == "white"
            else 7
        )

        if (
            kind == "pawn"
            and
            target[0] == promotion_row
        ):

            self.pieces[
                target
            ] = (
                color,
                "queen"
            )

        self.turn = self.enemy(
            self.turn
        )

        self.selected = None

        self.refresh()

        self.check_end()

    # =================================================
    # CHECK END
    # =================================================

    def check_end(self):

        color = self.turn

        moves = self.all_legal_moves(
            color
        )

        if not moves:

            self.game_over = True

            if self.in_check(
                color,
                self.pieces
            ):

                winner = (
                    "White"
                    if color == "black"
                    else "Black"
                )

                self.status.config(
                    text="Checkmate! "
                    + winner
                    + " wins!"
                )

                if (
                    self.bot
                    and
                    winner == "White"
                ):

                    complete_level(
                        self.level
                    )

                self.show_game_over(
                    winner + " wins!"
                )

            else:

                self.status.config(
                    text="Stalemate!"
                )

                self.show_game_over(
                    "Draw!"
                )

            return

        if self.in_check(
            color,
            self.pieces
        ):

            self.status.config(
                text=(
                    "White"
                    if color == "white"
                    else "Black"
                )
                +
                " is in check!"
            )

        else:

            self.status.config(
                text=(
                    "White"
                    if color == "white"
                    else "Black"
                )
                +
                "'s turn"
            )

        if (
            self.bot
            and
            self.turn == "black"
            and
            not self.game_over
        ):

            self.bot_job = self.parent.after(
                450,
                self.bot_move
            )

    # =================================================
    # BOT CANCEL
    # =================================================

    def cancel_bot(self):

        if self.bot_job is not None:

            try:
                self.parent.after_cancel(
                    self.bot_job
                )
            except:
                pass

            self.bot_job = None

    # =================================================
    # RESTART
    # =================================================

    def restart_confirm(self):

        box = tk.Toplevel(
            window
        )

        box.title(
            "Restart Game"
        )

        box.configure(
            bg="#202124"
        )

        box.transient(
            window
        )

        box.grab_set()

        tk.Label(
            box,
            text="Restart this game?",
            font=("Arial", 16, "bold"),
            bg="#202124",
            fg="white"
        ).pack(
            padx=30,
            pady=(18, 8)
        )

        tk.Label(
            box,
            text="Your current game will be lost.",
            font=("Arial", 10),
            bg="#202124",
            fg="#BDBDBD"
        ).pack(
            pady=3
        )

        buttons = tk.Frame(
            box,
            bg="#202124"
        )

        buttons.pack(
            pady=15
        )

        tk.Button(
            buttons,
            text="Restart",
            font=("Arial", 11, "bold"),
            command=lambda: [
                box.destroy(),
                self.restart()
            ]
        ).pack(
            side="left",
            padx=4
        )

        tk.Button(
            buttons,
            text="Main Menu",
            font=("Arial", 11, "bold"),
            command=lambda: [
                box.destroy(),
                back_from_chess()
            ]
        ).pack(
            side="left",
            padx=4
        )

        tk.Button(
            buttons,
            text="Cancel",
            font=("Arial", 11, "bold"),
            command=box.destroy
        ).pack(
            side="left",
            padx=4
        )


    def restart(self):

        self.cancel_bot()

        for widget in self.parent.winfo_children():
            widget.destroy()

        self.__init__(
            self.parent,
            self.bot,
            self.level
        )

    # =================================================
    # GAME OVER
    # =================================================

    def show_game_over(
        self,
        message
    ):

        self.cancel_bot()

        box = tk.Frame(
            self.parent,
            bg="#202124",
            bd=2,
            relief="solid"
        )

        box.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            box,
            text="Game Over!",
            font=("Arial", 22, "bold"),
            bg="#202124",
            fg="white"
        ).pack(
            padx=30,
            pady=(15, 6)
        )

        tk.Label(
            box,
            text=message,
            font=("Arial", 17, "bold"),
            bg="#202124",
            fg="#FFD54F"
        ).pack(
            pady=6
        )

        buttons = tk.Frame(
            box,
            bg="#202124"
        )

        buttons.pack(
            pady=14
        )

        tk.Button(
            buttons,
            text="Play Again",
            font=("Arial", 11, "bold"),
            command=lambda: [
                box.destroy(),
                self.restart()
            ]
        ).pack(
            side="left",
            padx=4
        )

        tk.Button(
            buttons,
            text="Main Menu",
            font=("Arial", 11, "bold"),
            command=lambda: [
                box.destroy(),
                back_from_chess()
            ]
        ).pack(
            side="left",
            padx=4
        )

        tk.Button(
            buttons,
            text="Close",
            font=("Arial", 11, "bold"),
            command=box.destroy
        ).pack(
            side="left",
            padx=4
        )

        self.undo_button.config(
            state="disabled"
        )

    # =================================================
    # CLICK
    # =================================================

    def click(
        self,
        row,
        col
    ):

        if self.game_over:
            return

        if (
            self.bot
            and
            self.turn == "black"
        ):
            return

        position = (
            row,
            col
        )

        if self.selected is None:

            if position in self.pieces:

                if (
                    self.pieces[
                        position
                    ][0]
                    ==
                    self.turn
                ):

                    self.selected = position
                    self.refresh()

            return

        if self.selected == position:

            self.selected = None
            self.refresh()
            return

        if (
            position in self.pieces
            and
            self.pieces[
                position
            ][0]
            ==
            self.turn
        ):

            self.selected = position
            self.refresh()
            return

        moves = self.legal_moves(
            self.selected,
            self.turn
        )

        if position in moves:

            self.make_move(
                self.selected,
                position
            )

        else:

            self.selected = None
            self.refresh()


# =====================================================
# NAVIGATION
# =====================================================

def open_offline():

    hide_welcome()
    close_game_menu()
    bottom_menu.pack_forget()

    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Button(
        content_frame,
        text="Back",
        font=("Arial", 14, "bold"),
        command=back_to_main
    ).place(
        x=20,
        y=20
    )

    tk.Label(
        content_frame,
        text="Offline Game",
        font=("Arial", 28, "bold"),
        bg="#202124",
        fg="white"
    ).pack(
        pady=75
    )

    tk.Button(
        content_frame,
        text="Play with Bot",
        font=("Arial", 18),
        width=20,
        height=2,
        command=open_bot_seasons
    ).pack(
        pady=8
    )

    tk.Button(
        content_frame,
        text="Two Player",
        font=("Arial", 18),
        width=20,
        height=2,
        command=open_two_player
    ).pack(
        pady=8
    )


def back_to_main():

    global current_game

    if current_game is not None:

        current_game.cancel_bot()
        current_game = None

    for widget in content_frame.winfo_children():
        widget.destroy()

    bottom_menu.pack(
        side="bottom",
        fill="x",
        pady=10
    )

    show_main_page()
    set_active(game)


def back_from_chess():

    back_to_main()


def open_two_player():

    global current_game

    hide_welcome()
    close_game_menu()
    bottom_menu.pack_forget()

    for widget in content_frame.winfo_children():
        widget.destroy()

    current_game = ChessGame(
        content_frame,
        bot=False
    )


# =====================================================
# BOT SEASONS
# =====================================================

def open_bot_seasons():

    hide_welcome()
    close_game_menu()
    bottom_menu.pack_forget()

    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Button(
        content_frame,
        text="Back",
        font=("Arial", 14, "bold"),
        command=open_offline
    ).place(
        x=20,
        y=20
    )

    tk.Label(
        content_frame,
        text="Play with Bot",
        font=("Arial", 25, "bold"),
        bg="#202124",
        fg="white"
    ).pack(
        pady=(55, 18)
    )

    seasons = tk.Frame(
        content_frame,
        bg="#202124"
    )

    seasons.pack()

    tk.Button(
        seasons,
        text="Season 1",
        font=("Arial", 15, "bold"),
        width=17,
        height=2,
        command=open_bot_levels
    ).pack(
        pady=7
    )

    tk.Button(
        seasons,
        text="Season 2",
        font=("Arial", 15, "bold"),
        width=17,
        height=2,
        state="disabled"
    ).pack(
        pady=7
    )

    tk.Button(
        seasons,
        text="Season 3",
        font=("Arial", 15, "bold"),
        width=17,
        height=2,
        state="disabled"
    ).pack(
        pady=7
    )

    tk.Label(
        content_frame,
        text="Complete the seasons to unlock future content.",
        font=("Arial", 10),
        bg="#202124",
        fg="#BDBDBD"
    ).pack(
        pady=10
    )


# =====================================================
# BOT LEVELS
# =====================================================

def open_bot_levels():

    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Button(
        content_frame,
        text="Back",
        font=("Arial", 13, "bold"),
        command=open_bot_seasons
    ).place(
        x=20,
        y=20
    )

    tk.Label(
        content_frame,
        text="Season 1",
        font=("Arial", 24, "bold"),
        bg="#202124",
        fg="white"
    ).pack(
        pady=(50, 10)
    )

    tk.Label(
        content_frame,
        text=
        f"{player_plan} - Unlocked through Level {current_level_unlocked}",
        font=("Arial", 11),
        bg="#202124",
        fg="#BDBDBD"
    ).pack(
        pady=2
    )

    levels_frame = tk.Frame(
        content_frame,
        bg="#202124"
    )

    levels_frame.pack(
        pady=18
    )

    for level in range(1, 11):

        unlocked = is_level_unlocked(
            level
        )

        if unlocked:

            text = f"Level {level}"
            state = "normal"

            command = (
                lambda l=level:
                start_bot_game(l)
            )

        else:

            text = f"Locked Level {level}"
            state = "disabled"
            command = None

        tk.Button(
            levels_frame,
            text=text,
            font=("Arial", 12, "bold"),
            width=14,
            height=2,
            state=state,
            command=command
        ).grid(
            row=(level - 1) // 2,
            column=(level - 1) % 2,
            padx=8,
            pady=7
        )


# =====================================================
# START BOT
# =====================================================

def start_bot_game(level):

    global current_game

    if not is_level_unlocked(level):
        return

    if current_game is not None:
        current_game.cancel_bot()

    for widget in content_frame.winfo_children():
        widget.destroy()

    current_game = ChessGame(
        content_frame,
        bot=True,
        level=level
    )


# =====================================================
# GAME MENU
# =====================================================

game_menu = tk.Frame(
    window,
    bg="#151515"
)

online = tk.Button(
    game_menu,
    text="Online Game",
    font=("Arial", 16),
    width=18,
    height=2
)

online.pack(
    pady=8
)

offline = tk.Button(
    game_menu,
    text="Offline Game",
    font=("Arial", 16),
    width=18,
    height=2,
    command=open_offline
)

offline.pack(
    pady=8
)


# =====================================================
# BOTTOM MENU
# =====================================================

bottom_menu = tk.Frame(
    window,
    bg="#151515"
)

bottom_menu.pack(
    side="bottom",
    fill="x",
    pady=10
)


profile = tk.Button(
    bottom_menu,
    text="Profile",
    font=("Arial", 12),
    width=12,
    height=2,
    command=open_profile
)

profile.pack(
    side="left",
    expand=True
)


chat = tk.Button(
    bottom_menu,
    text="Chat",
    font=("Arial", 12),
    width=12,
    height=2,
    command=open_chat
)

chat.pack(
    side="left",
    expand=True
)


game = tk.Button(
    bottom_menu,
    text="Game",
    font=("Arial", 12),
    width=12,
    height=2,
    command=open_game
)

game.pack(
    side="left",
    expand=True
)


top_players = tk.Button(
    bottom_menu,
    text="Top Players",
    font=("Arial", 12),
    width=12,
    height=2,
    command=open_top_players
)

top_players.pack(
    side="left",
    expand=True
)


shop = tk.Button(
    bottom_menu,
    text="Shop",
    font=("Arial", 12),
    width=12,
    height=2,
    command=open_shop
)

shop.pack(
    side="left",
    expand=True
)


# =====================================================
# START
# =====================================================

show_main_page()

window.mainloop()
