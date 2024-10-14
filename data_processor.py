import re
import pandas as pd
import io

def parse_and_process_markdown(file_path):
    root = _parse_markdown(file_path)
    return _process_section(root)

def _parse_markdown(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    lines = content.split('\n')
    
    root = {'title': 'Root', 'level': 0, 'content': [], 'subsections': [], 'categories': []}
    section_stack = [root]
    
    for line in lines:
        if line.strip().startswith('#'):
            _process_header(line, section_stack)
        elif '|' in line:
            _process_table_line(line, section_stack)
        else:
            _process_text_line(line, section_stack)
    
    return root

def _process_header(line, section_stack):
    level = len(re.match(r'^#+', line).group())
    title = line.strip('#').strip()
    
    new_section = {
        'title': title, 
        'level': level, 
        'content': [], 
        'subsections': [], 
        'categories': []
    }
    
    while section_stack[-1]['level'] >= level:
        section_stack.pop()
    
    new_section['categories'] = [s['title'] for s in section_stack] + [title]
    
    section_stack[-1]['subsections'].append(new_section)
    section_stack.append(new_section)

def _process_table_line(line, section_stack):
    if not section_stack[-1]['content'] or not isinstance(section_stack[-1]['content'][-1], list):
        section_stack[-1]['content'].append([])
    section_stack[-1]['content'][-1].append(line)

def _process_text_line(line, section_stack):
    if line.strip():
        section_stack[-1]['content'].append(line.strip())

def _process_section(section):
    processed_content = []
    for item in section['content']:
        if isinstance(item, list):
            processed_content.append(_process_table(item))
        else:
            processed_content.append(item)
    
    processed_subsections = [_process_section(subsection) for subsection in section['subsections']]
    
    return {
        'title': section['title'],
        'level': section['level'],
        'content': processed_content,
        'subsections': processed_subsections,
        'categories': section['categories']
    }

def _process_table(table_lines):
    table_str = '\n'.join(table_lines)
    df = pd.read_csv(io.StringIO(table_str), sep='|', skipinitialspace=True).dropna(axis=1, how='all')
    df.columns = df.columns.str.strip()
    return df

def print_parsed_markdown(section, indent=0):
    print("  " * indent + f"Section: {section['title']} (Level: {section['level']}, Categories: {' > '.join(section['categories'])})")
    for item in section['content']:
        if isinstance(item, pd.DataFrame):
            print("  " * (indent + 1) + "Table:")
            print(item.to_string(index=False))
        else:
            print("  " * (indent + 1) + f"Text: {item}")
    
    for subsection in section['subsections']:
        print_parsed_markdown(subsection, indent + 1)
