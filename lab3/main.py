
import argparse
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-n', '--number', type=int, default=200)
    parser.add_argument('--seed', type=int, help='Начальное значение для повторения розыгрыша')
    parser.add_argument('--show', action='store_true', help='Открыть окно графика')
    args = parser.parse_args()
    if args.number < 2:
        parser.error('Объем выборки должен быть не меньше 2')

    m, sigma = -0.5, 1.0
    rng = random.Random(args.seed)
    samples = [m + sigma * (sum(rng.random() for _ in range(12)) - 6)
               for _ in range(args.number)]
    output = Path(__file__).resolve().parent / 'output'
    output.mkdir(exist_ok=True)
    (output / 'samples.txt').write_text(
        '\n'.join(repr(x) for x in samples) + '\n', encoding='utf-8')

    intervals = max(1, int(math.log2(args.number)))
    a, b = math.floor(min(samples)), math.floor(max(samples)) + 1
    width = (b - a) / intervals
    edges = [a + i * width for i in range(intervals + 1)]
    counts = [0] * intervals
    for value in samples:
        index = min(int((value - a) / width), intervals - 1)
        counts[index] += 1

    rows = []
    for i, count in enumerate(counts):
        closing = ']' if i == intervals - 1 else ')'
        rows.append(f'| [{edges[i]:.6f}; {edges[i+1]:.6f}{closing} '
                    f'| {count} | {count / args.number:.6f} '
                    f'| {count / (args.number * width):.6f} |')

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(edges[:-1], [c / (args.number * width) for c in counts],
           width=width, align='edge', color='skyblue', edgecolor='black',
           alpha=0.7, label='Гистограмма относительных частот')
    xs = [a + (b - a) * i / 1000 for i in range(1001)]
    density = [math.exp(-((x - m) ** 2) / (2 * sigma ** 2)) /
               (sigma * math.sqrt(2 * math.pi)) for x in xs]
    ax.plot(xs, density, color='red', linewidth=2, label='Нормальная плотность f(x)')
    ax.set(title=f'Лабораторная №3, вариант 2: m = −0,5, σ = 1, n = {args.number}',
           xlabel='x', ylabel='Относительная частота / ширина интервала')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output / 'histogram.png', dpi=180)

    if args.show:
        plt.show()
    plt.close(fig)


if __name__ == '__main__':
    main()
