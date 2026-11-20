with open(r'd:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace sliding balcony door
text = text.replace('const [sbX1, sbY] = toCanvas(-2.55, -1.75);', 'const [sliderX1, sliderY] = toCanvas(-2.55, -1.75);')
text = text.replace('const [sbX2] = toCanvas(-0.35, -1.75);', 'const [sliderX2] = toCanvas(-0.35, -1.75);')
text = text.replace('ctx.moveTo(sbX1, sbY - 4); ctx.lineTo(sbX1 + (sbX2 - sbX1) * 0.55, sbY - 4);', 'ctx.moveTo(sliderX1, sliderY - 4); ctx.lineTo(sliderX1 + (sliderX2 - sliderX1) * 0.55, sliderY - 4);')
text = text.replace('ctx.moveTo(sbX1 + (sbX2 - sbX1) * 0.45, sbY + 4); ctx.lineTo(sbX2, sbY + 4);', 'ctx.moveTo(sliderX1 + (sliderX2 - sliderX1) * 0.45, sliderY + 4); ctx.lineTo(sliderX2, sliderY + 4);')

# Replace scale bar
text = text.replace('const sbX = size * 0.12, sbY = bBarY + 12;', 'const scaleBarX = size * 0.12, scaleBarY = bBarY + 12;')
text = text.replace("ctx.fillText('SCALE 1:50', sbX, sbY - 18);", "ctx.fillText('SCALE 1:50', scaleBarX, scaleBarY - 18);")
text = text.replace('ctx.moveTo(sbX, sbY); ctx.lineTo(sbX + 160, sbY);', 'ctx.moveTo(scaleBarX, scaleBarY); ctx.lineTo(scaleBarX + 160, scaleBarY);')
text = text.replace('const tx = sbX + i * (160 / 3);', 'const tx = scaleBarX + i * (160 / 3);')
text = text.replace('ctx.beginPath(); ctx.moveTo(tx, sbY - 5); ctx.lineTo(tx, sbY + 5); ctx.stroke();', 'ctx.beginPath(); ctx.moveTo(tx, scaleBarY - 5); ctx.lineTo(tx, scaleBarY + 5); ctx.stroke();')
text = text.replace('ctx.fillText(`${i}m`, tx - 6, sbY + 18);', 'ctx.fillText(`${i}m`, tx - 6, scaleBarY + 18);')

with open(r'd:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully resolved sbY identifier clash!')
