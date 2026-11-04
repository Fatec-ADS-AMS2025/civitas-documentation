# Capítulo 6: relatório de rastreabilidade técnica

Relaciona as principais afirmações de `capitulos/capitulo6.tex` às evidências nos repositórios. Este relatório não faz parte do documento LaTeX.

**Versões analisadas (branch `main`, clonadas em 3 nov. 2026):**

| Repositório | Commit | Data |
|---|---|---|
| `Fatec-ADS-AMS2025/civitas-backend` | `e7c3f30581640e45d215c1c2382b10e170430ad6` | 2026-04-03 |
| `Fatec-ADS-AMS2025/civitas-frontend` | `ed79c34c84de1521c787788721b4b5815ed3b546` | 2026-06-11 |

Prefixos usados: `API/` = `civitas-backend/Civitas.WebAPI/`; `WEB/` = `civitas-frontend/civitas-frontend/`.

Tipo de evidência: leitura estática do código, salvo indicação em contrário. Nada foi executado em nenhuma das duas aplicações.

## 1. Arquitetura de Desenvolvimento (6.1)

| Afirmação | Evidência |
|---|---|
| ASP.NET Core 9 / C# | `API/Civitas.WebAPI.csproj` (`net9.0`, SDK Web) |
| EF Core 9, Npgsql, AutoMapper, BCrypt, JWT Bearer, Swashbuckle | `API/Civitas.WebAPI.csproj` (`PackageReference`), uso em `API/Program.cs` |
| Next.js 15, React 19, TypeScript, Tailwind 4, Zustand, ExcelJS, jsPDF | `WEB/package.json`; uso em `WEB/src/` |
| **Axios declarado e não importado** | `WEB/package.json:12`; busca por `axios` em `WEB/src` sem resultado |
| Comunicação por Fetch API | `WEB/src/hooks/generic.ts`, `WEB/src/hooks/useAuth.ts`, `WEB/src/hooks/despesa.ts` |
| PostgreSQL acessado apenas pela API | `API/Program.cs` (`UseNpgsql`), `API/appsettings.json` (`DefaultConnection`); sem cliente de banco no front-end |
| URL base por `NEXT_PUBLIC_API_URL` | `WEB/src/hooks/generic.ts:5`, `WEB/src/hooks/useAuth.ts` |
| Porta local da API | `API/Properties/launchSettings.json` |
| Envelope `code`/`message`/`data` | `API/Objects/Contracts/Response.cs`, `ResponseEnum.cs`; `WEB/src/hooks/generic.ts` (`ResponseEnvelope`) |
| Branches `main`, `dev` e de tarefa; merges por PR | `git branch -a` e `git log` dos dois repositórios |
| Modelos de tarefa e PR | `civitas-backend/documentation/template/`, `civitas-frontend/.github/` |
| Workflow de build no front-end | `civitas-frontend/.github/workflows/build.yml`; ausência de `.github` no back-end (`main`) |
| Dockerfile no front-end e não no back-end (`main`) | `WEB/Dockerfile`; `git ls-files` do back-end |
| Modelo em Astah | `civitas-backend/documentation/ClassDiagram/Civitas_ERP_ClassDiagram.asta` |
| Divergência de contrato | Ver seção 5 |

## 2. Back-End (6.1.1)

