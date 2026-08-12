import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps
from tkinterdnd2 import TkinterDnD, DND_FILES


class ImageResizer:

  def __init__(self, root):
    self.root = root
    self.root.title("Image Resizer")
    self.root.geometry("400x450")

    self.file_path = ""

    # UI Elements
    self.btn_load = tk.Button(root, text="Select Photo", command=self.load_image)
    self.btn_load.pack(pady=10)

    self.lbl_drop = tk.Label(
        root,
        text="Drag and Drop Photo Here",
        bg="lightgray",
        width=40,
        height=5,
    )
    self.lbl_drop.pack(pady=10)
    self.lbl_drop.drop_target_register(DND_FILES)
    self.lbl_drop.dnd_bind("<<Drop>>", self.drop_image)

    self.lbl_info = tk.Label(root, text="No image selected")
    self.lbl_info.pack(pady=5)

    self.lbl_width = tk.Label(root, text="Target Width:")
    self.lbl_width.pack()
    self.entry_width = tk.Entry(root)
    self.entry_width.pack()

    self.lbl_height = tk.Label(root, text="Target Height:")
    self.lbl_height.pack()
    self.entry_height = tk.Entry(root)
    self.entry_height.pack()

    self.btn_resize = tk.Button(
        root, text="Resize and Save", command=self.start_resize_thread
    )
    self.btn_resize.pack(pady=15)

  def load_image(self):
    self.file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    if self.file_path:
      self.lbl_info.config(text=f"Selected: {os.path.basename(self.file_path)}")

  def drop_image(self, event):
    self.file_path = event.data.strip("{}")
    self.lbl_info.config(text=f"Selected: {os.path.basename(self.file_path)}")

  def start_resize_thread(self):
    threading.Thread(target=self.resize_image, daemon=True).start()

  def resize_image(self):
    if not self.file_path:
      messagebox.showerror("Error", "Please select an image first.")
      return

    try:
      width = int(self.entry_width.get())
      height = int(self.entry_height.get())
      target_size = (width, height)
    except ValueError:
      messagebox.showerror(
          "Error", "Please enter valid numbers for width and height."
      )
      return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")],
    )

    if save_path:
      try:
        # Open original image
        original_image = Image.open(self.file_path)

        # Convert mode if needed
        if original_image.mode not in ("RGB", "RGBA"):
          original_image = original_image.convert("RGBA")

        # Automatically scale and crop to fill the target size completely (no padding)
        cropped_image = ImageOps.fit(
            original_image, target_size, method=Image.Resampling.LANCZOS
        )

        # Handle JPEG format conversion (no transparency allowed)
        if save_path.lower().endswith((".jpg", ".jpeg")):
          cropped_image = cropped_image.convert("RGB")

        # Save file
        cropped_image.save(save_path)

        # Reset UI fields and values on the main thread safely
        self.root.after(0, self.reset_ui)

        messagebox.showinfo(
            "Success", "Image cropped and resized to fill screen!"
        )
      except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")

  def reset_ui(self):
    self.file_path = ""
    self.lbl_info.config(text="No image selected")
    self.entry_width.delete(0, tk.END)
    self.entry_height.delete(0, tk.END)


if __name__ == "__main__":
  root = TkinterDnD.Tk()
  app = ImageResizer(root)
  root.lift()
  root.attributes("-topmost", True)
  root.mainloop()