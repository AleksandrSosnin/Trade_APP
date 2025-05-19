# 📊 Объяснение функций расчёта: Плечо и Риск/Прибыль

## 🔹 Функция `calc_leverage()`: Расчёт кредитного плеча

Переменная	Значение
1. balance - Баланс трейдера в USDT
2. risk_percent	- Риск на сделку в % (например, 0.5%)
3. stop_percent	- Размер стоп-лосса в % от входа
4. max_leverage	 - Максимально допустимое плечо

🧮 Формулы:
    Максимально допустимый риск:
    risk_amount = balance * risk_percent

    Объём входа:
    position_size = risk_amount / stop_percent

    Требуемое плечо:
    required_leverage = position_size / balance

    Рекомендованное плечо (округляется):
    suggested_leverage = min(max_leverage, max(1, round(required_leverage + 0.5)))

# 📊 Функция calc_profit_risk(): Расчёт риска, прибыли и их соотношения


1. balance	Баланс трейдера
2. risk_percent	Риск на сделку в %
3. entry_price	Цена входа
4. stop_loss	Уровень стоп-лосса
5. take_profit	Цель по прибыли (тейк-профит)

🧮 Формулы:
    Сумма риска:
    risk_amount = balance * risk_percent

    Разница между входом и стопом:
    price_diff_stop = abs(entry_price - stop_loss)

    Объём позиции (в единицах актива):
    position_size = risk_amount / price_diff_stop

    Прибыль на одну единицу:
    profit_per_unit = abs(take_profit - entry_price)

    Потенциальная прибыль:
    potential_profit = position_size * profit_per_unit

    Соотношение риск/прибыль:
    risk_reward = potential_profit / risk_amount