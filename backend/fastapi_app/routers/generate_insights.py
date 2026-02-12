import math
from collections import Counter

SEMANTIC_HINTS = {
    "Категория": "product_category",
    "Артикул": "product_item",
    "Брой продадени": "quantity_sold",
    "Единична цена": "unit_price",
    "Обща цена": "total_price",
    "Магазин": "store",
    "Дата": "date",
    "Начин на плащане": "payment_method",
    
}

def _safe_nums(rows, col):
    nums = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        n = _to_number(r.get(col))
        if n is not None:
            nums.append(n)
    return nums

def kpi_total_revenue(columns, rows):
    col = next((c["name"] for c in columns if "цена" in c["name"].lower() or "revenue" in c["name"].lower()), None)
    if not col:
        return None

    nums = _safe_nums(rows, col)
    if not nums:
        return None

    total = sum(nums)

    return {
        "key": "total_revenue",
        "label": "Обща стойност продажби",
        "value": round(total, 2),
        "unit": "EUR",
        "trend": "neutral",
        "severity": "info"
    }

def kpi_avg_value(columns, rows):
    col = next((c["name"] for c in columns if c.get("dtype") == "numeric"), None)
    if not col:
        return None

    nums = _safe_nums(rows, col)
    if not nums:
        return None

    avg = sum(nums) / len(nums)

    return {
        "key": "average_value",
        "label": f"Средна стойност {col}",
        "value": round(avg, 2),
        "unit": "EUR",
        "trend": "neutral",
        "severity": "info"
    }

def kpi_total_quantity(columns, rows):
    col = next((c["name"] for c in columns if "брой" in c["name"].lower() or "quantity" in c["name"].lower()), None)
    if not col:
        return None

    nums = _safe_nums(rows, col)
    if not nums:
        return None

    return {
        "key": "total_quantity",
        "label": "Общо количество продадени артикули",
        "value": int(sum(nums)),
        "unit": "брой",
        "trend": "neutral",
        "severity": "info"
    }

def kpi_top_category(columns, rows):
    cat_col = next((c["name"] for c in columns if c.get("dtype") == "categorical"), None)
    val_col = next((c["name"] for c in columns if c.get("dtype") == "numeric"), None)

    if not cat_col or not val_col:
        return None

    totals = {}
    for r in rows:
        cat = r.get(cat_col)
        val = _to_number(r.get(val_col))
        if cat and val:
            totals[cat] = totals.get(cat, 0) + val

    if not totals:
        return None

    top = max(totals.items(), key=lambda x: x[1])

    return {
        "key": "top_category",
        "label": "Топ категория по стойност",
        "value": top[0],
        "unit": "",
        "trend": "up",
        "severity": "info"
    }

def kpi_revenue_concentration(columns, rows):
    cat_col = next((c["name"] for c in columns if c.get("dtype") == "categorical"), None)
    val_col = next((c["name"] for c in columns if c.get("dtype") == "numeric"), None)

    if not cat_col or not val_col:
        return None

    totals = {}
    total_revenue = 0

    for r in rows:
        cat = r.get(cat_col)
        val = _to_number(r.get(val_col))
        if cat and val:
            totals[cat] = totals.get(cat, 0) + val
            total_revenue += val

    if not totals or total_revenue == 0:
        return None

    top_val = max(totals.values())
    pct = top_val / total_revenue * 100

    return {
        "key": "revenue_concentration",
        "label": "Процент от общите продажби на топ категория",
        "value": round(pct, 1),
        "unit": "%",
        "trend": "neutral",
        "severity": "warning" if pct > 60 else "info"
    }

def kpi_avg_order_value(columns, rows):
    val_col = next((c["name"] for c in columns if c.get("dtype") == "numeric"), None)
    if not val_col:
        return None

    nums = _safe_nums(rows, val_col)
    if not nums:
        return None

    avg = sum(nums) / len(nums)

    return {
        "key": "average_order_value",
        "label": "Средна стойност на поръчка",
        "value": round(avg, 2),
        "unit": "EUR",
        "trend": "neutral",
        "severity": "info"
    }
    
def kpi_rows_count(columns, rows):
    return {
        "key": "rows_count",
        "label": "Брой редове в набора от данни",
        "value": len(rows),
        "unit": "реда",
        "trend": "neutral",
        "severity": "info"
    }
    
