
import os

filepath = 'index.html'

with open(filepath, 'r') as f:
    lines = f.readlines()

new_lines = []
css_inserted = False
js_var_inserted = False
js_logic_inserted = False
js_init_inserted = False

css_block = """
        /* HACKER MODE (SECRET) */
        body.hacker-mode {
            --pink-main: #00ff41;
            --pink-soft: #0d0208;
            --blue-main: #008f11;
            --blue-soft: #003b00;
            --white-soft: #000000;
            --dark-text: #00ff41;
            --muted: #008f11;
            background: #000 !important;
            font-family: 'Courier New', monospace !important;
        }
        body.hacker-mode .app-shell {
            background: #000 !important;
            border-color: #00ff41 !important;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
        }
        body.hacker-mode * {
            border-radius: 0 !important;
        }
        body.hacker-mode .welcome-title,
        body.hacker-mode .main-title {
            text-shadow: 0 0 5px #00ff41;
        }
"""

js_var_block = """            const projectNameEl = document.querySelector('.project-name');
"""

js_logic_block = """            // Secret Hacker Mode Trigger
            let hackerClickCount = 0;
            let hackerClickTimer = null;

            if (projectNameEl) {
                projectNameEl.style.cursor = 'pointer';
                projectNameEl.style.userSelect = 'none';

                projectNameEl.addEventListener('click', () => {
                    hackerClickCount++;

                    if (hackerClickTimer) clearTimeout(hackerClickTimer);

                    hackerClickTimer = setTimeout(() => {
                        hackerClickCount = 0;
                    }, 2000);

                    if (hackerClickCount >= 5) {
                        document.body.classList.toggle('hacker-mode');
                        const isHacker = document.body.classList.contains('hacker-mode');
                        localStorage.setItem('projectParkerHackerMode', isHacker);
                        alert(isHacker ? 'SYSTEM BREACHED. HACKER MODE ACTIVATED.' : 'SYSTEM RESTORED.');
                        hackerClickCount = 0;
                    }
                });
            }

"""

js_init_block = """                // Check stored hacker mode
                if (localStorage.getItem('projectParkerHackerMode') === 'true') {
                    document.body.classList.add('hacker-mode');
                }
"""

for line in lines:
    # CSS Insertion
    if not css_inserted and line.strip() == '</style>':
        new_lines.append(css_block)
        css_inserted = True

    new_lines.append(line)

    # JS Variable Insertion
    if not js_var_inserted and "const linksButtonsContainer = document.getElementById('links-buttons-container');" in line:
        new_lines.append(js_var_block)
        js_var_inserted = True

    # JS Logic Insertion
    if not js_logic_inserted and line.strip() == '// Init':
        # Insert before // Init, so we pop the last line (which is // Init), append block, then append // Init
        new_lines.pop()
        new_lines.append(js_logic_block)
        new_lines.append(line)
        js_logic_inserted = True

    # JS Init Check Insertion
    if not js_init_inserted and "loadLinkStatus(); // Load visited links" in line:
        new_lines.append(js_init_block)
        js_init_inserted = True

with open(filepath, 'w') as f:
    f.writelines(new_lines)

print("Modifications applied successfully.")