| Afirmação | Evidência |
|---|---|
| Projetos da solução | `API/Civitas.WebAPI.sln`, `civitas-backend/Civitas.WebAPI.Tests/` |
| Ordem do pipeline | `API/Program.cs` (`UseCors`, `UseHttpsRedirection`, `UseAuthentication`, `UseAuthorization`, `MapControllers`) |
| 13 controladores e rotas | `API/Controllers/*.cs` (12) e `API/controllers/FornecedorController.cs` (1), atributos `[Route]` |
| Padrão de verbos e `PATCH situacao/{id}` | Atributos `[Http*]` nos controladores (`documentos` e `orcamentos` não têm `PATCH`; `fluxos` usa `status/{id}`) |
| Serviço genérico | `API/Services/Entities/GenericService.cs` |
| Serviços com validação própria | `UsuarioService.cs`, `FornecedorService.cs`, `SecretariaService.cs`, `DespesaService.cs`, `AuthService.cs` |
| Serviços sem validação própria | `InstituicaoService.cs`, `OrcamentoService.cs`, `FluxoService.cs`, `DocumentoService.cs`, `TipoDespesaService.cs`, `TipoInstituicaoService.cs`, `UnidadeMedidaService.cs` (busca por `Validar`/`Validate`/`ArgumentException` sem resultado) |
| Repositório genérico, ordenação e paginação (máx. 100) | `API/Data/Repositories/GenericRepository.cs`, `API/Objects/Contracts/PaginationQuery.cs` |
| Consultas específicas | `API/Data/Repositories/UsuarioRepository.cs` (`GetByEmailAsync`), `DespesaRepository.cs` (`ExistsByNumeroDocumentoAndFornecedorAsync`) |
| Injeção de dependências com `AddScoped` | `API/Program.cs` |
| Controladores sem acesso direto ao banco | Busca por `AppDbContext`/`DbSet` em `Controllers` |
| Substituição do banco em testes | `civitas-backend/Civitas.WebAPI.Tests/Infrastructure/TestWebApplicationFactory.cs` |
| `Senha` ignorada no mapeamento | `API/Objects/Dtos/Mappings/MappingsProfile.cs` |
| 12 `DbSet` e Builders | `API/Data/AppDbContext.cs`, `API/Data/Builders/` |
| Índices únicos em usuário | `API/Data/Builders/UsuarioBuilder.cs` |
| Exclusão restrita em despesa | `API/Data/Builders/DespesaBuilder.cs` |
| Migrations não versionadas | `civitas-backend/.gitignore` (`**/Migrations/`); `git ls-files` lista apenas `AppDbContextModelSnapshot.cs`; instrução em `README.md` |
| Validação de usuário | `API/Services/Entities/UsuarioService.cs` |
| Data Annotations só em `AuditoriaDTO` | `API/Objects/Dtos/Entities/AuditoriaDTO.cs` |
| Fluxo de cadastro de despesa | `API/Controllers/DespesaController.cs` (`Post`), `DespesaService.cs` (`ValidarCadastroAsync`), `GenericService.cs` (`Create`), `GenericRepository.cs` (`Add`) |
| Códigos HTTP | Controladores, por exemplo `UsuarioController.cs` (`Conflict`), `AuthController.cs` (`Unauthorized`) |
| Swagger só em desenvolvimento, com XML e Bearer | `API/Program.cs`; `GenerateDocumentationFile` no `.csproj` |
| 26 métodos de teste (não executados) | Contagem de `[Fact]`/`[Theory]` em `civitas-backend/Civitas.WebAPI.Tests/*.cs` |

## 3. Front-End (6.1.2)

| Afirmação | Evidência |
|---|---|
| App Router e rotas | `WEB/src/app/` |
| TypeScript estrito; `allowJs`; página em JSX | `WEB/tsconfig.json`; `WEB/src/app/login/page.jsx` |
| Tailwind e variáveis | `WEB/postcss.config.mjs`, `WEB/src/app/globals.css` |
| Componente de formulário configurável | `WEB/src/components/Form/form.tsx` (`FormFieldConfig`, `FormMode`, `validate`) |
| Tabela e exportação | `WEB/src/components/Table/`, `export-utils.ts` (`import("exceljs")`, `import("jspdf")`) |
| Decomposição de despesas | `WEB/src/app/dashboard/despesas/_components/`, `WEB/src/hooks/useDespesasDashboard.ts`, `WEB/docs/SPRINT16_COMPONENTIZACAO_DESPESAS.md` |
| Autenticação por Context API | `WEB/src/contexts/AuthContext.ts` |
| Zustand: dois pontos de uso | `WEB/src/features/listing-center/store.ts` (`sessionStorage`), `WEB/src/hooks/useNavigationProgress.ts` |
| Serviço HTTP genérico; chaves técnicas ocultadas | `WEB/src/hooks/generic.ts` (`createHeaders`, `handleResponse`, `TECHNICAL_ERROR_KEYS`) |
| Coleções vazias em caso de falha | `WEB/src/hooks/generic.ts` (`getAllData`) |
| Sessão local e expiração | `WEB/src/lib/auth-storage.ts` (`authStorage`, `isExpired`) |
| Proteção de páginas no cliente | `WEB/src/app/dashboard/layout.tsx`; nenhum `middleware.*` no repositório |
| Máscaras e normalização | `WEB/src/lib/input-mask.ts`, `WEB/src/global/formPayload.ts`, `WEB/src/components/Input.tsx` |
| Recuperação de senha simulada | `WEB/src/hooks/useForgotPassword.ts` (`USE_REAL_FORGOT_PASSWORD_REQUEST`) |
| Link `/signup` sem página | `WEB/src/app/login/_components/login.tsx`; ausência de `WEB/src/app/signup` |
| Carga inicial no servidor sem token | `WEB/src/app/dashboard/{usuarios,fornecedor,instituicoes,despesas,unidades-consumidoras}/page.tsx` (`force-dynamic`); `isBrowser()` em `auth-storage.ts`; `createHeaders` em `generic.ts`. **Conclusão por análise estática, não observada em execução** |

## 4. Segurança da Informação (6.2)

Os valores de senha e de chave não são reproduzidos neste relatório nem no capítulo.