def kpi_category_count(columns, rows):
    print("Finding category column...", columns)
    category_col = None
    for c in columns:
        if c.get("dtype") == "categorical" and c["name"].lower() in ["категория", "product_category", "category"]:
            category_col = c["name"]
            
            break   
    if not category_col:
        return None
    
    values = {
        r.get(category_col) for r in rows
        if r.get(category_col)
    }
    print("VALUES:", values)
    return {
        "key": "category_count",
        "label": f"Брой уникални категории в '{category_col}'",
        "value": len(values),
        "unit": "категории",
        "trend": "neutral",
        "severity": "info"  
    }

def generate_kpis(columns, rows):
    kpis = []

    for fn in [
        
        kpi_rows_count,
        kpi_total_revenue,
        kpi_avg_order_value,
        kpi_category_count,
        
        #kpi_avg_value,
        #kpi_total_quantity,
        #kpi_top_category,
        #kpi_revenue_concentration
    ]:
        try:
            kpi = fn(columns, rows)
            if kpi:
                kpis.append(kpi)
        except Exception:
            continue

    return kpis


def top_revenue_dimension(columns, rows):
    insights = []

    cat_cols = [c["name"] for c in columns if c.get("dtype") == "categorical"]
    revenue_cols = [c["name"] for c in columns if c.get("dtype") == "numeric"]

    if not (cat_cols and revenue_cols):
        return insights

    cat = cat_cols[0]
    revenue = revenue_cols[-1]

    agg = {}
    for r in rows:
        k = r.get(cat)
        v = _to_number(r.get(revenue))
        if k and v is not None:
            agg[k] = agg.get(k, 0) + v

    if not agg:
        return insights

    top_key = max(agg, key=agg.get)
    insights.append({
        "title": f"Топ {cat} по приходи",
        "text": f"'{top_key}' генерира най-високи приходи ({agg[top_key]:.2f}).",
        "severity": "info"
    })

    return insights


def revenue_by_category(columns, rows):
    insights = []
    
    #1. find numeric columns
    numeric_cols = [
        c["name"] for c in columns
        if c.get("dtype") == "numeric"
    ]
    cat_cols = [
        c["name"] for c in columns
        if c.get("dtype") == "categorical"
    ]
    
    if not numeric_cols or not cat_cols or not rows:
        return []
    
    value_col = numeric_cols[-1]
    group_col = cat_cols[0]
    
    totals = {}
    
    for r in rows:
        key = r.get(group_col)
        val = _to_number(r.get(value_col))
        if key and val is not None:
            totals[key] = totals.get(key, 0) + val
            
    if not totals:
        return []
    
    total_sum = sum(totals.values())
    top_key, top_value = max(totals.items(), key=lambda x: x[1])
    ptc = (top_value / total_sum) * 100 if total_sum > 0 else 0
    
    insights.append({
        "title": f"Топ категория по приходи: {top_key}",
        "text": f"'{top_key}' допринася за {ptc:.1f}% от общите {value_col}.",
        "severity": "info"
    })
    
    if ptc > 60:
        insights.append({
            "title": f"Висока зависимост от категория: {top_key}",
            "text": f"Повече от 60% от приходите зависят от една категория.",
            "severity": "warning"
        })

    return insights

def quantity_concentration(columns, rows):
    insights = []

    if not {"Артикул", "Брой продадени"}.issubset(c["name"] for c in columns):
        return insights

    totals = {}

    for r in rows:
        item = r.get("Артикул")
        qty = _to_number(r.get("Брой продадени"))
        if item and qty is not None:
            totals[item] = totals.get(item, 0) + qty

    if not totals:
        return insights

    top_item, top_qty = max(totals.items(), key=lambda x: x[1])
    total_qty = sum(totals.values())

    pct = top_qty / total_qty * 100

    insights.append({
        "title": "Най-продаван артикул",
        "text": f"'{top_item}' допринася за {pct:.1f}% от общото количество продадени артикули.",
        "severity": "warning" if pct > 50 else "info"
    })

    return insights

