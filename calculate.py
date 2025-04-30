import math
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
            cp_with = (Decimal(m * d * (100 + proc_nds)) / Decimal(10000)).quantize(Decimal("0.01"))
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
