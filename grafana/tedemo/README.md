# SVGTE - Interactive SVG Dashboard

**Python-generated interactive SVG dashboard** for monitoring and controlling a dual-fan ventilation system with real-time gauges, status indicators, and animated effects.

## Features

| Component | Details |
|-----------|----------|
| **Dual Fans** | Animated rotating blades, operating hours counter |
| **Pressure Gauge** | 0-500 Pa, color-coded segments (red/yellow/green), low pressure warning |
| **RPM Gauge** | 0-4000 RPM semi-circle, dynamic indicator |
| **Status Indicators** | System health, fuse status, relay feedback |
| **Animations** | Rotating fans, exhaust particles, starfield background |
| **Interactive** | Click to toggle fans, cycle values, test configurations |

## Quick Start

```powershell
# Generate SVG
python generate\generate_svg.py

# View in browser
open te.svg  # or any modern web browser
```

Output is **fully self-contained** with embedded CSS and JavaScript.

## Architecture

```
generate_svg.py          → Python creates all SVG elements
                            ↓
                           defs.xml (CSS styles)
                           js/init.js (update functions)
                           js/render.js (data loading)
                            ↓
                          te.svg (output)
```

**Python**: Structure & elements | **JavaScript**: Updates & interactions

## File Structure

```
generate/
├── generate_svg.py      # SVG generator
├── js/
│   ├── init.js         # Update functions
│   └── render.js       # Data rendering
└── style/
    └── defs.xml        # Styles & gradients
```

## Development

| File | Edit for |
|------|----------|
| `generate_svg.py` | Add elements, change layout |
| `style/defs.xml` | Visual styles, animations |
| `js/init.js` | Update logic |
| `js/render.js` | Data source integration |

## Data Integration

**InfluxDB fields**: `Fan1_on`, `Fan2_on`, `Fan_Speed`, `Pressure_Sensor`, operational hours, status flags, etc.

See `DOCUMENTATION.md` for full InfluxDB query.

## Dependencies

- Python 3.10+ (stdlib only)
- Modern browser (SVG + CSS animations)
- SVG.js (runtime)

## Status Colors

🟢 Green = Active/OK | 🔴 Red = Error | ⚫ Gray = Disabled/Off
