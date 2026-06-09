import json

with open('churn_model.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        for i, line in enumerate(source):
            if "open(OUTPUT_DIR / 'error_analysis.md', 'w')" in line:
                source[i] = line.replace("open(OUTPUT_DIR / 'error_analysis.md', 'w')", "open(OUTPUT_DIR / 'error_analysis.md', 'w', encoding='utf-8')")
        
        # also check metrics.json just in case
        for i, line in enumerate(source):
            if "open(OUTPUT_DIR / 'metrics.json', 'w')" in line:
                source[i] = line.replace("open(OUTPUT_DIR / 'metrics.json', 'w')", "open(OUTPUT_DIR / 'metrics.json', 'w', encoding='utf-8')")
                
        # also model_card.md
        for i, line in enumerate(source):
            if "open(OUTPUT_DIR / 'model_card.md', 'w')" in line:
                source[i] = line.replace("open(OUTPUT_DIR / 'model_card.md', 'w')", "open(OUTPUT_DIR / 'model_card.md', 'w', encoding='utf-8')")

with open('churn_model.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
print("Fixed encoding issues in notebook")
