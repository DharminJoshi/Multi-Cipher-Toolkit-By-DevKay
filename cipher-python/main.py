import string
from collections import Counter
from typing import Optional, List, Tuple
import tkinter as tk
from tkinter import ttk, messagebox

class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Cipher Toolkit")

        self.cipher_methods = {
            "Caesar Cipher": self.caesar_gui,
            "Monoalphabetic Cipher": self.mono_gui,
            "Homophonic Cipher": self.homo_gui,
            "Playfair Cipher": self.playfair_gui,
            "Hill Cipher (2x2)": self.hill_gui,
            "Rail Fence Cipher": self.rail_gui,
            "Columnar Transposition": self.columnar_gui,
        }

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Select Cipher Method:").pack(pady=5)
        self.cipher_select = ttk.Combobox(self.root, values=list(self.cipher_methods.keys()), state='readonly')
        self.cipher_select.pack(pady=5)
        self.cipher_select.bind("<<ComboboxSelected>>", self.update_gui)

        self.form_frame = ttk.Frame(self.root)
        self.form_frame.pack(pady=10, fill="x")

        self.output_box = tk.Text(self.root, height=5, wrap='word')
        self.output_box.pack(pady=5, padx=10)

    def clear_frame(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def update_gui(self, event=None):
        self.clear_frame()
        method = self.cipher_select.get()
        if method in self.cipher_methods:
            self.cipher_methods[method]()

    def caesar_gui(self):
        self._create_text_input()
        self._create_shift_input()
        self._create_case_checkbox()
        self._create_mode_buttons(lambda text, shift, preserve, mode:
            CaesarCipher.encrypt(text, shift, preserve) if mode == 'e' else CaesarCipher.decrypt(text, shift, preserve))

    def mono_gui(self):
        self._create_text_input()
        self._create_keyword_input()
        self._create_mode_buttons(lambda text, keyword, _, mode:
            MonoalphabeticCipher.encrypt(text, keyword) if mode == 'e' else MonoalphabeticCipher.decrypt(text, keyword))

    def homo_gui(self):
        self._create_text_input()
        self._create_mode_buttons(lambda text, *_:
            HomophonicCipher.encrypt(text) if self.mode.get() == 'e' else HomophonicCipher.decrypt(text))

    def playfair_gui(self):
        self._create_text_input()
        self._create_keyword_input()
        self._create_mode_buttons(lambda text, keyword, _, mode:
            PlayfairCipher.encrypt(text, keyword) if mode == 'e' else PlayfairCipher.decrypt(text, keyword))

    def hill_gui(self):
        self._create_text_input()
        ttk.Label(self.form_frame, text="Key Matrix (2x2):").pack()
        self.entries = [tk.Entry(self.form_frame, width=5) for _ in range(4)]
        for i in range(2):
            row = ttk.Frame(self.form_frame)
            row.pack()
            for j in range(2):
                self.entries[i*2 + j].pack(in_=row, side=tk.LEFT, padx=2)

        self._create_mode_buttons(self._handle_hill)

    def rail_gui(self):
        self._create_text_input()
        ttk.Label(self.form_frame, text="Number of Rails:").pack()
        self.rails_entry = tk.Entry(self.form_frame)
        self.rails_entry.pack()

        self._create_mode_buttons(lambda text, *_:
            RailFenceCipher.encrypt(text, int(self.rails_entry.get())) if self.mode.get() == 'e' else RailFenceCipher.decrypt(text, int(self.rails_entry.get())))

    def columnar_gui(self):
        self._create_text_input()
        self._create_keyword_input()
        self._create_mode_buttons(lambda text, keyword, _, mode:
            ColumnarTranspositionCipher.encrypt(text, keyword) if mode == 'e' else ColumnarTranspositionCipher.decrypt(text, keyword))

    # --- Shared GUI Helpers ---
    def _create_text_input(self):
        ttk.Label(self.form_frame, text="Text:").pack()
        self.text_entry = tk.Entry(self.form_frame, width=50)
        self.text_entry.pack()

    def _create_shift_input(self):
        ttk.Label(self.form_frame, text="Shift:").pack()
        self.shift_entry = tk.Entry(self.form_frame)
        self.shift_entry.pack()

    def _create_keyword_input(self):
        ttk.Label(self.form_frame, text="Keyword:").pack()
        self.keyword_entry = tk.Entry(self.form_frame)
        self.keyword_entry.pack()

    def _create_case_checkbox(self):
        self.preserve_case = tk.BooleanVar(value=True)
        tk.Checkbutton(self.form_frame, text="Preserve Case", variable=self.preserve_case).pack()

    def _create_mode_buttons(self, func):
        self.mode = tk.StringVar(value='e')
        btn_frame = ttk.Frame(self.form_frame)
        btn_frame.pack(pady=5)

        tk.Radiobutton(btn_frame, text="Encrypt", variable=self.mode, value='e').pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(btn_frame, text="Decrypt", variable=self.mode, value='d').pack(side=tk.LEFT, padx=10)

        tk.Button(self.form_frame, text="Run", command=lambda: self.run_cipher(func)).pack(pady=5)

    def run_cipher(self, func):
        try:
            text = self.text_entry.get()
            keyword = self.keyword_entry.get() if hasattr(self, 'keyword_entry') else ''
            shift = int(self.shift_entry.get()) if hasattr(self, 'shift_entry') else 0
            preserve = self.preserve_case.get() if hasattr(self, 'preserve_case') else True
            mode = self.mode.get()

            output = func(text, keyword, preserve, mode)
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, output)
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    def _handle_hill(self, text, *_):
        try:
            key_vals = [int(entry.get()) for entry in self.entries]
            key_matrix = [[key_vals[0], key_vals[1]], [key_vals[2], key_vals[3]]]
            mode = self.mode.get()
            output = HillCipher.encrypt(text, key_matrix) if mode == 'e' else HillCipher.decrypt(text, key_matrix)
            if output is None:
                raise ValueError("Key matrix not invertible mod 26.")
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, output)
        except Exception as e:
            messagebox.showerror("Error", f"Hill Cipher Error:\n{e}")


