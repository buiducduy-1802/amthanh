import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from geopy.distance import geodesic
import math

class VoiceGPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tính Khoảng Cách GPS và Góc Bắn Pháo")
        self.root.geometry("500x500")
        
        self.label_info = tk.Label(root, text="Nhấn nút và nói tọa độ (vĩ độ, kinh độ)")
        self.label_info.pack(pady=10)
        
        self.button_listen1 = tk.Button(root, text="🎤 Nhập Tọa Độ 1", command=lambda: self.recognize_speech(1))
        self.button_listen1.pack(pady=5)
        self.coord1_var = tk.StringVar()
        self.entry_coord1 = tk.Entry(root, textvariable=self.coord1_var, font=("Arial", 12))
        self.entry_coord1.pack(pady=5)
        
        self.button_listen2 = tk.Button(root, text="🎤 Nhập Tọa Độ 2", command=lambda: self.recognize_speech(2))
        self.button_listen2.pack(pady=5)
        self.coord2_var = tk.StringVar()
        self.entry_coord2 = tk.Entry(root, textvariable=self.coord2_var, font=("Arial", 12))
        self.entry_coord2.pack(pady=5)
        
        self.button_calculate = tk.Button(root, text="📏 Tính Khoảng Cách và Góc Bắn", command=self.calculate_distance_and_angle)
        self.button_calculate.pack(pady=10)
        
        self.result_var = tk.StringVar()
        self.label_result = tk.Label(root, textvariable=self.result_var, font=("Arial", 14, "bold"))
        self.label_result.pack(pady=10)
        
    def recognize_speech(self, point):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                self.result_var.set("⏳ Đang nghe...")
                self.root.update()
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language="vi-VN")
                self.result_var.set("✅ Nhận diện thành công!")
                
                text = text.replace("phẩy", ",")  # Chuyển "phẩy" thành dấu phẩy
                if point == 1:
                    self.coord1_var.set(text)
                else:
                    self.coord2_var.set(text)
            except sr.UnknownValueError:
                self.result_var.set("❌ Không nhận diện được!")
            except sr.RequestError:
                self.result_var.set("❌ Lỗi kết nối!")
    
    def calculate_distance_and_angle(self):
        try:
            coord1 = tuple(map(float, self.coord1_var.get().split(",")))
            coord2 = tuple(map(float, self.coord2_var.get().split(",")))
            
            # Tính khoảng cách giữa hai tọa độ
            distance = geodesic(coord1, coord2).kilometers * 1000  # Đổi từ km sang m
            
            # Tốc độ ban đầu của đạn pháo (giả sử 500 m/s)
            velocity = 500  # m/s
            
            # Gia tốc trọng trường
            g = 9.81  # m/s²
            
            # Tính góc bắn
            sin_2theta = (g * distance) / (velocity ** 2)
            if sin_2theta > 1 or sin_2theta < -1:
                self.result_var.set("❌ Góc bắn không khả thi!")
                return
            
            angle = math.degrees(0.5 * math.asin(sin_2theta))  # Tính góc và chuyển đổi sang độ
            
            # Hiển thị kết quả
            self.result_var.set(f"Khoảng cách: {distance:.2f} m\nGóc bắn cần thiết: {angle:.2f} độ")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceGPSApp(root)
    root.mainloop()
