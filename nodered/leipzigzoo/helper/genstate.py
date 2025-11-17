import json
import re
import uuid

def generate_id():
    """Generates a random 16-character hexadecimal ID."""
    return uuid.uuid4().hex[:16]

def sanitize(text):
    """Cleans a string to be a valid JavaScript variable name component."""
    # Special case for multiple exclamation marks
    if re.fullmatch(r'!+', text):
        return "alarm"
        
    # Remove trailing exclamation marks
    text = text.rstrip('!')
    
    # Replace any non-alphanumeric characters with an underscore
    text = re.sub(r'[^\w\s-]', '_', text)
    # Replace whitespace and hyphens with a single underscore
    text = re.sub(r'[\s-]+', '_', text)
    # Replace multiple consecutive underscores with a single one
    text = re.sub(r'_+', '_', text)
    # Remove leading or trailing underscores
    text = text.strip('_')
    return text

def get_precision_from_value(value_str):
    """Calculates the number of decimal places in a string value."""
    # Clean the value string to handle cases like '-0.5'
    cleaned_value = value_str.strip()
    if '.' in cleaned_value:
        return len(cleaned_value.split('.')[-1])
    return 0

def process_data(file_path):
    """
    Reads the input file, processes the data, and returns a list of Node-RED nodes.
    """
    all_nodes = []
    x, y = 150, 100
    x_increment = 300
    max_x = 2400

    icpdas_precision_map = {
        'AI02': 0, 'AI05': 0, 'AI09': 0, 'AI10': 0,
        'AI07': 2, 'AI08': 2, 'AI11': 2, 'AI12': 2,
        'AI13': 2, 'AI14': 2, 'AI15': 2, 'AI16': 2
    }
    icpdas_keyword_map = {
        'AI02': 'pressure', 'AI05': 'pressure', 'AI09': 'snow', 'AI10': 'snow',
        'AI07': 'flow', 'AI08': 'flow', 'AI11': 'flow', 'AI12': 'flow',
        'AI13': 'flow', 'AI14': 'flow', 'AI15': 'flow', 'AI16': 'flow'
    }

    unit_map = {
        'pressure': 'Pa',
        'temperature': 'C',
        'flow': 'm/s',
        'druck': 'Pa',
        'temperatur': 'C',
        'durchfluss': 'm/s',
        'humidity': '', # Set to empty to avoid unsupported unit error
        'feuchte': ''   # Set to empty to avoid unsupported unit error
    }

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    full_data_lines = []
    previous_line = ""
    # Consolidate multi-line descriptions first
    for line in lines:
        line = line.strip()
        if not line or 'state_value' in line:
            continue
        if line.count(',') >= 3:
            if previous_line:
                full_data_lines.append(previous_line)
            previous_line = line
        else:
            previous_line += " " + line
    if previous_line:
        full_data_lines.append(previous_line)

    for line in full_data_lines:
        try:
            val_str, field, measurement, topic = [part.strip() for part in line.split(',')]
        except ValueError:
            # Handle lines that don't split into exactly 4 parts
            # This can happen with the icpdas data
            parts = [p.strip() for p in line.split(',')]
            if len(parts) == 4:
                 val_str, field, measurement, topic = parts
            elif 'icpdas' in line:
                val_str, field, measurement, topic = parts[0], parts[1], parts[2], parts[3] if len(parts) > 3 else "leipzigzoo/icpdas01"
            else:
                continue


        project = "leipzigzoo"
        name, lbl, tags_list, data_type, precision, unit = "", "", [], "num", "0", ""

        if 'icpdas01' in topic:
            device = "icpdas01"
            clean_field = field.replace('-', '')
            name = f"{project}_{device}_{clean_field}"
            
            keyword = icpdas_keyword_map.get(clean_field, 'value')
            lbl_name = f"LZ_{device}_{clean_field}_{keyword}"
            
            tags_list = [project, device, keyword]
            data_type = "num"
            precision = str(icpdas_precision_map.get(clean_field, get_precision_from_value(val_str)))
            unit = unit_map.get(keyword, "")

        else:
            topic_parts = topic.split('|')
            if len(topic_parts) != 3:
                continue

            device_part, address, description = topic_parts
            device = device_part.split('/')[-1]

            s_address = sanitize(address)
            s_description = sanitize(description)

            name = f"{project}_{device}_{s_address}"
            lbl_name = f"LZ_{device}_{s_address}_{s_description}"
            
            data_type = "bool" if "_BI" in address else "num"
            precision = "0" if data_type == "bool" else str(get_precision_from_value(val_str))
            
            keyword = 'unknown'
            # Find the appropriate keyword and unit
            for key in unit_map:
                if key in description.lower():
                    keyword = key
                    unit = unit_map.get(key, "")
                    break
            
            if 'störung' in description.lower() or 'alarm' in s_description.lower():
                keyword = 'störung'
            elif s_description == 'alarm':
                 keyword = 'alarm'


            tags_list = [project, device, keyword]

        state_id = generate_id()
        z_id = "c0292dea32408fa2"

        shared_state_node = {
            "id": state_id, "type": "shared-state", "name": name, "lbl": lbl_name,
            "tags": ",".join(tags_list), "historyCount": 2, "dataType": data_type,
            "boolType": "bool", "boolStrTrue": "", "boolStrFalse": "",
            "precision": precision, "numMin": "", "numMax": "", "unit": unit,
            "saveInterval": "30000"
        }

        get_state_node = {
            "id": generate_id(), "type": "get-shared-state", "z": z_id, "state": state_id,
            "name": lbl_name, "triggerOnInit": True, "triggerOnChange": True,
            "x": x, "y": y, "wires": [[]]
        }

        set_state_node = {
            "id": generate_id(), "type": "set-shared-state", "z": z_id, "state": state_id,
            "name": lbl_name, "triggerOnInit": True, "triggerOnChange": True,
            "provideOutput": True, "outputs": 1, "x": x, "y": y + 60, "wires": [[]]
        }

        all_nodes.extend([shared_state_node, get_state_node, set_state_node])

        x += x_increment
        if x > max_x:
            x = 150
            y += 200

    return all_nodes

if __name__ == "__main__":
    try:
        nodes = process_data('values.txt')
        print(json.dumps(nodes, indent=4, ensure_ascii=False))
    except FileNotFoundError:
        print("Error: 'values.txt' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
