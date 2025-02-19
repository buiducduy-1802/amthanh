import sys
import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from sympy import sympify
from decimal import Decimal

# Cấu hình UTF-8 để hỗ trợ tiếng Việt & tiếng Nga
sys.stdout.reconfigure(encoding='utf-8')

# Bảng chuyển đổi từ tiếng Việt và tiếng Nga sang ký hiệu toán học
TRANSLATION_DICT = {
    "cộng": "+", "trừ": "-", "nhân": "*", "chia": "/", "mũ": "**", "bằng": "=",
    "плюс": "+", "минус": "-", "умножить": "*", "разделить": "/", "степени": "**", "равно": "=",
    "x": "*",  # Thêm vào để chuyển "x" thành dấu nhân *
}

class VoiceCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Máy tính nhận diện giọng nói")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Nhãn chọn ngôn ngữ
        self.label_lang = tk.Label(root, text="Chọn ngôn ngữ:")
        self.label_lang.pack(pady=5)

        # Dropdown chọn ngôn ngữ
        self.lang_var = tk.StringVar(value="vi-VN")
        self.lang_menu = ttk.Combobox(root, textvariable=self.lang_var, values=["vi-VN", "ru-RU"])
        self.lang_menu.pack(pady=5)

        # Nút nhận diện giọng nói
        self.button_listen = tk.Button(root, text="🎤 Nhấn để nói", command=self.recognize_speech)
        self.button_listen.pack(pady=10)

        # Nhãn hiển thị phép tính
        self.label_expression = tk.Label(root, text="Biểu thức:", font=("Arial", 12))
        self.label_expression.pack(pady=5)

        # Ô hiển thị biểu thức toán học
        self.expression_var = tk.StringVar()
        self.entry_expression = tk.Entry(root, textvariable=self.expression_var, font=("Arial", 14), justify="center")
        self.entry_expression.pack(pady=5, padx=20, fill="x")

        # Nhãn kết quả
        self.label_result = tk.Label(root, text="Kết quả:", font=("Arial", 12))
        self.label_result.pack(pady=5)

        # Ô hiển thị kết quả
        self.result_var = tk.StringVar()
        self.entry_result = tk.Entry(root, textvariable=self.result_var, font=("Arial", 14), justify="center", state="readonly")
        self.entry_result.pack(pady=5, padx=20, fill="x")

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.result_var.set("⏳ Đang lắng nghe...")
            self.root.update()
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Thiết lập thời gian nghe tối đa cho mỗi câu
                language = self.lang_var.get()
                text = recognizer.recognize_google(audio, language=language).strip().lower()
                self.expression_var.set(self.convert_to_math(text))

                # Tự động tính toán sau khi nghe xong
                expression = self.expression_var.get()
                if expression:
                    result = self.calculate(expression)
                    self.result_var.set(self.format_result(result))

            except sr.UnknownValueError:
                self.result_var.set("❌ Không nhận diện được!")
            except sr.RequestError:
                self.result_var.set("❌ Lỗi kết nối!")

    def convert_to_math(self, expression):
        words = expression.split()
        return " ".join([TRANSLATION_DICT.get(word, word) for word in words])

    def calculate(self, expression):
        try:
            return sympify(expression).evalf()
        except Exception as e:
            return f"❌ Lỗi: {e}"

    def format_result(self, result):
        # Sử dụng Decimal để xử lý kết quả và loại bỏ số 0 thừa
        decimal_result = Decimal(str(result))
        if decimal_result == decimal_result.to_integral_value():
            return str(int(decimal_result))  # Chuyển thành kiểu int nếu là số nguyên
        else:
            return str(decimal_result)  # Nếu có phần thập phân thì giữ nguyên

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceCalculatorApp(root)
    root.mainloop()
