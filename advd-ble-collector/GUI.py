import tkinter as tk

class WelcomeWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Welcome to the program!")
        self.label.pack()

        self.device_type = tk.StringVar()
        self.device_type.set("TH")

        self.th_button = tk.Radiobutton(self, text="TH", variable=self.device_type, value="TH")
        self.td_button = tk.Radiobutton(self, text="TD", variable=self.device_type, value="TD")
        self.th_button.pack()
        self.td_button.pack()

        self.next_button = tk.Button(self, text="Next", command=self.next_window)
        self.next_button.pack()

    def next_window(self):
        start_serial = ""
        end_serial = ""
        timeout = ""
        self.master.switch_frame(ScanWindow, self.device_type.get(), start_serial, end_serial, timeout)

        class ScanWindow(tk.Frame):
    def __init__(self, master=None, device_type="", start_serial="", end_serial="", timeout=""):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.device_type = device_type
        self.start_serial = start_serial
        self.end_serial = end_serial
        self.timeout = timeout

    def create_widgets(self):
        self.start_label = tk.Label(self, text="Start Serial:")
        self.start_entry = tk.Entry(self)
        self.start_label.pack()
        self.start_entry.pack()

        self.end_label = tk.Label(self, text="End Serial:")
        self.end_entry = tk.Entry(self)
        self.end_label.pack()
        self.end_entry.pack()

        self.timeout_label = tk.Label(self, text="Timeout:")
        self.timeout_entry = tk.Entry(self)
        self.timeout_label.pack()
        self.timeout_entry.pack()

        self.scan_button = tk.Button(self, text="Scan", command=self.scan)
        self.scan_button.pack()

    def scan(self):
        # Асинхронный код сканирования
        print("Scanning...")

        # Проверка на таймаут
        if timeout:
            answer = tk.messagebox.askyesno("Timeout", "Timeout occurred. Do you want to retry?")
            if answer:
                self.timeout = tk.simpledialog.askstring("Timeout", "Enter new timeout value:")
                self.scan()
            else:
                self.master.switch_frame(ResultWindow, result_df)

class ResultWindow(tk.Frame):
    def __init__(self, master=None, result_df=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.result_df = result_df

    def create_widgets(self):
        self.result_label = tk.Label(self, text="Result:")
        self.result_label.pack()

        self.result_text = tk.Text(self)
        self.result_text.insert(tk.END, self.result_df.to_string())
        self.result_text.pack()

        self.save_button = tk.Button(self, text="Save Logs", command=self.save_logs)
        self.save_button.pack()

    def save_logs(self):
        # Выбор папки для сохранения
        folder_path = tk.filedialog.askdirectory()

        # Сохранение логов
        self.result_df.to_csv(folder_path + "/logs.csv", index=False)

        class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Program")
        self.geometry("400x300")
        self.switch_frame(WelcomeWindow)

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, *args)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

if __name__ == "__main__":
    app = Application()
    app.mainloop()