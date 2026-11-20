with open(r'D:\floor plans\jp-aviva-3d\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '<span>Spatial Timeline</span>'
replacement = '<span id="active-room-label">Spatial Timeline</span>'

if target in html:
    html = html.replace(target, replacement, 1)
    with open(r'D:\floor plans\jp-aviva-3d\index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Updated index.html successfully')
else:
    print('Target not found or already replaced')

with open(r'D:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update updateUI() in script.js
old_update_ui = """function updateUI() {
    const pct = Math.round(camState.progress * 100);
    const pElem = document.getElementById('progress-percent');
    if (pElem) pElem.textContent = `${pct}%`;
    const bElem = document.getElementById('progress-bar-fill');
    if (bElem) bElem.style.width = `${pct}%`;
}"""

new_update_ui = """function updateUI() {
    const pct = Math.round(camState.progress * 100);
    const pElem = document.getElementById('progress-percent');
    if (pElem) pElem.textContent = `${pct}%`;
    const bElem = document.getElementById('progress-bar-fill');
    if (bElem) bElem.style.width = `${pct}%`;
    const labelElem = document.getElementById('active-room-label');
    if (labelElem) {
        const p = camState.progress;
        if (p < 0.08) labelElem.textContent = '01 · Blueprint Plan Sheet (1:50)';
        else if (p < 0.16) labelElem.textContent = '02 · Walls Rise & Front Door Opens';
        else if (p < 0.28) labelElem.textContent = '03 · Living Sanctuary (2.75m × 3.95m)';
        else if (p < 0.42) labelElem.textContent = '04 · Kitchen Alcove (1.95m × 1.85m)';
        else if (p < 0.56) labelElem.textContent = '05 · Designer Bath Suite (1.15m × 1.30m)';
        else if (p < 0.70) labelElem.textContent = '06 · Master Bedroom Suite (2.45m × 2.75m)';
        else if (p < 0.90) labelElem.textContent = '07 · Balcony Deck (1.20m × 2.75m)';
        else labelElem.textContent = '08 · Mumbai Golden Sunset Finale';
    }
}"""

if old_update_ui in js:
    js = js.replace(old_update_ui, new_update_ui, 1)
    print('Updated updateUI in script.js')
else:
    print('old_update_ui not matched')

# Update applyProgressToScene in script.js to call updateUI and checkPhotoStop
old_apply_end = """    skyBillboard.visible = (camState.clipHeight > 1.35);
    ssaoPass.enabled = (camState.clipHeight > 1.30);
    composer.render();
};"""

new_apply_end = """    skyBillboard.visible = (camState.clipHeight > 1.35);
    ssaoPass.enabled = (camState.clipHeight > 1.30);
    updateUI();
    checkPhotoStop(p);
    composer.render();
};"""

if old_apply_end in js:
    js = js.replace(old_apply_end, new_apply_end, 1)
    print('Updated applyProgressToScene in script.js')
else:
    print('old_apply_end not matched')

with open(r'D:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('Finished updating script.js')