# --- Caesar Cipher --
class CaesarCipher:
    @staticmethod
    def encrypt(text: str, shift: int, preserve_case: bool = True) -> str:
        result = []
        for char in text:
            if char.isalpha():
                base = 65 if char.isupper() else 97
                shifted = chr((ord(char) - base + shift) % 26 + base)
                result.append(shifted if preserve_case else shifted.lower())
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, shift: int, preserve_case: bool = True) -> str:
        return CaesarCipher.encrypt(text, -shift, preserve_case)

# --- Monoalphabetic Substitution Cipher (Keyword Cipher) ---
class MonoalphabeticCipher:
    @staticmethod
    def generate_substitution_alphabet(keyword: str) -> str:
        keyword = ''.join(dict.fromkeys(keyword.lower()))  # remove duplicates
        alphabet = string.ascii_lowercase
        substitution = keyword + ''.join(c for c in alphabet if c not in keyword)
        return substitution

    @staticmethod
    def encrypt(text: str, keyword: str) -> str:
        substitution = MonoalphabeticCipher.generate_substitution_alphabet(keyword)
        result = []
        for ch in text:
            if ch.isalpha():
                is_upper = ch.isupper()
                idx = string.ascii_lowercase.index(ch.lower())
                sub_char = substitution[idx]
                result.append(sub_char.upper() if is_upper else sub_char)
            else:
                result.append(ch)
        return ''.join(result)

    @staticmethod
    def decrypt(text: str, keyword: str) -> str:
        substitution = MonoalphabeticCipher.generate_substitution_alphabet(keyword)
        result = []
        for ch in text:
            if ch.isalpha():
                is_upper = ch.isupper()
                ch_lower = ch.lower()
                idx = substitution.index(ch_lower)
                orig_char = string.ascii_lowercase[idx]
                result.append(orig_char.upper() if is_upper else orig_char)
            else:
                result.append(ch)
        return ''.join(result)

# --- Homophonic Substitution Cipher ---
class HomophonicCipher:
    # For simplicity: assign each letter multiple symbols from a pool of numbers
    import random

    SYMBOLS_POOL = {
        'a': ['12', '24', '36'],
        'b': ['45', '52'],
        'c': ['71', '13'],
        'd': ['33', '17'],
        'e': ['01', '02', '03', '04', '05', '06'],
        'f': ['37', '39'],
        'g': ['41', '43'],
        'h': ['21', '22'],
        'i': ['07', '08', '09'],
        'j': ['55'],
        'k': ['60'],
        'l': ['49', '50'],
        'm': ['53', '54'],
        'n': ['10', '11'],
        'o': ['14', '15', '16'],
        'p': ['18', '19'],
        'q': ['61'],
        'r': ['23', '25'],
        's': ['26', '27', '28'],
        't': ['29', '30', '31'],
        'u': ['32', '34'],
        'v': ['35'],
        'w': ['38', '40'],
        'x': ['42'],
        'y': ['44'],
        'z': ['46'],
    }

    @staticmethod
    def encrypt(text: str) -> str:
        result = []
        for ch in text.lower():
            if ch in HomophonicCipher.SYMBOLS_POOL:
                # choose random symbol for the letter
                symbol = HomophonicCipher.random.choice(HomophonicCipher.SYMBOLS_POOL[ch])
                result.append(symbol)
            else:
                result.append(ch)
        return ' '.join(result)

    @staticmethod
    def decrypt(cipher_text: str) -> str:
        reverse_map = {}
        for letter, codes in HomophonicCipher.SYMBOLS_POOL.items():
            for code in codes:
                reverse_map[code] = letter
        parts = cipher_text.split()
        result = []
        for part in parts:
            if part in reverse_map:
                result.append(reverse_map[part])
            else:
                result.append(part)
        return ''.join(result)