def quantity_price_consistency(columns, rows):
    insights = []

    qty_cols = [c["name"] for c in columns if "брой" in c["name"].lower() or "quantity" in c["name"].lower()]
    price_cols = [c["name"] for c in columns if "единична" in c["name"].lower() or "price" in c["name"].lower()]
    total_cols = [c["name"] for c in columns if "обща" in c["name"].lower() or "total" in c["name"].lower()]

    if not (qty_cols and price_cols and total_cols):
        return insights

    qty, price, total = qty_cols[0], price_cols[0], total_cols[0]

    mismatches = 0
    checked = 0

    for r in rows:
        q = _to_number(r.get(qty))
        p = _to_number(r.get(price))
        t = _to_number(r.get(total))
        if None in (q, p, t):
            continue
        checked += 1
        if abs(q * p - t) > 0.01:
            mismatches += 1

    if checked > 0 and mismatches > 0:
        insights.append({
            "title": "Несъответствие в изчисляването на приходите",
            "text": f"{mismatches} от {checked} реда имат количество × цена ≠ общо.",
            "severity": "warning"
        })

    return insights


def total_and_average_revenue(columns, rows):
    insights = []

    revenue_cols = [
        c["name"] for c in columns
        if c.get("dtype") == "numeric" and
        any(k in c["name"].lower() for k in ["total", "revenue", "amount", "цена", "стойност"])
    ]

    if not revenue_cols:
        return insights

    col = revenue_cols[0]
    nums = [_to_number(r.get(col)) for r in rows]
    nums = [n for n in nums if n is not None]

    if not nums:
        return insights

    total = sum(nums)
    avg = total / len(nums)

    insights.append({
        "title": f"Общо и средно ({col})",
        "text": f"Общо: {total:.2f}, Средно на ред: {avg:.2f}",
        "severity": "info"
    })

    return insights


def sales_by_date(columns, rows):
    insights = []

    if not {"Дата на продажба", "Обща цена"}.issubset(c["name"] for c in columns):
        return insights

    totals = {}

    for r in rows:
        d = r.get("Дата на продажба")
        val = _to_number(r.get("Обща цена"))
        if d and val:
            totals[d] = totals.get(d, 0) + val

    if len(totals) < 2:
        return insights

    dates = sorted(totals.keys())
    first, last = dates[0], dates[-1]

    if totals[last] > totals[first]:
        insights.append({
            "title": "Тенденция на продажбите",
            "text": "Продажбите показват възходящ тренд с времето.",
            "severity": "info"
        })
    else:
        insights.append({
            "title": "Тенденция на продажбите",
            "text": "Продажбите намаляват с времето.",
            "severity": "warning"
        })

    return insights


def price_quantity_mismatch(columns, rows):
    insights = []

    needed = {"Артикул", "Единична цена", "Брой продадени"}
    if not needed.issubset(c["name"] for c in columns):
        return insights

    data = []

    for r in rows:
        item = r.get("Артикул")
        price = _to_number(r.get("Единична цена"))
        qty = _to_number(r.get("Брой продадени"))
        if item and price and qty:
            data.append((item, price, qty))

    if not data:
        return insights

    # най-скъпо, но малко продавано
    data.sort(key=lambda x: (-x[1], x[2]))
    item, price, qty = data[0]

    insights.append({
        "title": "Скъп артикул с ниски продажби",
        "text": f"'{item}' има висока единична цена ({price:.2f}), но нисък обем продажби ({qty}).",
        "severity": "info"
    })

    return insights


def data_quality_insights(columns, rows):
    insights = []

    for c in columns:
        name = c["name"]
        missing = sum(
            1 for r in rows if r.get(name) in (None, "", " ")
        )
        pct = missing / len(rows) * 100

        if pct > 30:
            insights.append({
                "title": f"Липсващи данни в {name}",
                "text": f"{pct:.0f}% от редовете имат липсващи стойности.",
                "severity": "warning"
            })

    return insights

def missing_data_insight(columns, rows):
    insights = []

    total_rows = len(rows)
    if total_rows == 0:
        return insights

    for c in columns:
        name = c["name"]
        missing = sum(1 for r in rows if r.get(name) in (None, "", "NaN"))
        pct = missing / total_rows * 100

        if pct > 30:
            insights.append({
                "title": f"Липсващи данни в {name}",
                "text": f"{pct:.0f}% от редовете имат липсващи стойности.",
                "severity": "warning"
            })

    return insights