| Item solicitado | Conclusão | Evidência |
|---|---|---|
| 1. Autenticação JWT | Implementada | `API/Controllers/AuthController.cs`, `API/Services/Entities/AuthService.cs` |
| 2. Geração e validação | Implementadas (HMAC-SHA256, 60 min, `ClockSkew` zero); sem refresh ou revogação | `API/Services/Security/JwtTokenService.cs`, `API/Program.cs`, `API/appsettings.json` (`ExpirationMinutes`) |
| 3. BCrypt | Implementado, com custo padrão da biblioteca | `API/Services/Security/BCryptPasswordHashService.cs`, `UsuarioService.cs` (`Create`, `Update`, `ValidatePassword`) |
| 4. Autorização e permissões | **Sem perfis.** Nenhum `Roles`, `Policy`, `ClaimTypes` ou `User.` no código da API; `tipoUsuario` só é exibido no front-end | Buscas em `API/`; `WEB/src/app/dashboard/perfil/page.tsx` |
| 5. Proteção de endpoints | `[Authorize]` em 12 controladores; `AuthController` com `[AllowAnonymous]` no login | Atributos nos controladores |
| 6. Validação recebida | Parcial | Ver seção 2 |
| 7. Tratamento de erros | `StackTrace` nas respostas 500 de 12 arquivos de controlador; sem `UseExceptionHandler` | `git grep StackTrace`; `API/Program.cs` |
| 8. CORS | Qualquer origem, método e cabeçalho | `API/Program.cs` (`UseCors`) |
| 9. HTTPS | `UseHttpsRedirection`; sem `UseHsts`; perfis locais também em HTTP; padrão HTTP no front-end | `API/Program.cs`, `launchSettings.json`, `WEB/src/hooks/generic.ts`, `WEB/Dockerfile` |
| 10. Auditoria | Entidade e consultas existem. Nenhum serviço de negócio grava auditoria; `POST` e `PATCH` abertos a qualquer autenticado; sem tela | `API/Controllers/AuditoriaController.cs`, `API/Objects/Models/Auditoria.cs`; busca por `Auditoria` em `API/Services`; busca por `audit` em `WEB/src` |
| 11. Informações sensíveis | Chave JWT e senha do banco com valores reais versionados (verificado sem exibir valores: não são marcadores); senha em texto claro no `localStorage` com *Lembrar-me*; e-mail em logs do console | `API/appsettings.json`; `WEB/src/lib/auth-storage.ts` (`credentialsStorage`), `WEB/src/app/login/_components/login.tsx`, `WEB/src/hooks/useAuth.ts` |

### `DevBypassAuthorizationHandler`

| Aspecto | Evidência |
|---|---|
| Implementação: `context.Succeed` em todos os requisitos pendentes quando `DEV` é verdadeiro | `API/Services/Security/DevBypassAuthorizationHandler.cs` |
| Registro incondicional, sem verificação de ambiente | `API/Program.cs` (`AddSingleton<IAuthorizationHandler, DevBypassAuthorizationHandler>`) |
| `DEV` = falso na `main` | `API/appsettings.json` |
| `DEV` = verdadeiro na `dev` | `git show origin/dev:Civitas.WebAPI/appsettings.json` |
| Cobertura em teste (não executado) | `civitas-backend/Civitas.WebAPI.Tests/AuthorizationEndpointsTests.cs` (`GetProtectedRoute_WithoutToken_ReturnsSuccess_WhenDevTrue`) |

## 5. Contrato entre front-end e back-end (branches `main`)

| Chamada do front-end | Origem | Back-end `main` | Back-end `dev` |
|---|---|---|---|
| `unidades-consumidoras` | `WEB/src/hooks/unidadeConsumidora.ts` | Inexistente | Existe |
| `tipo-codigo` | `WEB/src/hooks/tipoCodigo.ts` | Inexistente | Existe |
| `despesas/pagas`, `atrasadas`, `excluidos` | `WEB/src/hooks/despesa.ts` | Inexistentes | Existem |
| `despesas/{id}/status`, `status-exclusao`, `documento/{hash}` | `WEB/src/hooks/despesa.ts` | Inexistentes | Existem |
| `POST`/`PUT despesas` em `multipart/form-data` | `WEB/src/hooks/despesa.ts` | `DespesaDTO` sem `[FromForm]` | `[FromForm]` |
| `auth/forgot-password` | `WEB/src/hooks/useForgotPassword.ts` | Inexistente | Não conferido em detalhe (a branch tem `AuthService` ampliado e `PasswordResetToken`) |
| `documentos`, `fluxos` | `WEB/src/hooks/documento.ts`, `fluxo.ts` | Existem | Removidos |

## 6. Diagrama de arquitetura

`figs/cap6_arquitetura_civitas.png` é gerada por `scripts/gerar_figura_cap6.py`. Cada bloco usa nomes encontrados no código citado acima. O diagrama não inclui componentes como gateway, cache, fila ou serviços externos porque eles não existem na `main`.
