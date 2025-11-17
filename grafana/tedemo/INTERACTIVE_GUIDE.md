# Interactive Features Guide

Quick reference for all clickable elements and behaviors.

## Interactive Elements

| Element | Location | Click Effect | Visual Result |
|---------|----------|-------------|----------------|
| **Fan 1/2** | Left/Right | Toggle power | Blades rotate/stop, exhaust show/hide, status green/gray |
| **Fuse_Dryer** | Bottom | Cycle pressure | 100120200350 Pa, arc color change |
| **Fuse_Fan2** | Right | Cycle RPM | 509002200, indicator rotates |
| **Fuse_Fan1** | Left | Toggle config | A/B swap: LOW 100120, segment resize |
| **Feedback_K1** | Left status | Cycle hours | 000100010000000888 |
| **Feedback_K2** | Right status | Cycle hours | 000100010000000888 |
| **Watchdog** | Center | Toggle error |  (greenred pulsating) |

---

## Status Colors

| Color | Meaning |
|-------|---------|
|  Green | Active/OK |
|  Red | Error/Inactive |
|  Gray | Disabled (fan off) |

---

## Test Scenarios

**Low Pressure Alert**:
1. Click Fuse_Dryer  100 Pa (indicator appears, disk red)
2. Click Fuse_Fan1  Config B (indicator stays, LOW=120)
3. Click Fuse_Dryer  200 Pa (indicator gone, disk white)

**Monitor Fans**:
1. Click Fan 1  ON (blades rotate, exhaust appears, status green)
2. Click Feedback_K1 (cycles operating hours)
3. Click Fan 1  OFF (blades stop, status gray)

**Test RPM**:
- Click Fuse_Fan2 repeatedly: 50  900  2200 (indicator rotates)

**System Error**:
- Click Watchdog:    (red pulsating)

---

## Tips

 All interactions provide immediate visual feedback
 Colors consistent throughout dashboard
 Status circles gray when fans OFF
 Pressure config affects low-pressure threshold
 All cycles wrap around to start

---

*See DOCUMENTATION.md for component details & ARCHITECTURE.md for technical reference*
