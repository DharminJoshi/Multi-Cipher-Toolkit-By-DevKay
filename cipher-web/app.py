from flask import Flask, render_template, request
from ciphers import CaesarCipher, MonoalphabeticCipher, PlayfairCipher, HillCipher, RailFenceCipher, ColumnarTranspositionCipher, HomophonicCipher

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        cipher = request.form["cipher"]
        mode = request.form["mode"]
        text = request.form["text"]
        keyword = request.form.get("keyword", "")
        shift = request.form.get("shift", "")
        rails = request.form.get("rails", "")
        preserve_case = request.form.get("preserve_case") == "on"

        try:
            if cipher == "caesar":
                shift = int(shift)
                if mode == "encrypt":
                    output = CaesarCipher.encrypt(text, shift, preserve_case)
                else:
                    output = CaesarCipher.decrypt(text, shift, preserve_case)

            elif cipher == "mono":
                if mode == "encrypt":
                    output = MonoalphabeticCipher.encrypt(text, keyword)
                else:
                    output = MonoalphabeticCipher.decrypt(text, keyword)

            elif cipher == "playfair":
                if mode == "encrypt":
                    output = PlayfairCipher.encrypt(text, keyword)
                else:
                    output = PlayfairCipher.decrypt(text, keyword)

            elif cipher == "hill":
                key_matrix = [[3, 3], [2, 5]]  # example fixed key
                if mode == "encrypt":
                    output = HillCipher.encrypt(text, key_matrix)
                else:
                    output = HillCipher.decrypt(text, key_matrix) or "Decryption failed (non-invertible matrix)"

            elif cipher == "railfence":
                rails = int(rails)
                if mode == "encrypt":
                    output = RailFenceCipher.encrypt(text, rails)
                else:
                    output = RailFenceCipher.decrypt(text, rails)

            elif cipher == "columnar":
                if mode == "encrypt":
                    output = ColumnarTranspositionCipher.encrypt(text, keyword)
                else:
                    output = ColumnarTranspositionCipher.decrypt(text, keyword)

            elif cipher == "homophonic":
                if mode == "encrypt":
                    output = HomophonicCipher.encrypt(text)
                else:
                    output = HomophonicCipher.decrypt(text)

        except Exception as e:
            output = f"Error: {str(e)}"

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)
