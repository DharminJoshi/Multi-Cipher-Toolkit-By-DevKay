# Multi-Cipher-Toolkit-By-DevKay

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-v2.2-green) ![Bootstrap](https://img.shields.io/badge/Bootstrap-v5-purple)

A web-based application that allows users to encrypt and decrypt text using multiple classical ciphers, including Caesar, Monoalphabetic, Playfair, Hill, Rail Fence, Columnar Transposition, and Homophonic Substitution.

---

## Features

- 🔐 **Multiple Ciphers Supported**: Caesar, Monoalphabetic, Playfair, Hill (2x2), Rail Fence, Columnar Transposition, Homophonic Substitution.
- 🔄 **Encrypt and Decrypt Modes**: Easily switch between encrypting and decrypting text.
- 🖋️ **Custom Keywords and Shifts**: Customize keys, shifts, and other cipher parameters.
- 🧑‍💻 **Preserve Case Option**: Preserve the original case of text for Caesar cipher.
- 📋 **Copy to Clipboard**: Easily copy the output with a convenient button.
- 🎨 **Responsive UI**: Built with Bootstrap for clean, user-friendly, and responsive interface.
- 🔗 **Social Links**: Connect with the developer via LinkedIn, Instagram, YouTube, Fiverr, and Discord.

---

## Tech Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Backend**: Python, Flask
- **Additional Libraries**: Custom Python classes for ciphers

---

## Getting Started

### Prerequisites

Ensure you have installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/latest/installation/)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DharminJoshi/Multi-Cipher-Toolkit-By-DevKay.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Multi-Cipher-Toolkit-By-DevKay
   ```
3. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
4. Install dependencies:
   ```bash
   pip install flask
   ```
5. Run the Flask app:
   ```bash
   flask run
   ```
6. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

---

## Usage

1. Select the cipher you want to use from the dropdown.
2. Choose the mode: Encrypt or Decrypt.
3. Enter the text you want to process.
4. Provide additional inputs as needed (shift number, keyword, rails count).
5. (Optional) Check “Preserve Case” for Caesar cipher.
6. Click **Go!** to see the output.
7. Use the **Copy to Clipboard** button next to the output to copy your result easily.
8. Connect with the developer through the social media links at the bottom of the page.

---

## Folder Structure

```
multi-cipher-toolkit-by-devkay/
├── cipher-web/
│   ├── app.py                   # Flask web app entry point
│   └── templates/
│       └── app.py               # HTML template (Jinja2)
├── cipher-python/
│   └── main.py                  # Python script with cipher implementations / CLI app
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
└── LICENSE                     # License file

```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repo.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature or fix bug"
   ```
4. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a Pull Request describing your changes.

---

## Future Enhancements

- Add more classical and modern ciphers.
- Support file upload and download for encryption/decryption.
- Implement user authentication to save cipher presets.
- Add dark mode toggle and theme customization.
- Improve error handling and input validation.

---

## Screenshots

![Screenshot of Multi-Cipher-Toolkit](https://github.com/user-attachments/assets/5d7505f8-0df1-4f1d-be04-4dd7bf8e67ac)


---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## © Copyright Disclaimer:

This project, **Multi-Cipher-Toolkit-By-DevKay**, is intended for educational and personal use only. All content, including code, images, and resources, are used under the principle of fair use. The project is a non-commercial, open-source endeavor created for learning purposes and is not associated with any official or commercial entity.

All trademarks, logos, and brand names mentioned or used in this project are the property of their respective owners. This project does not claim ownership of any of these trademarks, logos, or brand names.

The project is provided "as is" without any warranties, express or implied. The creator of this project is not responsible for any direct or indirect consequences arising from its use.

This project belongs to **DharminJoshi/DevKay** and is hosted on GitHub.

---

## ⚠️ Disclaimer

This project is intended **only for educational and personal use**.  
All source code, content, and references belong to their rightful owners.

> Provided "as is" — the developer assumes no liability for any misuse or consequences.

---

## Contact

For questions or feedback, please reach out:

- **Developer:** Dharmin Joshi / DevKay  
- **Email:** info.dharmin@gmail.com  
- **LinkedIn:** [https://www.linkedin.com/in/dharmin-joshi-3bab42232/](https://www.linkedin.com/in/dharmin-joshi-3bab42232/)  
- **GitHub:** [https://github.com/DharminJoshi](https://github.com/DharminJoshi)  

---

Thank you for using the **Multi-Cipher-Toolkit-By-DevKay**! Happy encrypting! 🔐🚀

---
