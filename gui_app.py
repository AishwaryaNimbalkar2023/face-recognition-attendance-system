import tkinter as tk
from tkinter import messagebox, ttk
import capture_faces
import encode_faces
import recognition_faces
from attendance_viewer import get_attendance_records

root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("1000x700")  

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def show_main_menu():
    clear_frame()
    tk.Label(main_frame, text="Welcome", font=("Arial", 28)).pack(pady=30)

    tk.Button(main_frame, text="Take Attendance", font=("Arial", 14), width=30, command=take_attendance).pack(pady=10)
    tk.Button(main_frame, text="Register New Student", font=("Arial", 14), width=30, command=show_register_form).pack(pady=10)
    tk.Button(main_frame, text="View Attendance", font=("Arial", 14), width=30, command=select_attendance_filter).pack(pady=10)
    tk.Button(main_frame, text="Exit", font=("Arial", 14), width=30, command=root.destroy).pack(pady=10)

def show_register_form():
    clear_frame()
    tk.Label(main_frame, text="Register New Student", font=("Arial", 20)).pack(pady=20)

    tk.Label(main_frame, text="Name:", font=("Arial", 14)).pack()
    entry_name = tk.Entry(main_frame, width=40, font=("Arial", 12))
    entry_name.pack()

    tk.Label(main_frame, text="Roll No:", font=("Arial", 14)).pack()
    entry_roll = tk.Entry(main_frame, width=40, font=("Arial", 12))
    entry_roll.pack()

    status_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="blue")
    status_label.pack(pady=5)

    def on_submit():
        name = entry_name.get().strip()
        roll_no = entry_roll.get().strip()

        if not name or not roll_no:
            messagebox.showerror("Error", "Please enter both Name and Roll No.")
            return

        capture_btn.config(state="disabled")
        back_btn.config(state="disabled")
        status_label.config(text="Encoding in progress...")

        root.after(100, lambda: run_encoding(name, roll_no))

    def run_encoding(name, roll_no):
        try:
            capture_faces.capture_faces(name, roll_no)
            encode_faces.train_and_save_encodings()
            status_label.config(text="Encoding complete.")
            messagebox.showinfo("Success", f"{name}'s photos captured and training updated.")
            show_main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            status_label.config(text="Encoding failed.")
            capture_btn.config(state="normal")
            back_btn.config(state="normal")

    capture_btn = tk.Button(main_frame, text="Capture Photos", font=("Arial", 14), command=on_submit)
    capture_btn.pack(pady=20)

    back_btn = tk.Button(main_frame, text="Back", font=("Arial", 12), command=show_main_menu)
    back_btn.pack()

def take_attendance():
    try:
        messagebox.showinfo("Info", "Please look into the camera to mark your attendance.")
        name, status = recognition_faces.recognize_and_mark_attendance()
        print(f"[DEBUG] Returned name: {name}, status: {status}")

        if name and status == "marked":
            messagebox.showinfo("Success", f"Attendance marked successfully for {name}.")
        elif name and status == "already":
            messagebox.showwarning("Warning", f"Attendance already marked for {name} today.")
        else:
            messagebox.showerror("Error", "No known face detected or an error occurred.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def select_attendance_filter():
    clear_frame()
    tk.Label(main_frame, text="View Attendance", font=("Arial", 20)).pack(pady=20)
    tk.Button(main_frame, text="Day-wise", font=("Arial", 14), width=30, command=show_daywise_attendance).pack(pady=10)
    tk.Button(main_frame, text="Month-wise", font=("Arial", 14), width=30, command=show_monthwise_attendance).pack(pady=10)
    tk.Button(main_frame, text="Back", font=("Arial", 12), command=show_main_menu).pack(pady=10)

def create_table(records, heading):
    clear_frame()
    tk.Label(main_frame, text=heading, font=("Arial", 20)).pack(pady=10)

    table_frame = tk.Frame(main_frame)
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("name", "student_id", "date", "time")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col.title())
        tree.column(col, width=200, anchor="center")

    for row in records:
        tree.insert("", "end", values=row)


    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    def download_csv():
        from tkinter import filedialog
        import csv

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Attendance CSV"
        )
        if file_path:
            try:
                with open(file_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)
                    writer.writerows(records)
                messagebox.showinfo("Success", f"CSV saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file:\n{e}")

    tk.Button(main_frame, text="Download CSV", font=("Arial", 12), command=download_csv).pack(pady=5)
    tk.Button(main_frame, text="Back", font=("Arial", 12), command=select_attendance_filter).pack(pady=10)

def show_daywise_attendance():
    clear_frame()
    tk.Label(main_frame, text="Enter Date (YYYY-MM-DD):", font=("Arial", 14)).pack(pady=10)
    entry_date = tk.Entry(main_frame, font=("Arial", 12), width=20)
    entry_date.pack()

    def fetch_data():
        date = entry_date.get().strip()
        try:
            records = get_attendance_records("day", date)
            if not records:
                messagebox.showinfo("Info", "No records found for that date.")
            else:
                create_table(records, f"Attendance on {date}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(main_frame, text="Fetch", font=("Arial", 12), command=fetch_data).pack(pady=10)
    tk.Button(main_frame, text="Back", font=("Arial", 12), command=select_attendance_filter).pack(pady=5)

def show_monthwise_attendance():
    clear_frame()
    tk.Label(main_frame, text="Enter Month (YYYY-MM):", font=("Arial", 14)).pack(pady=10)
    entry_month = tk.Entry(main_frame, font=("Arial", 12), width=20)
    entry_month.pack()

    def fetch_data():
        month = entry_month.get().strip()
        try:
            records = get_attendance_records("month", month)
            if not records:
                messagebox.showinfo("Info", "No records found for that month.")
            else:
                create_table(records, f"Attendance for {month}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(main_frame, text="Fetch", font=("Arial", 12), command=fetch_data).pack(pady=10)
    tk.Button(main_frame, text="Back", font=("Arial", 12), command=select_attendance_filter).pack(pady=5)

show_main_menu()
root.mainloop()

