import os
import re
from collections import defaultdict

def degiskenleri_bul(dizin):
    sabit_regex = re.compile(r'([A-Z_][A-Z0-9_]*)\s*=')
    model_field_regex = re.compile(r'^\s*(\w+)\s*=\s*models\.\w+Field')
    bulunanlar = defaultdict(list)

    for root, _, files in os.walk(dizin):
        if "migrations" in root:
            continue  # migrations klasörünü atla
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    for satir in f:
                        sabit = sabit_regex.search(satir)
                        if sabit:
                            bulunanlar[path].append(sabit.group(1))
                        else:
                            model_field = model_field_regex.match(satir)
                            if model_field:
                                bulunanlar[path].append(model_field.group(1))

    for dosya, degiskenler in bulunanlar.items():
        for degisken in degiskenler:
            print(f"{dosya}: {degisken}")

degiskenleri_bul('apps')
