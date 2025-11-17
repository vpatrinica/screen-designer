# Auto-generated from SVG by tools/svg_to_python.py
# Recreates the SVG DOM structure using create_element helper from generate_svg.py

def apply_blueprint(svg_root, create_element):
  n1_0 = create_element(svg_root, "title", None, "Clickable Power Button Components (ID-Styled)")
  n1_1 = create_element(svg_root, "defs", None, None)
    n2_0 = create_element(n1_1, "filter", {"id": "blur-effect", "x": "-50%", "y": "-50%", "width": "200%", "height": "200%"}, None)
      n3_0 = create_element(n2_0, "feGaussianBlur", {"in": "SourceGraphic", "stdDeviation": "1.5"}, None)
    n2_1 = create_element(n1_1, "style", None, "
      :root {
        --color-power-black: #000000;
        --color-power-off: #555555;
        --color-power-on: #00FF00;
      }
      
      @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      
      @keyframes pulse-brightness {
        0% { opacity: 0.6; }
        50% { opacity: 1.0; }
        100% { opacity: 0.6; }
      }
      
      /* --- Styles for Fan 1 --- */
      #power-fan1 {
        --power-color: var(--color-power-off); /* Default 'off' state */
        cursor: pointer;
      }
      #power-fan1.power-on {
        --power-color: var(--color-power-on); /* 'on' state */
      }
      #power-fan1 .intermediate-disk {
        fill: #333333;
      }
      #power-fan1 .power-bg-disk {
        fill: var(--color-power-black);
      }
      #power-fan1 .bg-animated-disk {
        fill: #000000;
      }
      #power-fan1.power-on .bg-animated-disk {
        fill: url(#animated-bg-gradient);
        animation: pulse-brightness 3s ease-in-out infinite;
        filter: url(#glow-filter);
      }
      #power-fan1 .rotor-disk {
        fill: #808080;
      }
      #power-fan1 .fan-blades {
        transform-origin: center;
        transform-box: fill-box;
      }
      #power-fan1.power-on .fan-blades {
        animation: spin 2s linear infinite;
      }
      #power-fan1 .fan-blade {
        fill: #666666;
        stroke: #404040;
        stroke-width: 0.2;
      }
      #power-fan1 .power-line {
        fill: var(--power-color); 
        stroke: none;
      }
      #power-fan1 .power-arc {
        stroke: var(--power-color); 
        fill: none;
        stroke-width: 0.75;
        stroke-linecap: round;
      }

      /* --- Styles for Fan 2 --- */
      #power-fan2 {
        --power-color: var(--color-power-off); /* Default 'off' state */
        cursor: pointer;
      }
      #power-fan2.power-on {
        --power-color: var(--color-power-on); /* 'on' state */
      }
      #power-fan2 .intermediate-disk {
        fill: #333333;
      }
      #power-fan2 .power-bg-disk {
        fill: var(--color-power-black);
      }
      #power-fan2 .bg-animated-disk {
        fill: #000000;
      }
      #power-fan2.power-on .bg-animated-disk {
        fill: url(#animated-bg-gradient);
        animation: pulse-brightness 3s ease-in-out infinite;
        filter: url(#glow-filter);
      }
      #power-fan2 .rotor-disk {
        fill: #808080;
      }
      #power-fan2 .fan-blades {
        transform-origin: center;
        transform-box: fill-box;
      }
      #power-fan2.power-on .fan-blades {
        animation: spin 2s linear infinite;
      }
      #power-fan2 .fan-blade {
        fill: #666666;
        stroke: #404040;
        stroke-width: 0.2;
      }
      #power-fan2 .power-line {
        fill: var(--power-color); 
        stroke: none;
      }
      #power-fan2 .power-arc {
        stroke: var(--power-color); 
        fill: none;
        stroke-width: 0.75;
        stroke-linecap: round;
      }

      .gauge-arc {
        fill: none;
        stroke: #666666;
        stroke-width: 2.25; /* scaled */
        stroke-linecap: round;
      }
      .gauge-arc-extra {
        fill: none;
        stroke-linecap: round;
      }
      .gauge-value-arc {
        fill: none;
        stroke: #00FF00;
        stroke-width: 0.75; /* scaled */
        stroke-linecap: round;
      }
      .gauge-tick {
        stroke: black;
        stroke-width: 0.375;
      }
      .gauge-label {
        fill: black;
        font-size: 3px;
        font-family: Arial, sans-serif;
      }
      .gauge-indicator {
        fill: #000000;
        stroke: #000000;
        stroke-width: 0.3;
      }
      .rpm-text {
        fill: #000000;
        font-size: 5px;
        font-weight: bold;
        font-family: Arial, sans-serif;
      }
      .rpm-value {
        fill: #000000;
        font-size: 4.5px;
        font-weight: bold;
        font-family: Arial, sans-serif;
      }
      .rpm-unit {
        fill: #000000;
        font-size: 2.5px;
        font-family: Arial, sans-serif;
        font-weight: bold;
      }
      .pressure-unit {
        fill: #000000;
        font-size: 3.5px;
        font-family: Arial, sans-serif;
        font-weight: bold;
      }
      /* Fan labels and counters */
      .fan-label {
        fill: #000000;
        font-size: 4px;
        font-weight: bold;
        font-family: 'Roboto', Arial, sans-serif;
      }
      .fan-number {
        fill: #000000;
        font-size: 4px;
        font-family: monospace, monospace;
      }
      .fan-units {
        fill: #000000;
        font-size: 3px;
        font-weight: bold;
        font-family: 'Roboto', Arial, sans-serif;
      }
      .fan-status-symbol {
        fill: gray;
      }
      .status-active {
        animation: pulse-brightness 3s ease-in-out infinite;
        filter: url(#glow-filter);
      }
      .status-label {
        fill: #000000;
        font-size: 3px;
        font-family: Arial, sans-serif;
        text-anchor: middle;
      }
      .pulsating-disk {
        animation: pulsate-red 2s ease-in-out infinite;
      }
      @keyframes pulsate-red {
        0% { opacity: 0.6; }
        50% { opacity: 1.0; }
        100% { opacity: 0.6; }
      }

      /* ===== NEW ANIMATION STYLES ===== */
      @keyframes exhaust-plume {
        0% {
          r: 2;
          opacity: 0.7;
          transform: translateY(0px);
        }
        100% {
          r: 10; /* Grow */
          opacity: 0;
          transform: translateY(20px); /* Move down 20 units */
        }
      }
      
      .plume-particle {
        fill: #ADD8E6; /* Light blueish-white */
        filter: url(#blur-effect);
        animation-name: exhaust-plume;
        /* duration and delay set by JS */
        animation-timing-function: linear;
        animation-iteration-count: infinite;
        transform-origin: center;
        transform-box: fill-box;
      }
    ")
    n2_2 = create_element(n1_1, "radialGradient", {"id": "animated-bg-gradient", "cx": "50%", "cy": "50%", "r": "50%"}, None)
      n3_0 = create_element(n2_2, "stop", {"offset": "0%", "style": "stop-color:#B0E0E6;stop-opacity:1.0"}, None)
      n3_1 = create_element(n2_2, "stop", {"offset": "50%", "style": "stop-color:#87CEEB;stop-opacity:1.0"}, None)
      n3_2 = create_element(n2_2, "stop", {"offset": "100%", "style": "stop-color:#4682B4;stop-opacity:0.9"}, None)
    n2_3 = create_element(n1_1, "radialGradient", {"id": "disk-gradient", "cx": "50%", "cy": "50%", "r": "50%"}, None)
      n3_0 = create_element(n2_3, "stop", {"offset": "0%", "style": "stop-color:#FFFFFF;stop-opacity:1.0"}, None)
      n3_1 = create_element(n2_3, "stop", {"offset": "70%", "style": "stop-color:#F0F0F0;stop-opacity:1.0"}, None)
      n3_2 = create_element(n2_3, "stop", {"offset": "100%", "style": "stop-color:#DADADA;stop-opacity:1.0"}, None)
    n2_4 = create_element(n1_1, "radialGradient", {"id": "red-gradient", "cx": "50%", "cy": "50%", "r": "50%"}, None)
      n3_0 = create_element(n2_4, "stop", {"offset": "0%", "style": "stop-color:#FF0000;stop-opacity:1.0"}, None)
      n3_1 = create_element(n2_4, "stop", {"offset": "100%", "style": "stop-color:#800000;stop-opacity:1.0"}, None)
    n2_5 = create_element(n1_1, "radialGradient", {"id": "status-red-gradient", "cx": "50%", "cy": "50%", "r": "50%"}, None)
      n3_0 = create_element(n2_5, "stop", {"offset": "0%", "style": "stop-color:#FF0000;stop-opacity:1.0"}, None)
      n3_1 = create_element(n2_5, "stop", {"offset": "100%", "style": "stop-color:#800000;stop-opacity:1.0"}, None)
    n2_6 = create_element(n1_1, "marker", {"id": "arrowhead", "markerWidth": "3", "markerHeight": "3", "refX": "1.5", "refY": "1.5", "orient": "auto", "markerUnits": "strokeWidth"}, None)
      n3_0 = create_element(n2_6, "polygon", {"points": "0 0, 3 1.5, 0 3", "fill": "black"}, None)
  n1_2 = create_element(svg_root, "rect", {"x": "0", "y": "-50", "width": "80", "height": "160", "fill": "#000011"}, None)
  n1_3 = create_element(svg_root, "g", {"id": "exhaust-container-1"}, None)
  n1_4 = create_element(svg_root, "g", {"id": "exhaust-container-2"}, None)
  n1_5 = create_element(svg_root, "g", {"id": "exhaust-container-center"}, None)
  n1_6 = create_element(svg_root, "g", {"id": "system-indicator"}, None)
    n2_0 = create_element(n1_6, "rect", {"x": "15.4", "y": "-37.9", "width": "49.5", "height": "100", "rx": "5", "ry": "5", "fill": "silver", "stroke": "silver", "stroke-width": "1"}, None)
    n2_1 = create_element(n1_6, "text", {"x": "32", "y": "36", "class": "fan-label"}, "SYSTEM")
    n2_2 = create_element(n1_6, "circle", {"cx": "40", "cy": "47.75", "r": "9", "fill": "black", "id": "no-errors-bg"}, None)
    n2_3 = create_element(n1_6, "circle", {"cx": "40", "cy": "47.75", "r": "8", "fill": "green", "class": "status-active", "id": "no-errors-disc"}, None)
    n2_4 = create_element(n1_6, "text", {"x": "40", "y": "47.75", "text-anchor": "middle", "dominant-baseline": "middle", "font-size": "10", "id": "no-errors-symbol"}, "✓")
  n1_7 = create_element(svg_root, "rect", {"id": "rect-behind-pressure-value", "x": "18", "y": "-39", "width": "44", "height": "35", "fill": "url(#disk-gradient)"}, None)
  n1_8 = create_element(svg_root, "rect", {"id": "rect-behind-speed-value", "x": "20", "y": "17", "width": "40", "height": "10", "fill": "url(#disk-gradient)"}, None)
  n1_9 = create_element(svg_root, "g", {"id": "fanspeed-container"}, None)
  n1_10 = create_element(svg_root, "g", {"id": "pressure-container"}, None)
  n1_11 = create_element(svg_root, "g", {"id": "status-indicators-fan1"}, None)
    n2_0 = create_element(n1_11, "g", {"id": "fuse-fan1"}, None)
      n3_0 = create_element(n2_0, "rect", {"x": "5", "y": "25", "width": "20", "height": "51", "rx": "5", "ry": "5", "fill": "silver", "stroke": "black", "stroke-width": "1"}, None)
      n3_1 = create_element(n2_0, "circle", {"cx": "10", "cy": "71", "r": "4", "fill": "black"}, None)
      n3_2 = create_element(n2_0, "circle", {"id": "status-Fuse_Fan1", "cx": "10", "cy": "71", "r": "3", "fill": "#00FF00", "class": "status-active"}, None)
      n3_3 = create_element(n2_0, "rect", {"x": "8.5", "y": "70", "width": "3", "height": "2", "fill": "transparent", "stroke": "black", "stroke-width": "0.5"}, None)
      n3_4 = create_element(n2_0, "line", {"x1": "7.5", "y1": "71", "x2": "12.5", "y2": "71", "stroke": "black", "stroke-width": "0.5"}, None)
    n2_1 = create_element(n1_11, "g", {"id": "feedback-k1"}, None)
      n3_0 = create_element(n2_1, "circle", {"cx": "20", "cy": "71", "r": "4", "fill": "black"}, None)
      n3_1 = create_element(n2_1, "circle", {"id": "status-Feedback_K1", "cx": "20", "cy": "71", "r": "3", "fill": "#00FF00", "class": "status-active"}, None)
      n3_2 = create_element(n2_1, "path", {"d": "M 22 70 L 21.5 71 L 22.5 71 Z", "fill": "black"}, None)
      n3_3 = create_element(n2_1, "path", {"d": "M 22 71 A 2 2 0 1 1 21.732 70", "stroke": "black", "fill": "none", "stroke-width": "0.5"}, None)
    n2_2 = create_element(n1_11, "g", {"id": "dryer-indicator"}, None)
      n3_0 = create_element(n2_2, "rect", {"x": "25", "y": "60", "width": "30", "height": "17", "rx": "5", "ry": "5", "fill": "silver", "stroke": "black", "stroke-width": "1"}, None)
      n3_1 = create_element(n2_2, "text", {"x": "34", "y": "65", "class": "fan-label"}, "DRYER")
      n3_2 = create_element(n2_2, "g", {"id": "fuse-dryer"}, None)
        n4_0 = create_element(n3_2, "circle", {"cx": "35", "cy": "71", "r": "4", "fill": "black"}, None)
        n4_1 = create_element(n3_2, "circle", {"id": "status-Fuse_Dryer", "cx": "35", "cy": "71", "r": "3", "fill": "#FF0000", "class": "status-active"}, None)
        n4_2 = create_element(n3_2, "rect", {"x": "33.5", "y": "70", "width": "3", "height": "2", "fill": "transparent", "stroke": "black", "stroke-width": "0.5"}, None)
        n4_3 = create_element(n3_2, "line", {"x1": "32.5", "y1": "71", "x2": "37.5", "y2": "71", "stroke": "black", "stroke-width": "0.5"}, None)
      n3_3 = create_element(n2_2, "g", {"id": "feedback-watchdog"}, None)
        n4_0 = create_element(n3_3, "circle", {"cx": "45", "cy": "71", "r": "4", "fill": "black"}, None)
        n4_1 = create_element(n3_3, "circle", {"id": "status-FeedbackPipeWatchdog", "cx": "45", "cy": "71", "r": "3", "fill": "#00FF00", "class": "status-active"}, None)
        n4_2 = create_element(n3_3, "path", {"d": "M 47 70 L 46.5 71 L 47.5 71 Z", "fill": "black"}, None)
        n4_3 = create_element(n3_3, "path", {"d": "M 47 71 A 2 2 0 1 1 46.732 70", "stroke": "black", "fill": "none", "stroke-width": "0.5"}, None)
    n2_3 = create_element(n1_11, "g", {"id": "status-indicators-fan2"}, None)
      n3_0 = create_element(n2_3, "g", {"id": "fuse-fan2"}, None)
        n4_0 = create_element(n3_0, "rect", {"x": "55", "y": "25", "width": "20", "height": "51", "rx": "5", "ry": "5", "fill": "silver", "stroke": "black", "stroke-width": "1"}, None)
        n4_1 = create_element(n3_0, "circle", {"cx": "60", "cy": "71", "r": "4", "fill": "black"}, None)
        n4_2 = create_element(n3_0, "circle", {"id": "status-Fuse_Fan2", "cx": "60", "cy": "71", "r": "3", "fill": "gray"}, None)
        n4_3 = create_element(n3_0, "rect", {"x": "58.5", "y": "70", "width": "3", "height": "2", "fill": "transparent", "stroke": "black", "stroke-width": "0.5"}, None)
        n4_4 = create_element(n3_0, "line", {"x1": "57.5", "y1": "71", "x2": "62.5", "y2": "71", "stroke": "black", "stroke-width": "0.5"}, None)
      n3_1 = create_element(n2_3, "g", {"id": "feedback-k2"}, None)
        n4_0 = create_element(n3_1, "circle", {"cx": "70", "cy": "71", "r": "4", "fill": "black"}, None)
        n4_1 = create_element(n3_1, "circle", {"id": "status-Feedback_K2", "cx": "70", "cy": "71", "r": "3", "fill": "gray"}, None)
        n4_2 = create_element(n3_1, "path", {"d": "M 72 70 L 71.5 71 L 72.5 71 Z", "fill": "black"}, None)
        n4_3 = create_element(n3_1, "path", {"d": "M 72 71 A 2 2 0 1 1 71.732 70", "stroke": "black", "fill": "none", "stroke-width": "0.5"}, None)
  n1_12 = create_element(svg_root, "g", {"id": "power-fan1-container"}, None)
  n1_13 = create_element(svg_root, "g", {"id": "power-fan2-container"}, None)
  n1_14 = create_element(svg_root, "g", {"id": "starfield-container"}, None)
