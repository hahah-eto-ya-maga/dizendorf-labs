"""Автономный HTML-отчёт: оформление, гистограммы и просмотр выборок."""

import html
import json
import math


LABELS = ('Среднее · x̄', 'Выборочная дисперсия · Dᵥ',
          'Исправленная дисперсия · S²', 'Выборочное СКО · σᵥ', 'Исправленное СКО · S')


def histogram(values, discrete=False):
    low, high = min(values), max(values)
    bins = int(high - low + 1) if discrete else max(1, int(math.log2(len(values))))
    bins = min(60, bins)
    step = (high - low + (1 if discrete else 0)) / bins if high > low or discrete else 1
    counts = [0] * bins
    for value in values:
        counts[min(bins - 1, int((value - low) / step))] += 1
    peak = max(counts)
    bars = []
    for i, count in enumerate(counts):
        height = count / peak * 100
        label = f'{low + i * step:.4g} … {low + (i + 1) * step:.4g}: {count} наблюдений'
        bars.append(f'<rect x="{10 + i * 580 / bins:.2f}" y="{112-height:.2f}" '
                    f'width="{max(1, 580 / bins-3):.2f}" height="{height:.2f}" rx="3">'
                    f'<title>{html.escape(label)}</title></rect>')
    return ('<svg viewBox="0 0 600 140" role="img" aria-label="Гистограмма количества наблюдений">'
            + ''.join(bars) + f'<text x="10" y="135">{low:.4g}</text>'
            + f'<text x="590" y="135" text-anchor="end">{high:.4g}</text></svg>')


def write_html(path, variant, datasets, created):
    sections = []
    for data in datasets:
        number = data['number']
        values = data['values']
        rows = ''.join(
            f'<tr><th scope="row">{label}</th><td>{estimate:.6f}</td>'
            f'<td>{truth:.6f}</td><td>{abs(estimate-truth):.6f}</td></tr>'
            for label, estimate, truth in zip(LABELS, data['estimates'], data['theoretical']))
        sections.append(f'''
<section class="card" id="lab{number}" data-index="{number-1}">
  <div class="section-head"><div><span class="eyebrow">Выборка 0{number}</span>
  <h2>{html.escape(data['description'])}</h2></div><span class="badge">N = {len(values)}</span></div>
  <p class="source">{html.escape(data['file'])}<br>Изменён: {html.escape(data['modified'])}</p>
  <div class="stats"><div><small>Минимум</small><strong>{min(values):.6f}</strong></div>
  <div><small>Среднее</small><strong>{data['estimates'][0]:.6f}</strong></div>
  <div><small>Максимум</small><strong>{max(values):.6f}</strong></div></div>
  <div class="chart">{histogram(values, number == 1)}<p>Распределение наблюдений · высота столбца — количество значений</p></div>
  <h3>Оценки и теория</h3><div class="table-wrap"><table>
  <thead><tr><th>Характеристика</th><th>Оценка</th><th>Теория</th><th>Абс. ошибка</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
  <p class="hint">Абсолютная ошибка = |оценка − теория|. Расхождение на случайной выборке ожидаемо.</p>
  <details class="samples"><summary>Посмотреть выборку · {len(values)} значений</summary>
  <div class="controls"><label>Порядок <select class="order"><option value="original">Исходный</option><option value="asc">По возрастанию</option><option value="desc">По убыванию</option></select></label>
  <label>На странице <select class="page-size"><option>20</option><option>50</option><option>100</option></select></label>
  <button class="download" type="button">Скачать CSV</button></div>
  <div class="table-wrap"><table><thead><tr><th>№ в исходной выборке</th><th>Значение xᵢ</th></tr></thead><tbody class="sample-rows"></tbody></table></div>
  <div class="pager"><button class="previous" type="button">← Назад</button><span class="page-label" aria-live="polite"></span><button class="next" type="button">Далее →</button></div>
  </details>
</section>''')
    payload = json.dumps([{'number': d['number'], 'values': d['values']} for d in datasets],
                         ensure_ascii=False, allow_nan=False).replace('<', '\\u003c')
    document = TEMPLATE.replace('%%VARIANT%%', str(variant)).replace('%%DATE%%', html.escape(created))
    document = document.replace('%%TOTAL%%', str(sum(len(d['values']) for d in datasets)))
    document = document.replace('%%SECTIONS%%', '\n'.join(sections)).replace('%%DATA%%', payload)
    path.write_text(document, encoding='utf-8')


