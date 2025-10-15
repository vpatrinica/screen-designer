Interactive Roof Sensor Map: Functionality Summary
This document outlines the complete feature set of the interactive roof sensor map application.

1. Visualization & Layout
Multi-View Display: The application is structured into five distinct, scrollable sections or "tiles": one "Full View" showing all sensors, and four dedicated views for each region (1-4).

Sensor Representation: Displays three types of sensors (Pressure, Flow, Snow), each with a unique, color-coded symbol based on the provided legend.

Alert Visualization: Sensors with a status: "red" in the data configuration are given a persistent, prominent "glow" effect to make them easily identifiable as critical alerts.

Responsive Design: The layout automatically adapts to different screen sizes. On narrow screens (like smartphones), the map and control panel stack vertically for a better user experience.

2. Navigation & Interactivity
Scroll-Based Navigation: Clicking a button in the Navigation Panel (Full View, Region 1, etc.) smoothly scrolls the page to the corresponding map view.

Clickable Region Labels: In the "Full View", the large, semi-transparent region numbers (1, 2, 3, 4) are clickable and also function as navigation links to scroll to that region's view.

"Back to Top" Rocket Button: When a user scrolls down from the "Full View", a "rocket" button appears in the bottom-right corner, allowing for a quick scroll back to the top.

Sensor Tooltips: Hovering the mouse over any sensor on any map displays a tooltip with its specific details (ID, type, and data).

List-to-Map Highlighting: Hovering over an item in the sensor list on the right panel highlights the corresponding sensor on the map.

Interactive Legend Filter: The legend in the control panel is clickable. Users can filter the sensor list to show only "Drucksensoren," "Durchflusssensoren," or "Schneesensoren." An "All" button is available to clear the filter.

Region-Based Filtering: Navigating to a specific region view (e.g., "Region 1") automatically filters the sensor list to show only the sensors present in that region.

3. Sensor Configuration & Editing
Sensor Selection: Clicking on any sensor node selects it, highlighting it with a blue border.

Edit Panel: When a sensor is selected, an "Edit Panel" appears in the right-hand toolbox.

Live Drag-and-Drop: The selected sensor can be clicked and dragged to a new position on the map.

Coordinate Input: The X and Y coordinates of the selected sensor can also be edited directly via input fields in the Edit Panel.

Update Position: An "Update Position" button saves the new coordinates to the current session's data and redraws the map to reflect the change.

4. Data & Exporting
Save/Load Configuration:

Save Config: Allows the user to download the current state of the sensorData array, including any positional edits, as a sensor-config.json file.

Load Config: Allows the user to upload a previously saved .json file to restore the map to that configuration.

Save SVG Map: Exports the current map view (without the UI panels) as a simple, non-interactive .svg file.

Save Standalone SVG: This is the most powerful export option. It generates a single, self-contained, and fully interactive .svg file. This file includes the map, the control panel (navigation, legend, sensor list), and all the necessary JavaScript and CSS to make it work independently in any modern web browser. All features, including tooltips, filtering, and navigation, are preserved in this export.