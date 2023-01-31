from rich import print
from pathlib import Path
import tinycss

css_file = Path("./pyguis/css/layout.css")
parser = tinycss.make_parser()
stylesheet = parser.parse_stylesheet(css_file.read_text())

rules = stylesheet.rules
print(f'Rules: {len(rules)}')

# Assert our rules
for r in rules:
    assert len([rr.as_css() for rr in r.selector]) == 1, f"use single selector"

# Find grid-template-areas under body
selectors = {idx: [rr.as_css() for rr in r.selector][0] for idx, r in enumerate(rules)}
print(selectors)

dnames = {
    selectors[idx]: [rr.name for rr in r.declarations] for idx, r in enumerate(rules)
}
print(dnames)

# breakpoint()
