import sys
import json
import xml.etree.ElementTree as xml
import xml.dom.minidom as minidom

ELEMENT_KEY = "el"
REPEAT_KEY = "repeat"
ATTRIBUTES_KEY = "attr"
ATTRIBUTE_PROVIDERS_KEY = "attr_providers"
INNER_TEXT_KEY = "inner"
INNER_TEXT_PROVIDERS_KEY = "inner_providers"
CHILDREN_KEY = "children"
REPEAT_MODS_KEY = "repeat_mods"
ADD_KEY = "ADD"
APPEND_KEY = "APPEND"
DELIMETER = ":"
INDEX_KEY = "IDX"

if (len(sys.argv) == 1):
    print "!!! Please provide a JSON file to parse !!!"
    sys.exit(1)
json_file_name = sys.argv[1]
json_file = json.load(open(json_file_name))
if (ELEMENT_KEY not in json_file):
    print "!!! JSON file must include at least one 'element' value !!!"
    sys.exit(2)
elements_to_visit = []

def add_to_xml(json_el, xml_el=None):
    repeat_mods = parse_all_repeat_mods(json_el)
    for i in range(json_el.get(REPEAT_KEY, 1)):
        created_xml = None
        if xml_el is None:
            created_xml = xml.Element(json_el[ELEMENT_KEY])
        else:
            created_xml = xml.SubElement(xml_el, json_el[ELEMENT_KEY])
        if INNER_TEXT_KEY in json_el:
            created_xml.text = json_el[INNER_TEXT_KEY]
        elif INNER_TEXT_PROVIDERS_KEY in json_el:
            created_xml.text = json_el[INNER_TEXT_PROVIDERS_KEY][i]
        for attr in json_el.get(ATTRIBUTES_KEY, {}):
            created_xml.set(attr, json_el[ATTRIBUTES_KEY][attr])
        for attr_provider in json_el.get(ATTRIBUTE_PROVIDERS_KEY, {}):
            created_xml.set(attr_provider, json_el[ATTRIBUTE_PROVIDERS_KEY][attr_provider][i])
        for mod in repeat_mods:
            mod(created_xml, i)
        for child in json_el.get(CHILDREN_KEY, []):
            add_to_xml(child, created_xml)
    return created_xml

def parse_all_repeat_mods(json_el):
    repeat_mods = []
    for mod in json_el.get(REPEAT_MODS_KEY, []) :
        repeat_mods.append(parse_repeat_mod(mod, json_el))
    return [mod for mod in repeat_mods if mod]

def is_int(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b

def parse_number(str_value):
    return int(str_value) if is_int(str_value) else float(str_value)

def parse_repeat_mod(mod_target, json_el):
    args = json_el[REPEAT_MODS_KEY][mod_target].split(DELIMETER)
    type = args[0]
    value = args[1]
    if type == ADD_KEY:
        value = parse_number(value)
        return lambda xml_el, index: xml_el.set(mod_target, str(index * value + parse_number(xml_el.get(mod_target))))
    elif type == APPEND_KEY:
        if value == INDEX_KEY:
            return lambda xml_el, index: xml_el.set(mod_target, xml_el.get(mod_target) + str(index))
        type = json_el[REPEAT_MODS_KEY][mod_target]
    print "Repeat mod of '{}' in '{}' element not supported. Skipping".format(type, json_el[ELEMENT_KEY])
    return None

xml_tree = add_to_xml(json_file)
minidom_xml = minidom.parseString(xml.tostring(xml_tree))
pretty_xml = minidom_xml.toprettyxml()
out_file_name = "{}.out.xml".format(json_file_name)
file = open(out_file_name, 'w')
file.write(pretty_xml)
file.close()
