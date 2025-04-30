import math
import pytest
from decimal import Decimal
import tkinter as tk
from tkinter import messagebox

# Импортируем тестируемые функции и класс из основного модуля (например, calculate.py)
from calculate import optimal_calc_prices, PriceCalculatorGUI

# Тесты для функции optimal_calc_prices

def test_typical_value():
    """
    При входных данных:
      - input_price: 1.81
      - proc_nds: 20
    ожидается, что:
      - цена с НДС будет 1.80
      - цена без НДС будет 1.50
    """
    cp_with, cp_without = optimal_calc_prices(Decimal("1.81"), 20)
    assert cp_with == Decimal("1.80")
    assert cp_without == Decimal("1.50")

def test_zero_tax():
    """
    При нулевой ставке НДС (proc_nds = 0) цена с НДС должна совпадать с исходной.
    """
    cp_with, cp_without = optimal_calc_prices(Decimal("1.81"), 0)
    assert cp_with == Decimal("1.81")
    assert cp_without == Decimal("1.81")

def test_max_tax():
    """
    При максимальном значении НДС (proc_nds = 99) и input_price = 100.00
    ожидается, что:
      - цена с НДС будет 99.50
      - цена без НДС будет 50.00
    Расчёт:
      g = gcd(100, 199) = 1  →  d = 100
      m_ideal = 100 * 10000 / (100 * 199) ≈ 50.2513 → m_floor = 50,
      Candidate floor:
        cp_with = (50 * 100 * 199)/10000 = 99.50,
        cp_without = (50 * 100)/100 = 50.00.
    """
    cp_with, cp_without = optimal_calc_prices(Decimal("100.00"), 99)
    assert cp_with == Decimal("99.50")
    assert cp_without == Decimal("50.00")

def test_high_precision():
    """
    Проверяет, что алгоритм корректно работает с очень точными входными данными
    и результат имеет ровно два знака после запятой.
    """
    input_price = Decimal("1.00000000000000000001")
    cp_with, cp_without = optimal_calc_prices(input_price, 18)
    assert cp_with.as_tuple().exponent == -2, "Цена с НДС должна иметь 2 знака после запятой"
    assert cp_without.as_tuple().exponent == -2, "Цена без НДС должна иметь 2 знака после запятой"


# Тесты для графического интерфейса

def test_gui_valid_input(monkeypatch):
    """
    Тестирует корректную работу GUI при корректном вводе.
    Симулируем ввод значений и проверяем, что поля с результатом обновляются.
    """
    root = tk.Tk()
    root.withdraw()  # скрываем окно, чтобы не показывалось окно во время теста
    app = PriceCalculatorGUI(root)

    # Задаём корректные значения в поля ввода
    app.entry_price.insert(0, "1.81")
    app.entry_proc.insert(0, "20")

    # Переопределяем messagebox.showerror, чтобы не появлялись всплывающие окна
    monkeypatch.setattr(messagebox, "showerror", lambda title, message: None)

    # Вызываем метод расчёта
    app.calculate()

    # Проверяем, что метки результатов обновлены правильно
    assert app.result_with["text"] == "1.80"
    assert app.result_without["text"] == "1.50"
    root.destroy()

def test_gui_invalid_price(monkeypatch):
    """
    Тестирует, что при неверном вводе цены (например, текст вместо числа)
    вызывается сообщение об ошибке.
    """
    root = tk.Tk()
    root.withdraw()
    app = PriceCalculatorGUI(root)

    # Ввод некорректного значения для цены
    app.entry_price.insert(0, "abc")
    app.entry_proc.insert(0, "20")

    errors = []
    def dummy_showerror(title, message):
        errors.append(message)
    monkeypatch.setattr(messagebox, "showerror", dummy_showerror)

    app.calculate()

    assert errors, "Ожидалось появление ошибки при неверном вводе цены"
    root.destroy()

def test_gui_invalid_proc(monkeypatch):
    """
    Тестирует, что при неверном значении процента (например, значение вне диапазона 0-99)
    вызывается сообщение об ошибке.
    """
    root = tk.Tk()
    root.withdraw()
    app = PriceCalculatorGUI(root)

    app.entry_price.insert(0, "1.81")
    app.entry_proc.insert(0, "150")  # вне допустимого диапазона

    errors = []
    monkeypatch.setattr(messagebox, "showerror", lambda title, message: errors.append(message))

    app.calculate()

    assert errors, "Ожидалось появление ошибки при неверном значении процента НДС"
    root.destroy()
