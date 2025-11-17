#!/usr/bin/env python3
"""
Generate te.svg programmatically using Python functions.
Mirrors the JavaScript creation logic from teXXX.svg.
"""
import xml.etree.ElementTree as ET
import math
import argparse
import os


def create_element(parent, tag, attribs=None, text=None):
    """Create an SVG element with attributes and optional text content."""
    elem = ET.SubElement(parent, tag)
    if attribs:
        for key, value in attribs.items():
            elem.set(key, str(value))
    if text:
        elem.text = str(text)
    return elem


def create_fan(parent, x, y, size, stroke_width, fan_id, initial_state):
    """
    Create a parametric fan component.
    Mirrors createFan() from teXXX.svg JavaScript.
    """
    cx = x + size / 2
    cy = y + size / 2
    
    # Main group
    group_attribs = {"id": fan_id}
    if initial_state == 'on':
        group_attribs['class'] = 'power-on'
    main_group = create_element(parent, "g", group_attribs)
    
    # Background disk
    create_element(main_group, "circle", {
        "class": "power-bg-disk",
        "cx": cx, "cy": cy, "r": 11
    })
    
    # Animated background disk
    create_element(main_group, "circle", {
        "class": "bg-animated-disk",
        "cx": cx, "cy": cy, "r": 10
    })
    
    # Fan blades group
    blades_group = create_element(main_group, "g", {"class": "fan-blades"})
    blade_radius = 10.5
    blade_angle = 360 / 5
    
    for i in range(5):
        angle = (i * blade_angle) * (math.pi / 180)
        blade_start_angle = angle - 0.3
        blade_end_angle = angle + 0.3
        inner_radius = 2
        outer_radius = blade_radius
        
        x1 = cx + inner_radius * math.cos(blade_start_angle)
        y1 = cy + inner_radius * math.sin(blade_start_angle)
        x2 = cx + outer_radius * math.cos(blade_start_angle)
        y2 = cy + outer_radius * math.sin(blade_start_angle)
        x3 = cx + outer_radius * math.cos(blade_end_angle)
        y3 = cy + outer_radius * math.sin(blade_end_angle)
        x4 = cx + inner_radius * math.cos(blade_end_angle)
        y4 = cy + inner_radius * math.sin(blade_end_angle)
        
        blade_path = f"M {x1} {y1} L {x2} {y2} L {x3} {y3} L {x4} {y4} Z"
        create_element(blades_group, "path", {"d": blade_path, "class": "fan-blade"})
    
    # Intermediate disk
    create_element(main_group, "circle", {
        "class": "intermediate-disk",
        "cx": cx, "cy": cy, "r": 6
    })
    
    # Rotor disk
    create_element(main_group, "circle", {
        "class": "rotor-disk",
        "cx": cx, "cy": cy, "r": 5
    })
    
    # Power line (vertical bar)
    rect_x = cx - (stroke_width / 2)
    rect_y = y
    create_element(main_group, "rect", {
        "class": "power-line",
        "x": rect_x, "y": rect_y,
        "width": stroke_width,
        "height": size / 2,
        "rx": stroke_width / 2
    })
    
    # Power arc
    r_arc = (size / 2) - (stroke_width / 2)
    start_angle_rad = -135 * (math.pi / 180)
    end_angle_rad = -45 * (math.pi / 180)
    
    start_x = cx + r_arc * math.cos(end_angle_rad)
    start_y = cy + r_arc * math.sin(end_angle_rad)
    end_x = cx + r_arc * math.cos(start_angle_rad)
    end_y = cy + r_arc * math.sin(start_angle_rad)
    
    arc_path_d = f"M {start_x:.3f} {start_y:.3f} A {r_arc} {r_arc} 0 1 1 {end_x:.3f} {end_y:.3f}"
    create_element(main_group, "path", {"class": "power-arc", "d": arc_path_d})
    
    # Labels - extract correct fan number from ID (e.g., "power-fan1" -> "FAN1")
    label_y = cy - 25
    if 'fan1' in fan_id.lower():
        fan_label = "FAN1"
    elif 'fan2' in fan_id.lower():
        fan_label = "FAN2"
    else:
        fan_label = "FAN"
    
    create_element(parent, "text", {
        "x": cx, "y": label_y,
        "class": "fan-label",
        "text-anchor": "middle",
        "dominant-baseline": "middle"
    }, fan_label)
    
    create_element(parent, "text", {
        "x": cx, "y": label_y + 6,
        "class": "fan-units",
        "text-anchor": "middle",
        "dominant-baseline": "middle"
    }, "Hours")
    
    # Add ID for operating hours text based on fan ID
    hours_id = f"{fan_label.lower()}-hours"
    create_element(parent, "text", {
        "id": hours_id,
        "x": cx, "y": label_y + 10,
        "class": "fan-number",
        "text-anchor": "middle",
        "dominant-baseline": "middle"
    }, "000000")


def create_exhaust(parent, cx, cy, num_particles, duration_sec):
    """
    Create exhaust particles (animated).
    Mirrors createExhaust() from teXXX.svg JavaScript.
    """
    import random
    for i in range(num_particles):
        particle = create_element(parent, "circle", {
            "class": "plume-particle",
            "cx": cx + (random.random() - 0.5) * 4,
            "cy": cy + (random.random() - 0.5) * 2,
            "r": "2"
        })
        # Set animation delay and duration as style
        delay = random.random() * duration_sec
        particle.set("style", f"animation-delay: {-delay}s; animation-duration: {duration_sec}s;")


