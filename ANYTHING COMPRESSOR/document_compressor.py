import os
from tkinter import (
    Tk,
    Label,
    Button,
    filedialog,
    StringVar,
    messagebox,
    Scale,
    HORIZONTAL,
)
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image


# Function to compress PDF
def compress_pdf(input_path, output_path):
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, "wb") as output_file:
            writer.write(output_file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compress PDF: {e}")


# Function to compress images
def compress_image(input_path, output_path, quality):
    try:
        img = Image.open(input_path)
        img.save(output_path, optimize=True, quality=quality)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compress image: {e}")


# Function to handle file compression
def compress_file():
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[("PDF files", "*.pdf"), ("Image files", "*.jpg *.jpeg *.png")],
    )
    if not file_path:
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".pdf" if file_path.endswith(".pdf") else ".jpg",
        filetypes=[("PDF files", "*.pdf"), ("Image files", "*.jpg *.jpeg *.png")],
    )

    if not output_path:
        return

    status.set("Compressing...")
    root.update()

    if file_path.endswith(".pdf"):
        compress_pdf(file_path, output_path)
    else:
        quality = compression_level.get()
        compress_image(file_path, output_path, quality)

    status.set("Compression Complete")
    messagebox.showinfo("Success", f"File compressed and saved to: {output_path}")


# Main GUI
root = Tk()
root.title("Document Compression App")
root.geometry("400x300")
root.resizable(False, False)

# Status label
status = StringVar()
status.set("Select a file to compress")
Label(root, textvariable=status, fg="blue", font=("Arial", 10)).pack(pady=10)

# Slider for compression level
Label(root, text="Set Compression Level (Image Quality):", font=("Arial", 10)).pack(
    pady=5
)
compression_level = Scale(
    root, from_=10, to=100, orient=HORIZONTAL, length=300, tickinterval=10
)
compression_level.set(70)  # Default quality level
compression_level.pack(pady=5)

# Compress button
Button(
    root,
    text="Compress File",
    command=compress_file,
    bg="green",
    fg="white",
    font=("Arial", 12),
).pack(pady=20)

# Exit button
Button(
    root, text="Exit", command=root.quit, bg="red", fg="white", font=("Arial", 12)
).pack(pady=10)

# Run the application
root.mainloop()
