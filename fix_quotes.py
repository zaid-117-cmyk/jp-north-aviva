import re

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'"10\'6" × 13\'0""', '"10\'6\\\" × 13\'0\\\""', text)
text = re.sub(r'"8\'0" × 9\'0""', '"8\'0\\\" × 9\'0\\\""', text)
text = re.sub(r'"6\'5" × 6\'1""', '"6\'5\\\" × 6\'1\\\""', text)
text = re.sub(r'"7\'1" × 4\'3""', '"7\'1\\\" × 4\'3\\\""', text)
text = re.sub(r'"3\'11" × 13\'0""', '"3\'11\\\" × 13\'0\\\""', text)
text = re.sub(r'"3\'9" × 4\'9""', '"3\'9\\\" × 4\'9\\\""', text)

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully fixed quotes in script.js')