def create_starfield(parent, num_particles):
    """
    Create starfield particles (animated lines).
    Mirrors createStarfield() from teXXX.svg JavaScript.
    """
    import random
    for i in range(num_particles):
        x = random.random() * 100
        y_start = -50
        y_end = 110
        len_streak = random.random() * 2 + 0.5
        duration = f"{random.random() * 3 + 2}s"
        delay = f"{random.random() * 5}s"
        
        line = create_element(parent, "line", {
            "x1": x, "x2": x,
            "stroke": "white",
            "stroke-width": random.random() * 0.3 + 0.1,
            "opacity": random.random() * 0.5 + 0.3
        })
        
        # Add animate elements for y1
        animate_y1 = create_element(line, "animate", {
            "attributeName": "y1",
            "from": y_start,
            "to": y_end,
            "dur": duration,
            "begin": delay,
            "repeatCount": "indefinite"
        })
        
        # Add animate elements for y2
        animate_y2 = create_element(line, "animate", {
            "attributeName": "y2",
            "from": y_start + len_streak,
            "to": y_end + len_streak,
            "dur": duration,
            "begin": delay,
            "repeatCount": "indefinite"
        })


def create_rpm_gauge(parent, cx, cy, gauge_id):
    """
    Create an RPM gauge.
    Mirrors createGauge() from teXXX.svg JavaScript.
    """
    gauge_group = create_element(parent, "g", {
        "class": "rpm-gauge",
        "id": gauge_id,
        "data-cx": cx,
        "data-cy": cy
    })
    
    gauge_radius = 15
    
    # Background disk (sector)
    disk_radius = 22.5
    disk_start = math.pi + (22.5 * math.pi / 180)
    disk_end = -22.5 * math.pi / 180
    expand = 40 * math.pi / 180
    disk_start_expanded = disk_start - expand
    disk_end_expanded = disk_end + expand
    
    # Normalize
    disk_end_norm = disk_end_expanded
    while disk_end_norm < disk_start_expanded:
        disk_end_norm += 2 * math.pi
    
    disk_angle_span = disk_end_norm - disk_start_expanded
    disk_large_arc = 1 if disk_angle_span > math.pi else 0
    disk_sweep = 1
    
    disk_start_x = cx + disk_radius * math.cos(disk_start_expanded)
    disk_start_y = cy + disk_radius * math.sin(disk_start_expanded)
    disk_end_x = cx + disk_radius * math.cos(disk_end_norm)
    disk_end_y = cy + disk_radius * math.sin(disk_end_norm)
    
    disk_path_d = f"M {cx} {cy} L {disk_start_x:.3f} {disk_start_y:.3f} A {disk_radius} {disk_radius} 0 {disk_large_arc} {disk_sweep} {disk_end_x:.3f} {disk_end_y:.3f} Z"
    create_element(gauge_group, "path", {
        "id": f"{gauge_id}-disk-path",
        "d": disk_path_d,
        "fill": "url(#disk-gradient)",
        "class": "gauge-disk"
    })
    
    # Gauge arc (main semi-circle)
    gauge_start_angle = 0
    gauge_end_angle = math.pi
    angle_span = abs(gauge_end_angle - gauge_start_angle)
    large_arc_flag = 1 if angle_span > math.pi else 0
    sweep_flag = 1
    
    rotated_start = gauge_start_angle + math.pi
    rotated_end = gauge_end_angle + math.pi
    
    gauge_arc_path = f"M {cx + gauge_radius * math.cos(rotated_start):.3f} {cy + gauge_radius * math.sin(rotated_start):.3f} A {gauge_radius} {gauge_radius} 0 {large_arc_flag} {sweep_flag} {cx + gauge_radius * math.cos(rotated_end):.3f} {cy + gauge_radius * math.sin(rotated_end):.3f}"
    create_element(gauge_group, "path", {"d": gauge_arc_path, "class": "gauge-arc"})
    
    # Value arc (initially empty, updated by JS)
    create_element(gauge_group, "path", {
        "id": f"{gauge_id}-value-arc",
        "class": "gauge-value-arc"
    })
    
    # Tick marks and labels
    max_rpm = 4000
    num_ticks = 4
    
    for i in range(num_ticks + 1):
        rpm = (i * max_rpm) / num_ticks
        angle = gauge_start_angle + (i * (gauge_end_angle - gauge_start_angle)) / num_ticks
        
        tick_inner_radius = gauge_radius - 4
        tick_outer_radius = gauge_radius - 2
        tick_x1 = cx + tick_inner_radius * math.cos(angle)
        tick_y1 = cy + tick_inner_radius * math.sin(angle)
        tick_x2 = cx + tick_outer_radius * math.cos(angle)
        tick_y2 = cy + tick_outer_radius * math.sin(angle)
        
        # Symmetric with respect to center
        tick_x1 = 2 * cx - tick_x1
        tick_y1 = 2 * cy - tick_y1
        tick_x2 = 2 * cx - tick_x2
        tick_y2 = 2 * cy - tick_y2
        
        create_element(gauge_group, "line", {
            "x1": tick_x1, "y1": tick_y1,
            "x2": tick_x2, "y2": tick_y2,
            "class": "gauge-tick"
        })
        
        # Number label
        if 0 <= i <= 4:
            label_radius = gauge_radius + 3
            label_x = cx + label_radius * math.cos(angle)
            label_y = cy + label_radius * math.sin(angle)
            
            label_x = 2 * cx - label_x
            label_y = 2 * cy - label_y
            
            radial_angle = math.atan2(label_y - cy, label_x - cx) * 180 / math.pi
            tangent_angle = radial_angle + 90
            
            create_element(gauge_group, "text", {
                "x": label_x, "y": label_y,
                "class": "gauge-label",
                "text-anchor": "middle",
                "dominant-baseline": "middle",
                "transform": f"rotate({tangent_angle}, {label_x}, {label_y})"
            }, str(int(rpm)))
    
    # Indicator triangle (initially at 0)
    indicator_group = create_element(gauge_group, "g", {"class": "rpm-indicator"})
    create_element(indicator_group, "polygon", {
        "id": f"{gauge_id}-indicator",
        "points": "0,0 0,0 0,0",
        "class": "gauge-indicator"
    })
    
    # RPM value text
    create_element(gauge_group, "text", {
        "id": f"{gauge_id}-value",
        "x": cx, "y": cy + 3.75,
        "class": "rpm-value",
        "text-anchor": "middle",
        "dominant-baseline": "middle"
    }, "0")
    
    # RPM unit text
    create_element(gauge_group, "text", {
        "x": cx, "y": cy + 7.5,
        "class": "rpm-unit",
        "text-anchor": "middle",
        "dominant-baseline": "middle"
    }, "RPM")


