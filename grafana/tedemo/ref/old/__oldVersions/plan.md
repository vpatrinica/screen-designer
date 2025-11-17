# SVG Visualization Refactoring Plan

This document outlines the plan to refactor the `te.svg` visualization based on the user's request.

## 1. Architecture Overview

The new architecture will separate concerns into different files, making the solution more modular, maintainable, and scalable.

-   **`generate_svg.py`**: A Python script responsible for generating the `te.svg` file. It will programmatically create all the necessary SVG elements, including fans, gauges, and status indicators, assigning them meaningful and consistent IDs. This removes the ad-hoc element creation from the client-side JavaScript.

-   **`te.svg`**: The main SVG file, which will be the output of the `generate_svg.py` script. This file will contain the SVG structure, inline styles, and links to external JavaScript files. It will not contain any inline element creation logic.

-   **`js/`**: A directory to hold the JavaScript files.
    -   **`init.js`**: This file will contain the initialization logic. It will run on SVG load, setting up initial states and attaching event listeners (e.g., for the fan power buttons).
    -   **`render.js`**: This file will define all the functions responsible for updating the SVG's appearance in response to data changes. For example, `updateFanSpeed(fanId, speed)` or `setPressure(value)`. These functions will target elements by their new, meaningful IDs.

## 2. State Variables and Element IDs

The SVG elements that change based on the application's state will have clear and predictable `id` attributes. This is crucial for the `render.js` functions to work correctly.

Here is a proposed mapping:

| State Variable      | Element ID (example)                | Description                                       |
| ------------------- | ----------------------------------- | ------------------------------------------------- |
| `fan1_on`           | `fan-1`                             | The main group for Fan 1, to toggle 'on'/'off' class. |
| `fan2_on`           | `fan-2`                             | The main group for Fan 2.                         |
| `fuse_fan1`         | `status-fuse-fan-1`                 | The indicator circle for Fan 1's fuse.            |
| `fuse_fan2`         | `status-fuse-fan-2`                 | The indicator circle for Fan 2's fuse.            |
| `fan1_speed`        | `fan-1-speed-gauge-value`           | The text element showing the RPM value for Fan 1. |
| `fan1_speed`        | `fan-1-speed-gauge-indicator`       | The needle/triangle of the RPM gauge for Fan 1.   |
| `pressure`          | `pressure-gauge-value`              | The text element for the pressure value.          |
| `pressure`          | `pressure-gauge-indicator`          | The needle/triangle of the pressure gauge.        |
| `set_pressure`      | `pressure-gauge-set-value-label`    | The text label for the "SET" pressure value.      |
| `normal_pressure`   | `pressure-gauge-normal-range`       | The green arc segment on the pressure gauge.      |
| `low_pressure`      | `pressure-gauge-low-range`          | The red arc segment on the pressure gauge.        |
| `high_pressure`     | `pressure-gauge-high-range`         | The yellow arc segment for high pressure.         |
| `fan1_hours`        | `fan-1-operating-hours`             | The 6-digit text element for Fan 1's hours.       |
| `fan2_hours`        | `fan-2-operating-hours`             | The 6-digit text element for Fan 2's hours.       |

## 3. Task Breakdown

1.  **Setup**:
    -   Create the `js/` directory.

2.  **Create `plan.md`**:
    -   Write this planning document.

3.  **Python SVG Generation (`generate_svg.py`)**:
    -   Create the Python script.
    -   Use a library like `xml.etree.ElementTree` to build the SVG structure.
    -   Define functions to generate the components (fan, RPM gauge, pressure gauge) with the new ID scheme.
    -   The script will output a complete `te.svg` file with inline styles.

4.  **Refactor JavaScript (`init.js`, `render.js`)**:
    -   Separate the existing JavaScript into two files:
        -   `init.js`: Will contain the `window.addEventListener('load', ...)` logic and any one-time setup.
        -   `render.js`: Will contain all the update functions (`updateRPMGauge`, `updatePressureGauge`, `updateStatuses`, etc.).
    -   Modify the functions in `render.js` to use `document.getElementById()` with the new, meaningful IDs.
    -   Remove all DOM element creation code (e.g., `document.createElementNS`) from the JavaScript, as Python now handles this.

5.  **Final Assembly**:
    -   Run `generate_svg.py` to create the final `te.svg`.
    -   The generated `te.svg` will be clean, containing only the SVG markup, inline styles, and links to the `.js` files.
    -   Open `te.svg` in a browser to verify that it looks and functions identically to the original, but with the new, refactored architecture.