def dataset_overview(columns, rows):
    insights = []
    overview = {
        "total_rows": len(rows),
        "total_columns": len(columns),
        "numeric_columns": sum(1 for c in columns if c.get("dtype") == "numeric"),
        "categorical_columns": sum(1 for c in columns if c.get("dtype") == "categorical"),
    }
    insights.append({
        "title": "Преглед на набора от данни",
        "text": (
            f"Общо редове: {overview['total_rows']}, "
            f"Общо колони: {overview['total_columns']}, "
            f"Числови колони: {overview['numeric_columns']}, "
            f"Категориални колони: {overview['categorical_columns']}"
        ),
        "severity": "info"
    })  
    return insights



def _to_number(v):
    """
    Конвертира стойност към float.
    Връща None ако не може.
    """
    if v is None:
        return None

    if isinstance(v, bool):
        return None

    if isinstance(v, (int, float)):
        return float(v)

    if isinstance(v, str):
        s = v.strip()
        if not s:
            return None

        # махаме интервали (хилядни разделители)
        s = s.replace(" ", "")

        # ако има и , и . → махаме хилядните запетаи
        if "," in s and "." in s:
            s = s.replace(",", "")
        else:
            # иначе , е десетична
            s = s.replace(",", ".")

        try:
            n = float(s)
            if math.isfinite(n):
                return n
        except ValueError:
            return None

    return None



def generate_insights(columns, rows):
    insights = []
    rows = [
    r for r in rows
    if isinstance(r, dict) and any(v is not None for v in r.values())
]


 

    if not columns or not rows:
        return [{
            "title": "Липсващи данни за анализ",
            "text": "Няма предоставени редове за анализ.",
            "severity": "info"
        }]

    # numeric колони
    numeric_cols = [
        c["name"] for c in columns
        if c.get("dtype") == "numeric"
    ]

    # categorical колони
    categorical_cols = [
        c["name"] for c in columns
        if c.get("dtype") == "categorical"
    ]

    # ---------- NUMERIC ----------
    for col in numeric_cols:
        nums = []

        for r in rows:
            if not isinstance(r, dict):
                continue
            n = _to_number(r.get(col))
            if n is not None:
                nums.append(n)

        if not nums:
            insights.append({
                "title": f"Няма числови данни в '{col}'",
                "text": f"Стойностите не могат да бъдат преобразувани в числа.",
                "severity": "warning"
            })
            continue

        avg = sum(nums) / len(nums)
        mn = min(nums)
        mx = max(nums)

        insights.append({
            "title": f"Статистика за {col}",
            "text": (
                f"Средно: {avg:.2f}, "
                f"Минимум: {mn:.2f}, "
                f"Максимум: {mx:.2f}, "
                f"Брой: {len(nums)}"
            ),
            "severity": "info"
        })

        # аномалия
        if avg > 0 and mx > avg * 5:
            insights.append({
                "title": f"Аномалия в {col}",
                "text": f"Максималната стойност ({mx:.2f}) е много по-голяма от средната ({avg:.2f}).",
                "severity": "warning"
            })

    # ---------- CATEGORICAL ----------
    for col in categorical_cols:
        vals = [
            r.get(col) for r in rows
            if isinstance(r, dict) and r.get(col)
        ]

        if not vals:
            continue

        ctr = Counter(vals)
        top, count = ctr.most_common(1)[0]
        pct = count / len(vals) * 100

        insights.append({
            "title": f"Топ стойност в {col}",
            "text": f"'{top}' се среща в {pct:.1f}% от редовете.",
            "severity": "info"
        })

        if pct > 70:
            insights.append({
                "title": f"Висока концентрация в {col}",
                "text": f"Една стойност доминира колоната.",
                "severity": "warning"
            })

    if not insights:
        insights.append({
            "title": "Не са открити модели",
            "text": "Данните са твърде малки или еднородни.",
            "severity": "info"
        })
        
    
        
    
    insights += revenue_by_category(columns, rows)
    insights += quantity_concentration(columns, rows)
    insights += top_revenue_dimension(columns, rows)
    insights += price_quantity_mismatch(columns, rows)
    insights += sales_by_date(columns, rows)
    insights += data_quality_insights(columns, rows)
    insights += total_and_average_revenue(columns, rows)
    
    insights += quantity_price_consistency(columns, rows)
    insights += missing_data_insight(columns, rows)
    insights += dataset_overview(columns, rows)  
    
    if not insights:
        insights.append({
            "title": "Не са генерирани изводи",
            "text": "Не бяха открити значими модели или проблеми в данните.",
            "severity": "info"
        })
        

    return insights

