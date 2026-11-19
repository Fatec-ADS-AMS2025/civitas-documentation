"""Verificações estáticas do Capítulo 6 (não substituem a compilação LaTeX)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
chapter = (ROOT / "capitulos" / "capitulo6.tex").read_text(encoding="utf-8")
main = (ROOT / "01Projeto.tex").read_text(encoding="utf-8")
others = main + "".join(
    (ROOT / "capitulos" / name).read_text(encoding="utf-8")
    for name in ("capitulo3.tex", "capitulo4.tex")
)
bib = (ROOT / "bibliografia.bib").read_text(encoding="utf-8")

assert main.count(r"\input{capitulos/capitulo6}") == 1
assert r"\chapter{Arquitetura de Software}" not in main

headings = re.findall(r"\\(chapter|section|subsection)\{([^}]+)\}", chapter)
assert headings == [
    ("chapter", "Arquitetura de Software"),
    ("section", "Arquitetura de Desenvolvimento"),
    ("subsection", "Back-End"),
    ("subsection", "Front-End"),
    ("section", "Segurança da Informação"),
], headings

legacy = re.compile(
    r"Comtur|SeniorCare|SeniorStock|turis|residente|enfermeiro|prontuário|"
    r"Flutter|\bDart\b|Azure DevOps|Startup\.cs",
    re.IGNORECASE,
)
assert not legacy.search(chapter), legacy.search(chapter)
for removed in ("Comtur", "Flutter", "Azure DevOps"):
    assert removed not in main, f"{removed} ainda presente em 01Projeto.tex"

for environment in ("figure", "quadro", "tabularx"):
    assert chapter.count(r"\begin{" + environment + "}") == chapter.count(
        r"\end{" + environment + "}"
    ), environment

labels = re.findall(r"\\label\{([^}]+)\}", chapter)
assert len(labels) == len(set(labels)), "Rótulo repetido no Capítulo 6"
other_labels = set(re.findall(r"\\label\{([^}]+)\}", others))
assert not (set(labels) & other_labels), "Rótulo repetido em outro arquivo"
refs = set(re.findall(r"\\(?:auto)?ref\{([^}]+)\}", chapter))
assert not (refs - set(labels) - other_labels), refs - set(labels) - other_labels

entries = re.findall(r"@\w+\{([^,\s]+),", bib)
duplicates = {key for key in entries if entries.count(key) > 1}
cites = set()
for group in re.findall(r"\\(?:paren|text|foot)?cite\{([^}]+)\}", chapter):
    cites.update(key.strip() for key in group.split(","))
assert not (cites - set(entries)), f"Citações sem bibliografia: {cites - set(entries)}"
assert not (cites & duplicates), f"Citações com chave duplicada: {cites & duplicates}"

# Caracteres especiais fora de ambientes verbatim: nenhum sem escape
body = re.sub(r"\\parencite\{[^}]*\}|\\textcite\{[^}]*\}|\\label\{[^}]*\}|\\ref\{[^}]*\}|\\input\{[^}]*\}|\\includegraphics(\[[^\]]*\])?\{[^}]*\}", "", chapter)
for pattern, name in ((r"(?<!\\)_", "_"), (r"(?<!\\)#", "#"), (r"(?<!\\)%", "%"), (r"(?<!\\)\$", "$")):
    assert not re.search(pattern, body), f"Caractere sem escape: {name}"
depth = 0
for character_index, character in enumerate(body):
    if character == "{" and body[character_index - 1] != "\\":
        depth += 1
    elif character == "}" and body[character_index - 1] != "\\":
        depth -= 1
    assert depth >= 0
assert depth == 0, "Chaves desbalanceadas"

assert chr(9) not in chapter, "Tabulação inesperada (possível comando LaTeX corrompido)"
assert (ROOT / "figs" / "cap6_arquitetura_civitas.png").exists()
print(f"OK: {len(labels)} rótulos, {len(cites)} referências citadas, {len(re.findall(chr(10), chapter))} linhas")
