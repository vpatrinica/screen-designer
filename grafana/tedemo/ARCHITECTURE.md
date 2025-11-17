# Code Architecture

## Core Principle: Separation of Concerns

**Python** creates ALL static SVG elements. **JavaScript** ONLY updates existing elements (no DOM creation).

```
generate_svg.py (880 lines)
    ↓
[Embedded CSS + JavaScript]
    ↓
te.svg (output file)
    ↓
Browser loads SVG
    ↓
js/init.js + js/render.js execute
    ↓
Update existing elements + handle clicks
```

---

## Quick Component Map

| Component | Purpose | Created By | Updated By |
|-----------|---------|------------|-----------|
| Fans (×2) | Power toggles, animations | Python `create_fan()` | JS click handlers |
| RPM Gauge | 0-4000 range, arc indicator | Python `create_rpm_gauge()` | `updateRPMGauge()` |
| Pressure Gauge | 0-500 Pa, 4-colored arc | Python `create_pressure_gauge()` | `updatePressureGauge()` |
| Status Circles (×8) | State indicators, colors | Python loop | `updateStatuses()` |
| System Indicator | ✓/✗ symbol | Python | `updateStatuses()` |
| Exhaust Particles | Animated puffs | Python `create_exhaust()` | `updateExhaust()` |
| Starfield | Background animation | Python `create_starfield()` | CSS only (always running) |

---

## Data Flow

**Generation** (Python):
```
create_fan() → Fan blades + power indicators + hours text
create_rpm_gauge() → RPM arc + indicator (empty, filled by JS)
create_pressure_gauge() → Pressure arc + indicator + colored segments (empty, updated by JS)
create_exhaust() → Animated particles (hidden initially)
create_starfield() → Background animation (always running)
Embed CSS + JavaScript → Write te.svg
```

**Runtime** (JavaScript):
```
Load → render.js loads InfluxDB data → options.statusData populated
       → updateRPMGauge() → updates arc + indicator
       → updatePressureGauge() → updates arc + color + indicator
       → updateStatuses() → updates circle colors
       → updateExhaust() → toggles visibility

Click → Fan → toggle power-on class + updateStatuses() + updateExhaust()
Click → Fuse_Dryer → cycle pressure → updatePressureGauge()
Click → Fuse_Fan2 → cycle RPM → updateRPMGauge()
Click → Fuse_Fan1 → toggle config → updatePressureGaugeSegments() + updatePressureGauge()
Click → Feedback_K1/K2 → cycle hours → update text
Click → Watchdog → toggle error → updateStatuses()
```

---

## Key Element IDs

**RPM Gauge**: `fanspeed`, `fanspeed-value-arc`, `fanspeed-value`, `fanspeed-indicator`

**Pressure Gauge**: `pressure`, `pressure-value-arc`, `pressure-value`, `pressure-indicator`, `pressure-{low,yellow-low,green,yellow-high}-arc`, `pressure-{low,normal,high,set}-label`

**Fans**: `power-fan{1,2}-container`, `power-fan{1,2}`, `fan{1,2}-hours`

**Status Circles**: `status-{Inflation, Feedback_K1, Feedback_K2, FeedbackPipeWatchdog, Fuse_Fan1, Fuse_Fan2, Fuse_Dryer}`

**System**: `no-errors-bg`, `no-errors-disc`, `no-errors-symbol`

**Containers**: `exhaust-container-{1,2,center}`

---

## State Management

**Global**: `options.statusData = {Fan1_On, Fan2_On, FanSpeed_RPM, Pressure, SetPressure_Low/Normal/High, FeedbackPipeWatchdog, Feedback_K1/K2, Fuse_Fan1/Fan2/Dryer, Inflation, NoEmergency, OperationalHours1/2}`

**Dependencies**:
- Fan power ON/OFF → blade rotation (CSS class) + status colors (green/gray) + exhaust visibility
- Pressure change → arc length/color + disk color + indicator rotation + low indicator visibility
- Config toggle → segment boundaries recalculate + labels update
- Error state → system symbol (✓/✗) + color (green/red)

---

## Geometry Calculations

**Pressure Gauge**: Start=-24.5 degrees (-0.4276 rad), End=204.5 degrees (3.5691 rad), Span=229 degrees (3.9968 rad)
- Formula: `angle = startAngle + (pressure/500 * span)` rotated by pi for SVG coords

**RPM Gauge**: Start=0 degrees, End=180 degrees (pi rad), Span=pi
- Formula: `angle = rpm/4000 * pi` rotated by pi for SVG coords

**Colored Segments**: Red [0→LOW] | Yellow [LOW→LOW+50] | Green [LOW+50→HIGH] | Yellow [HIGH→500]

**Indicator Rotation**: Triangle points calculated, then mirrored across center

---

## Functions

| Name | Purpose | Type | Input | Output |
|------|---------|------|-------|--------|
| create_element() | Create SVG element | Python | parent, tag, attrs | Element |
| create_fan() | Fan component | Python | parent, x, y, id, state | void |
| create_rpm_gauge() | RPM gauge | Python | parent, cx, cy, id | void |
| create_pressure_gauge() | Pressure gauge | Python | parent, cx, cy, id | void |
| create_exhaust() | Exhaust animation | Python | parent, cx, cy, particles, duration | void |
| create_starfield() | Starfield animation | Python | parent, particles | void |
| updateRPMGauge() | Update RPM | JavaScript | svgmap | void |
| updatePressureGauge() | Update pressure | JavaScript | svgmap | void |
| updatePressureGaugeSegments() | Reconfig segments | JavaScript | svgmap | void |
| updateStatuses() | Update indicators | JavaScript | svgmap | void |
| updateExhaust() | Toggle exhaust | JavaScript | svgmap | void |

---

## CSS Classes & Animations

**Classes**: power-on (blade rotation) | status-active (pulsate) | pulsating-disk (low pressure)

**Animations**: @keyframes spin (2s) | @keyframes pulse-brightness (3s) | @keyframes exhaust-plume | @keyframes pulsate-red

---

## Extension Points

**Add Gauge**: Python create_*() → Python main() call → JS update*() → JS render.js pipeline → CSS styles in defs.xml

**Add Status**: Python circle with ID → JS updateStatuses() logic → add click handler → test colors

**Add Animation**: Python animated element → CSS @keyframes → JS toggle class (if needed)

---

## Performance Notes

- 99 particles (44 exhaust + 55 starfield)
- Continuous CSS animations on fans + particles
- Updates on-demand (click events only)
- No DOM creation/destruction in JS
- Arc recalculation every update (acceptable cost)

---

*See DOCUMENTATION.md for component details & INTERACTIVE_GUIDE.md for user interactions*
