"""Verificações estáticas do Capítulo 4 (não substituem a compilação LaTeX)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
chapter = (ROOT / "capitulos" / "capitulo4.tex").read_text(encoding="utf-8")
main = (ROOT / "01Projeto.tex").read_text(encoding="utf-8")
chapter3 = (ROOT / "capitulos" / "capitulo3.tex").read_text(encoding="utf-8")
bib = (ROOT / "bibliografia.bib").read_text(encoding="utf-8")

assert main.count(r"\input{capitulos/capitulo4}") == 1
assert main.count(r"\chapter{Definição da Interface com o Usuário}") == 0
for heading in (
    "Descrição de Cenário",
    "Descrição de Personas",
    r"Esboços de Tela (\textit{Wireframes})",
    "Protótipos de Tela",
    "Acessibilidade e Inclusão de Pessoas com Deficiência",
    "Práticas de Acessibilidade Implementadas",
):
    assert heading in chapter, heading

legacy = re.compile(
    r"SeniorCare|SeniorStock|Lar dos Velhinhos|APAE|residente|idoso|"
    r"enfermeiro|recepcionista|médico|prontuário|SOAP|alergia|vacina|"
    r"religião|produto|estoque|prescrição|consulta médica",
    re.IGNORECASE,
)
assert not legacy.search(chapter), "Conteúdo legado encontrado no Capítulo 4"

for environment in ("figure", "quadro", "tabularx"):
    assert chapter.count(r"\begin{" + environment + "}") == chapter.count(
        r"\end{" + environment + "}"
    ), environment

labels = re.findall(r"\\label\{([^}]+)\}", chapter)
assert len(labels) == len(set(labels)), "Rótulo repetido no Capítulo 4"
other_labels = set(re.findall(r"\\label\{([^}]+)\}", chapter3 + main))
assert not (set(labels) & other_labels), "Rótulo do Capítulo 4 repetido em outro arquivo"
known_labels = set(labels) | other_labels
refs = set(re.findall(r"\\(?:auto)?ref\{([^}]+)\}", chapter))
assert not (refs - known_labels), f"Referências não encontradas: {refs - known_labels}"

keys = set(re.findall(r"@\w+\{([^,]+),", bib))
cites = set()
for group in re.findall(r"\\(?:paren|text)cite\{([^}]+)\}", chapter):
    cites.update(key.strip() for key in group.split(","))
assert not (cites - keys), f"Citações sem bibliografia: {cites - keys}"

figures = re.findall(r"\\includegraphics\[[^\]]+\]\{([^}]+)\}", chapter)
assert len(figures) == 9, f"Esperadas 9 figuras; encontradas {len(figures)}"
for relative in figures:
    assert (ROOT / relative).is_file(), relative

assert chapter.count(r"\caption{Cenário --") == 2
print(f"Capítulo 4: {len(labels)} rótulos, {len(refs)} referências, "
      f"{len(cites)} citações e {len(figures)} figuras verificados.")
