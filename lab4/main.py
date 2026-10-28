"""Лабораторная №4, часть 1: точечные оценки для выборок варианта 2."""

import math
from html_report import write_html
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def latest_sample(folder, lab_number):
    """Выбрать последнюю выборку по времени изменения файла."""
    candidates = [path for path in folder.glob(f'lab{lab_number}_*.txt')
                  if path.is_file()]
    # Совместимость с результатами старой версии третьей лабораторной.
    old_sample = folder / 'samples.txt'
    if lab_number == 3 and old_sample.is_file():
        candidates.append(old_sample)
    if not candidates:
        raise ValueError(
            f'Нет выборки в {folder}. Сначала запустите lab{lab_number}/main.py.')
    return max(candidates, key=lambda path: (path.stat().st_mtime_ns, path.name))


def read_sample(path):
    try:
        values = [float(value) for value in path.read_text(encoding='utf-8').split()]
    except ValueError as error:
        raise ValueError(f'В файле {path} найдено значение, не являющееся числом.') from error
    if len(values) < 2:
        raise ValueError(f'В файле {path} должно быть не меньше двух значений.')
    if not all(math.isfinite(value) for value in values):
        raise ValueError(f'В файле {path} есть бесконечные значения или NaN.')
    return values


def calculate(values):
    count = len(values)
    mean = math.fsum(values) / count
    squared_deviations = math.fsum((value - mean) ** 2 for value in values)
    variance = squared_deviations / count
    corrected_variance = squared_deviations / (count - 1)
    return mean, variance, corrected_variance, math.sqrt(variance), math.sqrt(corrected_variance)


def main():
    # Теоретические параметры распределений варианта 2.
    trials, probability = 11, 0.07
    a, b = -3, -1
    m, sigma = -0.5, 1.0
    distributions = [
        (1, 'Биномиальное: n = 11, p = 0.07',
         trials * probability, trials * probability * (1 - probability)),
        (2, 'Равномерное: a = -3, b = -1', (a + b) / 2, (b - a) ** 2 / 12),
        (3, 'Нормальное: m = -0.5, sigma = 1', m, sigma ** 2),
    ]
    lines = [
        'Лабораторная работа №4. Часть 1. Вариант 2.',
        'Точечные оценки и сравнение с теоретическими характеристиками.',
        'Выбор файлов: по последнему времени изменения.',
        '',
        'x_mean = sum(x_i) / N',
        'D_v = sum((x_i - x_mean)^2) / N',
        'S^2 = sum((x_i - x_mean)^2) / (N - 1)',
        'sigma_v = sqrt(D_v), S = sqrt(S^2)',
    ]
    datasets = []
    for number, description, true_mean, true_variance in distributions:
        path = latest_sample(ROOT / f'lab{number}' / 'output', number)
        values = read_sample(path)
        estimates = calculate(values)
        true_sigma = math.sqrt(true_variance)
        theoretical = (true_mean, true_variance, true_variance, true_sigma, true_sigma)
        names = ('Среднее (x_mean)', 'Выборочная дисперсия (D_v)',
                 'Исправленная дисперсия (S^2)', 'Выборочное СКО (sigma_v)',
                 'Исправленное СКО (S)')
        modified = datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        datasets.append({
            'number': number, 'description': description,
            'file': str(path.relative_to(ROOT)), 'modified': modified,
            'values': values, 'estimates': estimates, 'theoretical': theoretical,
        })
        lines.extend([
            '', f'Лабораторная №{number}. {description}',
            f'Файл: {path.relative_to(ROOT)}', f'Изменён: {modified}',
            f'Объём выборки N = {len(values)}',
            f'{"Характеристика":<30} {"Оценка":>12} {"Теория":>12} {"Абс. ошибка":>12}',
        ])
        for name, estimate, truth in zip(names, estimates, theoretical):
            lines.append(f'{name:<30} {estimate:12.6f} {truth:12.6f} {abs(estimate - truth):12.6f}')

    report = '\n'.join(lines) + '\n'
    output = Path(__file__).resolve().parent / 'output'
    output.mkdir(exist_ok=True)
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = output / f'lab4_part1_{current_time}.txt'
    filename.write_text(report, encoding='utf-8')
    print(report)
    print(f'Отчёт сохранён: {filename}')
    html_filename = filename.with_suffix('.html')
    write_html(html_filename, 2, datasets, current_time.replace('_', ' '))
    print(f'HTML-отчёт сохранён: {html_filename}')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(f'Ошибка: {error}')
