from json import dump
from os import walk

lines = []
terms = {}

# Get list of all directoring without any ignore keywords
d_ignore = ["git"]
all_dirs = [d[0] for d in walk("./") if not any(i in d[0] for i in d_ignore)];

for a,b,c in walk("./"):
    if not any(i in a for i in d_ignore):
        print(a, b, c)
        print()

print(all_dirs)

with open("unparsed_index.html", "r") as f:
    for line in f:
        line_split = line.split("$")
        if len(line_split) > 1:
            for i in range(1, len(line_split), 2):
                obj = line_split[i].replace("$", "")
                for d in all_dirs:
                    if obj in d:
                        html = "<a href=\"" + d + "/index.html\">" + obj + "</a>"
                        break
                line_split[i] = html
            line = "".join(line_split)
        lines.append(line)
    print(terms)

with open("index.html", "w") as f:
    for line in lines:
        f.write(line)

with open("term.json", "w") as f:
    dump(terms, f, indent=2)
