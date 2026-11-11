"""HTML второй части: результаты и вычисления для записи в тетрадь."""
from html import escape


def render_intervals(r, source):
    rows = ''.join(
        f'<tr><th scope="row">{escape(label)}</th><td>{low:.6f}</td>'
        f'<td>{high:.6f}</td><td>{truth:.6f}</td>'
        f'<td>{"Да" if low <= truth <= high else "Нет"}</td></tr>'
        for label, low, high, truth in r['rows'])
    n, df = r['n'], r['df']
    variance = r['rows'][2]
    sigma = r['rows'][3]
    return f'''
<section class="card">
<span class="eyebrow">Часть 2 · только выборка лабораторной №3</span>
<h2>Доверительные интервалы</h2>
<p class="source">Файл: {escape(source)}</p>
<div class="stats"><div><small>Надёжность α</small><strong>{r['confidence']:.2f}</strong></div>
<div><small>Объём N</small><strong>{n}</strong></div>
<div><small>Степени свободы N − 1</small><strong>{df}</strong></div></div>
<div class="table-wrap"><table><thead><tr><th>Параметр</th><th>Нижняя граница</th>
<th>Верхняя граница</th><th>Истинное значение</th><th>Попадает</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="hint">Сравнение выполняется по неокруглённым границам. Непопадание истинного значения само по себе не означает ошибку расчёта.</p>
<p>Надёжность 0,95 означает: при многократном повторении опыта около 95% интервалов,
построенных этим способом, содержат истинный параметр. После вычисления конкретного интервала
параметр фиксирован: он либо принадлежит интервалу, либо нет.</p>
<p class="hint">Формулы выведены для независимой нормальной выборки. В лабораторной №3 нормальный закон моделируется
суммой 12 равномерных величин, поэтому применение интервалов к этой выборке является приближённым.</p>
</section>
<section class="card calculations"><h2>Вычисления для тетради</h2>
<p>Исходные характеристики: x̄ = {r['mean']:.9f}, S² = {r['s2']:.9f}, S = {r['s']:.9f}.
В расчётах используется исправленная дисперсия S² с делителем N − 1.</p>
<h3>1. Среднее при известной σ = {r['sigma']:g}</h3>
<p class="equation">x̄ − z·σ/√N &lt; m &lt; x̄ + z·σ/√N</p>
<p>z = Φ⁻¹((1 + α)/2) = Φ⁻¹({1-r['tail']:.3f}) = {r['z']:.9f}.</p>
<p class="equation">δ = {r['z']:.6f} · {r['sigma']:g} / √{n} = {r['delta_known']:.9f}</p>
<p class="equation">{r['mean']:.6f} ± {r['delta_known']:.6f} → ({r['rows'][0][1]:.6f}; {r['rows'][0][2]:.6f})</p>
<p class="hint">Здесь Φ — функция распределения стандартного нормального закона от −∞ до x.
Запись Φ⁻¹(α/2) в конспекте относится к функции Лапласа — интегралу от 0 до x.
Обе записи дают одно и то же положительное критическое значение.</p>
<h3>2. Среднее при неизвестной σ</h3>
<p class="equation">x̄ − t·S/√N &lt; m &lt; x̄ + t·S/√N</p>
<p>t — квантиль распределения Стьюдента при вероятности {1-r['tail']:.3f}
и {df} степенях свободы: t = {r['student']:.9f}.</p>
<p class="equation">δ = {r['student']:.6f} · {r['s']:.6f} / √{n} = {r['delta_unknown']:.9f}</p>
<p class="equation">{r['mean']:.6f} ± {r['delta_unknown']:.6f} → ({r['rows'][1][1]:.6f}; {r['rows'][1][2]:.6f})</p>
<h3>3. Дисперсия σ²</h3>
<p>За пределами центрального интервала остаётся вероятность 1 − α = {1-r['confidence']:.2f},
по {r['tail']:.3f} в каждом хвосте. Поэтому вероятности слева от нужных квантилей:
(1 − α)/2 = {r['tail']:.3f} и (1 + α)/2 = {1-r['tail']:.3f}.
Квантили χ² с {df} степенями свободы:</p>
<p class="equation">qₗ = χ²({r['tail']:.3f}; {df}) = {r['chi_low']:.9f}<br>
qᵤ = χ²({1-r['tail']:.3f}; {df}) = {r['chi_high']:.9f}</p>
<p>Здесь χ²(p; ν) — квантиль, слева от которого находится вероятность p.</p>
<p class="equation">(N − 1)S²/qᵤ &lt; σ² &lt; (N − 1)S²/qₗ</p>
<p class="equation">{df} · {r['s2']:.6f} / {r['chi_high']:.6f} &lt; σ² &lt;
{df} · {r['s2']:.6f} / {r['chi_low']:.6f}<br>
{variance[1]:.6f} &lt; σ² &lt; {variance[2]:.6f}</p>
<p class="hint">Для нижней границы делим на больший квантиль, для верхней — на меньший.</p>
<h3>4. Среднее квадратическое отклонение σ</h3>
<p>Извлекаем квадратные корни из границ интервала для дисперсии:</p>
<p class="equation">√{variance[1]:.6f} &lt; σ &lt; √{variance[2]:.6f}<br>
{sigma[1]:.6f} &lt; σ &lt; {sigma[2]:.6f}</p>
</section>'''
