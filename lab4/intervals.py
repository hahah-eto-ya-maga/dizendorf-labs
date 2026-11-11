"""Двусторонние доверительные интервалы для нормальной выборки."""

import math
import statistics
from scipy.stats import chi2, t


def confidence_intervals(values, known_sigma, true_mean, confidence=0.95):
    if len(values) < 2 or not all(math.isfinite(x) for x in values):
        raise ValueError('Нужны хотя бы два конечных наблюдения.')
    if not 0 < confidence < 1 or not math.isfinite(known_sigma) or known_sigma <= 0:
        raise ValueError('Надёжность должна быть между 0 и 1, sigma > 0.')
    n = len(values)
    mean = statistics.mean(values)
    s2 = statistics.variance(values)
    if s2 <= 0:
        raise ValueError('Для интервальных оценок нужна положительная выборочная дисперсия.')
    s = math.sqrt(s2)
    df = n - 1
    tail = (1 - confidence) / 2
    z = statistics.NormalDist().inv_cdf(1 - tail)
    student = float(t.ppf(1 - tail, df))
    chi_low, chi_high = float(chi2.ppf(tail, df)), float(chi2.ppf(1 - tail, df))
    delta_known = z * known_sigma / math.sqrt(n)
    delta_unknown = student * s / math.sqrt(n)
    variance_bounds = (df * s2 / chi_high, df * s2 / chi_low)
    rows = [
        ('Среднее m · σ известна', mean - delta_known, mean + delta_known, true_mean),
        ('Среднее m · σ неизвестна', mean - delta_unknown, mean + delta_unknown, true_mean),
        ('Дисперсия σ²', *variance_bounds, known_sigma ** 2),
        ('СКО σ', *(math.sqrt(x) for x in variance_bounds), known_sigma),
    ]
    return dict(n=n, df=df, mean=mean, s2=s2, s=s, sigma=known_sigma,
                confidence=confidence, tail=tail, z=z, student=student,
                chi_low=chi_low, chi_high=chi_high, delta_known=delta_known,
                delta_unknown=delta_unknown, rows=rows)


def interval_text(result):
    r = result
    lines = ['', 'Часть 2. Доверительные интервалы для нормальной выборки.',
             f'Надёжность alpha = {r["confidence"]}; N = {r["n"]}; df = {r["df"]}',
             f'x_mean = {r["mean"]:.9f}; S^2 = {r["s2"]:.9f}; S = {r["s"]:.9f}',
             f'z = {r["z"]:.9f}; t = {r["student"]:.9f}',
             f'chi2_low = {r["chi_low"]:.9f}; chi2_high = {r["chi_high"]:.9f}',
             'm (sigma известна): x_mean +/- z*sigma/sqrt(N)',
             'm (sigma неизвестна): x_mean +/- t*S/sqrt(N)',
             'sigma^2: ((N-1)*S^2/chi2_high, (N-1)*S^2/chi2_low)',
             'sigma: квадратные корни границ интервала для sigma^2']
    for label, low, high, truth in r['rows']:
        lines.append(f'{label}: ({low:.9f}; {high:.9f}); теория = {truth}; '
                     f'попадает: {"да" if low <= truth <= high else "нет"}')
    return lines
