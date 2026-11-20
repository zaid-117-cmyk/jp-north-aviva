import os

BASE_DIR = r"D:\floor plans\jp-aviva-3d"
STYLE_PATH = os.path.join(BASE_DIR, "style.css")
SCRIPT_PATH = os.path.join(BASE_DIR, "script.js")

# 1. Update style.css
# Let's read style.css
with open(STYLE_PATH, "r", encoding="utf-8") as f:
    css_content = f.read()

# We will replace .brand-title, .progress-card, .progress-header, .room-plus-btn, .room-card etc.
# Let's inspect where .brand-title starts
brand_title_new_css = """
/* =========================================================
   TOP NAVIGATION HEADER WITH DYNAMIC CONTRAST
   ========================================================= */
.brand-title {
    display: flex;
    flex-direction: column;
    padding: 14px 20px;
    border-radius: 16px;
    background: rgba(15, 15, 18, 0.72);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    max-width: 480px;
}

.badge-checkpoint {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(212, 163, 89, 0.22);
    border: 1px solid #D4A359;
    color: #F5CF8E;
    font-size: 9.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    padding: 3px 10px;
    border-radius: 20px;
    width: fit-content;
    margin-bottom: 8px;
    transition: all 0.3s ease;
}

.brand-title h1 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.85rem;
    font-weight: 500;
    letter-spacing: 0.5px;
    color: #F8F9FA;
    line-height: 1.15;
    transition: color 0.3s ease;
}

.brand-title p {
    font-size: 0.78rem;
    color: rgba(248, 249, 250, 0.75);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 5px;
    font-weight: 500;
    transition: color 0.3s ease;
}

/* Dynamic Blueprint Mode (0–12% progress) */
.brand-title.blueprint-mode {
    background: rgba(248, 246, 240, 0.90);
    border: 1px solid rgba(22, 24, 27, 0.14);
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
}

.brand-title.blueprint-mode h1 {
    color: var(--ink-black);
}

.brand-title.blueprint-mode p {
    color: #4A4E54;
}

.brand-title.blueprint-mode .badge-checkpoint {
    background: rgba(212, 163, 89, 0.15);
    border-color: var(--gold);
    color: var(--gold-dark);
}
"""

progress_new_css = """
/* =========================================================
   BOTTOM PROGRESS BAR PILL (NO COLLISION, TABULAR-NUMS)
   ========================================================= */
.progress-card {
    background: rgba(15, 15, 18, 0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 16px;
    padding: 14px 20px;
    min-width: 380px;
    max-width: 460px;
    box-shadow: 0 10px 32px rgba(0, 0, 0, 0.35);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.progress-card.blueprint-mode {
    background: rgba(248, 246, 240, 0.92);
    border: 1px solid rgba(22, 24, 27, 0.14);
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: rgba(248, 249, 250, 0.75);
    margin-bottom: 10px;
    font-weight: 600;
}

.progress-card.blueprint-mode .progress-header {
    color: var(--ink-dim);
}

#active-room-label {
    flex: 1 1 auto;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 0.75rem;
    font-weight: 600;
    color: #F8F9FA;
}

.progress-card.blueprint-mode #active-room-label {
    color: var(--ink-black);
}

#progress-percent {
    flex: 0 0 auto;
    font-variant-numeric: tabular-nums;
    font-feature-settings: "tnum";
    font-family: 'Plus Jakarta Sans', monospace, sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    color: #D4A359;
    min-width: 46px;
    text-align: right;
}

.progress-card.blueprint-mode #progress-percent {
    color: var(--gold-dark);
}

.progress-bar-bg {
    width: 100%;
    height: 5px;
    background: rgba(255, 255, 255, 0.14);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 8px;
}

.progress-card.blueprint-mode .progress-bar-bg {
    background: rgba(22, 24, 27, 0.10);
}

.progress-bar-fill {
    width: 0%;
    height: 100%;
    background: linear-gradient(90deg, #D4A359, #F5CF8E);
    border-radius: 4px;
    transition: width 0.05s linear;
}

.progress-card.blueprint-mode .progress-bar-fill {
    background: linear-gradient(90deg, #D4A359, #8C6226);
}

.scroll-hint {
    font-size: 0.7rem;
    color: rgba(248, 249, 250, 0.65);
    display: flex;
    align-items: center;
    gap: 6px;
}

.progress-card.blueprint-mode .scroll-hint {
    color: var(--ink-dim);
}

.scroll-hint kbd {
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 2px 7px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.72rem;
    color: #F8F9FA;
}

.progress-card.blueprint-mode .scroll-hint kbd {
    background: rgba(22, 24, 27, 0.06);
    border-color: rgba(22, 24, 27, 0.14);
    color: var(--ink-black);
}
"""

