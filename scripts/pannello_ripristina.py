import pathlib, re

p = pathlib.Path("public/admin/config.yml")
t = p.read_text(encoding="utf-8")
marcatore = "# ==========================================================================\n# LE VERSIONI INGLESI\n"
if marcatore in t:
    t = t[: t.index(marcatore)].rstrip("\n") + "\n"
    p.write_text(t, encoding="utf-8", newline="")
    print("  sezione inglese rimossa, si riparte da quelle italiane")
print(f"  righe: {len(t.splitlines())}")
