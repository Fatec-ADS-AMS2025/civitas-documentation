# Capítulo 6: relatório de validação

Data da verificação: 3 nov. 2026. Este relatório não faz parte do documento LaTeX.

## 1. Resultado da compilação

**A compilação foi executada e terminou sem erros.** Ela rodou em uma cópia do projeto, em contêiner Docker, porque a máquina tem o TeXstudio, mas não tem distribuição TeX.

| Item | Resultado |
|---|---|
| Ambiente | `texlive/texlive:latest`, pdfTeX 1.40.29 (TeX Live 2026) |
| Sequência | `pdflatex`, `biber`, `pdflatex`, `pdflatex` em `extensao.tex` |
| Códigos de saída | 0 em todas as etapas |
| Erros de LaTeX (`^!`) | 0 |
| Avisos de LaTeX, incluindo citações e referências indefinidas e rótulos duplicados | 0 |
| Avisos e erros do Biber | 0 |
| `Overfull \hbox` | 2, de 1,59 pt, nos números de página 150 e 151 do sumário. Não foram introduzidos pelo texto do capítulo e não têm efeito visível relevante |
| PDF gerado | `extensao.pdf`, 158 páginas (ignorado pelo Git) |
| Capítulo no sumário | 6 (p. 82), 6.1 (p. 82), 6.1.1 (p. 86), 6.1.2 (p. 89), 6.2 (p. 92) |

Para repetir no PowerShell, a partir de `2026_ProjetoExtensaoFatec` (os arquivos gerados ficam na pasta do projeto, ignorados pelo Git):

```bash
docker run --rm -v "${PWD}:/work" -w /work texlive/texlive:latest sh -c "pdflatex -interaction=nonstopmode extensao.tex && biber extensao && pdflatex -interaction=nonstopmode extensao.tex && pdflatex -interaction=nonstopmode extensao.tex"
```

## 2. Outras verificações realizadas

| Verificação | Resultado |
|---|---|
| `scripts/verificar_capitulo6.py` (hierarquia, termos legados, rótulos, referências cruzadas, citações, caracteres especiais, chaves) | Passou: 8 rótulos, 51 referências citadas |
| `scripts/verificar_capitulo4.py` (regressão) | Passou |
| Termos `Comtur`, `Flutter` e `Azure DevOps` no PDF final | 0 ocorrências |
| Inspeção visual das páginas do capítulo | Títulos, figura e quadros posicionados corretamente; acentuação correta |
| Chaves duplicadas em `bibliografia.bib` | Nenhuma |
| Segredos no capítulo e nos relatórios | Nenhum valor reproduzido |
| Código dos repositórios `civitas-backend` e `civitas-frontend` | Não alterado; analisado em clones temporários |

Durante a validação, uma substituição automática corrompeu 19 comandos `\textit` (`\t` virou tabulação), e o erro não gerou falha de compilação. Ele foi percebido na conferência, corrigido, e o verificador passou a rejeitar tabulações no capítulo. Os números acima referem-se à versão corrigida.

## 3. O que não foi verificado

- **Testes automatizados do back-end:** não executados. O `dotnet test` foi bloqueado pelo controle de permissões do ambiente. O capítulo declara isso e não usa os testes como evidência. Um documento do front-end (`docs/SPRINT16_COMPONENTIZACAO_DESPESAS.md`) alerta que o projeto de testes pode não compilar.
- **Execução das aplicações:** nenhuma foi iniciada, e não houve banco de dados nem migrations. O erro na carga inicial sem token e as incompatibilidades de contrato são conclusões da leitura do código.
- **Build do front-end:** não executado.
- **Conformidade com a LGPD:** sem avaliação específica. O capítulo não declara conformidade.
- **Revisão ABNT da lista de referências por pessoa:** a formatação vem do estilo `biblatex-abnt`, sem conferência item a item contra a norma.

## 4. Referências bibliográficas

| Verificação | Referências | Método |
|---|---|---|
| DOI confirmado | Parnas (1972), Saltzer e Schroeder (1975), Kent e Souppaya (2006), Jones e Hardt (2012) | API Crossref |
| ISBN confirmado | Bass et al. (2021), Fowler, Anderson (2020), Chacon e Straub (2014), Martin (2019) | Open Library |
| URL e título confirmados | Documentação da Microsoft, Next.js, React, TypeScript, Tailwind, Zustand, MDN, Npgsql, AutoMapper, PostgreSQL, GitHub, OWASP; Fielding (2000); Provos e Mazières (1999) | Acesso HTTP |
| Trecho que sustenta a citação conferido | OWASP (HTML5, Password Storage, Secrets), Microsoft (CORS, HTTPS, configuração, migrations, `[ApiController]`), Next.js, Tailwind, TypeScript, Fetch API | Leitura da página |
| Confirmado por busca, com ressalva | ISO/IEC 27000:2018 (site da ISO recusou o acesso automatizado; dados confirmados em catálogos de normas) e Fontes (2008) | Busca na web |

Pontos a conferir:

