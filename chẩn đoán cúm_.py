import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import os


class FluDiagnosisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Chẩn Đoán Cảm Cúm AI")
        self.root.geometry("950x750")
        self.root.configure(bg='#f0f8ff')
        self.center_window()

        self.model = self.train_model()
        self.temp_var = StringVar(value="37.0")
        self.headache_var = IntVar(value=0)
        self.cough_var = IntVar(value=0)
        self.fatigue_var = IntVar(value=0)
        self.sore_throat_var = IntVar(value=0)
        self.runny_nose_var = IntVar(value=0)
        self.create_widgets()

    def center_window(self):
        self.root.update_idletasks()
        width = 950
        height = 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def convert_temp(self, x):
        try:
            if str(x).strip() == "<36":
                return 35.9
            elif str(x).strip() == ">40":
                return 40.1
            else:
                return float(x)
        except:
            return 37.0  # Giá trị mặc định nếu có lỗi

    def train_model(self):
        try:
            file_path = r"D:\UEH Kỳ 3\Trí tuệ nhân tạo\du_doan_cum_0.1.xlsx"
            data = pd.read_excel(file_path)
            required_columns = ['Nhiet_do', 'Dau_dau', 'Ho', 'Met_moi', 'Dau_hong', 'So_muoi', 'Cum']
            missing_columns = [col for col in required_columns if col not in data.columns]

            if missing_columns:
                messagebox.showwarning("Cảnh báo",
                                       f"File thiếu các cột: {', '.join(missing_columns)}\nSử dụng dữ liệu mẫu để huấn luyện.")
                return self.create_sample_model()

            data["Nhiet_do"] = data["Nhiet_do"].apply(self.convert_temp)

            X = []
            y = []

            # Xử lý dữ liệu từ file Excel
            for _, row in data.iterrows():
                a = 1 if row["Nhiet_do"] >= 38 else 0  # Sốt (≥38°C)
                b = int(row["Dau_dau"])  # Đau đầu
                c = int(row["Ho"])  # Ho
                d = int(row["Met_moi"])  # Mệt mỏi
                e = int(row["Dau_hong"])  # Đau họng
                g = int(row["So_muoi"])  # Sổ mũi
                X.append([a, b, c, d, e, g])
                y.append(int(row["Cum"]))

            X = np.array(X)
            y = np.array(y)

            # Huấn luyện mô hình Perceptron
            model = Perceptron(max_iter=1000, eta0=0.1, random_state=42)
            model.fit(X, y)
            return model

        except Exception as e:
            messagebox.showwarning("Cảnh báo",
                                   f"Không thể đọc file dữ liệu:\n{str(e)}\nSử dụng dữ liệu mẫu để huấn luyện.")
            return self.create_sample_model()

    def create_sample_model(self):
        # Tạo dữ liệu mẫu để huấn luyện
        np.random.seed(42)
        X = []
        y = []

        for _ in range(140):
            fever = np.random.choice([0, 1], p=[0.3, 0.7])
            headache = np.random.choice([0, 1], p=[0.2, 0.8])
            cough = np.random.choice([0, 1], p=[0.15, 0.85])
            fatigue = np.random.choice([0, 1], p=[0.1, 0.9])
            sore_throat = np.random.choice([0, 1], p=[0.25, 0.75])
            runny_nose = np.random.choice([0, 1], p=[0.3, 0.7])
            X.append([fever, headache, cough, fatigue, sore_throat, runny_nose])
            y.append(1)
        for _ in range(60):
            fever = np.random.choice([0, 1], p=[0.9, 0.1])
            headache = np.random.choice([0, 1], p=[0.7, 0.3])
            cough = np.random.choice([0, 1], p=[0.8, 0.2])
            fatigue = np.random.choice([0, 1], p=[0.6, 0.4])
            sore_throat = np.random.choice([0, 1], p=[0.75, 0.25])
            runny_nose = np.random.choice([0, 1], p=[0.7, 0.3])
            X.append([fever, headache, cough, fatigue, sore_throat, runny_nose])
            y.append(0)

        X = np.array(X)
        y = np.array(y)

        model = Perceptron(max_iter=1000, eta0=0.1, random_state=42)
        model.fit(X, y)

        return model

    def create_widgets(self):
        main_frame = Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        title_frame = Frame(main_frame, bg='#f0f8ff')
        title_frame.pack(fill=X, pady=(0, 20))
        title_font = tkFont.Font(family="Arial", size=28, weight="bold")
        title = Label(title_frame, text="🏥 HỆ THỐNG CHẨN ĐOÁN CẢM CÚM AI", font=title_font, fg='#2c3e50', bg='#f0f8ff')
        title.pack()

        content_frame = Frame(main_frame, bg='#f0f8ff')
        content_frame.pack(fill=BOTH, expand=True)

        left_frame = Frame(content_frame, bg='white', relief=RAISED, borderwidth=2)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

        form_title = Label(left_frame, text="📋 THÔNG TIN TRIỆU CHỨNG", font=("Arial", 16, "bold"), bg='white',
                           fg='#34495e')
        form_title.pack(pady=15)
        self.create_temperature_input(left_frame)

        symptoms_frame = Frame(left_frame, bg='white')
        symptoms_frame.pack(fill=X, padx=20, pady=10)

        Label(symptoms_frame, text="Các triệu chứng khác:",
              font=("Arial", 12, "bold"), bg='white', fg='#2c3e50').pack(anchor=W, pady=(0, 10))

        self.create_symptom_checkbox(symptoms_frame, "Đau đầu", self.headache_var)
        self.create_symptom_checkbox(symptoms_frame, "Ho", self.cough_var)
        self.create_symptom_checkbox(symptoms_frame, "Mệt mỏi", self.fatigue_var)
        self.create_symptom_checkbox(symptoms_frame, "Đau họng", self.sore_throat_var)
        self.create_symptom_checkbox(symptoms_frame, "Sổ mũi", self.runny_nose_var)

        btn_frame = Frame(left_frame, bg='white')
        btn_frame.pack(pady=20)

        self.diagnose_btn = Button(btn_frame, text="🔍 CHẨN ĐOÁN", command=self.diagnose, font=("Arial", 14, "bold"),
                                   bg='#3498db', fg='white', padx=30, pady=12,
                                   cursor='hand2', relief=RAISED, borderwidth=2)
        self.diagnose_btn.pack()
        self.diagnose_btn.bind('<Enter>', lambda e: self.diagnose_btn.config(bg='#2980b9'))
        self.diagnose_btn.bind('<Leave>', lambda e: self.diagnose_btn.config(bg='#3498db'))

        self.reset_btn = Button(btn_frame, text="🔄 LÀM MỚI",
                                command=self.reset_form,
                                font=("Arial", 12),
                                bg='#95a5a6', fg='white',
                                padx=20, pady=8,
                                cursor='hand2')
        self.reset_btn.pack(pady=10)
        self.reset_btn.bind('<Enter>', lambda e: self.reset_btn.config(bg='#7f8c8d'))
        self.reset_btn.bind('<Leave>', lambda e: self.reset_btn.config(bg='#95a5a6'))

        right_frame = Frame(content_frame, bg='white', relief=RAISED, borderwidth=2)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        result_title = Label(right_frame, text="KẾT QUẢ CHẨN ĐOÁN", font=("Arial", 16, "bold"), bg='white',
                             fg='#34495e')
        result_title.pack(pady=15)

        self.result_frame = Frame(right_frame, bg='white')
        self.result_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.result_label = Label(self.result_frame, text="Vui lòng nhập thông tin triệu chứng\nvà nhấn nút CHẨN ĐOÁN",
                                  font=("Arial", 14), bg='white', fg='#7f8c8d')
        self.result_label.pack(pady=50)

        info_frame = Frame(right_frame, bg='#ecf0f1', relief=SUNKEN, borderwidth=1)
        info_frame.pack(fill=X, padx=20, pady=10)

        info_text = """⚠️ LƯU Ý:
• Đây chỉ là công cụ hỗ trợ sơ bộ
• Không thay thế cho chẩn đoán y tế chuyên nghiệp
• Nếu có triệu chứng nghiêm trọng, hãy đến gặp bác sĩ"""

        Label(info_frame, text=info_text, font=("Arial", 10), bg='#ecf0f1', fg='#34495e', justify=LEFT).pack(padx=10,
                                                                                                             pady=10)
    def create_temperature_input(self, parent):
        temp_frame = Frame(parent, bg='white')
        temp_frame.pack(fill=X, padx=20, pady=10)
        Label(temp_frame, text="🌡️ Nhiệt độ cơ thể (°C):",
              font=("Arial", 12, "bold"), bg='white', fg='#2c3e50').pack(anchor=W)
        scale_frame = Frame(temp_frame, bg='white')
        scale_frame.pack(fill=X, pady=10)
        self.temp_scale = Scale(scale_frame, from_=35.0, to=42.0, orient=HORIZONTAL, resolution=0.1,
                                variable=self.temp_var,
                                length=300, sliderlength=20, bg='white', fg='#2c3e50', troughcolor='#ecf0f1',
                                activebackground='#3498db',
                                highlightthickness=0, command=self.update_temp_display)
        self.temp_scale.pack()
        self.temp_display = Label(temp_frame, text="37.0°C", font=("Arial", 24, "bold"), bg='white',
                                  fg=self.get_temp_color(37.0))
        self.temp_display.pack()
        self.temp_status = Label(temp_frame, text="Nhiệt độ bình thường", font=("Arial", 10), bg='white', fg='#27ae60')
        self.temp_status.pack()

    def create_symptom_checkbox(self, parent, text, variable):
        cb_frame = Frame(parent, bg='white')
        cb_frame.pack(fill=X, pady=5)
        cb = Checkbutton(cb_frame, text=text, variable=variable,
                         font=("Arial", 11), bg='white',
                         activebackground='#ecf0f1',
                         selectcolor='white',
                         cursor='hand2')
        cb.pack(anchor=W)

    def update_temp_display(self, value):
        temp = float(value)
        self.temp_display.config(text=f"{temp}°C", fg=self.get_temp_color(temp))

        if temp < 36.5:
            status = "Nhiệt độ thấp"
            color = '#3498db'
        elif temp < 37.5:
            status = "Nhiệt độ bình thường"
            color = '#27ae60'
        elif temp < 38.0:
            status = "Sốt nhẹ"
            color = '#f39c12'
        elif temp < 39.0:
            status = "Sốt vừa"
            color = '#e67e22'
        else:
            status = "Sốt cao - Cần đến bác sĩ!"
            color = '#e74c3c'

        self.temp_status.config(text=status, fg=color)

    def get_temp_color(self, temp):
        if temp < 36.5:
            return '#3498db'
        elif temp < 37.5:
            return '#27ae60'
        elif temp < 38.0:
            return '#f39c12'
        elif temp < 39.0:
            return '#e67e22'
        else:
            return '#e74c3c'

    def diagnose(self):
        if not hasattr(self, 'model') or self.model is None:
            messagebox.showerror("Lỗi", "Mô hình chưa được huấn luyện!")
            return

        temp_val = float(self.temp_var.get())
        a = 1 if temp_val >= 38 else 0  # Sốt (≥38°C)
        b = self.headache_var.get()  # Đau đầu
        c = self.cough_var.get()  # Ho
        d = self.fatigue_var.get()  # Mệt mỏi
        e = self.sore_throat_var.get()  # Đau họng
        g = self.runny_nose_var.get()  # Sổ mũi
        patient_data = [a, b, c, d, e, g]

        prediction = self.model.predict([patient_data])[0]
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        if prediction == 1:
            self.show_positive_result()
        else:
            self.show_negative_result()
        self.show_symptom_summary(patient_data, temp_val)

    def show_positive_result(self):
        result_icon = Label(self.result_frame, text="⚠️",
                            font=("Arial", 48), bg='white', fg='#e74c3c')
        result_icon.pack(pady=10)
        result_text = Label(self.result_frame, text="KẾT QUẢ: CÓ KHẢ NĂNG BỊ CÚM",
                            font=("Arial", 18, "bold"), bg='white', fg='#e74c3c')
        result_text.pack(pady=5)
        advice_frame = Frame(self.result_frame, bg='#ffe5e5', relief=RIDGE, borderwidth=2)
        advice_frame.pack(fill=X, pady=20)

        advice = """📌 LỜI KHUYÊN:
• Nghỉ ngơi nhiều và uống nhiều nước
• Đeo khẩu trang khi tiếp xúc với người khác
• Theo dõi nhiệt độ thường xuyên
• Nếu triệu chứng nặng hơn, hãy đến gặp bác sĩ
• Tránh đến nơi đông người"""

        Label(advice_frame, text=advice, font=("Arial", 11),
              bg='#ffe5e5', fg='#c0392b', justify=LEFT).pack(padx=15, pady=15)

    def show_negative_result(self):
        result_icon = Label(self.result_frame, text="✅",
                            font=("Arial", 48), bg='white', fg='#27ae60')
        result_icon.pack(pady=10)
        result_text = Label(self.result_frame, text="KẾT QUẢ: KHÔNG CÓ DẤU HIỆU CÚM",
                            font=("Arial", 18, "bold"), bg='white', fg='#27ae60')
        result_text.pack(pady=5)

        advice_frame = Frame(self.result_frame, bg='#e8f8e8', relief=RIDGE, borderwidth=2)
        advice_frame.pack(fill=X, pady=20)
        advice = """📌 LỜI KHUYÊN:
• Tiếp tục duy trì sức khỏe tốt
• Uống đủ nước và ăn uống điều độ
• Tập thể dục thường xuyên
• Giữ vệ sinh cá nhân
• Theo dõi sức khỏe định kỳ"""
        Label(advice_frame, text=advice, font=("Arial", 11),
              bg='#e8f8e8', fg='#27ae60', justify=LEFT).pack(padx=15, pady=15)

    def show_symptom_summary(self, features, actual_temp):
        summary_frame = Frame(self.result_frame, bg='#f8f9fa', relief=GROOVE, borderwidth=1)
        summary_frame.pack(fill=X, pady=10)
        Label(summary_frame, text="📊 Tóm tắt triệu chứng:",
              font=("Arial", 12, "bold"), bg='#f8f9fa', fg='#2c3e50').pack(anchor=W, padx=10, pady=5)

        symptoms = [
            (f"Sốt: {actual_temp}°C", features[0]),
            ("Đau đầu", features[1]),
            ("Ho", features[2]),
            ("Mệt mỏi", features[3]),
            ("Đau họng", features[4]),
            ("Sổ mũi", features[5])
        ]

        for symptom, value in symptoms:
            status = "✓ Có" if value == 1 else "✗ Không"
            color = '#e74c3c' if value == 1 else '#95a5a6'
            Label(summary_frame, text=f"  • {symptom}: {status}",
                  font=("Arial", 10), bg='#f8f9fa', fg=color).pack(anchor=W, padx=20)

        total_symptoms = sum(features)
        Label(summary_frame, text=f"\nTổng số triệu chứng: {total_symptoms}/6",
              font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#34495e').pack(pady=5)

    def reset_form(self):
        self.temp_var.set("37.0")
        self.headache_var.set(0)
        self.cough_var.set(0)
        self.fatigue_var.set(0)
        self.sore_throat_var.set(0)
        self.runny_nose_var.set(0)

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.result_label = Label(self.result_frame, text="Vui lòng nhập thông tin triệu chứng\nvà nhấn nút CHẨN ĐOÁN",
                                  font=("Arial", 14), bg='white', fg='#7f8c8d')
        self.result_label.pack(pady=50)
        self.update_temp_display("37.0")


if __name__ == "__main__":
    root = Tk()
    app = FluDiagnosisApp(root)
    root.mainloop()