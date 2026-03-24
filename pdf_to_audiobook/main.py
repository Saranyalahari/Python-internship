from tkinter import *
from tkinter import filedialog, messagebox
import threading

from pdf_reader import extract_text_from_pdf
from tts_converter import speak_text, save_audio, stop_speech
from utils import clean_text


pdf_text = ""


# 📂 Upload PDF
def upload_pdf():
    global pdf_text

    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")]
    )

    if file_path:
        raw_text = extract_text_from_pdf(file_path)
        pdf_text = clean_text(raw_text)

        messagebox.showinfo("Success", "PDF Loaded Successfully!")


# ▶️ Play Audio (Threaded)
def play_audio():
    if pdf_text == "":
        messagebox.showerror("Error", "Upload PDF first")
        return

    rate = speed_slider.get()
    volume = volume_slider.get()

    thread = threading.Thread(
        target=speak_text,
        args=(pdf_text, rate, volume)
    )
    thread.start()


# ⏹ Stop Audio
def stop_audio():
    stop_speech()


# 💾 Export MP3
def export_audio():
    if pdf_text == "":
        messagebox.showerror("Error", "Upload PDF first")
        return

    file = save_audio(pdf_text)
    messagebox.showinfo("Saved", f"Audio saved as {file}")


# 🎨 GUI
root = Tk()
root.title("PDF to Audiobook Converter")
root.geometry("450x400")


Label(root, text="PDF to Audiobook Converter",
      font=("Arial", 16, "bold")).pack(pady=10)


Button(root, text="Upload PDF", command=upload_pdf).pack(pady=10)


# 🎚 Speed Control
Label(root, text="Speech Speed").pack()
speed_slider = Scale(root, from_=100, to=250, orient=HORIZONTAL)
speed_slider.set(150)
speed_slider.pack()


# 🔊 Volume Control
Label(root, text="Volume").pack()
volume_slider = Scale(root, from_=0, to=1,
                      resolution=0.1, orient=HORIZONTAL)
volume_slider.set(1.0)
volume_slider.pack()


# 🎮 Controls
Button(root, text="Play Audio", command=play_audio,
       bg="green", fg="white").pack(pady=10)

Button(root, text="Stop Audio", command=stop_audio,
       bg="red", fg="white").pack(pady=5)

Button(root, text="Export MP3", command=export_audio,
       bg="blue", fg="white").pack(pady=10)


root.mainloop()