import re

target_file = "generate_pdf_dbms_units1_2.py"

with open(target_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("--- LINES WITH ASTERISKS ---")
for idx, line in enumerate(lines):
    line_num = idx + 1
    if "*" in line:
        print(f"Line {line_num}: {line.strip()}")
