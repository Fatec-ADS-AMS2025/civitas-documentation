"""Gera o diagrama de arquitetura do capítulo 6 (figs/cap6_arquitetura_civitas.png).

Cada bloco corresponde a elementos verificados nas branches main dos repositórios
civitas-frontend (ed79c34) e civitas-backend (e7c3f30). Não incluir componentes
que não existam no código.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FIGS = Path(__file__).resolve().parents[1] / "figs"
FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
INK = "#1f2a30"
MID = "#55636b"
LINE = "#7d8b92"
FRONT = "#e6f1f1"
BACK = "#eef0f6"
DATA = "#f5efe3"
WHITE = "#ffffff"

W, H = 2000, 1800
image = Image.new("RGB", (W, H), WHITE)
draw = ImageDraw.Draw(image)


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def box(bounds, fill=WHITE, outline=LINE, width=3, radius=14):
    draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)


def block(bounds, title, lines=(), fill=WHITE):
    box(bounds, fill=fill)
    x0, y0, x1, _ = bounds
    centre = (x0 + x1) / 2
    draw.text((centre, y0 + 16), title, font=font(30, True), fill=INK, anchor="ma")
    y = y0 + 58
    for line in lines:
        draw.text((centre, y), line, font=font(25), fill=MID, anchor="ma")
        y += 33


def group(bounds, title, fill):
    box(bounds, fill=fill, outline=INK, width=4, radius=18)
    draw.text((bounds[0] + 28, bounds[1] + 18), title, font=font(34, True), fill=INK)


def arrow(start, end, both=False, width=4):
    def head(tip, origin):
        size = 18
        (x, y), (ox, oy) = tip, origin
        if abs(x - ox) >= abs(y - oy):
            s = 1 if x > ox else -1
            points = [(x, y), (x - s * size, y - size * 0.6), (x - s * size, y + size * 0.6)]
        else:
            s = 1 if y > oy else -1
            points = [(x, y), (x - size * 0.6, y - s * size), (x + size * 0.6, y - s * size)]
        draw.polygon(points, fill=INK)

    draw.line([start, end], fill=INK, width=width)
    head(end, start)
    if both:
        head(start, end)


# --- Front-end -------------------------------------------------------------
group((40, 30, 1960, 490), "Aplicação front-end (civitas-frontend) – Next.js, React e TypeScript", FRONT)
block((80, 100, 660, 300), "Páginas e layouts", ["src/app (App Router)", "login, dashboard/*", "Client e Server Components"])
block((710, 100, 1290, 300), "Componentes reutilizáveis", ["src/components, src/features", "Form, Table, Sidebar", "estilização com Tailwind CSS"])
block((1340, 100, 1920, 300), "Estado e sessão", ["AuthContext + localStorage", "Zustand (listagens, navegação)", "lib/auth-storage.ts"])
block((400, 340, 1600, 465), "Serviços HTTP – src/hooks/generic.ts e especializações", ["GenericService<T>: Fetch API, cabeçalho Authorization, tratamento do envelope"])
arrow((370, 300), (560, 340))
arrow((1000, 300), (1000, 340))
arrow((1630, 300), (1440, 340))

# --- Comunicação ------------------------------------------------------------
arrow((1000, 490), (1000, 590), both=True, width=5)
draw.text((1030, 508), "HTTP + JSON  |  Authorization: Bearer <JWT>", font=font(27, True), fill=INK)
draw.text((1030, 545), "Envelope Response { code, message, data }", font=font(26), fill=MID)

# --- Back-end ---------------------------------------------------------------
group((40, 590, 1960, 1480), "API back-end (civitas-backend) – ASP.NET Core 9 e C#", BACK)
block((90, 660, 1400, 780), "Pipeline HTTP – Program.cs", ["UseCors → UseHttpsRedirection → UseAuthentication → UseAuthorization → MapControllers"])
block((90, 825, 1400, 945), "Controllers – 13 controladores sob /api", ["rotas, [Authorize]/[AllowAnonymous], códigos HTTP, objeto Response"])
block((90, 990, 1400, 1110), "Services – GenericService<T, TDto> e especializações", ["regras de negócio, validações, conversão com AutoMapper"])
block((90, 1155, 1400, 1275), "Repositories – GenericRepository<T> e especializações", ["interfaces em Data/Interfaces, consultas, paginação, SaveChanges"])
block((90, 1320, 1400, 1450), "Entity Framework Core – AppDbContext e Builders", ["mapeamento dos Models, provedor Npgsql"])
for top, bottom in ((780, 825), (945, 990), (1110, 1155), (1275, 1320)):
    arrow((745, top), (745, bottom), both=True)

block((1460, 660, 1920, 945), "Segurança", ["JwtTokenService", "BCryptPasswordHashService", "AuthService", "DevBypassAuthorizationHandler", "(controlado pela chave DEV)"])
block((1460, 990, 1920, 1275), "Objetos", ["Dtos (contratos da API)", "Models (entidades)", "MappingsProfile (AutoMapper)", "Contracts (Response,", "paginação)"])
arrow((1400, 720), (1460, 720))
arrow((1400, 1050), (1460, 1050))

# --- Persistência -----------------------------------------------------------
arrow((745, 1450), (745, 1590), both=True, width=5)
draw.text((775, 1520), "Comandos SQL gerados pelo EF Core", font=font(27, True), fill=INK)
group((400, 1590, 1600, 1760), "Persistência", DATA)
draw.text((1000, 1650), "PostgreSQL – banco de dados relacional civitas", font=font(30, True), fill=INK, anchor="ma")
draw.text((1000, 1695), "cadastros administrativos, despesas, orçamentos, documentos e auditoria", font=font(25), fill=MID, anchor="ma")

FIGS.mkdir(exist_ok=True)
image.save(FIGS / "cap6_arquitetura_civitas.png", dpi=(200, 200))
