import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("520x620")
app.title("📈 Калькулятор риска и прибыли")

tabview = ctk.CTkTabview(app, width=500, height=590)
tabview.pack(padx=10, pady=10)

tab1 = tabview.add("⚙️ Расчёт плеча")
tab2 = tabview.add("📊 Risk / Profit")

# ========== TAB 1: Расчёт плеча ==========
def calc_leverage():
    try:
        balance = float(balance_entry.get())
        risk_percent = float(risk_percent_entry.get()) / 100
        stop_percent = float(stop_percent_entry.get()) / 100
        max_leverage = float(max_leverage_entry.get())

        risk_amount = balance * risk_percent
        position_size = risk_amount / stop_percent
        required_leverage = position_size / balance if balance != 0 else 0
        suggested_leverage = min(max_leverage, max(1, round(required_leverage + 0.5)))

        color = "green" if required_leverage <= max_leverage else "red"

        result1.configure(
            text=(
                f"💰 Баланс: ${balance:.2f}\n"
                f"⚠️ Риск: {risk_percent * 100:.2f}% → ${risk_amount:.2f}\n"
                f"🛑 Стоп: {stop_percent * 100:.2f}%\n"
                f"📊 Объём входа: ${position_size:.2f}\n"
                f"⚙️ Требуемое плечо: x{required_leverage:.2f}\n"
                f"✅ Рекомендованное плечо: x{suggested_leverage}"
            ),
            text_color=color
        )
    except:
        result1.configure(text="❌ Проверь ввод", text_color="red")

ctk.CTkLabel(tab1, text="💰 Баланс (USDT):").pack(pady=(10, 0))
balance_entry = ctk.CTkEntry(tab1, placeholder_text="Напр. 1000")
balance_entry.pack(pady=5)

ctk.CTkLabel(tab1, text="📉 Риск на сделку (% от баланса):").pack(pady=(10, 0))
risk_percent_entry = ctk.CTkEntry(tab1, placeholder_text="Напр. 1")
risk_percent_entry.pack(pady=5)

ctk.CTkLabel(tab1, text="🛑 Стоп (% от входа):").pack(pady=(10, 0))
stop_percent_entry = ctk.CTkEntry(tab1, placeholder_text="Напр. 1.18")
stop_percent_entry.pack(pady=5)

ctk.CTkLabel(tab1, text="📈 Максимальное плечо:").pack(pady=(10, 0))
max_leverage_entry = ctk.CTkEntry(tab1, placeholder_text="Напр. 25")
max_leverage_entry.pack(pady=5)

ctk.CTkButton(tab1, text="📊 Рассчитать", command=calc_leverage).pack(pady=10)
result1 = ctk.CTkLabel(tab1, text="", wraplength=480, justify="left")
result1.pack(pady=10)

# ========== TAB 2: Risk / Profit ==========
def calc_profit_risk():
    try:
        balance = float(balance_entry2.get())
        risk_percent = float(risk_percent_entry2.get()) / 100
        entry_price = float(entry_price_entry.get())
        stop_loss = float(stop_loss_entry.get())
        take_profit = float(take_profit_entry.get())

        risk_amount = balance * risk_percent
        price_diff_stop = abs(entry_price - stop_loss)
        position_size = risk_amount / price_diff_stop

        profit_per_unit = abs(take_profit - entry_price)
        potential_profit = position_size * profit_per_unit

        risk_reward = potential_profit / risk_amount if risk_amount != 0 else 0

        if risk_reward >= 4:
            color = "green"
        elif risk_reward >= 2:
            color = "orange"
        else:
            color = "red"

        result2.configure(
            text=(
                f"💰 Риск: ${risk_amount:.2f}\n"
                f"📉 Объём позиции: {position_size:.4f} USDT\n"
                f"📈 Потенциальная прибыль: ${potential_profit:.2f}\n"
                f"⚖️ Соотношение риск/прибыль: {risk_reward:.2f}x"
            ),
            text_color=color
        )
    except:
        result2.configure(text="❌ Ошибка ввода", text_color="red")

ctk.CTkLabel(tab2, text="💰 Баланс (USDT):").pack(pady=(10, 0))
balance_entry2 = ctk.CTkEntry(tab2, placeholder_text="Напр. 5000")
balance_entry2.pack(pady=5)

ctk.CTkLabel(tab2, text="📉 Риск на сделку (%):").pack(pady=(10, 0))
risk_percent_entry2 = ctk.CTkEntry(tab2, placeholder_text="Напр. 0.5")
risk_percent_entry2.pack(pady=5)

ctk.CTkLabel(tab2, text="🚪 Цена входа:").pack(pady=(10, 0))
entry_price_entry = ctk.CTkEntry(tab2, placeholder_text="Напр. 95000")
entry_price_entry.pack(pady=5)

ctk.CTkLabel(tab2, text="🛑 Стоп-лосс (цена):").pack(pady=(10, 0))
stop_loss_entry = ctk.CTkEntry(tab2, placeholder_text="Напр. 92150")
stop_loss_entry.pack(pady=5)

ctk.CTkLabel(tab2, text="🎯 Тейк-профит (цена):").pack(pady=(10, 0))
take_profit_entry = ctk.CTkEntry(tab2, placeholder_text="Напр. 108000")
take_profit_entry.pack(pady=5)

ctk.CTkButton(tab2, text="📈 Рассчитать", command=calc_profit_risk).pack(pady=10)
result2 = ctk.CTkLabel(tab2, text="", wraplength=480, justify="left")
result2.pack(pady=10)

app.mainloop()
