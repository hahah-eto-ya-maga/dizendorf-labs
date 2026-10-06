import argparse
import random
import math
import matplotlib.pyplot as plt
import datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=200)
    args = parser.parse_args()

    n = args.number
    a = -3
    b = -1

    samples = []
    for _ in range(n):
        gamma = random.random()
        x = 2 * gamma - 3
        samples.append(x)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output = Path(__file__).resolve().parent / 'output'
    output.mkdir(exist_ok=True)
    txt_filename = output / f"lab2_{current_time}.txt"
    png_filename = output / f"lab2_{current_time}.png"

    with open(txt_filename, "w") as f:
        for val in samples:
            f.write(f"{val:.4f}\n")

    N = max(1, int(math.log2(n))) 
    
    plt.figure(figsize=(9, 6))
    
    plt.hist(samples, bins=N, range=(a, b), density=True, color='skyblue', edgecolor='black', alpha=0.7, label='Гистограмма')

    x_pdf = [a - 0.5, a, a, b, b, b + 0.5]
    y_pdf = [0, 0, 0.5, 0.5, 0, 0]
    plt.plot(x_pdf, y_pdf, color='red', linewidth=2, label='f(x)')

    plt.title(f'Равномерное распределение на ({a}, {b}), n={n}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(a - 0.5, b + 0.5)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.savefig(png_filename)

if __name__ == '__main__':
    main()
