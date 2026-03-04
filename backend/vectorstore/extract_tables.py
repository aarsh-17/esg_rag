import camelot
import pandas as pd
import re
import os


PDF_PATH = "backend/data/Shell.pdf"
OUTPUT_FILE = "information_dense_tables.xlsx"


# -----------------------------
# Helper: detect numeric values
# -----------------------------
def is_number(val):
    if pd.isna(val):
        return False

    val = str(val).strip()

    # Remove commas and percent signs
    val = val.replace(",", "").replace("%", "")

    # Remove units like mtpa, MWac, etc.
    val = re.sub(r"[a-zA-Z]+$", "", val).strip()

    return bool(re.match(r"^-?\d+(\.\d+)?$", val))


# -----------------------------
# Compute numeric density
# -----------------------------
def numeric_density(df):
    total_cells = df.size
    numeric_cells = 0

    for value in df.values.flatten():
        if is_number(value):
            numeric_cells += 1

    return numeric_cells / total_cells if total_cells > 0 else 0


# -----------------------------
# Remove obvious header/footer rows
# -----------------------------
def remove_noise_rows(df):
    noise_patterns = [
        "Shell Sustainability Report",
        "Our performance data",
        "Sustainability at",
        "Achieving net-zero",
        "Respecting nature",
        "Powering lives",
        "Security [A]",
        "Health",
        "Note:"
    ]

    mask = df.apply(
        lambda row: any(
            pattern.lower() in str(cell).lower()
            for pattern in noise_patterns
            for cell in row
        ),
        axis=1
    )

    return df[~mask]


# -----------------------------
# Extract information-dense tables
# -----------------------------
def extract_dense_tables(pdf_path):

    print("Reading PDF...")

    tables = camelot.read_pdf(
        pdf_path,
        pages="all",
        flavor="stream"
    )

    print("Total detected tables:", tables.n)

    dense_tables = []

    for i, table in enumerate(tables):

        df = table.df

        rows, cols = df.shape

        # Basic structural filter
        if rows < 6 or cols < 4:
            continue

        df = remove_noise_rows(df)

        density = numeric_density(df)

        # Numeric density threshold (adjustable)
        if density >= 0.15:
            dense_tables.append((i, df, density))

    return dense_tables

def remove_narrative_rows(df):

    cleaned_rows = []

    for _, row in df.iterrows():

        row_values = [str(cell).strip() for cell in row if str(cell).strip()]

        # Skip rows with only 1 long text cell
        if len(row_values) == 1 and len(row_values[0]) > 120:
            continue

        cleaned_rows.append(row)

    return pd.DataFrame(cleaned_rows, columns=df.columns)

def remove_section_headers(df):

    cleaned_rows = []

    for _, row in df.iterrows():

        row_text = " ".join(str(cell) for cell in row)

        # If no % and no number → likely header
        if "%" not in row_text and not re.search(r"\d", row_text):
            continue

        cleaned_rows.append(row)

    return pd.DataFrame(cleaned_rows, columns=df.columns)


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":

    dense_tables = extract_dense_tables(PDF_PATH)

    cleaned_tables = []

    for idx, df, density in dense_tables:
        df_clean = remove_narrative_rows(df)
        df_clean = remove_section_headers(df_clean)
        new_density = numeric_density(df_clean)

        cleaned_tables.append((idx, df_clean, new_density))

    dense_tables = cleaned_tables

    print("Dense tables found:", len(dense_tables))

    if not dense_tables:
        print("No tables to save.")
    else:
        dense_tables = sorted(dense_tables, key=lambda x: x[2], reverse=True)

        with pd.ExcelWriter(OUTPUT_FILE) as writer:
            for idx, df, density in dense_tables:
                sheet_name = f"table_{idx}_d{round(density,2)}"
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

        print(f"Saved dense tables to {OUTPUT_FILE}")