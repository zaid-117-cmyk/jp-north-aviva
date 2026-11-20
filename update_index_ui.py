with open(r"D:\floor plans\jp-aviva-3d\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update brand-title to add id="brand-title-card"
html = html.replace(
    '<div class="brand-title">',
    '<div class="brand-title" id="brand-title-card">',
    1
)

# 2. Update progress-card to add id="progress-card-pill"
html = html.replace(
    '<div class="progress-card">',
    '<div class="progress-card" id="progress-card-pill">',
    1
)

# 3. Replace room-interaction-container with complete interactive pitch spec card
old_interaction = html[html.find('<div id="room-interaction-container"'):html.find('<!-- External Libraries: Lenis & GSAP ScrollTrigger -->')]

new_interaction = """<div id="room-interaction-container" class="room-interaction-container">
        <!-- Minimalist '+' Button (fades in via GSAP only at eye-level photo stops) -->
        <button id="room-plus-btn" class="room-plus-btn" aria-label="Explore Room Specifications" title="Click to View Architectural Specifications">
            <span class="plus-beacon"></span>
            <span id="plus-icon" class="plus-icon">+</span>
            <span class="plus-label">PITCH SPECS</span>
        </button>

        <!-- Frosted Glass Architectural Spec Card -->
        <div id="room-card" class="room-card" style="display: none;" role="dialog" aria-modal="true" aria-labelledby="rc-name">
            <div class="rc-header">
                <div class="rc-tag-group">
                    <span id="rc-zone" class="rc-zone-tag">ZONE 01 · SOCIAL &amp; ENTERTAINMENT</span>
                    <span class="rc-spec-badge">ARCHITECTURAL SPECIFICATION</span>
                </div>
                <button id="room-card-close" class="rc-close-btn" aria-label="Close specification card">&times;</button>
            </div>

            <h2 id="rc-name" class="rc-title">Living &amp; Dining Sanctuary</h2>
            <p id="rc-subtitle" class="rc-subtitle">JP North Aviva · Wing A · Type R1 · MahaRERA Approved</p>

            <!-- Interactive Unit Toggle inside the card -->
            <div class="rc-unit-toggle-wrapper">
                <span class="rc-toggle-label">DISPLAY UNITS</span>
                <div class="rc-segmented-control" role="group" aria-label="Specification Unit Toggle">
                    <button type="button" class="rc-unit-btn active" data-unit="metric" onclick="window.setGlobalUnit('metric')">METRIC (m / m&sup2;)</button>
                    <button type="button" class="rc-unit-btn" data-unit="imperial" onclick="window.setGlobalUnit('imperial')">IMPERIAL (ft / sq.ft)</button>
                </div>
            </div>

            <div class="rc-metrics-grid">
                <div class="rc-metric-box">
                    <span class="rc-label">DIMENSIONS</span>
                    <div id="rc-dim-val" class="rc-metric-val">2.75m &times; 3.95m</div>
                    <div id="rc-dim-alt" class="rc-metric-sub">9'0" &times; 13'0"</div>
                </div>
                <div class="rc-metric-box">
                    <span class="rc-label">RERA CARPET AREA</span>
                    <div id="rc-area-val" class="rc-metric-val">10.86 m&sup2;</div>
                    <div id="rc-area-alt" class="rc-metric-sub">117 sq.ft</div>
                </div>
                <div class="rc-metric-box rc-metric-full">
                    <span class="rc-label">CEILING CLEAR HEIGHT</span>
                    <div id="rc-height-val" class="rc-metric-val">2.85 m (9'4" Clear Slab-to-Slab)</div>
                </div>
            </div>

            <div class="rc-section">
                <span class="rc-section-title">FLOORING &amp; FINISH SPECIFICATIONS</span>
                <p id="rc-finishes" class="rc-val-text">High-gloss Italian Calacatta vitrified tiles (800&times;1600mm), "Whispering Smoke" (#ECE8E1) matte acrylic emulsion with 100mm shadow-gap baseboard, and Scandinavian Oak joinery.</p>
            </div>

            <div class="rc-section">
                <span class="rc-section-title">ELECTRICAL, HVAC &amp; AMENITIES</span>
                <p id="rc-amenities" class="rc-val-text">Inverter Split AC (24&deg;C digital display), 65" Ultra-Thin 4K OLED Smart TV with Ambilight backlighting, recessed 3000K architectural warm LED downlights.</p>
            </div>

            <div class="rc-section">
                <span class="rc-section-title">JP INFRA SALES PITCH HIGHLIGHTS</span>
                <ul id="rc-pitch-points" class="rc-pitch-list">
                    <li>Zero space wastage: maximizes usable carpet area under MahaRERA standards.</li>
                    <li>Direct seamless circulation into private North-facing enclosed balcony.</li>
                    <li>Large format porcelain floor tiles create expansive visual perception.</li>
                </ul>
            </div>
        </div>
    </div>

    """

html = html[:html.find('<div id="room-interaction-container"')] + new_interaction + html[html.find('<!-- External Libraries: Lenis & GSAP ScrollTrigger -->'):]

with open(r"D:\floor plans\jp-aviva-3d\index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully updated index.html with new architecture, IDs, and Spec Card markup")
