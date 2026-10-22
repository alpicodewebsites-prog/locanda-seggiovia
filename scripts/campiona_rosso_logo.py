from PIL import Image
from collections import Counter
import pathlib

p = pathlib.Path("src/assets/locanda-logo.png")
im = Image.open(p).convert("RGBA")
print(f"  logo: {im.size[0]}x{im.size[1]}")

# Solo i pixel opachi e chiaramente rossi (R molto piu' alto di G e B).
rossi = []
for r, g, b, a in im.getdata():
    if a < 200:
        continue
    if r > 90 and r - g > 45 and r - b > 45:
        rossi.append((r, g, b))

print(f"  pixel rossi opachi: {len(rossi)}")
if rossi:
    c = Counter(rossi)
    print("  i 6 rossi piu' frequenti:")
    for (r, g, b), n in c.most_common(6):
        print(f"    #{r:02x}{g:02x}{b:02x}  {n} pixel")
    mr = sum(x[0] for x in rossi) // len(rossi)
    mg = sum(x[1] for x in rossi) // len(rossi)
    mb = sum(x[2] for x in rossi) // len(rossi)
    print(f"  media: #{mr:02x}{mg:02x}{mb:02x}")
