from json import dump
from os import walk
from os import path
from os import chdir
from os import listdir

terms = {}

# Get list of all directoring without any ignore keywords
d_ignore = ["git", "scripts"]
all_dirs = [d[0] for d in walk("./") if not any(i in d[0] for i in d_ignore)];
all_dirs_rel = all_dirs.copy()

for i in range(len(all_dirs)):
    chdir(all_dirs_rel[i])
    depth = len([x for x in all_dirs[i].split("/") if x != '']) - 1
    all_dirs_rel = ["../" * depth + i for i in all_dirs] # Probably dont need all of these

    if "unparsed_index.html" in listdir("./"):
        lines = []
        with open("unparsed_index.html", "r") as f:
            for line in f:
                line_split = line.split("$")
                if len(line_split) > 1:
                    for i in range(1, len(line_split), 2):
                        obj = line_split[i].replace("$", "")
                        for d in all_dirs:
                            if obj in d: # Object name is in directory name
                                html = "<a href=\"" + path.join(d, "index.html")  + "\">" + obj + "</a>"
                                line_split[i] = html
                                break
                    line = "".join(line_split)
                lines.append("\t\t" + line)

        with open("index.html", "w") as f:
            with open(path.join(all_dirs_rel[0], "templates", "header.html"), "r") as header:
                for h in header:
                    f.write(h)

            f.write(f"\t\t<base href=\"{all_dirs_rel[0]}\">\n")

            with open(path.join(all_dirs_rel[0], "templates", "middle.html"), "r") as middle:
                for m in middle:
                    f.write(m)

            for line in lines:
                f.write(line)

            with open(path.join(all_dirs_rel[0], "templates", "footer.html"), "r") as footer:
                for ft in footer:
                    f.write(ft)

print("Done parsing")
