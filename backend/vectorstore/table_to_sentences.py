import pandas as pd
import re
import json
import os


def is_year(col):
    return re.fullmatch(r"20\d{2}", col) is not None


def clean_number(value):
    if isinstance(value, str):
        value = value.replace(",", "").strip()
    try:
        return float(value)
    except:
        return None


def process_sheet(df, sheet_name):
    df.columns = df.columns.astype(str).str.strip()

    # Skip sheet if no Unit column
    unit_col = next((col for col in df.columns if col.lower() == "unit"), None)
    if not unit_col:
        return []

    # Detect year columns
    year_cols = [col for col in df.columns if is_year(col)]
    if not year_cols:
        return []

    # Assume first column is metric
    metric_col = df.columns[0]

    facts = []

    for _, row in df.iterrows():
        metric = str(row[metric_col]).strip()

        if metric.lower() == "nan" or metric == "":
            continue

        unit = str(row[unit_col]).strip()

        for year in year_cols:
            value = clean_number(row[year])

            if value is None:
                continue

            facts.append({
                "sheet": sheet_name,
                "metric": metric,
                "year": year,
                "value": value,
                "unit": unit,
                "text": f"In {year}, {metric} was {value} {unit}."
            })

    return facts


def process_excel_file(file_path, output_json_path):
    excel_file = pd.ExcelFile(file_path)

    all_facts = []

    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)
        sheet_facts = process_sheet(df, sheet_name)

        if sheet_facts:
            all_facts.extend(sheet_facts)
        else:
            print(f"Skipping sheet '{sheet_name}' (no valid unit-based table found).")

    # Save to JSON
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(all_facts, f, indent=2)

    print(f"\nSaved {len(all_facts)} facts to {output_json_path}")


if __name__ == "__main__":
    input_file = "information_dense_tables.xlsx"
    output_file = "structured_tables.json"

    process_excel_file(input_file, output_file)