TEMPLATE = r'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Лабораторная 4 · Вариант %%VARIANT%%</title>
<style>
:root{color-scheme:light;--ink:#18332e;--muted:#63756f;--line:#dce5df;--accent:#166c56;--paper:#f3f5ef}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,sans-serif}
main{max-width:1040px;margin:auto;padding:40px 22px 70px}.eyebrow{text-transform:uppercase;letter-spacing:.16em;font-size:11px;font-weight:750;color:var(--accent)}
header{padding:24px 0 30px}h1{font-size:clamp(34px,6vw,58px);line-height:1.08;letter-spacing:-.045em;margin:18px 0}header p{max-width:640px;color:var(--muted)}
.meta{display:flex;gap:12px;flex-wrap:wrap;font-size:13px;color:var(--muted)}.badge{background:#e5f1e9;padding:7px 13px;border-radius:30px;white-space:nowrap;font-size:13px;font-weight:650}
nav{display:flex;flex-wrap:wrap;gap:9px;margin:22px 0}nav a,button{border:1px solid var(--line);background:white;color:var(--ink);border-radius:10px;padding:10px 15px;text-decoration:none;font:inherit;font-size:14px;cursor:pointer}
nav a:hover,button:hover{background:#e5f1e9}button:disabled{opacity:.4;cursor:default}:focus-visible{outline:3px solid #c48626;outline-offset:3px}
.card{background:#fff;border:1px solid var(--line);border-radius:20px;padding:28px;margin-bottom:22px;scroll-margin-top:20px}.section-head{display:flex;justify-content:space-between;gap:16px;align-items:start}h2{font-size:23px;line-height:1.3;margin:8px 0}h3{font-size:17px;margin:24px 0 12px}.source{font-size:12px;color:var(--muted);overflow-wrap:anywhere}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:22px 0}.stats>div{background:#f5f7f2;border-radius:12px;padding:15px}.stats small{display:block;color:var(--muted)}.stats strong{display:block;font-size:clamp(15px,3vw,24px);font-variant-numeric:tabular-nums;margin-top:4px}
.chart{padding:16px 12px 4px;border:1px solid var(--line);border-radius:14px}.chart svg{display:block;width:100%;max-height:190px;fill:var(--accent)}.chart text{fill:var(--muted);font:11px system-ui}.chart p,.hint{font-size:12px;color:var(--muted)}.chart p{margin:4px 0 8px}
.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}th,td{text-align:right;padding:12px 10px;border-bottom:1px solid #e8eee9;white-space:nowrap}th:first-child{text-align:left}thead{background:#f5f7f2;font-size:12px;color:var(--muted)}tbody th{font-weight:500}tbody tr:hover{background:#f8faf6}td:last-child{color:var(--accent)}
summary{cursor:pointer;font-weight:650;padding:15px 0}.samples{margin-top:22px;border-top:1px solid var(--line)}.controls{display:flex;gap:12px;align-items:end;flex-wrap:wrap;margin:8px 0 15px}.controls label{font-size:12px;color:var(--muted)}select{display:block;background:white;border:1px solid var(--line);border-radius:8px;padding:10px;font:inherit;color:var(--ink);margin-top:4px}.pager{display:flex;gap:10px;align-items:center;justify-content:space-between;margin-top:18px}.page-label{font-size:12px;text-align:center;color:var(--muted)}
.explainer{background:#e9eee4;border-radius:16px;padding:22px;margin-top:24px}.explainer h2{font-size:19px}.formulas{display:grid;grid-template-columns:1fr 1fr;gap:16px}.formulas p{margin:0;font-size:14px}.formulas b{display:block;margin-bottom:4px}footer{font-size:12px;color:var(--muted);margin-top:26px}
@media(max-width:600px){main{padding:20px 12px 40px}.card{padding:18px 14px}.section-head{display:block}.section-head .badge{display:inline-block;margin-top:8px}.stats{gap:5px}.stats>div{padding:10px 6px}.stats small{font-size:11px}.formulas{grid-template-columns:1fr}th,td{padding:10px 8px}.pager button{padding:9px 10px}}
@media print{body{background:white}main{max-width:none;padding:0}nav,.controls,.pager,.samples{display:none}.card{break-inside:avoid;border-radius:0;padding:14px;margin:10px 0}.table-wrap{overflow:visible}header{padding:0}h1{font-size:32px}.chart svg{max-height:120px}*{print-color-adjust:exact}}
</style></head><body><main>
<header><span class="eyebrow">Теория вероятностей и математическая статистика</span>
<h1>От выборки<br>к оценке.</h1><p>Лабораторная работа №4 · Часть 1. Точечные оценки среднего, дисперсии и стандартного отклонения.</p>
<div class="meta"><span class="badge">Вариант %%VARIANT%%</span><span>3 выборки · %%TOTAL%% наблюдений</span><span>%%DATE%%</span></div>
<nav aria-label="Разделы отчёта"><a href="#lab1">01 · Биномиальное</a><a href="#lab2">02 · Равномерное</a><a href="#lab3">03 · Нормальное</a><button id="print" type="button">Печать / PDF</button></nav></header>
<noscript><p>Для листания выборок включите JavaScript. Таблицы оценок и гистограммы доступны без него.</p></noscript>
%%SECTIONS%%
<aside class="explainer"><h2>Что означают числа</h2><div class="formulas">
<p><b>Среднее: x̄ = Σxᵢ / N</b>Оценка центра распределения по наблюдениям.</p>
<p><b>Дисперсия: Dᵥ = Σ(xᵢ − x̄)² / N</b>Средний квадрат отклонения от выборочного среднего.</p>
<p><b>Исправленная дисперсия: S² = N·Dᵥ / (N − 1)</b>Поправка устраняет систематическое занижение оценки дисперсии.</p>
<p><b>СКО: σᵥ = √Dᵥ; S = √S²</b>Меры разброса в тех же единицах, что и исходные наблюдения.</p>
</div></aside><footer>Использованы последние TXT-выборки по времени изменения файлов. Теоретические характеристики соответствуют варианту %%VARIANT%%. Отчёт содержит только первую часть лабораторной работы.</footer>
</main><script id="sample-data" type="application/json">%%DATA%%</script>
<script>
'use strict';
const datasets=JSON.parse(document.getElementById('sample-data').textContent);
document.getElementById('print').addEventListener('click',()=>window.print());
document.querySelectorAll('.card').forEach(card=>{
 const data=datasets[Number(card.dataset.index)];
 const original=data.values.map((value,index)=>({value,index:index+1}));
 let ordered=original.slice(),page=0;
 const size=card.querySelector('.page-size'),order=card.querySelector('.order');
 const previous=card.querySelector('.previous'),next=card.querySelector('.next');
 function render(){
  const limit=Number(size.value),pages=Math.ceil(ordered.length/limit);
  page=Math.max(0,Math.min(page,pages-1));
  const start=page*limit,stop=Math.min(start+limit,ordered.length);
  const fragment=document.createDocumentFragment();
  ordered.slice(start,stop).forEach(item=>{
   const row=document.createElement('tr');
   [item.index,item.value.toString()].forEach(value=>{const cell=document.createElement('td');cell.textContent=value;row.appendChild(cell);});
   fragment.appendChild(row);
  });
  card.querySelector('.sample-rows').replaceChildren(fragment);
  card.querySelector('.page-label').textContent=`${start+1}–${stop} из ${ordered.length} · страница ${page+1}/${pages}`;
  previous.disabled=page===0;next.disabled=page===pages-1;
 }
 order.addEventListener('change',()=>{ordered=original.slice();if(order.value!=='original')ordered.sort((a,b)=>order.value==='asc'?a.value-b.value:b.value-a.value);page=0;render();});
 size.addEventListener('change',()=>{page=0;render();});
 previous.addEventListener('click',()=>{page--;render();});next.addEventListener('click',()=>{page++;render();});
 card.querySelector('.download').addEventListener('click',()=>{
  const csv='index,value\n'+ordered.map(item=>`${item.index},${item.value}`).join('\n');
  const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
  const link=document.createElement('a');link.href=url;link.download=`lab${data.number}_variant%%VARIANT%%.csv`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 });
 render();
});
</script></body></html>
'''
