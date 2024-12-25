# Import Necessary Libraries
import random                       # For generating random OTP
import re                           # For pattern matching (Email & OTP match)
import smtplib                      # For sending email through simple mail transfer protocol
import tkinter as tk                # For creating Graphical User Interface
from tkinter import messagebox      # Displaying messagebox for user to enter Email & OTP
import yaml                         # For loading yaml configuration file   

# Setting retry attempts to 3
retry_attempts = 3

# Generate a random 6 digit OTP
def generate_otp():
    return random.randint(100000, 999999)

# Define a function to load YAML config
def get_details():
    with open("details.yaml", "r") as file:
        return yaml.safe_load(file)

# Access email configuration
email_config = get_details()

sender_email = email_config["SENDER_EMAIL"]
sender_password = email_config["SENDER_PASSWORD"]


# Sending the OTP to users email
# Initializing a connection to Gmail's SMTP server
def send_otp_via_email(email_address, otp):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        
        # Upgrading the server to TLS (transport layer security) for data integrity and data security
        server.starttls()
        server.login(sender_email,sender_password)
        message = f"Subject: Your OTP\n\nYour OTP is {otp}"
        server.sendmail(sender_email, email_address, message)
        server.quit()
        
        # Debugging (to trace the flow of the program during code execution)
        print(f"Sending OTP {otp} to {email_address}")
        messagebox.showinfo("Success", "OTP sent successfully!")
    
    except Exception as e:
        print(f"Failed to send email: {e}")
        messagebox.showerror("Error", "Failed to send OTP")


# Ensure the submitted OTP matches the generated OTP
def verify_otp():
    global generated_otp, retry_attempts
    try: 
        entered_otp = int(otp_entry.get())
        if entered_otp == generated_otp:
            messagebox.showinfo("Success", "OTP verified successfully!")
            retry_attempts = 3  # Reset the attempts on successful verification
        else:
            retry_attempts -= 1
        if retry_attempts > 0:
                messagebox.showerror("Error", f"Invalid OTP. You have {retry_attempts} attempt(s) left.")
        else:
            messagebox.showerror("Error", "Invalid OTP.")
    except:
        messagebox.showerror("Error", "Please enter a valid 6-digit OTP")


# OTP sending process
def send_otp_to_email():
    global generated_otp, retry_attempts 
    email = email_entry.get()
    
    # Regex pattern for email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'

    if not re.match(email_pattern, email):
        messagebox.showerror("Error", "Please enter a valid email address")
    else:
        generated_otp = generate_otp()
        send_otp_via_email(email, generated_otp)
        retry_attempts = 3


# Graphical user interface setup using tkinter
GUI = tk.Tk()
GUI.title("OTP Verification System")
GUI.geometry("400x400")

# Gmail input
tk.Label(GUI, text="Enter Your Gmail Address").pack(pady=5)
email_entry = tk.Entry(GUI, width=20)
email_entry.pack(pady=5)

# Send OTP Button
send_otp_button = tk.Button(GUI, text="Send OTP", command=send_otp_to_email, bg="blue", fg="white")
send_otp_button.pack(pady=5)

# OTP input
tk.Label(GUI, text="Enter OTP").pack(pady=5)
otp_entry = tk.Entry(GUI, width=10)
otp_entry.pack(pady=5)

# Verify OTP Button
verify_otp_button = tk.Button(GUI, text="Verify OTP", command=verify_otp, bg="green", fg="white")
verify_otp_button.pack(pady=5)

# Run Tkinter Loop
GUI.mainloop()