# --- Playfair Cipher ---
class PlayfairCipher:
    @staticmethod
    def generate_key_table(keyword: str) -> List[List[str]]:
        keyword = keyword.lower().replace('j', 'i')
        seen = set()
        key_string = ""
        for ch in keyword:
            if ch.isalpha() and ch not in seen:
                seen.add(ch)
                key_string += ch
        for ch in string.ascii_lowercase:
            if ch != 'j' and ch not in seen:
                seen.add(ch)
                key_string += ch
        # 5x5 matrix
        return [list(key_string[i*5:(i+1)*5]) for i in range(5)]

    @staticmethod
    def find_position(table: List[List[str]], ch: str) -> Tuple[int, int]:
        for r in range(5):
            for c in range(5):
                if table[r][c] == ch:
                    return r, c
        raise ValueError(f"Character {ch} not found in key table")

    @staticmethod
    def preprocess_text(text: str) -> str:
        text = text.lower().replace('j', 'i')
        text = ''.join(ch for ch in text if ch.isalpha())
        result = ""
        i = 0
        while i < len(text):
            a = text[i]
            b = ''
            if i+1 < len(text):
                b = text[i+1]
            if a == b:
                result += a + 'x'
                i += 1
            else:
                if b:
                    result += a + b
                    i += 2
                else:
                    result += a + 'x'
                    i += 1
        return result

    @staticmethod
    def encrypt(text: str, keyword: str) -> str:
        table = PlayfairCipher.generate_key_table(keyword)
        text = PlayfairCipher.preprocess_text(text)
        result = []
        for i in range(0, len(text), 2):
            a, b = text[i], text[i+1]
            r1, c1 = PlayfairCipher.find_position(table, a)
            r2, c2 = PlayfairCipher.find_position(table, b)
            if r1 == r2:
                result.append(table[r1][(c1+1)%5])
                result.append(table[r2][(c2+1)%5])
            elif c1 == c2:
                result.append(table[(r1+1)%5][c1])
                result.append(table[(r2+1)%5][c2])
            else:
                result.append(table[r1][c2])
                result.append(table[r2][c1])
        return ''.join(result).upper()

    @staticmethod
    def decrypt(text: str, keyword: str) -> str:
        table = PlayfairCipher.generate_key_table(keyword)
        text = text.lower()
        result = []
        for i in range(0, len(text), 2):
            a, b = text[i], text[i+1]
            r1, c1 = PlayfairCipher.find_position(table, a)
            r2, c2 = PlayfairCipher.find_position(table, b)
            if r1 == r2:
                result.append(table[r1][(c1-1)%5])
                result.append(table[r2][(c2-1)%5])
            elif c1 == c2:
                result.append(table[(r1-1)%5][c1])
                result.append(table[(r2-1)%5][c2])
            else:
                result.append(table[r1][c2])
                result.append(table[r2][c1])
        # Return as lowercase, user can capitalize if desired
        return ''.join(result)

