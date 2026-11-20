# refine_stop2_and_stop7.py
with open(r"d:\floor plans\jp-aviva-3d\script.js", "r", encoding="utf-8") as f:
    code = f.read()

# Stop 2 (Living Room Hold)
old_stop2 = """// Leg 2A (16% to 26%): The Descent & Ink-to-Material Reveal
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.45,
    posY: 1.45,
    posZ: 0.85,
    targetX: -1.85,
    targetY: 1.05,
    targetZ: -0.45,
    duration: 0.10,
    ease: 'power2.inOut'
});
// Leg 2B (26% to 34%): The Hold (Eye-level Photo Stop at Y = 1.45m)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.45,
    posY: 1.45,
    posZ: 0.85,
    targetX: -1.85,
    targetY: 1.05,
    targetZ: -0.45,
    duration: 0.08,
    ease: 'none'
});"""

new_stop2 = """// Leg 2A (16% to 26%): The Descent & Ink-to-Material Reveal
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.85,
    posY: 1.45,
    posZ: 0.45,
    targetX: -1.90,
    targetY: 1.10,
    targetZ: -0.55,
    duration: 0.10,
    ease: 'power2.inOut'
});
// Leg 2B (26% to 34%): The Hold (Eye-level Photo Stop at Y = 1.45m)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.85,
    posY: 1.45,
    posZ: 0.45,
    targetX: -1.90,
    targetY: 1.10,
    targetZ: -0.55,
    duration: 0.08,
    ease: 'none'
});"""

if old_stop2 in code:
    code = code.replace(old_stop2, new_stop2, 1)
    print("Updated Stop 2 camera position cleanly into open living space.")
else:
    print("Warning: old_stop2 not found.")

# Stop 7 (Balcony Hold)
old_stop7 = """// Leg 5A (90% to 95%): The Descent onto Teak Deck & Golden Sunset Reveal
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: -2.60,
    sweepBalconyZ: -2.65,
    posX: -1.60,
    posY: 1.40,
    posZ: -1.85,
    targetX: -1.60,
    targetY: 1.10,
    targetZ: -2.85,
    duration: 0.05,
    ease: 'power2.inOut'
});
// Leg 5B (95% to 100%): The Hold (Sunset Photo Stop Finale framing lounge chair & sunset)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: -2.60,
    sweepBalconyZ: -2.65,
    posX: -1.60,
    posY: 1.40,
    posZ: -1.85,
    targetX: -1.60,
    targetY: 1.10,
    targetZ: -2.85,
    duration: 0.05,
    ease: 'none'
});"""

new_stop7 = """// Leg 5A (90% to 95%): The Descent onto Teak Deck & Golden Sunset Reveal
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: -2.60,
    sweepBalconyZ: -2.65,
    posX: -1.55,
    posY: 1.35,
    posZ: -1.75,
    targetX: -1.55,
    targetY: 0.88,
    targetZ: -2.60,
    duration: 0.05,
    ease: 'power2.inOut'
});
// Leg 5B (95% to 100%): The Hold (Sunset Photo Stop Finale framing lounge chair & sunset)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    sweepKitchenZ: 2.65,
    sweepBedroomZ: -2.60,
    sweepBalconyZ: -2.65,
    posX: -1.55,
    posY: 1.35,
    posZ: -1.75,
    targetX: -1.55,
    targetY: 0.88,
    targetZ: -2.60,
    duration: 0.05,
    ease: 'none'
});"""

if old_stop7 in code:
    code = code.replace(old_stop7, new_stop7, 1)
    print("Updated Stop 7 balcony camera position.")
else:
    print("Warning: old_stop7 not found.")

with open(r"d:\floor plans\jp-aviva-3d\script.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved script.js!")
