from decimal import Decimal
from calculate import optimal_calc_prices


def test_typical_value():
    """
    При входных данных:
      - input_price: 1.81
      - proc_nds: 20
    Ожидается, что:
      - Цена с НДС: 1.80
      - Цена без НДС: 1.50
    """
    cp_with, cp_without = optimal_calc_prices(Decimal("1.81"), 20)
    assert cp_with == Decimal("1.80")
    assert cp_without == Decimal("1.50")


def test_zero_tax():
    """
    При нулевой ставке НДС (proc_nds = 0) цена с НДС должна совпадать с исходной,
    как и цена без НДС.
    """
    cp_with, cp_without = optimal_calc_prices(Decimal("1.81"), 0)
    assert cp_with == Decimal("1.81")
    assert cp_without == Decimal("1.81")


def test_max_tax():
    """
    При максимальном значении НДС (proc_nds = 99) и input_price = 100.00
    ожидается:
      - Цена с НДС = 99.50
      - Цена без НДС = 50.00

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

    # Проверяем количество десятичных разрядов (экспонента должна быть равна -2)
    assert cp_with.as_tuple().exponent == -2, "Цена с НДС должна иметь 2 знака после запятой"
    assert cp_without.as_tuple().exponent == -2, "Цена без НДС должна иметь 2 знака после запятой"
