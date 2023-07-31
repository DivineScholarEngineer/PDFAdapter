import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import io
import os
import sys
from PDF_DOCX import PDF_DOCX as pd

class PDFtoText:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(0, 0)
        self.window.title('PDF To Document')

        # Add Image Logo
        self.logo = Image.open('pdfLogo.png')
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(image=self.logo)
        self.logo_label.grid(column=1, row=0)

        # Labels - Instructions
        self.instructions = tk.Label(self.window, text='Select a PDF File or Image to Text')
        self.instructions.grid(columnspan=3, column=0, row=1)

        # Browse button
        self.browse_btn = tk.Button(self.window, text='Browse', command=self.open_file)
        self.browse_btn.grid(column=1, row=2)

        # Text Box
        self.text_box = tk.Text(self.window, height=10, width=50, padx=15, pady=15)
        self.text_box.grid(column=1, row=3)

        # Save button
        self.save_btn = tk.Button(self.window, text='Save', command=self.save_file)
        self.save_btn.grid(row=4, column=0, sticky=tk.W)

        # Clear button
        self.clear_btn = tk.Button(self.window, text='Clear', command=self.clear_text)
        self.clear_btn.grid(row=4, column=2, sticky=tk.E)

        # Exit button
        self.exit_btn = tk.Button(self.window, text='Exit', width=6, command=self.exit_click)
        self.exit_btn.grid(row=5, column=0, sticky=tk.W)

    def open_file(self):
        self.file_path = filedialog.askopenfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf"), ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        if self.file_path == '':
            messagebox.showerror("Error", "Please select a file.")
        else:
            # pdf_docx = PDF_DOCX()
            text = pd().runner(self.file_path)
            if text == '':
                messagebox.showerror("Error", "The selected file is empty.")
            else:
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, text)

    def save_file(self):
        text_content = self.text_box.get(1.0, tk.END)
        if not text_content.strip():
            messagebox.showwarning('Error', 'No text to save.')
            return

        file_path = filedialog.asksaveasfile(initialfile=f'{os.path.splitext(os.path.basename(self.file_path))[0]}.txt',
                                             defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path.name, 'w', encoding='utf-8') as f:
                f.write(text_content)
            messagebox.showinfo('Success', 'Text saved successfully.')

    def clear_text(self):
        self.text_box.delete(1.0, tk.END)

    def exit_click(self):
        self.window.destroy()
        sys.exit()

    def run(self):
        self.window.mainloop()