# update_photo_stop_framing.py
with open(r"d:\floor plans\jp-aviva-3d\script.js", "r", encoding="utf-8") as f:
    code = f.read()

# Refine Stop 2 (Living Hold)
code = code.replace(
"""// Leg 2A (16% to 26%): The Descent & Ink-to-Material Reveal
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.40,
    posY: 1.50,
    posZ: 0.60,
    targetX: -1.95,
    targetY: 1.35,
    targetZ: -0.45,
    duration: 0.10,
    ease: 'power2.inOut'
});
// Leg 2B (26% to 34%): The Hold (Eye-level Photo Stop at Y = 1.50m)
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: -1.65,
    posX: -0.40,
    posY: 1.50,
    posZ: 0.60,
    targetX: -1.95,
    targetY: 1.35,
    targetZ: -0.45,
    duration: 0.08,
    ease: 'none'
});""",
"""// Leg 2A (16% to 26%): The Descent & Ink-to-Material Reveal
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
)

# Refine Stop 7 (Balcony Hold)
code = code.replace(
"""// Leg 5A (90% to 95%): The Descent onto Teak Deck & Golden Sunset Reveal
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
    targetY: 0.80,
    targetZ: -2.75,
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
    targetY: 0.80,
    targetZ: -2.75,
    duration: 0.05,
    ease: 'none'
});""",
"""// Leg 5A (90% to 95%): The Descent onto Teak Deck & Golden Sunset Reveal
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
)

with open(r"d:\floor plans\jp-aviva-3d\script.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated photo stop framing successfully!")
