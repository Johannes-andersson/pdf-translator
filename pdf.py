import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
import re
import logging
import time
import threading
from deep_translator import GoogleTranslator  # Use deep-translator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename='pdf_translator.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to split text into sentences using regular expressions
def split_into_sentences(text):
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(text)
    return sentences

# Function to select PDF file
def select_pdf():
    filepath = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")], defaultextension=".pdf"
    )
    if filepath:
        input_path_var.set(filepath)

# Function to select the output file path
def select_output_path():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
    )
    if filepath:
        output_path_var.set(filepath)

# Function to translate the text content
def translate_text(content, src_lang, dest_lang):
    try:
        translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(content)
        return translated
    except Exception as e:
        logging.error(f"Translation Error: {e}")
        return content  # Return original content if translation fails

# Function to process and translate the PDF file
def translate_pdf():
    input_path = input_path_var.get()
    output_path = output_path_var.get()

    if not input_path or not output_path:
        root.after(0, lambda: messagebox.showerror("Error", "Please select input and output files."))
        return

    try:
        # Suppress PyPDF2 warnings
        logging.getLogger('PyPDF2').setLevel(logging.ERROR)

        reader = PdfReader(input_path)
        c = canvas.Canvas(output_path)

        # Register a built-in CID font for better Unicode support
        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

        language_pairs = {
            "English to Spanish": ("en", "es"),
            "Spanish to English": ("es", "en"),
        }

        src_lang, dest_lang = language_pairs.get(lang_var.get(), ("en", "es"))

        for page_num, page in enumerate(reader.pages):
            try:
                text = page.extract_text()
                logging.info(f"Extracted text from page {page_num}")

                if text:
                    # Use regex to split text into sentences
                    sentences = split_into_sentences(text)
                    translated_sentences = []

                    for sentence in sentences:
                        if sentence.strip():
                            translated_sentence = translate_text(sentence, src_lang, dest_lang)
                            translated_sentences.append(translated_sentence)
                            time.sleep(0.1)  # Add a small delay to prevent rate-limiting

                    translated_text = ' '.join(translated_sentences)
                    logging.info(f"Translated text for page {page_num}")

                    width = float(page.mediabox.width)
                    height = float(page.mediabox.height)

                    c.setPageSize((width, height))

                    textobject = c.beginText()
                    textobject.setFont("HeiseiMin-W3", 12)  # Use the CID font

                    x_margin = 50
                    y_margin = 50
                    y_position = height - y_margin
                    max_width = width - 2 * x_margin

                    # Split translated text into words
                    words = translated_text.replace('\n', ' ').split(' ')
                    line = ''
                    for word in words:
                        test_line = line + word + ' '
                        if stringWidth(test_line, "HeiseiMin-W3", 12) <= max_width:
                            line = test_line
                        else:
                            textobject.setTextOrigin(x_margin, y_position)
                            textobject.textLine(line.strip())
                            y_position -= 14
                            line = word + ' '
                            if y_position <= y_margin:
                                c.drawText(textobject)
                                c.showPage()
                                c.setPageSize((width, height))
                                textobject = c.beginText()
                                textobject.setFont("HeiseiMin-W3", 12)
                                y_position = height - y_margin
                    if line:
                        textobject.setTextOrigin(x_margin, y_position)
                        textobject.textLine(line.strip())

                    c.drawText(textobject)
                    c.showPage()
                else:
                    logging.warning(f"No text extracted from page {page_num}.")
            except Exception as e:
                logging.error(f"Error processing page {page_num}: {e}")
                continue  # Skip to the next page

        # Save the PDF after all pages are processed
        c.save()
        logging.info("PDF has been translated and saved successfully.")
        root.after(0, show_success_message)

    except Exception as e:
        logging.error(f"Error translating PDF: {e}")
        root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {e}"))
    finally:
        # Re-enable the start button
        root.after(0, lambda: start_button.config(state='normal'))

def show_success_message():
    messagebox.showinfo("Success", "PDF has been translated and saved successfully!")

def start_translation():
    if input_path_var.get() and output_path_var.get():
        start_button.config(state='disabled')
        translation_thread = threading.Thread(target=translate_pdf)
        translation_thread.start()
    else:
        messagebox.showerror("Error", "Please select the input and output PDF paths before starting.")

# GUI Setup
root = tk.Tk()
root.title("PDF Translator")
root.geometry("400x350")

# Variables
input_path_var = tk.StringVar()
output_path_var = tk.StringVar()
lang_var = tk.StringVar(value="English to Spanish")

# Input PDF Path
tk.Label(root, text="Select PDF to Translate:").pack(pady=10)
tk.Entry(root, textvariable=input_path_var, width=40).pack(pady=5)
tk.Button(root, text="Browse", command=select_pdf).pack(pady=5)

# Output PDF Path
tk.Label(root, text="Select Output PDF Path:").pack(pady=10)
tk.Entry(root, textvariable=output_path_var, width=40).pack(pady=5)
tk.Button(root, text="Save As", command=select_output_path).pack(pady=5)

# Language Selection
tk.Label(root, text="Select Translation Direction:").pack(pady=10)
tk.OptionMenu(root, lang_var, "English to Spanish", "Spanish to English").pack(pady=5)

# Start Translation Button
start_button = tk.Button(root, text="Start Translation", command=start_translation)
start_button.pack(pady=20)

root.mainloop()















