with open('D:/floor plans/jp-aviva-3d/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(// (?:Leg|--- STOP)[\s\S]*?ease:\s*[\'\"][\w\.]+[\'\"]\s*\n\}\);)', text)
for m in matches:
    lines = m.splitlines()
    title = lines[0]
    pos = [l.strip() for l in lines if any(k in l for k in ['posX', 'posZ', 'posY', 'duration', 'fov'])]
    tgt = [l.strip() for l in lines if 'target' in l]
    print(title)
    print('   ', ' | '.join(pos))
    print('   ', ' | '.join(tgt))
