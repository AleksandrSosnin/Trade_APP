import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab
import os
import datetime
import re
import telegram

# Удаляем недопустимые символы из имени файла
def sanitize_filename(name):
    return re.sub(r'[\\/:"*?<>|]+', '_', name)

class TradingJournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Journal")
        self.root.geometry("800x700")
        self.root.configure(bg="black")
        self.setup_ui()

    def setup_ui(self):
        style = {
            "bg": "black",
            "fg": "white",
            "highlight": "#33ccff",
            "entry_bg": "#1e1e1e",
            "entry_fg": "white"
        }

        self.entries = {}

        # Главный фрейм
        main_frame = tk.Frame(self.root, bg=style["bg"])
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Заголовок
        tk.Label(main_frame, text="Журнал сделок", bg=style["bg"], fg="white",
                 font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        # Универсальная функция для создания поля ввода
        def create_entry(label, row, is_dropdown=False, options=None):
            tk.Label(main_frame, text=label + ":", bg=style["bg"], fg=style["highlight"],
                     font=("Helvetica", 10, "bold")).grid(row=row, column=0, sticky="e", pady=4, padx=5)
            if is_dropdown and options:
                var = tk.StringVar()
                dropdown = ttk.Combobox(main_frame, textvariable=var, values=options, state="readonly")
                dropdown.grid(row=row, column=1, sticky="ew", padx=5)
                self.entries[label] = var
            else:
                entry = tk.Entry(main_frame, bg=style["entry_bg"], fg=style["entry_fg"])
                entry.grid(row=row, column=1, sticky="ew", padx=5)
                self.entries[label] = entry

        row = 1  # начальная строка

        # Простые текстовые поля
        fields_plain = ["Название монеты", "Дата", "Вход", "Выход", "Стоп", "Тейк",
                        "Частичная/полная прибыль или убыток"]

        for field in fields_plain:
            create_entry(field, row)
            row += 1

        # Выпадающие списки
        fields_dropdown = {
            "Лонг/шорт": ["Лонг", "Шорт"],
            "Риск/прибыль": [f"1/{i}" for i in range(2, 11)],
            "Таймфрейм": ["5м", "15м", "30м", "1ч", "4ч", "1д"],
            "Вход по рынку/по лимитке": ["по рынку", "по лимитке"],
            "Плечо": [str(i) for i in range(1, 51)]
        }

        for field, options in fields_dropdown.items():
            create_entry(field, row, is_dropdown=True, options=options)
            row += 1

        # Отбор инструмента (чекбоксы)
        tk.Label(main_frame, text="Отбор инструмента (мин. 1):", bg=style["bg"], fg=style["highlight"],
                 font=("Helvetica", 10, "bold")).grid(row=row, column=0, sticky="nw", pady=5)
        self.instrument_checks = {}
        instruments = [
            "Монета на объемах", "Интенсивный тренд с вертикальным ускорением",
            "Монета в топе по количеству сделок", "Недавний листинг"
        ]
        instr_frame = tk.Frame(main_frame, bg=style["bg"])
        instr_frame.grid(row=row, column=1, sticky="w")
        for i, item in enumerate(instruments):
            var = tk.IntVar()
            chk = tk.Checkbutton(instr_frame, text=item, variable=var, bg=style["bg"], fg=style["fg"],
                                 selectcolor="gray", activebackground=style["bg"], activeforeground=style["highlight"])
            chk.grid(row=i, sticky="w")
            self.instrument_checks[item] = var
        row += 1

        # Критерии сетапа (чекбоксы)
        tk.Label(main_frame, text="Критерии сетапа (мин. 3):", bg=style["bg"], fg=style["highlight"],
                 font=("Helvetica", 10, "bold")).grid(row=row, column=0, sticky="nw", pady=5)
        self.criteria_checks = {}
        criteria = [
            "Движение по тренду", "3 касания уровня",
            "Уровень наторгован", "Основа уровня экстремум"
        ]
        crit_frame = tk.Frame(main_frame, bg=style["bg"])
        crit_frame.grid(row=row, column=1, sticky="w")
        for i, item in enumerate(criteria):
            var = tk.IntVar()
            chk = tk.Checkbutton(crit_frame, text=item, variable=var, bg=style["bg"], fg=style["fg"],
                                 selectcolor="gray", activebackground=style["bg"], activeforeground=style["highlight"])
            chk.grid(row=i, sticky="w")
            self.criteria_checks[item] = var
        row += 1

        # Комментарий
        tk.Label(main_frame, text="Комментарий:", bg=style["bg"], fg=style["highlight"],
                 font=("Helvetica", 10, "bold")).grid(row=row, column=0, sticky="ne", pady=5)
        self.comment = tk.Text(main_frame, height=4, bg=style["entry_bg"], fg=style["entry_fg"], wrap="word")
        self.comment.grid(row=row, column=1, sticky="ew", padx=5)
        row += 1

        # Кнопка сохранения
        save_btn = tk.Button(main_frame, text="Сохранить как изображение", bg=style["highlight"],
                             fg="black", font=("Helvetica", 11, "bold"), command=self.save_as_image)
        save_btn.grid(row=row, column=0, columnspan=2, pady=15)

        # Кнопка отправки в Telegram
        tg_btn = tk.Button(main_frame, text="Отправить в Telegram", bg="#77dd77",
                           fg="black", font=("Helvetica", 11, "bold"), command=self.send_to_telegram)
        tg_btn.grid(row=row + 1, column=0, columnspan=2, pady=5)

        # Автоматическое растяжение второго столбца
        main_frame.grid_columnconfigure(1, weight=1)

    # Метод для сохранения в изображение
    def save_as_image(self):
        x1 = self.root.winfo_rootx()
        y1 = self.root.winfo_rooty()
        x2 = x1 + self.root.winfo_width()
        y2 = y1 + self.root.winfo_height()

        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"trading_journal_{timestamp}.png"
        screenshot.save(filename)
        print(f"Сохранено как {filename}")

    def send_to_telegram(self):
        token = "7908473226:AAHyuBDItexsDtaLc_xbVrv3FefOoAD5O4E"
        chat_id = "218615700"  # заменишь позже

        bot = telegram.Bot(token=token)

        # Сбор всех полей
        info = []
        for key, widget in self.entries.items():
            value = widget.get() if isinstance(widget, tk.Entry) else widget.get()  # Для Text и Combobox
            info.append(f"#{key.replace(' ', '_')} {value}")

        for key, var in self.instrument_checks.items():
            if var.get():
                info.append(f"#Отбор {key.replace(' ', '_')}")

        for key, var in self.criteria_checks.items():
            if var.get():
                info.append(f"#Критерий {key.replace(' ', '_')}")

        comment = self.comment.get("1.0", tk.END).strip()
        if comment:
            info.append(f"#Комментарий: {comment}")

        message = "\n".join(info)

        # Отправка в Telegram
        try:
            bot.send_message(chat_id=chat_id, text=message)
            print("Отправлено в Telegram.")
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingJournalApp(root)
    root.mainloop()
