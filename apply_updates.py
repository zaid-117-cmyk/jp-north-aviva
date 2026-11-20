import sys
import re

path = 'D:/floor plans/jp-aviva-3d/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# -------------------------------------------------------------
# 1. STOP 2: Living Room Camera Un-crop & Framing
# -------------------------------------------------------------
old_stop2 = '''// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary (Balanced architectural framing: TV Wall, Coffee Table, Sofa & Balcony)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.46,
    posZ: 1.95,
    targetX: 1.25,
    targetY: 1.10,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold (Flawless Balanced Composition: TV Wall, Marble Table, Boucle Sofa & Balcony Horizon)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.46,
    posZ: 1.95,
    targetX: 1.25,
    targetY: 1.10,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'none'
});'''

new_stop2 = '''// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary (Balanced architectural framing: Full OLED TV Wall, Coffee Table, Sofa & Balcony)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.46,
    posZ: 2.10,
    targetX: 0.98,
    targetY: 1.10,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold (Flawless Balanced Composition: Full OLED TV Wall, Marble Table, Boucle Sofa & Balcony Horizon)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.46,
    posZ: 2.10,
    targetX: 0.98,
    targetY: 1.10,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'none'
});'''

assert old_stop2 in content, 'Stop 2 pattern not found'
content = content.replace(old_stop2, new_stop2, 1)
print('[OK] 1. Stop 2 Living room camera updated (posZ: 2.10, targetX: 0.98)')

# -------------------------------------------------------------
# 2. SOFA BACKREST CUSHIONS LOWERED BY 3CM (0.63 -> 0.60)
# -------------------------------------------------------------
old_c1 = 'chaiseBackCushion.position.set(2.64, 0.63, -0.05);'
new_c1 = 'chaiseBackCushion.position.set(2.64, 0.60, -0.05);'
assert old_c1 in content, 'chaiseBackCushion pattern not found'
content = content.replace(old_c1, new_c1, 1)

old_c2 = 'bc.position.set(2.64, 0.63, cz);'
new_c2 = 'bc.position.set(2.64, 0.60, cz);'
assert old_c2 in content, 'bc cushion pattern not found'
content = content.replace(old_c2, new_c2, 1)
print('[OK] 2. Sofa backrest cushions lowered by 3cm to y = 0.60m')

# -------------------------------------------------------------
# 3. STAGE LABEL DELAYED TO 57%
# -------------------------------------------------------------
old_l1 = 'else if (p >= 0.44 && p < 0.52) stopIdx = 3;'
new_l1 = 'else if (p >= 0.44 && p < 0.57) stopIdx = 3;'
assert old_l1 in content, 'stopIdx 3 pattern not found'
content = content.replace(old_l1, new_l1, 1)

old_l2 = 'else if (p >= 0.58 && p < 0.66) stopIdx = 4;'
new_l2 = 'else if (p >= 0.57 && p < 0.66) stopIdx = 4;'
assert old_l2 in content, 'stopIdx 4 pattern not found'
content = content.replace(old_l2, new_l2, 1)

match = re.search(r'else if \(p < 0\.52\) labelElem\.textContent = [^\n]+', content)
assert match, 'labelElem pattern not found'
matched_text = match.group(0)
replaced_text = matched_text.replace('p < 0.52', 'p < 0.57')
content = content.replace(matched_text, replaced_text, 1)
print('[OK] 3. Stage label transition delayed from 52% to 57%')

# -------------------------------------------------------------
# 4. BATHROOM CAMERA PULLED BACK 12CM (-0.18 -> -0.30)
# -------------------------------------------------------------
old_stop4 = '''// --- STOP 4: 52% to 65% (05 - BATH & W.C. 1.15M x 1.30M Doorway Framing) ---
// Leg 4A1 (52% to 56%): Glide South out of Kitchen Portal into Central Passage Hub directly facing Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    posX: -1.14,
    posY: 1.50,
    posZ: -0.24,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold (Eye level posY = 1.45m, targetY = 1.18m)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.45,
    posZ: -0.18,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, WC & Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.45,
    posZ: -0.18,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.05,
    ease: 'none'
});'''

new_stop4 = '''// --- STOP 4: 52% to 65% (05 - BATH & W.C. 1.15M x 1.30M Doorway Framing) ---
// Leg 4A1 (52% to 56%): Glide South out of Kitchen Portal into Central Passage Hub directly facing Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    posX: -1.14,
    posY: 1.50,
    posZ: -0.30,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold (Pulled back 12cm to posZ = -0.30m to frame full WC)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.45,
    posZ: -0.30,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, Un-Cropped WC & Framed Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.45,
    posZ: -0.30,
    targetX: -1.14,
    targetY: 1.18,
    targetZ: 1.38,
    duration: 0.05,
    ease: 'none'
});'''

assert old_stop4 in content, 'Stop 4 pattern not found'
content = content.replace(old_stop4, new_stop4, 1)
print('[OK] 4. Bathroom camera pulled back 12cm (posZ: -0.30m)')

# Save back to file
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nALL UPDATES SUCCESSFULLY WRITTEN TO SCRIPT.JS!')