# --- Hill Cipher (2x2 matrix) ---
class HillCipher:
    @staticmethod
    def mod_inv(a: int, m: int) -> Optional[int]:
        # Modular inverse using extended Euclidean algorithm
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    @staticmethod
    def matrix_multiply(mat: List[List[int]], vec: List[int]) -> List[int]:
        return [(mat[0][0]*vec[0] + mat[0][1]*vec[1]) % 26,
                (mat[1][0]*vec[0] + mat[1][1]*vec[1]) % 26]

    @staticmethod
    def encrypt(text: str, key_matrix: List[List[int]]) -> str:
        text = ''.join(ch.lower() for ch in text if ch.isalpha())
        if len(text) % 2 != 0:
            text += 'x'
        result = []
        for i in range(0, len(text), 2):
            pair = [ord(text[i]) - 97, ord(text[i+1]) - 97]
            encrypted_pair = HillCipher.matrix_multiply(key_matrix, pair)
            result.append(chr(encrypted_pair[0] + 97))
            result.append(chr(encrypted_pair[1] + 97))
        return ''.join(result).upper()

    @staticmethod
    def decrypt(ciphertext: str, key_matrix: List[List[int]]) -> Optional[str]:
        # Find determinant
        det = (key_matrix[0][0]*key_matrix[1][1] - key_matrix[0][1]*key_matrix[1][0]) % 26
        det_inv = HillCipher.mod_inv(det, 26)
        if det_inv is None:
            return None  # no inverse, can't decrypt

        # Compute inverse matrix mod 26
        inv_matrix = [
            [(key_matrix[1][1]*det_inv) % 26, (-key_matrix[0][1]*det_inv) % 26],
            [(-key_matrix[1][0]*det_inv) % 26, (key_matrix[0][0]*det_inv) % 26]
        ]

        ciphertext = ciphertext.lower()
        result = []
        for i in range(0, len(ciphertext), 2):
            pair = [ord(ciphertext[i]) - 97, ord(ciphertext[i+1]) - 97]
            decrypted_pair = HillCipher.matrix_multiply(inv_matrix, pair)
            result.append(chr(decrypted_pair[0] + 97))
            result.append(chr(decrypted_pair[1] + 97))
        return ''.join(result)

# --- Rail Fence Cipher ---
class RailFenceCipher:
    @staticmethod
    def encrypt(text: str, rails: int) -> str:
        if rails <= 1:
            return text
        fence = [''] * rails
        rail = 0
        var = 1
        for ch in text:
            fence[rail] += ch
            rail += var
            if rail == 0 or rail == rails - 1:
                var = -var
        return ''.join(fence)

    @staticmethod
    def decrypt(ciphertext: str, rails: int) -> str:
        if rails <= 1:
            return ciphertext
        # Create empty matrix to mark places
        pattern = [['\n'] * len(ciphertext) for _ in range(rails)]
        rail = 0
        var = 1
        for i in range(len(ciphertext)):
            pattern[rail][i] = '*'
            rail += var
            if rail == 0 or rail == rails - 1:
                var = -var

        # Fill matrix with ciphertext chars
        index = 0
        for r in range(rails):
            for c in range(len(ciphertext)):
                if pattern[r][c] == '*' and index < len(ciphertext):
                    pattern[r][c] = ciphertext[index]
                    index += 1

        # Read matrix in zigzag to reconstruct plaintext
        result = []
        rail = 0
        var = 1
        for i in range(len(ciphertext)):
            result.append(pattern[rail][i])
            rail += var
            if rail == 0 or rail == rails - 1:
                var = -var
        return ''.join(result)

# --- Columnar Transposition Cipher ---
class ColumnarTranspositionCipher:
    @staticmethod
    def get_order(key: str) -> List[int]:
        key_lower = key.lower()
        order = sorted([(char, i) for i, char in enumerate(key_lower)])
        return [pos for char, pos in order]

    @staticmethod
    def encrypt(text: str, key: str) -> str:
        key_len = len(key)
        order = ColumnarTranspositionCipher.get_order(key)
        text = text.replace(" ", "")  # remove spaces
        # Pad text to fit matrix
        pad_length = (key_len - len(text) % key_len) % key_len
        text += 'X' * pad_length

        # Create matrix row-wise
        matrix = [list(text[i:i+key_len]) for i in range(0, len(text), key_len)]

        # Read columns by order
        result = []
        for col in order:
            for row in matrix:
                result.append(row[col])
        return ''.join(result)

    @staticmethod
    def decrypt(ciphertext: str, key: str) -> str:
        key_len = len(key)
        order = ColumnarTranspositionCipher.get_order(key)
        col_len = len(ciphertext) // key_len
        # Create empty columns
        columns = [''] * key_len
        start = 0
        # Fill columns based on order
        cols = [''] * key_len
        for i, col_idx in enumerate(order):
            cols[col_idx] = ciphertext[start:start+col_len]
            start += col_len
        # Read row-wise from columns
        result = []
        for i in range(col_len):
            for col in cols:
                result.append(col[i])
        return ''.join(result).rstrip('X')

