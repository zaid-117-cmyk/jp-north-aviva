with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

modal_html = """    <!-- Interactive Modal: Book a Private Site Visit -->
    <div id="modal-site-visit" class="interactive-modal-overlay" role="dialog" aria-modal="true" aria-labelledby="msv-title" aria-hidden="true">
        <div class="modal-card">
            <button type="button" class="modal-close-btn" onclick="window.closeModal('modal-site-visit')" aria-label="Close modal">&times;</button>
            <div class="modal-badge">JP NORTH AVIVA · WING A</div>
            <h2 id="msv-title" class="modal-title">Book a Private Site Visit</h2>
            <p class="modal-subtitle">Walk through the actual 27.96 Sq.M. (301 Sq.Ft.) 1 BHK show flat at North Garden City, Mira Road East. MahaRERA: P51700023940.</p>
            
            <form id="site-visit-form" onsubmit="window.submitBookingForm(event)" class="modal-form">
                <div class="form-group">
                    <label for="visitor-name">Full Name</label>
                    <input type="text" id="visitor-name" required placeholder="e.g. Rahul Sharma" class="modal-input">
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="visitor-phone">Phone Number</label>
                        <input type="tel" id="visitor-phone" required placeholder="+91 98765 43210" class="modal-input">
                    </div>
                    <div class="form-group">
                        <label for="visitor-date">Preferred Date</label>
                        <input type="date" id="visitor-date" required class="modal-input">
                    </div>
                </div>
                <button type="submit" class="modal-submit-btn">Confirm Private Site Visit</button>
            </form>

            <div id="booking-success-state" class="booking-success-state" style="display: none;">
                <div class="success-icon">OK</div>
                <h3>Visit Request Confirmed!</h3>
                <p>Thank you. A Senior JP Infra Relationship Executive will contact you within 30 minutes with gate pass details.</p>
                <button type="button" class="modal-done-btn" onclick="window.closeModal('modal-site-visit')">Close Window</button>
            </div>
        </div>
    </div>

    <!-- Interactive Modal: Download Floorplan Specs -->
    <div id="modal-floorplan-specs" class="interactive-modal-overlay" role="dialog" aria-modal="true" aria-labelledby="mfs-title" aria-hidden="true">
        <div class="modal-card modal-wide">
            <button type="button" class="modal-close-btn" onclick="window.closeModal('modal-floorplan-specs')" aria-label="Close modal">&times;</button>
            <div class="modal-badge">ARCHITECTURAL SPECIFICATION BREAKDOWN</div>
            <h2 id="mfs-title" class="modal-title">JP North Aviva · Floorplan Specs</h2>
            <p class="modal-subtitle">Wing A · Type R1 · Typical Floor (Flat A1 to A12) · MahaRERA: P51700023940</p>

            <div class="specs-table-container">
                <table class="specs-table">
                    <thead>
                        <tr>
                            <th>Zone Name</th>
                            <th>Metric (m)</th>
                            <th>Imperial (ft)</th>
                            <th>RERA Carpet</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Living &amp; Dining Sanctuary</td><td>2.75m &times; 3.95m</td><td>9'0" &times; 13'0"</td><td>10.86 m² [117 sq.ft]</td></tr>
                        <tr><td>Gourmet Kitchen Alcove</td><td>1.95m &times; 1.85m</td><td>6'5" &times; 6'1"</td><td>3.61 m² [39 sq.ft]</td></tr>
                        <tr><td>Bath &amp; W.C. Suite</td><td>1.15m &times; 1.30m</td><td>3'9" &times; 4'3"</td><td>1.50 m² [16 sq.ft]</td></tr>
                        <tr><td>Master Bedroom Suite</td><td>2.45m &times; 2.75m</td><td>8'0" &times; 9'0"</td><td>6.74 m² [73 sq.ft]</td></tr>
                        <tr><td>Enclosed Balcony Deck &amp; Utility</td><td>1.20m &times; 2.75m</td><td>3'11" &times; 9'0"</td><td>2.18 m² [23 sq.ft]</td></tr>
                        <tr><td>Cupboard Niche</td><td>0.60m &times; 2.15m</td><td>2'0" &times; 7'1"</td><td>1.29 m² [14 sq.ft]</td></tr>
                        <tr class="highlight-row"><td><strong>Total RERA Carpet Area</strong></td><td><strong>Clear Height: 2.85m</strong></td><td><strong>9'4" Slab Height</strong></td><td><strong>27.96 m² [301 sq.ft]</strong></td></tr>
                    </tbody>
                </table>
            </div>

            <div class="modal-action-row">
                <button type="button" class="modal-submit-btn" onclick="window.triggerDownloadAction()">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:8px;vertical-align:middle;"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
                    Download Official Sanctioned CAD Specifications (.txt)
                </button>
            </div>
        </div>
    </div>
"""

target = '    <!-- External Libraries: Lenis & GSAP ScrollTrigger -->'
assert target in html, 'Target in index.html not found'
html = html.replace(target, modal_html + '\n' + target)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('[OK] index.html modals injected successfully')