- **Citações de livros:** as obras não foram lidas na íntegra. Conferir com o exemplar as citações conceituais de Sommerville, Bass, Fowler, Evans, Martin, Anderson e Fontes. O ano de Fowler (2002) e de Anderson (2020) segue a primeira publicação conhecida dessas edições; o catálogo consultado indica outras datas de impressão.
- **Data nas referências on-line:** as páginas sem data publicada não têm campo `year`, então o estilo gera citações como "(Microsoft, 2026a)" com base no acesso.
- **Correção de entrada existente:** em `Fontes2008`, o autor estava como "Eduardo Fontes" e passou a "Edison Fontes", com local Rio de Janeiro.
- **Entradas suspeitas não usadas no capítulo, mantidas sem alteração:** `Bass2016`, `Bass2016ArquiteturaPT`, `Bradley2020`, `Anderson2021`, `Fowler2012`, `Proise2021`, `Lerman2019`, `Schildt2009`, `Skeet2019`. Vários dados parecem incorretos, por exemplo a 2ª edição de Anderson datada de 2021, e Fowler datado de 2012. Elas não aparecem na lista impressa, porque nenhum capítulo as cita agora.

## 5. Divergências para revisão da equipe

### 5.1 Decisão principal: `main` está defasada em relação a `dev`

Seguindo a tarefa, o capítulo descreve a `main`. Porém, a `main` do back-end é de abril de 2026 e está 93 commits atrás da `dev`, enquanto a `main` do front-end, de junho, já depende de recursos que só existem na `dev` do back-end (tabela na seção 5 do relatório de rastreabilidade). Os Capítulos 2 a 4 também descrevem o sistema mais próximo da `dev`.

**A equipe precisa decidir:** promover a `dev` para a `main` ou reescrever o trecho do capítulo. Se a `dev` for promovida, será preciso revisar as seções sobre despesas, documentos, fluxos, unidade consumidora, Docker e `DEV`.

### 5.2 Capítulo 6 em relação aos capítulos anteriores

| Tema | Documentação anterior | Código (`main`) |
|---|---|---|
| Perfis (Cap. 3; RNF-02) | Permissões distintas para Administrador, Funcionário e Visitante | Sem autorização por perfil |
| Visitante (Cap. 3) | Consulta informações públicas | Sem rota anônima além do login; sem página pública |
| Auditoria (RF17, RF18; RNF-07) | Trilha de auditoria das operações | Sem registro automático; sem tela |
| RF02 (encerramento de sessão) | Encerramento de sessão | Só remove dados locais; o token continua válido até expirar |
| RF10 a RF13 (despesas) | Unidade consumidora, valores, juros, multa, hash do documento, exclusão lógica | Ausentes na `Despesa` da `main`; presentes no front-end |
| Dicionário de classes (Cap. 3) | Inclui `UnidadeConsumidora` e `TipoCodigo` | Ausentes do back-end na `main` |
| RNF-02 (HTTPS, LGPD) | Exigidos como requisito | HTTPS parcial; LGPD não avaliada |
| RF15 (paginação) e `Orcamento` | Consulta com paginação e filtros | `orcamentos` sem `/inativos` e sem exclusão; o front-end chama `status-exclusao` |

### 5.3 Conteúdo legado fora do Capítulo 6 (não alterado, por restrição da tarefa)

- **Capítulo 5, Banco de Dados:** scripts SQL de outro sistema (`resident`, `allergy`, `health_insurance`, `product`) e menção a "pontos turísticos" na seção de mapeamento objeto-relacional.
- **`conclusao.tex`:** descreve o *SeniorCareManager*.
- **`02Horas.tex`:** inclui PDFs de sprint do *SeniorCareManager* e uma tarefa de 2024.
- **`01Projeto.tex`:** bloco antigo do Capítulo 3 mantido dentro de `\iffalse` (sem efeito no PDF).

### 5.4 Achados de segurança para encaminhar à equipe

Em ordem de prioridade. Nenhum foi corrigido aqui, por restrição da tarefa.

1. **Segredos versionados:** a chave de assinatura JWT e a senha do banco estão em `appsettings.json`. Devem ser substituídas e retiradas do versionamento, porque permanecem no histórico do Git.
2. **Autorização por perfil inexistente:** qualquer usuário ativo acessa todas as operações da API.
3. **`DEV = true` na branch `dev`:** se implantada com esse valor, a API fica sem exigência de autenticação.
4. **Senha em texto claro no `localStorage`** com a opção *Lembrar-me*.
5. **`stack trace` nas respostas 500** e CORS irrestrito.
6. **Auditoria manual e editável** por qualquer usuário autenticado.

## 6. Critérios de conclusão

| Critério | Situação |
|---|---|
| Duas aplicações analisadas | Atendido, por leitura do código |
| Capítulo exclusivo do Civitas, sem resíduos de projetos anteriores | Atendido no Capítulo 6; restam resíduos em outros capítulos (5.3) |
| Quatro seções completas, com a hierarquia pedida | Atendido |
| Arquitetura e tecnologias conforme o código | Atendido para a `main` |
| Integração explicada | Atendido, com a divergência registrada |
| Segurança diferencia implementado, parcial e previsto | Atendido (Quadro 6.2) |
| Referências corretas | Atendido, com os pontos a conferir da seção 4 |
| Estrutura LaTeX compatível | Atendido |
| Compilação informada | Atendido: executada, sem erros |
