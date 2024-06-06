import re

def extract_json_from_markdown(markdown: str) -> str:
    json_match = re.search(r'```json\n([\s\S]+?)\n```', markdown)
    if json_match:
        return json_match.group(1)
    return markdown