def create_pressure_gauge(parent, cx, cy, gauge_id):
    """
    Create a pressure gauge with colored segments.
    Mirrors createPressureGauge() from teXXX.svg JavaScript.
    """
    gauge_group = create_element(parent, "g", {
        "class": "pressure-gauge",
        "id": gauge_id,
        "data-cx": cx,
        "data-cy": cy
    })
    
    gauge_radius = 15
    extra_radius1 = 25
    extra_radius2 = 30
    
    # Background disk
    disk_radius = 36.5
    disk_start = math.pi + (22.5 * math.pi / 180)
    disk_end = -22.5 * math.pi / 180
    expand = 57.5 * math.pi / 180
    disk_start_expanded = disk_start - expand
    disk_end_expanded = disk_end + expand
    
    disk_end_norm = disk_end_expanded
    while disk_end_norm < disk_start_expanded:
        disk_end_norm += 2 * math.pi
    
    disk_angle_span = disk_end_norm - disk_start_expanded
    disk_large_arc = 1 if disk_angle_span > math.pi else 0
    disk_sweep = 1
    
    disk_start_x = cx + disk_radius * math.cos(disk_start_expanded)
    disk_start_y = cy + disk_radius * math.sin(disk_start_expanded)
    disk_end_x = cx + disk_radius * math.cos(disk_end_norm)
    disk_end_y = cy + disk_radius * math.sin(disk_end_norm)
    
    disk_path_d = f"M {cx} {cy} L {disk_start_x:.3f} {disk_start_y:.3f} A {disk_radius} {disk_radius} 0 {disk_large_arc} {disk_sweep} {disk_end_x:.3f} {disk_end_y:.3f} Z"
    create_element(gauge_group, "path", {
        "id": f"{gauge_id}-disk-path",
        "d": disk_path_d,
        "fill": "url(#disk-gradient)",
        "class": "gauge-disk"
    })
    
    # Main gauge arc
    gauge_start_angle = -24.5 * math.pi / 180
    gauge_end_angle = math.pi + 24.5 * math.pi / 180
    angle_span = abs(gauge_end_angle - gauge_start_angle)
    large_arc_flag = 1 if angle_span > math.pi else 0
    sweep_flag = 1
    rotated_start = gauge_start_angle + math.pi
    rotated_end = gauge_end_angle + math.pi
    
    gauge_arc_path = f"M {cx + gauge_radius * math.cos(rotated_start):.3f} {cy + gauge_radius * math.sin(rotated_start):.3f} A {gauge_radius} {gauge_radius} 0 {large_arc_flag} {sweep_flag} {cx + gauge_radius * math.cos(rotated_end):.3f} {cy + gauge_radius * math.sin(rotated_end):.3f}"
    create_element(gauge_group, "path", {"d": gauge_arc_path, "class": "gauge-arc"})
    
    # Value arc (initially empty)
    create_element(gauge_group, "path", {
        "id": f"{gauge_id}-value-arc",
        "class": "gauge-value-arc"
    })
    
    # Colored segments
    max_pressure = 500
    low_start = gauge_start_angle
    low_end = gauge_start_angle + (100 / max_pressure) * (gauge_end_angle - gauge_start_angle)
    yellow_end = gauge_start_angle + (150 / max_pressure) * (gauge_end_angle - gauge_start_angle)
    green_end = gauge_start_angle + (350 / max_pressure) * (gauge_end_angle - gauge_start_angle)
    high_end = gauge_start_angle + (500 / max_pressure) * (gauge_end_angle - gauge_start_angle)
    
    # Helper function for colored arcs
    def create_colored_arc(start, end, color, arc_id=None):
        angle_span = abs(end - start)
        large_arc = 1 if angle_span > math.pi else 0
        rotated_start = start + math.pi
        rotated_end = end + math.pi
        arc_path = f"M {cx + extra_radius2 * math.cos(rotated_start):.3f} {cy + extra_radius2 * math.sin(rotated_start):.3f} A {extra_radius2} {extra_radius2} 0 {large_arc} 1 {cx + extra_radius2 * math.cos(rotated_end):.3f} {cy + extra_radius2 * math.sin(rotated_end):.3f}"
        attribs = {
            "d": arc_path,
            "stroke": color,
            "stroke-width": "11",
            "fill": "none",
            "stroke-linecap": "round"
        }
        if arc_id:
            attribs["id"] = arc_id
        create_element(gauge_group, "path", attribs)
        return rotated_start, rotated_end, large_arc
    
    # Yellow segment (100-150)
    yellow_rs, yellow_re, yellow_la = create_colored_arc(low_end, yellow_end, "yellow", f"{gauge_id}-yellow-low-arc")
    
    # Low segment (0-100, red)
    low_rs, low_re, low_la = create_colored_arc(low_start, low_end, "red", f"{gauge_id}-low-arc")
    
    # Text path for LOW label
    low_text_arc = f"M {cx + (extra_radius2 - 2) * math.cos(low_rs):.3f} {cy + (extra_radius2 - 2) * math.sin(low_rs):.3f} A {extra_radius2 - 2} {extra_radius2 - 2} 0 {low_la} 1 {cx + (extra_radius2 - 2) * math.cos(low_re):.3f} {cy + (extra_radius2 - 2) * math.sin(low_re):.3f}"
    create_element(gauge_group, "path", {
        "d": low_text_arc,
        "id": f"{gauge_id}-low-text-path",
        "opacity": "0"
    })
    
    # Green segment (150-350)
    green_rs, green_re, green_la = create_colored_arc(yellow_end, green_end, "green", f"{gauge_id}-green-arc")
    
    # Text path for NORMAL label
    normal_text_arc = f"M {cx + (extra_radius2 + 1.0) * math.cos(green_rs):.3f} {cy + (extra_radius2 + 1.0) * math.sin(green_rs):.3f} A {extra_radius2 + 1.0} {extra_radius2 + 1.0} 0 {green_la} 1 {cx + (extra_radius2 + 1.0) * math.cos(green_re):.3f} {cy + (extra_radius2 + 1.0) * math.sin(green_re):.3f}"
    create_element(gauge_group, "path", {
        "d": normal_text_arc,
        "id": f"{gauge_id}-normal-text-path",
        "opacity": "0"
    })
    
    # High segment (350-500, yellow)
    high_rs, high_re, high_la = create_colored_arc(green_end, high_end, "yellow", f"{gauge_id}-yellow-high-arc")
    
    # High segment (350-500, yellow)
    high_rs, high_re, high_la = create_colored_arc(green_end, high_end, "yellow", f"{gauge_id}-yellow-high-arc")
    
    # Text path for HIGH label
    high_text_arc = f"M {cx + (extra_radius2 - 2) * math.cos(high_rs):.3f} {cy + (extra_radius2 - 2) * math.sin(high_rs):.3f} A {extra_radius2 - 2} {extra_radius2 - 2} 0 {high_la} 1 {cx + (extra_radius2 - 2) * math.cos(high_re):.3f} {cy + (extra_radius2 - 2) * math.sin(high_re):.3f}"
    create_element(gauge_group, "path", {
        "d": high_text_arc,
        "id": f"{gauge_id}-high-text-path",
        "opacity": "0"
    })
    
    # Labels
    low_label = create_element(gauge_group, "text", {"fill": "black", "font-size": "4px"})
    create_element(low_label, "textPath", {
        "href": f"#{gauge_id}-low-text-path",
        "startOffset": "50%",
        "text-anchor": "middle",
        "id": f"{gauge_id}-low-label"
    }, "LOW 100")
    
    normal_label = create_element(gauge_group, "text", {"fill": "black", "font-size": "4px"})
    create_element(normal_label, "textPath", {
        "href": f"#{gauge_id}-normal-text-path",
        "startOffset": "50%",
        "text-anchor": "middle",
        "id": f"{gauge_id}-normal-label"
    }, "NORMAL 250")
    
    # SET label path
    set_start_ratio = 200 / max_pressure
    set_end_ratio = 300 / max_pressure
    set_start_angle = gauge_start_angle + set_start_ratio * (gauge_end_angle - gauge_start_angle) + math.pi
    set_end_angle = gauge_start_angle + set_end_ratio * (gauge_end_angle - gauge_start_angle) + math.pi
    set_angle_span = abs(set_end_angle - set_start_angle)
    set_large_arc = 1 if set_angle_span > math.pi else 0
    set_text_arc = f"M {cx + (extra_radius2 - 4.5) * math.cos(set_start_angle):.3f} {cy + (extra_radius2 - 4.5) * math.sin(set_start_angle):.3f} A {extra_radius2 - 4.5} {extra_radius2 - 4.5} 0 {set_large_arc} 1 {cx + (extra_radius2 - 4.5) * math.cos(set_end_angle):.3f} {cy + (extra_radius2 - 4.5) * math.sin(set_end_angle):.3f}"
    create_element(gauge_group, "path", {
        "d": set_text_arc,
        "id": f"{gauge_id}-set-text-path",
        "opacity": "0"
    })
    
    set_label = create_element(gauge_group, "text", {"fill": "black", "font-size": "4px"})
    create_element(set_label, "textPath", {
        "href": f"#{gauge_id}-set-text-path",
        "startOffset": "50%",
        "text-anchor": "middle",
        "id": f"{gauge_id}-set-label"
    }, "SET 250")
    
    high_label = create_element(gauge_group, "text", {"fill": "black", "font-size": "4px"})
    create_element(high_label, "textPath", {
        "href": f"#{gauge_id}-high-text-path",
        "startOffset": "50%",
        "text-anchor": "middle",
        "id": f"{gauge_id}-high-label"
    }, "HIGH 350")
    
    # Tick marks
    num_ticks = 5
    for i in range(num_ticks + 1):
        pressure = (i * max_pressure) / num_ticks
        angle = gauge_start_angle + (i * (gauge_end_angle - gauge_start_angle)) / num_ticks
        tick_inner_radius = gauge_radius - 4
        tick_outer_radius = gauge_radius - 2
        tick_x1 = cx + tick_inner_radius * math.cos(angle)
        tick_y1 = cy + tick_inner_radius * math.sin(angle)
        tick_x2 = cx + tick_outer_radius * math.cos(angle)
        tick_y2 = cy + tick_outer_radius * math.sin(angle)
        tick_x1 = 2 * cx - tick_x1
        tick_y1 = 2 * cy - tick_y1
        tick_x2 = 2 * cx - tick_x2
        tick_y2 = 2 * cy - tick_y2
        
        create_element(gauge_group, "line", {
            "x1": tick_x1, "y1": tick_y1,
            "x2": tick_x2, "y2": tick_y2,
            "class": "gauge-tick"
        })
        
        if 0 <= i <= 5:
            label_radius = gauge_radius + 3
            label_x = cx + label_radius * math.cos(angle)
            label_y = cy + label_radius * math.sin(angle)
            label_x = 2 * cx - label_x
            label_y = 2 * cy - label_y
            radial_angle = math.atan2(label_y - cy, label_x - cx) * 180 / math.pi
            tangent_angle = radial_angle + 90
            create_element(gauge_group, "text", {
                "x": label_x, "y": label_y,
                "class": "gauge-label",
                "text-anchor": "middle",
                "dominant-baseline": "middle",
                "transform": f"rotate({tangent_angle}, {label_x}, {label_y})"
            }, str(int(pressure)))
    
    # Minor ticks
    for i in [0.5, 1.5, 2.5, 3.5, 4.5]:
        angle = gauge_start_angle + (i * (gauge_end_angle - gauge_start_angle)) / num_ticks
        tick_inner_radius = gauge_radius - 4
        tick_outer_radius = gauge_radius - 3
        tick_x1 = cx + tick_inner_radius * math.cos(angle)
        tick_y1 = cy + tick_inner_radius * math.sin(angle)
        tick_x2 = cx + tick_outer_radius * math.cos(angle)
        tick_y2 = cy + tick_outer_radius * math.sin(angle)
        tick_x1 = 2 * cx - tick_x1
        tick_y1 = 2 * cy - tick_y1
        tick_x2 = 2 * cx - tick_x2
        tick_y2 = 2 * cy - tick_y2
        create_element(gauge_group, "line", {
            "x1": tick_x1, "y1": tick_y1,
            "x2": tick_x2, "y2": tick_y2,
            "class": "gauge-tick"
        })
    
    # Indicator triangle (initially at 0)
    indicator_group = create_element(gauge_group, "g", {"class": "pressure-indicator"})
    create_element(indicator_group, "polygon", {
        "id": f"{gauge_id}-indicator",
        "points": "0,0 0,0 0,0",
        "class": "gauge-indicator"
    })
    
    # Pressure value and unit
    create_element(gauge_group, "text", {
        "id": f"{gauge_id}-value",
        "x": cx, "y": cy + 5.25,
        "class": "rpm-value",
        "text-anchor": "middle",
        "dominant-baseline": "middle"
    }, "0")
    
    create_element(gauge_group, "text", {
        "x": cx, "y": cy - 0.5,
        "class": "pressure-unit",
        "text-anchor": "middle",
        "dominant-baseline": "middle"
    }, "Pa")
    
    # Low pressure indicator (initially with opacity 0)
    low_label_x = cx - 3.5
    low_label_y = cy - 10.5
    low_indicator_group = create_element(gauge_group, "g", {
        "class": "low-pressure-indicator",
        "id": f"{gauge_id}-low-pressure-indicator",
        "transform": f"translate({low_label_x}, {low_label_y}) scale(0.5)",
        "opacity": "0"
    })
    
    # Path 1 - wavy arrow
    create_element(low_indicator_group, "path", {
        "d": "M 4 2 C 3 4, 5 6, 4 8 C 3 10, 5 12, 4 14",
        "marker-end": "url(#arrowhead)",
        "stroke": "black",
        "stroke-width": "1",
        "fill": "none"
    })
    
    # Path 2 - wavy arrow
    create_element(low_indicator_group, "path", {
        "d": "M 7 2 C 6 4, 8 6, 7 8 C 6 10, 8 12, 7 14",
        "marker-end": "url(#arrowhead)",
        "stroke": "black",
        "stroke-width": "1",
        "fill": "none"
    })
    
    # Vertical line
    create_element(low_indicator_group, "line", {
        "x1": "11.5", "y1": "2",
        "x2": "11.5", "y2": "14",
        "stroke": "black",
        "stroke-width": "1"
    })
    
    # Tick marks
    for y in [2, 5, 8, 11, 14]:
        create_element(low_indicator_group, "line", {
            "x1": "9.5", "y1": str(y),
            "x2": "11.5", "y2": str(y),
            "stroke": "black",
            "stroke-width": "1"
        })


