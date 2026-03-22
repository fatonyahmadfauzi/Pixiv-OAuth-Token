import re
import sys
from pathlib import Path

def clean_readme(input_path, output_path):
    text = Path(input_path).read_text(encoding='utf-8')
    
    # Remove the language link
    text = re.sub(r'(?m)^> 🌐 Available in other languages:.*$', '', text)
    
    # Convert local markdown links to absolute github links
    # Matches [Text](link) where link does not start with http or #
    def replacer(m):
        link = m.group(1)
        if link.startswith('http') or link.startswith('#') or link.startswith('mailto:'):
            return m.group(0) # Keep unchanged
        # It's a local link, prepend github repo base URL
        base_url = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/blob/main/"
        return f"]({base_url}{link})"
    
    text = re.sub(r'\]\(([^)]+)\)', replacer, text)
    
    # Remove excessive blank lines if any were left by the removal
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip() + '\n'
    
    Path(output_path).write_text(text, encoding='utf-8')

if __name__ == "__main__":
    if len(sys.argv) == 3:
        clean_readme(sys.argv[1], sys.argv[2])
