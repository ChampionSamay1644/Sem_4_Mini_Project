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

         # Load and set background image
        self.original_image = Image.open(img_path)
        self.img = ImageTk.PhotoImage(self.original_image)
        
        # Create and place a label with the background image
        self.background_label = tk.Label(root, image=self.img, bg='white')
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind the window resize event
        root.bind("<Configure>", self.resize_image)
    

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

        # Load credentials from the database
        self.credentials = self.load_credentials_from_database()

    def resize_image(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the original image
        resized_image = self.original_image.resize((new_width, new_height))

        # Create a new PhotoImage object
        self.img = ImageTk.PhotoImage(resized_image)

        # Update the label
        self.background_label.config(image=self.img)
        self.background_label.image = self.img  # Keep a reference to avoid garbage collection

    def load_credentials_from_database(self):
        try:
            admins_ref = db.reference('/admins')
            admins_data = admins_ref.get()
            print("Loaded credentials:", admins_data)  # Debug print
            return admins_data
        except Exception as e:
            print("Error loading credentials from the database:", e)
            return {}

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both username and password.")
            return

        if username in self.credentials and 'password' in self.credentials[username]:
            if self.credentials[username]['password'] == password:
                role = self.credentials[username].get('role', 'User')  # Fetch role, default to 'User' if not found
                messagebox.showinfo("Login Successful", f"Welcome, {username}! \n You are logged in as a {role}.")
                
                match role:
                    case 'admin':
                        self.open_admin_window()
                    case 'HR':
                        self.open_hr_window()
                    case 'boss':
                        self.open_boss_window()
                    case 'employee':
                        self.open_employee_window()
                    case _:
                        messagebox.showerror("Login Failed", "Invalid role. Please try again.")

        else:
            messagebox.show.showerror("Login Failed", "Invalid username or password. Please try again.")

    def open_admin_window(self):
        self.root.destroy()  # Close the main login window
        admin_window = tk.Tk()  # Use Tk() to create a new window
        admin_window.geometry("800x600")  # Set the window size
        admin_window.title("Admin Window")

        # Background image for the admin window
        admin_img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")
        admin_original_image = Image.open(admin_img_path)
        self.admin_img = ImageTk.PhotoImage(admin_original_image)

        admin_background_label = tk.Label(admin_window, image=self.admin_img, bg='white')
        admin_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome message for the admin
        welcome_label = tk.Label(admin_window, text="Welcome Admin!", font=("Helvetica", 18, "bold"), fg="white", bg='black')
        welcome_label.pack(pady=20)

        # Buttons for Admin window
        create_remove_hr_button = tk.Button(admin_window, text="Create/Remove HR Login", command=self.create_remove_hr, font=("Helvetica", 14))
        create_remove_hr_button.pack(pady=10)

        # Bind the window resize event for the admin window
        admin_window.bind("<Configure>", lambda event, img=self.admin_img, label=admin_background_label: self.resize_image(event, img, label))

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

        # Buttons for HR window
        salary_management_button = tk.Button(hr_window, text="Salary Management", command=self.salary_management, font=("Helvetica", 14))
        salary_management_button.pack(pady=10)

        employee_add_remove_button = tk.Button(hr_window, text="Employee Add/Remove", command=self.employee_add_remove, font=("Helvetica", 14))
        employee_add_remove_button.pack(pady=10)

        approve_bonus_button = tk.Button(hr_window, text="Approve Bonus", command=self.approve_bonus, font=("Helvetica", 14))
        approve_bonus_button.pack(pady=10)

        approve_resignation_button = tk.Button(hr_window, text="Approve Resignation", command=self.approve_resignation, font=("Helvetica", 14))
        approve_resignation_button.pack(pady=10)

        check_hours_attended_button = tk.Button(hr_window, text="Check Employee Hours Attended", command=self.check_hours_attended, font=("Helvetica", 14))
        check_hours_attended_button.pack(pady=10)

        survey_feedback_button = tk.Button(hr_window, text="Survey/Feedback", command=self.survey_feedback, font=("Helvetica", 14))
        survey_feedback_button.pack(pady=10)

        # Bind the window resize event for the HR window
        hr_window.bind("<Configure>", lambda event, img=self.hr_img, label=hr_background_label: self.resize_image(event, img, label))
        # Run the main loop for the HR window
        hr_window.mainloop()

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

        # Bind the window resize event for the employee window
        employee_window.bind("<Configure>", lambda event, img=self.employee_img, label=employee_background_label: self.resize_image(event, img, label))

        # Run the main loop for the employee window
        employee_window.mainloop()

    def open_boss_window(self):
        self.root.destroy()  # Close the main login window
        boss_window = tk.Tk()  # Use Tk() to create a new window
        boss_window.geometry("800x600")  # Set the window size
        boss_window.title("Boss Window")

        # Background image for the boss window
        boss_img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")
        boss_original_image = Image.open(boss_img_path)
        self.boss_img = ImageTk.PhotoImage(boss_original_image)

        boss_background_label = tk.Label(boss_window, image=self.boss_img, bg='white')
        boss_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome message for the boss
        welcome_label = tk.Label(boss_window, text="Welcome Boss!", font=("Helvetica", 18, "bold"), fg="white", bg='black')
        welcome_label.pack(pady=20)

        # Buttons for Boss window
        boss_buttons_frame = tk.Frame(boss_window, bg='white')
        boss_buttons_frame.pack(pady=20)

        performance_review_button = tk.Button(boss_buttons_frame, text="Performance Review Approval", command=self.perform_review_approval, font=("Helvetica", 14))
        performance_review_button.grid(row=0, column=0, padx=10)

        approve_vacations_sick_leaves_button = tk.Button(boss_buttons_frame, text="Approve Vacations and Sick Leaves", command=self.approve_vacations_sick_leaves, font=("Helvetica", 14))
        approve_vacations_sick_leaves_button.grid(row=0, column=1, padx=10)

        progress_on_task_button = tk.Button(boss_buttons_frame, text="Progress on Task", command=self.progress_on_task, font=("Helvetica", 14))
        progress_on_task_button.grid(row=0, column=2, padx=10)

        approve_promotion_button = tk.Button(boss_buttons_frame, text="Approve Promotion", command=self.approve_promotion, font=("Helvetica", 14))
        approve_promotion_button.grid(row=1, column=0, pady=10)

        approve_resignation_button = tk.Button(boss_buttons_frame, text="Approve Resignation", command=self.approve_resignation, font=("Helvetica", 14))
        approve_resignation_button.grid(row=1, column=1, pady=10)

        request_bonus_button = tk.Button(boss_buttons_frame, text="Request for Bonus", command=self.request_bonus, font=("Helvetica", 14))
        request_bonus_button.grid(row=1, column=2, pady=10)

        # Bind the window resize event for the boss window
        boss_window.bind("<Configure>", lambda event, img=self.boss_img, label=boss_background_label: self.resize_image(event, img, label))

        # Run the main loop for the boss window
        boss_window.mainloop()

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

    def create_remove_hr(self):
        messagebox.showinfo("Admin Window", "Create/Remove HR Login Button Pressed")
   
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



def main():
    root = tk.Tk()
    root.geometry("800x600")  # Set the window size
    app = CreativeLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
