

with open("profile.md","r") as f:
    content=f.read()
lines=content.split("\n")
id = set()
for line in lines:
    if line.startswith("["):
        id.add(line[1:line.find("]")])

print(id)