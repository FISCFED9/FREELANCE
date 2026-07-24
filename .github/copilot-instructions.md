# GitHub Copilot instructions


<!-- github-copilot-toolbox:mcp-skills-awareness-begin -->

### MCP & Skills awareness (GitHub Copilot Toolbox)

_Last synced: 2026-07-24T17:48:44.230Z._

- **Full report:** `.github/copilot-toolbox-mcp-skills-awareness.md` in this workspace (auto-overwritten on each scan). Use it as ground truth for configured servers and skill folders.
- **MCP:** For **live tools**, use **Copilot Chat → Agent** and **trust/start** the right servers in the MCP UI.
- **When the user’s task matches a server** (e.g. “open this Confluence page” and a **Confluence** / **Atlassian** MCP is listed), **prefer that server id** and plan on Agent + MCP for actions—not only file search.
- **Skills:** Folders below contain `SKILL.md`; attach or cite paths in chat when relevant.

#### Workspace MCP

- `c:\Users\alber\OneDrive\Documentos\GitHub\FREELANCE\.vscode\mcp.json` _(workspace: FREELANCE)_ — _file missing_

_No active workspace servers in mcp.json._

#### User MCP

- `C:\Users\alber\AppData\Roaming\Code\User\mcp.json` — _servers defined_

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

#### Project skills

- **ace-pattern-learning** — `c:\Users\alber\OneDrive\Documentos\GitHub\FREELANCE\.github\skills\ace-pattern-learning` — Search ACE playbook before implementing, building, fixing, debugging, or refactoring code. Capture patterns after completing substantial coding work.

#### User skills

- **skill-creator** — `C:\Users\alber\.claude\skills\skill-creator` — Create new skills, modify and improve existing skills. Use when users want to create a skill from scratch, edit, or optimize an existing skill.

<!-- github-copilot-toolbox:mcp-skills-awareness-end -->
