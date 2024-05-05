import tkinter as tk
from tkinter import messagebox

def run_script(email, password, sleeptime, url, no_folder_flag):
    from main_script import main
    main(email, password, sleeptime, url, no_folder_flag)

def setup_gui():
    app = tk.Tk()
    app.title('Pinterest Downloader GUI')

    tk.Label(app, text="E-Mail:").grid(row=0, column=0)
    email_entry = tk.Entry(app)
    email_entry.grid(row=0, column=1)

    tk.Label(app, text="Passwort:").grid(row=1, column=0)
    password_entry = tk.Entry(app, show="*")
    password_entry.grid(row=1, column=1)

    tk.Label(app, text="Sleeptime (default 2):").grid(row=2, column=0)
    sleeptime_entry = tk.Entry(app)
    sleeptime_entry.insert(0, "2")
    sleeptime_entry.grid(row=2, column=1)

    tk.Label(app, text="URL Pinwand").grid(row=3, column=0)
    url_entry = tk.Entry(app)
    url_entry.grid(row=3, column=1)

    folder_check_var = tk.BooleanVar(value=True)
    tk.Checkbutton(app, text="In Ordner strukturieren", variable=folder_check_var).grid(row=4, columnspan=2)

    def on_run_clicked():
        run_script(email_entry.get(), password_entry.get(), sleeptime_entry.get(), url_entry.get(), not folder_check_var.get())

    run_button = tk.Button(app, text="Download starten!", command=on_run_clicked)
    run_button.grid(row=5, columnspan=2)

    app.mainloop()

if __name__ == "__main__":
    setup_gui()