def load_javascript_from_file(filepath):
    """Load JavaScript code from file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None


def main(output_filename: str = "te.svg"):
    """
    Generate te.svg programmatically.
    """
    # Create SVG root
    svg = ET.Element("svg", {
        "xmlns:dc": "http://purl.org/dc/elements/1.1/",
        "xmlns:cc": "http://creativecommons.org/ns#",
        "xmlns:rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "xmlns:svg": "http://www.w3.org/2000/svg",
        "xmlns": "http://www.w3.org/2000/svg",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "viewBox": "0 0 100 100",
        "width": "60mm",
        "height": "120mm",
        "version": "1.1",
        "id": "svgAirflowM1"
    })
    
    # Read simplified update-only JavaScript
    here = os.path.dirname(os.path.abspath(__file__))
    update_js_path = os.path.join(here, "js", "update.js")
    
    js_code = ""
    if os.path.exists(update_js_path):
        # Read the update.js file
        with open(update_js_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
    
    # Embed JavaScript with proper CDATA wrapping
    if js_code:
        script = create_element(svg, "script", {"type": "text/javascript"})
        script.text = f"\n    <![CDATA[\n{js_code}\n    ]]>\n  "
    
    # Add title
    #create_element(svg, "title", text="Clickable Power Button Components (ID-Styled)")
    
    # Create defs with styles
    defs = create_element(svg, "defs")
    
    # Get paths
    here = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(here, "style/defs.xml")
    
    # Filters
    blur_filter = create_element(defs, "filter", {
        "id": "blur-effect",
        "x": "-50%", "y": "-50%",
        "width": "200%", "height": "200%"
    })
    create_element(blur_filter, "feGaussianBlur", {
        "in": "SourceGraphic",
        "stdDeviation": "1.5"
    })
    
    # Extract and add styles from teXXX.svg
    if os.path.exists(style_path):
        tree = ET.parse(style_path)
        root = tree.getroot()
         
        for style_elem in root.findall("style"):
            if style_elem.text:
                style = create_element(defs, "style")
                style.text = style_elem.text
                break
    
    # Gradients
    anim_gradient = create_element(defs, "radialGradient", {
        "id": "animated-bg-gradient",
        "cx": "50%", "cy": "50%", "r": "50%"
    })
    create_element(anim_gradient, "stop", {
        "offset": "0%",
        "style": "stop-color:#B0E0E6;stop-opacity:1.0"
    })
    create_element(anim_gradient, "stop", {
        "offset": "50%",
        "style": "stop-color:#87CEEB;stop-opacity:1.0"
    })
    create_element(anim_gradient, "stop", {
        "offset": "100%",
        "style": "stop-color:#4682B4;stop-opacity:0.9"
    })
    
    disk_gradient = create_element(defs, "radialGradient", {
        "id": "disk-gradient",
        "cx": "50%", "cy": "50%", "r": "50%"
    })
    create_element(disk_gradient, "stop", {
        "offset": "0%",
        "style": "stop-color:#FFFFFF;stop-opacity:1.0"
    })
    create_element(disk_gradient, "stop", {
        "offset": "70%",
        "style": "stop-color:#F0F0F0;stop-opacity:1.0"
    })
    create_element(disk_gradient, "stop", {
        "offset": "100%",
        "style": "stop-color:#DADADA;stop-opacity:1.0"
    })
    
    red_gradient = create_element(defs, "radialGradient", {
        "id": "red-gradient",
        "cx": "50%", "cy": "50%", "r": "50%"
    })
    create_element(red_gradient, "stop", {
        "offset": "0%",
        "style": "stop-color:#FF0000;stop-opacity:1.0"
    })
    create_element(red_gradient, "stop", {
        "offset": "100%",
        "style": "stop-color:#800000;stop-opacity:1.0"
    })
    
    status_red_gradient = create_element(defs, "radialGradient", {
        "id": "status-red-gradient",
        "cx": "50%", "cy": "50%", "r": "50%"
    })
    create_element(status_red_gradient, "stop", {
        "offset": "0%",
        "style": "stop-color:#FF0000;stop-opacity:1.0"
    })
    create_element(status_red_gradient, "stop", {
        "offset": "100%",
        "style": "stop-color:#800000;stop-opacity:1.0"
    })
    
    # Marker for arrowhead
    marker = create_element(defs, "marker", {
        "id": "arrowhead",
        "markerWidth": "3",
        "markerHeight": "3",
        "refX": "1.5",
        "refY": "1.5",
        "orient": "auto",
        "markerUnits": "strokeWidth"
    })
    create_element(marker, "polygon", {
        "points": "0 0, 3 1.5, 0 3",
        "fill": "black"
    })
    
    # Background
    create_element(svg, "rect", {
        "x": "0", "y": "-50",
        "width": "80", "height": "160",
        "fill": "#000011"
    })
    
    # Containers for dynamic elements (exhaust and starfield)
    exhaust_container_1 = create_element(svg, "g", {"id": "exhaust-container-1"})
    exhaust_container_2 = create_element(svg, "g", {"id": "exhaust-container-2"})
    exhaust_container_center = create_element(svg, "g", {"id": "exhaust-container-center"})
    
    # Create exhaust particles (static elements, animated by CSS)
    create_exhaust(exhaust_container_1, 15, 78, 10, 3)
    create_exhaust(exhaust_container_2, 65, 78, 10, 3)
    create_exhaust(exhaust_container_center, 40, 78, 24, 3)
    
    # Create starfield (static elements with SMIL animation)
    starfield_container = create_element(svg, "g", {"id": "starfield-container"})
    create_starfield(starfield_container, 75)
    
    # System indicator
    system_indicator = create_element(svg, "g", {"id": "system-indicator"})
    create_element(system_indicator, "rect", {
        "x": "15.4", "y": "-37.9",
        "width": "49.5", "height": "100",
        "rx": "5", "ry": "5",
        "fill": "silver",
        "stroke": "silver",
        "stroke-width": "1"
    })
    create_element(system_indicator, "text", {
        "x": "32", "y": "36",
        "class": "fan-label"
    }, "SYSTEM")
    create_element(system_indicator, "circle", {
        "cx": "40", "cy": "47.75", "r": "8",
        "fill": "white",
        "stroke": "black",
        "stroke-width": "1",
        "id": "no-errors-bg"
    })
    create_element(system_indicator, "circle", {
        "cx": "40", "cy": "47.75", "r": "8",
        "fill": "green",
        "class": "status-active",
        "id": "no-errors-disc"
    })
    create_element(system_indicator, "text", {
        "x": "40", "y": "48.75",
        "text-anchor": "middle",
        "dominant-baseline": "middle",
        "font-size": "10",
        "font-weight": "bold",
        "id": "no-errors-symbol"
    }, "✓")
    
    # Background rectangles
    create_element(svg, "rect", {
        "id": "rect-behind-pressure-value",
        "x": "18", "y": "-39",
        "width": "44", "height": "35",
        "fill": "url(#disk-gradient)"
    })
    create_element(svg, "rect", {
        "id": "rect-behind-speed-value",
        "x": "20", "y": "17",
        "width": "40", "height": "10",
        "fill": "url(#disk-gradient)"
    })
    
    # Gauges
    fanspeed_container = create_element(svg, "g", {"id": "fanspeed-container"})
    create_rpm_gauge(fanspeed_container, 40, 18, "fanspeed")
    
    pressure_container = create_element(svg, "g", {"id": "pressure-container"})
    create_pressure_gauge(pressure_container, 40, -13, "pressure")
    
    # Status indicators
    status_indicators_fan1 = create_element(svg, "g", {"id": "status-indicators-fan1"})
    fuse_fan1 = create_element(status_indicators_fan1, "g", {"id": "fuse-fan1"})
    create_element(fuse_fan1, "rect", {
        "x": "5", "y": "25",
        "width": "20", "height": "51",
        "rx": "5", "ry": "5",
        "fill": "silver",
        "stroke": "black",
        "stroke-width": "1"
    })
    create_element(fuse_fan1, "circle", {
        "cx": "10", "cy": "71", "r": "4",
        "fill": "black"
    })
    create_element(fuse_fan1, "circle", {
        "id": "status-Fuse_Fan1",
        "cx": "10", "cy": "71", "r": "3",
        "fill": "#00FF00",
        "class": "status-active"
    })
    create_element(fuse_fan1, "rect", {
        "x": "8.5", "y": "70",
        "width": "3", "height": "2",
        "fill": "transparent",
        "stroke": "black",
        "stroke-width": "0.5"
    })
    create_element(fuse_fan1, "line", {
        "x1": "7.5", "y1": "71",
        "x2": "12.5", "y2": "71",
        "stroke": "black",
        "stroke-width": "0.5"
    })
    
    feedback_k1 = create_element(status_indicators_fan1, "g", {"id": "feedback-k1"})
    create_element(feedback_k1, "circle", {
        "cx": "20", "cy": "71", "r": "4",
        "fill": "black"
    })
    create_element(feedback_k1, "circle", {
        "id": "status-Feedback_K1",
        "cx": "20", "cy": "71", "r": "3",
        "fill": "#00FF00",
        "class": "status-active"
    })
    create_element(feedback_k1, "path", {
        "d": "M 22 70 L 21.5 71 L 22.5 71 Z",
        "fill": "black"
    })
    create_element(feedback_k1, "path", {
        "d": "M 22 71 A 2 2 0 1 1 21.732 70",
        "stroke": "black",
        "fill": "none",
        "stroke-width": "0.5"
    })
    
    # Dryer indicator
    dryer_indicator = create_element(svg, "g", {"id": "dryer-indicator"})
    create_element(dryer_indicator, "rect", {
        "x": "25", "y": "60",
        "width": "30", "height": "17",
        "rx": "5", "ry": "5",
        "fill": "silver",
        "stroke": "black",
        "stroke-width": "1"
    })
    create_element(dryer_indicator, "text", {
        "x": "34", "y": "65",
        "class": "fan-label"
    }, "DRYER")
    
    fuse_dryer = create_element(dryer_indicator, "g", {"id": "fuse-dryer"})
    create_element(fuse_dryer, "circle", {
        "cx": "35", "cy": "71", "r": "4",
        "fill": "black"
    })
    create_element(fuse_dryer, "circle", {
        "id": "status-Fuse_Dryer",
        "cx": "35", "cy": "71", "r": "3",
        "fill": "#FF0000",
        "class": "status-active"
    })
    create_element(fuse_dryer, "rect", {
        "x": "33.5", "y": "70",
        "width": "3", "height": "2",
        "fill": "transparent",
        "stroke": "black",
        "stroke-width": "0.5"
    })
    create_element(fuse_dryer, "line", {
        "x1": "32.5", "y1": "71",
        "x2": "37.5", "y2": "71",
        "stroke": "black",
        "stroke-width": "0.5"
    })
    
    feedback_watchdog = create_element(dryer_indicator, "g", {"id": "feedback-watchdog"})
    create_element(feedback_watchdog, "circle", {
        "cx": "45", "cy": "71", "r": "4",
        "fill": "black"
    })
    create_element(feedback_watchdog, "circle", {
        "id": "status-FeedbackPipeWatchdog",
        "cx": "45", "cy": "71", "r": "3",
        "fill": "#00FF00",
        "class": "status-active"
    })
    create_element(feedback_watchdog, "path", {
        "d": "M 47 70 L 46.5 71 L 47.5 71 Z",
        "fill": "black"
    })
    create_element(feedback_watchdog, "path", {
        "d": "M 47 71 A 2 2 0 1 1 46.732 70",
        "stroke": "black",
        "fill": "none",
        "stroke-width": "0.5"
    })
    
    # Status indicators Fan 2
    status_indicators_fan2 = create_element(svg, "g", {"id": "status-indicators-fan2"})
    fuse_fan2 = create_element(status_indicators_fan2, "g", {"id": "fuse-fan2"})
    create_element(fuse_fan2, "rect", {
        "x": "55", "y": "25",
        "width": "20", "height": "51",
        "rx": "5", "ry": "5",
        "fill": "silver",
        "stroke": "black",
        "stroke-width": "1"
    })
    create_element(fuse_fan2, "circle", {
        "cx": "60", "cy": "71", "r": "4",
        "fill": "black"
    })
    create_element(fuse_fan2, "circle", {
        "id": "status-Fuse_Fan2",
        "cx": "60", "cy": "71", "r": "3",
        "fill": "gray"
    })
    create_element(fuse_fan2, "rect", {
        "x": "58.5", "y": "70",
        "width": "3", "height": "2",
        "fill": "transparent",
        "stroke": "black",
        "stroke-width": "0.5"
    })
    create_element(fuse_fan2, "line", {
        "x1": "57.5", "y1": "71",
        "x2": "62.5", "y2": "71",
        "stroke": "black",
        "stroke-width": "0.5"
    })
    
    feedback_k2 = create_element(status_indicators_fan2, "g", {"id": "feedback-k2"})
    create_element(feedback_k2, "circle", {
        "cx": "70", "cy": "71", "r": "4",
        "fill": "black"
    })
    create_element(feedback_k2, "circle", {
        "id": "status-Feedback_K2",
        "cx": "70", "cy": "71", "r": "3",
        "fill": "gray"
    })
    create_element(feedback_k2, "path", {
        "d": "M 72 70 L 71.5 71 L 72.5 71 Z",
        "fill": "black"
    })
    create_element(feedback_k2, "path", {
        "d": "M 72 71 A 2 2 0 1 1 71.732 70",
        "stroke": "black",
        "fill": "none",
        "stroke-width": "0.5"
    })
    
    # Fan containers
    power_fan1_container = create_element(svg, "g", {"id": "power-fan1-container"})
    create_fan(power_fan1_container, 10, 50, 10, 0.75, "power-fan1", "on")
    
    power_fan2_container = create_element(svg, "g", {"id": "power-fan2-container"})
    create_fan(power_fan2_container, 60, 50, 10, 0.75, "power-fan2", "off")
    
    # Write to file
    tree = ET.ElementTree(svg)
    ET.indent(tree, space="  ")
    
    # Write to string first
    import io
    stream = io.BytesIO()
    tree.write(stream, encoding="utf-8", xml_declaration=False)
    svg_content = stream.getvalue().decode('utf-8')
    
    # Prepend XML declaration
    svg_content = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + svg_content
    
    # Fix escaped entities in JavaScript CDATA sections
    svg_content = svg_content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    
    # Write final content
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"✓ {output_filename} generated successfully using Python functions")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate te.svg using Python functions"
    )
    parser.add_argument(
        "output", 
        nargs="?", 
        default="te.svg", 
        help="Output SVG file path (default: te.svg)"
    )
    args = parser.parse_args()
    exit(main(args.output))
