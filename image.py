import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import firebase_admin
from firebase_admin import db, credentials

# Initialize Firebase Admin SDK
cred = credentials.Certificate("credentials.json")  # Path: credentials.json
firebase_admin.initialize_app(cred, {'databaseURL': 'https://hr-management-system-f7c9f-default-rtdb.asia-southeast1.firebasedatabase.app/'})

class CreativeLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Management System")
        self.employee_original_image = None
        self.employee_img = None
        self.boss_original_image = None
        self.boss_img = None

        # Construct the full path to the image file
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load and set the background image
        self.original_image = Image.open(img_path)
        self.img = ImageTk.PhotoImage(self.original_image)

        # Create and place a label with the background image
        self.background_label = tk.Label(root, image=self.img, bg='white')
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind the window resize event
        root.bind("<Configure>", lambda event, img=self.img, label=self.background_label: self.resize_image(event, img, label))

        # Label for Username
        username_label = tk.Label(root, text="Username", font=("Helvetica", 12, "bold"), bg='white')
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        # Username entry
        self.username_entry = tk.Entry(root, font=("Helvetica", 12, "bold"))
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")  # Default text

        # Label for Password
        password_label = tk.Label(root, text="Password", font=("Helvetica", 12, "bold"), bg='white')
        password_label.place(relx=0.5, rely=0.5, anchor="center")

        # Password entry
        self.password_entry = tk.Entry(root, show="*", font=("Helvetica", 12, "bold"))
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry.insert(0, "")  # Default text

        # Login button
        self.login_button = tk.Button(root, text="Login", command=self.login, font=("Helvetica", 14))
        self.login_button.place(relx=0.5, rely=0.65, anchor="center")

        # Exit button
        self.exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Helvetica", 14))
        self.exit_button.place(relx=0.5, rely=0.75, anchor="center")

        # Credits button
        self.credits_button = tk.Button(root, text="Credits", command=self.show_credits, font=("Helvetica", 14))
        self.credits_button.place(relx=0.5, rely=0.85, anchor="center")

        # # Load credentials from the database
        # self.credentials = self.load_credentials_from_database()

    def resize_image(self, event, img, label):
        new_width = event.width
        new_height = event.height

        # Resize the original image
        resized_image = self.original_image.resize((new_width, new_height))

        # Create a new PhotoImage object
        self.img = ImageTk.PhotoImage(resized_image)

        #for future purposes, if we break something remove comment and activate this(DO NOT DELETE, DELETE IF YOU GAY)
        # try:
        #     if self.root.winfo_exists():  # Check if the main window still exists
        #         # Update the label only if the main window exists
        #         label.config(image=self.img)
        #         label.image = self.img  # Keep a reference to avoid garbage collection
        # except tk.TclError:
        #     pass  # Ignore TclError if the main window has been destroyed


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username or password is empty
        if not username or not password:
            messagebox.showerror("Login Failed", "Username and password are required. Please enter both.")
            return

        admins = db.reference('admins')

        if admins.child(username).child('password').get() == password:
            role = admins.child(username).child('role').get()  # Fetch role, default to 'User' if not found
            messagebox.showinfo("Login Successful", f"Welcome, {username}!\nYou are logged in as a {role}.")

            match role:
                case 'admin':
                    self.open_admin_window()
                case 'HR':
                    self.open_hr_window()
                case 'boss':
                    self.open_boss_window()
                case 'employee':
                    self.open_employee_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    def open_admin_window(self):
        self.root.destroy()  # Close the main login window
        admin_window = tk.Tk()  # Use Tk() to create a new window
        admin_window.geometry("800x600")  # Set the window size
        admin_window.title("Admin Window")

        # Background image for the admin window
        admin_img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")
        admin_original_image = Image.open(admin_img_path)
        admin_img = ImageTk.PhotoImage(admin_original_image)

        admin_background_label = tk.Label(admin_window, image=admin_img, bg='white')
        admin_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome message for the admin
        welcome_label = tk.Label(admin_window, text="Welcome Admin!", font=("Helvetica", 18, "bold"), fg="white", bg='black')
        welcome_label.pack(pady=20)

        # Buttons for Admin window
        buttons_info = [
            ("Create/Remove HR Login", self.create_remove_hr)
        ]

        admin_buttons_frame = tk.Frame(admin_window, bg='black')  # Define admin_buttons_frame
        admin_buttons_frame.pack(pady=20)

        for i, (button_text, button_command) in enumerate(buttons_info):
            button = tk.Button(admin_buttons_frame, text=button_text, command=button_command, font=("Helvetica", 14),
                            width=20, height=2, bd=0, fg='white', bg='#2E4053', activebackground='#566573')
            button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

        # Bind the window resize event for the admin window
        admin_window.bind("<Configure>", lambda event, img=admin_img, label=admin_background_label: self.resize_image(event, img, label))

        # Run the main loop for the admin window
        admin_window.mainloop()


    def open_hr_window(self):
     self.root.destroy()  # Close the main login window
     hr_window = tk.Tk()  # Use Tk() to create a new window
     hr_window.geometry("800x600")  # Set the window size
     hr_window.title("HR Window")

     # Background image for the HR window
     hr_img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")
     hr_original_image = Image.open(hr_img_path)
     self.hr_img = ImageTk.PhotoImage(hr_original_image)

     hr_background_label = tk.Label(hr_window, image=self.hr_img, bg='white')
     hr_background_label.place(x=0, y=0, relwidth=1, relheight=1)

     # Welcome message for the HR
     welcome_label = tk.Label(hr_window, text="Welcome HR!", font=("Helvetica", 18, "bold"), fg="white", bg='black')
     welcome_label.pack(pady=20)

     buttons_info = [
         ("Salary Management", self.salary_management),
         ("Employee Add/Remove", self.employee_add_remove),
         ("Approve Bonus", self.approve_bonus),
         ("Approve Resignation", self.approve_resignation),
         ("Check Employee Hours", self.check_hours_attended),
         ("Survey/Feedback", self.survey_feedback)
     ]

     hr_buttons_frame = tk.Frame(hr_window, bg='black')  # Define hr_buttons_frame
     hr_buttons_frame.pack(pady=20)

     for i, (button_text, button_command) in enumerate(buttons_info):
        button = tk.Button(hr_buttons_frame, text=button_text, command=button_command, font=("Helvetica", 14),
                           width=30, height=2, bd=0, fg='white', bg='#2E4053', activebackground='#566573')
        button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

     # Bind the window resize event for the HR window
     hr_window.bind("<Configure>", lambda event, img=self.hr_img, label=hr_background_label: self.resize_image(event, img, label))

     #  Run the main loop for the HR window
     hr_window.mainloop()


    def open_boss_window(self):
        self.root.destroy()  # Close the main login window
        boss_window = tk.Tk()  # Use Tk() to create a new window
        boss_window.geometry("800x600")  # Set the window size
        boss_window.title("Boss Window")

        # Background image for the boss window
        boss_img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")
        self.boss_original_image = Image.open(boss_img_path)
        self.boss_img = ImageTk.PhotoImage(self.boss_original_image)

        boss_background_label = tk.Label(boss_window, image=self.boss_img, bg='white')
        boss_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome message for the boss
        welcome_label = tk.Label(boss_window, text="Welcome Boss!", font=("Helvetica", 18, "bold"), fg="white", bg='black')
        welcome_label.pack(pady=20)

        buttons_info = [
            ("Performance Review Approval", self.perform_review_approval),
            ("Approve Vacations and Sick Leaves", self.approve_vacations_sick_leaves),
            ("Progress on Task", self.progress_on_task),
            ("Approve Promotion", self.approve_promotion),
            ("Approve Resignation", self.approve_resignation),
            ("Request for Bonus", self.request_bonus)
        ]

        boss_buttons_frame = tk.Frame(boss_window, bg='black')  # Define boss_buttons_frame
        boss_buttons_frame.pack(pady=20)

        for i, (button_text, button_command) in enumerate(buttons_info):
            button = tk.Button(boss_buttons_frame, text=button_text, command=button_command, font=("Helvetica", 14),
                            width=30, height=2, bd=0, fg='white', bg='#2E4053', activebackground='#566573')
            button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

        # Bind the window resize event for the boss window
        boss_window.bind("<Configure>", lambda event, img=self.boss_img, label=boss_background_label: self.resize_image(event, img, label))

        # Run the main loop for the boss window
        boss_window.mainloop()

   
   
    def open_employee_window(self):
        self.root.destroy()  # Close the main login window
        employee_window = tk.Tk()  # Use Tk() to create a new window
        employee_window.geometry("800x600")  # Set the window size
        employee_window.title("Employee Window")

        # Background image for the employee window
        employee_img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")
        self.employee_original_image = Image.open(employee_img_path)
        self.employee_img = ImageTk.PhotoImage(self.employee_original_image)

        employee_background_label = tk.Label(employee_window, image=self.employee_img, bg='white')
        employee_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome message for the employee
        welcome_label = tk.Label(employee_window, text="Welcome Employee!", font=("Helvetica", 18, "bold"), fg="white", bg='black')
        welcome_label.pack(pady=20)

        buttons_info = [
            ("Sick/Vacation Days View", self.sick_vacation_days_view),
            ("Apply for Vacation Days", self.apply_for_vacation_days),
            ("Apply for Resignation", self.apply_for_resignation),
            ("Check Progress on Tasks", self.check_progress_on_tasks),
            ("Submit Survey/Feedback/Complaint", self.submit_survey_feedback_complaint)
        ]

        employee_buttons_frame = tk.Frame(employee_window, bg='black')  # Define employee_buttons_frame
        employee_buttons_frame.pack(pady=20)

        for i, (button_text, button_command) in enumerate(buttons_info):
            button = tk.Button(employee_buttons_frame, text=button_text, command=button_command, font=("Helvetica", 14),
                            width=30, height=2, bd=0, fg='white', bg='#2E4053', activebackground='#566573')
            button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

        # Bind the window resize event for the employee window
        employee_window.bind("<Configure>", lambda event, img=self.employee_img, label=employee_background_label: self.resize_image(event, img, label))

        # Run the main loop for the employee window
        employee_window.mainloop()


    def salary_management(self):
        messagebox.showinfo("HR Window", "Salary Management Button Pressed")

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

    def perform_review_approval(self):
        messagebox.showinfo("Boss Window", "Performance Review Approval Button Pressed")

    def approve_vacations_sick_leaves(self):
        messagebox.showinfo("Boss Window", "Approve Vacations and Sick Leaves Button Pressed")

    def progress_on_task(self):
        messagebox.showinfo("Boss Window", "Progress on Task Button Pressed")

    def approve_promotion(self):
        messagebox.showinfo("Boss Window", "Approve Promotion Button Pressed")

    def approve_resignation(self):
        messagebox.showinfo("Boss Window", "Approve Resignation Button Pressed")

    def request_bonus(self):
        messagebox.showinfo("Boss Window", "Request for Bonus Button Pressed")

    def create_remove_hr(self):
        messagebox.showinfo("Admin Window", "Create/Remove HR Login Button Pressed")

    def sick_vacation_days_view(self):
        messagebox.showinfo("Employee Window", "Sick/Vacation Days View Button Pressed")

    def apply_for_vacation_days(self):
       messagebox.showinfo("Employee Window", "Apply for Vacation Days Button Pressed")
   
    def apply_for_resignation(self):
       messagebox.showinfo("Employee Window", "Apply for Resignation Button Pressed")
   
    def check_progress_on_tasks(self):
       messagebox.showinfo("Employee Window", "Check Progress on Tasks Button Pressed")
   
    def submit_survey_feedback_complaint(self):
       messagebox.showinfo("Employee Window", "Submit Survey/Feedback/Complaint Button Pressed")
   
    def show_credits(self):
        credits_dialog = tk.Toplevel(self.root)
        credits_dialog.title("Credits")

        # You can customize the credits information as per your needs
        credits_text = (
            "HR Management System\n\n"
            "Developed by: \n Samay Pandey, Armaan Nakhuda, Sushant Navle\n"
            "Stage Completition: Stage 4 completed\n"
            "Date: 6th Feb 2024\n"
            "\nSpecial Thanks to:\n- OpenAI\n- Firebase\n- Yash Patil\n"
        )

        credits_label = tk.Label(credits_dialog, text=credits_text, font=("Helvetica", 12))
        credits_label.pack(padx=20, pady=20)

def main():
    root = tk.Tk()
    root.geometry("800x600")  # Set the window size
    app = CreativeLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()