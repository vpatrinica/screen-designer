const SVG_NS = "http://www.w3.org/2000/svg";

/**
 * Creates a parametric power button and appends it to a container.
 */
function createPowerButton(containerId, params) {

  const { x, y, size, strokeWidth, id, initialState } = params;

  const cx = x + size / 2;
  const cy = y + size / 2;
  const r_bg = size / 2;

  const rect = {
    x: cx - (strokeWidth / 2),
    y: y,
    width: strokeWidth,
    height: size / 2,
    rx: strokeWidth / 2
  };

  const r_arc = (size / 2) - (strokeWidth / 2);
  const startAngleRad = -135 * (Math.PI / 180);
  const endAngleRad = -45 * (Math.PI / 180);

  const startX = cx + r_arc * Math.cos(endAngleRad);
  const startY = cy + r_arc * Math.sin(endAngleRad);
  const endX = cx + r_arc * Math.cos(startAngleRad);
  const endY = cy + r_arc * Math.sin(startAngleRad);

  const arcPathD = `M ${startX.toFixed(3)} ${startY.toFixed(3)} A ${r_arc} ${r_arc} 0 1 1 ${endX.toFixed(3)} ${endY.toFixed(3)}`;

  const container = document.getElementById(containerId);
  if (!container) { return; }

  const mainGroup = document.createElementNS(SVG_NS, "g");
  mainGroup.setAttribute("id", id);

  // ** NOTE: The .power-button-component class is no longer added. **

  // We still use the 'power-on' class for state toggling
  if (initialState === 'on') {
    mainGroup.classList.add("power-on");
  }

  // Child elements (still use classes for styling)
  const bgDisk = document.createElementNS(SVG_NS, "circle");
  bgDisk.setAttribute("class", "power-bg-disk");
  bgDisk.setAttribute("cx", cx);
  bgDisk.setAttribute("cy", cy);
  bgDisk.setAttribute("r", r_bg);

  const lineRect = document.createElementNS(SVG_NS, "rect");
  lineRect.setAttribute("class", "power-line");
  lineRect.setAttribute("x", rect.x);
  lineRect.setAttribute("y", rect.y);
  lineRect.setAttribute("width", rect.width);
  lineRect.setAttribute("height", rect.height);
  lineRect.setAttribute("rx", rect.rx);

  const arcPath = document.createElementNS(SVG_NS, "path");
  arcPath.setAttribute("class", "power-arc");
  arcPath.setAttribute("d", arcPathD);

  mainGroup.appendChild(bgDisk);
  mainGroup.appendChild(lineRect);
  mainGroup.appendChild(arcPath);
  container.appendChild(mainGroup);
}

/**
 * Toggles the 'power-on' class for a given element ID.
 */
function togglePowerButton(buttonId) {
  const buttonGroup = document.getElementById(buttonId);
  if (buttonGroup) {
    buttonGroup.classList.toggle("power-on");
  }
}

/**
 * Initialize the power buttons after SVG is loaded
 */
function initPowerButtons() {
  // ---
  // 1. INITIALIZATION CALLS
  // ---

  createPowerButton(
    "power-fan1-container",
    {
      id: "power-fan1",
      x: 10,
      y: 65,
      size: 10,
      strokeWidth: 0.75,
      initialState: 'on'
    }
  );

  createPowerButton(
    "power-fan2-container",
    {
      id: "power-fan2",
      x: 50,
      y: 65,
      size: 10,
      strokeWidth: 0.75,
      initialState: 'off'
    }
  );

  // ---
  // 2. ADD CLICK LISTENERS
  // ---

  const fan1Container = document.getElementById("power-fan1-container");
  if (fan1Container) {
    fan1Container.addEventListener("click", () => {
      togglePowerButton("power-fan1");
    });
  }

  const fan2Container = document.getElementById("power-fan2-container");
  if (fan2Container) {
    fan2Container.addEventListener("click", () => {
      togglePowerButton("power-fan2");
    });
  }
}

// Initialize when the window loads (ensures all scripts are loaded)
window.addEventListener('load', initPowerButtons);