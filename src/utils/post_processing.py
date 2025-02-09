import re
import json

def extract_json_objects(text):
    json_pattern = r'\{.*?\}'
    json_matches = re.findall(json_pattern, text, re.DOTALL)
    json_objects = []
    
    for match in json_matches:
        try:
            json_obj = json.loads(match)
            json_objects.append(json_obj)
        except json.JSONDecodeError:
            continue
    
    return json_objects

def display_json(json, html=False):
    '''Displays the extracted json data.'''
    from json2html import json2html
    from IPython.display import HTML, display
    if html:
        html_table = json2html.convert(json=json)
        display(HTML(html_table))
    else:
        display(json)