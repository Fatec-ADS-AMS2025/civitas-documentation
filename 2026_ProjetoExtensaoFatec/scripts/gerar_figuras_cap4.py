"""Gera cartões de personas e esboços do capítulo 4 a partir dos fluxos do Civitas.

Os esboços representam a organização das telas, sem simular registros ou resultados.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


FIGS = Path(__file__).resolve().parents[1] / "figs"
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
INK = "#26333a"
MID = "#6b7780"
LINE = "#aeb9be"
PALE = "#edf1f2"
WHITE = "#ffffff"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size)


def text(draw, xy, value, size=25, bold=False, fill=INK):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def box(draw, bounds, fill=WHITE, outline=LINE, width=3, radius=10):
    draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)


def field(draw, bounds, label):
    x1, y1, x2, y2 = bounds
    text(draw, (x1, y1 - 34), label, 20, True)
    box(draw, bounds)


def button(draw, bounds, label, dark=False):
    box(draw, bounds, fill=INK if dark else PALE, outline=INK, width=2)
    f = font(21, True)
    b = draw.textbbox((0, 0), label, font=f)
    x = (bounds[0] + bounds[2] - (b[2] - b[0])) / 2
    y = (bounds[1] + bounds[3] - (b[3] - b[1])) / 2 - 2
    draw.text((x, y), label, font=f, fill=WHITE if dark else INK)


def base(title, subtitle, with_sidebar=True):
    im = Image.new("RGB", (1600, 900), WHITE)
    d = ImageDraw.Draw(im)
    if with_sidebar:
        box(d, (25, 25, 250, 875), fill=PALE, outline=LINE, radius=12)
        text(d, (60, 65), "CIVITAS", 30, True)
        for y, label in [(160, "Painel"), (225, "Usuários"), (290, "Secretarias"),
                         (355, "Fornecedores"), (420, "Orçamentos"), (485, "Despesas")]:
            text(d, (58, y), label, 22)
        x = 295
    else:
        x = 70
    text(d, (x, 58), title, 42, True)
    text(d, (x, 113), subtitle, 22, fill=MID)
    d.line((x, 157, 1550, 157), fill=LINE, width=3)
    return im, d, x


def save(im, name):
    im.save(FIGS / name, optimize=True)


def login():
    im, d, x = base("Acesso ao Civitas", "Esboço da tela de autenticação", False)
    box(d, (170, 210, 760, 800), fill=PALE)
    text(d, (245, 300), "Área institucional", 34, True)
    text(d, (245, 365), "Conteúdo de apresentação", 24)
    box(d, (880, 210, 1430, 800))
    text(d, (940, 275), "Entrar", 38, True)
    field(d, (940, 390, 1370, 445), "E-mail")
    field(d, (940, 510, 1370, 565), "Senha")
    text(d, (940, 600), "[ ] Lembrar-me", 21)
    text(d, (1190, 600), "Esqueci a senha", 21)
    button(d, (940, 675, 1370, 740), "Entrar", True)
    save(im, "cap4_wireframe_login.png")


def dashboard():
    im, d, x = base("Painel gerencial", "Resumo operacional e financeiro")
    button(d, (1260, 72, 1510, 133), "Atualizar painel")
    for i, title in enumerate(["Saldo atual", "Total orçado", "Total gasto", "Base ativa"]):
        left = 295 + i * 308
        box(d, (left, 195, left + 282, 380), fill=PALE)
        text(d, (left + 22, 222), title, 23, True)
        text(d, (left + 22, 290), "Dado consolidado", 20, fill=MID)
    box(d, (295, 430, 1510, 800))
    text(d, (325, 460), "Despesas recentes", 28, True)
    field(d, (325, 565, 720, 620), "Pesquisar")
    for i, col in enumerate(["Documento", "Vencimento", "Valor", "Situação"]):
        text(d, (335 + i * 285, 660), col, 21, True)
    d.line((325, 705, 1480, 705), fill=LINE, width=2)
    d.line((325, 755, 1480, 755), fill=LINE, width=2)
    save(im, "cap4_wireframe_painel.png")


def usuarios():
    im, d, x = base("Usuários", "Consulta e manutenção de contas")
    button(d, (1260, 72, 1510, 133), "Cadastrar", True)
    box(d, (295, 195, 1510, 355), fill=PALE)
    field(d, (325, 265, 705, 320), "Nome ou CPF")
    button(d, (745, 265, 995, 320), "Filtrar")
    box(d, (295, 405, 1510, 805))
    for i, col in enumerate(["Nome", "CPF", "Matrícula", "Tipo", "Situação", "Ações"]):
        text(d, (325 + i * 193, 445), col, 20, True)
    for y in [500, 575, 650, 725]:
        d.line((325, y, 1480, y), fill=LINE, width=2)
    save(im, "cap4_wireframe_usuarios.png")


def despesas():
    im, d, x = base("Despesas", "Pesquisa, registro e acompanhamento")
    button(d, (1250, 72, 1510, 133), "Nova despesa", True)
    box(d, (295, 195, 1510, 390), fill=PALE)
    field(d, (325, 270, 630, 325), "Busca")
    field(d, (660, 270, 960, 325), "Período")
    field(d, (990, 270, 1290, 325), "Instituição")
    button(d, (1320, 270, 1480, 325), "Aplicar")
    box(d, (295, 440, 1510, 820))
    for i, col in enumerate(["Documento", "Instituição", "Vencimento", "Valor", "Estado", "Ações"]):
        text(d, (325 + i * 193, 475), col, 20, True)
    for y in [525, 595, 665, 735]:
        d.line((325, y, 1480, y), fill=LINE, width=2)
    save(im, "cap4_wireframe_despesas.png")


def persona(name, role, age, area, goals, tasks, needs, output):
    im = Image.new("RGB", (1600, 900), WHITE)
    d = ImageDraw.Draw(im)
    box(d, (35, 35, 1565, 865), fill=WHITE, outline=LINE, radius=18)
    box(d, (35, 35, 1565, 205), fill=PALE, outline=LINE, radius=18)
    text(d, (85, 68), name, 48, True)
    text(d, (88, 135), f"{role}  |  {age} anos  |  {area}", 26)
    for top, heading, rows in [(250, "Objetivos", goals), (430, "Tarefas frequentes", tasks),
                               (610, "Necessidades da interface", needs)]:
        text(d, (85, top), heading, 30, True)
        d.line((85, top + 47, 1510, top + 47), fill=LINE, width=2)
        for i, row in enumerate(rows):
            text(d, (105, top + 72 + 45 * i), "• " + row, 24)
    save(im, output)


if __name__ == "__main__":
    login()
    dashboard()
    usuarios()
    despesas()
    persona("Helena Martins", "Administradora", 45, "coordenação administrativa",
            ["Conferir cadastros e acompanhar a execução orçamentária.",
             "Identificar registros que precisam de correção ou acompanhamento."],
            ["Gerenciar usuários, secretarias e orçamentos.",
             "Consultar o painel e os registros de auditoria."],
            ["Visão resumida antes do detalhamento.",
             "Filtros claros e distinção entre situação cadastral e financeira."],
            "cap4_persona_administradora.png")
    persona("Rafael Lima", "Funcionário", 33, "rotina financeira",
            ["Registrar despesas com dados consistentes.",
             "Localizar rapidamente lançamentos e comprovantes."],
            ["Consultar orçamento, fornecedor e unidade consumidora.",
             "Preencher despesa e acompanhar seu estado."],
            ["Formulário organizado por etapas e campos identificados.",
             "Pesquisa, filtros e mensagens de validação compreensíveis."],
            "cap4_persona_funcionario.png")
