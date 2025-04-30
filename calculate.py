import math
import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, getcontext, localcontext, ROUND_FLOOR

# Устанавливаем высокую точность для вычислений
getcontext().prec = 28


def optimal_calc_prices(input_price: Decimal, proc_nds: int) -> (Decimal, Decimal):
    """
    Оптимальное решение:
      - Вычисляем g = gcd(100, 100 + proc_nds)
      - Определяем минимальный шаг дискретизации: d = 100 // g
      - Все допустимые значения цены без НДС имеют вид: (m * d) / 100,
        где m – целое число.
      - Цена с НДС равна: (m * d * (100 + proc_nds)) / 10000.

    Вычисляем вещественное m_ideal и затем выбираем двух кандидатов:
      m_floor = floor(m_ideal) и m_ceil = m_floor + 1,
    возвращая тот, для которого абсолютная разница:
         |CalculatedPriceWithNDS - InputPriceWithNDS|
    минимальна. Результаты возвращаются с ровно 2 знаками после запятой.
    """
    # Вычисляем НОД для 100 и (100 + proc_nds)
    g = math.gcd(100, 100 + proc_nds)
    # Минимальный шаг дискретизации
    d = 100 // g

    with localcontext() as ctx:
        ctx.prec = 28
        # Идеальное (вещественное) значение m:
        m_ideal = input_price * Decimal(10000) / Decimal(d * (100 + proc_nds))
        m_floor = int(m_ideal.to_integral_value(rounding=ROUND_FLOOR))
        m_ceil = m_floor + 1

        def candidate(m: int):
            cp_with = (Decimal(m * d * (100 + proc_nds)) / Decimal(10000)).quantize(
                Decimal("0.01")
            )
            cp_without = (Decimal(m * d) / Decimal(100)).quantize(Decimal("0.01"))
            return cp_with, cp_without

        cand_floor = candidate(m_floor)
        cand_ceil = candidate(m_ceil)

        err_floor = abs(cand_floor[0] - input_price)
        err_ceil = abs(cand_ceil[0] - input_price)

        if err_floor <= err_ceil:
            return cand_floor
        else:
            return cand_ceil


class PriceCalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Калькулятор цены с НДС и без НДС")

        # Метка и поле ввода для рекомендованной цены с НДС
        self.label_price = tk.Label(master, text="Рекомендуемая цена с НДС:")
        self.label_price.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.entry_price = tk.Entry(master, width=30)
        self.entry_price.grid(row=0, column=1, padx=10, pady=5)

        # Метка и поле ввода для процента НДС
        self.label_proc = tk.Label(master, text="Процент НДС (0–99):")
        self.label_proc.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entry_proc = tk.Entry(master, width=30)
        self.entry_proc.grid(row=1, column=1, padx=10, pady=5)

        # Кнопка для расчета
        self.calc_button = tk.Button(
            master, text="Рассчитать цены", command=self.calculate
        )
        self.calc_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Метки для отображения результатов
        self.label_result_with = tk.Label(master, text="Рассчитанная цена с НДС:")
        self.label_result_with.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.result_with = tk.Label(master, text="", fg="blue")
        self.result_with.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.label_result_without = tk.Label(master, text="Рассчитанная цена без НДС:")
        self.label_result_without.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.result_without = tk.Label(master, text="", fg="blue")
        self.result_without.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    def calculate(self):
        # Считывание данных с полей ввода
        price_str = self.entry_price.get().strip()
        proc_str = self.entry_proc.get().strip()

        try:
            input_price = Decimal(price_str)
        except Exception as e:
            messagebox.showerror("Ошибка ввода", f"Неверное значение цены с НДС:\n{e}")
            return

        try:
            proc_nds = int(proc_str)
            if proc_nds < 0 or proc_nds > 99:
                raise ValueError("Процент НДС должен быть от 0 до 99.")
        except Exception as e:
            messagebox.showerror(
                "Ошибка ввода", f"Неверное значение процента НДС:\n{e}"
            )
            return

        try:
            cp_with, cp_without = optimal_calc_prices(input_price, proc_nds)
            self.result_with.config(text=str(cp_with))
            self.result_without.config(text=str(cp_without))
        except Exception as e:
            messagebox.showerror("Ошибка вычисления", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PriceCalculatorGUI(root)
    root.mainloop()
