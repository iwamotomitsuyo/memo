import tkinter as tk
from tkinter import filedialog, font
from PIL import Image, ImageTk
import cv2


class MemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memo App")
        self.geometry("800x600")
       
        # フォント設定
        self.selected_font = ("Helvetica", 12)
       
        # 動画再生
        self.play_background_video("background_video.mp4")
       
        # メモ入力欄
        self.text_widget = tk.Text(self, bg="white", fg="black", font=self.selected_font)
        self.text_widget.place(relx=0.1, rely=0.23, relwidth=0.8, relheight=0.65)
       
        # ファイルメニュー
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
       
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Exit", command=self.quit)
       
        # フォントメニュー
        self.font_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Font", menu=self.font_menu)
        self.font_menu.add_command(label="Select Font", command=self.select_font)
       


    def play_background_video(self, video_file):
        self.cap = cv2.VideoCapture(video_file)
        self.video_frame = tk.Label(self)
        self.video_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.update_video_frame()


    def update_video_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.video_frame.configure(image=frame)
            self.video_frame.image = frame
            self.after(30, self.update_video_frame)
        else:
            self.cap.release()
            self.play_background_video("background_video.mp4")  # 動画が終了したら再度再生


            # メモ入力欄を最前面に移動
            self.text_widget.lift()


    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                text_content = self.text_widget.get("1.0", tk.END)
                file.write(text_content)
            print("File saved successfully.")
   
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert("1.0", file_content)
            print("File opened successfully.")


    def select_font(self):
        self.selected_font = font.families()
        font_dialog = tk.Toplevel()
        font_dialog.title("Select Font")
        font_dialog.geometry("400x300")
       
        font_listbox = tk.Listbox(font_dialog, selectmode=tk.SINGLE)
        font_listbox.pack(fill=tk.BOTH, expand=True)
        for font_family in self.selected_font:
            font_listbox.insert(tk.END, font_family)
       
        font_listbox.bind("<Double-Button-1>", lambda event: self.apply_selected_font(font_listbox.get(tk.ACTIVE)))


    def apply_selected_font(self, selected_font_family):
        self.selected_font = (selected_font_family, 12)  # フォントサイズはデフォルトで12に設定
        self.text_widget.config(font=self.selected_font)


if __name__ == "__main__":
    app = MemoApp()
    app.mainloop()
