def choose_main_metric(numeric_columns):
    PRIORITY_NAMES = [
        "revenue",
        "sales",
        "amount",
        "total",
        "price",
        "cost",
        "value",
    ]

    for name in PRIORITY_NAMES:
        for col in numeric_columns:
            if name in col.lower():
                return col

    return numeric_columns[0] if numeric_columns else None


def build_main_chart(df, schema):
    numeric_cols = schema.get("numeric", [])
    date_cols = schema.get("date", [])
    cat_cols = schema.get("categorical", [])

    main_metric = choose_main_metric(numeric_cols)

    if not main_metric:
        return None

    # 1. Time series chart
    if date_cols:
        date_col = date_cols[0]

        temp = df[[date_col, main_metric]].dropna()

        if len(temp) > 1:
            grouped = (
                temp.groupby(date_col)[main_metric]
                .sum()
                .sort_index()
            )

            labels = grouped.index.astype(str).tolist()
            values = grouped.values.tolist()

            return {
                "type": "line",
                "title": f"{main_metric} over time",
                "labels": labels,
                "values": values,
            }

    # 2. Category bar chart
    for col in cat_cols:
        unique_count = df[col].nunique()

        if unique_count <= 20:
            temp = df[[col, main_metric]].dropna()

            grouped = (
                temp.groupby(col)[main_metric]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            labels = grouped.index.astype(str).tolist()
            values = grouped.values.tolist()

            return {
                "type": "bar",
                "title": f"{main_metric} by {col}",
                "labels": labels,
                "values": values,
            }

    return None