hotspots_new_css = """
/* =========================================================
   INTERACTIVE PITCH HOTSPOTS & SLEEK SPEC CARD
   ========================================================= */
.room-interaction-container {
    position: fixed;
    bottom: 32px;
    right: 36px;
    z-index: 100;
    pointer-events: none;
}

.room-plus-btn {
    pointer-events: auto;
    height: 46px;
    padding: 0 18px 0 14px;
    border-radius: 23px;
    background: rgba(15, 15, 18, 0.82);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1.5px solid rgba(212, 163, 89, 0.55);
    color: #F8F9FA;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 0 16px rgba(212, 163, 89, 0.25);
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    opacity: 0;
    transform: translateY(14px) scale(0.9);
    user-select: none;
}

.room-plus-btn.visible {
    opacity: 1;
    transform: translateY(0) scale(1);
    pointer-events: auto;
}

.room-plus-btn:hover {
    background: rgba(22, 24, 27, 0.95);
    border-color: #D4A359;
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.5), 0 0 24px rgba(212, 163, 89, 0.45);
}

.room-plus-btn.active {
    border-color: #F5CF8E;
    background: rgba(212, 163, 89, 0.25);
}

.room-plus-btn.active .plus-icon {
    transform: rotate(45deg);
}

.plus-beacon {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #D4A359;
    box-shadow: 0 0 0 0 rgba(212, 163, 89, 0.8);
    animation: pulse-beacon 2s infinite cubic-bezier(0.45, 0, 0.2, 1);
}

@keyframes pulse-beacon {
    0% {
        box-shadow: 0 0 0 0 rgba(212, 163, 89, 0.85);
    }
    70% {
        box-shadow: 0 0 0 12px rgba(212, 163, 89, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(212, 163, 89, 0);
    }
}

.plus-icon {
    font-size: 20px;
    font-weight: 300;
    line-height: 1;
    color: #D4A359;
    transition: transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.plus-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #F8F9FA;
}

/* Frosted Glass Architectural Spec Card */
.room-card {
    pointer-events: none;
    position: fixed;
    bottom: 92px;
    right: 36px;
    width: 440px;
    max-width: calc(100vw - 48px);
    max-height: calc(100vh - 130px);
    overflow-y: auto;
    background: rgba(14, 16, 20, 0.88);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid rgba(212, 163, 89, 0.45);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(255, 255, 255, 0.08) inset;
    z-index: 99;
    opacity: 0;
    transform: translateY(20px) scale(0.96);
    transition: opacity 0.32s cubic-bezier(0.16, 1, 0.3, 1), transform 0.32s cubic-bezier(0.16, 1, 0.3, 1);
}

.room-card.open {
    opacity: 1;
    transform: translateY(0) scale(1);
    pointer-events: auto;
}

.rc-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
}

.rc-tag-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.rc-zone-tag {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #D4A359;
}

.rc-designer-badge {
    display: inline-block;
    font-size: 8.5px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    background: rgba(212, 163, 89, 0.18);
    border: 1px solid rgba(212, 163, 89, 0.45);
    color: #F5CF8E;
    padding: 2px 8px;
    border-radius: 10px;
    width: fit-content;
}

.rc-header-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}

.rc-unit-toggle {
    display: inline-flex;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 14px;
    padding: 2px;
    gap: 2px;
}

.rc-unit-btn {
    background: transparent;
    border: none;
    outline: none;
    padding: 3px 8px;
    border-radius: 12px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.8px;
    color: rgba(248, 249, 250, 0.65);
    cursor: pointer;
    transition: all 0.2s ease;
}

.rc-unit-btn:hover {
    color: #F8F9FA;
}

.rc-unit-btn.active {
    background: #D4A359;
    color: #141619;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.rc-close-btn {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    outline: none;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    font-size: 18px;
    line-height: 1;
    color: rgba(248, 249, 250, 0.7);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
}

.rc-close-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    color: #FFFFFF;
}

.rc-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: #F8F9FA;
    line-height: 1.2;
    margin-top: 8px;
}

.rc-subtitle {
    font-size: 9.5px;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: rgba(248, 249, 250, 0.55);
    margin-top: 3px;
    font-weight: 600;
}

.rc-divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, rgba(212, 163, 89, 0.5), rgba(255, 255, 255, 0.06));
    margin: 14px 0;
}

.rc-section {
    margin-bottom: 14px;
}

.rc-label {
    display: block;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #D4A359;
    margin-bottom: 5px;
}

.rc-val-text {
    font-size: 12px;
    line-height: 1.55;
    color: rgba(248, 249, 250, 0.88);
    font-weight: 400;
}

/* Metrics Grid: Dimensions & Floor Area */
.rc-metrics-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 6px;
}

.rc-metric-box {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 12px;
    padding: 10px 12px;
}

.rc-metric-box.full-width {
    grid-column: 1 / -1;
}

.rc-metric-val {
    font-size: 14px;
    font-weight: 700;
    color: #F8F9FA;
    letter-spacing: 0.2px;
    font-variant-numeric: tabular-nums;
}

.rc-metric-alt {
    font-size: 10.5px;
    color: rgba(248, 249, 250, 0.55);
    margin-top: 2px;
    font-style: italic;
    font-variant-numeric: tabular-nums;
}

.rc-pitch-list {
    margin: 0;
    padding-left: 18px;
    font-size: 12px;
    line-height: 1.55;
    color: rgba(248, 249, 250, 0.88);
}

.rc-pitch-list li {
    margin-bottom: 4px;
}

.rc-pitch-list li::marker {
    color: #D4A359;
}

/* Scrollbar for Room Card */
.room-card::-webkit-scrollbar {
    width: 5px;
}

.room-card::-webkit-scrollbar-thumb {
    background: rgba(212, 163, 89, 0.3);
    border-radius: 4px;
}

.room-card::-webkit-scrollbar-thumb:hover {
    background: rgba(212, 163, 89, 0.6);
}
"""

# Let's cleanly construct the entire style.css
# We can read the base styles (lines 1 to 81)
idx_brand = css_content.find(".brand-title {")
idx_nav_controls = css_content.find("/* Navigation Controls Group */")
idx_progress = css_content.find("/* Scroll Progress Card */")
idx_room_card = css_content.find("/* =========================================================")
idx_room_card_actual = css_content.find("INTERACTIVE ROOM CARD", idx_progress)
if idx_room_card_actual != -1:
    idx_section_start = css_content.rfind("/* =", 0, idx_room_card_actual)
else:
    idx_section_start = css_content.find(".room-interaction-container")

part1 = css_content[:idx_brand]
part2 = css_content[idx_nav_controls:idx_progress]
part_responsive = css_content[css_content.find("/* Responsive adjustments */"):]

full_new_css = part1 + brand_title_new_css.strip() + "\n\n" + part2 + progress_new_css.strip() + "\n\n" + hotspots_new_css.strip() + "\n\n" + part_responsive

with open(STYLE_PATH, "w", encoding="utf-8") as f:
    f.write(full_new_css)

print("Updated style.css successfully!")
