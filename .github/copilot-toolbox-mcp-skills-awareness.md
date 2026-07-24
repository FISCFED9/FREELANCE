# GitHub Copilot Toolbox — MCP & Skills awareness

_Generated: 2026-07-24T17:48:42.880Z_

## How to use this report

- **Saved copy:** This file is **`.github/copilot-toolbox-mcp-skills-awareness.md`** — refreshed whenever the toolbox runs an MCP & Skills scan (including on workspace open when auto-scan is enabled). It is meant for **Copilot workspace context** together with `.github/copilot-instructions.md` (which gets a shorter replaceable summary when auto-merge is on).
- **MCP:** Lists **configured** servers from `mcp.json`. **Live tool use** still requires **Copilot Chat → Agent** with those servers **trusted/started** in the MCP tools UI.
- **Skills:** **On-disk** folders with `SKILL.md`. Copilot does not auto-load them; attach `SKILL.md` or paths in chat when useful.
- **Task routing:** When the user’s request matches a server’s purpose (e.g. Confluence → Confluence/Atlassian MCP), prefer that **server id** from the tables below.

---

## MCP — workspace

Workspace `mcp.json` _(folder: FREELANCE)_

- **c:\Users\alber\OneDrive\Documentos\GitHub\FREELANCE\.vscode\mcp.json** — _File missing_

_No active workspace servers in mcp.json._

## MCP — user profile

- **C:\Users\alber\AppData\Roaming\Code\User\mcp.json** — _File exists — servers defined_

| Server id | Kind | Detail |
|-----------|------|--------|
| io.github.upstash/context7 | stdio | npx @upstash/context7-mcp@1.0.31 |
| io.github.github/github-mcp-server | http | https://api.githubcopilot.com/mcp/ |
| io.github.wonderwhy-er/desktop-commander | stdio | npx --registry https://registry.npmjs.org @wonderwhy-er/desktop-commander@0.2.40 |
| io.github.netdata/mcp-server | http | https://app.netdata.cloud/api/v1/mcp |
| io.github.ChromeDevTools/chrome-devtools-mcp | stdio | npx --registry https://registry.npmjs.org chrome-devtools-mcp@0.23.0 |
| firecrawl/firecrawl-mcp-server | stdio | npx -y firecrawl-mcp@latest |
| io.github.tavily-ai/tavily-mcp | stdio | npx tavily-mcp@0.2.15 |
| com.stripe/mcp | http | https://mcp.stripe.com |
| com.supabase/mcp | http | https://mcp.supabase.com/mcp |
| io.github.mongodb-js/mongodb-mcp-server | stdio | npx mongodb-mcp-server@1.10.0 --allowRequestOverrides ${input:allowRequestOverrides} --apiClientId ${input:apiClientId} --apiClientSecret ${input:apiClientSecret} --assistantBaseUrl ${input:assistantBaseUrl} --atlasTemporaryDatabaseUserLifetimeMs ${input:atlasTemporaryDatabaseUserLifetimeMs} --confirmationRequiredTools ${input:confirmationRequiredTools} --connectionString ${input:connectionString} --disabledTools ${input:disabledTools} --dryRun ${input:dryRun} --exportCleanupIntervalMs ${input:exportCleanupIntervalMs} --exportTimeoutMs ${input:exportTimeoutMs} --exportsPath ${input:exportsPath} --externallyManagedSessions ${input:externallyManagedSessions} --healthCheckHost ${input:healthCheckHost} --healthCheckPort ${input:healthCheckPort} --httpBodyLimit ${input:httpBodyLimit} --httpHeaders ${input:httpHeaders} --httpHost ${input:httpHost} --httpPort ${input:httpPort} --httpResponseType ${input:httpResponseType} --idleTimeoutMs ${input:idleTimeoutMs} --indexCheck ${input:indexCheck} --logPath ${input:logPath} --loggers ${input:loggers} --maxBytesPerQuery ${input:maxBytesPerQuery} --maxDocumentsPerQuery ${input:maxDocumentsPerQuery} --maxTimeMS ${input:maxTimeMS} --mcpClientLogLevel ${input:mcpClientLogLevel} --monitoringServerFeatures ${input:monitoringServerFeatures} --monitoringServerHost ${input:monitoringServerHost} --monitoringServerPort ${input:monitoringServerPort} --notificationTimeoutMs ${input:notificationTimeoutMs} --previewFeatures ${input:previewFeatures} --readOnly ${input:readOnly} --telemetry ${input:telemetry} --transport ${input:transport} --voyageApiKey ${input:voyageApiKey} |
| com.apify/apify-mcp-server | http | https://mcp.apify.com/ |
| com.figma.mcp/mcp | http | https://mcp.figma.com/mcp |
| elastic/mcp-server-elasticsearch | stdio | docker run -i --rm -e ES_URL -e ES_API_KEY docker.elastic.co/mcp/elasticsearch:latest stdio |
| ollama | stdio | npx -y ollama-mcp |

## Skills (local `SKILL.md` folders)

### Project-scoped

- **ace-pattern-learning** — `c:\Users\alber\OneDrive\Documentos\GitHub\FREELANCE\.github\skills\ace-pattern-learning`
  - Search ACE playbook before implementing, building, fixing, debugging, or refactoring code. Capture patterns after completing substantial coding work.

### User-scoped

- **skill-creator** — `C:\Users\alber\.claude\skills\skill-creator`
  - Create new skills, modify and improve existing skills. Use when users want to create a skill from scratch, edit, or optimize an existing skill.

---

## Suggested next steps

- **MCP:** Command Palette → `MCP: List Servers` (or this extension’s hub **MCP** tab) → start/trust servers in **Copilot Chat → Agent → tools**.
- **Edit config:** `MCP: Open Workspace Folder MCP Configuration` / `MCP: Open User Configuration`.
- **Refresh this report:** run **Intelligence — scan MCP & Skills awareness** again after changing `mcp.json` or adding skills.

_Report from GitHub Copilot Toolbox extension._