# --- User interface ---
def get_int_input(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                print(f"❌ Enter a number between {min_val} and {max_val}.")
                continue
            return value
        except ValueError:
            print("❌ Invalid input. Please enter an integer.")

def main():
    print("=== Multi Cipher Toolkit By DevKay ===")
    while True:
        print("\nSelect cipher method:")
        print("1. Caesar Cipher")
        print("2. Monoalphabetic Substitution (Keyword Cipher)")
        print("3. Homophonic Substitution (Simplified)")
        print("4. Playfair Cipher")
        print("5. Hill Cipher (2x2 matrix)")
        print("6. Rail Fence Cipher")
        print("7. Columnar Transposition Cipher")
        print("0. Exit")

        choice = input("Enter choice: ").strip()
        if choice == '0':
            print("Goodbye!")
            break

        if choice == '1':
            mode = input("Encrypt or Decrypt? (e/d): ").lower()
            text = input("Enter text: ")
            shift = get_int_input("Enter shift (e.g., 3): ")
            preserve_case = input("Preserve case? (y/n): ").lower() == 'y'
            if mode == 'e':
                out = CaesarCipher.encrypt(text, shift, preserve_case)
            else:
                out = CaesarCipher.decrypt(text, shift, preserve_case)
            print("Output:", out)

        elif choice == '2':
            mode = input("Encrypt or Decrypt? (e/d): ").lower()
            text = input("Enter text: ")
            keyword = input("Enter keyword (letters only): ").lower()
            if not keyword.isalpha():
                print("❌ Keyword must be alphabetic letters only.")
                continue
            if mode == 'e':
                out = MonoalphabeticCipher.encrypt(text, keyword)
            else:
                out = MonoalphabeticCipher.decrypt(text, keyword)
            print("Output:", out)

        elif choice == '3':
            mode = input("Encrypt or Decrypt? (e/d): ").lower()
            if mode == 'e':
                text = input("Enter text: ")
                out = HomophonicCipher.encrypt(text)
            else:
                cipher_text = input("Enter ciphertext (space-separated codes): ")
                out = HomophonicCipher.decrypt(cipher_text)
            print("Output:", out)

        elif choice == '4':
            mode = input("Encrypt or Decrypt? (e/d): ").lower()
            text = input("Enter text: ")
            keyword = input("Enter keyword (letters only): ").lower()
            if not keyword.isalpha():
                print("❌ Keyword must be alphabetic letters only.")
                continue
            if mode == 'e':
                out = PlayfairCipher.encrypt(text, keyword)
            else:
                out = PlayfairCipher.decrypt(text, keyword)
            print("Output:", out)

        elif choice == '5':
            mode = input("Encrypt or Decrypt? (e/d): ").lower()
            text = input("Enter text (letters only): ").lower()
            if any(ch not in string.ascii_lowercase for ch in text):
                print("❌ Text must contain only letters a-z.")
                continue
            if len(text) % 2 != 0:
                text += 'x'  # pad
            print("Enter 2x2 key matrix elements (numbers 0-25):")
            try:
                a = get_int_input("a (row1 col1): ", 0, 25)
                b = get_int_input("b (row1 col2): ", 0, 25)
                c = get_int_input("c (row2 col1): ", 0, 25)
                d = get_int_input("d (row2 col2): ", 0, 25)
                key_matrix = [[a,b],[c,d]]
            except Exception as e:
                print("Invalid key matrix input.", e)
                continue

            if mode == 'e':
                out = HillCipher.encrypt(text, key_matrix)
            else:
                out = HillCipher.decrypt(text, key_matrix)
                if out is None:
                    print("❌ Key matrix is not invertible modulo 26, can't decrypt.")
                    continue
            print("Output:", out)

        elif choice == '6':
            mode = input("Encrypt or Decrypt? (e/d): ").lower()
            text = input("Enter text: ")
            rails = get_int_input("Enter number of rails (>=2): ", 2)
            if mode == 'e':
                out = RailFenceCipher.encrypt(text, rails)
            else:
                out = RailFenceCipher.decrypt(text, rails)
            print("Output:", out)

        elif choice == '7':
            mode = input("Encrypt or Decrypt? (e/d): ").lower()
            text = input("Enter text: ")
            key = input("Enter key (letters only): ").lower()
            if not key.isalpha():
                print("❌ Key must be alphabetic letters only.")
                continue
            if mode == 'e':
                out = ColumnarTranspositionCipher.encrypt(text, key)
            else:
                out = ColumnarTranspositionCipher.decrypt(text, key)
            print("Output:", out)

        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()
