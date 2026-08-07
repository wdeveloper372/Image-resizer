import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from tkinterdnd2 import TkinterDnD, DND_FILES

class ImageResizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer")
        self.root.geometry("400x3555)

        self.file_path = ""

        # UI Elements
        self.btn_load = tk.Button(root, text="Select Photo", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.lbl_drop = tk.Label(root, text="Drag and Drop Photo Here", bg="lightgray", width=40, height=5)
        self.lbl_drop.pack(pady=10)
        self.lbl_drop.drop_target_register(DND_FILES)
        self.lbl_drop.dnd_bind('<<Drop>>', self.drop_image)

        self.lbl_info = tk.Label(root, text="No image selected")
        self.lbl_info.pack(pady=5)

        self.lbl_width = tk.Label(root, text="New Width:")
        self.lbl_width.pack()
        self.entry_width = tk.Entry(root)
        self.entry_width.pack()

        self.lbl_height = tk.Label(root, text="New Height:")
        self.lbl_height.pack()
        self.entry_height = tk.Entry(root)
        self.entry_height.pack()

        self.btn_resize = tk.Button(root, text="Resize and Save", command=self.resize_image)
        self.btn_resize.pack(pady=15)

    def load_image(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        )
        if self.file_path:
            self.lbl_info.config(text=f"Selected: {os.path.basename(self.file_path)}")

    def drop_image(self, event):
        self.file_path = event.data.strip('{}')
        self.lbl_info.config(text=f"Selected: {os.path.basename(self.file_path)}")

    def resize_image(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for width and height.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")],
        )

        if save_path:
            try:
                img = Image.open(self.file_path)
                img_resized = img.resize((width, height))
                img_resized.save(save_path)
                messagebox.showinfo("Success", "Image resized and saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageResizer(root)
    root.mainloop()
