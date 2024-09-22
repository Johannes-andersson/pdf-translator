# pdf-translator


Here's a detailed and organized README file template for your PDF Translator project. This README will guide users on how to set up, run, and troubleshoot the project.

PDF Translator
This project is a Python-based PDF Translator that extracts text from PDF files, translates the text using Google Translator from deep-translator, and saves the translated text back into a new PDF file. The tool is designed to handle multi-page documents and works with various languages supported by Google Translator.

Features
Extracts text from each page of a PDF.
Translates text using Google Translator.
Supports translation to multiple languages.
Saves the translated text into a new PDF with the original layout preserved.
Technologies Used
Python 3.7+
deep-translator for translation
PyPDF2 for PDF manipulation
reportlab for creating PDFs
Installation
Step 1: Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/pdf-translator.git
cd pdf-translator
Step 2: Set Up a Virtual Environment (Optional but Recommended)
It's recommended to create a virtual environment to manage dependencies.

bash
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy code
venv\Scripts\activate
On macOS/Linux:

bash
Copy code
source venv/bin/activate
Step 3: Install Required Packages
Install the required dependencies using pip:

bash
Copy code
pip install -r requirements.txt
If you don't have a requirements.txt, create one with the following content:

plaintext
Copy code
PyPDF2
reportlab
deep-translator
nltk
Usage
1. Run the Script
Use the command below to run the script:

bash
Copy code
python pdf.py
2. Select the PDF File
The program will prompt you to select the input PDF file that you want to translate.

3. Choose Output File Location
The program will prompt you to select the output path where the translated PDF will be saved.

4. Set the Target Language
The program will ask you to specify the language code for translation (e.g., en for English, es for Spanish, fr for French). Refer to Google Translate language codes for more options.

5. Translation Process
The script will extract, translate, and save each page of the PDF file, displaying the progress in the terminal.

Example Command
bash
Copy code
python pdf.py
Troubleshooting
Common Errors and Fixes
ImportError: "deep_translator" could not be resolved

Ensure the deep-translator package is installed: pip install deep-translator
Verify that the correct Python interpreter is selected in your IDE (e.g., VS Code).
Translation Error: list index out of range

This error typically occurs when there's an issue with text extraction. Make sure your PDF is not encrypted or protected.
Multiple Definitions Warning (e.g., /MediaBox)

These warnings are common when PDFs have complex structures or duplicate dictionary definitions. They usually don’t affect the output but can indicate minor inconsistencies in the PDF structure.
Crash When Moving the Program Window

Ensure your system has sufficient resources (memory, CPU) to handle the operation. The crash could be due to high resource usage during the translation process.
Resource 'punkt_tab' Not Found

This error can occur when using NLTK for sentence tokenization. Make sure NLTK data is properly installed:

python
Copy code
import nltk
nltk.download('punkt')
Logging
All logs related to text extraction, translation, and errors are printed in the terminal. Use these logs to identify any specific page causing issues.

Customization
Changing the Target Language
Modify the script to set a default language or add options for frequently used languages directly in the code.

Adjusting Output Formatting
You can modify how the translated text is formatted by editing the section of the code that uses reportlab to generate the new PDF.

Contribution
Contributions are welcome! Feel free to submit a pull request or report any issues.

Fork the repository.
Create your feature branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a pull request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
deep-translator for providing translation services.
PyPDF2 for PDF manipulation.
reportlab for creating PDFs.
Special thanks to the Python community for the extensive support and resources.
