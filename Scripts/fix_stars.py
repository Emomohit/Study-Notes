import re

target_file = "generate_pdf_dbms_units1_2.py"

with open(target_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for idx, line in enumerate(lines):
    line_num = idx + 1
    # Bypass canvas constructor lines to preserve *args and **kwargs
    if line_num in [32, 33]:
        new_lines.append(line)
        continue
    
    # Replace ** with alternating <b> and </b> using a list container to count
    if "**" in line:
        count = [0]
        def repl(match):
            count[0] += 1
            return "<b>" if count[0] % 2 == 1 else "</b>"
        
        line_replaced = re.sub(r"\*\*", repl, line)
        new_lines.append(line_replaced)
    else:
        new_lines.append(line)

with open(target_file, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Successfully replaced double asterisks with <b> and </b> in text strings!")
