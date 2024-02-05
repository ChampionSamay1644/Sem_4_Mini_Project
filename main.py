import datetime
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from tkinter import END, IntVar, Listbox, Radiobutton, messagebox
from tkinter import simpledialog, ttk,scrolledtext
from PIL import Image, ImageTk
import os
import firebase_admin
from firebase_admin import db, credentials
import threading
from tkinter import Label
from tkinter import Tk, Canvas, PhotoImage


# Initialize Firebase Admin SDK
cred = credentials.Certificate("credentials.json")  # Path: credentials.json
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://hr-management-system-f7c9f-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)

class CreativeLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Management System")
        self.employee_original_image = None
        self.employee_img = None
        self.boss_original_image = None
        self.boss_img = None
        self.company_name_text = None  # Initialize company_name_text attribute
        self.current_question_index = 0  # Initialize the current question index
        self.db_data = {}  # Initialize db_data as an empty dictionary
        self.selected_values = {}  # Initialize selected_values as an empty dictionary


        # Construct the full path to the image file
        img_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "HR_background.png" #change jpg to png for main background
        )

        # Focus on window
        root.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(root)

        # create a canvas that resizes with the window
        self.company_logo_canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.company_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        root.bind("<Configure>", self.on_window_resize_main)

        # import the image as the background on the canvas
        self.load_image_main(img_path)

        # Label for Username
        username_label = tk.Label(
            root, text="Username", font=("Helvetica", 12, "bold"), bg="white"
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        # Username entry
        self.username_entry = tk.Entry(root, font=("Helvetica", 12, "bold"))
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")  # Default text

        # Label for Password
        password_label = tk.Label(
            root, text="Password", font=("Helvetica", 12, "bold"), bg="white"
        )
        password_label.place(relx=0.5, rely=0.5, anchor="center")

        # Password entry
        self.password_entry = tk.Entry(root, show="*", font=("Helvetica", 12, "bold"))
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry.insert(0, "")  # Default text

        # threading.Thread(target=self.load_image_main, args=(img_path,)).start()
        #this is to fix our gui time consuming problem
        
        # Login button
        self.login_button = tk.Button(
            root, text="Login", command=self.login, font=("Helvetica", 14)
        )
        self.login_button.place(
            relx=0.5, rely=0.65, anchor="center", width=100, height=30
        )

        # Exit button
        self.exit_button = tk.Button(
            root, text="Exit", command=root.destroy, font=("Helvetica", 14)
        )
        self.exit_button.place(
            relx=0.5, rely=0.75, anchor="center", width=100, height=30
        )

        # Credits button
        self.credits_button = tk.Button(
            root, text="Credits", command=self.show_credits, font=("Helvetica", 14)
        )
        self.credits_button.place(
            relx=0.5, rely=0.85, anchor="center", width=100, height=30
        )

        # Bind the Enter key to the login function
        root.bind("<Return>", lambda event: self.login())

        # Bind the Escape key to the exit function
        root.bind("<Escape>", lambda event: root.destroy())

    def load_image_main(self, img_path):
        # Load image and adjust canvas size
        self.original_company_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_main()

    def load_image_common(self):
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        try:
            self.original_common_image = Image.open(img_path)
        except Exception as e:
            print(f"Error loading image: {e}")
        
    def resize_canvas_and_image_common(self,username,role):
        window_width = self.common_canvas.winfo_width()
        window_height = self.common_canvas.winfo_height()
        self.common_canvas.config(width=window_width, height=window_height)

        resized_image = self.original_common_image.resize((window_width, window_height))
        self.common_image = ImageTk.PhotoImage(resized_image)

        self.common_canvas.delete("all")
        self.common_canvas.create_image(0, 0, image=self.common_image, anchor="nw")

        # Add text to the top center of the canvas
        text_content = f"Hello, {username}"
        text_position = (window_width // 2, 20)  # Top center of the canvas
        self.common_canvas.create_text(text_position, text=text_content, anchor="center")
        self.common_canvas.itemconfig(self.common_canvas.find_all()[-1], fill="white")
        
        # if role=="employee":
        #     list=self.getdata(username)
        #     text1=f"EID: {list[0]}\nName: {username}\nDesignation: {list[1]}\nSalary: {list[2]}\nHours Attended: {list[3]}\nBonus: {list[4]}\nSick Days: {list[5]}\nVacation Days: {list[6]}\nSurvey: {list[7]}"
        #     self.common_canvas.create_text(
        #         10,  # X-coordinate (left)
        #         self.common_canvas.winfo_height() - 10,  # Y-coordinate (bottom)
        #         font=("Helvetica", 15, "bold"),
        #         text=text1,
        #         fill="white",
        #         anchor="sw"  # Anchor to bottom left
        #     )
    
    def getdata(self,username,role):
        if role=="employee":
            emp_ref = db.reference("/employee")
            list=[]
            list.append(emp_ref.child(username).child("emp_id").get())
            list.append(emp_ref.child(username).child("designation").get())
            list.append(emp_ref.child(username).child("salary").get())
            list.append(emp_ref.child(username).child("hours_attended").get())
            list.append(emp_ref.child(username).child("bonus").get())
            list.append(emp_ref.child(username).child("sick_days").get())
            list.append(emp_ref.child(username).child("vacation_days").get())
            list.append(emp_ref.child(username).child("survey").child("available").get())
            
            return list
        elif role=="boss":
            boss_ref = db.reference("/boss")
            list=[]
            list.append(boss_ref.child(username).child("boss_id").get())
            list.append(boss_ref.child(username).child("designation").get())
            list.append(boss_ref.child(username).child("salary").get())
            list.append(boss_ref.child(username).child("hours_attended").get())
            list.append(boss_ref.child(username).child("bonus").get())
            list.append(boss_ref.child(username).child("sick_days").get())
            list.append(boss_ref.child(username).child("vacation_days").get())
            
            return list
        elif role=="HR":
            hr_ref = db.reference("/HR")
            list=[]
            list.append(hr_ref.child(username).child("hr_id").get())
            list.append(hr_ref.child(username).child("designation").get())
            list.append(hr_ref.child(username).child("salary").get())
            list.append(hr_ref.child(username).child("hours_attended").get())
            list.append(hr_ref.child(username).child("bonus").get())
            list.append(hr_ref.child(username).child("sick_days").get())
            list.append(hr_ref.child(username).child("vacation_days").get())
            
            return list
    
    def on_window_resize_common(self,username,role, event=None):
        self.resize_canvas_and_image_common(username,role)
    
    def create_common_window(self, title,username,role):
    
        common_window = tk.Tk()
        common_window.geometry("800x600")
        common_window.title(title)

        self.common_canvas = tk.Canvas(common_window, bg="white", highlightthickness=0)
        self.common_canvas.pack(fill=tk.BOTH, expand=True)

        common_window.bind("<Configure>",lambda event,username=username,role=role:self.on_window_resize_common(username,role))

        self.load_image_common()
        self.resize_canvas_and_image_common(username,role)
        
        return common_window, self.common_canvas
        
    def center_window_all(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (900 / 2)
        y = (screen_height / 2) - (600 / 2)
        window.geometry("%dx%d+%d+%d" % (900, 600, x, y))
        
    def resize_canvas_and_image_main(self):
        # Get the current window size
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Resize the canvas to the current window size
        self.company_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_company_logo_image.resize(
            (window_width, window_height)
        )
        self.company_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.company_logo_canvas.delete("all")
        self.company_logo_canvas.create_image(
            0, 0, image=self.company_logo_image, anchor="nw"
        )

        # Redraw the company name text
        if hasattr(self, "company_name_text"):
            self.company_logo_canvas.delete(
                self.company_name_text
            )  # Remove the old text
        self.company_name_text = self.company_logo_canvas.create_text(
            window_width / 2,
            100,
            text="Ben Dover Inc",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    def on_window_resize_main(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_main()

    def show_credits(self):
        # Create a new Toplevel window for the credits
        credits_dialog = tk.Toplevel(self.root)
        credits_dialog.title("Credits")

        # You can customize the credits information as per your needs
        credits_text = (
            "HR Management System\n\n"
            "Developed by: \n -Samay Pandey, \n-Armaan Nakhuda, \n-Sushant Navle, \n-Peeyush Karnik(assuming he does any work)\n\n"
            "Stage Completition: Stage 4 completed\n Stage 5/6 in progress\n"
            "Date: 6th Feb 2024\n"
            "\nSpecial Thanks to:\n- Firebase\n- OpenAI\n- Yash Patil\n- Zane Fernandes\n- Ninad Walke\n"
        )
        
        # Create a label for credits information
        credits_label = tk.Label(
            credits_dialog, text=credits_text, font=("Helvetica", 12)
        )
        credits_label.pack(padx=20, pady=20)

        # Center the credits dialog relative to the main application window
        credits_dialog.update_idletasks()

        app_x = self.root.winfo_x()
        app_y = self.root.winfo_y()
        app_width = self.root.winfo_width()
        app_height = self.root.winfo_height()

        credits_width = credits_dialog.winfo_width()
        credits_height = credits_dialog.winfo_height()

        x = app_x + (app_width - credits_width) // 2
        y = app_y + (app_height - credits_height) // 2

        credits_dialog.geometry(f"{credits_width}x{credits_height}+{x}+{y}")

        credits_dialog.mainloop()

    def profile(self,username,role):
        # Create a new Toplevel window for the profile
        profile_dialog = tk.Toplevel()
        profile_dialog.title("Profile")
        profile_dialog.geometry("800x600")
        
        # Create a canvas that resizes with the window
        self.profile_canvas = tk.Canvas(profile_dialog, bg="white", highlightthickness=0)
        self.profile_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Import the image as the background on the canvas
        self.load_image_profile(username,role)
        
        # Bind window resize event to function
        profile_dialog.bind("<Configure>", lambda event: self.on_window_resize_profile(username,role, event))
        
        # Create an exit button in canvas and place at middle of screen
        exit_button = tk.Button(
            self.profile_canvas,
            text="Exit",
            command=profile_dialog.destroy,
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="#FF4500",
            activebackground="#FF6347",
        )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")
        
        # Focus on window
        profile_dialog.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(profile_dialog)
        
        # Bind the Escape key to the exit function
        profile_dialog.bind("<Escape>", lambda event: profile_dialog.destroy())
        
        # Run the main loop for the profile window
        profile_dialog.mainloop()
        
    def load_image_profile(self,username,role):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_profile_image = Image.open(img_path)
        self.resize_canvas_and_image_profile(username,role)
        
    def resize_canvas_and_image_profile(self,username,role, event=None):
        # Get the profile window size
        window_width = self.profile_canvas.winfo_width()
        window_height = self.profile_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.profile_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_profile_image.resize((window_width, window_height))
        self.profile_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.profile_canvas.delete("all")
        self.profile_canvas.create_image(0, 0, image=self.profile_image, anchor="nw")

        list=self.getdata(username,role)
        text1=f"EID: {list[0]}\nName: {username}\nRole: {role}\nDesignation: {list[1]}\nSalary: {list[2]}\nHours Attended: {list[3]}\nBonus: {list[4]}\nSick Days: {list[5]}\nVacation Days: {list[6]}"
        if role=="employee":
            text1+=f"\nSurvey: {list[7]}"
        self.profile_canvas.create_text(
            10,  # X-coordinate (left)
            self.profile_canvas.winfo_height() - 10,  # Y-coordinate (bottom)
            font=("Helvetica", 15, "bold"),
            text=text1,
            fill="white",
            anchor="sw"  # Anchor to bottom left
        )
        
    def on_window_resize_profile(self,username,role, event=None):
        self.resize_canvas_and_image_profile(username,role)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username or password is empty
        if not username or not password:
            messagebox.showerror(
                "Login Failed", "Username and password are required. Please enter both."
            )
            return

        admins_ref = db.reference("/admins")
        hr_ref = db.reference("/HR")
        boss_ref = db.reference("/boss")
        employee_ref = db.reference("/employee")

        if admins_ref.child(username).child("password").get() == password:
            role = admins_ref.child(username).child("role").get()
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!\nYou are logged in as a {role}.",
            )
            self.open_admin_window(role, username)
            return

        if hr_ref.child(username).child("password").get() == password:
            role = hr_ref.child(username).child("role").get()
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!\nYou are logged in as a {role}.",
            )
            self.open_hr_window(role, username)
            return

        if boss_ref.child(username).child("password").get() == password:
            role = boss_ref.child(username).child("role").get()
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!\nYou are logged in as a {role}.",
            )
            self.open_boss_window(role, username)
            return

        if employee_ref.child(username).child("password").get() == password:
            role = employee_ref.child(username).child("role").get()
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!\nYou are logged in as a {role}.",
            )
            self.open_employee_window(role, username)
            return

        messagebox.showerror(
            "Login Failed", "Invalid username or password. Please try again."
        )

    def open_admin_window(self, role, username):
        if hasattr(self, "root") and self.root.winfo_exists():
            self.root.destroy()  # Close the main login window
        # admin_window = tk.Tk()  # Use Tk() to create a new window
        # admin_window.geometry("900x600")  # Set the window size
        # admin_window.title("Admin Window")
        admin_window,self.admin_logo_canvas=self.create_common_window("Admin Window",username,role)
        # window_width = self.admin_logo_canvas.winfo_width()
        # window_height = self.admin_logo_canvas.winfo_height()
         # create a canvas that resizes with the window
        # self.admin_logo_canvas = tk.Canvas(admin_window, bg="white", highlightthickness=0)
        # self.admin_logo_canvas.pack(fill=tk.BOTH, expand=True)
        
        #put a text onto the canvas and redraw the canvas
    #     self.admin_logo_canvas.create_text(
    #         window_width / 2,
    #         100,
    #         text=f"Welcome {username}!",
    #         font=("Helvetica", 28, "bold"),
    #         fill="white",
    #         tag="welcome_text"
    #     )
    # # Raise the text to make sure it's on top
    #     self.admin_logo_canvas.tag_raise("welcome_text")
    #     # Force an immediate redraw
    #     self.admin_logo_canvas.update_idletasks()
    #     self.admin_logo_canvas.update()
        
        # bind window resize event to function
        # admin_window.bind("<Configure>", lambda event: self.on_window_resize_common(event))

        #create a button on the canvas
        self.create_all_admin_button = tk.Button(
            self.admin_logo_canvas, text="Create HR Login", command=lambda:self.create_all_admin(), font=("Helvetica", 14)
        )
        self.create_all_admin_button.pack(
            pady=20
        )
        self.create_all_admin_button.place(
            relx=0.5, rely=0.4, anchor="center", width=200, height=30
        )
        self.remove_all_admin_button = tk.Button(
            self.admin_logo_canvas, text="Remove HR Login", command=lambda:self.remove_all_admin(), font=("Helvetica", 14)
        )
        self.remove_all_admin_button.pack(
            pady=20
        )
        self.remove_all_admin_button.place(
            relx=0.5, rely=0.5, anchor="center", width=200, height=30
        )
        
        #create combo box to select the role
        self.role_entry = ttk.Combobox(
            self.admin_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("HR", "boss", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.6, anchor="center")
        self.role_entry.current(0)
        
        #create a new button to login as the selected role
        self.login_as_button = tk.Button(
            self.admin_logo_canvas, text="Login as selected role", command=lambda:self.login_as_selected_role(username,admin_window), font=("Helvetica", 14)
        )
        self.login_as_button.pack(
            pady=20
        )
        self.login_as_button.place(
            relx=0.5, rely=0.7, anchor="center", width=200, height=30
        )
        
         # bind window resize event to function
        #admin_window.bind("<Configure>", lambda event: self.on_window_resize_common(event,username))
        
         # import the image as the background on the canvas
        # self.load_image_admin(username)

        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.admin_logo_canvas,
        text="Exit",
        command=admin_window.destroy,
        font=("Helvetica", 14),
        width=15,
        height=2,
        bd=0,
        fg="white",
        bg="#FF4500",
        activebackground="#FF6347",
    )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")

        # focus on window
        admin_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(admin_window)

        # Bind the Escape key to the exit function
        admin_window.bind("<Escape>", lambda event: admin_window.destroy())

        # Run the main loop for the admin window
        admin_window.mainloop()

    def login_as_selected_role(self,username,admin_window):
        role = self.role_entry.get()
        admin_window.destroy()
        if role == "HR":
            self.open_hr_window(role, username)
        elif role == "boss":
            self.open_boss_window(role, username)
        elif role == "employee":
            self.open_employee_window(role, username)
            
    def load_image_admin(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_admin_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_admin(username)
    
    def resize_canvas_and_image_admin(self,username):
        username_admin = username
        # Get the admin window size
        window_width = self.admin_logo_canvas.winfo_width()
        window_height = self.admin_logo_canvas.winfo_height()
       

        # Resize the canvas to the current window size
        self.admin_logo_canvas.config(width=window_width, height=window_height)


        # Resize the image if needed
        resized_image = self.original_company_logo_image.resize(
            (window_width, window_height)
        )
        self.admin_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.admin_logo_canvas.delete("all")
        self.admin_logo_canvas.create_image(
            0, 0, image=self.admin_logo_image, anchor="nw"
        )

         #redraw the admin name text    
        if hasattr(self, "admin_name_text"):
            self.admin_logo_canvas.delete(
                self.admin_name_text
            )  # Remove the old text
        self.admin_name_text = self.admin_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_admin}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )
    
    def on_window_resize_admin(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_admin(username)

    def create_all_admin(self):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Create HR Login")

        #create a canvas that resizes with the window
        self.create_hr_logo_canvas = tk.Canvas(create_remove_hr_window, bg="white", highlightthickness=0)
        self.create_hr_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        create_remove_hr_window.bind("<Configure>", lambda event: self.on_window_resize_create_hr(event))

        # import the image as the background on the canvas
        self.load_image_create_hr()

        #create a new entry for username on canvas
        username_label = tk.Label(
            self.create_hr_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(
            pady=20
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(
            self.create_hr_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(
            pady=20
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a new entry for password on canvas
        password_label = tk.Label(
            self.create_hr_logo_canvas,
            text="Password",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        password_label.pack(
            pady=20
        )
        password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(
            self.create_hr_logo_canvas, show="", font=("Helvetica", 12, "bold")
        )
        self.password_entry.pack(
            pady=20
        )
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry.insert(0, "")
        # create a new checkbox for role with options- HR, boss, employee on canvas
        role_label = tk.Label(
            self.create_hr_logo_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        role_label.place(relx=0.5, rely=0.65, anchor="center")
        self.role_entry = ttk.Combobox(
            self.create_hr_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("HR", "boss", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.7, anchor="center")
        self.role_entry.current(0)
        # create a new button for adding the new login on canvas
        add_button = tk.Button(
            self.create_hr_logo_canvas,
            text="Add",
            command=self.add_login_to_database,
            font=("Helvetica", 14),
        )
        add_button.pack(
            pady=20
        )
        add_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        # store the values in 3 variables when the button is pressed
        add_button.bind(
            "<Button-1>",
            lambda event: self.add_login_to_database(create_remove_hr_window),
        )
        # Bind the Escape key to the exit function
        create_remove_hr_window.bind(
            "<Escape>", lambda event: create_remove_hr_window.destroy()
        )
        # focus on window
        create_remove_hr_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(create_remove_hr_window)
        # Run the main loop for the create_remove_hr_window
        create_remove_hr_window.mainloop()

    def load_image_create_hr(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_create_hr_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_create_hr()

    def resize_canvas_and_image_create_hr(self):
        # Get the create_hr window size
        window_width = self.create_hr_logo_canvas.winfo_width()
        window_height = self.create_hr_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.create_hr_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_create_hr_logo_image.resize(
            (window_width, window_height)
        )
        self.create_hr_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.create_hr_logo_canvas.delete("all")
        self.create_hr_logo_canvas.create_image(
            0, 0, image=self.create_hr_logo_image, anchor="nw"
        )

    def on_window_resize_create_hr(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_create_hr()

    def remove_all_admin(self):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Remove HR Login")

        #create a canvas that resizes with the window
        self.remove_hr_logo_canvas = tk.Canvas(create_remove_hr_window, bg="white", highlightthickness=0)
        self.remove_hr_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        create_remove_hr_window.bind("<Configure>", lambda event: self.on_window_resize_remove_hr(event))

        # import the image as the background on the canvas
        self.load_image_remove_hr()

        #create a new entry for username on canvas
        username_label = tk.Label(
            self.remove_hr_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(
            pady=20
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(
            self.remove_hr_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(
            pady=20
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a checkbox for role with options- HR, boss, employee on canvas
        role_label = tk.Label(
            self.remove_hr_logo_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        role_label.place(relx=0.5, rely=0.5, anchor="center")
        self.role_entry = ttk.Combobox(
            self.remove_hr_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("HR", "boss", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.role_entry.current(0)
        # create a new button for removing the login on canvas
        remove_button = tk.Button(
            self.remove_hr_logo_canvas,
            text="Remove",
            command=self.remove_login_from_database,
            font=("Helvetica", 14),
        )
        remove_button.pack(
            pady=20
        )
        remove_button.place(relx=0.5, rely=0.65, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        remove_button.bind(
            "<Button-1>",
            lambda event: self.remove_login_from_database(create_remove_hr_window),
        )
        # Bind the Escape key to the exit function
        create_remove_hr_window.bind(
            "<Escape>", lambda event: create_remove_hr_window.destroy()
        )
        # focus on window
        create_remove_hr_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(create_remove_hr_window)

    def load_image_remove_hr(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_remove_hr_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_remove_hr()

    def resize_canvas_and_image_remove_hr(self):
        # Get the remove_hr window size
        window_width = self.remove_hr_logo_canvas.winfo_width()
        window_height = self.remove_hr_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.remove_hr_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_remove_hr_logo_image.resize(
            (window_width, window_height)
        )
        self.remove_hr_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.remove_hr_logo_canvas.delete("all")
        self.remove_hr_logo_canvas.create_image(
            0, 0, image=self.remove_hr_logo_image, anchor="nw"
        )

    def on_window_resize_remove_hr(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_remove_hr()

    def open_hr_window(self, role, username):
        # self.root.destroy()  # Close the main login window
        # hr_window = tk.Tk()  # Use Tk() to create a new window
        # hr_window.geometry("800x600")  # Set the window size
        # hr_window.title("HR Window")
        if hasattr(self, "root"):
            try:
                if self.root.winfo_exists():
                    self.root.destroy()  # Close the main login window
            except:
                pass
            
        self.treeview = None
        
        hr_window,self.hr_logo_canvas=self.create_common_window("HR Window",username,role)
        
        # create a canvas that resizes with the window
        # self.hr_logo_canvas = tk.Canvas(hr_window, bg="white", highlightthickness=0)
        # self.hr_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        # hr_window.bind("<Configure>", lambda event: self.on_window_resize_hr(event,username))

        # import the image as the background on the canvas
        # self.load_image_hr(username)


        #buttons of HR window
        self.salary_management_button = tk.Button(
            self.hr_logo_canvas, text="Salary Management", command=lambda:self.salary_management(), font=("Helvetica", 14)
        )
        self.salary_management_button.pack(
            pady=20
        )
        self.salary_management_button.place(
            relx=0.75, rely=0.3, anchor="center", width=200, height=30
        )
        self.employee_add_remove_button = tk.Button(
            self.hr_logo_canvas, text="Employee Add/Remove", command=lambda:self.employee_add_remove(), font=("Helvetica", 14)
        )
        self.employee_add_remove_button.pack(
            pady=20
        )
        self.employee_add_remove_button.place(
            relx=0.75, rely=0.375, anchor="center", width=230, height=30
        )
        self.approve_bonus_button = tk.Button(
            self.hr_logo_canvas, text="Approve Bonus", command=lambda:self.approve_bonus(), font=("Helvetica", 14)
        )
        self.approve_bonus_button.pack(
            pady=20
        )
        self.approve_bonus_button.place(

            relx=0.75, rely=0.450, anchor="center", width=200, height=30
        )
        self.approve_resignation_button = tk.Button(
            self.hr_logo_canvas, text="Approve Resignation", command=lambda:self.approve_resignation(), font=("Helvetica", 14)
        )
        self.approve_resignation_button.pack(
            pady=20
        )
        self.approve_resignation_button.place(
            relx=0.75, rely=0.525, anchor="center", width=200, height=30
        )
        self.check_hours_attended_button = tk.Button(
            self.hr_logo_canvas, text="Check Employee Hours Attended", command=lambda:self.check_hours_attended(), font=("Helvetica", 14)
        )
        self.check_hours_attended_button.pack(
            pady=20
        )
        self.check_hours_attended_button.place(
            relx=0.75, rely=0.6, anchor="center", width=300, height=30
        )
        self.survey_feedback_button = tk.Button(
            self.hr_logo_canvas, text="Survey/Feedback", command=lambda:self.survey_feedback(), font=("Helvetica", 14)
        )
        self.survey_feedback_button.pack(
            pady=20
        )
        self.survey_feedback_button.place(
            relx=0.75, rely=0.675, anchor="center", width=200, height=30
        )
        self.addbe_button = tk.Button(
            self.hr_logo_canvas, text="Add Boss/Employee", command=lambda:self.create_all_hr(), font=("Helvetica", 14)
        )
        self.addbe_button.pack(
            pady=20
        )
        self.addbe_button.place(
            relx=0.75, rely=0.750, anchor="center", width=300, height=30
        )
        self.removebe_button = tk.Button(
            self.hr_logo_canvas, text="Remove Boss/Employee", command=lambda:self.remove_all_hr(), font=("Helvetica", 14)
        )
        self.removebe_button.pack(
            pady=20
        )
        self.removebe_button.place(
            relx=0.75, rely=0.825, anchor="center", width=300, height=30
        )

        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.hr_logo_canvas,
        text="Exit",
        command=hr_window.destroy,
        font=("Helvetica", 14),
        width=15,
        height=2,
        bd=0,
        fg="white",
        bg="#FF4500",
        activebackground="#FF6347",
    )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")
        
        profile_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "profile.png" #change jpg to png for main background
        )
        profile_img = PhotoImage(file=profile_path)
        
        resized_profile_img = profile_img.subsample(4, 4)
        
        profile_btn = tk.Button(
            self.hr_logo_canvas, image=resized_profile_img, command=lambda:self.profile(username,role),borderwidth=0, font=("Helvetica", 14)
        )
        profile_btn.pack(
            pady=20
        )
        profile_btn.place(
            relx=0.95, rely=0.05, anchor="center", width=50, height=50
        )

        # focus on window
        hr_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(hr_window)

        # Bind the Escape key to the exit function
        hr_window.bind("<Escape>", lambda event: hr_window.destroy())

        #  Run the main loop for the HR window
        hr_window.mainloop()
        
    def load_image_hr(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_hr_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_hr(username)

    def resize_canvas_and_image_hr(self,username):
        username_hr = username
        # Get the hr window size
        window_width = self.hr_logo_canvas.winfo_width()
        window_height = self.hr_logo_canvas.winfo_height()
       

        # Resize the canvas to the current window size
        self.hr_logo_canvas.config(width=window_width, height=window_height)


        # Resize the image if needed
        resized_image = self.original_hr_logo_image.resize(
            (window_width, window_height)
        )
        self.hr_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.hr_logo_canvas.delete("all")
        self.hr_logo_canvas.create_image(
            0, 0, image=self.hr_logo_image, anchor="nw"
        )

         #redraw the hr name text    
        if hasattr(self, "hr_name_text"):
            self.hr_logo_canvas.delete(
                self.hr_name_text
            )
        self.hr_name_text = self.hr_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_hr}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    def on_window_resize_hr(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_hr(username)

    def salary_management(self):
        #create a frame with clickable text
        salary_management_frame = tk.Toplevel()
        salary_management_frame.geometry("800x600")  # Set the window size
        salary_management_frame.title("Salary Management")
        
        #create a canvas that resizes with the window
        self.salary_management_canvas = tk.Canvas(salary_management_frame, bg="white", highlightthickness=0)
        self.salary_management_canvas.pack(fill=tk.BOTH, expand=True)
        
        # bind window resize event to function
        salary_management_frame.bind("<Configure>", lambda event: self.on_window_resize_salary_management(event))
        
        # import the image as the background on the canvas
        self.load_image_salary_management()
        
        #create a scrollable frame
        self.scrollable_frame = tk.Frame(self.salary_management_canvas, bg="white")
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)
        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        #create a treeview to display the employees
        if self.treeview is None:
            self.treeview = ttk.Treeview(
                self.scrollable_frame, columns=("Employee",), show="headings", selectmode="browse"
            )
            self.treeview.heading("Employee", text="Employee")
            self.treeview.column("Employee", width=200, anchor="center")
            self.treeview.tag_configure("clickable", foreground="blue", font=("Helvetica", 12, "underline"))
            self.treeview.bind("<Double-1>", lambda event: self.open_employee_details_window(self.treeview.item(self.treeview.selection())["values"][0]))

            # Add a vertical scrollbar to the Treeview
            scrollbar = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.treeview.yview)
            scrollbar.pack(side="right", fill="y")
            self.treeview.configure(yscrollcommand=scrollbar.set)

            # Pack the Treeview to the scrollable frame
            self.treeview.pack(fill="both", expand=True)

        # Configure grid row and column weights
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)


        # Now you can safely use self.treeview
        self.treeview.delete(*self.treeview.get_children())
        
        #create a tick box for role of the employee
        role_label = tk.Label(
            self.salary_management_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        #place it Extreme top middle
        role_label.place(relx=0.5, rely=0.1, anchor="center")
        self.role_entry = ttk.Combobox(
            self.salary_management_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("None","HR", "boss", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.2, anchor="center")
        self.role_entry.current(0)
        
        self .role_entry.bind("<<ComboboxSelected>>", self.role_selected)
        
        #center the window
        self.center_window_all(salary_management_frame)
        
        #focus on window
        salary_management_frame.focus_force()
        
        #bind the escape key to the exit function
        salary_management_frame.bind("<Escape>", lambda event: salary_management_frame.destroy())
        
        # Run the main loop for the salary_management_frame
        salary_management_frame.mainloop()
        
    def role_selected(self, event):
        selected_role = self.role_entry.get()
        if selected_role:
            self.populate_employee_list(selected_role)
    
    def populate_employee_list(self, role):
        # Clear the existing items in the Treeview
        self.treeview.delete(*self.treeview.get_children())
        
        if role == "HR":
            employees = list(( db.reference("/HR").get()).keys())
        elif role == "boss":
            employees = list(( db.reference("/boss").get()).keys())
        elif role == "None":
            return
        else:
            employees = list(( db.reference("/employee").get()).keys())

        # Populate the Treeview with employee names
        for employee in employees:
            self.treeview.insert("", "end", values=(employee,), tags=("clickable",))

    def open_employee_details_window(self, employee_name):
        #Function to open another window with employee details
        employee_details_window = tk.Toplevel()
        employee_details_window.geometry("400x300")
        employee_details_window.title(f"Details for {employee_name}")
        employee_details_window.focus_force()
        
        #create a canvas that resizes with the window
        self.employee_details_canvas = tk.Canvas(employee_details_window, bg="white", highlightthickness=0)
        self.employee_details_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.load_image_employee_details_new(employee_name)
        
        # bind window resize event to function
        employee_details_window.bind("<Configure>", lambda event: self.on_window_resize_employee_details_new(employee_name,event))
        
        #create a button to edit salary
        edit_salary_button = tk.Button(
            self.employee_details_canvas,
            text="Edit Salary",
            command=lambda:self.edit_salary(employee_name),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        edit_salary_button.place(relx=0.2, rely=0.9, anchor="s")
        
        #create a button to edit bonus
        edit_bonus_button = tk.Button(
            self.employee_details_canvas,
            text="Edit Bonus",
            command=lambda:self.edit_bonus(employee_name),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        edit_bonus_button.place(relx=0.8, rely=0.9, anchor="s")
        
        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.employee_details_canvas,
        text="Exit",
        command=employee_details_window.destroy,
        font=("Helvetica", 14),
        width=15,
        height=2,
        bd=0,
        fg="white",
        bg="#FF4500",
        activebackground="#FF6347",
    )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")
        
        # Center the window with function center_window_test
        self.center_window_all(employee_details_window)
        
        # Bind the Escape key to the exit function
        employee_details_window.bind("<Escape>", lambda event: self.handle_employee_details_window_exit(event, employee_details_window))
        
        # Run the main loop for the employee details window
        employee_details_window.mainloop()
        
    def handle_employee_details_window_exit(self, event, employee_details_window):
        if hasattr(self, "salary_management_canvas") and self.salary_management_canvas.winfo_exists():
            self.salary_management_canvas.focus_force()
            
    def edit_salary(self, employee_name):
        #Create a window to edit the salary of the employee
        edit_salary_window = tk.Toplevel()
        edit_salary_window.geometry("400x300")
        edit_salary_window.title(f"Edit Salary for {employee_name}")
        
        #create an entry for new salary
        new_salary_label = tk.Label(
            edit_salary_window,
            text="New Salary",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        new_salary_label.pack(
            pady=20
        )
        new_salary_label.place(relx=0.5, rely=0.3, anchor="center")
        
        #Create an entry for the new salary
        self.new_salary_entry = tk.Entry(
            edit_salary_window, font=("Helvetica", 12, "bold")
        )
        self.new_salary_entry.pack(
            pady=20
        )
        self.new_salary_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.new_salary_entry.insert(0, "")
        #create a submit button to change the salary
        submit_button = tk.Button(
            edit_salary_window,
            text="Submit",
            command=lambda:self.new_submit_salary(employee_name, edit_salary_window),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        submit_button.place(relx=0.5, rely=0.9, anchor="s")
        
        #bind the enter key to the submit button
        edit_salary_window.bind("<Return>", lambda event: self.new_submit_salary(employee_name, edit_salary_window))
        
        #bind the escape key to the exit function
        edit_salary_window.bind("<Escape>", lambda event: edit_salary_window.destroy())
        
        #center the window
        self.center_window_all(edit_salary_window)
        
        #focus on window
        edit_salary_window.focus_force()
        
        # Run the main loop for the edit_salary_window
        edit_salary_window.mainloop()
        
    def new_submit_salary(self, employee_name, edit_salary_window):
        #Get the new salary from the entry
        new_salary = self.new_salary_entry.get()
        #Ask for confirmation 
        if messagebox.askyesno("Confirm", f"Are you sure you want to change the salary of {employee_name} to {new_salary}?"):
            #Change the salary in the database
            db.reference("/employee").child(employee_name).child("salary").set(new_salary)
        #Close the window
        edit_salary_window.destroy()
        #focus on the salary management window
        self.employee_details_canvas.focus_force()
                    
    def edit_bonus(self, employee_name):
        #Create a window to edit the bonus of the employee
        edit_bonus_window = tk.Toplevel()
        edit_bonus_window.geometry("400x300")
        edit_bonus_window.title(f"Edit Bonus for {employee_name}")
        
        #create an entry for new bonus
        new_bonus_label = tk.Label(
            edit_bonus_window,
            text="New Bonus",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        new_bonus_label.pack(
            pady=20
        )
        new_bonus_label.place(relx=0.5, rely=0.3, anchor="center")
        
        #Create an entry for the new bonus
        self.new_bonus_entry = tk.Entry(
            edit_bonus_window, font=("Helvetica", 12, "bold")
        )
        self.new_bonus_entry.pack(
            pady=20
        )
        self.new_bonus_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.new_bonus_entry.insert(0, "")
        #create a submit button to change the bonus
        submit_button = tk.Button(
            edit_bonus_window,
            text="Submit",
            command=lambda:self.new_submit_bonus(employee_name, edit_bonus_window),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        submit_button.place(relx=0.5, rely=0.9, anchor="s")
        
        #bind the enter key to the submit button
        edit_bonus_window.bind("<Return>", lambda event: self.new_submit_bonus(employee_name, edit_bonus_window))
        
        #bind the escape key to the exit function
        edit_bonus_window.bind("<Escape>", lambda event: edit_bonus_window.destroy())
        
        #center the window
        self.center_window_all(edit_bonus_window)
        
        #focus on window
        edit_bonus_window.focus_force()
        
        # Run the main loop for the edit_bonus_window
        edit_bonus_window.mainloop()
        
    def new_submit_bonus(self, employee_name, edit_bonus_window):
        #Get the new bonus from the entry
        new_bonus = self.new_bonus_entry.get()
        #Ask for confirmation 
        if messagebox.askyesno("Confirm", f"Are you sure you want to change the bonus of {employee_name} to {new_bonus}?"):
            #Change the bonus in the database
            db.reference("/employee").child(employee_name).child("bonus").set(new_bonus)
        #Close the window
        edit_bonus_window.destroy()
        #focus on the salary management window
        self.employee_details_canvas.focus_force()
    
    def load_image_employee_details_new(self,employee_name):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_employee_details_image = Image.open(img_path)
        self.resize_canvas_and_image_employee_details_new(employee_name)
        
    def resize_canvas_and_image_employee_details_new(self,employee_name):
        # Get the employee details window size
        window_width = self.employee_details_canvas.winfo_width()
        window_height = self.employee_details_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.employee_details_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_employee_details_image.resize(
            (window_width, window_height)
        )
        self.employee_details_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.employee_details_canvas.delete("all")
        self.employee_details_canvas.create_image(
            0, 0, image=self.employee_details_image, anchor="nw"
        )
        
        #create text with employee name, role, salary, hours attended, bonus
        employee_details_text="Employee Name: "+str(employee_name)+"\nRole: "+str(db.reference("/employee").child(employee_name).child("role").get())+"\nSalary: "+str(db.reference("/employee").child(employee_name).child("salary").get())+"\nHours Attended: "+str(db.reference("/employee").child(employee_name).child("hours_attended").get())+"\nBonus: "+str(db.reference("/employee").child(employee_name).child("bonus").get())
        self.employee_details_canvas.create_text(
            window_width / 2,
            window_height / 2,
            text=employee_details_text,
            font=("Helvetica", 14, "bold"),
            fill="white",
            tag="employee_details_text"
        )
    
    def on_window_resize_employee_details_new(self,employee_name, event):
        # Handle window resize event
        self.resize_canvas_and_image_employee_details_new(employee_name)
        
    def load_image_salary_management(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_salary_management_image = Image.open(img_path)
        self.resize_canvas_and_image_salary_management()
    
    def resize_canvas_and_image_salary_management(self):
        # Get the salary_management window size
        window_width = self.salary_management_canvas.winfo_width()
        window_height = self.salary_management_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.salary_management_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_salary_management_image.resize(
            (window_width, window_height)
        )
        self.salary_management_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.salary_management_canvas.delete("all")
        self.salary_management_canvas.create_image(
            0, 0, image=self.salary_management_image, anchor="nw"
        )
    
    def on_window_resize_salary_management(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_salary_management()

    def employee_add_remove(self):
        messagebox.showinfo("HR Window", "Employee Add/Remove Button Pressed")

    def approve_bonus(self):
        messagebox.showinfo("HR Window", "Approve Bonus Button Pressed")

    def approve_resignation(self):
        messagebox.showinfo("HR Window", "Approve Resignation Button Pressed")

    def check_hours_attended(self):
        messagebox.showinfo("HR Window", "Check Employee Hours Attended Button Pressed")

    def survey_feedback(self):
        messagebox.showinfo("HR Window", "Survey/Feedback Button Pressed")

    def create_all_hr(self):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Create Boss/Employee Login")

        #create a canvas that resizes with the window
        self.create_be_logo_canvas = tk.Canvas(create_remove_hr_window, bg="white", highlightthickness=0)
        self.create_be_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        create_remove_hr_window.bind("<Configure>", lambda event: self.on_window_resize_create_be(event))

        # import the image as the background on the canvas
        self.load_image_create_be()

        #create a new entry for username on canvas
        username_label = tk.Label(
            self.create_be_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(
            pady=20
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(
            self.create_be_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(
            pady=20
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a new entry for password on canvas
        password_label = tk.Label(
            self.create_be_logo_canvas,
            text="Password",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        password_label.pack(
            pady=20
        )
        password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(

            self.create_be_logo_canvas, show="", font=("Helvetica", 12, "bold")
        )
        self.password_entry.pack(
            pady=20
        )
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry.insert(0, "")
        # create a checkbox for role with options- HR, boss, employee on canvas
        role_label = tk.Label(
            self.create_be_logo_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        role_label.place(relx=0.5, rely=0.65, anchor="center")
        self.role_entry = ttk.Combobox(
            self.create_be_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("boss", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.7, anchor="center")
        self.role_entry.current(0)
        # create a new button for adding the new login on canvas
        add_button = tk.Button(
            self.create_be_logo_canvas,
            text="Add",
            command=self.add_login_to_database,
            font=("Helvetica", 14),
        )
        add_button.pack(
            pady=20
        )
        add_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        # store the values in 3 variables when the button is pressed
        add_button.bind(
            "<Button-1>",
            lambda event: self.add_login_to_database(create_remove_hr_window),
        )
        # Bind the Escape key to the exit function
        create_remove_hr_window.bind(
            "<Escape>", lambda event: create_remove_hr_window.destroy()
        )
        # focus on window
        create_remove_hr_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(create_remove_hr_window)
        # Run the main loop for the create_remove_hr_window
        create_remove_hr_window.mainloop()

    def load_image_create_be(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_create_be_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_create_be()

    def resize_canvas_and_image_create_be(self):
        # Get the create_be window size
        window_width = self.create_be_logo_canvas.winfo_width()
        window_height = self.create_be_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.create_be_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_create_be_logo_image.resize(
            (window_width, window_height)
        )
        self.create_be_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.create_be_logo_canvas.delete("all")
        self.create_be_logo_canvas.create_image(
            0, 0, image=self.create_be_logo_image, anchor="nw"
        )

    def on_window_resize_create_be(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_create_be()

    def remove_all_hr(self):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Remove Boss/Employee Login")
      
        #create a canvas that resizes with the window
        self.remove_be_logo_canvas = tk.Canvas(create_remove_hr_window, bg="white", highlightthickness=0)
        self.remove_be_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        create_remove_hr_window.bind("<Configure>", lambda event: self.on_window_resize_remove_be(event))

        # import the image as the background on the canvas
        self.load_image_remove_be()

        #create a new entry for username on canvas
        username_label = tk.Label(
            self.remove_be_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(
            pady=20
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        self.username_entry = tk.Entry(

            self.remove_be_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(
            pady=20
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a checkbox for role with options- HR, boss, employee on canvas
        role_label = tk.Label(
            self.remove_be_logo_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        role_label.place(relx=0.5, rely=0.5, anchor="center")
        self.role_entry = ttk.Combobox(
            self.remove_be_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("boss", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.role_entry.current(0)
        # create a new button for removing the login on canvas
        remove_button = tk.Button(
            self.remove_be_logo_canvas,
            text="Remove",
            command=self.remove_login_from_database,
            font=("Helvetica", 14),
        )
        remove_button.pack(
            pady=20
        )
        remove_button.place(relx=0.5, rely=0.65, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        remove_button.bind(

            "<Button-1>",
            lambda event: self.remove_login_from_database(create_remove_hr_window),
        )
        # Bind the Escape key to the exit function
        create_remove_hr_window.bind(
            "<Escape>", lambda event: create_remove_hr_window.destroy()
        )
        # focus on window
        create_remove_hr_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(create_remove_hr_window)
        # Run the main loop for the create_remove_hr_window
        create_remove_hr_window.mainloop()

    def load_image_remove_be(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_remove_be_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_remove_be()

    def resize_canvas_and_image_remove_be(self):
        # Get the remove_be window size
        window_width = self.remove_be_logo_canvas.winfo_width()
        window_height = self.remove_be_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.remove_be_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_remove_be_logo_image.resize(
            (window_width, window_height)
        )
        self.remove_be_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.remove_be_logo_canvas.delete("all")
        self.remove_be_logo_canvas.create_image(
            0, 0, image=self.remove_be_logo_image, anchor="nw"
        )

    def on_window_resize_remove_be(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_remove_be()

    def open_boss_window(self, role, username):
        self.root.destroy()  # Close the main login window    
        boss_window = tk.Tk()  # Use Tk() to create a new window
        boss_window.geometry("900x600")  # Set the window size
        boss_window.title("Boss Window")

        #create a canvas that resizes with the window
        self.boss_logo_canvas = tk.Canvas(boss_window, bg="white", highlightthickness=0)
        self.boss_logo_canvas.pack(fill=tk.BOTH, expand=True)

       # bind window resize event to function
        boss_window.bind("<Configure>", lambda event: self.on_window_resize_boss(event,username))

       # import the image as the background on the canvas
        self.load_image_boss(username)

        #buttons of Boss window
        self.perform_review_approval_button = tk.Button(
            self.boss_logo_canvas, text="Performance Review Approval", command=lambda:self.perform_review_approval(), font=("Helvetica", 14)
        )
        self.perform_review_approval_button.pack(
            pady=20
        )
        self.perform_review_approval_button.place(
            relx=0.5, rely=0.3, anchor="center", width=300, height=30
        )
        self.approve_vacations_sick_leaves_button = tk.Button(
            self.boss_logo_canvas, text="Approve Vacations and Sick Leaves", command=lambda:self.approve_vacations_sick_leaves(username,role), font=("Helvetica", 14)
        )
        self.approve_vacations_sick_leaves_button.pack(
            pady=20
        )
        self.approve_vacations_sick_leaves_button.place(
            relx=0.5, rely=0.4, anchor="center", width=320, height=30
        )
        self.progress_on_task_button = tk.Button(
            self.boss_logo_canvas, text="Progress on Task", command=lambda:self.progress_on_task(), font=("Helvetica", 14)
        )
        self.progress_on_task_button.pack(
            pady=20
        )
        self.progress_on_task_button.place(
          relx=0.5, rely=0.5, anchor="center", width=200, height=30
        )
        self.approve_promotion_button = tk.Button(
            self.boss_logo_canvas, text="Approve Promotion", command=lambda:self.approve_promotion(), font=("Helvetica", 14)
        )
        self.approve_promotion_button.pack(
            pady=20
        )
        self.approve_promotion_button.place(
            relx=0.5, rely=0.6, anchor="center", width=200, height=30
        )
        self.approve_resignation_button = tk.Button(
            self.boss_logo_canvas, text="Approve Resignation", command=lambda:self.approve_resignation(), font=("Helvetica", 14)
        )
        self.approve_resignation_button.pack(
            pady=20
        )
        self.approve_resignation_button.place(
            relx=0.5, rely=0.7, anchor="center", width=200, height=30
        )
        self.request_bonus_button = tk.Button(
            self.boss_logo_canvas, text="Request for Bonus", command=lambda:self.request_bonus(), font=("Helvetica", 14)
        )
        self.request_bonus_button.pack(
            pady=20
        )
        self.request_bonus_button.place(
            relx=0.5, rely=0.8, anchor="center", width=200, height=30
        )

        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.boss_logo_canvas,
        text="Exit",
        command=boss_window.destroy,
        font=("Helvetica", 14),
        width=15,
        height=2,
        bd=0,
        fg="white",
        bg="#FF4500",
        activebackground="#FF6347",
    )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")

        # focus on window
        boss_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(boss_window)

        # Bind the Escape key to the exit function
        boss_window.bind("<Escape>", lambda event: boss_window.destroy())

        # Run the main loop for the boss window
        boss_window.mainloop()

    def load_image_boss(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_boss_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_boss(username)

    def resize_canvas_and_image_boss(self,username):
        username_boss = username
        # Get the boss window size
        window_width = self.boss_logo_canvas.winfo_width()
        window_height = self.boss_logo_canvas.winfo_height()
       
        # Resize the canvas to the current window size
        self.boss_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_boss_logo_image.resize(
            (window_width, window_height)
        )
        self.boss_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.boss_logo_canvas.delete("all")
        self.boss_logo_canvas.create_image(
            0, 0, image=self.boss_logo_image, anchor="nw"
        )

         #redraw the boss name text    
        if hasattr(self, "boss_name_text"):
            self.boss_logo_canvas.delete(
                self.boss_name_text
            )  # Remove the old text

        self.boss_name_text = self.boss_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_boss}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    def on_window_resize_boss(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_boss(username)

    def perform_review_approval(self):
        messagebox.showinfo("Boss Window", "Performance Review Approval Button Pressed")

    def approve_vacations_sick_leaves(self, role, username):
        approve_window = tk.Toplevel()  # Use Tk() to create a new window
        approve_window.geometry("800x600")  # Set the window size
        approve_window.title("Approve Vacations and Sick Leaves")


        #create a canvas that resizes with the window
        self.approve_leaves_logo_canvas = tk.Canvas(approve_window, bg="white", highlightthickness=0)
        self.approve_leaves_logo_canvas.pack(fill=tk.BOTH, expand=True)

       # bind window resize event to function
        approve_window.bind("<Configure>", lambda event: self.on_window_resize_approve_leaves(event,username))

       # import the image as the background on the canvas
        self.load_image_approve_leaves(username)


     # Assuming you have values for the employee data
        employee_data_with_provisional_vacation_above_zero = self.get_employee_data_with_provisional_vacation_above_zero(username)
        employee_data_with_sick_days_above_zero = self.get_employee_data_with_sick_days_above_zero(username)

     # Call the method with different rely values and click handlers for each list
        self.display_employee_list_on_canvas(
            self.approve_leaves_logo_canvas,
            employee_data_with_provisional_vacation_above_zero,
            rely=0.2,
            click_handler=self.show_employee_details_vacation
        )

        self.display_employee_list_on_canvas(
            self.approve_leaves_logo_canvas,
            employee_data_with_sick_days_above_zero,
            rely=0.7,
            click_handler=self.show_employee_details_sick
        )



        # Bind the Escape key to the exit function
        approve_window.bind(
            "<Escape>", lambda event: approve_window.destroy()
        )
        # focus on window
        approve_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(approve_window)
        # Run the main loop for the create_remove_hr_window
        approve_window.mainloop()
               
    def load_image_approve_leaves(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_approve_leaves_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_approve_leaves(username)

    def resize_canvas_and_image_approve_leaves(self,username):
        # Get the boss window size
        window_width = self.approve_leaves_logo_canvas.winfo_width()
        window_height = self.approve_leaves_logo_canvas.winfo_height()
       
        # Resize the canvas to the current window size
        self.approve_leaves_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_approve_leaves_logo_image.resize(
            (window_width, window_height)
        )
        self.approve_leaves_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.approve_leaves_logo_canvas.delete("all")
        self.approve_leaves_logo_canvas.create_image(
            0, 0, image=self.approve_leaves_logo_image, anchor="nw"
        )

        #redraw the text vacation days and sick days
        if hasattr(self, "vacation_days_text"):
            self.approve_leaves_logo_canvas.delete(
                self.vacation_days_text
            )
        self.vacation_days_text = self.approve_leaves_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Vacation Days",
            font=("Helvetica", 18, "bold"),
            fill="white",
        )
        if hasattr(self, "sick_days_text"):
            self.approve_leaves_logo_canvas.delete(
                self.sick_days_text
            )
        self.sick_days_text = self.approve_leaves_logo_canvas.create_text(
            window_width / 2,
            400,
            text=f"Sick Days",
            font=("Helvetica", 18, "bold"),
            fill="white",
        )

    def on_window_resize_approve_leaves(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_approve_leaves(username)

    def get_employee_data_with_provisional_vacation_above_zero(self, username):
        emp_ref = db.reference("/employee")
        employee_data_1 = [user for user in emp_ref.get() if self.get_employee_data(user, "vacation_days") > 0]
        return employee_data_1

    def get_employee_data_with_sick_days_above_zero(self, username):
        emp_ref = db.reference("/employee")
        employee_data_2 = [user for user in emp_ref.get() if self.get_employee_data(user, "sick_days") > 0]
        return employee_data_2

    def display_employee_list_on_canvas(self, canvas, employee_data, rely, click_handler=None):
        if len(employee_data) > 0:
            employee_list = Listbox(canvas, font=("Helvetica", 12, "bold"), bg="white", fg="black", width=30, height=5)
            employee_list.pack(pady=20)
            employee_list.place(relx=0.5, rely=rely + 0.09, anchor="center")

            def on_employee_click(event):
                # Clear previous selection
                employee_list.selection_clear(0, tk.END)

                # Get the selected item
                selected_index = employee_list.nearest(event.y)
                employee_info = employee_data[selected_index]

                # Set the selection to the clicked item
                employee_list.selection_set(selected_index)

                # Bind click event to the provided handler function, if available
                if click_handler:
                    click_handler(employee_info)

            # Bind the click event to the custom function
            employee_list.bind("<ButtonRelease-1>", on_employee_click)

            # Insert employee names into the listbox
            for employee_info in employee_data:
                employee_list.insert(tk.END, employee_info)
        else:
            self.display_no_employee_message(canvas, "No employees to approve")

    def display_no_employee_message(self, canvas, message):
        no_employee_label = Label(canvas, text=message, font=("Helvetica", 12, "bold"), bg="white")
        no_employee_label.pack(pady=20)
        no_employee_label.place(relx=0.5, rely=0.5, anchor="center")

    def get_employee_data(self, username, data_type):
        emp_ref = db.reference("/employee")
        data = emp_ref.child(username).child(data_type).get()
        return data if data is not None else 0
    
    def show_employee_details_vacation(self, employee_data_1):
     # create a new window to show employee details along with 2 radio buttons to approve or deny the request
        employee_details_window = tk.Toplevel()
        employee_details_window.geometry("800x600")  # Set the window size
        employee_details_window.title("Vacation Approve/Deny")

        #create a canvas that resizes with the window
        self.employee_details_logo_canvas = tk.Canvas(employee_details_window, bg="white", highlightthickness=0)
        self.employee_details_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        employee_details_window.bind("<Configure>", lambda event: self.on_window_resize_employee_details(event))

        # import the image as the background on the canvas
        self.load_image_employee_details()

        # show the username of the employee using label on the canvas
        username_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(pady=20)
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        self.username_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(pady=20)
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Get the username from the employee data
        username_data = employee_data_1  # Assuming username data is directly available in employee_data_1
        self.username_entry.insert(0, username_data)

        # Make the entry widget read-only
        self.username_entry.configure(state="readonly")

        # show the reason for vacation days of the employee using label on the canvas
        provisional_vacation_days_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Vacation Days",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        provisional_vacation_days_label.pack(pady=20)
        provisional_vacation_days_label.place(relx=0.5, rely=0.5, anchor="center")

        self.provisional_vacation_days_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.provisional_vacation_days_entry.pack(pady=20)
        self.provisional_vacation_days_entry.place(relx=0.5, rely=0.55, anchor="center")

        # Get the vacation days from the employee data
        provisional_vacation_days = self.get_employee_data(employee_data_1, "vacation_days")
        self.provisional_vacation_days_entry.insert(0, provisional_vacation_days)

        # Make the entry widget read-only
        self.provisional_vacation_days_entry.configure(state="readonly")

        # show the reason for vacation days of the employee using label on the canvas
        reason_for_vacation_days_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Reason for Vacation Days",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        reason_for_vacation_days_label.pack(pady=20)
        reason_for_vacation_days_label.place(relx=0.5, rely=0.65, anchor="center")

        self.reason_for_vacation_days_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.reason_for_vacation_days_entry.pack(pady=20)
        self.reason_for_vacation_days_entry.place(relx=0.5, rely=0.7, anchor="center")

        # Get the reason for vacation days from the employee data
        reason_for_vacation_days = self.get_employee_data(employee_data_1, "vacation_reason")

        # Insert the text into the entry widget
        self.reason_for_vacation_days_entry.insert(0, reason_for_vacation_days)

        # Make the entry widget read-only
        self.reason_for_vacation_days_entry.configure(state="readonly")

        # create a new button for approving the vacation days on canvas
        approve_button = tk.Button(
            self.employee_details_logo_canvas,
            text="Approve",
            command=lambda:self.approve_vacation_days(employee_data_1),
            font=("Helvetica", 14),
        )
        approve_button.pack(
            pady=20
        )
        approve_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        approve_button.bind(
            "<Button-1>",
            lambda event: self.approve_vacation_days(employee_data_1),
        )
        # create a new button for denying the vacation days on canvas
        deny_button = tk.Button(
            self.employee_details_logo_canvas,
            text="Deny",
            command=lambda:self.deny_vacation_days(employee_data_1),
            font=("Helvetica", 14),
        )
        deny_button.pack(
            pady=20
        )
        deny_button.place(relx=0.5, rely=0.9, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        deny_button.bind(
            "<Button-1>",
            lambda event: self.deny_vacation_days(employee_data_1),
        )
        # Bind the Escape key to the exit function
        employee_details_window.bind(
            "<Escape>", lambda event: employee_details_window.destroy()
        )
        # focus on window
        employee_details_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(employee_details_window)
        # Run the main loop for the create_remove_hr_window
        employee_details_window.mainloop()

    def show_employee_details_sick(self, employee_data_2):
     # create a new window to show employee details along with 2 radio buttons to approve or deny the request
        employee_details_window = tk.Toplevel()
        employee_details_window.geometry("800x600")  # Set the window size
        employee_details_window.title("Sick Approve/Deny")

        #create a canvas that resizes with the window
        self.employee_details_logo_canvas = tk.Canvas(employee_details_window, bg="white", highlightthickness=0)
        self.employee_details_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        employee_details_window.bind("<Configure>", lambda event: self.on_window_resize_employee_details(event))

        # import the image as the background on the canvas
        self.load_image_employee_details()

        # show the username of the employee using label on the canvas
        username_label = tk.Label(
            self.employee_details_logo_canvas,
            text=f"Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(pady=20)
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        self.username_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(pady=20)
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Get the username from the employee data
        username_data = employee_data_2  # Assuming username data is directly available in employee_data_2
        self.username_entry.insert(0, username_data)

        # Make the entry widget read-only
        self.username_entry.configure(state="readonly")

        # show the reason for sick days of the employee using label on the canvas
        provisional_vacation_days_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Sick Days",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        provisional_vacation_days_label.pack(pady=20)
        provisional_vacation_days_label.place(relx=0.5, rely=0.5, anchor="center")

        self.provisional_vacation_days_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.provisional_vacation_days_entry.pack(pady=20)
        self.provisional_vacation_days_entry.place(relx=0.5, rely=0.55, anchor="center")

        # Get the sick days from the employee data
        provisional_vacation_days = self.get_employee_data(employee_data_2, "sick_days")
        self.provisional_vacation_days_entry.insert(0, provisional_vacation_days)

        # Make the entry widget read-only
        self.provisional_vacation_days_entry.configure(state="readonly")

        # show the reason for sick days of the employee using label on the canvas
        reason_for_sick_days_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Reason for Sick Days",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        reason_for_sick_days_label.pack(pady=20)
        reason_for_sick_days_label.place(relx=0.5, rely=0.65, anchor="center")

        self.reason_for_sick_days_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.reason_for_sick_days_entry.pack(pady=20)
        self.reason_for_sick_days_entry.place(relx=0.5, rely=0.7, anchor="center")

        # Get the reason for sick days from the employee data
        reason_for_sick_days = self.get_employee_data(employee_data_2, "sick_reason")

        # Insert the text into the entry widget
        self.reason_for_sick_days_entry.insert(0, reason_for_sick_days)

        # Make the entry widget read-only
        self.reason_for_sick_days_entry.configure(state="readonly")

        # create a new button for approving the vacation days on canvas
        approve_button = tk.Button(
            self.employee_details_logo_canvas,
            text="Approve",
            command=lambda:self.approve_sick_days(employee_data_2),
            font=("Helvetica", 14),
        )
        approve_button.pack(
            pady=20
        )
        approve_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        approve_button.bind(
            "<Button-1>",
            lambda event: self.approve_sick_days(employee_data_2),
        )
        # create a new button for denying the vacation days on canvas
        deny_button = tk.Button(
            self.employee_details_logo_canvas,
            text="Deny",
            command=lambda:self.deny_sick_days(employee_data_2),
            font=("Helvetica", 14),
        )
        deny_button.pack(
            pady=20
        )
        deny_button.place(relx=0.5, rely=0.9, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        deny_button.bind(
            "<Button-1>",
            lambda event: self.deny_sick_days(employee_data_2),
        )
        # Bind the Escape key to the exit function
        employee_details_window.bind(
            "<Escape>", lambda event: employee_details_window.destroy()
        )
        # focus on window
        employee_details_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(employee_details_window)
        # Run the main loop for the create_remove_hr_window
        employee_details_window.mainloop()

    def load_image_employee_details(self):

        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_employee_details_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_employee_details()

    def resize_canvas_and_image_employee_details(self):
        # Get the employee_details window size
        window_width = self.employee_details_logo_canvas.winfo_width()
        window_height = self.employee_details_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.employee_details_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_employee_details_logo_image.resize(
            (window_width, window_height)
        )
        self.employee_details_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.employee_details_logo_canvas.delete("all")
        self.employee_details_logo_canvas.create_image(
            0, 0, image=self.employee_details_logo_image, anchor="nw"
        )

    def on_window_resize_employee_details(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_employee_details()

    def approve_vacation_days(self, employee_data):
        # get the username, provisional vacation days and reason for vacation days from the employee details window
        username = self.username_entry.get()
        provisional_vacation_days = self.provisional_vacation_days_entry.get()
        reason_for_vacation_days = self.reason_for_vacation_days_entry.get()
        # update the provisional vacation days in the database for the employee
        emp_ref = db.reference("/employee")
        emp_ref.child(employee_data).update({"vacation_days": 0})
        # update the reason for vacation days in the database for the employee
        emp_ref.child(employee_data).update({"reason_for_vacation_days": reason_for_vacation_days})
        # update the vacation days in the database for the employee
        emp_ref.child(employee_data).update({"vacation_approved": provisional_vacation_days})
        emp_ref.child(employee_data).update({"vacation_approved_denied": "Approved"})
        # close the employee details window
        self.employee_details_logo_canvas.destroy()
        # show a message that the vacation days have been approved
        messagebox.showinfo("Approve Vacation Days", "Vacation Days Approved")

    def deny_vacation_days(self, employee_data):
        # get the username, provisional vacation days and reason for vacation days from the employee details window
        username = self.username_entry.get()
        provisional_vacation_days = self.provisional_vacation_days_entry.get()
        reason_for_vacation_days = self.reason_for_vacation_days_entry.get()
        # update the provisional vacation days in the database for the employee
        emp_ref = db.reference("/employee")
        emp_ref.child(employee_data).update({"vacation_days": 0})
        # update the reason for vacation days in the database for the employee
        emp_ref.child(employee_data).update({"reason_for_vacation_days": reason_for_vacation_days})
        emp_ref.child(employee_data).update({"vacation_approved_denied": "Denied"})
        # close the employee details window
        self.employee_details_logo_canvas.destroy()
        # show a message that the vacation days have been denied
        messagebox.showinfo("Deny Vacation Days", "Vacation Days Denied")

    def approve_sick_days(self, employee_data):
        # get the username, provisional vacation days and reason for vacation days from the employee details window
        username = self.username_entry.get()
        provisional_vacation_days = self.provisional_vacation_days_entry.get()
        reason_for_vacation_days = self.reason_for_sick_days_entry.get()
        # update the provisional vacation days in the database for the employee
        emp_ref = db.reference("/employee")
        emp_ref.child(employee_data).update({"sick_days": 0})
        # update the reason for vacation days in the database for the employee
        emp_ref.child(employee_data).update({"reason_for_sick_days": reason_for_vacation_days})
        # update the vacation days in the database for the employee
        emp_ref.child(employee_data).update({"sick_approved": provisional_vacation_days})
        emp_ref.child(employee_data).update({"sick_approved_denied": "Approved"})
        # close the employee details window
        self.employee_details_logo_canvas.destroy()
        # show a message that the vacation days have been approved
        messagebox.showinfo("Approve Sick Days", "Sick Days Approved")

    def deny_sick_days(self, employee_data):
       # get the username, provisional vacation days and reason for vacation days from the employee details window
        username = self.username_entry.get()
        provisional_vacation_days = self.provisional_vacation_days_entry.get()
        reason_for_vacation_days = self.reason_for_sick_days_entry.get()
        # update the provisional vacation days in the database for the employee
        emp_ref = db.reference("/employee")
        emp_ref.child(employee_data).update({"sick_days": 0})
        # update the reason for vacation days in the database for the employee
        emp_ref.child(employee_data).update({"reason_for_sick_days": reason_for_vacation_days})
        emp_ref.child(employee_data).update({"sick_approved_denied": "Denied"})
        # close the employee details window
        self.employee_details_logo_canvas.destroy()
        # show a message that the vacation days have been denied
        messagebox.showinfo("Deny Sick Days", "Sick Days Denied")
    
    def progress_on_task(self):
        messagebox.showinfo("Boss Window", "Progress on Task Button Pressed")

    def approve_promotion(self):
        messagebox.showinfo("Boss Window", "Approve Promotion Button Pressed")

    def approve_resignatin(self):
        messagebox.showinfo("Boss Window", "Approve Resignation Button Pressed")

    def request_bonus(self):
        messagebox.showinfo("Boss Window", "Request for Bonus Button Pressed")

    def open_employee_window(self, role, username):
        self.root.destroy()  # Close the main login window
        employee_window = tk.Tk()  # Use Tk() to create a new window
        employee_window.geometry("900x600")  # Set the window size
        employee_window.title("Employee Window")

        #create a canvas that resizes with the window
        self.employee_logo_canvas = tk.Canvas(employee_window, bg="white", highlightthickness=0)
        self.employee_logo_canvas.pack(fill=tk.BOTH, expand=True)

         # bind window resize event to function
        employee_window.bind("<Configure>", lambda event: self.on_window_resize_employee(event,username))

        # import the image as the background on the canvas
        self.load_image_employee(username)
        
                # focus on window
        employee_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(employee_window)
        
        #Check if Sick/Vacation Days are approved
        emp_ref = db.reference("/employee")
        vacation_approved = emp_ref.child(username).child("vacation_approved_denied").get()
        sick_approved = emp_ref.child(username).child("sick_approved_denied").get()
        if sick_approved != None and sick_approved == "Approved":
            messagebox.showinfo("Sick Days Approved", "Your Sick Days have been approved")
            emp_ref.child(username).update({"sick_approved_denied": "None"})
        if vacation_approved != None and vacation_approved == "Approved":
            messagebox.showinfo("Vacation Days Approved", "Your Vacation Days have been approved")
            emp_ref.child(username).update({"vacation_approved_denied": "None"})
        if sick_approved != None and sick_approved == "Denied":
            messagebox.showinfo("Sick Days Denied", "Your Sick Days have been denied")
            emp_ref.child(username).update({"sick_approved_denied": "None"})
        if vacation_approved != None and vacation_approved == "Denied":
            messagebox.showinfo("Vacation Days Denied", "Your Vacation Days have been denied")
            emp_ref.child(username).update({"vacation_approved_denied": "None"})
        
        #add buttons and use a function to place them in the canvas
        self.add_buttons_to_canvas_employee(username)

        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.employee_logo_canvas,
        text="Exit",
        command=employee_window.destroy,
        font=("Helvetica", 14),
        width=15,
        height=2,
        bd=0,
        fg="white",
        bg="#FF4500",
        activebackground="#FF6347",
    )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")

        profile_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "profile.png" #change jpg to png for main background
        )
        profile_img = PhotoImage(file=profile_path)
        
        resized_profile_img = profile_img.subsample(4, 4)
        
        profile_btn = tk.Button(
            self.employee_logo_canvas, image=resized_profile_img, command=lambda:self.profile(username,role),borderwidth=0, font=("Helvetica", 14)
        )
        profile_btn.pack(
            pady=20
        )
        profile_btn.place(
            relx=0.95, rely=0.05, anchor="center", width=50, height=50
        )
        
        # Bind the Escape key to the exit function
        employee_window.bind("<Escape>", lambda event: employee_window.destroy())

        # Run the main loop for the employee window
        employee_window.mainloop()

    def add_buttons_to_canvas_employee(self,username):
        #buttons of Employee window to the right side of the screen
        self.apply_for_vacation_days_button = tk.Button(
            self.employee_logo_canvas, text="Apply for Sick/Vacation Days", command=lambda:self.apply_for_vacation_days(username), font=("Helvetica", 14)
        )
        self.apply_for_vacation_days_button.pack(
            pady=20
        )
        self.apply_for_vacation_days_button.place(
            relx=0.75, rely=0.3, anchor="center", width=300, height=30
        )

        self.apply_for_resignation_button = tk.Button(
            self.employee_logo_canvas, text="Apply for Resignation", command=lambda:self.apply_for_resignation(username), font=("Helvetica", 14)
        )
        self.apply_for_resignation_button.pack(
            pady=20
        )
        self.apply_for_resignation_button.place(
            relx=0.75, rely=0.4, anchor="center", width=300, height=30
        )

        self.check_progress_on_tasks_button = tk.Button(
            self.employee_logo_canvas, text="Check and update Progress on Tasks", command=lambda:self.check_progress_on_tasks(username), font=("Helvetica", 14)
        )
        self.check_progress_on_tasks_button.pack(
            pady=20
        )
        self.check_progress_on_tasks_button.place(
            relx=0.75, rely=0.5, anchor="center", width=350, height=30
        )

        self.submit_survey_button = tk.Button(
            self.employee_logo_canvas, text="View and Submit Survey", command=lambda:self.submit_survey(username), font=("Helvetica", 14)
        )
        self.submit_survey_button.pack(
            pady=20
        )
        self.submit_survey_button.place(
            relx=0.75, rely=0.6, anchor="center", width=300, height=30
        )

        self.submit_complaint_button = tk.Button(

            self.employee_logo_canvas, text="Submit Complaint", command=lambda:self.submit_complaint(), font=("Helvetica", 14)
        )
        self.submit_complaint_button.pack(
            pady=20
        )
        self.submit_complaint_button.place(
            relx=0.75, rely=0.7, anchor="center", width=300, height=30
        )
    
    def load_image_employee(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_employee_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_employee(username)

    def resize_canvas_and_image_employee(self, username):
        # Get the employee window size
        window_width = self.employee_logo_canvas.winfo_width()
        window_height = self.employee_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.employee_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_employee_logo_image.resize(
            (window_width, window_height)
        )
        self.employee_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.employee_logo_canvas.delete("all")
        self.employee_logo_canvas.create_image(
            0, 0, image=self.employee_logo_image, anchor="nw"
        )

        # Redraw the employee name text
        self.redraw_employee_name(username)

        # Redraw the employee details text
        # self.redraw_employee_details(username)

    def redraw_employee_name(self, username):
        username_employee = username
        window_width = self.employee_logo_canvas.winfo_width()
        
        # Check if the employee name text already exists and delete it
        if hasattr(self, "employee_name_text"):
            self.employee_logo_canvas.delete(self.employee_name_text)

        # Create and place the employee name text
        self.employee_name_text = self.employee_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_employee}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    # def redraw_employee_details(self, username):
    #     window_height = self.employee_logo_canvas.winfo_height()
    #     employee_ref = db.reference("/employee")
    #     emp_id = employee_ref.child(username).child("emp_id").get()
    #     designation = employee_ref.child(username).child("designation").get()
    #     salary = employee_ref.child(username).child("salary").get()
    #     sick_approved = employee_ref.child(username).child("sick_approved").get()
    #     vacation_approved = employee_ref.child(username).child("vacation_approved").get()
    #     bonus = employee_ref.child(username).child("bonus").get()
    #     hours_attended = employee_ref.child(username).child("hours_attended").get()
    #     survey = employee_ref.child(username).child("survey").child("available").get()
    #     vacation_a_d = employee_ref.child(username).child("vacation_approved_denied").get()
    #     sick_a_d = employee_ref.child(username).child("sick_approved_denied").get()

    #     # Check if the employee details text already exists and delete it
    #     if hasattr(self, "employee_details_text"):
    #         self.employee_logo_canvas.delete(self.employee_details_text)

    #     # Create and place the employee details text
    #     self.employee_details_text = self.employee_logo_canvas.create_text(
    #         # Place it on the leftmost of the window
    #         10,
    #         window_height - 10,
    #         text=f"Employee ID: {emp_id}\nDesignation: {designation}\nSalary: {salary}\nSick Days: {sick_approved}\nVacation Days: {vacation_approved}\nBonus: {bonus}\nHours Attended: {hours_attended}\nSurvey Available: {survey}\nVacation Approved/Denied: {vacation_a_d}\nSick Approved/Denied: {sick_a_d}\n\n\n\n\n",
    #         font=("Helvetica", 18, "bold"),
    #         fill="white",
    #         anchor="sw",
    #     )

    def on_window_resize_employee(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_employee(username)

    def apply_for_vacation_days_load_image(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_apply_for_vacation_days_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_apply_for_vacation_days()
    
    def resize_canvas_and_image_apply_for_vacation_days(self):
        # Get the apply_for_vacation_days window size
        window_width = self.apply_for_vacation_days_canvas.winfo_width()
        window_height = self.apply_for_vacation_days_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.apply_for_vacation_days_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_apply_for_vacation_days_logo_image.resize(
            (window_width, window_height)
        )
        self.apply_for_vacation_days_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.apply_for_vacation_days_canvas.delete("all")
        self.apply_for_vacation_days_canvas.create_image(
            0, 0, image=self.apply_for_vacation_days_logo_image, anchor="nw"
        )
    
    def on_window_resize_apply_for_vacation_days(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_apply_for_vacation_days()  

    def apply_for_vacation_days(self, username):
        # Create a new window for the apply_for_vacation_days top level
        apply_for_vacation_days_window = tk.Toplevel()
        apply_for_vacation_days_window.geometry("800x600")  # Set the window size
        apply_for_vacation_days_window.title("Apply for Sick/Vacation Days")

        # create the canvas
        self.apply_for_vacation_days_canvas = tk.Canvas(apply_for_vacation_days_window, bg="white", highlightthickness=0)
        self.apply_for_vacation_days_canvas.pack(fill=tk.BOTH, expand=True)

        # load the image
        self.apply_for_vacation_days_load_image()

        # Create a dropdown menu for sick/vacation days
        options = ["Select Type", "Sick Days", "Vacation Days"]
        selected_option = tk.StringVar()
        selected_option.set(options[0])  # Set the default option

        dropdown_menu = tk.OptionMenu(self.apply_for_vacation_days_canvas, selected_option, *options)
        dropdown_menu.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)

        # Create entry widgets for number of days and reason
        self.number_of_days_entry = tk.Entry(self.apply_for_vacation_days_canvas)
        self.number_of_days_entry.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)
        self.number_of_days_entry.insert(0, "0")  # Default value
        self.number_of_days_entry.bind("<FocusIn>", lambda event: self.days_entry_del())  # Delete the default value when the user clicks on the entry widget

        self.reason_entry = tk.Entry(self.apply_for_vacation_days_canvas)
        self.reason_entry.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)
        self.reason_entry.insert(0, "Vacation reason")  # Default value
        self.reason_entry.bind("<FocusIn>", lambda event: self.reason_entry_del())  # Delete the default value when the user clicks on the entry widget

        # Create a button to submit the vacation request
        submit_button = tk.Button(self.apply_for_vacation_days_canvas, text="Submit", command=lambda: self.submit_vacation_request(username, selected_option.get(), apply_for_vacation_days_window))
        submit_button.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)

        # Bind the Escape key to the exit function
        apply_for_vacation_days_window.bind("<Escape>", lambda event: apply_for_vacation_days_window.destroy())

        # bind window resize event to function
        apply_for_vacation_days_window.bind("<Configure>", lambda event: self.on_window_resize_apply_for_vacation_days(event))

        # focus on window
        apply_for_vacation_days_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(apply_for_vacation_days_window)

        # Run the main loop for the apply_for_vacation_days_window
        apply_for_vacation_days_window.mainloop()

    def submit_vacation_request(self, username, selected_option, apply_for_vacation_days_window):
        # Retrieve the entered values
        number_of_days = self.number_of_days_entry.get()
        reason = self.reason_entry.get()

        # Check if the values are entered and valid
        if not number_of_days:
            messagebox.showinfo("Employee Window", "Please enter a number of days.")
        elif not number_of_days.isdigit():
            messagebox.showinfo("Employee Window", "Please enter a valid number of days.")
        elif not reason:
            messagebox.showinfo("Employee Window", "Please enter a reason.")
        elif number_of_days == "0":
            messagebox.showinfo("Employee Window", "Please enter a number of days.")
        elif reason == "Vacation reason":
            messagebox.showinfo("Employee Window", "Please enter a reason.")
        elif selected_option == "Select Type":
            messagebox.showinfo("Employee Window", "Please select sick or vacation days.")
        elif selected_option == "Sick Days" and int(number_of_days) > (db.reference("sick_days_uni").get() - (self.get_employee_data(username, "sick_days"))):
            messagebox.showinfo("Employee Window", "You do not have enough sick days.")
        elif selected_option == "Vacation Days" and int(number_of_days) > (db.reference("vacation_uni").get() - (self.get_employee_data(username, "vacation_days"))):
            messagebox.showinfo("Employee Window", "You do not have enough vacation days.")
        else:
            # Convert number_of_days string to int
            number_of_days_int = int(number_of_days)

            # Check if the number of days is at least 1
            if number_of_days_int < 1:
                messagebox.showinfo("Employee Window", "Please enter at least 1 day.")
            else:
                # Update the database
                emp_ref = db.reference("/employee")
                if selected_option == "Sick Days":
                    emp_ref.child(username).update({"sick_days": self.get_employee_data(username, "sick_days") + number_of_days_int})
                    emp_ref.child(username).update({"sick_reason": reason})
                    #add pending approval for sick days in the database in approved/denied sick days
                    emp_ref.child(username).update({"sick_approved_denied": "pending"})
                else:
                    emp_ref.child(username).update({"vacation_days": self.get_employee_data(username, "vacation_days") + number_of_days_int})
                    emp_ref.child(username).update({"vacation_reason": reason})
                    emp_ref.child(username).update({"vacation_approved_denied": "pending"})

                # Show a message that the request has been submitted
                messagebox.showinfo("Employee Window", "Request submitted.")

                # Close the apply_for_vacation_days_window
                apply_for_vacation_days_window.destroy()
    
    def apply_for_resignation(self,username):
        # Create a new window for the apply_for_resignation top level
        apply_for_resignation_window = tk.Toplevel()
        apply_for_resignation_window.geometry("800x600")  # Set the window size
        apply_for_resignation_window.title("Apply for Resignation")
        
        #create the canvas
        self.apply_for_resignation_canvas = tk.Canvas(apply_for_resignation_window, bg="white", highlightthickness=0)
        self.apply_for_resignation_canvas.pack(fill=tk.BOTH, expand=True)
        
        #load the image
        self.apply_for_resignation_load_image()
                
        # Create entry widget for reason of resignation (bigger size)
        self.reason_entry = tk.Entry(self.apply_for_resignation_canvas, width=50, font=("Helvetica", 14))
        self.reason_entry.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)
        self.reason_entry.insert(0, "Reason for resignation")  # Default value
        self.reason_entry.bind("<FocusIn>", lambda event: self.reason_entry_del())  # Delete the default value when the user clicks on the entry widget

        # Create a DateEntry widget for the resignation date (bigger size)
        self.date_entry = DateEntry(
        self.apply_for_resignation_canvas,
        width=15,
        background="darkblue",
        foreground="white",
        borderwidth=2,
        year=2024,
        font=("Helvetica", 14),
        date_pattern='dd/mm/yyyy'  # Set the date format here
        )
        self.date_entry.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)
        self.date_entry.bind("<FocusIn>", lambda event: self.date_entry_del())  # Delete the default value when the user clicks on the entry widget

        # Create a button to submit the resignation request
        submit_button = tk.Button(self.apply_for_resignation_canvas, text="Submit", command=lambda: self.submit_resignation_request(apply_for_resignation_window, username))
        submit_button.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)

        # bind window resize event to function
        apply_for_resignation_window.bind("<Configure>", lambda event: self.on_window_resize_apply_for_resignation(event))
        
        # Bind the Escape key to the exit function
        apply_for_resignation_window.bind("<Escape>", lambda event: apply_for_resignation_window.destroy())
        
        # focus on window
        apply_for_resignation_window.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(apply_for_resignation_window)
        
        # Run the main loop for the apply_for_resignation_window
        apply_for_resignation_window.mainloop()
    
    def apply_for_resignation_load_image(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_apply_for_resignation_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_apply_for_resignation()
    
    def resize_canvas_and_image_apply_for_resignation(self):
        # Get the apply_for_resignation window size
        window_width = self.apply_for_resignation_canvas.winfo_width()
        window_height = self.apply_for_resignation_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.apply_for_resignation_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_apply_for_resignation_logo_image.resize(
            (window_width, window_height)
        )
        self.apply_for_resignation_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.apply_for_resignation_canvas.delete("all")
        self.apply_for_resignation_canvas.create_image(
            0, 0, image=self.apply_for_resignation_logo_image, anchor="nw"
        )
    
    def on_window_resize_apply_for_resignation(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_apply_for_resignation()
         
    def submit_resignation_request(self, apply_for_resignation_window, username):
        # Retrieve the entered values
        reason = self.reason_entry.get()
        date = self.date_entry.get()

        # Check if the date is at least 2 weeks from now
        if not reason:
            messagebox.showinfo("Employee Window", "Please enter a reason.")
        elif date == "Date of resignation":
            messagebox.showinfo("Employee Window", "Please enter a date.")
        elif db.reference("/employee").child(username).child("apply_for_resignation").get() != None:
            messagebox.showinfo("Employee Window", "You have already applied for resignation.")
        else:
            # Convert date string to datetime object
            date_format = "%d/%m/%Y"
            date_obj = datetime.datetime.strptime(date, date_format)

            # Convert datetime object back to string in the desired format
            date_str_formatted = date_obj.strftime("%d/%m/%Y")

            # Check if the date is at least 2 weeks from now
            if date_obj < datetime.datetime.now() + datetime.timedelta(weeks=2):
                messagebox.showinfo("Employee Window", "Please enter a date at least 2 weeks from now.")
            else:
                # Add the resignation request to the database
                db.reference("/employee").child(username).child("apply_for_resignation").set(date_str_formatted)
                db.reference("/employee").child(username).child("resignation_reason").set(reason)
                messagebox.showinfo("Employee Window", "Resignation request submitted successfully.")

                apply_for_resignation_window.destroy()

    def check_progress_on_tasks(self, username):
        # Create a new window for the check_progress_on_tasks top level
        check_progress_on_tasks_window = tk.Toplevel()
        check_progress_on_tasks_window.geometry("800x600")  # Set the window size
        check_progress_on_tasks_window.title("Check Progress on Tasks")
        
        #create the canvas
        self.check_progress_on_tasks_canvas = tk.Canvas(check_progress_on_tasks_window, bg="white", highlightthickness=0)
        self.check_progress_on_tasks_canvas.pack(fill=tk.BOTH, expand=True)
        
        #load the image
        self.check_progress_on_tasks_load_image(username)

        # bind window resize event to function
        check_progress_on_tasks_window.bind("<Configure>", lambda event: self.on_window_resize_check_progress_on_tasks(username,event))
        
        # Bind the escape key to the exit function
        check_progress_on_tasks_window.bind("<Escape>", lambda event: check_progress_on_tasks_window.destroy())

        # Focus on window
        check_progress_on_tasks_window.focus_force()

        # Center the window
        self.center_window_all(check_progress_on_tasks_window)

        # Run the main loop for the check_progress_on_tasks_window
        check_progress_on_tasks_window.mainloop()
        
    def check_progress_on_tasks_load_image(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_check_progress_on_tasks_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_check_progress_on_tasks(username)
    
    def resize_canvas_and_image_check_progress_on_tasks(self,username):
        # Get the check_progress_on_tasks window size
        window_width = self.check_progress_on_tasks_canvas.winfo_width()
        window_height = self.check_progress_on_tasks_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.check_progress_on_tasks_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_check_progress_on_tasks_logo_image.resize(
            (window_width, window_height)
        )
        self.check_progress_on_tasks_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.check_progress_on_tasks_canvas.delete("all")
        self.check_progress_on_tasks_canvas.create_image(
            0, 0, image=self.check_progress_on_tasks_logo_image, anchor="nw"
        )
        
        # Information labels
        labels_info = [
            ("Project ID", db.reference("/employee").child(username).child("project").child("id").get()),
            ("Project Name", db.reference("/employee").child(username).child("project").child("name").get()),
            ("Project Description", db.reference("/employee").child(username).child("project").child("description").get()),
            ("Project Progress", str(db.reference("/employee").child(username).child("project").child("progress").get()) + "%"),
            ("Project Deadline", db.reference("/employee").child(username).child("project").child("deadline").get()),
            ("Task Description", db.reference("/employee").child(username).child("project").child("task").child("description").get()),
            ("Task Status", db.reference("/employee").child(username).child("project").child("task").child("status").get()),
        ]

        for i, (label_text, value) in enumerate(labels_info):
            #create text onto the canvas
            text_label=self.check_progress_on_tasks_canvas.create_text(
                window_width / 2,
                100 + i * 50,
                text=f"{label_text}: {value}",
                font=("Helvetica", 14, "bold"),
                fill="white",
            )
            if label_text == "Task Status" and value == "In Progress":
                set_task_status_to_completed_button = tk.Button(self.check_progress_on_tasks_canvas, text="Set Task Status to Completed", command=lambda: self.set_task_status_to_completed(username))
                set_task_status_to_completed_button.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)
                set_task_status_to_completed_button.place(relx=0.5, rely=0.5, anchor="center", width=300, height=30)
                # Place the button next to the current label_text
                button_relx = self.check_progress_on_tasks_canvas.bbox(text_label)[2] + 10  # Get the right boundary of the text
                set_task_status_to_completed_button.place(relx=button_relx, rely=0.5, anchor="w", width=300, height=30)
            
        # Members label
        members_list = db.reference("/employee").child(username).child("project").child("members").get()
        members = "\n".join([f"{key}: {value}" for key, value in members_list.items()])

        self.check_progress_on_tasks_canvas.create_text(
            10,
            10,
            text=f"Members:\n{members}",
            font=("Helvetica", 14, "bold"),
            fill="white",
            anchor="nw",
        )
     
    def on_window_resize_check_progress_on_tasks(self,username, event):
        # Handle window resize event
        self.resize_canvas_and_image_check_progress_on_tasks(username)

    def set_task_status_to_completed(self,username):
        db.reference("/employee").child(username).child("project").child("task").child("status").set("Completed")
        db.reference("/employee").child(username).child("project").child("progress").set(db.reference("/employee").child(username).child("project").child("progress").get()+10)
        messagebox.showinfo("Employee Window", "Task Status set to Completed")
        
    def submit_survey(self, username):
        # Create a new window for the submit_survey top level
        submit_survey_window = tk.Toplevel()
        submit_survey_window.geometry("800x600")  # Set the window size
        submit_survey_window.title("Submit Survey")
        self.submit_survey_window = submit_survey_window

        # Create the canvas
        self.submit_survey_canvas = tk.Canvas(submit_survey_window, bg="white", highlightthickness=0)
        self.submit_survey_canvas.pack(fill=tk.BOTH, expand=True)

        # Pull child classes from Survey_Qs in the db using the .get function
        survey_questions = db.reference("/Survey_Qs").get()

        # Store the keys of the survey questions in a list
        survey_questions_keys = list(survey_questions.keys())

        # Bind the window resize event to the function
        submit_survey_window.bind("<Configure>", lambda event: self.display_survey_questions(survey_questions_keys, survey_questions,username))
       
        # Bind the Escape key to the exit function
        submit_survey_window.bind("<Escape>", lambda event: submit_survey_window.destroy())
     
        # Focus on the window
        submit_survey_window.focus_force()

        # Center the window
        self.center_window_all(submit_survey_window)

        # Main loop for the submit_survey_window
        submit_survey_window.mainloop()

    def resize_canvas_and_image_submit_survey(self,):

        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_submit_survey_logo_image = Image.open(img_path)

        # Get the submit_survey window size
        window_width = self.submit_survey_canvas.winfo_width()
        window_height = self.submit_survey_canvas.winfo_height()
         # Resize the image if needed
        resized_image = self.original_submit_survey_logo_image.resize(
            (window_width, window_height)
        )
        self.submit_survey_logo_image = ImageTk.PhotoImage(resized_image)

        # Redraw the image
        self.submit_survey_canvas.create_image(
            0, 0, image=self.submit_survey_logo_image, anchor="nw"
        )
       
    def display_survey_questions(self, survey_questions_keys, survey_questions,username):
        # Clear only the text from the canvas
        self.submit_survey_canvas.delete("all")
        
        # Resize canvas and image
        self.resize_canvas_and_image_submit_survey()

        # Check if the current question index is out of bounds
        if self.current_question_index < 0:
            self.current_question_index = 0
        elif self.current_question_index >= len(survey_questions_keys):
            self.current_question_index = len(survey_questions_keys) - 1

        # Get the current question key
        current_question_key = survey_questions_keys[self.current_question_index]

        # Display the question on the canvas
        question_text = f"Question {self.current_question_index + 1}: {survey_questions[current_question_key]}"
        self.submit_survey_canvas.create_text(
            10,
            10,
            text=question_text,
            font=("Helvetica", 14, "bold"),
            fill="white",
            anchor="nw",
        )

        # Check if buttons have been created
        if not hasattr(self, 'buttons_created') or not self.buttons_created:
            # Create a frame within the canvas to contain the buttons
            button_frame = tk.Frame(self.submit_survey_canvas, bg="white")
            button_frame.pack(pady=20, side=tk.BOTTOM)

            # Create radio buttons for each question
            self.radio_var = tk.StringVar()
            self.radio_var.set(None)  # Set default value

            options = ["Very Poor", "Poor", "Average", "Good", "Very Good"]
            for i, option in enumerate(options):
                tk.Radiobutton(
                    self.submit_survey_canvas,
                    text=option,
                    variable=self.radio_var,
                    radio_var=None,
                    value=option,
                    command=lambda value=option: self.store_selected_value(value)
                ).place(x=20, y=50 + i * 30)

               
            # Create a button to go to the next question
            next_button = tk.Button(button_frame, text="Next", command=lambda: self.next_question(survey_questions_keys, survey_questions,username))
            next_button.grid(row=0, column=1)

            # Create a button to go to the previous question also pass the survey_questions_keys, survey_questions as arguments
            previous_button = tk.Button(button_frame, text="Previous", command=lambda: self.previous_question(survey_questions_keys, survey_questions,username))
            previous_button.grid(row=0, column=0)

            # Create a button to submit the survey at the bottom center of the window
            submit_button = tk.Button(button_frame, text="Submit", command=lambda: self.submit_survey_request(username))
            submit_button.grid(row=0, column=2)

            # Set the flag to indicate that buttons have been created
            self.buttons_created = True
                
    def next_question(self,survey_questions_keys, survey_questions,username):
        # Increment the current question index
        self.current_question_index += 1     

          # Clear the selected radio button
        self.clear_selected_radio_button()

        # Display the next question
        self.display_survey_questions(survey_questions_keys, survey_questions,username)

    def previous_question(self,survey_questions_keys, survey_questions,username):
        # Decrement the current question index
        self.current_question_index -= 1

          # Clear the selected radio button
        self.clear_selected_radio_button()

        # Display the previous question
        self.display_survey_questions(survey_questions_keys, survey_questions,username)

    def clear_selected_radio_button(self):
        # Check if a value is selected for the current question
        stored_value = self.selected_values.get(self.current_question_index)

        # If a value is present, set the radio variable to that value
        if stored_value is not None and stored_value in ["Very Poor", "Poor", "Average", "Good", "Very Good"]:
            self.radio_var.set(stored_value)
        else:
            # Otherwise, clear the selected radio button by setting the variable to None
            self.radio_var.set(None)

    def on_window_resize_submit_survey(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_submit_survey()

    def submit_survey_request(self, username):

        stored_value = self.selected_values.get(self.current_question_index)
        # Check if there are any unanswered questions
        if stored_value is None or not stored_value in ["Very Poor", "Poor", "Average", "Good", "Very Good"]:

            self.buttons_created = False

            # If any question is not answered, show a messagebox and return without submitting
            messagebox.showwarning("Incomplete Survey", "Please answer all survey questions before submitting.")
            return

        else:# Show a message that the survey has been submitted
            messagebox.showinfo("Employee Window", "Survey submitted successfully.")
            
            # Store the selected values in the database
            db.reference("/employee").child(username).child("survey").set(self.selected_values)

            # Set the value of the "available" key in the survey to False
            db.reference("/employee").child(username).child("survey").child("available").set("No")

            # Clear the selected values and reset the current question index
            self.buttons_created = False
            self.current_question_index = 0

            # Destroy the survey window
            self.submit_survey_window.destroy()
            
    def store_selected_value(self, value):
       #store the selected value in relation to the question index
        self.selected_values[self.current_question_index] = value

    def submit_complaint(self):
       # Create a new window for the submit_complaint top level
        submit_complaint_window = tk.Toplevel()
        submit_complaint_window.geometry("800x600")
        submit_complaint_window.title("Submit Complaint")
        
        #create the canvas
        self.submit_complaint_canvas = tk.Canvas(submit_complaint_window, bg="white", highlightthickness=0)
        self.submit_complaint_canvas.pack(fill=tk.BOTH, expand=True)
        
        #load the image
        self.submit_complaint_load_image()
        
        #create an entry to take the employees name whose complaint is being submitted
        self.employee_name_entry = tk.Entry(self.submit_complaint_canvas)
        self.employee_name_entry.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)
        self.employee_name_entry.insert(0, "Employee Name")  # Default value
        self.employee_name_entry.bind("<FocusIn>", lambda event:self.employee_name_entry_del())
        
        # Create entry widget for complaint
        self.complaint_entry = tk.Entry(self.submit_complaint_canvas, width=50, font=("Helvetica", 14))
        self.complaint_entry.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)
        self.complaint_entry.insert(0, "Complaint")
        self.complaint_entry.bind("<FocusIn>", lambda event: self.complaint_entry_del())  # Delete the default value when the user clicks on the entry widget
        
        # Create a button to submit the complaint
        submit_button = tk.Button(self.submit_complaint_canvas, text="Submit", command=lambda: self.submit_complaint_request(submit_complaint_window))
        submit_button.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)
        
        # Bind the Escape key to the exit function
        submit_complaint_window.bind("<Escape>", lambda event: submit_complaint_window.destroy())
        
        # bind window resize event to function
        submit_complaint_window.bind("<Configure>", lambda event: self.on_window_resize_submit_complaint(event))
        
        # focus on window
        submit_complaint_window.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(submit_complaint_window)
        
        # Run the main loop for the submit_complaint_window
        submit_complaint_window.mainloop()
        
    def submit_complaint_load_image(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_submit_complaint_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_submit_complaint()
        
    def resize_canvas_and_image_submit_complaint(self):
        # Get the submit_complaint window size
        window_width = self.submit_complaint_canvas.winfo_width()
        window_height = self.submit_complaint_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.submit_complaint_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_submit_complaint_logo_image.resize(
            (window_width, window_height)
        )
        self.submit_complaint_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.submit_complaint_canvas.delete("all")
        self.submit_complaint_canvas.create_image(
            0, 0, image=self.submit_complaint_logo_image, anchor="nw"
        )
        
    def on_window_resize_submit_complaint(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_submit_complaint()
        
    def submit_complaint_request(self, submit_complaint_window):
        # Retrieve the entered values
        employee_name = self.employee_name_entry.get()
        complaint = self.complaint_entry.get()

        # Check if the complaint is valid
        if not employee_name:
            messagebox.showinfo("Employee Window", "Please enter an employee name.")
        elif not complaint:
            messagebox.showinfo("Employee Window", "Please enter a complaint.")
        else:
            # Add the complaint to the database
            db.reference("/employee").child(employee_name).child("complaint").set(complaint)
            messagebox.showinfo("Employee Window", "Complaint submitted successfully.")
            submit_complaint_window.destroy()
        
    def employee_name_entry_del(self):
        if self.employee_name_entry.get() == "Employee Name":
            self.employee_name_entry.delete(0, tk.END)
            
    def complaint_entry_del(self):
        if self.complaint_entry.get() == "Complaint":
            self.complaint_entry.delete(0, tk.END)
        
    def center_window_all(self, window):
        # Get the width and height of the screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate the x and y coordinates to center the main window
        x = (screen_width / 2) - (900 / 2)
        y = (screen_height / 2) - (600 / 2)

        # Set the dimensions of the screen and where it is placed
        window.geometry("%dx%d+%d+%d" % (900, 600, x, y))

    def add_login_to_database(self, create_remove_hr_window):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()

        admins_ref = db.reference("/admins")
        hr_ref = db.reference("/HR")
        boss_ref = db.reference("/boss")
        employee_ref = db.reference("/employee")
        emp_id_ref = db.reference("/")
        emp_uni = emp_id_ref.child("emp_id").get()

        if (
            admins_ref.child(username).get()
            or hr_ref.child(username).get()
            or boss_ref.child(username).get()
            or employee_ref.child(username).get()
        ):
            messagebox.showinfo(
                "Add HR Login", "Username already exists. Choose a different username."
            )
        else:
            # Add the new login to the database
            if role == "HR":
                hr_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "post:": "",
                        "salary": "",
                        "emp_id": emp_uni + 1,
                    }
                )
                emp_id_ref.child("emp_id").set(emp_uni + 1)
            elif role == "boss":
                boss_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "designnation: ": "",
                        "salary": "",
                        "emp_ids": emp_uni + 1,
                    }
                )
                emp_id_ref.child("emp_id").set(emp_uni + 1)
            elif role == "employee":
                employee_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "designation": "",
                        "emp_id": emp_uni + 1,
                        "salary": "",
                        "sick_days": "",
                        "vacation_days": "",
                        "bonus": "",
                        "hours_attended": "",
                        "apply_for_resignation": "",
                        "apply_for_vacation": "",
                        "progress_on_task": "",
                        "survey": "",
                        "feedback": "",
                        "vacation_reason": "",
                        "vacation_approved": "",
                        "sick_approved": "",
                        "sick_reason": "",
                        "vacation_approved_denied": "",
                        "sick_approved_denied": "",
                        
                    }
                )
                emp_id_ref.child("emp_id").set(emp_uni + 1)
            messagebox.showinfo("Add HR Login", "Login added successfully.")
        # close the window
        create_remove_hr_window.destroy()

    def remove_login_from_database(self, create_remove_hr_window):
        username = self.username_entry.get()
        role = self.role_entry.get()
        admins_ref = db.reference("/admins")
        hr_ref = db.reference("/HR")
        boss_ref = db.reference("/boss")
        employee_ref = db.reference("/employee")
        if role == "HR":
            if hr_ref.child(username).get():
                # Remove the login from the database
                hr_ref.child(username).delete()
                messagebox.showinfo("Remove HR Login", "Login removed successfully.")
            else:
                messagebox.showinfo("Remove HR Login", "Username does not exist.")
        elif role == "boss":
            if boss_ref.child(username).get():
                # Remove the login from the database
                boss_ref.child(username).delete()
                messagebox.showinfo("Remove HR Login", "Login removed successfully.")
            else:
                messagebox.showinfo("Remove HR Login", "Username does not exist.")
        elif role == "employee":
            if employee_ref.child(username).get():
                # Remove the login from the database
                employee_ref.child(username).delete()
                messagebox.showinfo("Remove HR Login", "Login removed successfully.")
            else:
                messagebox.showinfo("Remove HR Login", "Username does not exist.")
        # close the window
        create_remove_hr_window.destroy()

    def days_entry_del(self):
        if self.number_of_days_entry.get() == "0":
            self.number_of_days_entry.delete(0, tk.END)

    def reason_entry_del(self):
        if self.reason_entry.get() == "Vacation reason":
            self.reason_entry.delete(0, tk.END)
        if self.reason_entry.get() == "Reason for resignation":
            self.reason_entry.delete(0, tk.END)
    
    def date_entry_del(self):
        if self.date_entry.get() == "mm/dd/yyyy":
            self.date_entry.delete(0, tk.END)
        
def main():
    
    root = tk.Tk()
    root.geometry("900x600")  # Set the window size
    app = CreativeLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()