# SVG Dashboard Documentation

**Technical reference for the dual-fan ventilation monitoring dashboard.**

---

## Components

### Gauges

#### Pressure (0-500 Pa)
| Segment | Range | Color |
|---------|-------|-------|
| Critical | 0  LOW | Red |
| Warning | LOW  LOW+50 | Yellow |
| Normal | LOW+50  HIGH | Green |
| Over | HIGH  500 | Yellow |

**Configs**: A: LOW=100, B: LOW=120

#### RPM (0-4000)
Semi-circle gauge, rotating indicator, blue arc

### Fans
| Fan | Power | Status | Hours |
|-----|-------|--------|-------|
| 1 | Left | Fuse_Fan1, Feedback_K1 | 6-digit |
| 2 | Right | Fuse_Fan2, Feedback_K2 | 6-digit |

States: OFF (gray)  ON (rotating, exhaust visible)

### Status Indicators
- Inflation, Feedback_K1/K2, FeedbackPipeWatchdog
- Fuse_Fan1, Fuse_Fan2, Fuse_Dryer

Colors: Green=OK | Red=Error | Gray=Disabled

### System Indicator
Green  or Red  (with pulsation on error)

### Animations
- Exhaust: Particles rise & fade (fans ON only)
- Starfield: 75 falling streaks
- Disk Pulsate: Red when pressure  LOW
- Blade Spin: 360° (2s loop)

---

## Interactions

| Element | Action | Result |
|---------|--------|--------|
| Fan 1/2 | Click | Toggle power  rotate/stop blades |
| Fuse_Dryer | Click | Cycle: 100120200350 Pa |
| Fuse_Fan2 | Click | Cycle: 509002200 RPM |
| Fuse_Fan1 | Click | Toggle: Config A  B |
| Feedback_K1/K2 | Click | Cycle operating hours |
| Watchdog | Click | Toggle:    (error) |

---

## Python: generate_svg.py

`python
create_element(parent, tag, attribs, text)
create_fan(parent, x, y, size, id, state)
create_rpm_gauge(parent, cx, cy, id)
create_pressure_gauge(parent, cx, cy, id)
create_exhaust(parent, cx, cy, particles, dur)
create_starfield(parent, particles)
main()  #  te.svg
`

## JavaScript: js/init.js

`javascript
options.statusData
options.updateRPMGauge()
options.updatePressureGauge()
options.updatePressureGaugeSegments()
options.updateStatuses()
options.updateExhaust()
`

## JavaScript: js/render.js

`javascript
getFieldValue(name)        # Extract from InfluxDB
options.statusData = {...} # Load all fields
# Call all update functions
`

---

## Configuration

| Setting | Config A | Config B |
|---------|----------|----------|
| LOW | 100 | 120 |
| NORMAL | 250 | 200 |
| HIGH | 350 | 400 |
| SET | 250 | 225 |

**Timings**: Blade 2s | Exhaust 3s | Status pulse 3s

---

## InfluxDB Fields

Fan1_On, Fan2_On, FanSpeed_RPM, Pressure, SetPressure_Low/Normal/High
FeedbackPipeWatchdog, Feedback_K1/K2, Fuse_Fan1/Fan2/Dryer
Inflation, NoEmergency, OperationalHours1/2

---

## Development

**Add Gauge**: Python create_*()  main()  JS update*()  CSS

**Add Status**: Circle in Python  updateStatuses() logic  click handler

**Performance**: Cache DOM refs | CSS transforms | Batch updates

---

*See ARCHITECTURE.md for technical details & INTERACTIVE_GUIDE.md for interactions*
