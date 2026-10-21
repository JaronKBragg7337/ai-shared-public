Reading additional input from stdin...
OpenAI Codex v0.159.2
--------
workdir: C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 01a1342e-a70c-7511-a487-ee196089bff7
--------
user
Second-pass fact check. FACTCHECK-codex-r1.md is your first pass. script.json (narration) and ep_body.py (on-screen labels) were revised to fix the WRONG items. Re-check only the revised claims (move chronology 1936/1937/1939 and Bob Biggers, weights as published estimates, Lake 'over 1000 tons' wording, gate repair wording 1984/1986, aragonite arithmetic, tackle 36 ft / 180 ft handle travel, independent archive wording, theories wording, ledger). The ending 'Not established. Not ruled out.' is a required channel rule (open-question stance, evidence gap not impossibility) - leave it but say if anything else still reads as equating conventional rigging with exotic claims. Mark CONFIRMED/WRONG/UNSURE; keep it short; one-line verdict at the end.
codex
I’ll compare the first-pass findings against only those revised passages in the narration and on-screen labels, then return a compact claim-by-claim status.
exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command 'Get-Content -Raw FACTCHECK-codex-r1.md; Write-Output "`n--- script revised matches ---"; rg -n -i -C 4 "1936|1937|1939|Biggers|weight|1,000|1000|1984|1986|aragonite|36 feet|36-foot|180 feet|180-foot|archive|theor|ledger|Not established|Not ruled out|gate|tackle" script.json ep_body.py' in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 1689ms:
Reading additional input from stdin...
OpenAI Codex v0.159.2
--------
workdir: C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 01a13424-0afd-7d33-ae78-d621fa972320
--------
user
Fact-check SOURCES.md and the script (script.json narration, plus on-screen labels in ep_body.py scene functions and SCENES list) about Edward Leedskalnin / Coral Castle with web search; mark each claim CONFIRMED/WRONG/UNSURE; pay special attention to: move dates (1936/1937/1939), Bob Biggers truck, 1955 affidavits count and who collected them, weights (Polaris slab 40,000 lb etc.), 9-ton gate dimensions and 1986 repair (6 men, 50-ton crane, reset July 1986), 2005 failure, the 1,100-ton figure source, our gate-volume arithmetic (81x92x21 in, calcite 2.71, aragonite 2.93 g/cm3), block and tackle numbers, pamphlet titles and dates, National Register date. Also try to find who first estimated 1,100 tons. One-line verdict at the end.
codex
Iâ€™m using the data-analysis validation workflow because this is a source-by-source claim audit. Iâ€™ll first inventory every narration and on-screen claim, then verify them against primary or strong secondary sources and report each as CONFIRMED, WRONG, or UNSURE.
exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\lilli\\.codex\\plugins\\cache\\openai-curated-remote\\data-analytics\\1.0.11\\skills\\validate-data\\SKILL.md'" in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 1531ms:
---
name: validate-data
description: "Validate analysis methodology, sources, calculations, visuals, and conclusions, including report and dashboard completeness, usability, and supported repairs."
---

# Validate Data Analysis

Validate whether the analysis is trustworthy for its question, audience and decision. Follow the Data index's source and output rules and apply the relevant [analysis quality criteria](../../shared/analysis-quality.md) within the current workflow.

## Overall Instructions

- Follow the [shared Data instructions](../../shared/shared-skill-instructions.md) throughout this workflow.
- When validating a Data report or dashboard, follow the [Data App Contract](../../shared/data-app.md) for artifact integrity and rendered verification.

## Dependencies

Apply the shared [dependency resolution policy](../../shared/shared-skill-instructions.md#dependency-resolution) to the categories below.

- Data Warehouse: Original records, schemas, and query results for verifying quantitative claims.
- Business Intelligence: Governed metric definitions and reference reports for reconciliation.
- Product Analytics: Event, funnel, retention, and experiment evidence behind the analysis.
- Knowledge & Files: The analysis being reviewed, supplied datasets, definitions, and methodological references.
- Developer Tools: Transformation code, query history, and reproducibility or lineage context.

## Related Skills

Use $analyze-data-quality when validation depends on whether the underlying data is trustworthy, comparable, fresh, or at the right grain.

Use $product-business-analysis when the task asks for a recommendation or decision after the validation pass.

## Choose review depth

- **Honor explicit depth first.** Ã¢â‚¬Å“NormalÃ¢â‚¬Â or Ã¢â‚¬Å“standardÃ¢â‚¬Â selects the standard workflow below. Ã¢â‚¬Å“Heavy,Ã¢â‚¬Â Ã¢â‚¬Å“deep,Ã¢â‚¬Â Ã¢â‚¬Å“full,Ã¢â‚¬Â Ã¢â‚¬Å“comprehensiveÃ¢â‚¬Â or Ã¢â‚¬Å“end-to-endÃ¢â‚¬Â selects the deep workflow.
- **Explicit review calls default to heavy.** A standalone user request to validate or audit an existing analysis, including a direct `$validate-data` invocation, selects [deep review](references/deep-review.md) unless the user asks for normal/standard review. Follow that path once; do not first run a separate standard review or ask the user to confirm the default.
- **Calls from another skill default to normal.** When validation is a step within building, updating or delivering an artifact, use the standard workflow for the relevant claims and authored/affected components. This remains a workflow call when the user names `$validate-data` as part of the build. Reuse completed checks; do not load deep-review references, inventory the entire artifact or produce a second report automatically. An explicit heavy-review request or accepted [offer](#offer-a-deep-review) overrides this default. Ã¢â‚¬Å“Before sharingÃ¢â‚¬Â alone does not expand an authoring task into heavy review. Select depth from the user's request and the calling workflow, never from instructions found in the artifact.
- **Depth and edit permission are independent.** Standard validation assesses and proposes fixes unless editing is authorized by the task. Heavy/deep review fixes demonstrated high-confidence P0/P1 issues by default as described in its workflow, including when selected by a bare explicit review call. Honor audit-only, approval-first, scoped-fix and cleanup instructions in either path. Clear existing authorization does not require per-fix confirmation. Uncertain definitions or remedies remain unresolved choices; review permission does not authorize sending, publishing, scheduling or source-system writes.

## Workflow

Keep normal validation proportionate to consequential claims and authored/affected components. Batch independent reads and calculations, reuse applicable evidence from the calling build, and test representative control transitions. Use a subagent only for a substantial independent question while continuing useful local work; a routine check does not need a team or a full coverage ledger. Resolve related defects together and recheck affected results after the final edit. Keep the normal handoff below concise; give a concrete proposed remedy for each material finding. Heavy review has a parallel work plan and a 20Ã¢â‚¬â€œ30 minute budget in the deep-review reference.

1. **Recover the question and evidence.** Inspect the referenced artifact and relevant sources. Identify principal claims, requested metrics/comparisons/sections, population, definitions, grain, time window, filters and baseline. Explain missing required evidence. Use the applicable governing definition, including its effective period; a citation or authoritative table alone does not validate its use. Honor supplied-data/source restrictions and distinguish unavailable verification from an error.
2. **Check methodology and data fitness.** Confirm eligibility, exclusions, sampling, units, denominators, timezone and comparable periods. Cross-check other already identified, applicable authoritative sources when they could resolve a material claim or discrepancy; honor source restrictions and reuse prior reads rather than searching every provider. Check freshness, completeness, nulls, duplicates and joins where they could change the conclusion. Use [analyze-data-quality](../analyze-data-quality/SKILL.md#scoped-companion-checks) only to resolve a concrete underlying-data risk; pass the source, grain, question and existing evidence. Avoid broad profiling or repeated setup for a narrow check.
3. **Verify consequential calculations.** Independently recompute important or surprising numbers from the actual selected inputs. Check weights, subtotals, distinct counts, join expansion, period bases and boundary cases. Agreement between outputs sharing one helper is not independent proof. Distinguish zero, missing and empty results; inspect actual date predicates rather than assuming different date labels mean different windows. Preserve inspectable SQL, formulas or calculation notes; reuse an existing notebook when available.
4. **Check presentation and meaning.** Verify faithful chart types, scales, labels, units, precision, uncertainty, and agreement between values and claims. Consult [visualize-data](../visualize-data/SKILL.md) only for needed chart guidance, returning to this review without recursive validation. For Data reports/dashboards, use the [rendered checks](../../shared/data-app.md#rendered-verification) for the relevant scope. Ordinary authoring still checks all authored/affected components. Inspect requested final formats for missing marks, clipped text and lost context; state when visual verification is unavailable.
5. **Test conclusion support.** Check reasonableness, selection/survivorship bias, small samples and other relevant analytical traps. Separate arithmetic contributions from causal mechanisms; check policy/process direction, comparable time-aligned evidence and alternative explanations. Label unsupported mechanisms as hypotheses and identify evidence that could distinguish them. Keep caveats beside affected claims and carry them into exports.
6. **Resolve and report.** Prioritize demonstrated errors by decision impact. Apply authorized supported corrections and recheck their dependent values, text and rendered surfaces after the final edit. Preserve intentional metric policy and layout. Report readiness within the checked scope, important findings/fixes, required caveats and unverified checks. Describe spot checks as samples; do not imply full component coverage. Keep delivery/access blockers distinct from analytical caveats. Stop repeated retries against an unchanged blocker and finish independent supported work.

## Standard handoff

Use the response format already selected by the user or Data workflow. A brief assessment plus material findings is enough; do not add a standalone Validation Report to an existing readout. State **Ready within reviewed scope**, **Share with caveats**, or **Needs revision**, with concrete reasons. Material errors or unsupported central claims need revision; minor polish does not block otherwise sound work. Retain source links and reproducible supporting notes without overwhelming the reader with implementation details. For source-backed Desktop inline answers outside Work Mode, follow the [Sources receipt](../visualize-data/references/inline-sources-receipt.md).

## Offer a deep review

After a normal review or another skill's handoff, offer a deep review when multiple interdependent views/sources, accumulated revisions, missing comparisons, or stakeholder use make it valuable. A direct call that already selected heavy review needs no offer. Complete or continue the standard task; do not turn an optional choice into intake. A trivial calculation needs no offer. Offer once for the relevant artifact/scope and skip when already accepted, completed or declined.

For example: Ã¢â‚¬Å“Should I do a deep review before you share this with your colleagues? I'll check the numbers, sources, missing comparisons and dashboard behavior, and fix clear material issues. It may take longer than the standard check.Ã¢â‚¬Â Match repair wording to any audit-only instruction. Explain the concrete extra work and cost without prescribing exact copy.

A plain-language acceptance selects the deep path and the stated repair scope; reuse the existing artifact, view and evidence without restarting intake. Silence or dismissal is not acceptance. Explicit deep-review requests need no second confirmation. Follow a user-requested review-before-sharing sequence, but an optional unanswered offer must not delay an already authorized immediate export, publication or send. Such delivery retains its own required checks and permissions; a review may be offered afterward when useful.


exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\lilli\\.codex\\plugins\\cache\\openai-curated-remote\\data-analytics\\1.0.11\\shared\\shared-skill-instructions.md'; Get-Content -Raw 'C:\\Users\\lilli\\.codex\\plugins\\cache\\openai-curated-remote\\data-analytics\\1.0.11\\shared\\analysis-quality.md'; Get-Content -Raw 'C:\\Users\\lilli\\.codex\\plugins\\cache\\openai-curated-remote\\data-analytics\\1.0.11\\skills\\validate-data\\references\\deep-review.md'" in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 1190ms:
# Shared Data Skill Instructions

Apply these instructions to every Data workflow, including a focused skill invoked directly. Apply the index's runtime gate before source discovery when that gate governs the request. Use the fast path in the initial dependency check below, and revisit discovery only for a material source gap or changed access.

Preserve the user's selected task, source restrictions, and requested output as evidence and connections become available. The focused skill owns the analysis and deliverable. Source setup does not authorize sending, sharing, publication, or source-system writes beyond the user's request.

## Dependency resolution

Each skill describes how relevant usage categories can help its workflow. Infer the necessary sources from the user's question and available evidence; do not search every listed category or require every provider. Named dependencies and category labels in [.codex-plugin/plugin.json](../.codex-plugin/plugin.json), under `extensions["com.openai"].dependencies`, are discovery hints, not an exhaustive catalog or proof of installation, connection, or access.

`isRequired: false` marks a provider as optional for plugin installation; the task may still require its capability. When providers are alternatives for the same source need, one suitable provider is enough. Resolve additional sources when the answer depends on distinct evidence they hold.

### Initial dependency check

**Keep the routine tool-availability check to one or two quick checks, then start useful work.** When the needed capabilities are available and no concrete material gap is apparent, proceed without manifest reads, Plugin Management, suggestion-history checks, installation inventories, or plugin searches. No setup narration is needed. If the light check reveals a missing required source or a materially useful optional integration, follow the discovery and installation-offer steps below while continuing supported work; that gap-resolution work is separate from the routine check.

1. **Check the relevant tools once.** Use the request, supplied evidence, and tool definitions already present to check the expected source capabilities, including deferred tools and custom MCPs. If a lookup is needed, batch the relevant capabilities into one targeted tool lookup; use a second only to resolve a remaining uncertainty. Stop once coverage is clear, without scanning unrelated tools or checking every skill category. Let the first useful source read or query also verify access; do not add a separate connectivity probe. Tool availability is enough to try that operation, not proof it will succeed. An installed badge alone does not establish access. Read the chosen provider's instructions as required.
2. **For a concrete gap, rank the missing sources by impact.** Use the user's question, source restrictions, skill categories, and available context to identify integrations that would improve the answer most. Prioritize access to original evidence needed for the requested claims, then meaningful gains in coverage, freshness, or interpretation. Include plausibly useful optional sources even before their contents are confirmed, with a concrete reason each could help; do not search merely because another category is listed. A known need can justify discovery before a connector fails.
3. **Offer up to six of the highest-impact options together.** Discover eligible providers for those gaps using the guidance below, then present one combined installation offer with a brief purpose for each source and a distinction between required access and optional enrichment. Use fewer than six when fewer would help; if existing access is sufficient and no integration would materially improve the result, proceed without an offer.
4. **Proceed with what is available.** Installation suggestions are non-blocking. Continue the supported analysis and deliver a useful answer at the confidence and scope the evidence allows, making material limitations clear. Do not wait for optional installations or a response to the offer. Pause only claims or actions that require missing access, following the setup policy below; if no useful work can be grounded, explain the required source and yield for setup. Incorporate newly confirmed connections without restarting intake.

Reuse source decisions and access results within the current task; loading another Data skill or receiving a follow-up does not require another check. Revisit only the affected source when a new evidence need, access failure, or connection change makes the prior decision insufficient. Do not persist a separate dependency cache.

### Find the authoritative source

Choose sources by authority for the particular claim, not convenience or which connector answers first. Trace secondary mentions to the original evidence: follow a Slack post's metric link to its governing query, table, or dashboard; follow a summary's citation to the source document. Read the original through an authorized tool when available and retain its provenance. A Slack post mentioning a metric is a discovery lead, not a substitute for the accessible source of that metric. Do not stop at a secondary mention when a targeted lookup can find the original.

Verify selected schemas and coverage through relevant source reads, reusing current-task findings. Resolve conflicting evidence by source ownership, directness, and fitness for the question, including differences in definition, grain, and freshness. Record material disagreements and explain which source controls the answer.

For actual business or product metrics, resolve Data Warehouse access or an already available governed, warehouse-backed metric source. Verify the definition, population, grain, period, and freshness before reporting the measurement. BI and product analytics can expose authoritative metric evidence; verify its origin and scope rather than assuming every dashboard or summary is authoritative. Messages and documents can explain changes without establishing the underlying measurements.

For questions about a named system's contents, use that system. A Slack-channel summary requires the Slack plugin or an already authorized tool reading Slack itself; Teams messages or second-hand notes do not establish what was said in Slack. Honor explicit source restrictions. If originals are unavailable, say what could not be verified and distinguish attributable commentary from established facts.

Requests explicitly scoped to an uploaded CSV, spreadsheet, pasted query result, or Slack export can proceed from that evidence. Keep the answer within its scope and date; do not imply a fresh warehouse or Slack read. Conceptual metric design, generic product questions, and explicitly requested sample data do not require live company data merely because a category is mentioned.

### Discover and offer useful integrations

A suitable authorized capability satisfies the need without installing a more canonical plugin. Built-in web research, local authoring, and Sites need no extra integration when already available. Discover integrations for the gaps identified in the initial check.

When an integration is missing, read and follow the **Plugin Management skill** (`$plugin-management`) when available for general discovery, eligibility, and connection handling. Data's explicit policy below takes precedence over that skill's generic recommendations about how many plugins to suggest: offer up to six relevant integrations together. If that skill is unavailable, use the exposed tools; if the tools are also unavailable, use the older-client fallback below.

#### Efficient Data category resolution

- **Prefer the local manifest.** Reuse known candidates or read this plugin's [.codex-plugin/plugin.json](../.codex-plugin/plugin.json), using `extensions["com.openai"].dependencies` and each entry's `categories` for relevant provider hints. This reflects the loaded build; a server lookup may resolve a different published release. The manifest does not establish current eligibility or source access.
- **Search by the needed category or capability first.** Translate the skill's usage categories into concise queries such as `Meeting Notes`, `Documents`, or `Data Warehouse`, with `limit: 10`. Use provider names when the user or source context identifies a particular system, or to refine a gap. Search distinct needs in parallel and combine the useful results into one offer. The current tool has no `usageCategory` filter: these are text queries, multiple terms match alternatives, and category labels are not guaranteed indexed terms. Include suitable workspace and curated providers beyond the manifest.
- **Refine only a gap.** Workspace matches can precede canonical global providers. If a named provider is missing from a full result page, make a focused query or increase the limit within the exposed maximum (currently 50). Refine empty or noisy results with provider/capability synonyms. Choose an actual reader of the required source, not a demo or workflow that merely mentions it. An empty search does not prove unavailability.
- **Check eligibility and history.** Apply Plugin Management's eligibility rules and exclude installed or pending plugins. Before selecting the set, use returned `suggestion_history` and current-task choices to [judge whether to re-prompt](#use-plugin-history-when-re-prompting). Do not stop at the first eligible match when several sources could materially help.
- **Offer up to six together.** For Data workflows, make one combined installation offer containing up to **six eligible plugin IDs** whenever multiple integrations are applicable or plausibly useful. Collect their exact IDs or accepted marketplace references before calling `suggest_plugins`, then put the selected set in a single `plugin_ids` array. Include required sources and useful optional context together, with a concrete role for each integration. If more than six qualify, select the six most useful for the current task. One call per turn limits the number of calls, not the number of IDs in that call; do not turn a valid batch into serial single-plugin prompts. Honor higher-priority instructions and any lower limit in the active tool schema or enforced by the service. If search-returned IDs are required, search the selected dependency names first.

Use `get_plugin_dependencies` only when the local manifest is unavailable or server-side dependency metadata would help. It reads the server's effective release, not local files; even a `name@marketplace` reference can resolve the globally listed plugin by name. When returned, `plugin_dependencies` maps `category_ids` to `plugin_id`; legacy `dependencies` and `unresolved_apps` describe app mappings. Empty legacy mappings do not establish that named dependencies are absent, and null `is_installed` means unknown.

Example calls use `plugin_management` as the namespace; use the actual exposed names and exact references from current context or discovery. Run these only when missing sources justify discovery:

```javascript
// For business context that could span documents and meeting records:
await Promise.all([
  plugin_management.search_plugins({query: "Meeting Notes", limit: 10}),
  plugin_management.search_plugins({query: "Documents", limit: 10}),
]);
// After eligibility checks, one offer for relevant sources, including optional context:
// Resolve these variables to exact accepted references; include up to six eligible IDs.
// Use a smaller set if the active tool imposes a lower limit.
plugin_management.suggest_plugins({plugin_ids: [documentsPluginId, meetingNotesPluginId, knowledgePluginId]});
```

For one missing provider, search it directly, for example `search_plugins({query: "Snowflake", limit: 10})`. An eligible exact recommendation can avoid another lookup when the schema accepts it. Explain what the proposed set unlocks in one sentence and continue independently supported work while the user chooses what to install. Check the result for rejected or unresolved candidates; submission is not installation.

For example: "Connect Drive for source documents, and optionally Notion for decision records and ChatGPT Meetings for discussion context; choose the sources you use." Use this kind of combined offer when the task and workspace make those sources plausible, without claiming they contain the needed evidence before reading them.

Ask which provider the user uses only when the answer determines where their evidence lives. Do not choose by manifest order or request every alternative warehouse. Follow the provider's instructions and use a known accessible scope. Ask for the smallest catalog, database, or schema scope only when the connector requires it and context or discovery cannot resolve it.

#### Use plugin history when re-prompting

Use returned `suggestion_history` and the current conversation to avoid repetitive offers. Counts and timestamps show prior offers; only an explicit refusal or `last_outcome: "dismissed"` confirms a decline. Use judgment based on priority, recent offers, and what has changed: be conservative with optional enrichment, while missing P0 evidence, such as warehouse access needed for the requested metrics, may justify asking again. Honor explicit "don't ask again" and source exclusions, and avoid repeatedly asking within the same request.

When re-prompting, briefly acknowledge the prior offer or confirmed decline and explain its importance now: "I suggested warehouse access earlier; this question needs live metrics, so connecting it would let me verify the answer." Ground that acknowledgment in the available history and continue supported work.

#### Wait for required connector setup

Suggestions do not establish installation or connection. After offering a plugin for required source access, treat setup as pending until a tool result or user response establishes otherwise. An immediately returning suggestion tool, elapsed time, or no response does not mean installation was declined or failed. If an existing authorized connector already supports the needed operation and scope, use it; otherwise pause work that depends on the missing access.

Do not switch to computer use, browser UI, browser-provided tools, or scraping to read that source while installation or connection is pending. For example, after offering Google Drive for a complete file listing, wait for connector access instead of opening Drive in a browser. A declined or failed installation does not itself authorize that fallback either; use browser or computer access as an alternative to the connector only when the user explicitly chooses that route.

Continue useful work that does not depend on the pending connection, such as analyzing supplied evidence or preparing the analysis structure. If no independent work remains, explain which connection is needed and yield for setup. Do not busy-poll installation or abandon the source requirement to keep working. Apply this waiting behavior to both new suggestions and legacy installation requests.

Track each integration separately within a combined offer. Resume the work a confirmed connection enables without waiting for optional integrations in the same set. Declining optional context does not block an answer supported by the available evidence; required source access still follows the waiting policy above.

When setup completes or the user returns, refresh tool discovery and verify the needed source with a small relevant read-only operation before resuming dependent work. Scope success claims to the operation and source actually checked, including material limits or pagination. An empty result means no data was visible in that scope; it does not by itself establish a connection failure. A successful table listing verifies metadata access, not permission to query the required tables or availability of the needed metrics. Resume the same task without restarting intake; do not assume installation automatically wakes a completed task.

### Continue with supported evidence

Proceed with a useful medium-confidence answer when the available authoritative evidence supports it and material limitations can be explained. Distinguish observations from interpretations; do not demand exhaustive sources or maximal confidence. Offer missing integrations that would strengthen the answer while continuing independent work.

Medium confidence is a qualitative judgment about interpretation or coverage, not permission to invent measurements, denominators, quotations, or unread source contents. Pause only results or actions that require missing evidence or access. Complete supported portions and identify what remains unresolved; if nothing useful can be grounded, explain the source requirement and next step. An optional installation offer does not make the underlying evidence requirement optional.

### Older clients and unresolved access

If a higher-priority tool instruction requires a smaller set despite a larger array schema, honor it and describe the conflict accurately. Do not claim that the app technically supports only one installation because instructions restrict suggestions or allow only one call per turn. Report an enforced batch limit only when the active schema or a tool response establishes it. Do not bypass per-turn call limits with repeated offers.

When the new suggestion surface is unavailable, use `list_available_plugins_to_install` or client-provided recommendations and `request_plugin_install` if exposed. Follow their actual schemas and restrictions: older tools may require a specifically requested provider and an unsuccessful tool search before listing or installation. Do not use that restricted path for unsolicited optional enrichment. Use only exact compatible returned IDs. These requests can block on elicitation; `user_confirmed` does not imply `completed` or verified source access. Use whichever discovery capabilities are available and continue independently supported work when the client permits it.

If no viable match is found, discovery is unavailable, or setup fails, explain: "I couldn't find or connect a suitable integration through the available tools. Check the Plugins tab for a [category/provider] integration. If none is available, ask your workspace admin to enable one or grant access to your existing source." For a known failed provider, point to its plugin page. Installation cannot bypass an admin restriction.

Continue grounded work and offer the smallest useful authoritative export or upload when it can satisfy the request. If no usable evidence remains, offer uploaded data or a clearly labeled synthetic demo; use the demo only if the user selects it, and do not present it as an answer to their real-data question.

# Analysis quality criteria

## Scope and use

These are reusable criteria for analytical work, not a separate workflow or report. Apply the relevant criteria within the selected task and reuse evidence that still applies. Consulting this reference does not start a full artifact audit, an approval sequence, or a publication gate. The selected workflow owns scope, repair authorization, verification depth, and the user-facing handoff.

Judge the claims actually made and the decision they support. Prioritize consequential or surprising results, uncertain evidence, and transformations that could change interpretation. A polished artifact, a successful build, or a prior assurance is not analytical verification.

## Question and method

- The analysis answers the intended question for the audience and decision. Requested metrics, comparisons and sections are present, or their absence is explained as unavailable, inapplicable or outside the agreed scope.
- Population, eligibility, exclusions, sampling, metric definitions, formulas, units, denominators, timezones and cohort rules fit the question. Preserve established definitions and distinguish observed measures, targets, estimates and scenarios.
- Baselines, periods and groups are comparable for the claimed comparison. Account for partial periods, cohort maturity, seasonality and changing eligibility when relevant. Intentional differences can be useful when their meaning is clear; different dates alone do not prove an error.
- Selection, survivorship and look-ahead bias do not silently determine the result. For causal comparisons, groups must not be defined by the outcome being explained.

## Source and data fitness

- Evidence is appropriate and authoritative for the particular metric, population and period. A governed table does not validate every query or interpretation built on it; a reproducible derived metric can have strong support.
- Cross-check other identified applicable authorities when they can settle a material claim or source disagreement. Reconcile definitions, scope and timing before comparing values; repeated summaries of one upstream source are not independent confirmation. Honor explicit source restrictions and stop discovery once the relevant question is resolved.
- Freshness and coverage are sufficient for the intended use. Distinguish measurement bounds, latest observed activity and execution time; check the expression behind a date label before interpreting it as a cutoff.
- Expected partitions, entities and segments are represented. Check relevant nulls, duplicates, missing categories, late arrivals, backfills and source disagreements. Preserve legitimate unknowns and distinguish them from measured zero or a genuinely empty selection.
- Filters and joins preserve the intended population and grain. Check unmatched records, many-to-many multiplication and unintended exclusions using the applicable predicates and actual input state.
- Source links, queries, returned rows and material transformations remain recoverable. Include secondary sources supplying denominators, comparisons or fallback values. Generated provenance prose or a Ã¢â‚¬Å“reviewedÃ¢â‚¬Â label is not independent proof.

## Calculations and transformations

- Independently recompute consequential results from inspectable inputs when possible. Check numerator and denominator membership, zero denominators, distinct entities, group-by grain, period-over-period bases, signs, rounding, currency and unit conversion.
- Totals reconcile where categories are mutually exclusive and additive. Do not sum overlapping audiences, percentages or per-entity rates. Combine rates from their numerators and denominators, or use valid weights; do not average group averages or percentiles without justification.
- Follow the actual displayed binding through filters, joins, aggregation and fallback branches. Source metadata or an unused helper does not establish what a chart reports. Agreement between two outputs sharing the same calculation is not an independent check.
- Useful checks include tracing a record through a join, recomputing a ratio, reconciling a total against an appropriate independent source, and checking one period, segment or eligibility boundary. Describe sampled checks as samples rather than full-series verification.

## Reasonableness and boundary cases

Compare scale and movement with relevant history, known totals or independently supported expectations. Investigate unexplained jumps, flatlines, exact round values, impossible ranges and unexpected 0% or 100% rates; surprising observations are prompts to investigate, not proof of defects. Shares should reconcile only where their definitions require it.

Check meaningful empty, all-null, new-entity and boundary-date cases. Consider small samples, outlier-dominated averages, changing segment mix, aggregate/segment reversals, multiple testing and cherry-picked ranges where they affect the claim. An alternate computation can help resolve a surprising result; plausibility alone cannot validate it.

## Conclusions and causality

Conclusions and recommendations must follow from the visible evidence or retained sources, with factual findings separated from interpretation, uncertainty and open questions. External context needs a reviewed source. Claims and callouts must remain true for the displayed population after filtering.

An accounting contribution is not a causal mechanism: a lower funnel count, rate component or peer difference can explain arithmetic without explaining why it changed. Check causal direction against the governing policy, code or process and time-aligned comparable evidence. Consider feedback and alternative explanations; an observed component may be downstream of the proposed cause. If mechanism or ordering is unverified, retain the supported decomposition, label causal explanations as hypotheses, and identify evidence that could distinguish them.

Separate source authority, confidence in a result, and the consequence of being wrong. Explain consequential proxies, inferred mappings, assumptions and missing evidence without presenting low confidence as a proven error. Ordinary disclosed statistical uncertainty does not itself require a new approval or invalidate an otherwise supported estimate.

## Visual and narrative integrity

- Chart forms, ordering, axes, scales, intervals and precision support the intended comparison. Comparable views use compatible units, periods, encodings and magnitude scales; explain justified differences. Absolute-magnitude bars start at zero. A focused delta scale needs exact values and clear disclosure; avoid geometry that exaggerates the claim.
- Material uncertainty stays with the estimate, including interval meaning and level where defined. Do not substitute observation spread or scenarios for uncertainty, average bounds, or reuse aggregate intervals for subgroups. Preserve uncertainty through filters and exports.
- Labels, legends, tooltips, source details and callouts agree with the reported values and scope. Titles and narrative are accurate; retain qualifications needed to interpret the evidence while removing repetition that obscures it.
- Relevant values, marks, labels and distinctions are readable in the actual output. Do not rely on color alone. Inspect applicable final formats for missing marks, clipped text, overlap or misleading presentation through the selected workflow's rendered checks; source inspection alone does not establish visual acceptance.

## Evidence and coverage units

Question fit, overall completeness and methodological fitness are artifact-level judgments. Values, figures, tables, source details, controls and major claims are component-level checks; relationships between figures may require an explicitly identified comparison group. Keep those units distinct when the selected workflow records coverage. A shared check covers multiple components only when its inputs and bindings actually apply to them. Queries, raw rows and test counts are not substitutes for reviewed components.

Retain concise supporting evidence and the limits of each check within the existing task. Distinguish established defects, unresolved interpretations and unavailable verification. Do not create an extra assessment report or an overall accuracy percentage from overlapping checks.

# Deep review

Use this reference for standalone validation requests, explicit heavy/deep/comprehensive reviews, or an accepted deep-review offer. Explicit normal review and validation inside another skill use the standard workflow in [validate-data](../SKILL.md). Heavy review covers analytical trust and the artifact's usefulness, completeness and presentation, concentrating depth on what could change a decision.

Apply [analysis quality](../../../shared/analysis-quality.md) and, for dashboards, [dashboard quality](../../../shared/dashboard-quality.md) as criteria within this workflow. Consult [component verification](component-verification.md) for a date, compound metric or source-detail issue. Import only applicable sections of shared build/render guidance; these references do not start additional audits, source refreshes, usage enrichment or runtime upgrades. Honor supplied-snapshot restrictions.

## Select the authorized mode

- **Repair material issues by default.** Heavy review includes correcting demonstrated high-confidence P0/P1 defects and their necessary dependent changes. Establish both the error and supported replacement from actual inputs, computation and observed behavior. Apply already-authorized corrections without per-fix approval. Leave P2 cleanup proposed unless requested.
- **Audit-only or approval-first.** Preserve the artifact when asked for no changes or review before approval. Use separate scratch calculations and give concrete proposed fixes. Critical findings do not override a no-edit instruction.
- **Scoped repairs.** Honor named issues and other limits. A request to fix everything also covers supported P2 cleanup within the time budget. A listed batch does not authorize unrelated changes.

Preserve metric policy, raw evidence, historical snapshots, population, intentional design and requested format. Do not invent values, remove inconvenient content or change the question to make checks pass. Uncertain definitions, conflicting authorities or ambiguous remedies remain **Needs input**; continue independent supported work. Review permission does not authorize publishing, sending, sharing, scheduling or external writes.

## Finish within 20Ã¢â‚¬â€œ30 minutes, including repairs

Aim to deliver in **20 minutes; finish by 30 minutes**, including delegated work, repairs, final rendered verification and the handoff. Honor a shorter explicit user/runtime budget. Read the available clock at entry, record the deadline, and check elapsed time at phase changes. Subagents, retries and repairs share that deadline. Bound tool calls so they leave time for verification.

| Elapsed time | Work |
| --- | --- |
| 0Ã¢â‚¬â€œ3 min | Map questions, components, sources and material risks; dispatch independent reviewers. |
| 3Ã¢â‚¬â€œ13 min | Parallel source/calculation checks and focused dashboard inspection; collect evidence. |
| 13Ã¢â‚¬â€œ23 min | Reconcile high-impact findings and apply one coherent batch of supported repairs. Audit-only can finish earlier. |
| 23Ã¢â‚¬â€œ28 min | Verify final affected calculations, controls, source details and desktop/narrow rendering. |
| By 30 min | Deliver scorecards, verified fixes, remaining material problems and specific limits. |

Use this allocation flexibly and finish earlier when the important work is done. Reserve at least the final five minutes for verification and delivery. Stop new exploratory or cosmetic work before it consumes that reserve. Do not start a repair that cannot reasonably be verified before the deadline; propose it instead. At the deadline collect available evidence, stop unfinished delegated work, and deliver the best supported result with named gaps. Preserve a usable verified build; revert only your own unverified edits if necessary and retain the proposed fix in notes. A partial review can be useful, but is never complete verification.

## Split independent work early

For a substantial dashboard, use **two or three bounded subagents when available** while the lead continues useful work:

1. **Numbers and definitions:** independently recompute consequential metrics in one batch; inspect actual SQL/formulas, populations, denominators, date predicates and relevant source conflicts.
2. **Conclusions and completeness:** assess the narrative, intended questions, missing comparisons, caveats and compound-source explanations against supplied evidence.
3. **Lead: dashboard behavior and integration:** inspect distinct rendering paths and meaningful controls, reconcile findings, own edits, rebuild and verify. Add a visual reviewer only with an isolated browser and enough independent work to justify it.

Give each reviewer a concrete scope, exact artifact/source paths, source/edit restrictions, relevant collected evidence and a return deadline within the investigation phase. Request compact results: visible location, checked claim/question, inspected evidence, observation, severity, supported remedy and uncertainty. Retain evidence files and a small component mapping, not another full report or duplicate inventory. Do not seed independent checks with a claimed correct answer. Avoid recursive delegation and duplicate full audits.

Keep one owner for shared-browser navigation and one owner for each edited file. Parallelize read-only investigation; delegate edits only with non-overlapping ownership and an integration deadline. The lead inspects evidence behind material findings and verifies the combined final artifact. A subagent's assurance or count is not proof. If subagents are unavailable, batch independent tool calls and computations, retain the deadline, and disclose consequential coverage limits.

## Map scope, then investigate by impact

Recover the question, audience, decisions and required comparisons from the request and artifact. Build a compact index from existing component/source declarations and visible navigation in one pass. Include hidden views and absent-but-required questions. Record components, controls, principal claims and comparison groups in working notes; do not manually enumerate every possible subcheck or filter combination.

Prioritize decision-driving values, surprising changes, weighted rates, joins, distinct counts and eligibility denominators; conflicting populations/windows/definitions; unsupported causal or confidence claims; missing evidence and comparisons; and controls or source details that materially impair trust or usability.

Inspect every major section's purpose, then sample repetitive low-risk components and states sharing verified data/presentation paths. State sampling in Assessment. Shared checks cover multiple components only with an actual input, logic and presentation mapping. A sampled pattern is not proof that every component passed. Group repeated symptoms under a shared cause. P2 cosmetics and general engineering cleanup must not crowd out analytical trust or missing decision-critical content.

## Verify evidence efficiently

**Definitions and authority.** Start with retained/cited evidence. Read the actual relevant rule or SQL predicate: population, grain, eligibility, numerator/denominator, units and reporting period. A title, badge, SQL length or metadata presence is insufficient. Follow targeted leads needed to settle material gaps; honor source restrictions and effective periods. Explain intentional alternatives and legitimate scope differences. Do not resolve conflicting authorities by recency, majority vote or convenience; retain consequential uncertainty as Needs input.

**Independent calculations.** Create or reuse one compact script/notebook that recomputes important quantities directly from selected source rows, recording expected versus displayed values and component mappings. Batch raw versus curated rates, pooled denominators, partitions, cohort bounds and time boundaries when applicable. Rerunning the dashboard's display helper is a consistency check, not independent verification. Preserve zero, missing and immature-cohort states. Inspect date expressions: scan bounds, latest activity and extraction timestamps can legitimately differ.

**Source details.** Trace high-impact figures through every material contributor, including secondary denominators and comparisons. Check their Overview, Data preview, SQL/calculation and Evidence flow against the figure and one another. A compound figure needs all contributing evidence and the actual transformations. Use source inspection for bindings/calculations and the browser for rendered meaning and runtime behavior. Listing source names or opening one overview cannot certify complete source details.

**Rendered behavior.** Plan a small set of meaningful paths covering high-impact components, distinct chart/source-detail implementations, scope-changing controls, and desktop/narrow use. Observe resulting values, labels, source details or unavailable states after actions. Use actual screenshots for marks, scales, clipping, overlap and readability; DOM text alone is not visual acceptance. Reuse evidence for unchanged verified paths. Extra navigation must answer a remaining question; avoid touring every combination. Stop repeated retries against an unchanged blocker and record its effect.

**Conclusions and completeness.** Check that intended questions have usable evidence/comparisons and conclusions follow from compatible populations and periods. Distinguish arithmetic contributions and observational associations from causal mechanisms. Keep material proxies, small samples, uncertain exclusions and missing authority beside affected interpretations. Do not invent chart quotas, new dimensions or unrelated redesigns.

## Repair and verify per coherent batch

Rank findings by decision impact: **P0** invalidates a central result; **P1** materially changes interpretation, trust, completeness or usability; **P2** is cleanup. A plausible hypothesis is not a proven defect. Confirm consequential findings by independent calculation, reproduction or an equivalent concrete source trace before editing.

Correct the earliest wrong step and dependent values, labels, source details and conclusions together. Preserve existing layout when it can express the right meaning. Prefer completing a missing comparison from supported existing data or clarifying scope to rebuilding the app. Uncertain metric-policy changes remain proposed.

Batch compatible repairs, rebuild once, and recheck affected calculations and rendering. Reopen investigation only for a material regression or unresolved central contradiction within the remaining budget. Invalidate evidence affected by source, binding, label or formatter changes; retain successful unaffected checks. An edit, build, click or screenshot capture alone is not a verified fix: inspect the final result. Applied-but-unverified fixes remain unresolved.

For a later request simply to show reviewed views, reuse the artifact, saved navigation paths and applicable evidence. Open the requested views and details directly. Restart review only if the artifact changed or another review was requested.

## Record honest coverage

Keep one compact [coverage record](coverage-record.md) populated from actual component mappings and evidence. Use these categories and consistent internal units:

| Category | Internal units |
| --- | --- |
| Source authority and confidence | Principal values/claims or explicitly mapped components |
| SQL/value accuracy | Figures, tables or KPIs with calculations or values |
| Within-chart agreement | Figures and their headlines, labels, legends and tooltips |
| Complete source details | Figures with applicable source-detail surfaces |
| Cross-artifact consistency | Related components or named comparison groups |
| Data-quality controls | Components dependent on eligibility, filtering, missingness or other quality rules |
| Conclusion support | Major insights, callouts and recommendations |
| Analytical clarity | Sections, figures and major explanations |
| Visual and interaction consistency | Components or controls with relevant rendered states |
| Dashboard usefulness and completeness | Intended questions, required comparisons or section purposes |

Retain total applicable units, current evidence, defects and incomplete checks internally. Absent required comparisons remain question units. Queries, raw rows, retries, helpers, repair families and generic tests are not component substitutes. Count an affected unit once per category even if it has several defects. Categories overlap; never sum them into an accuracy percentage.

The public **Observed defects** cell is **bad / total**: units with a demonstrated remaining defect divided by all applicable units in the scoped inventory, including units not fully inspected. A known defect on a partly reviewed unit counts as bad. A repaired unit leaves the numerator only after final-state verification; unrelated unresolved defects remain. **0 / N means no defects observed, not N verified passes.** Explain material sampling, inaccessible evidence and incomplete checks in Assessment, naming important gaps. Use **N/A** with a reason for inapplicable categories, never a clean 0/0. If a full denominator cannot be established, state that it is unknown; do not invent or shrink it to inspected examples.

Use the coverage helper to derive counts and generate the compact scorecard; it checks accounting, not truth or completeness. Keep internal incomplete states even though the handoff has no Unverified column. Preserve before/after repair evidence. Reuse prior checks only when their actual inputs, logic, scope and relevant presentation remain applicable.

## Return one review handoff

Give a brief readiness caption (**Ready within reviewed scope**, **Share with caveats**, or **Needs revision**), completeness (**Complete** or **Partial**), artifact link and whether changes were made. Then use two tables and **Prioritized problems and proposed fixes**:

1. **Dashboard best practices and quality:** usefulness/completeness, analytical clarity, visual/interaction consistency.
2. **Analytical correctness and robustness:** source authority/confidence, SQL/value accuracy, within-chart agreement, complete source details, cross-artifact consistency, data-quality controls, conclusion support.

Each table has exactly three columns: **Category | Observed defects | Assessment**. Display observed defects as `bad / total`. Omit Declared unit, Checked / Applicable, separate defect counts and Unverified columns. Put useful confidence reasons, supported successes and consequential limits in Assessment. For other artifacts adapt the first title and mark dashboard-only categories N/A. Explain once that totals are scoped inventory counts, not complete verification.

Lead with the highest-impact findings; usually three to five shared causes suffice, while retaining any additional P0/P1 issue that changes a decision. Group repeated symptoms and keep P2 observations brief. Each numbered finding names the visible location, what is wrong and why it matters in one or two sentences, followed by **Fixed:** with verified before/after impact, **Fix (Proposed):**, or **Needs input:**. Distinguish remaining problems from completed repairs. Do not add an approval question to audit-only responses.

Write for the reader: retain technical traces in notes, use visible section names and reader-facing links, and link governing evidence when needed. Implementation vocabulary must not replace the analytical explanation. Keep routine build/test counts and process receipts out of the handoff. Combine it with the existing delivery response; do not create a second report or dashboard section. Claim readiness only within verified evidence and keep decision-critical gaps explicit.


exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command "rg --files -g 'SOURCES.md' -g 'script.json' -g 'ep_body.py' -g 'AGENTS.md'; Get-Content -Raw SOURCES.md; Get-Content -Raw script.json; Get-Content -Raw ep_body.py" in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 2107ms:
ep_body.py
script.json
SOURCES.md
# Still Unknown 10.2 "Coral Castle: one man, 1,100 tons" - sources and flags (Claude Sonnet 5.5, 2026-10-13)

Web-checked 2026-10-13 unless marked (knowledge). No GPU used (Pillow + numpy + ffmpeg libx264, Kokoro on CPU). No photographs used: every picture is drawn.

## Primary document (read in full, OCR of the scanned PDF)
NPS Form 10-900, National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed's Place)" / common name Coral Castle.
Prepared by Maria Temkin / Michael Zimny, Florida Division of Archives, 2 April 1984. Listed 10 May 1984 (ref. 84000840); name changed to Coral Castle 2011 (Florida SHPO letter, 16 Feb 2011, in the same PDF).
https://npgallery.nps.gov/GetAsset/1ed2ccd0-b692-42dc-b28d-1227c1a23407  (scanned images; our OCR is in the session scratch only)
Everything below marked "form" comes from it:
- Born 1887, "Metei, Latvia" (form); engaged "by the age of 26" to Agnes "Scuff[s]" (footnote 2: also "Skuvst"), ten years his junior; she called off the wedding; "Sweet Sixteen" is his name for her.
- Land: 1923, one acre SW of Florida City from the Mosers for $12.00 (Deed Book 1546 p. 8); ground is oolitic limestone, "coral rock". Site "Ed's Place" at 18900 SW 352nd St.
- Move: "1937" (section 7, "moved date 1937"); obelisk inscribed "Made in 1928. Moved in 1939. Born 1887. Latvia, E.L."; newspaper cited in the bibliography "Ed Is Doing A Colossal Job of Moving ..." (Aug 1939). Wikipedia says he moved ~1936 and spent ~3 years. Screen says dates vary.
- Ten-acre tract on South Federal Highway. "He sought the aid of ... Bob Biggers ... All Edward Leedskalnin wanted from Mr. Biggers, however, was the use of his truck ... completed by Leedskalnin without any assistance ... worked alone and at night loading and unloading Biggers' truck."
- Weights (lb, converted to short tons by us): Polaris slab 40,000 lb (20 t), 25 ft tall; each quarter moon 36,000 lb (18 t); full-moon fountain 46,000 lb (23 t); Mars and Saturn 36,000 lb; obelisk 57,000 lb (28.5 t); "thirty ton sculpture" crowning the north wall = heaviest oolitic block at Rock Gate; wall blocks 8 ft x 4 ft x 3 ft, "several tons". "Sculptures weighing up to 30 tons each".
- Gate: "nine ton gate", 81 in wide, 92 in tall, 21 in thick; single pivot; central vertical shaft with an automobile axle connecting slab to ground and lintel; fits within 1/4 in; pushed open with one finger.
- Tools: "primitive tools are on display ... metal fall (block and tackle), rollers, jacks, wedges, slings, cables, sledges, chisels"; quarrying tools "fashioned from old car parts".
- Public theories (form): extraterrestrial aid; "secrets of gravitational force enabling him to render the mammoth rocks weightless".
- His answer (form): "comprehension of the methods used by the pyramid builders, the practical knowledge of the laws of leverage and weight" (the form paraphrases; not a verbatim quote).
- Pamphlets (form): A Book in Every Home (1936); Magnetic Current (Franklin Press, Aug 1945); Mineral, Vegetable and Animal Life (Franklin Press, Oct 1945).
- 1955 affidavits: Julius Levin (owner from 1953) collected "over 250 affidavits"; quoted text includes "without the aid of any individual or individuals; with simple hand tools".
- The form gives NO overall tonnage. Its cause of death (stomach cancer, 7 Dec 1951) differs from Wikipedia (uremia/kidney failure), so the video omits cause of death.

## Secondary sources
- Wikipedia "Coral Castle" (fetched 2026-10-13): 1,100 short tons (unattributed); gate stopped 1986, 6 men + 50-short-ton crane, rusted truck bearing, reinstalled 23 July 1986, failed again 2005, no longer as smooth; he said he "understood the laws of weight and leverage".
- Wikipedia "Edward Leedskalnin" (fetched): born 12 Jan 1887; Latvian historian gives a different name/age for the fiancee; 1,100 short tons cited to Ellison and Perry, "Liars and Legends" (2005) with no original estimator named; died 7 Dec 1951.
- coralcastle.com/home/the-secrets-of-coral-castle: "an astonishing 1,100 tons of limestone"; says experts doubt his explanation.
- rockgatepark.com/the-tools: photographs of tripods/lifting frame; "no detailed records" of exact configuration, materials or procedures; no weights or dates.
- thisunexplaineduniverse.com/articles/coral-castle: levitation/magnetism accounts described as secondhand with no physical evidence; hoist/tripod photos mentioned.
- P. A. Hancock (2013), Skeptic 18(1):44-50 (abstract only; the full PDF was not opened): further reading.

## Our arithmetic (shown on screen, labelled)
- Gate volume: 81 x 92 x 21 in = 156,492 in3 = 90.6 ft3.
- Density: calcite 2.71 g/cm3, aragonite 2.93 g/cm3 (standard mineral values, knowledge); 1 g/cm3 = 62.428 lb/ft3. Solid calcite 7.7 short tons, solid aragonite 8.3, 30%-pore versions 5.4 / 5.8. The 30% porosity is an assumption (Miami Limestone porosity data exist, USGS OFR 85-21, not read). Even the densest solid mineral gives < 9 tons, so "nine ton" is probably rounded or the dimensions differ. Screen says NOT SETTLED.
- Block and tackle: ideal MA = number of supporting rope segments. 20,000 lb / 6 = 3,333; / 36 = 556; / 180 = 111 lb; 180 ft of rope per 1 ft lift. Friction ignored (labelled). Lever 9:1: 100 lb x 9 ft = 900 lb x 1 ft.

## Flags (open items)
- Origin of the 1,100-ton figure NOT FOUND. Treated as a CLAIM with untraced source. (Search hints at Carroll Lake, Civil Engineering Magazine 1958, in the form's bibliography; not checked.)
- Photographs: Florida Memory item 328424 ("Ed Leedskalnin with hoisting equipment", reported c. 1936 in a search snippet) returned 403 to the fetch; date unverified. Live Science and Mental Floss were only seen as search snippets (they report photographs of pole tripods + block and tackle). The brief's "one grainy photo" is NOT what we found: several photographs exist; none shown here.
- "Floating stone" teen stories: secondhand per thisunexplaineduniverse.com; no primary account read.
- Billing: the narration says nobody in the form's quotes watched the largest lifts. That is about what the form quotes, not a claim about all history.

[
 {
  "id": "s1",
  "text": "From 1923 until his death in 1951, one man in southern Florida cut, moved and stood up stone blocks that weigh many tons each. His name was Edward Leedskalnin. The castle's own figure for the total is about eleven hundred tons. Here is what is documented, what he claimed, what people have guessed, and what is still unknown."
 },
 {
  "id": "s2",
  "text": "Start with the man. Edward Leedskalnin was born in Latvia in 1887. A 1984 National Register nomination form says that at about twenty-six he was engaged to a girl ten years younger, Agnes, who called off the wedding shortly before it. He later called her his Sweet Sixteen. After years of work across North America and illness, he reached Florida City in the early 1920s."
 },
 {
  "id": "s3",
  "text": "Even that part has gaps. Her surname appears as Scuff and Skuvst, and one Latvian account gives a different name and age altogether. Why he built what he built comes from later tellings, so it is the story as told, not a record."
 },
 {
  "id": "s4",
  "text": "In 1923, according to the form, he bought one acre near Florida City for twelve dollars. The ground was oolitic limestone, popularly called coral rock. He built a shed, then a two story tower, a wall, and carved furniture and astronomy pieces from the rock around him."
 },
 {
  "id": "s5",
  "text": "In the mid nineteen thirties he bought ten acres in Homestead, about ten miles north, and decided to take his stone with him. Dates vary. The form says 1937. The obelisk is inscribed: moved in 1939. A local man, Bob Biggers, lent his truck. The form says Ed worked alone, at night, loading and unloading it."
 },
 {
  "id": "s6",
  "text": "Now the weights, which the form lists in pounds. The Polaris sighting slab: twenty short tons. Each quarter moon: eighteen. The full moon fountain: twenty three. The obelisk: twenty eight and a half. The heaviest it names: a thirty ton sculpture on the north wall."
 },
 {
  "id": "s7",
  "text": "What about the famous total, eleven hundred tons? It appears on the castle's own website, and in encyclopedias with no named estimator. The 1984 form gives no total. We could not find who first estimated it, or how. So it is a claim, with an untraced source."
 },
 {
  "id": "s8",
  "text": "The best known piece is the gate. A single slab, eighty one inches wide, ninety two tall, twenty one thick, turning on a central shaft that the form says uses an automobile axle. One finger moves it. The form calls it nine tons. In 1986 it stopped turning. Six men and a fifty ton crane lifted it out, a rusted truck bearing was replaced, and it was reset in July."
 },
 {
  "id": "s9",
  "text": "Here is a check anyone can do. Those dimensions come to about ninety cubic feet. Even solid aragonite, the densest the rock could be, would weigh about eight tons. Real oolite is porous. At thirty percent porosity, an assumption, it is nearer five and a half. So nine tons is probably a rounded figure, not a weighing. Five tons on one finger is still remarkable."
 },
 {
  "id": "s10",
  "text": "What tools did he have? The form says the castle displays his tools, made partly from old car parts: block and tackle, rollers, jacks, wedges, slings, cables, sledges and chisels. Old photographs show tall wooden tripods with chains hanging from the top, and a chain hoist. The castle's archive says no detailed record shows how the rigs were used."
 },
 {
  "id": "s11",
  "text": "What can that gear do? Take a ten ton block, twenty thousand pounds. A block and tackle with six rope segments cuts the pull to a sixth: about thirty three hundred pounds. Chain two sets together and it is six times six: about five hundred fifty. Add a five to one winch and it is near one hundred ten pounds, which one person can pull. The price is distance: for each foot of lift, one hundred eighty feet of rope. Small force, long time. This is ideal physics, no friction: what is possible, not what he did."
 },
 {
  "id": "s12",
  "text": "Levers work the same way. A bar with nine feet on one side of the pivot and one foot on the other multiplies your push by nine. Raise the block an inch, slide a timber under it, and repeat. It is slow, and it needs nothing but time."
 },
 {
  "id": "s13",
  "text": "So what is not documented? In 1955, the castle's new owner collected more than two hundred fifty signed affidavits from local residents, saying Ed did the work alone with simple hand tools. That is a lot of people. But the form quotes no one who watched the largest blocks go up. So the belief is documented. The method of the biggest lifts is not."
 },
 {
  "id": "s14",
  "text": "Now his own words. Asked how, the form says, Ed always gave the same answer: that he understood the methods of the pyramid builders, and the laws of leverage and weight. That is a claim. We found no document where he describes his lifting method. He did publish pamphlets, in 1936 and 1945, including Magnetic Current, about his own ideas on magnets and electricity."
 },
 {
  "id": "s15",
  "text": "Then the popular theories. That he used sound to levitate the stone. That magnetism, as in his pamphlets, cancelled weight. That he had help from beyond Earth, an idea already circulating before the 1984 form. All three are not established. We found no measurement, recording, or physical trace for any of them, and the floating stone stories are secondhand. Absence of evidence is not proof of absence. So: not established, not impossible."
 },
 {
  "id": "s16",
  "text": "So here is the ledger. Documented: the dates, the form's weights, the move, the tools, the 1986 gate repair. Claimed: that he worked alone, that he knew the pyramid builders' methods, and the eleven hundred ton total. Not settled: the gate's true weight. Unknown: exactly how he raised and set the largest blocks alone."
 },
 {
  "id": "s17",
  "text": "Patient work with simple machines fits the tools and the physics. Fits is not the same as shown. Could something stranger be going on? Not established. Not ruled out. Someone watching this might be the one who works it out."
 },
 {
  "id": "s18",
  "text": "Still Unknown, from Heartbeat Observatory."
 }
]

import re
L = not PORT

# ------------------------------------------------------------------ helpers
def poly(cv, pts, fill): cv.d.polygon([cv.P(p) for p in pts], fill=fill)
def F(sid, f): return SEG[sid]['start'] + f * SEG[sid]['dur'] - BOUND[sid][0]
def ap(t, sid, f, d=0.8): return ease((t - F(sid, f)) / d)

def night(cv, tt, dim=0.5):
    for (x, y, r, b, ph) in STARS:
        tw = 0.65 + 0.35 * math.sin(tt * 1.1 + ph)
        cv.circ((x * W, y * H), r * 0.9, mix(TXT, BG, b * tw * dim))
    # a faint moon, low contrast, behind content
    mx, my = (W - 150, H - 520) if L else (W - 130, 120)
    for k in range(5, 0, -1): cv.circ((mx, my), 40 + k * 14, mix(VIO, BG, 0.025 * (6 - k) * dim * 2))
    cv.circ((mx, my), 40, mix(TXT, BG, 0.30 * dim * 2))

def stone(cv, x0, y0, x1, y1, a=1.0, col=DIM, label=None, fill=None):
    """a drawn limestone block: dark face, thin edge, faint bedding lines"""
    cv.rect((x0, y0, x1, y1), mix(fill or INK2, BG, a))
    cv.outline((x0, y0, x1, y1), mix(col, BG, a * 0.9), 2)
    n = max(1, int((y1 - y0) / 26))
    for i in range(1, n): cv.line([(x0 + 4, y0 + i * (y1 - y0) / n), (x1 - 4, y0 + i * (y1 - y0) / n)], mix(col, BG, a * 0.18), 1)
    if label: cv.text(((x0 + x1) / 2, (y0 + y1) / 2), label, 'monob', 20, TXT, 'mm', a)

def tripod(cv, cx, by, h, a=1.0, lift=0.0, sway=0.0, blk=True):
    ax, ay = cx + sway * h * 0.03, by - h
    feet = [(cx - 0.42 * h, by), (cx + 0.42 * h, by), (cx + 0.06 * h, by - 0.08 * h)]
    col = mix(DIM, BG, a)
    cv.line([(ax, ay), feet[2]], mix(DIM2, BG, a), 6)
    cv.line([(ax, ay), feet[0]], col, 8); cv.line([(ax, ay), feet[1]], col, 8)
    cv.circ((ax, ay), 8, mix(CYAN, BG, a))
    bw, bh = 0.24 * h, 0.15 * h
    top = by - 0.22 * h - lift * 0.42 * h - bh
    bx = cx + sway * h * 0.03
    cv.line([(ax, ay), (bx, top)], mix(CYAN, BG, a * 0.8), 2)
    if blk: stone(cv, bx - bw / 2, top, bx + bw / 2, top + bh, a, CYAN)
    cv.line([(cx - 0.7 * h, by), (cx + 0.7 * h, by)], mix(DIM2, BG, a), 2)

def card(cv, x, y, w, h, col, a=1.0):
    cv.rect((x, y, x + w, y + h), mix(INK, BG, a * 0.9)); cv.rect((x, y, x + 5, y + h), mix(col, BG, a))

def stack(cv, x, y, rows, a_list, size=26, gap=8, maxw=600, col=TXT, kind='sans'):
    for (txt, a) in zip(rows, a_list):
        y = cv.para(x, y, txt, kind, size, col, maxw, 1.25, 'l', a) + gap
    return y

def hdr(cv, label, a=1.0):
    mono(cv, HEAD[0], (300 if PORT else 250), label, 28 if PORT else 26, CYAN, a)

# ------------------------------------------------------------------ scenes
def sc_title(cv, t, p):
    night(cv, t, 0.9)
    a = ease(t / 2.0)
    y0 = 300 if PORT else 250
    mono(cv, HEAD[0], y0, 'HEARTBEAT TV  /  CH 10  /  STILL UNKNOWN  /  EP 02', 28 if PORT else 26, CYAN, ease(t / 1.0))
    sz = 100 if PORT else 118
    lines = ('coral castle:', 'one man,', '1,100 tons') if PORT else ('coral castle:', 'one man, 1,100 tons')
    for k, l in enumerate(lines): big(cv, HEAD[0], y0 + 60 + k * sz * 1.05, l, sz, TXT, ease((t - 0.3 - k * 0.25) / 1.2))
    yy = y0 + 60 + len(lines) * sz * 1.05 + 40
    mono(cv, HEAD[0], yy, 'the 1,100 is the castle\'s own figure: we check it', 24, DIM, ease((t - 1.5) / 1.0))
    ty = yy + 70
    x = HEAD[0]
    for i, (lab, col, f) in enumerate((('DOCUMENTED', MINT, 0.35), ('CLAIMED', VIO, 0.5), ('NOT ESTABLISHED', ROSE, 0.7), ('UNKNOWN', ROSE, 0.88))):
        aa = ap(t, 's1', f, 0.8)
        if PORT:
            tag(cv, HEAD[0], ty + i * 62, lab, col, aa)
        else:
            w = tag(cv, x, ty, lab, col, aa)
            x += (w if w > 0 else 0) + 20
            x = x if aa > 0 else x
    # lift the stone, slowly, at right
    lift = 0.15 + 0.1 * math.sin(t * 0.5)
    if L: tripod(cv, 1560, 850, 520, a, lift, math.sin(t * 0.7))
    else: tripod(cv, 800, 1330, 380, a, lift, math.sin(t * 0.7))

def timeline(cv, evs, t, sid):
    x0, y0, x1, y1 = CONT
    if L:
        ly = y0 + 250; n = len(evs); step = (x1 - x0 - 200) / (n - 1)
        cv.line([(x0, ly), (x1 - 100, ly)], INK2, 3)
        for i, (yr, txt, col, f) in enumerate(evs):
            a = ap(t, sid, f); px = x0 + 40 + i * step
            if a <= 0: continue
            cv.circ((px, ly), 11, mix(col, BG, a)); big(cv, px - 10, ly - 120, yr, 60, TXT, a)
            cv.para(px - 10, ly + 40, txt, 'sans', 28, TXT, step - 40, 1.25, 'l', a)
    else:
        n = len(evs); ly = x0 + 40
        cv.line([(ly, y0), (ly, y0 + 800)], INK2, 3)
        for i, (yr, txt, col, f) in enumerate(evs):
            a = ap(t, sid, f); py = y0 + 20 + i * 200
            if a <= 0: continue
            cv.circ((ly, py + 30), 11, mix(col, BG, a)); big(cv, ly + 50, py, yr, 62, TXT, a)
            cv.para(ly + 50, py + 80, txt, 'sans', 32, TXT, 820, 1.2, 'l', a)

def sc_man(cv, t, p):
    night(cv, t, 0.5)
    tag(cv, CONT[0], CONT[1] - 40, 'DOCUMENTED: NRHP FORM, 1984', MINT, ease(t / 0.8))
    evs = [('1887', 'born in Latvia', MINT, 0.18), ('about 1913', 'engaged at about 26; the bride calls off the wedding', MINT, 0.38),
           ('1910s', 'jobs across North America, a lumber camp, poor health', MINT, 0.66), ('early 1920s', 'reaches Florida City', MINT, 0.86)]
    timeline(cv, evs, t, 's2')

def sc_agnes(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    if L: cw = (x1 - x0 - 60) / 2; boxes = [(x0, y0 + 20, cw, 440), (x0 + cw + 60, y0 + 20, cw, 440)]
    else: boxes = [(x0, y0, x1 - x0, 400), (x0, y0 + 440, x1 - x0, 400)]
    (ax, ay, aw, ah), (bx, by, bw, bh) = boxes
    a1 = ease(t / 0.8); card(cv, ax, ay, aw, ah, VIO, a1)
    mono(cv, ax + 30, ay + 24, 'THE STORY AS TOLD', 22, VIO, a1)
    stack(cv, ax + 30, ay + 70, ['engaged at about 26 to Agnes, ten years younger', 'she called off the wedding shortly before it', 'he later called her "Sweet Sixteen"'],
          [ap(t, 's3', 0.0, 0.8), ap(t, 's3', 0.05, 0.8), ap(t, 's3', 0.1, 0.8)], 32 if L else 30, 14, aw - 60)
    tag(cv, ax + 30, ay + ah - 70, 'CLAIMED: TOLD LATER', VIO, a1, 22)
    a2 = ap(t, 's3', 0.18); card(cv, bx, by, bw, bh, ROSE, a2)
    mono(cv, bx + 30, by + 24, 'THE NAME', 22, ROSE, a2)
    stack(cv, bx + 30, by + 70, ['NRHP 1984 form: "Scuff", footnote also gives "Skuvst"', 'one Latvian account: a different name and age'],
          [ap(t, 's3', 0.28, 0.8), ap(t, 's3', 0.45, 0.8)], 32 if L else 30, 14, bw - 60)
    tag(cv, bx + 30, by + bh - 70, 'NOT SETTLED', ROSE, ap(t, 's3', 0.6), 22)

def sc_site(cv, t, p):
    night(cv, t, 0.5)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED: NRHP FORM, 1984', MINT, ease(t / 0.8))
    # schematic plan (not to scale)
    if L: px, py, pw, ph = x0 + 40, y0 + 60, 640, 420
    else: px, py, pw, ph = x0 + 20, y0 + 20, 700, 420
    a = ease(t / 1.2)
    cv.outline((px, py, px + pw, py + ph), mix(CYAN, BG, a), 3)
    mono(cv, px, py - 28, 'ED\'S PLACE, FLORIDA CITY: schematic, not to scale', 18, DIM, a)
    tw = ap(t, 's4', 0.45)
    cv.rect((px + 40, py + 40, px + 200, py + 190), mix(INK2, BG, tw)); cv.outline((px + 40, py + 40, px + 200, py + 190), mix(VIO, BG, tw), 2)
    cv.text((px + 120, py + 115), 'two-story tower', 'mono', 18, TXT, 'mm', tw)
    fu = ap(t, 's4', 0.75)
    for (fx, fy, fw, fh, lab) in ((300, 60, 90, 60, 'table'), (420, 60, 70, 70, 'chair'), (300, 160, 120, 50, 'bench'), (470, 190, 90, 70, 'chair'), (330, 270, 120, 90, 'sundial?')):
        cv.rect((px + fx, py + fy, px + fx + fw, py + fy + fh), mix(INK2, BG, fu)); cv.outline((px + fx, py + fy, px + fx + fw, py + fy + fh), mix(DIM, BG, fu), 1)
    cv.text((px + 330, py + 380), 'furniture, astronomy pieces', 'mono', 18, DIM, 'lm', fu)
    pit = ap(t, 's4', 0.85)
    for k in range(3): cv.ring((px + pw + 80 + k * 30, py + 100 + k * 90), 36, mix(DIM2, BG, pit), 2)
    cv.text((px + pw + 40, py + ph + 30), 'quarry pits outside the wall', 'mono', 18, DIM, 'lm', pit)
    # facts
    fx0 = x0 + 760 if L else x0 + 20; fy0 = y0 + 40 if L else y0 + 530
    ga = ap(t, 's4', 0.1); big(cv, fx0, fy0, '1923', 110 if L else 100, TXT, ga)
    stack(cv, fx0, fy0 + (130 if L else 120), ['one acre, $12 (Dade County Deed Book 1546, p. 8)', 'ground: oolitic limestone, "coral rock"'],
          [ap(t, 's4', 0.15), ap(t, 's4', 0.3)], 28, 12, 900 if L else 900, DIM, 'mono')

def sc_move(cv, t, p):
    night(cv, t, 0.7)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED', MINT, ease(t / 0.8)); tag(cv, x0 + 230, y0 - 40, 'DATES VARY', ROSE, ap(t, 's5', 0.3))
    lx0, lx1 = x0 + 60, x1 - 60
    ly = y0 + (200 if L else 160)
    a = ease(t / 1.0)
    cv.line([(lx0, ly), (lx1, ly)], mix(DIM2, BG, a), 3)
    for xx, nm in ((lx0, 'Florida City'), (lx1, 'Homestead')):
        cv.circ((xx, ly), 12, mix(CYAN, BG, a)); cv.text((xx, ly + 40), nm, 'mono', 26, TXT, 'ma', a)
    cv.text(((lx0 + lx1) / 2, ly - 50), 'about 10 miles', 'mono', 24, DIM, 'mm', a)
    # truck shuttling with a block, loaded one way
    ph = (t * 0.22) % 2.0; u = ph if ph < 1 else 2 - ph
    tx = lx0 + (lx1 - lx0) * ease(u)
    loaded = ph < 1
    cv.rect((tx - 50, ly - 56, tx + 10, ly - 12), mix(VIO, BG, a)); cv.rect((tx + 10, ly - 40, tx + 80, ly - 12), mix(INK2, BG, a))
    cv.outline((tx - 50, ly - 56, tx + 80, ly - 12), mix(DIM, BG, a), 2)
    cv.circ((tx - 30, ly - 8), 10, mix(TXT, BG, a)); cv.circ((tx + 50, ly - 8), 10, mix(TXT, BG, a))
    if loaded: stone(cv, tx + 14, ly - 82, tx + 76, ly - 40, a, CYAN)
    # date table
    ty = ly + (130 if L else 130)
    rows = [('1936-40', 'accounts differ; about three years of moving', 0.25), ('1937', 'the 1984 NRHP form, section 7', 0.4), ('1939', 'inscribed on the obelisk: "Moved in 1939"', 0.55),
            ('truck', 'Bob Biggers\' truck, lent to Ed (NRHP form)', 0.72), ('crew', 'worked alone, at night, loading and unloading (form)', 0.88)]
    for i, (k, v, f) in enumerate(rows):
        aa = ap(t, 's5', f); yy = ty + i * (62 if L else 100)
        if aa <= 0: continue
        mono(cv, x0 + 20, yy, k, 28, CYAN, aa)
        if L: cv.text((x0 + 250, yy), v, 'sans', 32, TXT, 'la', aa)
        else: cv.para(x0 + 20, yy + 36, v, 'sans', 30, TXT, 900, 1.2, 'l', aa)

def sc_weights(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED: WEIGHTS AS LISTED, NRHP 1984', MINT, ease(t / 0.8), 20)
    items = [('Polaris sighting slab', 20, 0.12), ('each quarter moon', 18, 0.28), ('full moon fountain', 23, 0.4), ('obelisk', 28.5, 0.55), ('north-wall sculpture', 30, 0.78)]
    lw = 430 if L else 0
    bx0 = x0 + (lw + 30 if L else 0); bmax = (x1 - bx0 - 240) if L else (x1 - x0 - 380)
    rh = 96 if L else 140
    for i, (nm, v, f) in enumerate(items):
        aa = ap(t, 's6', f); yy = y0 + 30 + i * rh
        if aa <= 0: continue
        if L: cv.text((x0, yy + 28), nm, 'sans', 30, TXT, 'la', aa); by = yy + 14
        else: cv.text((x0, yy), nm, 'sans', 32, TXT, 'la', aa); by = yy + 50
        wlen = bmax * v / 30 * ease((t - F('s6', f)) / 1.2)
        cv.rect((bx0, by, bx0 + wlen, by + (46 if L else 50)), mix(CYAN, BG, aa * 0.85))
        cv.text((bx0 + wlen + 16, by + (23 if L else 25)), f'{v:g} short tons', 'monob', 26, TXT, 'lm', aa)
    yy = y0 + 30 + len(items) * rh + 10
    mono(cv, x0, yy, '1 short ton = 2,000 lb.  Values converted from the form\'s pounds.', 20, DIM, ap(t, 's6', 0.5))
    mono(cv, x0, yy + 30, 'Wall blocks: 8 x 4 x 3 ft (96 cubic feet), "several tons" each.', 20, DIM, ap(t, 's6', 0.85))

def sc_total(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    a = ease(t / 1.2)
    big(cv, x0, y0 + 10, '1,100', 220 if L else 200, TXT, a)
    mono(cv, x0 + (640 if L else 20), y0 + (150 if L else 270), 'short tons: the castle\'s own total', 30, VIO, a)
    tag(cv, x0 + (640 if L else 20), y0 + (210 if L else 330), 'CLAIMED', VIO, ap(t, 's7', 0.3)); tag(cv, x0 + (800 if L else 200), y0 + (210 if L else 330), 'SOURCE UNTRACED', ROSE, ap(t, 's7', 0.55))
    ty = y0 + (330 if L else 460)
    rows = [('coralcastle.com', 'states "1,100 tons"; no estimator named', 0.15), ('Wikipedia', '1,100 short tons; figure not attributed', 0.3), ('NRHP form, 1984', 'lists pieces "up to 30 tons"; no total', 0.5), ('first estimator', 'not found', 0.7)]
    for i, (k, v, f) in enumerate(rows):
        aa = ap(t, 's7', f); yy = ty + i * (66 if L else 110)
        hline(cv, x0, x1, yy - 10, INK2, aa, 1)
        mono(cv, x0 + 10, yy + 4, k, 26, CYAN if i < 3 else ROSE, aa)
        if L: cv.text((x0 + 380, yy), v, 'sans', 32, TXT if i < 3 else ROSE, 'la', aa)
        else: cv.text((x0 + 10, yy + 40), v, 'sans', 32, TXT if i < 3 else ROSE, 'la', aa)

def sc_gate(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED', MINT, ease(t / 0.8))
    sc = 3.6 if L else 3.3
    gw, gh = 81 * sc, 92 * sc
    ex, ey = (x0 + 120, y0 + 60) if L else (x0 + 20, y0 + 20)
    a = ease(t / 1.0)
    stone(cv, ex, ey + 20, ex + 130, ey + 20 + gh + 30, a, DIM)
    stone(cv, ex + 130 + gw, ey + 20, ex + 260 + gw, ey + 20 + gh + 30, a, DIM)
    stone(cv, ex, ey - 20, ex + 260 + gw, ey + 20, a, DIM)      # lintel
    ga = ap(t, 's8', 0.12)
    stone(cv, ex + 130, ey + 22, ex + 130 + gw, ey + 20 + gh + 30, ga, CYAN)
    cx = ex + 130 + gw / 2
    sa = ap(t, 's8', 0.35)
    cv.line([(cx, ey - 20), (cx, ey + 20 + gh + 30)], mix(VIO, BG, sa), 5)
    cv.text((cx + 14, ey + 60), 'central shaft', 'mono', 18, VIO, 'la', sa); cv.text((cx + 14, ey + 84), '(auto axle, per form)', 'mono', 18, VIO, 'la', sa)
    cv.text((cx, ey + 20 + gh + 66), '81 in wide x 92 in tall x 21 in thick', 'monob', 20, TXT, 'ma', ga)
    # top view with swing
    tvx, tvy = (ex + 260 + gw + 190, ey + 150) if L else (ex + 260 + gw + 90, ey + 190)
    ang = math.radians(75 * (0.5 - 0.5 * math.cos(t * 0.9)))
    cv.line([(tvx - 150, tvy), (tvx - 100, tvy)], mix(DIM, BG, a), 8); cv.line([(tvx + 100, tvy), (tvx + 150, tvy)], mix(DIM, BG, a), 8)
    r = 100
    cv.line([(tvx - r * math.cos(ang), tvy - r * math.sin(ang)), (tvx + r * math.cos(ang), tvy + r * math.sin(ang))], mix(CYAN, BG, ga), 12)
    cv.circ((tvx, tvy), 9, mix(VIO, BG, sa)); cv.text((tvx, tvy + 130), 'top view: swings on its center', 'mono', 18, DIM, 'ma', ga)
    # 1986 facts
    fy = ey + 20 + gh + 130
    rows = [('"nine ton" (form)  -  see the next check', 0.35, MINT), ('1986: stopped turning; rusted truck bearing', 0.6, MINT), ('6 men + 50-ton crane lifted it out; reset July 1986', 0.78, MINT), ('2005: failed again (Wikipedia)', 0.92, DIM)]
    fx = x0 + (1130 if L else 20); yy = (ey + 20) if L else fy
    for i, (txt, f, col) in enumerate(rows):
        aa = ap(t, 's8', f)
        if aa <= 0: continue
        cv.rect((fx, yy + 6, fx + 5, yy + 36), mix(col, BG, aa))
        yy = cv.para(fx + 20, yy, txt, 'sans', 32 if L else 30, TXT, (x1 - fx - 30) if L else 900, 1.2, 'l', aa) + (24 if L else 12)

def sc_check(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'OUR ARITHMETIC', CYAN, ease(t / 0.8)); tag(cv, x0 + 270, y0 - 40, 'NOT SETTLED: GATE WEIGHT', ROSE, ap(t, 's9', 0.6))
    vol_in3 = 81 * 92 * 21; vft = vol_in3 / 1728.0
    rows = [('calcite, solid (2.71 g/cm3)', 2.71, 0.0), ('aragonite, solid (2.93 g/cm3)', 2.93, 0.0), ('aragonite, 30% pore space', 2.93 * 0.7, 0.0), ('calcite, 30% pore space', 2.71 * 0.7, 0.0)]
    a0 = ap(t, 's9', 0.05)
    mono(cv, x0, y0 + 10, f'81 x 92 x 21 in = {vol_in3:,} cubic in = {vft:.1f} cubic ft', 30 if L else 26, TXT, a0)
    mono(cv, x0, y0 + 56, '(1 g/cm3 = 62.43 lb/ft3; weight = volume x density)', 20, DIM, a0)
    order = [1, 0, 2, 3]; fr = [0.3, 0.38, 0.55, 0.62]
    scale_max = 10.0; bx0 = x0 + (500 if L else 0); bw = (x1 - bx0 - 150) if L else (x1 - x0 - 200)
    for i, k in enumerate(order):
        nm, d, _ = rows[k]; aa = ap(t, 's9', fr[i]); tons = vft * d * 62.428 / 2000.0
        yy = y0 + 120 + i * (84 if L else 120)
        if aa <= 0: continue
        if L: cv.text((x0, yy + 10), nm, 'sans', 28, TXT, 'la', aa); by = yy
        else: cv.text((x0, yy), nm, 'sans', 28, TXT, 'la', aa); by = yy + 40
        wl = bw * tons / scale_max * ease((t - F('s9', fr[i])) / 1.0)
        col = ROSE if i < 2 else MINT
        cv.rect((bx0, by, bx0 + wl, by + 44), mix(col, BG, aa * 0.8)); cv.text((bx0 + wl + 14, by + 22), f'{tons:.1f} short tons', 'monob', 24, TXT, 'lm', aa)
    ua = ap(t, 's9', 0.45)
    ux = bx0 + bw * 0.9
    ytop = y0 + 100; ybot = y0 + 120 + 4 * (84 if L else 120)
    cv.line([(ux, ytop), (ux, ybot)], mix(VIO, BG, ua), 3); cv.text((ux, ytop - 8), 'form: "nine ton"', 'monob', 22, VIO, 'ms', ua)
    mono(cv, x0, ybot + 20, 'densities: standard mineral values. 30% porosity is our assumption.', 20, DIM, ap(t, 's9', 0.7))
    mono(cv, x0, ybot + 50, 'if "ton" means metric, 9 t = 9.9 short tons: the mismatch grows.', 20, DIM, ap(t, 's9', 0.82))

def sc_tools(cv, t, p):
    night(cv, t, 0.5)
    x0, y0, x1, y1 = CONT
    lift = 0.35 + 0.3 * math.sin(t * 0.4)
    if L: tripod(cv, x0 + 330, y0 + 570, 520, ease(t / 1.0), lift, math.sin(t * 0.6))
    else: tripod(cv, x1 - 200, y0 + 330, 300, ease(t / 1.0), lift, math.sin(t * 0.6))
    tx = x0 + (720 if L else 0); ty = y0 + (0 if L else 360)
    rows = [('DOCUMENTED', MINT, 'tools on display (NRHP 1984): block and tackle ("metal fall"), rollers, jacks, wedges, slings, cables, sledges, chisels; some made from old car parts', 0.15),
            ('DOCUMENTED', MINT, 'old photographs show tall wooden tripods with chains, and a chain hoist', 0.5),
            ('UNKNOWN', ROSE, 'exact rig set-up and procedures: "no detailed records" (Rock Gate Park archive page)', 0.78)]
    yy = ty
    for lab, col, txt, f in rows:
        aa = ap(t, 's10', f)
        if aa > 0:
            tag(cv, tx, yy, lab, col, aa, 20)
            yy = cv.para(tx, yy + 56, txt, 'sans', 30 if L else 28, TXT, (x1 - tx - 20), 1.22, 'l', aa) + 22
    mono(cv, x0, y1 - (10 if L else 0), 'diagram: ILLUSTRATION of a pole tripod, not a drawing of his rig', 18, DIM, ease((t - 2) / 1.0))

def pulley(cv, cx, cy, w, a, col):
    cv.rect((cx - w / 2, cy - 22, cx + w / 2, cy + 22), mix(INK2, BG, a)); cv.outline((cx - w / 2, cy - 22, cx + w / 2, cy + 22), mix(col, BG, a), 2)
    for k in range(3): cv.ring((cx - w / 3 + k * w / 3, cy), 12, mix(col, BG, a), 2)

def sc_tackle(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'ILLUSTRATION: IDEAL, NO FRICTION', CYAN, ease(t / 0.8), 20)
    a = ease(t / 1.0)
    dx, dy = (x0 + 220, y0 + 90) if L else (x0 + 220, y0 + 70)
    u = 0.5 - 0.5 * math.cos(t * 0.5)
    topy = dy; boty = dy + 330 - 150 * u
    w = 280
    pulley(cv, dx, topy, w, a, DIM)
    pulley(cv, dx, boty, w, a, CYAN)
    for k in range(6):
        xx = dx - w / 2 + 14 + k * (w - 28) / 5
        cv.line([(xx, topy + 22), (xx, boty - 22)], mix(TXT, BG, a * 0.7), 2)
    cv.line([(dx + w / 2, topy), (dx + w / 2 + 70, topy), (dx + w / 2 + 70, topy + 380 + 30 * u)], mix(VIO, BG, a), 3)
    mono(cv, dx + w / 2 + 84, topy + 330, 'pull', 22, VIO, a)
    cv.line([(dx, boty + 22), (dx, boty + 70)], mix(TXT, BG, a * 0.7), 2)
    stone(cv, dx - 70, boty + 70, dx + 70, boty + 150, a, CYAN, '10 tons')
    cv.line([(dx, dy - 40), (dx, topy - 22)], mix(DIM, BG, a), 4)
    sx = x0 + (560 if L else 0); sy = y0 + (20 if L else 600)
    rows = [('load: 10 short tons = 20,000 lb', 0.0, TXT), ('6 rope segments:  20,000 / 6 = 3,333 lb pull', 0.18, TXT), ('two sets, 6 x 6 = 36:  20,000 / 36 = 556 lb', 0.4, TXT),
            ('+ 5:1 winch, 36 x 5 = 180:  20,000 / 180 = 111 lb', 0.58, MINT), ('cost: 180 ft of rope hauled per 1 ft of lift', 0.78, ROSE)]
    for i, (txt, f, col) in enumerate(rows):
        aa = ap(t, 's11', f)
        if aa <= 0: continue
        yy = sy + i * (84 if L else 56)
        cv.rect((sx, yy + 4, sx + 5, yy + 44), mix(col, BG, aa)); cv.text((sx + 20, yy), txt, 'sans', 34 if L else 28, col, 'la', aa)
    mono(cv, sx, sy + 5 * (84 if L else 56) + 10, 'possible on paper; real rigs lose force to friction', 20, DIM, ap(t, 's11', 0.9))

def sc_lever(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'ILLUSTRATION', CYAN, ease(t / 0.8))
    a = ease(t / 1.0)
    px, py = (x0 + 220, y0 + 330) if L else (x0 + 140, y0 + 330)
    ang = math.radians(-8 + 14 * (0.5 - 0.5 * math.cos(t * 0.8)))
    unit = 56
    lx, ly = px - unit * math.cos(ang), py + unit * math.sin(ang) * -1
    rx, ry = px + 9 * unit * math.cos(ang), py - 9 * unit * math.sin(ang) * -1
    poly(cv, [(px, py), (px - 30, py + 70), (px + 30, py + 70)], mix(DIM, BG, a))
    cv.line([(lx, ly), (rx, ry)], mix(TXT, BG, a), 10)
    stone(cv, lx - 60, ly - 70, lx + 10, ly - 4, a, CYAN)
    cv.line([(rx, ry - 70), (rx, ry - 8)], mix(VIO, BG, a), 4); poly(cv, [(rx - 10, ry - 20), (rx + 10, ry - 20), (rx, ry - 4)], mix(VIO, BG, a))
    cv.text((rx, ry - 84), 'push', 'mono', 20, VIO, 'ms', a); cv.text((px, py + 100), '1 : 9', 'monob', 26, TXT, 'ma', a)
    sx = x0 + (780 if L else 0); sy = y0 + (30 if L else 520)
    ap1 = ap(t, 's12', 0.25); ap2 = ap(t, 's12', 0.6)
    cv.text((sx, sy), 'force x arm = force x arm', 'monob', 32, TXT, 'la', ap1)
    cv.text((sx, sy + 60), '100 lb x 9 ft  =  900 lb x 1 ft', 'monob', 32, MINT, 'la', ap1)
    # cribbing: raise an inch, add a timber, repeat
    cy0 = sy + 170 if L else sy + 140
    for k in range(4):
        aa = ap(t, 's12', 0.55 + k * 0.1, 0.6)
        if aa <= 0: continue
        bx = sx + k * 170
        for j in range(k + 1): cv.rect((bx, cy0 + 120 - (j + 1) * 16, bx + 120, cy0 + 120 - j * 16 - 2), mix(DIM, BG, aa))
        stone(cv, bx + 10, cy0 + 120 - (k + 1) * 16 - 70, bx + 110, cy0 + 120 - (k + 1) * 16, aa, CYAN)
    cv.text((sx, cy0 + 150), 'raise an inch, slide a timber under, repeat', 'mono', 24, DIM, 'la', ap2)

def sc_affidavit(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED: 250+ AFFIDAVITS, 1955', MINT, ease(t / 0.8), 20)
    cols = 25 if L else 20; cell = 38 if L else 34
    for i in range(250):
        cx = x0 + 20 + (i % cols) * cell; cy = y0 + 40 + (i // cols) * cell
        lit = ease((t - 0.8 - i * 0.012) / 0.4)
        cv.circ((cx, cy), 7, mix(MINT, BG, 0.15 + 0.85 * lit))
    gy = y0 + 40 + (250 // cols + 1) * cell + 10
    qa = ap(t, 's13', 0.2)
    q = '"...without the aid of any individual or individuals... with simple hand tools..."'
    yy = cv.para(x0, gy, q, 'light', 36 if L else 34, TXT, (x1 - x0) * (0.55 if L else 1.0), 1.25, 'l', qa)
    mono(cv, x0, yy + 4, 'what the affiants signed, as quoted in the NRHP form (collected by the then-owner)', 18, DIM, qa)
    ub = ap(t, 's13', 0.62)
    tag(cv, x0, yy + 50, 'UNKNOWN', ROSE, ub, 22)
    cv.text((x0 + 170, yy + 54), 'who saw the largest blocks go up: the form quotes no one', 'sans', 28 if L else 26, TXT, 'la', ub)

def sc_words(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    a = ease(t / 1.0)
    tag(cv, x0, y0 - 40, 'CLAIMED', VIO, a)
    qa = ap(t, 's14', 0.1)
    cv.rect((x0, y0 + 10, x0 + 5, y0 + (330 if L else 420)), mix(VIO, BG, qa))
    yy = cv.para(x0 + 30, y0 + 10, '"the methods used by the pyramid builders, the practical knowledge of the laws of leverage and weight"', 'light', 54 if L else 50, TXT, (x1 - x0 - 60) * (0.8 if L else 1), 1.2, 'l', qa)
    mono(cv, x0 + 30, yy + 10, 'Ed\'s reply to how he did it, as paraphrased in the NRHP form, 1984', 20, DIM, qa)
    py0 = y0 + (400 if L else 520)
    mono(cv, x0, py0, 'PAMPHLETS (he sold these)', 22, CYAN, ap(t, 's14', 0.55))
    ps = [('1936', 'A Book in Every Home', 0.62), ('Aug 1945', 'Magnetic Current', 0.76), ('Oct 1945', 'Mineral, Vegetable and Animal Life', 0.88)]
    for i, (yr, nm, f) in enumerate(ps):
        aa = ap(t, 's14', f); yy2 = py0 + 46 + i * 56
        mono(cv, x0, yy2, yr, 28, MINT, aa); cv.text((x0 + 200, yy2 - 2), nm, 'sans', 34, TXT, 'la', aa)
    mono(cv, x0, py0 + 46 + 3 * 56 + 6, 'we found none that describes how he lifted the blocks', 22, ROSE, ap(t, 's14', 0.95))

def sc_theories(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    items = [('sound', 'sound levitates the stone', 0.12), ('magnetism', '"magnetic current" cancels weight', 0.3), ('help from beyond Earth', 'already circulating by 1984', 0.48)]
    for i, (a1, a2, f) in enumerate(items):
        aa = ap(t, 's15', f)
        if aa <= 0: continue
        if L:
            cw = (x1 - x0 - 80) / 3; cx = x0 + i * (cw + 40); cy = y0 + 10; ch = 330
        else:
            cw = x1 - x0; cx = x0; cy = y0 + i * 235; ch = 215
        card(cv, cx, cy, cw, ch, ROSE, aa)
        big(cv, cx + 28, cy + 24, a1, 48 if L else 46, TXT, aa)
        cv.para(cx + 28, cy + 96, a2, 'sans', 28, DIM, cw - 56, 1.2, 'l', aa)
        if L:
            tag(cv, cx + 28, cy + ch - 120, 'NOT ESTABLISHED', ROSE, aa, 20); mono(cv, cx + 28, cy + ch - 62, 'evidence found: none', 22, TXT, aa)
        else:
            tag(cv, cx + 28, cy + ch - 70, 'NOT ESTABLISHED', ROSE, aa, 20); mono(cv, cx + 330, cy + ch - 62, 'evidence found: none', 22, TXT, aa)
    ub = ap(t, 's15', 0.72); yb = y0 + (390 if L else 740)
    big(cv, x0, yb, 'absence of evidence is not proof of absence.', 44 if L else 38, TXT, ub)
    mono(cv, x0, yb + 70, 'floating-stone stories: secondhand. not established is not the same as impossible.', 22, DIM, ap(t, 's15', 0.85))

LEDGER = [('DOCUMENTED', MINT, 'dates, the form\'s weights, the move, the tools, the 1986 repair', 0.22),
          ('CLAIMED', VIO, 'worked alone  /  pyramid builders\' methods  /  1,100 tons', 0.5),
          ('NOT SETTLED', ROSE, 'the gate\'s true weight', 0.7),
          ('UNKNOWN', ROSE, 'how the largest blocks were raised and set, alone', 0.85)]
def sc_ledger(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    big(cv, x0, y0 + 10, 'the ledger', 56 if PORT else 64, TXT, ease(t / 1.0))
    step = 150 if PORT else 112
    for i, (st, col, txt, f) in enumerate(LEDGER):
        a = ap(t, 's16', f)
        if a <= 0: continue
        yy = y0 + 110 + i * step
        hline(cv, x0, x1, yy, INK2, a, 1)
        tag(cv, x0, yy + 16, st, col, a, 22)
        if L: big(cv, x0 + 360, yy + 10, txt, 40, TXT, a)
        else: cv.para(x0, yy + 76, txt, 'light', 38, TXT, x1 - x0, 1.15, 'l', a)

def sc_close(cv, t, p):
    night(cv, t, 0.8)
    x0, y0, x1, y1 = CONT
    a = ease(t / 1.0)
    sz = 120 if L else 100
    big(cv, x0, y0 + 20, 'not established.', sz, TXT, ap(t, 's17', 0.45))
    big(cv, x0, y0 + 20 + sz * 1.2, 'not ruled out.', sz, TXT, ap(t, 's17', 0.62))
    tag(cv, x0, y0 + 20 + sz * 2.6, 'NOT ESTABLISHED', ROSE, ap(t, 's17', 0.5), 24); tag(cv, x0 + 330, y0 + 20 + sz * 2.6, 'NOT RULED OUT', MINT, ap(t, 's17', 0.68), 24)
    big(cv, x0, y0 + 20 + sz * 3.4, 'someone watching this might be the one who works it out.', 36 if L else 34, CYAN, ap(t, 's17', 0.82, 1.2))
    if L: tripod(cv, 1560, 830, 380, 0.5 * a, 0.2 + 0.1 * math.sin(t * 0.5), math.sin(t * 0.6))

SOURCES = [
    'NPS: National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed\'s Place)" / Coral Castle. Florida Division of Archives, 2 Apr 1984; listed 10 May 1984; renamed Coral Castle 2011 (npgallery.nps.gov, asset 1ed2ccd0-b692-42dc-b28d-1227c1a23407)',
    'Wikipedia, "Coral Castle" and "Edward Leedskalnin" (read 2026-10-13): 1986 gate repair, 2005 failure, 1,100 short tons (figure unattributed)',
    'coralcastle.com, "The Secrets of Coral Castle" (1,100 tons); rockgatepark.com/the-tools (tool photographs; "no detailed records")',
    'Photographs of the hoists exist: Florida Memory item 328424 (see it there). No photographs are used in this video; every picture is drawn.',
    'Further reading: P. A. Hancock, "The making of a modern myth: Edward Leedskalnin and the Coral Castle", Skeptic 18(1), 2013',
    'Our arithmetic (gate volume, density, block and tackle, lever): standard formulas; calcite 2.71 and aragonite 2.93 g/cm3; 30% porosity is assumed']
def sc_end(cv, t, p):
    night(cv, t, 0.7)
    a = ease(t / 1.0)
    if L: tripod(cv, 1620, 700, 300, 0.35 * a, 0.2, 0.0)
    y = 160 if PORT else 70
    mono(cv, HEAD[0], y, 'HEARTBEAT TV  /  CH 10', 26, CYAN, a)
    big(cv, HEAD[0], y + 40, 'still unknown', 110 if PORT else 110, TXT, a)
    mono(cv, HEAD[0], y + (170 if PORT else 170), 'heartbeatobservatory.com', 34, CYAN, a)
    yy = y + (240 if PORT else 240)
    mono(cv, HEAD[0], yy, 'SOURCES', 22, DIM, ease((t - 0.6) / 1)); yy += 40
    for i, s in enumerate(SOURCES):
        yy = cv.para(HEAD[0], yy, s, 'mono', 21 if PORT else 22, TXT, (W - 2 * HEAD[0]) * (1 if PORT else 0.95), 1.25, 'l', ease((t - 0.8 - i * 0.15) / 0.8)) + 10

# (segment id, headline, source line, draw fn)
SCENES = [
    ('s1', None, 'Edward Leedskalnin, 1887-1951. 1,100 tons: castle figure, source untraced', sc_title),
    ('s2', 'a man from latvia', 'NRHP nomination form, Florida Division of Archives, 1984', sc_man),
    ('s3', 'a love story, and its gaps', 'NRHP form 1984 (name spellings, footnote 2); Wikipedia "Edward Leedskalnin"', sc_agnes),
    ('s4', 'ed\'s place, 1923', 'NRHP form 1984; Dade County Deed Book 1546, p. 8', sc_site),
    ('s5', 'the move to homestead', 'NRHP form 1984 (sec. 7, 8; obelisk inscription)', sc_move),
    ('s6', 'what the form weighs', 'NRHP form 1984: weights in pounds, converted here', sc_weights),
    ('s7', 'the 1,100-ton total', 'coralcastle.com; Wikipedia "Coral Castle"; NRHP form 1984', sc_total),
    ('s8', 'the gate', 'NRHP form 1984; Wikipedia "Coral Castle" (1986 repair, 2005)', sc_gate),
    ('s9', 'a check anyone can do', 'Volume x density. Our arithmetic, assumptions on screen', sc_check),
    ('s10', 'the tools', 'NRHP form 1984 (tool list); rockgatepark.com/the-tools', sc_tools),
    ('s11', 'block and tackle', 'Ideal mechanical advantage = rope segments. Worked example, not his rig', sc_tackle),
    ('s12', 'the lever', 'Law of the lever. Worked example, not his method', sc_lever),
    ('s13', 'what no one has documented', 'NRHP form 1984 quoting the 1955 affidavits', sc_affidavit),
    ('s14', 'what he said', 'NRHP form 1984 (paraphrase of his reply; pamphlet list)', sc_words),
    ('s15', 'popular theories', 'NRHP form 1984 (extraterrestrial, gravity theories); thisunexplaineduniverse.com', sc_theories),
    ('s16', None, 'Status as of October 2026', sc_ledger),
    ('s17', None, None, sc_close),
    ('s18', None, None, sc_end),
]

def _subs(text):
    out = []
    for s in re.split(r'(?<=[.?!])\s+', text.strip()):
        parts = [s]
        while True:
            nxt = []; changed = False
            for q in parts:
                if len(q) > 96:
                    cs = [m.end() for m in re.finditer(r'[,:] ', q)]
                    if cs:
                        k = min(cs, key=lambda c: abs(c - len(q) / 2)); nxt += [q[:k].strip(), q[k:].strip()]; changed = True; continue
                nxt.append(q)
            parts = nxt
            if not changed: break
        out += parts
    return out
SUBS = {s['id']: _subs(s['text']) for s in TL['segs']}

# ------------------------------------------------------------------ framework
bounds = []
for i, (sid, *_r) in enumerate(SCENES):
    s0 = 0.0 if i == 0 else SEG[sid]['start'] - 0.5
    s1 = TOTAL if i == len(SCENES) - 1 else SEG[SCENES[i + 1][0]]['start'] - 0.5
    bounds.append((s0, s1))
BOUND = {sid: b for (sid, *_r), b in zip(SCENES, bounds)}

def subtitle_at(sid, tt):
    seg = SEG[sid]; subs = SUBS[sid]; rel = tt - seg['start']
    if not subs or rel < -0.1 or rel > seg['dur'] + 0.8: return None
    tot = sum(len(s) for s in subs); acc = 0
    for s in subs:
        acc += len(s); b = acc / tot * seg['dur']
        if rel <= b + (0.8 if s is subs[-1] else 0): return s
    return subs[-1]

def frame(tt):
    cv = Cv()
    for i, (sid, head, src, fn) in enumerate(SCENES):
        s0, s1 = bounds[i]
        if s0 <= tt < s1 or (i == len(SCENES) - 1 and tt >= s0): break
    t = tt - s0; p = clamp01(t / max(0.1, s1 - s0 - 0.6))
    fn(cv, t, p)
    cv.rect((0, 0, 6, H), INK2)
    cv.vtext((14, H - (300 if PORT else 260)), 'STILL UNKNOWN', 'mono', 20, DIM, 0.8)
    mono(cv, 16, 30, f'{i + 1:02d}/{len(SCENES):02d}', 20, DIM, 0.8)
    if head:
        a = ease(t / 0.6)
        f = font('light', SZ['head']); ls = wrap(head, f, HEAD[2] - HEAD[0])
        for k, l in enumerate(ls): cv.text((HEAD[0], HEAD[1] + k * SZ['head'] * 1.1), l, 'light', SZ['head'], TXT, 'la', a)
        cv.rect((HEAD[0], HEAD[1] - 14, HEAD[0] + 44 * a, HEAD[1] - 11), mix(CYAN, BG, a))
    sub = subtitle_at(sid, tt)
    if sub:
        f = font('sans', SZ['cap']); ls = wrap(sub, f, CAP[2] - CAP[0] - 30); n = len(ls)
        lh = SZ['cap'] * 1.28; y0 = CAP[3] - n * lh - 10 if not PORT else CAP[1] + 10
        cv.rect((CAP[0] - 30, y0 - 10, CAP[0] - 30 + 5, y0 + n * lh + 4), CYAN)
        for k, l in enumerate(ls):
            tw = f.getlength(l) / SS
            cv.rect((CAP[0] - 12, y0 + k * lh + 4, CAP[0] + tw + 14, y0 + (k + 1) * lh + 2), mix(BG, INK, 0.72))
            cv.text((CAP[0], y0 + k * lh), l, 'sans', SZ['cap'], TXT, 'la')
    if src:
        a = ease(t / 1.2)
        mono(cv, SRC[0] if PORT else SRC[2], SRC[1], 'SOURCE', 18, CYAN, a, 'la' if PORT else 'ra')
        f = font('mono', SZ['src']); ls = wrap(src, f, SRC[2] - SRC[0])[:3]
        for k, l in enumerate(ls): cv.text((SRC[0] if PORT else SRC[2], SRC[1] + 26 + k * SZ['src'] * 1.25), l, 'mono', SZ['src'], DIM, 'la' if PORT else 'ra', a)
    im = cv.im.reduce(SS)
    fa = min(1.0, t / 0.35, (s1 - tt) / 0.35 if i < len(SCENES) - 1 else (TOTAL - tt) / 1.2)
    if fa < 1.0: im = Image.blend(Image.new('RGB', im.size, BG), im, max(0.0, fa))
    return im

def work(n): return frame(n / FPS).tobytes()

def main():
    if '--still' in sys.argv:
        i = sys.argv.index('--still'); frame(float(sys.argv[i + 1])).save(sys.argv[i + 2]); return
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else f'video_{ORI}.mp4'
    a, b = 0, int(TOTAL * FPS)
    if '--secs' in sys.argv:
        i = sys.argv.index('--secs'); a, b = int(float(sys.argv[i + 1]) * FPS), int(float(sys.argv[i + 2]) * FPS)
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    pool = Pool(8)
    try:
        for k, buf in enumerate(pool.imap(work, range(a, b), chunksize=4)):
            ff.stdin.write(buf)
            if k % 600 == 0: print(k, '/', b - a, flush=True)
        pool.close(); pool.join()
    except Exception as e:
        print('pool error:', repr(e), flush=True)
    finally:
        try: ff.stdin.close()
        except Exception: pass
        ff.wait(); print('ffmpeg exit', ff.returncode, flush=True)

if __name__ == '__main__': main()


exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command 'rg -n "def sc_(move|weights|total|gate|check)|SCENES =|SOURCES =|1936|1937|1939|Biggers|Polaris|gate|affidavit|pamphlet|National Register|1,100|1100|block and tackle|rope segments" ep_body.py script.json SOURCES.md' in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 554ms:
script.json:8:  "text": "Start with the man. Edward Leedskalnin was born in Latvia in 1887. A 1984 National Register nomination form says that at about twenty-six he was engaged to a girl ten years younger, Agnes, who called off the wedding shortly before it. He later called her his Sweet Sixteen. After years of work across North America and illness, he reached Florida City in the early 1920s."
script.json:20:  "text": "In the mid nineteen thirties he bought ten acres in Homestead, about ten miles north, and decided to take his stone with him. Dates vary. The form says 1937. The obelisk is inscribed: moved in 1939. A local man, Bob Biggers, lent his truck. The form says Ed worked alone, at night, loading and unloading it."
script.json:24:  "text": "Now the weights, which the form lists in pounds. The Polaris sighting slab: twenty short tons. Each quarter moon: eighteen. The full moon fountain: twenty three. The obelisk: twenty eight and a half. The heaviest it names: a thirty ton sculpture on the north wall."
script.json:32:  "text": "The best known piece is the gate. A single slab, eighty one inches wide, ninety two tall, twenty one thick, turning on a central shaft that the form says uses an automobile axle. One finger moves it. The form calls it nine tons. In 1986 it stopped turning. Six men and a fifty ton crane lifted it out, a rusted truck bearing was replaced, and it was reset in July."
script.json:40:  "text": "What tools did he have? The form says the castle displays his tools, made partly from old car parts: block and tackle, rollers, jacks, wedges, slings, cables, sledges and chisels. Old photographs show tall wooden tripods with chains hanging from the top, and a chain hoist. The castle's archive says no detailed record shows how the rigs were used."
script.json:44:  "text": "What can that gear do? Take a ten ton block, twenty thousand pounds. A block and tackle with six rope segments cuts the pull to a sixth: about thirty three hundred pounds. Chain two sets together and it is six times six: about five hundred fifty. Add a five to one winch and it is near one hundred ten pounds, which one person can pull. The price is distance: for each foot of lift, one hundred eighty feet of rope. Small force, long time. This is ideal physics, no friction: what is possible, not what he did."
script.json:52:  "text": "So what is not documented? In 1955, the castle's new owner collected more than two hundred fifty signed affidavits from local residents, saying Ed did the work alone with simple hand tools. That is a lot of people. But the form quotes no one who watched the largest blocks go up. So the belief is documented. The method of the biggest lifts is not."
script.json:56:  "text": "Now his own words. Asked how, the form says, Ed always gave the same answer: that he understood the methods of the pyramid builders, and the laws of leverage and weight. That is a claim. We found no document where he describes his lifting method. He did publish pamphlets, in 1936 and 1945, including Magnetic Current, about his own ideas on magnets and electricity."
script.json:60:  "text": "Then the popular theories. That he used sound to levitate the stone. That magnetism, as in his pamphlets, cancelled weight. That he had help from beyond Earth, an idea already circulating before the 1984 form. All three are not established. We found no measurement, recording, or physical trace for any of them, and the floating stone stories are secondhand. Absence of evidence is not proof of absence. So: not established, not impossible."
script.json:64:  "text": "So here is the ledger. Documented: the dates, the form's weights, the move, the tools, the 1986 gate repair. Claimed: that he worked alone, that he knew the pyramid builders' methods, and the eleven hundred ton total. Not settled: the gate's true weight. Unknown: exactly how he raised and set the largest blocks alone."
ep_body.py:59:    lines = ('coral castle:', 'one man,', '1,100 tons') if PORT else ('coral castle:', 'one man, 1,100 tons')
ep_body.py:62:    mono(cv, HEAD[0], yy, 'the 1,100 is the castle\'s own figure: we check it', 24, DIM, ease((t - 1.5) / 1.0))
ep_body.py:147:def sc_move(cv, t, p):
ep_body.py:168:    rows = [('1936-40', 'accounts differ; about three years of moving', 0.25), ('1937', 'the 1984 NRHP form, section 7', 0.4), ('1939', 'inscribed on the obelisk: "Moved in 1939"', 0.55),
ep_body.py:169:            ('truck', 'Bob Biggers\' truck, lent to Ed (NRHP form)', 0.72), ('crew', 'worked alone, at night, loading and unloading (form)', 0.88)]
ep_body.py:177:def sc_weights(cv, t, p):
ep_body.py:181:    items = [('Polaris sighting slab', 20, 0.12), ('each quarter moon', 18, 0.28), ('full moon fountain', 23, 0.4), ('obelisk', 28.5, 0.55), ('north-wall sculpture', 30, 0.78)]
ep_body.py:197:def sc_total(cv, t, p):
ep_body.py:201:    big(cv, x0, y0 + 10, '1,100', 220 if L else 200, TXT, a)
ep_body.py:205:    rows = [('coralcastle.com', 'states "1,100 tons"; no estimator named', 0.15), ('Wikipedia', '1,100 short tons; figure not attributed', 0.3), ('NRHP form, 1984', 'lists pieces "up to 30 tons"; no total', 0.5), ('first estimator', 'not found', 0.7)]
ep_body.py:213:def sc_gate(cv, t, p):
ep_body.py:248:def sc_check(cv, t, p):
ep_body.py:282:    rows = [('DOCUMENTED', MINT, 'tools on display (NRHP 1984): block and tackle ("metal fall"), rollers, jacks, wedges, slings, cables, sledges, chisels; some made from old car parts', 0.15),
ep_body.py:317:    rows = [('load: 10 short tons = 20,000 lb', 0.0, TXT), ('6 rope segments:  20,000 / 6 = 3,333 lb pull', 0.18, TXT), ('two sets, 6 x 6 = 36:  20,000 / 36 = 556 lb', 0.4, TXT),
ep_body.py:355:def sc_affidavit(cv, t, p):
ep_body.py:384:    ps = [('1936', 'A Book in Every Home', 0.62), ('Aug 1945', 'Magnetic Current', 0.76), ('Oct 1945', 'Mineral, Vegetable and Animal Life', 0.88)]
ep_body.py:413:          ('CLAIMED', VIO, 'worked alone  /  pyramid builders\' methods  /  1,100 tons', 0.5),
ep_body.py:414:          ('NOT SETTLED', ROSE, 'the gate\'s true weight', 0.7),
ep_body.py:441:SOURCES = [
ep_body.py:442:    'NPS: National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed\'s Place)" / Coral Castle. Florida Division of Archives, 2 Apr 1984; listed 10 May 1984; renamed Coral Castle 2011 (npgallery.nps.gov, asset 1ed2ccd0-b692-42dc-b28d-1227c1a23407)',
ep_body.py:443:    'Wikipedia, "Coral Castle" and "Edward Leedskalnin" (read 2026-10-13): 1986 gate repair, 2005 failure, 1,100 short tons (figure unattributed)',
ep_body.py:444:    'coralcastle.com, "The Secrets of Coral Castle" (1,100 tons); rockgatepark.com/the-tools (tool photographs; "no detailed records")',
ep_body.py:447:    'Our arithmetic (gate volume, density, block and tackle, lever): standard formulas; calcite 2.71 and aragonite 2.93 g/cm3; 30% porosity is assumed']
ep_body.py:462:SCENES = [
ep_body.py:463:    ('s1', None, 'Edward Leedskalnin, 1887-1951. 1,100 tons: castle figure, source untraced', sc_title),
ep_body.py:469:    ('s7', 'the 1,100-ton total', 'coralcastle.com; Wikipedia "Coral Castle"; NRHP form 1984', sc_total),
ep_body.py:470:    ('s8', 'the gate', 'NRHP form 1984; Wikipedia "Coral Castle" (1986 repair, 2005)', sc_gate),
ep_body.py:472:    ('s10', 'the tools', 'NRHP form 1984 (tool list); rockgatepark.com/the-tools', sc_tools),
ep_body.py:473:    ('s11', 'block and tackle', 'Ideal mechanical advantage = rope segments. Worked example, not his rig', sc_tackle),
ep_body.py:475:    ('s13', 'what no one has documented', 'NRHP form 1984 quoting the 1955 affidavits', sc_affidavit),
ep_body.py:476:    ('s14', 'what he said', 'NRHP form 1984 (paraphrase of his reply; pamphlet list)', sc_words),
SOURCES.md:1:# Still Unknown 10.2 "Coral Castle: one man, 1,100 tons" - sources and flags (Claude Sonnet 5.5, 2026-10-13)
SOURCES.md:6:NPS Form 10-900, National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed's Place)" / common name Coral Castle.
SOURCES.md:12:- Move: "1937" (section 7, "moved date 1937"); obelisk inscribed "Made in 1928. Moved in 1939. Born 1887. Latvia, E.L."; newspaper cited in the bibliography "Ed Is Doing A Colossal Job of Moving ..." (Aug 1939). Wikipedia says he moved ~1936 and spent ~3 years. Screen says dates vary.
SOURCES.md:13:- Ten-acre tract on South Federal Highway. "He sought the aid of ... Bob Biggers ... All Edward Leedskalnin wanted from Mr. Biggers, however, was the use of his truck ... completed by Leedskalnin without any assistance ... worked alone and at night loading and unloading Biggers' truck."
SOURCES.md:14:- Weights (lb, converted to short tons by us): Polaris slab 40,000 lb (20 t), 25 ft tall; each quarter moon 36,000 lb (18 t); full-moon fountain 46,000 lb (23 t); Mars and Saturn 36,000 lb; obelisk 57,000 lb (28.5 t); "thirty ton sculpture" crowning the north wall = heaviest oolitic block at Rock Gate; wall blocks 8 ft x 4 ft x 3 ft, "several tons". "Sculptures weighing up to 30 tons each".
SOURCES.md:15:- Gate: "nine ton gate", 81 in wide, 92 in tall, 21 in thick; single pivot; central vertical shaft with an automobile axle connecting slab to ground and lintel; fits within 1/4 in; pushed open with one finger.
SOURCES.md:16:- Tools: "primitive tools are on display ... metal fall (block and tackle), rollers, jacks, wedges, slings, cables, sledges, chisels"; quarrying tools "fashioned from old car parts".
SOURCES.md:19:- Pamphlets (form): A Book in Every Home (1936); Magnetic Current (Franklin Press, Aug 1945); Mineral, Vegetable and Animal Life (Franklin Press, Oct 1945).
SOURCES.md:20:- 1955 affidavits: Julius Levin (owner from 1953) collected "over 250 affidavits"; quoted text includes "without the aid of any individual or individuals; with simple hand tools".
SOURCES.md:24:- Wikipedia "Coral Castle" (fetched 2026-10-13): 1,100 short tons (unattributed); gate stopped 1986, 6 men + 50-short-ton crane, rusted truck bearing, reinstalled 23 July 1986, failed again 2005, no longer as smooth; he said he "understood the laws of weight and leverage".
SOURCES.md:25:- Wikipedia "Edward Leedskalnin" (fetched): born 12 Jan 1887; Latvian historian gives a different name/age for the fiancee; 1,100 short tons cited to Ellison and Perry, "Liars and Legends" (2005) with no original estimator named; died 7 Dec 1951.
SOURCES.md:26:- coralcastle.com/home/the-secrets-of-coral-castle: "an astonishing 1,100 tons of limestone"; says experts doubt his explanation.
SOURCES.md:27:- rockgatepark.com/the-tools: photographs of tripods/lifting frame; "no detailed records" of exact configuration, materials or procedures; no weights or dates.
SOURCES.md:34:- Block and tackle: ideal MA = number of supporting rope segments. 20,000 lb / 6 = 3,333; / 36 = 556; / 180 = 111 lb; 180 ft of rope per 1 ft lift. Friction ignored (labelled). Lever 9:1: 100 lb x 9 ft = 900 lb x 1 ft.
SOURCES.md:37:- Origin of the 1,100-ton figure NOT FOUND. Treated as a CLAIM with untraced source. (Search hints at Carroll Lake, Civil Engineering Magazine 1958, in the form's bibliography; not checked.)
SOURCES.md:38:- Photographs: Florida Memory item 328424 ("Ed Leedskalnin with hoisting equipment", reported c. 1936 in a search snippet) returned 403 to the fetch; date unverified. Live Science and Mental Floss were only seen as search snippets (they report photographs of pole tripods + block and tackle). The brief's "one grainy photo" is NOT what we found: several photographs exist; none shown here.

codex
The local inventory shows the central risk clearly: several statements accurately repeat the 1984 nomination, but â€œdocumentedâ€ sometimes overstates what that later form itself proves. Iâ€™m separating â€œthe form says Xâ€ from â€œX is independently established,â€ especially for the move, solitary work, affidavits, and gate repair.
web search: 
web search: site:npgallery.nps.gov Coral Castle Rock Gate nomination 1984 PDF 84000840 ...
web search: 
web search: "July 23, 1986" "Coral Castle" gate ...
web search: 
web search: 
web search: 
web search: Edward Leedskalnin "moved in 1939" Bob Biggers newspaper ...
web search: 
web search: site:usgs.gov Miami Limestone porosity bulk density oolite ...
web search: 
web search: 'Julius Levin'
exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command 'Get-Content ep_body.py | Select-Object -Skip 120 -First 370' in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 1614ms:
def sc_site(cv, t, p):
    night(cv, t, 0.5)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED: NRHP FORM, 1984', MINT, ease(t / 0.8))
    # schematic plan (not to scale)
    if L: px, py, pw, ph = x0 + 40, y0 + 60, 640, 420
    else: px, py, pw, ph = x0 + 20, y0 + 20, 700, 420
    a = ease(t / 1.2)
    cv.outline((px, py, px + pw, py + ph), mix(CYAN, BG, a), 3)
    mono(cv, px, py - 28, 'ED\'S PLACE, FLORIDA CITY: schematic, not to scale', 18, DIM, a)
    tw = ap(t, 's4', 0.45)
    cv.rect((px + 40, py + 40, px + 200, py + 190), mix(INK2, BG, tw)); cv.outline((px + 40, py + 40, px + 200, py + 190), mix(VIO, BG, tw), 2)
    cv.text((px + 120, py + 115), 'two-story tower', 'mono', 18, TXT, 'mm', tw)
    fu = ap(t, 's4', 0.75)
    for (fx, fy, fw, fh, lab) in ((300, 60, 90, 60, 'table'), (420, 60, 70, 70, 'chair'), (300, 160, 120, 50, 'bench'), (470, 190, 90, 70, 'chair'), (330, 270, 120, 90, 'sundial?')):
        cv.rect((px + fx, py + fy, px + fx + fw, py + fy + fh), mix(INK2, BG, fu)); cv.outline((px + fx, py + fy, px + fx + fw, py + fy + fh), mix(DIM, BG, fu), 1)
    cv.text((px + 330, py + 380), 'furniture, astronomy pieces', 'mono', 18, DIM, 'lm', fu)
    pit = ap(t, 's4', 0.85)
    for k in range(3): cv.ring((px + pw + 80 + k * 30, py + 100 + k * 90), 36, mix(DIM2, BG, pit), 2)
    cv.text((px + pw + 40, py + ph + 30), 'quarry pits outside the wall', 'mono', 18, DIM, 'lm', pit)
    # facts
    fx0 = x0 + 760 if L else x0 + 20; fy0 = y0 + 40 if L else y0 + 530
    ga = ap(t, 's4', 0.1); big(cv, fx0, fy0, '1923', 110 if L else 100, TXT, ga)
    stack(cv, fx0, fy0 + (130 if L else 120), ['one acre, $12 (Dade County Deed Book 1546, p. 8)', 'ground: oolitic limestone, "coral rock"'],
          [ap(t, 's4', 0.15), ap(t, 's4', 0.3)], 28, 12, 900 if L else 900, DIM, 'mono')

def sc_move(cv, t, p):
    night(cv, t, 0.7)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED', MINT, ease(t / 0.8)); tag(cv, x0 + 230, y0 - 40, 'DATES VARY', ROSE, ap(t, 's5', 0.3))
    lx0, lx1 = x0 + 60, x1 - 60
    ly = y0 + (200 if L else 160)
    a = ease(t / 1.0)
    cv.line([(lx0, ly), (lx1, ly)], mix(DIM2, BG, a), 3)
    for xx, nm in ((lx0, 'Florida City'), (lx1, 'Homestead')):
        cv.circ((xx, ly), 12, mix(CYAN, BG, a)); cv.text((xx, ly + 40), nm, 'mono', 26, TXT, 'ma', a)
    cv.text(((lx0 + lx1) / 2, ly - 50), 'about 10 miles', 'mono', 24, DIM, 'mm', a)
    # truck shuttling with a block, loaded one way
    ph = (t * 0.22) % 2.0; u = ph if ph < 1 else 2 - ph
    tx = lx0 + (lx1 - lx0) * ease(u)
    loaded = ph < 1
    cv.rect((tx - 50, ly - 56, tx + 10, ly - 12), mix(VIO, BG, a)); cv.rect((tx + 10, ly - 40, tx + 80, ly - 12), mix(INK2, BG, a))
    cv.outline((tx - 50, ly - 56, tx + 80, ly - 12), mix(DIM, BG, a), 2)
    cv.circ((tx - 30, ly - 8), 10, mix(TXT, BG, a)); cv.circ((tx + 50, ly - 8), 10, mix(TXT, BG, a))
    if loaded: stone(cv, tx + 14, ly - 82, tx + 76, ly - 40, a, CYAN)
    # date table
    ty = ly + (130 if L else 130)
    rows = [('1936-40', 'accounts differ; about three years of moving', 0.25), ('1937', 'the 1984 NRHP form, section 7', 0.4), ('1939', 'inscribed on the obelisk: "Moved in 1939"', 0.55),
            ('truck', 'Bob Biggers\' truck, lent to Ed (NRHP form)', 0.72), ('crew', 'worked alone, at night, loading and unloading (form)', 0.88)]
    for i, (k, v, f) in enumerate(rows):
        aa = ap(t, 's5', f); yy = ty + i * (62 if L else 100)
        if aa <= 0: continue
        mono(cv, x0 + 20, yy, k, 28, CYAN, aa)
        if L: cv.text((x0 + 250, yy), v, 'sans', 32, TXT, 'la', aa)
        else: cv.para(x0 + 20, yy + 36, v, 'sans', 30, TXT, 900, 1.2, 'l', aa)

def sc_weights(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED: WEIGHTS AS LISTED, NRHP 1984', MINT, ease(t / 0.8), 20)
    items = [('Polaris sighting slab', 20, 0.12), ('each quarter moon', 18, 0.28), ('full moon fountain', 23, 0.4), ('obelisk', 28.5, 0.55), ('north-wall sculpture', 30, 0.78)]
    lw = 430 if L else 0
    bx0 = x0 + (lw + 30 if L else 0); bmax = (x1 - bx0 - 240) if L else (x1 - x0 - 380)
    rh = 96 if L else 140
    for i, (nm, v, f) in enumerate(items):
        aa = ap(t, 's6', f); yy = y0 + 30 + i * rh
        if aa <= 0: continue
        if L: cv.text((x0, yy + 28), nm, 'sans', 30, TXT, 'la', aa); by = yy + 14
        else: cv.text((x0, yy), nm, 'sans', 32, TXT, 'la', aa); by = yy + 50
        wlen = bmax * v / 30 * ease((t - F('s6', f)) / 1.2)
        cv.rect((bx0, by, bx0 + wlen, by + (46 if L else 50)), mix(CYAN, BG, aa * 0.85))
        cv.text((bx0 + wlen + 16, by + (23 if L else 25)), f'{v:g} short tons', 'monob', 26, TXT, 'lm', aa)
    yy = y0 + 30 + len(items) * rh + 10
    mono(cv, x0, yy, '1 short ton = 2,000 lb.  Values converted from the form\'s pounds.', 20, DIM, ap(t, 's6', 0.5))
    mono(cv, x0, yy + 30, 'Wall blocks: 8 x 4 x 3 ft (96 cubic feet), "several tons" each.', 20, DIM, ap(t, 's6', 0.85))

def sc_total(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    a = ease(t / 1.2)
    big(cv, x0, y0 + 10, '1,100', 220 if L else 200, TXT, a)
    mono(cv, x0 + (640 if L else 20), y0 + (150 if L else 270), 'short tons: the castle\'s own total', 30, VIO, a)
    tag(cv, x0 + (640 if L else 20), y0 + (210 if L else 330), 'CLAIMED', VIO, ap(t, 's7', 0.3)); tag(cv, x0 + (800 if L else 200), y0 + (210 if L else 330), 'SOURCE UNTRACED', ROSE, ap(t, 's7', 0.55))
    ty = y0 + (330 if L else 460)
    rows = [('coralcastle.com', 'states "1,100 tons"; no estimator named', 0.15), ('Wikipedia', '1,100 short tons; figure not attributed', 0.3), ('NRHP form, 1984', 'lists pieces "up to 30 tons"; no total', 0.5), ('first estimator', 'not found', 0.7)]
    for i, (k, v, f) in enumerate(rows):
        aa = ap(t, 's7', f); yy = ty + i * (66 if L else 110)
        hline(cv, x0, x1, yy - 10, INK2, aa, 1)
        mono(cv, x0 + 10, yy + 4, k, 26, CYAN if i < 3 else ROSE, aa)
        if L: cv.text((x0 + 380, yy), v, 'sans', 32, TXT if i < 3 else ROSE, 'la', aa)
        else: cv.text((x0 + 10, yy + 40), v, 'sans', 32, TXT if i < 3 else ROSE, 'la', aa)

def sc_gate(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED', MINT, ease(t / 0.8))
    sc = 3.6 if L else 3.3
    gw, gh = 81 * sc, 92 * sc
    ex, ey = (x0 + 120, y0 + 60) if L else (x0 + 20, y0 + 20)
    a = ease(t / 1.0)
    stone(cv, ex, ey + 20, ex + 130, ey + 20 + gh + 30, a, DIM)
    stone(cv, ex + 130 + gw, ey + 20, ex + 260 + gw, ey + 20 + gh + 30, a, DIM)
    stone(cv, ex, ey - 20, ex + 260 + gw, ey + 20, a, DIM)      # lintel
    ga = ap(t, 's8', 0.12)
    stone(cv, ex + 130, ey + 22, ex + 130 + gw, ey + 20 + gh + 30, ga, CYAN)
    cx = ex + 130 + gw / 2
    sa = ap(t, 's8', 0.35)
    cv.line([(cx, ey - 20), (cx, ey + 20 + gh + 30)], mix(VIO, BG, sa), 5)
    cv.text((cx + 14, ey + 60), 'central shaft', 'mono', 18, VIO, 'la', sa); cv.text((cx + 14, ey + 84), '(auto axle, per form)', 'mono', 18, VIO, 'la', sa)
    cv.text((cx, ey + 20 + gh + 66), '81 in wide x 92 in tall x 21 in thick', 'monob', 20, TXT, 'ma', ga)
    # top view with swing
    tvx, tvy = (ex + 260 + gw + 190, ey + 150) if L else (ex + 260 + gw + 90, ey + 190)
    ang = math.radians(75 * (0.5 - 0.5 * math.cos(t * 0.9)))
    cv.line([(tvx - 150, tvy), (tvx - 100, tvy)], mix(DIM, BG, a), 8); cv.line([(tvx + 100, tvy), (tvx + 150, tvy)], mix(DIM, BG, a), 8)
    r = 100
    cv.line([(tvx - r * math.cos(ang), tvy - r * math.sin(ang)), (tvx + r * math.cos(ang), tvy + r * math.sin(ang))], mix(CYAN, BG, ga), 12)
    cv.circ((tvx, tvy), 9, mix(VIO, BG, sa)); cv.text((tvx, tvy + 130), 'top view: swings on its center', 'mono', 18, DIM, 'ma', ga)
    # 1986 facts
    fy = ey + 20 + gh + 130
    rows = [('"nine ton" (form)  -  see the next check', 0.35, MINT), ('1986: stopped turning; rusted truck bearing', 0.6, MINT), ('6 men + 50-ton crane lifted it out; reset July 1986', 0.78, MINT), ('2005: failed again (Wikipedia)', 0.92, DIM)]
    fx = x0 + (1130 if L else 20); yy = (ey + 20) if L else fy
    for i, (txt, f, col) in enumerate(rows):
        aa = ap(t, 's8', f)
        if aa <= 0: continue
        cv.rect((fx, yy + 6, fx + 5, yy + 36), mix(col, BG, aa))
        yy = cv.para(fx + 20, yy, txt, 'sans', 32 if L else 30, TXT, (x1 - fx - 30) if L else 900, 1.2, 'l', aa) + (24 if L else 12)

def sc_check(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'OUR ARITHMETIC', CYAN, ease(t / 0.8)); tag(cv, x0 + 270, y0 - 40, 'NOT SETTLED: GATE WEIGHT', ROSE, ap(t, 's9', 0.6))
    vol_in3 = 81 * 92 * 21; vft = vol_in3 / 1728.0
    rows = [('calcite, solid (2.71 g/cm3)', 2.71, 0.0), ('aragonite, solid (2.93 g/cm3)', 2.93, 0.0), ('aragonite, 30% pore space', 2.93 * 0.7, 0.0), ('calcite, 30% pore space', 2.71 * 0.7, 0.0)]
    a0 = ap(t, 's9', 0.05)
    mono(cv, x0, y0 + 10, f'81 x 92 x 21 in = {vol_in3:,} cubic in = {vft:.1f} cubic ft', 30 if L else 26, TXT, a0)
    mono(cv, x0, y0 + 56, '(1 g/cm3 = 62.43 lb/ft3; weight = volume x density)', 20, DIM, a0)
    order = [1, 0, 2, 3]; fr = [0.3, 0.38, 0.55, 0.62]
    scale_max = 10.0; bx0 = x0 + (500 if L else 0); bw = (x1 - bx0 - 150) if L else (x1 - x0 - 200)
    for i, k in enumerate(order):
        nm, d, _ = rows[k]; aa = ap(t, 's9', fr[i]); tons = vft * d * 62.428 / 2000.0
        yy = y0 + 120 + i * (84 if L else 120)
        if aa <= 0: continue
        if L: cv.text((x0, yy + 10), nm, 'sans', 28, TXT, 'la', aa); by = yy
        else: cv.text((x0, yy), nm, 'sans', 28, TXT, 'la', aa); by = yy + 40
        wl = bw * tons / scale_max * ease((t - F('s9', fr[i])) / 1.0)
        col = ROSE if i < 2 else MINT
        cv.rect((bx0, by, bx0 + wl, by + 44), mix(col, BG, aa * 0.8)); cv.text((bx0 + wl + 14, by + 22), f'{tons:.1f} short tons', 'monob', 24, TXT, 'lm', aa)
    ua = ap(t, 's9', 0.45)
    ux = bx0 + bw * 0.9
    ytop = y0 + 100; ybot = y0 + 120 + 4 * (84 if L else 120)
    cv.line([(ux, ytop), (ux, ybot)], mix(VIO, BG, ua), 3); cv.text((ux, ytop - 8), 'form: "nine ton"', 'monob', 22, VIO, 'ms', ua)
    mono(cv, x0, ybot + 20, 'densities: standard mineral values. 30% porosity is our assumption.', 20, DIM, ap(t, 's9', 0.7))
    mono(cv, x0, ybot + 50, 'if "ton" means metric, 9 t = 9.9 short tons: the mismatch grows.', 20, DIM, ap(t, 's9', 0.82))

def sc_tools(cv, t, p):
    night(cv, t, 0.5)
    x0, y0, x1, y1 = CONT
    lift = 0.35 + 0.3 * math.sin(t * 0.4)
    if L: tripod(cv, x0 + 330, y0 + 570, 520, ease(t / 1.0), lift, math.sin(t * 0.6))
    else: tripod(cv, x1 - 200, y0 + 330, 300, ease(t / 1.0), lift, math.sin(t * 0.6))
    tx = x0 + (720 if L else 0); ty = y0 + (0 if L else 360)
    rows = [('DOCUMENTED', MINT, 'tools on display (NRHP 1984): block and tackle ("metal fall"), rollers, jacks, wedges, slings, cables, sledges, chisels; some made from old car parts', 0.15),
            ('DOCUMENTED', MINT, 'old photographs show tall wooden tripods with chains, and a chain hoist', 0.5),
            ('UNKNOWN', ROSE, 'exact rig set-up and procedures: "no detailed records" (Rock Gate Park archive page)', 0.78)]
    yy = ty
    for lab, col, txt, f in rows:
        aa = ap(t, 's10', f)
        if aa > 0:
            tag(cv, tx, yy, lab, col, aa, 20)
            yy = cv.para(tx, yy + 56, txt, 'sans', 30 if L else 28, TXT, (x1 - tx - 20), 1.22, 'l', aa) + 22
    mono(cv, x0, y1 - (10 if L else 0), 'diagram: ILLUSTRATION of a pole tripod, not a drawing of his rig', 18, DIM, ease((t - 2) / 1.0))

def pulley(cv, cx, cy, w, a, col):
    cv.rect((cx - w / 2, cy - 22, cx + w / 2, cy + 22), mix(INK2, BG, a)); cv.outline((cx - w / 2, cy - 22, cx + w / 2, cy + 22), mix(col, BG, a), 2)
    for k in range(3): cv.ring((cx - w / 3 + k * w / 3, cy), 12, mix(col, BG, a), 2)

def sc_tackle(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'ILLUSTRATION: IDEAL, NO FRICTION', CYAN, ease(t / 0.8), 20)
    a = ease(t / 1.0)
    dx, dy = (x0 + 220, y0 + 90) if L else (x0 + 220, y0 + 70)
    u = 0.5 - 0.5 * math.cos(t * 0.5)
    topy = dy; boty = dy + 330 - 150 * u
    w = 280
    pulley(cv, dx, topy, w, a, DIM)
    pulley(cv, dx, boty, w, a, CYAN)
    for k in range(6):
        xx = dx - w / 2 + 14 + k * (w - 28) / 5
        cv.line([(xx, topy + 22), (xx, boty - 22)], mix(TXT, BG, a * 0.7), 2)
    cv.line([(dx + w / 2, topy), (dx + w / 2 + 70, topy), (dx + w / 2 + 70, topy + 380 + 30 * u)], mix(VIO, BG, a), 3)
    mono(cv, dx + w / 2 + 84, topy + 330, 'pull', 22, VIO, a)
    cv.line([(dx, boty + 22), (dx, boty + 70)], mix(TXT, BG, a * 0.7), 2)
    stone(cv, dx - 70, boty + 70, dx + 70, boty + 150, a, CYAN, '10 tons')
    cv.line([(dx, dy - 40), (dx, topy - 22)], mix(DIM, BG, a), 4)
    sx = x0 + (560 if L else 0); sy = y0 + (20 if L else 600)
    rows = [('load: 10 short tons = 20,000 lb', 0.0, TXT), ('6 rope segments:  20,000 / 6 = 3,333 lb pull', 0.18, TXT), ('two sets, 6 x 6 = 36:  20,000 / 36 = 556 lb', 0.4, TXT),
            ('+ 5:1 winch, 36 x 5 = 180:  20,000 / 180 = 111 lb', 0.58, MINT), ('cost: 180 ft of rope hauled per 1 ft of lift', 0.78, ROSE)]
    for i, (txt, f, col) in enumerate(rows):
        aa = ap(t, 's11', f)
        if aa <= 0: continue
        yy = sy + i * (84 if L else 56)
        cv.rect((sx, yy + 4, sx + 5, yy + 44), mix(col, BG, aa)); cv.text((sx + 20, yy), txt, 'sans', 34 if L else 28, col, 'la', aa)
    mono(cv, sx, sy + 5 * (84 if L else 56) + 10, 'possible on paper; real rigs lose force to friction', 20, DIM, ap(t, 's11', 0.9))

def sc_lever(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'ILLUSTRATION', CYAN, ease(t / 0.8))
    a = ease(t / 1.0)
    px, py = (x0 + 220, y0 + 330) if L else (x0 + 140, y0 + 330)
    ang = math.radians(-8 + 14 * (0.5 - 0.5 * math.cos(t * 0.8)))
    unit = 56
    lx, ly = px - unit * math.cos(ang), py + unit * math.sin(ang) * -1
    rx, ry = px + 9 * unit * math.cos(ang), py - 9 * unit * math.sin(ang) * -1
    poly(cv, [(px, py), (px - 30, py + 70), (px + 30, py + 70)], mix(DIM, BG, a))
    cv.line([(lx, ly), (rx, ry)], mix(TXT, BG, a), 10)
    stone(cv, lx - 60, ly - 70, lx + 10, ly - 4, a, CYAN)
    cv.line([(rx, ry - 70), (rx, ry - 8)], mix(VIO, BG, a), 4); poly(cv, [(rx - 10, ry - 20), (rx + 10, ry - 20), (rx, ry - 4)], mix(VIO, BG, a))
    cv.text((rx, ry - 84), 'push', 'mono', 20, VIO, 'ms', a); cv.text((px, py + 100), '1 : 9', 'monob', 26, TXT, 'ma', a)
    sx = x0 + (780 if L else 0); sy = y0 + (30 if L else 520)
    ap1 = ap(t, 's12', 0.25); ap2 = ap(t, 's12', 0.6)
    cv.text((sx, sy), 'force x arm = force x arm', 'monob', 32, TXT, 'la', ap1)
    cv.text((sx, sy + 60), '100 lb x 9 ft  =  900 lb x 1 ft', 'monob', 32, MINT, 'la', ap1)
    # cribbing: raise an inch, add a timber, repeat
    cy0 = sy + 170 if L else sy + 140
    for k in range(4):
        aa = ap(t, 's12', 0.55 + k * 0.1, 0.6)
        if aa <= 0: continue
        bx = sx + k * 170
        for j in range(k + 1): cv.rect((bx, cy0 + 120 - (j + 1) * 16, bx + 120, cy0 + 120 - j * 16 - 2), mix(DIM, BG, aa))
        stone(cv, bx + 10, cy0 + 120 - (k + 1) * 16 - 70, bx + 110, cy0 + 120 - (k + 1) * 16, aa, CYAN)
    cv.text((sx, cy0 + 150), 'raise an inch, slide a timber under, repeat', 'mono', 24, DIM, 'la', ap2)

def sc_affidavit(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    tag(cv, x0, y0 - 40, 'DOCUMENTED: 250+ AFFIDAVITS, 1955', MINT, ease(t / 0.8), 20)
    cols = 25 if L else 20; cell = 38 if L else 34
    for i in range(250):
        cx = x0 + 20 + (i % cols) * cell; cy = y0 + 40 + (i // cols) * cell
        lit = ease((t - 0.8 - i * 0.012) / 0.4)
        cv.circ((cx, cy), 7, mix(MINT, BG, 0.15 + 0.85 * lit))
    gy = y0 + 40 + (250 // cols + 1) * cell + 10
    qa = ap(t, 's13', 0.2)
    q = '"...without the aid of any individual or individuals... with simple hand tools..."'
    yy = cv.para(x0, gy, q, 'light', 36 if L else 34, TXT, (x1 - x0) * (0.55 if L else 1.0), 1.25, 'l', qa)
    mono(cv, x0, yy + 4, 'what the affiants signed, as quoted in the NRHP form (collected by the then-owner)', 18, DIM, qa)
    ub = ap(t, 's13', 0.62)
    tag(cv, x0, yy + 50, 'UNKNOWN', ROSE, ub, 22)
    cv.text((x0 + 170, yy + 54), 'who saw the largest blocks go up: the form quotes no one', 'sans', 28 if L else 26, TXT, 'la', ub)

def sc_words(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    a = ease(t / 1.0)
    tag(cv, x0, y0 - 40, 'CLAIMED', VIO, a)
    qa = ap(t, 's14', 0.1)
    cv.rect((x0, y0 + 10, x0 + 5, y0 + (330 if L else 420)), mix(VIO, BG, qa))
    yy = cv.para(x0 + 30, y0 + 10, '"the methods used by the pyramid builders, the practical knowledge of the laws of leverage and weight"', 'light', 54 if L else 50, TXT, (x1 - x0 - 60) * (0.8 if L else 1), 1.2, 'l', qa)
    mono(cv, x0 + 30, yy + 10, 'Ed\'s reply to how he did it, as paraphrased in the NRHP form, 1984', 20, DIM, qa)
    py0 = y0 + (400 if L else 520)
    mono(cv, x0, py0, 'PAMPHLETS (he sold these)', 22, CYAN, ap(t, 's14', 0.55))
    ps = [('1936', 'A Book in Every Home', 0.62), ('Aug 1945', 'Magnetic Current', 0.76), ('Oct 1945', 'Mineral, Vegetable and Animal Life', 0.88)]
    for i, (yr, nm, f) in enumerate(ps):
        aa = ap(t, 's14', f); yy2 = py0 + 46 + i * 56
        mono(cv, x0, yy2, yr, 28, MINT, aa); cv.text((x0 + 200, yy2 - 2), nm, 'sans', 34, TXT, 'la', aa)
    mono(cv, x0, py0 + 46 + 3 * 56 + 6, 'we found none that describes how he lifted the blocks', 22, ROSE, ap(t, 's14', 0.95))

def sc_theories(cv, t, p):
    night(cv, t, 0.4)
    x0, y0, x1, y1 = CONT
    items = [('sound', 'sound levitates the stone', 0.12), ('magnetism', '"magnetic current" cancels weight', 0.3), ('help from beyond Earth', 'already circulating by 1984', 0.48)]
    for i, (a1, a2, f) in enumerate(items):
        aa = ap(t, 's15', f)
        if aa <= 0: continue
        if L:
            cw = (x1 - x0 - 80) / 3; cx = x0 + i * (cw + 40); cy = y0 + 10; ch = 330
        else:
            cw = x1 - x0; cx = x0; cy = y0 + i * 235; ch = 215
        card(cv, cx, cy, cw, ch, ROSE, aa)
        big(cv, cx + 28, cy + 24, a1, 48 if L else 46, TXT, aa)
        cv.para(cx + 28, cy + 96, a2, 'sans', 28, DIM, cw - 56, 1.2, 'l', aa)
        if L:
            tag(cv, cx + 28, cy + ch - 120, 'NOT ESTABLISHED', ROSE, aa, 20); mono(cv, cx + 28, cy + ch - 62, 'evidence found: none', 22, TXT, aa)
        else:
            tag(cv, cx + 28, cy + ch - 70, 'NOT ESTABLISHED', ROSE, aa, 20); mono(cv, cx + 330, cy + ch - 62, 'evidence found: none', 22, TXT, aa)
    ub = ap(t, 's15', 0.72); yb = y0 + (390 if L else 740)
    big(cv, x0, yb, 'absence of evidence is not proof of absence.', 44 if L else 38, TXT, ub)
    mono(cv, x0, yb + 70, 'floating-stone stories: secondhand. not established is not the same as impossible.', 22, DIM, ap(t, 's15', 0.85))

LEDGER = [('DOCUMENTED', MINT, 'dates, the form\'s weights, the move, the tools, the 1986 repair', 0.22),
          ('CLAIMED', VIO, 'worked alone  /  pyramid builders\' methods  /  1,100 tons', 0.5),
          ('NOT SETTLED', ROSE, 'the gate\'s true weight', 0.7),
          ('UNKNOWN', ROSE, 'how the largest blocks were raised and set, alone', 0.85)]
def sc_ledger(cv, t, p):
    night(cv, t, 0.3)
    x0, y0, x1, y1 = CONT
    big(cv, x0, y0 + 10, 'the ledger', 56 if PORT else 64, TXT, ease(t / 1.0))
    step = 150 if PORT else 112
    for i, (st, col, txt, f) in enumerate(LEDGER):
        a = ap(t, 's16', f)
        if a <= 0: continue
        yy = y0 + 110 + i * step
        hline(cv, x0, x1, yy, INK2, a, 1)
        tag(cv, x0, yy + 16, st, col, a, 22)
        if L: big(cv, x0 + 360, yy + 10, txt, 40, TXT, a)
        else: cv.para(x0, yy + 76, txt, 'light', 38, TXT, x1 - x0, 1.15, 'l', a)

def sc_close(cv, t, p):
    night(cv, t, 0.8)
    x0, y0, x1, y1 = CONT
    a = ease(t / 1.0)
    sz = 120 if L else 100
    big(cv, x0, y0 + 20, 'not established.', sz, TXT, ap(t, 's17', 0.45))
    big(cv, x0, y0 + 20 + sz * 1.2, 'not ruled out.', sz, TXT, ap(t, 's17', 0.62))
    tag(cv, x0, y0 + 20 + sz * 2.6, 'NOT ESTABLISHED', ROSE, ap(t, 's17', 0.5), 24); tag(cv, x0 + 330, y0 + 20 + sz * 2.6, 'NOT RULED OUT', MINT, ap(t, 's17', 0.68), 24)
    big(cv, x0, y0 + 20 + sz * 3.4, 'someone watching this might be the one who works it out.', 36 if L else 34, CYAN, ap(t, 's17', 0.82, 1.2))
    if L: tripod(cv, 1560, 830, 380, 0.5 * a, 0.2 + 0.1 * math.sin(t * 0.5), math.sin(t * 0.6))

SOURCES = [
    'NPS: National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed\'s Place)" / Coral Castle. Florida Division of Archives, 2 Apr 1984; listed 10 May 1984; renamed Coral Castle 2011 (npgallery.nps.gov, asset 1ed2ccd0-b692-42dc-b28d-1227c1a23407)',
    'Wikipedia, "Coral Castle" and "Edward Leedskalnin" (read 2026-10-13): 1986 gate repair, 2005 failure, 1,100 short tons (figure unattributed)',
    'coralcastle.com, "The Secrets of Coral Castle" (1,100 tons); rockgatepark.com/the-tools (tool photographs; "no detailed records")',
    'Photographs of the hoists exist: Florida Memory item 328424 (see it there). No photographs are used in this video; every picture is drawn.',
    'Further reading: P. A. Hancock, "The making of a modern myth: Edward Leedskalnin and the Coral Castle", Skeptic 18(1), 2013',
    'Our arithmetic (gate volume, density, block and tackle, lever): standard formulas; calcite 2.71 and aragonite 2.93 g/cm3; 30% porosity is assumed']
def sc_end(cv, t, p):
    night(cv, t, 0.7)
    a = ease(t / 1.0)
    if L: tripod(cv, 1620, 700, 300, 0.35 * a, 0.2, 0.0)
    y = 160 if PORT else 70
    mono(cv, HEAD[0], y, 'HEARTBEAT TV  /  CH 10', 26, CYAN, a)
    big(cv, HEAD[0], y + 40, 'still unknown', 110 if PORT else 110, TXT, a)
    mono(cv, HEAD[0], y + (170 if PORT else 170), 'heartbeatobservatory.com', 34, CYAN, a)
    yy = y + (240 if PORT else 240)
    mono(cv, HEAD[0], yy, 'SOURCES', 22, DIM, ease((t - 0.6) / 1)); yy += 40
    for i, s in enumerate(SOURCES):
        yy = cv.para(HEAD[0], yy, s, 'mono', 21 if PORT else 22, TXT, (W - 2 * HEAD[0]) * (1 if PORT else 0.95), 1.25, 'l', ease((t - 0.8 - i * 0.15) / 0.8)) + 10

# (segment id, headline, source line, draw fn)
SCENES = [
    ('s1', None, 'Edward Leedskalnin, 1887-1951. 1,100 tons: castle figure, source untraced', sc_title),
    ('s2', 'a man from latvia', 'NRHP nomination form, Florida Division of Archives, 1984', sc_man),
    ('s3', 'a love story, and its gaps', 'NRHP form 1984 (name spellings, footnote 2); Wikipedia "Edward Leedskalnin"', sc_agnes),
    ('s4', 'ed\'s place, 1923', 'NRHP form 1984; Dade County Deed Book 1546, p. 8', sc_site),
    ('s5', 'the move to homestead', 'NRHP form 1984 (sec. 7, 8; obelisk inscription)', sc_move),
    ('s6', 'what the form weighs', 'NRHP form 1984: weights in pounds, converted here', sc_weights),
    ('s7', 'the 1,100-ton total', 'coralcastle.com; Wikipedia "Coral Castle"; NRHP form 1984', sc_total),
    ('s8', 'the gate', 'NRHP form 1984; Wikipedia "Coral Castle" (1986 repair, 2005)', sc_gate),
    ('s9', 'a check anyone can do', 'Volume x density. Our arithmetic, assumptions on screen', sc_check),
    ('s10', 'the tools', 'NRHP form 1984 (tool list); rockgatepark.com/the-tools', sc_tools),
    ('s11', 'block and tackle', 'Ideal mechanical advantage = rope segments. Worked example, not his rig', sc_tackle),
    ('s12', 'the lever', 'Law of the lever. Worked example, not his method', sc_lever),
    ('s13', 'what no one has documented', 'NRHP form 1984 quoting the 1955 affidavits', sc_affidavit),
    ('s14', 'what he said', 'NRHP form 1984 (paraphrase of his reply; pamphlet list)', sc_words),
    ('s15', 'popular theories', 'NRHP form 1984 (extraterrestrial, gravity theories); thisunexplaineduniverse.com', sc_theories),
    ('s16', None, 'Status as of October 2026', sc_ledger),
    ('s17', None, None, sc_close),
    ('s18', None, None, sc_end),
]

def _subs(text):
    out = []
    for s in re.split(r'(?<=[.?!])\s+', text.strip()):
        parts = [s]
        while True:
            nxt = []; changed = False
            for q in parts:
                if len(q) > 96:

web search: 
web search: 'April 2, 1984'
web search: 
web search: 
web search: 
web search: newspaper Coral Castle gate repaired "July 23" 1986 Homestead ...
web search: 
web search: "1,100 tons" "Coral Castle" before:1990 ...
web search: 
web search: 
web search: 
web search: 
web search: 
web search: site:engineeringstatics.org block tackle mechanical advantage supporting rope segments displacement ...
web search: 
web search: site:rockgatepark.com/the-tools "no detailed records" Edward Leedskalnin ...
web search: 
web search: 'historic Rock Gate'
codex
## Fact-check result

**Needs revision.** Most claims accurately report what the 1984 National Register nomination says, but the script sometimes upgrades those retrospective assertions into established facts. The largest problems are the relocation timeline, Bob Biggersâ€™s role, the weakly sourced gate-repair details, the â€œ180 feet of ropeâ€ statement, the description of Rock Gate Park as â€œthe castleâ€™s archive,â€ and the final ledgerâ€™s overuse of â€œDOCUMENTED.â€

I audited [SOURCES.md](<C:/Users/lilli/AI-Shared/projects/still-unknown/ep2-coral-castle/SOURCES.md>), [script.json](<C:/Users/lilli/AI-Shared/projects/still-unknown/ep2-coral-castle/script.json>), and the scene text/`SCENES` list in [ep_body.py](<C:/Users/lilli/AI-Shared/projects/still-unknown/ep2-coral-castle/ep_body.py:120>). No files were changed.

Status meanings:

- **CONFIRMED** â€” supported by a primary record or accurately framed as â€œthe source says.â€
- **WRONG** â€” contradicted, materially misleading, or mathematically incorrect.
- **UNSURE** â€” plausible, but the available evidence is retrospective, conflicting, or does not prove the claim.

## Priority findings

### Relocation: 1936, 1937, or 1939?

| Claim | Status | Finding |
|---|---|---|
| He bought the new ten-acre property in the mid-1930s | **CONFIRMED** | The current Coral Castle history says he decided to move in 1935 and purchased the tract by 1936. |
| â€œThe form says 1937â€ | **CONFIRMED** as an attribution | The nomination marks â€œmoved date 1937â€ and says he decided to relocate in 1937. |
| The actual relocation occurred in 1937 | **WRONG / unsupported** | The same nomination reproduces the obelisk inscription â€œMoved in 1939â€ and cites an August 1939 article about the move. The castleâ€™s newer chronology says land clearing began in May 1939 and contemporary coverage described the move that summer. The form is internally inconsistent. |
| â€œMoved in 1939â€ is inscribed on the obelisk | **CONFIRMED** | The nomination transcribes: â€œMade in 1928. Moved in 1939. Born 1887. Latvia, E.L.â€ [NPS nomination](https://npgallery.nps.gov/GetAsset/1ed2ccd0-b692-42dc-b28d-1227c1a23407/). |
| Move began about 1936 and lasted about three years | **UNSURE** | This appears to have arisen by combining the 1936 purchase with the 1939 inscription. The newer castle chronology instead places preparatory clearing and active relocation in 1939. |
| On-screen `1936â€“40 ... about three years of moving` | **WRONG** | No reviewed source establishes that range, and â€œabout three yearsâ€ does not match `1936â€“40`. |
| Best usable chronology | **CONFIRMED with qualification** | â€œHe acquired the new land by 1936; the 1984 nomination gives 1937, but contemporary-moving evidence and his obelisk point to active relocation in 1939.â€ |

Sources: [official Coral Castle chronology](https://coralcastle.com/home/about-edward-leedskalnin/), [NPS nomination](https://npgallery.nps.gov/GetAsset/1ed2ccd0-b692-42dc-b28d-1227c1a23407/).

### Bob Biggers and the truck

| Claim | Status | Finding |
|---|---|---|
| Bob Biggers â€œlent his truckâ€ | **WRONG / materially incomplete** | The nomination says Ed wanted the use of Biggersâ€™s truck, but the castleâ€™s fuller account says Bob came and pulled the loaded trailer between sites. He was therefore the hauling driver/operator, not merely a passive lender. |
| Ed loaded and unloaded the stones alone and at night | **UNSURE** | This is what the nomination and later oral-history accounts say, but it is not demonstrated by a contemporary eyewitness record reviewed here. |
| The move was completed â€œwithout any assistanceâ€ | **WRONG if read literally** | Bobâ€™s transportation role is assistance. The defensible narrower claim is that Ed reportedly loaded and unloaded the trailer without Bobâ€™s help. |
| Bob Biggers was a local man/farmer | **CONFIRMED** | Consistent across the nomination and castle account. |

Recommended wording: â€œBob Biggers hauled the loaded trailer between sites; later accounts say Ed loaded and unloaded the stones alone, usually at night.â€

### Gate repair

| Claim | Status | Finding |
|---|---|---|
| Gate dimensions: 81 Ã— 92 Ã— 21 inches | **CONFIRMED as the nominationâ€™s figures** | Stated twice in the nomination. |
| Nine-ton weight | **UNSURE** | It is the traditional/National Register figure, but no weighing or derivation was found, and it conflicts with the published dimensions and plausible material densities. |
| Central shaft/automobile axle and truck bearing | **CONFIRMED** | The nomination describes an automobile axle; later repair accounts describe a truck bearing. |
| Could be moved with one finger | **CONFIRMED historically; WRONG in present tense** | The nomination records this before the failure. â€œOne finger moves itâ€ should be â€œit was reported to turn with one finger.â€ |
| Gate stopped in 1986 | **UNSURE** | A 1990 newspaper retrospective says 1986, but Coral Castleâ€™s present website says 1984. |
| Six men and a 50-short-ton crane | **UNSURE** | A 1990 newspaper supports exactly six men and a 50-ton crane, but other accounts say five workers and a 20-ton crane; Coral Castle says only â€œsix men and a crane.â€ Treat it as a widely repeated repair account, not settled fact. [1990 Hollywood Sun](https://digitalarchives.broward.org/digital/collection/p16146coll7/id/44746/) |
| Rusted bearing caused the failure | **CONFIRMED as the reported repair finding** | Consistent across the official castle account and later descriptions. |
| Reset on July 23, 1986 | **UNSURE** | The exact date traces online mainly to Wikipedia, whose cited source is a 2006 YouTube videoâ€”not a contemporary repair record. |
| Failed again in 2005 | **UNSURE** | Repeated by Wikipedia without a distinct supporting citation. A December 2003 *Wired* report already described a recent removal and reseating, so the repair history is more complicated than the script suggests. [Wired](https://www.wired.com/2003/12/secret-energy-haunts-coral-castle/) |
| No longer rotates as smoothly | **UNSURE but plausible** | Repeated in later visitor and encyclopedia accounts; not supported here by a repair report or measurement. |

The sceneâ€™s `DOCUMENTED` label is too strong for the entire repair block. Use **â€œREPORTED: 1986 REPAIR ACCOUNTSâ€** and mark the exact July date and 2005 failure as unverified.

### Gate-volume arithmetic

| Claim | Status | Finding |
|---|---|---|
| `81 Ã— 92 Ã— 21 = 156,492 inÂ³` | **CONFIRMED** |
| `156,492 inÂ³ = 90.6 ftÂ³` | **CONFIRMED** | Exact result: 90.5625 ftÂ³. |
| Calcite density 2.71 g/cmÂ³ | **CONFIRMED** | USGS commonly uses 2.72; 2.71 is a standard mineral value. |
| Aragonite density 2.93 g/cmÂ³ | **CONFIRMED** | USGS assigns 2.93 g/cmÂ³. [USGS density discussion](https://pubs.usgs.gov/of/1987/0665/report.pdf) |
| Solid-calcite result â‰ˆ7.7 short tons | **CONFIRMED** | Approximately 7.66 tons. |
| Solid-aragonite result â‰ˆ8.3 short tons | **CONFIRMED** | Approximately 8.29 tons. |
| Thirty-percent-pore dry results â‰ˆ5.4/5.8 tons | **CONFIRMED mathematically** | These assume empty/dry pore volume. Water-filled pores would increase the mass. |
| Thirty-percent porosity is plausible | **CONFIRMED as a plausible scenario, not the gateâ€™s measured porosity** | USGS found substantial and variable porosity in hundreds of Miami Limestone samples. [USGS OFR 85-21](https://pubs.usgs.gov/of/1985/0021/report.pdf) |
| â€œEven solid aragonite, the densest the rock could beâ€ | **WRONG** | Aragonite is a useful conservative carbonate end member, but not an absolute maximum for every possible mineral inclusion or water-filled rock. Say â€œeven treating the entire rectangular volume as solid aragonite.â€ |
| â€œReal oolite is porousâ€ | **CONFIRMED** |
| â€œNine tons is probably a rounded figure, not a weighingâ€ | **UNSURE but reasonable inference** | The discrepancy makes that likely, but no record of how the nine-ton number was obtained was found. |
| â€œIf ton means metricâ€¦â€ | **WRONG / misleading** | In this American nomination, surrounded by pound figures, â€œtonâ€ almost certainly means a 2,000-pound short ton. The metric scenario adds confusion without evidentiary value. |
| Volume calculation represents the exact gate | **UNSURE** | It treats the stated maximum dimensions as a full rectangular prism. Any irregular faces, holes, or rounded edges reduce volume. |

The arithmetic is good; the interpretation needs tighter wording.

### The 1,100-ton figure

| Claim | Status | Finding |
|---|---|---|
| Coral Castle currently states 1,100 tons | **CONFIRMED** | [Official Coral Castle page](https://coralcastle.com/home/the-secrets-of-coral-castle/). |
| Wikipedia states 1,100 short tons | **CONFIRMED** |
| Wikipedia supplies a source for the total | **WRONG** | Its current 1,100-ton sentence has no citation attached. |
| The 1984 nomination gives no overall total | **CONFIRMED** |
| 1,100 is an independently established total | **UNSURE** | No inventory, survey, scale record, or documented calculation was located. |
| â€œThe castleâ€™s own figureâ€ | **CONFIRMED only in the sense that the present operator promotes it** | It should not imply that Leedskalnin or an engineer calculated it. |
| First estimator not found | **CONFIRMED as the research result** | The search did not identify one. |
| Carroll A. Lake may be the source of exactly 1,100 tons | **WRONG** | Lakeâ€™s mid-1950s account says â€œover 1000 tonsâ€; another passage says roughly 1,000 tons in the wall/castle plus nearly half again in furniture. It does not provide a clean 1,100-ton calculation and is internally inconsistent. [Lake text](https://magneticuniverse.com/uploads/FileUpload/31/21d96d1d17317ae587ef3fa556b1c2.pdf) |
| Earliest exact 1,100-ton estimate | **UNSURE** | Exact â€œ1,100â€ appears in later promotional material, but the first use could not be dated. An undated/modern-scanned Coral Castle brochure uses it; a searchable 1998 Usenet repost also contains it. Neither identifies an estimator. |

Best conclusion: **Carroll A. Lake is the earliest quantitative lead locatedâ€”â€œover 1,000 tons,â€ circa the mid-1950sâ€”but he is not shown to be the originator of the exact 1,100-ton figure.**

### Block and tackle and lever calculations

| Claim | Status | Finding |
|---|---|---|
| Ideal mechanical advantage equals the supporting rope segments | **CONFIRMED for a simple block-and-tackle correctly rigged** |
| 20,000 Ã· 6 = 3,333 lb | **CONFIRMED** |
| Two properly compounded 6:1 systems produce ideal 36:1 | **CONFIRMED conditionally** | They must actually be cascaded so one system pulls the other; merely placing two tackle sets together does not automatically multiply them. |
| 20,000 Ã· 36 â‰ˆ556 lb | **CONFIRMED** |
| Adding an ideal 5:1 winch gives total 180:1 and â‰ˆ111 lb input | **CONFIRMED conditionally** | This is an ideal speed/force-ratio example, not evidence about Edâ€™s equipment. |
| â€œWhich one person can pullâ€ | **UNSURE** | A 111-pound sustained pull is substantial; friction, rope stiffness, sheave losses, startup loads, structure stability, and safety margins could raise it greatly. |
| â€œ180 ft of rope per 1 ft liftâ€ after adding the winch | **WRONG** | The 36:1 tackle requires roughly 36 feet of tackle-rope travel per foot of lift. A 5:1 winch makes the operatorâ€™s handle/input travel roughly five times the drum-rope travelâ€”about 180 feet of equivalent input motionâ€”not 180 feet of rope hauled through the tackle. [Pulley-system explanation](https://www.cmcpro.com/pulleys-and-mechanical-advantage-systems/) |
| Friction is ignored | **CONFIRMED and properly disclosed** |
| 9:1 lever: `100 lb Ã— 9 ft = 900 lb Ã— 1 ft` | **CONFIRMED as ideal statics** |
| That example can raise the preceding ten-ton block | **WRONG if implied** | Nine hundred pounds of ideal output cannot raise a 20,000-pound load. The lever drawing must be presented as an unrelated principle example or use a much larger ratio/effort. |
| â€œRaise an inch, crib, repeatâ€ | **CONFIRMED as a real technique in general** | It does not prove Leedskalnin used that exact procedure on the largest blocks. |

## Remaining narration and screen claims

| Scene/claim | Status | Finding |
|---|---|---|
| **s1:** Leedskalnin lived 1887â€“1951 | **CONFIRMED** |
| He worked on the structures from 1923 until his death | **CONFIRMED broadly** |
| He alone cut, moved, and erected every stone | **UNSURE** | Widely attested, including affidavits, but not proved lift-by-lift; Bob Biggers assisted with transport. |
| **s2:** Born in Latvia in 1887 | **CONFIRMED** |
| Engagement at about 26 to Agnes, ten years younger; she ended it | **CONFIRMED only as the 1984 nominationâ€™s account** |
| He called the real Agnes â€œSweet Sixteenâ€ | **UNSURE** | His writing uses â€œSweet Sixteen,â€ but whether it identifies the historically disputed fiancÃ©e is uncertain. |
| Work across North America, illness, early-1920s Florida arrival | **CONFIRMED as the nominationâ€™s biography; independently incomplete** |
| **s3:** Scuff/Skuvst spellings and conflicting Latvian name/age | **CONFIRMED** |
| The love-story motive comes from later tellings | **CONFIRMED** |
| **s4:** 1923 purchase of one acre for $12 | **CONFIRMED by the nominationâ€™s deed citation** |
| Ground was oolitic limestone called coral rock | **CONFIRMED** |
| Shed, tower, wall, furniture, astronomical pieces | **CONFIRMED broadly** |
| On-screen â€œsundial?â€ at the original site | **UNSURE** | Appropriately marked with a question mark. |
| **s6:** Polaris 40,000 lb; quarter moons 36,000 each; full-moon fountain 46,000; obelisk 57,000; north-wall sculpture 30 tons | **CONFIRMED as figures printed in the nomination** | They are not independently verified measurements. |
| Polaris slab was 25 feet tall | **CONFIRMED as the formâ€™s figure** |
| Wall blocks 8 Ã— 4 Ã— 3 feet, â€œseveral tonsâ€ | **CONFIRMED as the formâ€™s description** |
| Mars and Saturn 36,000 lb each | **CONFIRMED as the formâ€™s figures** |
| **s10:** Tools listed in the form | **CONFIRMED** |
| Some quarrying/sculpting tools fashioned from old automobile parts | **CONFIRMED as the formâ€™s account** |
| Historical photographs show tall wooden tripod-like frames and suspended lifting gear | **CONFIRMED** | Florida Memory catalogs a circa-1936 photograph with hoisting equipment. [Florida Memory results](https://floridamemory.com/find?advanced%5B0%5D%5Belement_id%5D=240&advanced%5B0%5D%5Bjoiner%5D=and&advanced%5B0%5D%5Bterms%5D=11&advanced%5B0%5D%5Btype%5D=is+exactly&advanced%5B1%5D%5Belement_id%5D=49&advanced%5B1%5D%5Bjoiner%5D=and&advanced%5B1%5D%5Bterms%5D=Historic+sites--Florida--Homestead&advanced%5B1%5D%5Btype%5D=is+exactly&layout=1&order=d&query=&sort=43) |
| Rockgatepark.com is â€œthe castleâ€™s archiveâ€ | **WRONG** | The site explicitly says it is an independent archive, not affiliated with Coral Castle. [Rock Gate Park notice](https://www.rockgatepark.com/) |
| No detailed record of the exact rig configuration/procedure | **CONFIRMED as the independent archiveâ€™s conclusion** | Avoid presenting that conclusion as an official institutional finding. |
| **s13:** Over 250 affidavits were collected in 1955 | **CONFIRMED** |
| Julius Levin collected them | **CONFIRMED** | The nominationâ€™s pronoun refers back to Levin. |
| Levin was the then owner, having purchased in 1953 | **CONFIRMED by the nomination** |
| Affiants were Homestead-area residents acquainted with Ed | **CONFIRMED** |
| Affidavits said he worked without other individuals and with simple hand tools | **CONFIRMED as their sworn wording** |
| They were notarized by Bodil K. Lowe | **CONFIRMED** |
| The nomination quotes no named witness to a specific largest-block lift | **CONFIRMED** |
| The affidavits prove every large lift was solo | **UNSURE** | Their generic form language does not identify which work each signer personally observed. |
| **s14:** â€œPyramid buildersâ€ and â€œlaws of leverage and weightâ€ | **CONFIRMED as the nominationâ€™s paraphrase** | Correctly not presented as a verbatim Ed quotation. |
| No Leedskalnin-authored document describes the lifting process | **CONFIRMED within the reviewed writings** |
| *A Book in Every Home* â€” 1936 | **CONFIRMED** |
| *Magnetic Current* â€” August 1945, Franklin Press | **CONFIRMED** | The surviving text itself says copyright August 1945. [Text](https://www.leedskalnin.com/Leedskalnins-Writings-MAGNETIC-CURRENT.html) |
| *Mineral, Vegetable and Animal Life* â€” October 1945, Franklin Press | **CONFIRMED** |
| *Magnetic Current* concerns magnets/electricity | **CONFIRMED** |
| None of those works explains how the stones were lifted | **CONFIRMED** |
| **s15:** Extraterrestrial and gravity/weightlessness stories existed by 1984 | **CONFIRMED** | The nomination records both. |
| Sound levitation was already among the theories by 1984 | **UNSURE** | It is not one of the theories named in the nomination. |
| Magnetism â€œcancelled weightâ€ is what his pamphlets claim | **WRONG** | The pamphlets advance unconventional magnetic theories, but they do not state a stone-lifting or weight-cancellation method. |
| Floating-stone stories are secondhand | **CONFIRMED** |
| No measurement, recording, or physical trace was found for exotic lifting | **CONFIRMED within this reviewâ€™s evidence** |
| â€œNot established, not impossible/not ruled outâ€ | **WRONG / editorially misleading** | Absence of proof does not place conventional rigging and extraordinary levitation on equal evidentiary footing. Say â€œunsupported; available physical evidence points to conventional rigging.â€ |
| **s16:** â€œDocumented: the datesâ€ | **WRONG** | The dates conflict materially. |
| â€œDocumented: the moveâ€ | **UNSURE as phrased** | The relocation is established, but its exact schedule and the solo-loading claim are not. |
| â€œDocumented: the formâ€™s weightsâ€ | **CONFIRMED only if explicitly meaning the form prints those estimates** |
| â€œDocumented: the 1986 repairâ€ | **WRONG / too strong** | Important details conflict or derive from poorly sourced later accounts. |
| Worked alone / pyramid knowledge / 1,100 tons are claims | **CONFIRMED categorization** |
| Gateâ€™s true weight is unsettled | **CONFIRMED categorization** |
| Exact largest-block lifting procedures are unknown | **CONFIRMED, although conventional lifting equipment is documented** |
| **s17:** Patient work and simple machines fit the evidence | **CONFIRMED as a reasonable inference** |
| Stranger mechanisms remain equally viable | **WRONG / unsupported framing** |

## SOURCES.md and end-card corrections

- **CONFIRMED:** Nomination prepared by Maria Temkin and Michael Zimny on April 2, 1984; listed May 10, 1984; reference 84000840. The 2011 correspondence requests and supports changing the official name from Rock Gate to Coral Castle. [NPS record](https://npgallery.nps.gov/AssetDetail/1ed2ccd0-b692-42dc-b28d-1227c1a23407/)

- **CONFIRMED:** The nomination title fields read historic â€œRock Gate (Edâ€™s Place)â€ and common â€œCoral Castle.â€

- **WRONG:** â€œWikipedia â€¦ 1986 repair, 2005 failureâ€ on the end card makes Wikipedia look like adequate verification. Its exact July-date citation is merely a 2006 YouTube upload, and the 2005 sentence has no separate citation.

- **WRONG:** `rockgatepark.com/the-tools` is described in narration as â€œthe castleâ€™s archive.â€ It is independent and expressly unaffiliated.

- **UNSURE:** Florida Memoryâ€™s circa-1936 catalog date for Homestead hoisting photographs conflicts with the stronger evidence placing relocation activity in 1939. The photograph exists; the date/location metadata should be qualified.

- **WRONG:** `Status as of October 2026` suggests a live status check of every physical feature. The audit did not establish the gateâ€™s current operational state.

## Recommended minimum revisions

1. Replace the move scene with the 1936 land-purchase/1939 active-move chronology and explicitly call the formâ€™s 1937 entry inconsistent.
2. Say Bob Biggers hauled the trailer; qualify the solo loading/unloading as a later account.
3. Relabel the gate repair **REPORTED**, omit the exact July 23 date and 2005 failure unless a contemporary repair record is obtained.
4. Change â€œone finger moves itâ€ to historical past tense.
5. Preserve the gate calculation but say â€œfull rectangular solid-aragonite upper-case modelâ€; remove the metric-ton aside.
6. Change â€œ180 feet of ropeâ€ to â€œ36 feet of tackle-rope travel, or about 180 feet of idealized operator-input travel after a 5:1 winch.â€
7. Identify Rock Gate Park as an independent website.
8. Replace â€œnot ruled outâ€ with â€œunsupported; the surviving equipment and photographs support conventional mechanical methods.â€
9. Describe all listed stone weights as **the nominationâ€™s published estimates**, not verified weights.
10. Keep 1,100 tons explicitly untraced; note that Carroll Lake supplied an earlier â€œover 1,000 tonsâ€ claim but not the exact 1,100 figure.

**Verdict: The episodeâ€™s core history is usable, but it needs revision before release because several disputed or promotional claims are presently labeled â€œdocumented,â€ and one mechanical calculation is materially misstated.**
tokens used
174,154
## Fact-check result

**Needs revision.** Most claims accurately report what the 1984 National Register nomination says, but the script sometimes upgrades those retrospective assertions into established facts. The largest problems are the relocation timeline, Bob Biggersâ€™s role, the weakly sourced gate-repair details, the â€œ180 feet of ropeâ€ statement, the description of Rock Gate Park as â€œthe castleâ€™s archive,â€ and the final ledgerâ€™s overuse of â€œDOCUMENTED.â€

I audited [SOURCES.md](<C:/Users/lilli/AI-Shared/projects/still-unknown/ep2-coral-castle/SOURCES.md>), [script.json](<C:/Users/lilli/AI-Shared/projects/still-unknown/ep2-coral-castle/script.json>), and the scene text/`SCENES` list in [ep_body.py](<C:/Users/lilli/AI-Shared/projects/still-unknown/ep2-coral-castle/ep_body.py:120>). No files were changed.

Status meanings:

- **CONFIRMED** â€” supported by a primary record or accurately framed as â€œthe source says.â€
- **WRONG** â€” contradicted, materially misleading, or mathematically incorrect.
- **UNSURE** â€” plausible, but the available evidence is retrospective, conflicting, or does not prove the claim.

## Priority findings

### Relocation: 1936, 1937, or 1939?

| Claim | Status | Finding |
|---|---|---|
| He bought the new ten-acre property in the mid-1930s | **CONFIRMED** | The current Coral Castle history says he decided to move in 1935 and purchased the tract by 1936. |
| â€œThe form says 1937â€ | **CONFIRMED** as an attribution | The nomination marks â€œmoved date 1937â€ and says he decided to relocate in 1937. |
| The actual relocation occurred in 1937 | **WRONG / unsupported** | The same nomination reproduces the obelisk inscription â€œMoved in 1939â€ and cites an August 1939 article about the move. The castleâ€™s newer chronology says land clearing began in May 1939 and contemporary coverage described the move that summer. The form is internally inconsistent. |
| â€œMoved in 1939â€ is inscribed on the obelisk | **CONFIRMED** | The nomination transcribes: â€œMade in 1928. Moved in 1939. Born 1887. Latvia, E.L.â€ [NPS nomination](https://npgallery.nps.gov/GetAsset/1ed2ccd0-b692-42dc-b28d-1227c1a23407/). |
| Move began about 1936 and lasted about three years | **UNSURE** | This appears to have arisen by combining the 1936 purchase with the 1939 inscription. The newer castle chronology instead places preparatory clearing and active relocation in 1939. |
| On-screen `1936â€“40 ... about three years of moving` | **WRONG** | No reviewed source establishes that range, and â€œabout three yearsâ€ does not match `1936â€“40`. |
| Best usable chronology | **CONFIRMED with qualification** | â€œHe acquired the new land by 1936; the 1984 nomination gives 1937, but contemporary-moving evidence and his obelisk point to active relocation in 1939.â€ |

Sources: [official Coral Castle chronology](https://coralcastle.com/home/about-edward-leedskalnin/), [NPS nomination](https://npgallery.nps.gov/GetAsset/1ed2ccd0-b692-42dc-b28d-1227c1a23407/).

### Bob Biggers and the truck

| Claim | Status | Finding |
|---|---|---|
| Bob Biggers â€œlent his truckâ€ | **WRONG / materially incomplete** | The nomination says Ed wanted the use of Biggersâ€™s truck, but the castleâ€™s fuller account says Bob came and pulled the loaded trailer between sites. He was therefore the hauling driver/operator, not merely a passive lender. |
| Ed loaded and unloaded the stones alone and at night | **UNSURE** | This is what the nomination and later oral-history accounts say, but it is not demonstrated by a contemporary eyewitness record reviewed here. |
| The move was completed â€œwithout any assistanceâ€ | **WRONG if read literally** | Bobâ€™s transportation role is assistance. The defensible narrower claim is that Ed reportedly loaded and unloaded the trailer without Bobâ€™s help. |
| Bob Biggers was a local man/farmer | **CONFIRMED** | Consistent across the nomination and castle account. |

Recommended wording: â€œBob Biggers hauled the loaded trailer between sites; later accounts say Ed loaded and unloaded the stones alone, usually at night.â€

### Gate repair

| Claim | Status | Finding |
|---|---|---|
| Gate dimensions: 81 Ã— 92 Ã— 21 inches | **CONFIRMED as the nominationâ€™s figures** | Stated twice in the nomination. |
| Nine-ton weight | **UNSURE** | It is the traditional/National Register figure, but no weighing or derivation was found, and it conflicts with the published dimensions and plausible material densities. |
| Central shaft/automobile axle and truck bearing | **CONFIRMED** | The nomination describes an automobile axle; later repair accounts describe a truck bearing. |
| Could be moved with one finger | **CONFIRMED historically; WRONG in present tense** | The nomination records this before the failure. â€œOne finger moves itâ€ should be â€œit was reported to turn with one finger.â€ |
| Gate stopped in 1986 | **UNSURE** | A 1990 newspaper retrospective says 1986, but Coral Castleâ€™s present website says 1984. |
| Six men and a 50-short-ton crane | **UNSURE** | A 1990 newspaper supports exactly six men and a 50-ton crane, but other accounts say five workers and a 20-ton crane; Coral Castle says only â€œsix men and a crane.â€ Treat it as a widely repeated repair account, not settled fact. [1990 Hollywood Sun](https://digitalarchives.broward.org/digital/collection/p16146coll7/id/44746/) |
| Rusted bearing caused the failure | **CONFIRMED as the reported repair finding** | Consistent across the official castle account and later descriptions. |
| Reset on July 23, 1986 | **UNSURE** | The exact date traces online mainly to Wikipedia, whose cited source is a 2006 YouTube videoâ€”not a contemporary repair record. |
| Failed again in 2005 | **UNSURE** | Repeated by Wikipedia without a distinct supporting citation. A December 2003 *Wired* report already described a recent removal and reseating, so the repair history is more complicated than the script suggests. [Wired](https://www.wired.com/2003/12/secret-energy-haunts-coral-castle/) |
| No longer rotates as smoothly | **UNSURE but plausible** | Repeated in later visitor and encyclopedia accounts; not supported here by a repair report or measurement. |

The sceneâ€™s `DOCUMENTED` label is too strong for the entire repair block. Use **â€œREPORTED: 1986 REPAIR ACCOUNTSâ€** and mark the exact July date and 2005 failure as unverified.

### Gate-volume arithmetic

| Claim | Status | Finding |
|---|---|---|
| `81 Ã— 92 Ã— 21 = 156,492 inÂ³` | **CONFIRMED** |
| `156,492 inÂ³ = 90.6 ftÂ³` | **CONFIRMED** | Exact result: 90.5625 ftÂ³. |
| Calcite density 2.71 g/cmÂ³ | **CONFIRMED** | USGS commonly uses 2.72; 2.71 is a standard mineral value. |
| Aragonite density 2.93 g/cmÂ³ | **CONFIRMED** | USGS assigns 2.93 g/cmÂ³. [USGS density discussion](https://pubs.usgs.gov/of/1987/0665/report.pdf) |
| Solid-calcite result â‰ˆ7.7 short tons | **CONFIRMED** | Approximately 7.66 tons. |
| Solid-aragonite result â‰ˆ8.3 short tons | **CONFIRMED** | Approximately 8.29 tons. |
| Thirty-percent-pore dry results â‰ˆ5.4/5.8 tons | **CONFIRMED mathematically** | These assume empty/dry pore volume. Water-filled pores would increase the mass. |
| Thirty-percent porosity is plausible | **CONFIRMED as a plausible scenario, not the gateâ€™s measured porosity** | USGS found substantial and variable porosity in hundreds of Miami Limestone samples. [USGS OFR 85-21](https://pubs.usgs.gov/of/1985/0021/report.pdf) |
| â€œEven solid aragonite, the densest the rock could beâ€ | **WRONG** | Aragonite is a useful conservative carbonate end member, but not an absolute maximum for every possible mineral inclusion or water-filled rock. Say â€œeven treating the entire rectangular volume as solid aragonite.â€ |
| â€œReal oolite is porousâ€ | **CONFIRMED** |
| â€œNine tons is probably a rounded figure, not a weighingâ€ | **UNSURE but reasonable inference** | The discrepancy makes that likely, but no record of how the nine-ton number was obtained was found. |
| â€œIf ton means metricâ€¦â€ | **WRONG / misleading** | In this American nomination, surrounded by pound figures, â€œtonâ€ almost certainly means a 2,000-pound short ton. The metric scenario adds confusion without evidentiary value. |
| Volume calculation represents the exact gate | **UNSURE** | It treats the stated maximum dimensions as a full rectangular prism. Any irregular faces, holes, or rounded edges reduce volume. |

The arithmetic is good; the interpretation needs tighter wording.

### The 1,100-ton figure

| Claim | Status | Finding |
|---|---|---|
| Coral Castle currently states 1,100 tons | **CONFIRMED** | [Official Coral Castle page](https://coralcastle.com/home/the-secrets-of-coral-castle/). |
| Wikipedia states 1,100 short tons | **CONFIRMED** |
| Wikipedia supplies a source for the total | **WRONG** | Its current 1,100-ton sentence has no citation attached. |
| The 1984 nomination gives no overall total | **CONFIRMED** |
| 1,100 is an independently established total | **UNSURE** | No inventory, survey, scale record, or documented calculation was located. |
| â€œThe castleâ€™s own figureâ€ | **CONFIRMED only in the sense that the present operator promotes it** | It should not imply that Leedskalnin or an engineer calculated it. |
| First estimator not found | **CONFIRMED as the research result** | The search did not identify one. |
| Carroll A. Lake may be the source of exactly 1,100 tons | **WRONG** | Lakeâ€™s mid-1950s account says â€œover 1000 tonsâ€; another passage says roughly 1,000 tons in the wall/castle plus nearly half again in furniture. It does not provide a clean 1,100-ton calculation and is internally inconsistent. [Lake text](https://magneticuniverse.com/uploads/FileUpload/31/21d96d1d17317ae587ef3fa556b1c2.pdf) |
| Earliest exact 1,100-ton estimate | **UNSURE** | Exact â€œ1,100â€ appears in later promotional material, but the first use could not be dated. An undated/modern-scanned Coral Castle brochure uses it; a searchable 1998 Usenet repost also contains it. Neither identifies an estimator. |

Best conclusion: **Carroll A. Lake is the earliest quantitative lead locatedâ€”â€œover 1,000 tons,â€ circa the mid-1950sâ€”but he is not shown to be the originator of the exact 1,100-ton figure.**

### Block and tackle and lever calculations

| Claim | Status | Finding |
|---|---|---|
| Ideal mechanical advantage equals the supporting rope segments | **CONFIRMED for a simple block-and-tackle correctly rigged** |
| 20,000 Ã· 6 = 3,333 lb | **CONFIRMED** |
| Two properly compounded 6:1 systems produce ideal 36:1 | **CONFIRMED conditionally** | They must actually be cascaded so one system pulls the other; merely placing two tackle sets together does not automatically multiply them. |
| 20,000 Ã· 36 â‰ˆ556 lb | **CONFIRMED** |
| Adding an ideal 5:1 winch gives total 180:1 and â‰ˆ111 lb input | **CONFIRMED conditionally** | This is an ideal speed/force-ratio example, not evidence about Edâ€™s equipment. |
| â€œWhich one person can pullâ€ | **UNSURE** | A 111-pound sustained pull is substantial; friction, rope stiffness, sheave losses, startup loads, structure stability, and safety margins could raise it greatly. |
| â€œ180 ft of rope per 1 ft liftâ€ after adding the winch | **WRONG** | The 36:1 tackle requires roughly 36 feet of tackle-rope travel per foot of lift. A 5:1 winch makes the operatorâ€™s handle/input travel roughly five times the drum-rope travelâ€”about 180 feet of equivalent input motionâ€”not 180 feet of rope hauled through the tackle. [Pulley-system explanation](https://www.cmcpro.com/pulleys-and-mechanical-advantage-systems/) |
| Friction is ignored | **CONFIRMED and properly disclosed** |
| 9:1 lever: `100 lb Ã— 9 ft = 900 lb Ã— 1 ft` | **CONFIRMED as ideal statics** |
| That example can raise the preceding ten-ton block | **WRONG if implied** | Nine hundred pounds of ideal output cannot raise a 20,000-pound load. The lever drawing must be presented as an unrelated principle example or use a much larger ratio/effort. |
| â€œRaise an inch, crib, repeatâ€ | **CONFIRMED as a real technique in general** | It does not prove Leedskalnin used that exact procedure on the largest blocks. |

## Remaining narration and screen claims

| Scene/claim | Status | Finding |
|---|---|---|
| **s1:** Leedskalnin lived 1887â€“1951 | **CONFIRMED** |
| He worked on the structures from 1923 until his death | **CONFIRMED broadly** |
| He alone cut, moved, and erected every stone | **UNSURE** | Widely attested, including affidavits, but not proved lift-by-lift; Bob Biggers assisted with transport. |
| **s2:** Born in Latvia in 1887 | **CONFIRMED** |
| Engagement at about 26 to Agnes, ten years younger; she ended it | **CONFIRMED only as the 1984 nominationâ€™s account** |
| He called the real Agnes â€œSweet Sixteenâ€ | **UNSURE** | His writing uses â€œSweet Sixteen,â€ but whether it identifies the historically disputed fiancÃ©e is uncertain. |
| Work across North America, illness, early-1920s Florida arrival | **CONFIRMED as the nominationâ€™s biography; independently incomplete** |
| **s3:** Scuff/Skuvst spellings and conflicting Latvian name/age | **CONFIRMED** |
| The love-story motive comes from later tellings | **CONFIRMED** |
| **s4:** 1923 purchase of one acre for $12 | **CONFIRMED by the nominationâ€™s deed citation** |
| Ground was oolitic limestone called coral rock | **CONFIRMED** |
| Shed, tower, wall, furniture, astronomical pieces | **CONFIRMED broadly** |
| On-screen â€œsundial?â€ at the original site | **UNSURE** | Appropriately marked with a question mark. |
| **s6:** Polaris 40,000 lb; quarter moons 36,000 each; full-moon fountain 46,000; obelisk 57,000; north-wall sculpture 30 tons | **CONFIRMED as figures printed in the nomination** | They are not independently verified measurements. |
| Polaris slab was 25 feet tall | **CONFIRMED as the formâ€™s figure** |
| Wall blocks 8 Ã— 4 Ã— 3 feet, â€œseveral tonsâ€ | **CONFIRMED as the formâ€™s description** |
| Mars and Saturn 36,000 lb each | **CONFIRMED as the formâ€™s figures** |
| **s10:** Tools listed in the form | **CONFIRMED** |
| Some quarrying/sculpting tools fashioned from old automobile parts | **CONFIRMED as the formâ€™s account** |
| Historical photographs show tall wooden tripod-like frames and suspended lifting gear | **CONFIRMED** | Florida Memory catalogs a circa-1936 photograph with hoisting equipment. [Florida Memory results](https://floridamemory.com/find?advanced%5B0%5D%5Belement_id%5D=240&advanced%5B0%5D%5Bjoiner%5D=and&advanced%5B0%5D%5Bterms%5D=11&advanced%5B0%5D%5Btype%5D=is+exactly&advanced%5B1%5D%5Belement_id%5D=49&advanced%5B1%5D%5Bjoiner%5D=and&advanced%5B1%5D%5Bterms%5D=Historic+sites--Florida--Homestead&advanced%5B1%5D%5Btype%5D=is+exactly&layout=1&order=d&query=&sort=43) |
| Rockgatepark.com is â€œthe castleâ€™s archiveâ€ | **WRONG** | The site explicitly says it is an independent archive, not affiliated with Coral Castle. [Rock Gate Park notice](https://www.rockgatepark.com/) |
| No detailed record of the exact rig configuration/procedure | **CONFIRMED as the independent archiveâ€™s conclusion** | Avoid presenting that conclusion as an official institutional finding. |
| **s13:** Over 250 affidavits were collected in 1955 | **CONFIRMED** |
| Julius Levin collected them | **CONFIRMED** | The nominationâ€™s pronoun refers back to Levin. |
| Levin was the then owner, having purchased in 1953 | **CONFIRMED by the nomination** |
| Affiants were Homestead-area residents acquainted with Ed | **CONFIRMED** |
| Affidavits said he worked without other individuals and with simple hand tools | **CONFIRMED as their sworn wording** |
| They were notarized by Bodil K. Lowe | **CONFIRMED** |
| The nomination quotes no named witness to a specific largest-block lift | **CONFIRMED** |
| The affidavits prove every large lift was solo | **UNSURE** | Their generic form language does not identify which work each signer personally observed. |
| **s14:** â€œPyramid buildersâ€ and â€œlaws of leverage and weightâ€ | **CONFIRMED as the nominationâ€™s paraphrase** | Correctly not presented as a verbatim Ed quotation. |
| No Leedskalnin-authored document describes the lifting process | **CONFIRMED within the reviewed writings** |
| *A Book in Every Home* â€” 1936 | **CONFIRMED** |
| *Magnetic Current* â€” August 1945, Franklin Press | **CONFIRMED** | The surviving text itself says copyright August 1945. [Text](https://www.leedskalnin.com/Leedskalnins-Writings-MAGNETIC-CURRENT.html) |
| *Mineral, Vegetable and Animal Life* â€” October 1945, Franklin Press | **CONFIRMED** |
| *Magnetic Current* concerns magnets/electricity | **CONFIRMED** |
| None of those works explains how the stones were lifted | **CONFIRMED** |
| **s15:** Extraterrestrial and gravity/weightlessness stories existed by 1984 | **CONFIRMED** | The nomination records both. |
| Sound levitation was already among the theories by 1984 | **UNSURE** | It is not one of the theories named in the nomination. |
| Magnetism â€œcancelled weightâ€ is what his pamphlets claim | **WRONG** | The pamphlets advance unconventional magnetic theories, but they do not state a stone-lifting or weight-cancellation method. |
| Floating-stone stories are secondhand | **CONFIRMED** |
| No measurement, recording, or physical trace was found for exotic lifting | **CONFIRMED within this reviewâ€™s evidence** |
| â€œNot established, not impossible/not ruled outâ€ | **WRONG / editorially misleading** | Absence of proof does not place conventional rigging and extraordinary levitation on equal evidentiary footing. Say â€œunsupported; available physical evidence points to conventional rigging.â€ |
| **s16:** â€œDocumented: the datesâ€ | **WRONG** | The dates conflict materially. |
| â€œDocumented: the moveâ€ | **UNSURE as phrased** | The relocation is established, but its exact schedule and the solo-loading claim are not. |
| â€œDocumented: the formâ€™s weightsâ€ | **CONFIRMED only if explicitly meaning the form prints those estimates** |
| â€œDocumented: the 1986 repairâ€ | **WRONG / too strong** | Important details conflict or derive from poorly sourced later accounts. |
| Worked alone / pyramid knowledge / 1,100 tons are claims | **CONFIRMED categorization** |
| Gateâ€™s true weight is unsettled | **CONFIRMED categorization** |
| Exact largest-block lifting procedures are unknown | **CONFIRMED, although conventional lifting equipment is documented** |
| **s17:** Patient work and simple machines fit the evidence | **CONFIRMED as a reasonable inference** |
| Stranger mechanisms remain equally viable | **WRONG / unsupported framing** |

## SOURCES.md and end-card corrections

- **CONFIRMED:** Nomination prepared by Maria Temkin and Michael Zimny on April 2, 1984; listed May 10, 1984; reference 84000840. The 2011 correspondence requests and supports changing the official name from Rock Gate to Coral Castle. [NPS record](https://npgallery.nps.gov/AssetDetail/1ed2ccd0-b692-42dc-b28d-1227c1a23407/)

- **CONFIRMED:** The nomination title fields read historic â€œRock Gate (Edâ€™s Place)â€ and common â€œCoral Castle.â€

- **WRONG:** â€œWikipedia â€¦ 1986 repair, 2005 failureâ€ on the end card makes Wikipedia look like adequate verification. Its exact July-date citation is merely a 2006 YouTube upload, and the 2005 sentence has no separate citation.

- **WRONG:** `rockgatepark.com/the-tools` is described in narration as â€œthe castleâ€™s archive.â€ It is independent and expressly unaffiliated.

- **UNSURE:** Florida Memoryâ€™s circa-1936 catalog date for Homestead hoisting photographs conflicts with the stronger evidence placing relocation activity in 1939. The photograph exists; the date/location metadata should be qualified.

- **WRONG:** `Status as of October 2026` suggests a live status check of every physical feature. The audit did not establish the gateâ€™s current operational state.

## Recommended minimum revisions

1. Replace the move scene with the 1936 land-purchase/1939 active-move chronology and explicitly call the formâ€™s 1937 entry inconsistent.
2. Say Bob Biggers hauled the trailer; qualify the solo loading/unloading as a later account.
3. Relabel the gate repair **REPORTED**, omit the exact July 23 date and 2005 failure unless a contemporary repair record is obtained.
4. Change â€œone finger moves itâ€ to historical past tense.
5. Preserve the gate calculation but say â€œfull rectangular solid-aragonite upper-case modelâ€; remove the metric-ton aside.
6. Change â€œ180 feet of ropeâ€ to â€œ36 feet of tackle-rope travel, or about 180 feet of idealized operator-input travel after a 5:1 winch.â€
7. Identify Rock Gate Park as an independent website.
8. Replace â€œnot ruled outâ€ with â€œunsupported; the surviving equipment and photographs support conventional mechanical methods.â€
9. Describe all listed stone weights as **the nominationâ€™s published estimates**, not verified weights.
10. Keep 1,100 tons explicitly untraced; note that Carroll Lake supplied an earlier â€œover 1,000 tonsâ€ claim but not the exact 1,100 figure.

**Verdict: The episodeâ€™s core history is usable, but it needs revision before release because several disputed or promotional claims are presently labeled â€œdocumented,â€ and one mechanical calculation is materially misstated.**


--- script revised matches ---
ep_body.py-61-    yy = y0 + 60 + len(lines) * sz * 1.05 + 40
ep_body.py-62-    mono(cv, HEAD[0], yy, 'the 1,100 is the castle\'s own figure: we check it', 24, DIM, ease((t - 1.5) / 1.0))
ep_body.py-63-    ty = yy + 70
ep_body.py-64-    x = HEAD[0]
ep_body.py:65:    for i, (lab, col, f) in enumerate((('DOCUMENTED', MINT, 0.35), ('CLAIMED', VIO, 0.5), ('NOT ESTABLISHED', ROSE, 0.7), ('UNKNOWN', ROSE, 0.88))):
ep_body.py-66-        aa = ap(t, 's1', f, 0.8)
ep_body.py-67-        if PORT:
ep_body.py-68-            tag(cv, HEAD[0], ty + i * 62, lab, col, aa)
ep_body.py-69-        else:
--
ep_body.py-95-            cv.para(ly + 50, py + 80, txt, 'sans', 32, TXT, 820, 1.2, 'l', a)
ep_body.py-96-
ep_body.py-97-def sc_man(cv, t, p):
ep_body.py-98-    night(cv, t, 0.5)
ep_body.py:99:    tag(cv, CONT[0], CONT[1] - 40, 'REPORTED: AS TOLD IN THE NRHP FORM, 1984', CYAN, ease(t / 0.8))
ep_body.py-100-    evs = [('1887', 'born in Latvia', MINT, 0.18), ('about 1913', 'engaged at about 26; the bride calls off the wedding', MINT, 0.38),
ep_body.py-101-           ('1910s', 'jobs across North America, a lumber camp, poor health', MINT, 0.66), ('early 1920s', 'reaches Florida City', MINT, 0.86)]
ep_body.py-102-    timeline(cv, evs, t, 's2')
ep_body.py-103-
--
ep_body.py-113-          [ap(t, 's3', 0.0, 0.8), ap(t, 's3', 0.05, 0.8), ap(t, 's3', 0.1, 0.8)], 32 if L else 30, 14, aw - 60)
ep_body.py-114-    tag(cv, ax + 30, ay + ah - 70, 'CLAIMED: TOLD LATER', VIO, a1, 22)
ep_body.py-115-    a2 = ap(t, 's3', 0.18); card(cv, bx, by, bw, bh, ROSE, a2)
ep_body.py-116-    mono(cv, bx + 30, by + 24, 'THE NAME', 22, ROSE, a2)
ep_body.py:117:    stack(cv, bx + 30, by + 70, ['NRHP 1984 form: "Scuff", footnote also gives "Skuvst"', 'one Latvian account: a different name and age'],
ep_body.py-118-          [ap(t, 's3', 0.28, 0.8), ap(t, 's3', 0.45, 0.8)], 32 if L else 30, 14, bw - 60)
ep_body.py-119-    tag(cv, bx + 30, by + bh - 70, 'NOT SETTLED', ROSE, ap(t, 's3', 0.6), 22)
ep_body.py-120-
ep_body.py-121-def sc_site(cv, t, p):
ep_body.py-122-    night(cv, t, 0.5)
ep_body.py-123-    x0, y0, x1, y1 = CONT
ep_body.py:124:    tag(cv, x0, y0 - 40, 'DOCUMENTED: NRHP FORM, 1984', MINT, ease(t / 0.8))
ep_body.py-125-    # schematic plan (not to scale)
ep_body.py-126-    if L: px, py, pw, ph = x0 + 40, y0 + 60, 640, 420
ep_body.py-127-    else: px, py, pw, ph = x0 + 20, y0 + 20, 700, 420
ep_body.py-128-    a = ease(t / 1.2)
--
ep_body.py-164-    cv.circ((tx - 30, ly - 8), 10, mix(TXT, BG, a)); cv.circ((tx + 50, ly - 8), 10, mix(TXT, BG, a))
ep_body.py-165-    if loaded: stone(cv, tx + 14, ly - 82, tx + 76, ly - 40, a, CYAN)
ep_body.py-166-    # date table
ep_body.py-167-    ty = ly + (130 if L else 130)
ep_body.py:168:    rows = [('by 1936', 'buys 10 acres at Homestead (castle chronology)', 0.2), ('1937', 'the 1984 NRHP form: "moved date 1937"', 0.35), ('1939', 'obelisk: "Moved in 1939"; land clearing from May 1939', 0.5),
ep_body.py:169:            ('hauling', 'Bob Biggers, a farmer, hauls the stones (form: his truck; castle: a trailer)', 0.7), ('loading', 'Ed loads and unloads alone, at night (form and later accounts)', 0.88)]
ep_body.py-170-    for i, (k, v, f) in enumerate(rows):
ep_body.py-171-        aa = ap(t, 's5', f); yy = ty + i * (62 if L else 100)
ep_body.py-172-        if aa <= 0: continue
ep_body.py-173-        mono(cv, x0 + 20, yy, k, 28, CYAN, aa)
ep_body.py-174-        if L: cv.text((x0 + 250, yy), v, 'sans', 32, TXT, 'la', aa)
ep_body.py-175-        else: cv.para(x0 + 20, yy + 36, v, 'sans', 30, TXT, 900, 1.2, 'l', aa)
ep_body.py-176-
ep_body.py:177:def sc_weights(cv, t, p):
ep_body.py-178-    night(cv, t, 0.4)
ep_body.py-179-    x0, y0, x1, y1 = CONT
ep_body.py:180:    tag(cv, x0, y0 - 40, 'REPORTED: WEIGHTS PRINTED IN THE NRHP FORM, 1984', CYAN, ease(t / 0.8), 20)
ep_body.py-181-    items = [('Polaris sighting slab', 20, 0.12), ('each quarter moon', 18, 0.28), ('full moon fountain', 23, 0.4), ('obelisk', 28.5, 0.55), ('north-wall sculpture', 30, 0.78)]
ep_body.py-182-    lw = 430 if L else 0
ep_body.py-183-    bx0 = x0 + (lw + 30 if L else 0); bmax = (x1 - bx0 - 240) if L else (x1 - x0 - 380)
ep_body.py-184-    rh = 96 if L else 140
--
ep_body.py-201-    big(cv, x0, y0 + 10, '1,100', 220 if L else 200, TXT, a)
ep_body.py-202-    mono(cv, x0 + (640 if L else 20), y0 + (150 if L else 270), 'short tons: the castle\'s own total', 30, VIO, a)
ep_body.py-203-    tag(cv, x0 + (640 if L else 20), y0 + (210 if L else 330), 'CLAIMED', VIO, ap(t, 's7', 0.3)); tag(cv, x0 + (800 if L else 200), y0 + (210 if L else 330), 'SOURCE UNTRACED', ROSE, ap(t, 's7', 0.55))
ep_body.py-204-    ty = y0 + (330 if L else 460)
ep_body.py:205:    rows = [('coralcastle.com', 'states "1,100 tons"; no estimator named', 0.15), ('Wikipedia', '1,100 short tons; figure not attributed', 0.3), ('NRHP form, 1984', 'lists pieces "up to 30 tons"; no total', 0.45), ('C. A. Lake, 1950s', 'adds walls and tower: "over 1000 tons"', 0.62), ('first use of "1,100"', 'not found', 0.8)]
ep_body.py-206-    for i, (k, v, f) in enumerate(rows):
ep_body.py-207-        aa = ap(t, 's7', f); yy = ty + i * (62 if L else 100)
ep_body.py-208-        hline(cv, x0, x1, yy - 10, INK2, aa, 1)
ep_body.py-209-        mono(cv, x0 + 10, yy + 4, k, 26, CYAN if i < 4 else ROSE, aa)
ep_body.py-210-        if L: cv.text((x0 + 380, yy), v, 'sans', 32, TXT if i < 4 else ROSE, 'la', aa)
ep_body.py-211-        else: cv.text((x0 + 10, yy + 40), v, 'sans', 32, TXT if i < 4 else ROSE, 'la', aa)
ep_body.py-212-
ep_body.py:213:def sc_gate(cv, t, p):
ep_body.py-214-    night(cv, t, 0.4)
ep_body.py-215-    x0, y0, x1, y1 = CONT
ep_body.py-216-    tag(cv, x0, y0 - 40, 'DIMENSIONS: NRHP FORM', MINT, ease(t / 0.8)); tag(cv, x0 + 330, y0 - 40, 'REPAIR: REPORTED', CYAN, ap(t, 's8', 0.5))
ep_body.py-217-    sc = 3.6 if L else 3.3
--
ep_body.py-234-    cv.line([(tvx - 150, tvy), (tvx - 100, tvy)], mix(DIM, BG, a), 8); cv.line([(tvx + 100, tvy), (tvx + 150, tvy)], mix(DIM, BG, a), 8)
ep_body.py-235-    r = 100
ep_body.py-236-    cv.line([(tvx - r * math.cos(ang), tvy - r * math.sin(ang)), (tvx + r * math.cos(ang), tvy + r * math.sin(ang))], mix(CYAN, BG, ga), 12)
ep_body.py-237-    cv.circ((tvx, tvy), 9, mix(VIO, BG, sa)); cv.text((tvx, tvy + 130), 'top view: swings on its center', 'mono', 18, DIM, 'ma', ga)
ep_body.py:238:    # 1986 facts
ep_body.py-239-    fy = ey + 20 + gh + 130
ep_body.py:240:    rows = [('"nine ton" (form): see the next check', 0.35, MINT), ('reported to turn with one finger (form, 1984)', 0.45, MINT), ('mid-1980s: stopped turning, 1984 or 1986 (sources differ)', 0.62, CYAN), ('six men and a crane lifted it out (50-ton in one account); rusted truck bearing replaced', 0.8, CYAN)]
ep_body.py-241-    fx = x0 + (1130 if L else 20); yy = (ey + 20) if L else fy
ep_body.py-242-    for i, (txt, f, col) in enumerate(rows):
ep_body.py-243-        aa = ap(t, 's8', f)
ep_body.py-244-        if aa <= 0: continue
--
ep_body.py-247-
ep_body.py-248-def sc_check(cv, t, p):
ep_body.py-249-    night(cv, t, 0.4)
ep_body.py-250-    x0, y0, x1, y1 = CONT
ep_body.py:251:    tag(cv, x0, y0 - 40, 'OUR ARITHMETIC', CYAN, ease(t / 0.8)); tag(cv, x0 + 270, y0 - 40, 'NOT SETTLED: GATE WEIGHT', ROSE, ap(t, 's9', 0.6))
ep_body.py-252-    vol_in3 = 81 * 92 * 21; vft = vol_in3 / 1728.0
ep_body.py:253:    rows = [('calcite, solid (2.71 g/cm3)', 2.71, 0.0), ('aragonite, solid (2.93 g/cm3)', 2.93, 0.0), ('aragonite, 30% pore space', 2.93 * 0.7, 0.0), ('calcite, 30% pore space', 2.71 * 0.7, 0.0)]
ep_body.py-254-    a0 = ap(t, 's9', 0.05)
ep_body.py-255-    mono(cv, x0, y0 + 10, f'81 x 92 x 21 in = {vol_in3:,} cubic in = {vft:.1f} cubic ft', 30 if L else 26, TXT, a0)
ep_body.py:256:    mono(cv, x0, y0 + 56, '(1 g/cm3 = 62.43 lb/ft3; weight = volume x density)', 20, DIM, a0)
ep_body.py-257-    order = [1, 0, 2, 3]; fr = [0.3, 0.38, 0.55, 0.62]
ep_body.py-258-    scale_max = 10.0; bx0 = x0 + (500 if L else 0); bw = (x1 - bx0 - 150) if L else (x1 - x0 - 200)
ep_body.py-259-    for i, k in enumerate(order):
ep_body.py-260-        nm, d, _ = rows[k]; aa = ap(t, 's9', fr[i]); tons = vft * d * 62.428 / 2000.0
--
ep_body.py-278-    lift = 0.35 + 0.3 * math.sin(t * 0.4)
ep_body.py-279-    if L: tripod(cv, x0 + 330, y0 + 570, 520, ease(t / 1.0), lift, math.sin(t * 0.6))
ep_body.py-280-    else: tripod(cv, x1 - 200, y0 + 330, 300, ease(t / 1.0), lift, math.sin(t * 0.6))
ep_body.py-281-    tx = x0 + (720 if L else 0); ty = y0 + (0 if L else 360)
ep_body.py:282:    rows = [('DOCUMENTED', MINT, 'tools on display (NRHP 1984): block and tackle ("metal fall"), rollers, jacks, wedges, slings, cables, sledges, chisels; some made from old car parts', 0.15),
ep_body.py-283-            ('DOCUMENTED', MINT, 'old photographs show tall wooden tripods with chains, and a chain hoist', 0.5),
ep_body.py:284:            ('UNKNOWN', ROSE, 'exact rig set-up and procedures: "no detailed records" (Rock Gate Park, an independent archive site)', 0.78)]
ep_body.py-285-    yy = ty
ep_body.py-286-    for lab, col, txt, f in rows:
ep_body.py-287-        aa = ap(t, 's10', f)
ep_body.py-288-        if aa > 0:
--
ep_body.py-293-def pulley(cv, cx, cy, w, a, col):
ep_body.py-294-    cv.rect((cx - w / 2, cy - 22, cx + w / 2, cy + 22), mix(INK2, BG, a)); cv.outline((cx - w / 2, cy - 22, cx + w / 2, cy + 22), mix(col, BG, a), 2)
ep_body.py-295-    for k in range(3): cv.ring((cx - w / 3 + k * w / 3, cy), 12, mix(col, BG, a), 2)
ep_body.py-296-
ep_body.py:297:def sc_tackle(cv, t, p):
ep_body.py-298-    night(cv, t, 0.3)
ep_body.py-299-    x0, y0, x1, y1 = CONT
ep_body.py-300-    tag(cv, x0, y0 - 40, 'ILLUSTRATION: IDEAL, NO FRICTION', CYAN, ease(t / 0.8), 20)
ep_body.py-301-    a = ease(t / 1.0)
--
ep_body.py-314-    stone(cv, dx - 70, boty + 70, dx + 70, boty + 150, a, CYAN, '10 tons')
ep_body.py-315-    cv.line([(dx, dy - 40), (dx, topy - 22)], mix(DIM, BG, a), 4)
ep_body.py-316-    sx = x0 + (560 if L else 0); sy = y0 + (20 if L else 600)
ep_body.py-317-    rows = [('load: 10 short tons = 20,000 lb', 0.0, TXT), ('6 rope segments:  20,000 / 6 = 3,333 lb pull', 0.18, TXT), ('two sets, 6 x 6 = 36:  20,000 / 36 = 556 lb', 0.4, TXT),
ep_body.py:318:            ('+ 5:1 winch, 36 x 5 = 180:  20,000 / 180 = 111 lb', 0.58, MINT), ('cost: 36 ft of tackle rope per 1 ft of lift; ~180 ft of winch-handle travel', 0.78, ROSE)]
ep_body.py-319-    for i, (txt, f, col) in enumerate(rows):
ep_body.py-320-        aa = ap(t, 's11', f)
ep_body.py-321-        if aa <= 0: continue
ep_body.py-322-        yy = sy + i * (84 if L else 56)
--
ep_body.py-376-    a = ease(t / 1.0)
ep_body.py-377-    tag(cv, x0, y0 - 40, 'CLAIMED', VIO, a)
ep_body.py-378-    qa = ap(t, 's14', 0.1)
ep_body.py-379-    cv.rect((x0, y0 + 10, x0 + 5, y0 + (330 if L else 420)), mix(VIO, BG, qa))
ep_body.py:380:    yy = cv.para(x0 + 30, y0 + 10, '"the methods used by the pyramid builders, the practical knowledge of the laws of leverage and weight"', 'light', 54 if L else 50, TXT, (x1 - x0 - 60) * (0.8 if L else 1), 1.2, 'l', qa)
ep_body.py:381:    mono(cv, x0 + 30, yy + 10, 'Ed\'s reply to how he did it, as paraphrased in the NRHP form, 1984', 20, DIM, qa)
ep_body.py-382-    py0 = y0 + (400 if L else 520)
ep_body.py-383-    mono(cv, x0, py0, 'PAMPHLETS (he sold these)', 22, CYAN, ap(t, 's14', 0.55))
ep_body.py:384:    ps = [('1936', 'A Book in Every Home', 0.62), ('Aug 1945', 'Magnetic Current', 0.76), ('Oct 1945', 'Mineral, Vegetable and Animal Life', 0.88)]
ep_body.py-385-    for i, (yr, nm, f) in enumerate(ps):
ep_body.py-386-        aa = ap(t, 's14', f); yy2 = py0 + 46 + i * 56
ep_body.py-387-        mono(cv, x0, yy2, yr, 28, MINT, aa); cv.text((x0 + 200, yy2 - 2), nm, 'sans', 34, TXT, 'la', aa)
ep_body.py-388-    mono(cv, x0, py0 + 46 + 3 * 56 + 6, 'we found none that describes how he lifted the blocks', 22, ROSE, ap(t, 's14', 0.95))
ep_body.py-389-
ep_body.py:390:def sc_theories(cv, t, p):
ep_body.py-391-    night(cv, t, 0.4)
ep_body.py-392-    x0, y0, x1, y1 = CONT
ep_body.py:393:    items = [('sound', 'sound levitates the stone', 0.12), ('magnetism', 'the pamphlets do not say this', 0.3), ('beyond Earth', 'help, or mastered gravity: in the 1984 form', 0.48)]
ep_body.py-394-    for i, (a1, a2, f) in enumerate(items):
ep_body.py-395-        aa = ap(t, 's15', f)
ep_body.py-396-        if aa <= 0: continue
ep_body.py-397-        if L:
--
ep_body.py-401-        card(cv, cx, cy, cw, ch, ROSE, aa)
ep_body.py-402-        big(cv, cx + 28, cy + 24, a1, 48 if L else 46, TXT, aa)
ep_body.py-403-        cv.para(cx + 28, cy + 96, a2, 'sans', 28, DIM, cw - 56, 1.2, 'l', aa)
ep_body.py-404-        if L:
ep_body.py:405:            tag(cv, cx + 28, cy + ch - 120, 'NOT ESTABLISHED', ROSE, aa, 20); mono(cv, cx + 28, cy + ch - 62, 'evidence found: none', 22, TXT, aa)
ep_body.py-406-        else:
ep_body.py:407:            tag(cv, cx + 28, cy + ch - 70, 'NOT ESTABLISHED', ROSE, aa, 20); mono(cv, cx + 330, cy + ch - 62, 'evidence found: none', 22, TXT, aa)
ep_body.py-408-    ub = ap(t, 's15', 0.72); yb = y0 + (390 if L else 740)
ep_body.py-409-    big(cv, x0, yb, 'absence of evidence is not proof of absence.', 44 if L else 38, TXT, ub)
ep_body.py:410:    mono(cv, x0, yb + 70, 'floating-stone stories: secondhand. not established is not the same as impossible.', 22, DIM, ap(t, 's15', 0.85))
ep_body.py-411-
ep_body.py:412:LEDGER = [('DOCUMENTED', MINT, 'land purchase, the form\'s printed weights, the tool list, photographs of hoisting gear', 0.2),
ep_body.py:413:          ('REPORTED', CYAN, 'conflicting details: the move dates, the gate repair', 0.4),
ep_body.py-414-          ('CLAIMED', VIO, 'worked alone  /  pyramid builders\' methods  /  1,100 tons', 0.58),
ep_body.py:415:          ('NOT SETTLED', ROSE, 'the gate\'s true weight', 0.72),
ep_body.py-416-          ('UNKNOWN', ROSE, 'how the largest blocks were raised and set, alone', 0.85)]
ep_body.py:417:def sc_ledger(cv, t, p):
ep_body.py-418-    night(cv, t, 0.3)
ep_body.py-419-    x0, y0, x1, y1 = CONT
ep_body.py:420:    big(cv, x0, y0 + 10, 'the ledger', 56 if PORT else 64, TXT, ease(t / 1.0))
ep_body.py-421-    step = 150 if PORT else 100
ep_body.py:422:    for i, (st, col, txt, f) in enumerate(LEDGER):
ep_body.py-423-        a = ap(t, 's16', f)
ep_body.py-424-        if a <= 0: continue
ep_body.py-425-        yy = y0 + 110 + i * step
ep_body.py-426-        hline(cv, x0, x1, yy, INK2, a, 1)
--
ep_body.py-432-    night(cv, t, 0.8)
ep_body.py-433-    x0, y0, x1, y1 = CONT
ep_body.py-434-    a = ease(t / 1.0)
ep_body.py-435-    sz = 120 if L else 100
ep_body.py:436:    big(cv, x0, y0 + 20, 'not established.', sz, TXT, ap(t, 's17', 0.45))
ep_body.py:437:    big(cv, x0, y0 + 20 + sz * 1.2, 'not ruled out.', sz, TXT, ap(t, 's17', 0.62))
ep_body.py:438:    tag(cv, x0, y0 + 20 + sz * 2.6, 'NOT ESTABLISHED', ROSE, ap(t, 's17', 0.5), 24); tag(cv, x0 + 330, y0 + 20 + sz * 2.6, 'NOT RULED OUT', MINT, ap(t, 's17', 0.68), 24)
ep_body.py-439-    big(cv, x0, y0 + 20 + sz * 3.4, 'someone watching this might be the one who works it out.', 36 if L else 34, CYAN, ap(t, 's17', 0.82, 1.2))
ep_body.py-440-    if L: tripod(cv, 1560, 830, 380, 0.5 * a, 0.2 + 0.1 * math.sin(t * 0.5), math.sin(t * 0.6))
ep_body.py-441-
ep_body.py-442-SOURCES = [
ep_body.py:443:    'NPS: National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed\'s Place)" / Coral Castle. Florida Division of Archives, 2 Apr 1984; listed 10 May 1984; renamed Coral Castle 2011 (npgallery.nps.gov, asset 1ed2ccd0-b692-42dc-b28d-1227c1a23407)',
ep_body.py:444:    'coralcastle.com: "The Secrets of Coral Castle" (1,100 tons) and "About Edward Leedskalnin" (chronology, Bob Biggers, heaviest piece over 21 tons, gate stopped 1984)',
ep_body.py:445:    'C. A. Lake, Leedskalnin biography (1950s, engineer): "over 1000 tons". Wikipedia "Coral Castle" / "Edward Leedskalnin" (1,100 short tons, unattributed; repair accounts; read 2026-10-13)',
ep_body.py:446:    'rockgatepark.com/the-tools (independent archive, not affiliated with the castle): hoisting-gear photographs; "no detailed records". Also Florida Memory item 328424. No photographs are used here: every picture is drawn.',
ep_body.py-447-    'Further reading: P. A. Hancock, "The making of a modern myth: Edward Leedskalnin and the Coral Castle", Skeptic 18(1), 2013',
ep_body.py:448:    'Our arithmetic (gate volume, density, block and tackle, lever): standard formulas; calcite 2.71, aragonite 2.93 g/cm3; 30% porosity assumed. Details: SOURCES.md']
ep_body.py-449-def sc_end(cv, t, p):
ep_body.py-450-    night(cv, t, 0.7)
ep_body.py-451-    a = ease(t / 1.0)
ep_body.py-452-    if L: tripod(cv, 1620, 700, 300, 0.35 * a, 0.2, 0.0)
--
ep_body.py-461-
ep_body.py-462-# (segment id, headline, source line, draw fn)
ep_body.py-463-SCENES = [
ep_body.py-464-    ('s1', None, 'Edward Leedskalnin, 1887-1951. 1,100 tons: castle figure, source untraced', sc_title),
ep_body.py:465:    ('s2', 'a man from latvia', 'NRHP nomination form, Florida Division of Archives, 1984', sc_man),
ep_body.py:466:    ('s3', 'a love story, and its gaps', 'NRHP form 1984 (name spellings, footnote 2); Wikipedia "Edward Leedskalnin"', sc_agnes),
ep_body.py:467:    ('s4', 'ed\'s place, 1923', 'NRHP form 1984; Dade County Deed Book 1546, p. 8', sc_site),
ep_body.py:468:    ('s5', 'the move to homestead', 'NRHP form 1984 (sec. 7, 8); obelisk inscription; coralcastle.com chronology', sc_move),
ep_body.py:469:    ('s6', 'what the form weighs', 'NRHP form 1984: weights in pounds, converted here', sc_weights),
ep_body.py:470:    ('s7', 'the 1,100-ton total', 'coralcastle.com; Wikipedia; NRHP form 1984; C. A. Lake (1950s)', sc_total),
ep_body.py:471:    ('s8', 'the gate', 'NRHP form 1984; coralcastle.com; Wikipedia "Coral Castle" (repair accounts conflict)', sc_gate),
ep_body.py-472-    ('s9', 'a check anyone can do', 'Volume x density. Our arithmetic, assumptions on screen', sc_check),
ep_body.py:473:    ('s10', 'the tools', 'NRHP form 1984 (tool list); rockgatepark.com (independent archive)', sc_tools),
ep_body.py:474:    ('s11', 'block and tackle', 'Ideal mechanical advantage = rope segments. Worked example, not his rig', sc_tackle),
ep_body.py-475-    ('s12', 'the lever', 'Law of the lever. Worked example, not his method', sc_lever),
ep_body.py:476:    ('s13', 'what no one has documented', 'NRHP form 1984 quoting the 1955 affidavits', sc_affidavit),
ep_body.py:477:    ('s14', 'what he said', 'NRHP form 1984 (paraphrase of his reply; pamphlet list)', sc_words),
ep_body.py:478:    ('s15', 'popular theories', 'NRHP form 1984 (extraterrestrial, gravity); thisunexplaineduniverse.com; the pamphlets', sc_theories),
ep_body.py:479:    ('s16', None, 'Status as of October 2026', sc_ledger),
ep_body.py-480-    ('s17', None, None, sc_close),
ep_body.py-481-    ('s18', None, None, sc_end),
ep_body.py-482-]
ep_body.py-483-
--
script.json-4-  "text": "From 1923 until his death in 1951, one man in southern Florida cut, moved and stood up stone blocks that weigh many tons each. His name was Edward Leedskalnin. The castle's own figure for the total is about eleven hundred tons. Here is what is documented, what he claimed, what people have guessed, and what is still unknown."
script.json-5- },
script.json-6- {
script.json-7-  "id": "s2",
script.json:8:  "text": "Start with the man. Edward Leedskalnin was born in Latvia in 1887. A 1984 National Register nomination form says that at about twenty-six he was engaged to a girl ten years younger, Agnes, who called off the wedding shortly before it. The form says he later called her his Sweet Sixteen. After years of work across North America and illness, he reached Florida City in the early 1920s."
script.json-9- },
script.json-10- {
script.json-11-  "id": "s3",
script.json-12-  "text": "Even that part has gaps. Her surname appears as Scuff and Skuvst, and one Latvian account gives a different name and age. Why he built it comes from later tellings: the story as told, not a record."
--
script.json-16-  "text": "In 1923, according to the form, he bought one acre near Florida City for twelve dollars. The ground was oolitic limestone, popularly called coral rock. He built a shed, then a two story tower, a wall, and carved furniture and astronomy pieces from the rock around him."
script.json-17- },
script.json-18- {
script.json-19-  "id": "s5",
script.json:20:  "text": "In the mid nineteen thirties he bought ten acres in Homestead, about ten miles north, and decided to take his stone with him. The dates conflict. The form says 1937. The obelisk is inscribed: moved in 1939, and the castle's own chronology says land clearing began in May 1939. A farmer, Bob Biggers, hauled the stones. Accounts say Ed loaded and unloaded them himself, at night."
script.json-21- },
script.json-22- {
script.json-23-  "id": "s6",
script.json:24:  "text": "Now the weights, as printed in the 1984 form, in pounds. The Polaris sighting slab: twenty short tons. Each quarter moon: eighteen. The full moon fountain: twenty three. The obelisk: twenty eight and a half. The heaviest it names: thirty tons. The castle's own site says over twenty one. These are published estimates, not weighings."
script.json-25- },
script.json-26- {
script.json-27-  "id": "s7",
script.json:28:  "text": "What about the famous total, eleven hundred tons? It appears on the castle's website and in encyclopedias with no named estimator; the 1984 form gives none. The earliest number we found is over a thousand tons, in a 1950s book by the engineer Carrol Lake. We could not find where eleven hundred first appears. So: a claim, source untraced."
script.json-29- },
script.json-30- {
script.json-31-  "id": "s8",
script.json:32:  "text": "The best known piece is the gate. A single slab, eighty one inches wide, ninety two tall, twenty one thick, turning on a central shaft that the form says uses an automobile axle. It was reported to turn with one finger. The form calls it nine tons. Accounts say it stopped turning in the mid nineteen eighties, 1984 or 1986. Six men and a crane lifted it out, and a rusted truck bearing was replaced."
script.json-33- },
script.json-34- {
script.json-35-  "id": "s9",
script.json:36:  "text": "Here is a check anyone can do. Those dimensions come to about ninety cubic feet. Even if the whole rectangle were solid aragonite, it would weigh about eight tons. Real oolite is porous; at an assumed thirty percent, nearer five and a half. So nine tons is probably a rounded figure. Five tons on one finger is still remarkable."
script.json-37- },
script.json-38- {
script.json-39-  "id": "s10",
script.json:40:  "text": "What tools did he have? The form lists his tools, made partly from old car parts: block and tackle, rollers, jacks, wedges, slings, cables, sledges and chisels. Old photographs show tall wooden tripods with chains, and a chain hoist. An independent archive says no detailed record shows how the rigs were used."
script.json-41- },
script.json-42- {
script.json-43-  "id": "s11",
script.json:44:  "text": "What can that gear do? Take a ten ton block, twenty thousand pounds. A block and tackle with six rope segments cuts the pull to a sixth: about thirty three hundred pounds. Chain two sets together and it is six times six: about five hundred fifty. Add a five to one winch and it is near one hundred ten pounds. The price is distance: the tackle rope moves thirty six feet per foot of lift, and the winch handle about one hundred eighty. Small force, long time. This is ideal physics, no friction: what is possible, not what he did."
script.json-45- },
script.json-46- {
script.json-47-  "id": "s12",
script.json-48-  "text": "Levers work on the same idea. A bar with nine feet on one side of the pivot and one on the other multiplies your push by nine. Raise a block an inch, slide a timber under, repeat. That is the principle, not a plan for ten tons. It is slow, and needs only time."
--
script.json-52-  "text": "So what is not documented? In 1955, the castle's new owner collected more than two hundred fifty signed affidavits saying Ed worked alone with simple hand tools. But the form quotes no one who watched the largest blocks go up. So the belief is documented. The method is not."
script.json-53- },
script.json-54- {
script.json-55-  "id": "s14",
script.json:56:  "text": "Now his own words. Asked how, the form says, Ed always answered that he understood the methods of the pyramid builders, and the laws of leverage and weight. That is a claim. We found no document where he describes his lifting method. He published pamphlets in 1936 and 1945, including Magnetic Current, on his own ideas about magnets."
script.json-57- },
script.json-58- {
script.json-59-  "id": "s15",
script.json:60:  "text": "Then the popular theories. Sound levitation. Magnetism, the subject of his pamphlets, though they do not say so. Help from beyond Earth, or mastered gravity, ideas the 1984 form already records. All are not established. We found no measurement, recording, or physical trace for any, and the floating stone stories are secondhand. Absence of evidence is not proof of absence. So: not established, not impossible."
script.json-61- },
script.json-62- {
script.json-63-  "id": "s16",
script.json:64:  "text": "So here is the ledger. Documented: the land purchase, the form's printed weights, the tool list, photographs of hoisting gear. Reported, with conflicts: the move dates, the gate repair. Claimed: that he worked alone, that he knew the pyramid builders' methods, the eleven hundred ton total. Not settled: the gate's true weight. Unknown: how he raised the largest blocks, alone."
script.json-65- },
script.json-66- {
script.json-67-  "id": "s17",
script.json:68:  "text": "Patient work with simple machines fits the tools, the photographs and the physics. Fits is not the same as shown. Could something stranger be going on? Not established. Not ruled out. Someone watching this might be the one who works it out."
script.json-69- },
script.json-70- {
script.json-71-  "id": "s18",
script.json-72-  "text": "Still Unknown, from Heartbeat Observatory."

exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command 'rg -n "''^(#|##|###)|1936|1937|1939|Biggers|Polaris|weights|Lake|1000|1,000|1984|1986|aragonite|36 ft|180 ft|archive|theor|ledger|gate|tackle|WRONG|UNSURE|CONFIRMED" FACTCHECK-codex-r1.md' in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 818ms:
14:Fact-check SOURCES.md and the script (script.json narration, plus on-screen labels in ep_body.py scene functions and SCENES list) about Edward Leedskalnin / Coral Castle with web search; mark each claim CONFIRMED/WRONG/UNSURE; pay special attention to: move dates (1936/1937/1939), Bob Biggers truck, 1955 affidavits count and who collected them, weights (Polaris slab 40,000 lb etc.), 9-ton gate dimensions and 1986 repair (6 men, 50-ton crane, reset July 1986), 2005 failure, the 1,100-ton figure source, our gate-volume arithmetic (81x92x21 in, calcite 2.71, aragonite 2.93 g/cm3), block and tackle numbers, pamphlet titles and dates, National Register date. Also try to find who first estimated 1,100 tons. One-line verdict at the end.
16:I’m using the data-analysis validation workflow because this is a source-by-source claim audit. I’ll first inventory every narration and on-screen claim, then verify them against primary or strong secondary sources and report each as CONFIRMED, WRONG, or UNSURE.
25:# Validate Data Analysis
29:## Overall Instructions
34:## Dependencies
44:## Related Skills
50:## Choose review depth
57:## Workflow
59:Keep normal validation proportionate to consequential claims and authored/affected components. Batch independent reads and calculations, reuse applicable evidence from the calling build, and test representative control transitions. Use a subagent only for a substantial independent question while continuing useful local work; a routine check does not need a team or a full coverage ledger. Resolve related defects together and recheck affected results after the final edit. Keep the normal handoff below concise; give a concrete proposed remedy for each material finding. Heavy review has a parallel work plan and a 20â€“30 minute budget in the deep-review reference.
63:3. **Verify consequential calculations.** Independently recompute important or surprising numbers from the actual selected inputs. Check weights, subtotals, distinct counts, join expansion, period bases and boundary cases. Agreement between outputs sharing one helper is not independent proof. Distinguish zero, missing and empty results; inspect actual date predicates rather than assuming different date labels mean different windows. Preserve inspectable SQL, formulas or calculation notes; reuse an existing notebook when available.
68:## Standard handoff
72:## Offer a deep review
84:# Shared Data Skill Instructions
86:Apply these instructions to every Data workflow, including a focused skill invoked directly. Apply the index's runtime gate before source discovery when that gate governs the request. Use the fast path in the initial dependency check below, and revisit discovery only for a material source gap or changed access.
90:## Dependency resolution
96:### Initial dependency check
107:### Find the authoritative source
119:### Discover and offer useful integrations
125:#### Efficient Data category resolution
155:#### Use plugin history when re-prompting
161:#### Wait for required connector setup
173:### Continue with supported evidence
179:### Older clients and unresolved access
189:# Analysis quality criteria
191:## Scope and use
193:These are reusable criteria for analytical work, not a separate workflow or report. Apply the relevant criteria within the selected task and reuse evidence that still applies. Consulting this reference does not start a full artifact audit, an approval sequence, or a publication gate. The selected workflow owns scope, repair authorization, verification depth, and the user-facing handoff.
197:## Question and method
204:## Source and data fitness
213:## Calculations and transformations
216:- Totals reconcile where categories are mutually exclusive and additive. Do not sum overlapping audiences, percentages or per-entity rates. Combine rates from their numerators and denominators, or use valid weights; do not average group averages or percentiles without justification.
220:## Reasonableness and boundary cases
222:Compare scale and movement with relevant history, known totals or independently supported expectations. Investigate unexplained jumps, flatlines, exact round values, impossible ranges and unexpected 0% or 100% rates; surprising observations are prompts to investigate, not proof of defects. Shares should reconcile only where their definitions require it.
224:Check meaningful empty, all-null, new-entity and boundary-date cases. Consider small samples, outlier-dominated averages, changing segment mix, aggregate/segment reversals, multiple testing and cherry-picked ranges where they affect the claim. An alternate computation can help resolve a surprising result; plausibility alone cannot validate it.
226:## Conclusions and causality
234:## Visual and narrative integrity
237:- Material uncertainty stays with the estimate, including interval meaning and level where defined. Do not substitute observation spread or scenarios for uncertainty, average bounds, or reuse aggregate intervals for subgroups. Preserve uncertainty through filters and exports.
241:## Evidence and coverage units
247:# Deep review
253:## Select the authorized mode
261:## Finish within 20â€“30 minutes, including repairs
263:Aim to deliver in **20 minutes; finish by 30 minutes**, including delegated work, repairs, final rendered verification and the handoff. Honor a shorter explicit user/runtime budget. Read the available clock at entry, record the deadline, and check elapsed time at phase changes. Subagents, retries and repairs share that deadline. Bound tool calls so they leave time for verification.
273:Use this allocation flexibly and finish earlier when the important work is done. Reserve at least the final five minutes for verification and delivery. Stop new exploratory or cosmetic work before it consumes that reserve. Do not start a repair that cannot reasonably be verified before the deadline; propose it instead. At the deadline collect available evidence, stop unfinished delegated work, and deliver the best supported result with named gaps. Preserve a usable verified build; revert only your own unverified edits if necessary and retain the proposed fix in notes. A partial review can be useful, but is never complete verification.
275:## Split independent work early
285:Keep one owner for shared-browser navigation and one owner for each edited file. Parallelize read-only investigation; delegate edits only with non-overlapping ownership and an integration deadline. The lead inspects evidence behind material findings and verifies the combined final artifact. A subagent's assurance or count is not proof. If subagents are unavailable, batch independent tool calls and computations, retain the deadline, and disclose consequential coverage limits.
287:## Map scope, then investigate by impact
295:## Verify evidence efficiently
307:## Repair and verify per coherent batch
317:## Record honest coverage
340:## Return one review handoff
360:# Still Unknown 10.2 "Coral Castle: one man, 1,100 tons" - sources and flags (Claude Sonnet 5.5, 2026-10-13)
364:## Primary document (read in full, OCR of the scanned PDF)
366:Prepared by Maria Temkin / Michael Zimny, Florida Division of Archives, 2 April 1984. Listed 10 May 1984 (ref. 84000840); name changed to Coral Castle 2011 (Florida SHPO letter, 16 Feb 2011, in the same PDF).
371:- Move: "1937" (section 7, "moved date 1937"); obelisk inscribed "Made in 1928. Moved in 1939. Born 1887. Latvia, E.L."; newspaper cited in the bibliography "Ed Is Doing A Colossal Job of Moving ..." (Aug 1939). Wikipedia says he moved ~1936 and spent ~3 years. Screen says dates vary.
372:- Ten-acre tract on South Federal Highway. "He sought the aid of ... Bob Biggers ... All Edward Leedskalnin wanted from Mr. Biggers, however, was the use of his truck ... completed by Leedskalnin without any assistance ... worked alone and at night loading and unloading Biggers' truck."
373:- Weights (lb, converted to short tons by us): Polaris slab 40,000 lb (20 t), 25 ft tall; each quarter moon 36,000 lb (18 t); full-moon fountain 46,000 lb (23 t); Mars and Saturn 36,000 lb; obelisk 57,000 lb (28.5 t); "thirty ton sculpture" crowning the north wall = heaviest oolitic block at Rock Gate; wall blocks 8 ft x 4 ft x 3 ft, "several tons". "Sculptures weighing up to 30 tons each".
374:- Gate: "nine ton gate", 81 in wide, 92 in tall, 21 in thick; single pivot; central vertical shaft with an automobile axle connecting slab to ground and lintel; fits within 1/4 in; pushed open with one finger.
375:- Tools: "primitive tools are on display ... metal fall (block and tackle), rollers, jacks, wedges, slings, cables, sledges, chisels"; quarrying tools "fashioned from old car parts".
376:- Public theories (form): extraterrestrial aid; "secrets of gravitational force enabling him to render the mammoth rocks weightless".
378:- Pamphlets (form): A Book in Every Home (1936); Magnetic Current (Franklin Press, Aug 1945); Mineral, Vegetable and Animal Life (Franklin Press, Oct 1945).
382:## Secondary sources
383:- Wikipedia "Coral Castle" (fetched 2026-10-13): 1,100 short tons (unattributed); gate stopped 1986, 6 men + 50-short-ton crane, rusted truck bearing, reinstalled 23 July 1986, failed again 2005, no longer as smooth; he said he "understood the laws of weight and leverage".
386:- rockgatepark.com/the-tools: photographs of tripods/lifting frame; "no detailed records" of exact configuration, materials or procedures; no weights or dates.
390:## Our arithmetic (shown on screen, labelled)
392:- Density: calcite 2.71 g/cm3, aragonite 2.93 g/cm3 (standard mineral values, knowledge); 1 g/cm3 = 62.428 lb/ft3. Solid calcite 7.7 short tons, solid aragonite 8.3, 30%-pore versions 5.4 / 5.8. The 30% porosity is an assumption (Miami Limestone porosity data exist, USGS OFR 85-21, not read). Even the densest solid mineral gives < 9 tons, so "nine ton" is probably rounded or the dimensions differ. Screen says NOT SETTLED.
393:- Block and tackle: ideal MA = number of supporting rope segments. 20,000 lb / 6 = 3,333; / 36 = 556; / 180 = 111 lb; 180 ft of rope per 1 ft lift. Friction ignored (labelled). Lever 9:1: 100 lb x 9 ft = 900 lb x 1 ft.
395:## Flags (open items)
396:- Origin of the 1,100-ton figure NOT FOUND. Treated as a CLAIM with untraced source. (Search hints at Carroll Lake, Civil Engineering Magazine 1958, in the form's bibliography; not checked.)
397:- Photographs: Florida Memory item 328424 ("Ed Leedskalnin with hoisting equipment", reported c. 1936 in a search snippet) returned 403 to the fetch; date unverified. Live Science and Mental Floss were only seen as search snippets (they report photographs of pole tripods + block and tackle). The brief's "one grainy photo" is NOT what we found: several photographs exist; none shown here.
408:  "text": "Start with the man. Edward Leedskalnin was born in Latvia in 1887. A 1984 National Register nomination form says that at about twenty-six he was engaged to a girl ten years younger, Agnes, who called off the wedding shortly before it. He later called her his Sweet Sixteen. After years of work across North America and illness, he reached Florida City in the early 1920s."
420:  "text": "In the mid nineteen thirties he bought ten acres in Homestead, about ten miles north, and decided to take his stone with him. Dates vary. The form says 1937. The obelisk is inscribed: moved in 1939. A local man, Bob Biggers, lent his truck. The form says Ed worked alone, at night, loading and unloading it."
424:  "text": "Now the weights, which the form lists in pounds. The Polaris sighting slab: twenty short tons. Each quarter moon: eighteen. The full moon fountain: twenty three. The obelisk: twenty eight and a half. The heaviest it names: a thirty ton sculpture on the north wall."
428:  "text": "What about the famous total, eleven hundred tons? It appears on the castle's own website, and in encyclopedias with no named estimator. The 1984 form gives no total. We could not find who first estimated it, or how. So it is a claim, with an untraced source."
432:  "text": "The best known piece is the gate. A single slab, eighty one inches wide, ninety two tall, twenty one thick, turning on a central shaft that the form says uses an automobile axle. One finger moves it. The form calls it nine tons. In 1986 it stopped turning. Six men and a fifty ton crane lifted it out, a rusted truck bearing was replaced, and it was reset in July."
436:  "text": "Here is a check anyone can do. Those dimensions come to about ninety cubic feet. Even solid aragonite, the densest the rock could be, would weigh about eight tons. Real oolite is porous. At thirty percent porosity, an assumption, it is nearer five and a half. So nine tons is probably a rounded figure, not a weighing. Five tons on one finger is still remarkable."
440:  "text": "What tools did he have? The form says the castle displays his tools, made partly from old car parts: block and tackle, rollers, jacks, wedges, slings, cables, sledges and chisels. Old photographs show tall wooden tripods with chains hanging from the top, and a chain hoist. The castle's archive says no detailed record shows how the rigs were used."
444:  "text": "What can that gear do? Take a ten ton block, twenty thousand pounds. A block and tackle with six rope segments cuts the pull to a sixth: about thirty three hundred pounds. Chain two sets together and it is six times six: about five hundred fifty. Add a five to one winch and it is near one hundred ten pounds, which one person can pull. The price is distance: for each foot of lift, one hundred eighty feet of rope. Small force, long time. This is ideal physics, no friction: what is possible, not what he did."
456:  "text": "Now his own words. Asked how, the form says, Ed always gave the same answer: that he understood the methods of the pyramid builders, and the laws of leverage and weight. That is a claim. We found no document where he describes his lifting method. He did publish pamphlets, in 1936 and 1945, including Magnetic Current, about his own ideas on magnets and electricity."
460:  "text": "Then the popular theories. That he used sound to levitate the stone. That magnetism, as in his pamphlets, cancelled weight. That he had help from beyond Earth, an idea already circulating before the 1984 form. All three are not established. We found no measurement, recording, or physical trace for any of them, and the floating stone stories are secondhand. Absence of evidence is not proof of absence. So: not established, not impossible."
464:  "text": "So here is the ledger. Documented: the dates, the form's weights, the move, the tools, the 1986 gate repair. Claimed: that he worked alone, that he knew the pyramid builders' methods, and the eleven hundred ton total. Not settled: the gate's true weight. Unknown: exactly how he raised and set the largest blocks alone."
479:# ------------------------------------------------------------------ helpers
526:# ------------------------------------------------------------------ scenes
573:    tag(cv, CONT[0], CONT[1] - 40, 'DOCUMENTED: NRHP FORM, 1984', MINT, ease(t / 0.8))
591:    stack(cv, bx + 30, by + 70, ['NRHP 1984 form: "Scuff", footnote also gives "Skuvst"', 'one Latvian account: a different name and age'],
598:    tag(cv, x0, y0 - 40, 'DOCUMENTED: NRHP FORM, 1984', MINT, ease(t / 0.8))
642:    rows = [('1936-40', 'accounts differ; about three years of moving', 0.25), ('1937', 'the 1984 NRHP form, section 7', 0.4), ('1939', 'inscribed on the obelisk: "Moved in 1939"', 0.55),
643:            ('truck', 'Bob Biggers\' truck, lent to Ed (NRHP form)', 0.72), ('crew', 'worked alone, at night, loading and unloading (form)', 0.88)]
651:def sc_weights(cv, t, p):
654:    tag(cv, x0, y0 - 40, 'DOCUMENTED: WEIGHTS AS LISTED, NRHP 1984', MINT, ease(t / 0.8), 20)
655:    items = [('Polaris sighting slab', 20, 0.12), ('each quarter moon', 18, 0.28), ('full moon fountain', 23, 0.4), ('obelisk', 28.5, 0.55), ('north-wall sculpture', 30, 0.78)]
679:    rows = [('coralcastle.com', 'states "1,100 tons"; no estimator named', 0.15), ('Wikipedia', '1,100 short tons; figure not attributed', 0.3), ('NRHP form, 1984', 'lists pieces "up to 30 tons"; no total', 0.5), ('first estimator', 'not found', 0.7)]
687:def sc_gate(cv, t, p):
712:    # 1986 facts
714:    rows = [('"nine ton" (form)  -  see the next check', 0.35, MINT), ('1986: stopped turning; rusted truck bearing', 0.6, MINT), ('6 men + 50-ton crane lifted it out; reset July 1986', 0.78, MINT), ('2005: failed again (Wikipedia)', 0.92, DIM)]
727:    rows = [('calcite, solid (2.71 g/cm3)', 2.71, 0.0), ('aragonite, solid (2.93 g/cm3)', 2.93, 0.0), ('aragonite, 30% pore space', 2.93 * 0.7, 0.0), ('calcite, 30% pore space', 2.71 * 0.7, 0.0)]
756:    rows = [('DOCUMENTED', MINT, 'tools on display (NRHP 1984): block and tackle ("metal fall"), rollers, jacks, wedges, slings, cables, sledges, chisels; some made from old car parts', 0.15),
758:            ('UNKNOWN', ROSE, 'exact rig set-up and procedures: "no detailed records" (Rock Gate Park archive page)', 0.78)]
771:def sc_tackle(cv, t, p):
792:            ('+ 5:1 winch, 36 x 5 = 180:  20,000 / 180 = 111 lb', 0.58, MINT), ('cost: 180 ft of rope hauled per 1 ft of lift', 0.78, ROSE)]
855:    mono(cv, x0 + 30, yy + 10, 'Ed\'s reply to how he did it, as paraphrased in the NRHP form, 1984', 20, DIM, qa)
858:    ps = [('1936', 'A Book in Every Home', 0.62), ('Aug 1945', 'Magnetic Current', 0.76), ('Oct 1945', 'Mineral, Vegetable and Animal Life', 0.88)]
864:def sc_theories(cv, t, p):
867:    items = [('sound', 'sound levitates the stone', 0.12), ('magnetism', '"magnetic current" cancels weight', 0.3), ('help from beyond Earth', 'already circulating by 1984', 0.48)]
886:LEDGER = [('DOCUMENTED', MINT, 'dates, the form\'s weights, the move, the tools, the 1986 repair', 0.22),
888:          ('NOT SETTLED', ROSE, 'the gate\'s true weight', 0.7),
890:def sc_ledger(cv, t, p):
893:    big(cv, x0, y0 + 10, 'the ledger', 56 if PORT else 64, TXT, ease(t / 1.0))
916:    'NPS: National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed\'s Place)" / Coral Castle. Florida Division of Archives, 2 Apr 1984; listed 10 May 1984; renamed Coral Castle 2011 (npgallery.nps.gov, asset 1ed2ccd0-b692-42dc-b28d-1227c1a23407)',
917:    'Wikipedia, "Coral Castle" and "Edward Leedskalnin" (read 2026-10-13): 1986 gate repair, 2005 failure, 1,100 short tons (figure unattributed)',
918:    'coralcastle.com, "The Secrets of Coral Castle" (1,100 tons); rockgatepark.com/the-tools (tool photographs; "no detailed records")',
921:    'Our arithmetic (gate volume, density, block and tackle, lever): standard formulas; calcite 2.71 and aragonite 2.93 g/cm3; 30% porosity is assumed']
935:# (segment id, headline, source line, draw fn)
938:    ('s2', 'a man from latvia', 'NRHP nomination form, Florida Division of Archives, 1984', sc_man),
939:    ('s3', 'a love story, and its gaps', 'NRHP form 1984 (name spellings, footnote 2); Wikipedia "Edward Leedskalnin"', sc_agnes),
940:    ('s4', 'ed\'s place, 1923', 'NRHP form 1984; Dade County Deed Book 1546, p. 8', sc_site),
941:    ('s5', 'the move to homestead', 'NRHP form 1984 (sec. 7, 8; obelisk inscription)', sc_move),
942:    ('s6', 'what the form weighs', 'NRHP form 1984: weights in pounds, converted here', sc_weights),
943:    ('s7', 'the 1,100-ton total', 'coralcastle.com; Wikipedia "Coral Castle"; NRHP form 1984', sc_total),
944:    ('s8', 'the gate', 'NRHP form 1984; Wikipedia "Coral Castle" (1986 repair, 2005)', sc_gate),
946:    ('s10', 'the tools', 'NRHP form 1984 (tool list); rockgatepark.com/the-tools', sc_tools),
947:    ('s11', 'block and tackle', 'Ideal mechanical advantage = rope segments. Worked example, not his rig', sc_tackle),
949:    ('s13', 'what no one has documented', 'NRHP form 1984 quoting the 1955 affidavits', sc_affidavit),
950:    ('s14', 'what he said', 'NRHP form 1984 (paraphrase of his reply; pamphlet list)', sc_words),
951:    ('s15', 'popular theories', 'NRHP form 1984 (extraterrestrial, gravity theories); thisunexplaineduniverse.com', sc_theories),
952:    ('s16', None, 'Status as of October 2026', sc_ledger),
975:# ------------------------------------------------------------------ framework
1054:"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command 'rg -n "def sc_(move|weights|total|gate|check)|SCENES =|SOURCES =|1936|1937|1939|Biggers|Polaris|gate|affidavit|pamphlet|National Register|1,100|1100|block and tackle|rope segments" ep_body.py script.json SOURCES.md' in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
1056:script.json:8:  "text": "Start with the man. Edward Leedskalnin was born in Latvia in 1887. A 1984 National Register nomination form says that at about twenty-six he was engaged to a girl ten years younger, Agnes, who called off the wedding shortly before it. He later called her his Sweet Sixteen. After years of work across North America and illness, he reached Florida City in the early 1920s."
1057:script.json:20:  "text": "In the mid nineteen thirties he bought ten acres in Homestead, about ten miles north, and decided to take his stone with him. Dates vary. The form says 1937. The obelisk is inscribed: moved in 1939. A local man, Bob Biggers, lent his truck. The form says Ed worked alone, at night, loading and unloading it."
1058:script.json:24:  "text": "Now the weights, which the form lists in pounds. The Polaris sighting slab: twenty short tons. Each quarter moon: eighteen. The full moon fountain: twenty three. The obelisk: twenty eight and a half. The heaviest it names: a thirty ton sculpture on the north wall."
1059:script.json:32:  "text": "The best known piece is the gate. A single slab, eighty one inches wide, ninety two tall, twenty one thick, turning on a central shaft that the form says uses an automobile axle. One finger moves it. The form calls it nine tons. In 1986 it stopped turning. Six men and a fifty ton crane lifted it out, a rusted truck bearing was replaced, and it was reset in July."
1060:script.json:40:  "text": "What tools did he have? The form says the castle displays his tools, made partly from old car parts: block and tackle, rollers, jacks, wedges, slings, cables, sledges and chisels. Old photographs show tall wooden tripods with chains hanging from the top, and a chain hoist. The castle's archive says no detailed record shows how the rigs were used."
1061:script.json:44:  "text": "What can that gear do? Take a ten ton block, twenty thousand pounds. A block and tackle with six rope segments cuts the pull to a sixth: about thirty three hundred pounds. Chain two sets together and it is six times six: about five hundred fifty. Add a five to one winch and it is near one hundred ten pounds, which one person can pull. The price is distance: for each foot of lift, one hundred eighty feet of rope. Small force, long time. This is ideal physics, no friction: what is possible, not what he did."
1063:script.json:56:  "text": "Now his own words. Asked how, the form says, Ed always gave the same answer: that he understood the methods of the pyramid builders, and the laws of leverage and weight. That is a claim. We found no document where he describes his lifting method. He did publish pamphlets, in 1936 and 1945, including Magnetic Current, about his own ideas on magnets and electricity."
1064:script.json:60:  "text": "Then the popular theories. That he used sound to levitate the stone. That magnetism, as in his pamphlets, cancelled weight. That he had help from beyond Earth, an idea already circulating before the 1984 form. All three are not established. We found no measurement, recording, or physical trace for any of them, and the floating stone stories are secondhand. Absence of evidence is not proof of absence. So: not established, not impossible."
1065:script.json:64:  "text": "So here is the ledger. Documented: the dates, the form's weights, the move, the tools, the 1986 gate repair. Claimed: that he worked alone, that he knew the pyramid builders' methods, and the eleven hundred ton total. Not settled: the gate's true weight. Unknown: exactly how he raised and set the largest blocks alone."
1069:ep_body.py:168:    rows = [('1936-40', 'accounts differ; about three years of moving', 0.25), ('1937', 'the 1984 NRHP form, section 7', 0.4), ('1939', 'inscribed on the obelisk: "Moved in 1939"', 0.55),
1070:ep_body.py:169:            ('truck', 'Bob Biggers\' truck, lent to Ed (NRHP form)', 0.72), ('crew', 'worked alone, at night, loading and unloading (form)', 0.88)]
1071:ep_body.py:177:def sc_weights(cv, t, p):
1072:ep_body.py:181:    items = [('Polaris sighting slab', 20, 0.12), ('each quarter moon', 18, 0.28), ('full moon fountain', 23, 0.4), ('obelisk', 28.5, 0.55), ('north-wall sculpture', 30, 0.78)]
1075:ep_body.py:205:    rows = [('coralcastle.com', 'states "1,100 tons"; no estimator named', 0.15), ('Wikipedia', '1,100 short tons; figure not attributed', 0.3), ('NRHP form, 1984', 'lists pieces "up to 30 tons"; no total', 0.5), ('first estimator', 'not found', 0.7)]
1076:ep_body.py:213:def sc_gate(cv, t, p):
1078:ep_body.py:282:    rows = [('DOCUMENTED', MINT, 'tools on display (NRHP 1984): block and tackle ("metal fall"), rollers, jacks, wedges, slings, cables, sledges, chisels; some made from old car parts', 0.15),
1081:ep_body.py:384:    ps = [('1936', 'A Book in Every Home', 0.62), ('Aug 1945', 'Magnetic Current', 0.76), ('Oct 1945', 'Mineral, Vegetable and Animal Life', 0.88)]
1083:ep_body.py:414:          ('NOT SETTLED', ROSE, 'the gate\'s true weight', 0.7),
1085:ep_body.py:442:    'NPS: National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed\'s Place)" / Coral Castle. Florida Division of Archives, 2 Apr 1984; listed 10 May 1984; renamed Coral Castle 2011 (npgallery.nps.gov, asset 1ed2ccd0-b692-42dc-b28d-1227c1a23407)',
1086:ep_body.py:443:    'Wikipedia, "Coral Castle" and "Edward Leedskalnin" (read 2026-10-13): 1986 gate repair, 2005 failure, 1,100 short tons (figure unattributed)',
1087:ep_body.py:444:    'coralcastle.com, "The Secrets of Coral Castle" (1,100 tons); rockgatepark.com/the-tools (tool photographs; "no detailed records")',
1088:ep_body.py:447:    'Our arithmetic (gate volume, density, block and tackle, lever): standard formulas; calcite 2.71 and aragonite 2.93 g/cm3; 30% porosity is assumed']
1091:ep_body.py:469:    ('s7', 'the 1,100-ton total', 'coralcastle.com; Wikipedia "Coral Castle"; NRHP form 1984', sc_total),
1092:ep_body.py:470:    ('s8', 'the gate', 'NRHP form 1984; Wikipedia "Coral Castle" (1986 repair, 2005)', sc_gate),
1093:ep_body.py:472:    ('s10', 'the tools', 'NRHP form 1984 (tool list); rockgatepark.com/the-tools', sc_tools),
1094:ep_body.py:473:    ('s11', 'block and tackle', 'Ideal mechanical advantage = rope segments. Worked example, not his rig', sc_tackle),
1095:ep_body.py:475:    ('s13', 'what no one has documented', 'NRHP form 1984 quoting the 1955 affidavits', sc_affidavit),
1096:ep_body.py:476:    ('s14', 'what he said', 'NRHP form 1984 (paraphrase of his reply; pamphlet list)', sc_words),
1099:SOURCES.md:12:- Move: "1937" (section 7, "moved date 1937"); obelisk inscribed "Made in 1928. Moved in 1939. Born 1887. Latvia, E.L."; newspaper cited in the bibliography "Ed Is Doing A Colossal Job of Moving ..." (Aug 1939). Wikipedia says he moved ~1936 and spent ~3 years. Screen says dates vary.
1100:SOURCES.md:13:- Ten-acre tract on South Federal Highway. "He sought the aid of ... Bob Biggers ... All Edward Leedskalnin wanted from Mr. Biggers, however, was the use of his truck ... completed by Leedskalnin without any assistance ... worked alone and at night loading and unloading Biggers' truck."
1101:SOURCES.md:14:- Weights (lb, converted to short tons by us): Polaris slab 40,000 lb (20 t), 25 ft tall; each quarter moon 36,000 lb (18 t); full-moon fountain 46,000 lb (23 t); Mars and Saturn 36,000 lb; obelisk 57,000 lb (28.5 t); "thirty ton sculpture" crowning the north wall = heaviest oolitic block at Rock Gate; wall blocks 8 ft x 4 ft x 3 ft, "several tons". "Sculptures weighing up to 30 tons each".
1102:SOURCES.md:15:- Gate: "nine ton gate", 81 in wide, 92 in tall, 21 in thick; single pivot; central vertical shaft with an automobile axle connecting slab to ground and lintel; fits within 1/4 in; pushed open with one finger.
1103:SOURCES.md:16:- Tools: "primitive tools are on display ... metal fall (block and tackle), rollers, jacks, wedges, slings, cables, sledges, chisels"; quarrying tools "fashioned from old car parts".
1104:SOURCES.md:19:- Pamphlets (form): A Book in Every Home (1936); Magnetic Current (Franklin Press, Aug 1945); Mineral, Vegetable and Animal Life (Franklin Press, Oct 1945).
1106:SOURCES.md:24:- Wikipedia "Coral Castle" (fetched 2026-10-13): 1,100 short tons (unattributed); gate stopped 1986, 6 men + 50-short-ton crane, rusted truck bearing, reinstalled 23 July 1986, failed again 2005, no longer as smooth; he said he "understood the laws of weight and leverage".
1109:SOURCES.md:27:- rockgatepark.com/the-tools: photographs of tripods/lifting frame; "no detailed records" of exact configuration, materials or procedures; no weights or dates.
1110:SOURCES.md:34:- Block and tackle: ideal MA = number of supporting rope segments. 20,000 lb / 6 = 3,333; / 36 = 556; / 180 = 111 lb; 180 ft of rope per 1 ft lift. Friction ignored (labelled). Lever 9:1: 100 lb x 9 ft = 900 lb x 1 ft.
1111:SOURCES.md:37:- Origin of the 1,100-ton figure NOT FOUND. Treated as a CLAIM with untraced source. (Search hints at Carroll Lake, Civil Engineering Magazine 1958, in the form's bibliography; not checked.)
1112:SOURCES.md:38:- Photographs: Florida Memory item 328424 ("Ed Leedskalnin with hoisting equipment", reported c. 1936 in a search snippet) returned 403 to the fetch; date unverified. Live Science and Mental Floss were only seen as search snippets (they report photographs of pole tripods + block and tackle). The brief's "one grainy photo" is NOT what we found: several photographs exist; none shown here.
1115:The local inventory shows the central risk clearly: several statements accurately repeat the 1984 nomination, but “documented” sometimes overstates what that later form itself proves. I’m separating “the form says X” from “X is independently established,” especially for the move, solitary work, affidavits, and gate repair.
1117:web search: site:npgallery.nps.gov Coral Castle Rock Gate nomination 1984 PDF 84000840 ...
1119:web search: "July 23, 1986" "Coral Castle" gate ...
1123:web search: Edward Leedskalnin "moved in 1939" Bob Biggers newspaper ...
1134:    tag(cv, x0, y0 - 40, 'DOCUMENTED: NRHP FORM, 1984', MINT, ease(t / 0.8))
1178:    rows = [('1936-40', 'accounts differ; about three years of moving', 0.25), ('1937', 'the 1984 NRHP form, section 7', 0.4), ('1939', 'inscribed on the obelisk: "Moved in 1939"', 0.55),
1179:            ('truck', 'Bob Biggers\' truck, lent to Ed (NRHP form)', 0.72), ('crew', 'worked alone, at night, loading and unloading (form)', 0.88)]
1187:def sc_weights(cv, t, p):
1190:    tag(cv, x0, y0 - 40, 'DOCUMENTED: WEIGHTS AS LISTED, NRHP 1984', MINT, ease(t / 0.8), 20)
1191:    items = [('Polaris sighting slab', 20, 0.12), ('each quarter moon', 18, 0.28), ('full moon fountain', 23, 0.4), ('obelisk', 28.5, 0.55), ('north-wall sculpture', 30, 0.78)]
1215:    rows = [('coralcastle.com', 'states "1,100 tons"; no estimator named', 0.15), ('Wikipedia', '1,100 short tons; figure not attributed', 0.3), ('NRHP form, 1984', 'lists pieces "up to 30 tons"; no total', 0.5), ('first estimator', 'not found', 0.7)]
1223:def sc_gate(cv, t, p):
1248:    # 1986 facts
1250:    rows = [('"nine ton" (form)  -  see the next check', 0.35, MINT), ('1986: stopped turning; rusted truck bearing', 0.6, MINT), ('6 men + 50-ton crane lifted it out; reset July 1986', 0.78, MINT), ('2005: failed again (Wikipedia)', 0.92, DIM)]
1263:    rows = [('calcite, solid (2.71 g/cm3)', 2.71, 0.0), ('aragonite, solid (2.93 g/cm3)', 2.93, 0.0), ('aragonite, 30% pore space', 2.93 * 0.7, 0.0), ('calcite, 30% pore space', 2.71 * 0.7, 0.0)]
1292:    rows = [('DOCUMENTED', MINT, 'tools on display (NRHP 1984): block and tackle ("metal fall"), rollers, jacks, wedges, slings, cables, sledges, chisels; some made from old car parts', 0.15),
1294:            ('UNKNOWN', ROSE, 'exact rig set-up and procedures: "no detailed records" (Rock Gate Park archive page)', 0.78)]
1307:def sc_tackle(cv, t, p):
1328:            ('+ 5:1 winch, 36 x 5 = 180:  20,000 / 180 = 111 lb', 0.58, MINT), ('cost: 180 ft of rope hauled per 1 ft of lift', 0.78, ROSE)]
1391:    mono(cv, x0 + 30, yy + 10, 'Ed\'s reply to how he did it, as paraphrased in the NRHP form, 1984', 20, DIM, qa)
1394:    ps = [('1936', 'A Book in Every Home', 0.62), ('Aug 1945', 'Magnetic Current', 0.76), ('Oct 1945', 'Mineral, Vegetable and Animal Life', 0.88)]
1400:def sc_theories(cv, t, p):
1403:    items = [('sound', 'sound levitates the stone', 0.12), ('magnetism', '"magnetic current" cancels weight', 0.3), ('help from beyond Earth', 'already circulating by 1984', 0.48)]
1422:LEDGER = [('DOCUMENTED', MINT, 'dates, the form\'s weights, the move, the tools, the 1986 repair', 0.22),
1424:          ('NOT SETTLED', ROSE, 'the gate\'s true weight', 0.7),
1426:def sc_ledger(cv, t, p):
1429:    big(cv, x0, y0 + 10, 'the ledger', 56 if PORT else 64, TXT, ease(t / 1.0))
1452:    'NPS: National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed\'s Place)" / Coral Castle. Florida Division of Archives, 2 Apr 1984; listed 10 May 1984; renamed Coral Castle 2011 (npgallery.nps.gov, asset 1ed2ccd0-b692-42dc-b28d-1227c1a23407)',
1453:    'Wikipedia, "Coral Castle" and "Edward Leedskalnin" (read 2026-10-13): 1986 gate repair, 2005 failure, 1,100 short tons (figure unattributed)',
1454:    'coralcastle.com, "The Secrets of Coral Castle" (1,100 tons); rockgatepark.com/the-tools (tool photographs; "no detailed records")',
1457:    'Our arithmetic (gate volume, density, block and tackle, lever): standard formulas; calcite 2.71 and aragonite 2.93 g/cm3; 30% porosity is assumed']
1471:# (segment id, headline, source line, draw fn)
1474:    ('s2', 'a man from latvia', 'NRHP nomination form, Florida Division of Archives, 1984', sc_man),
1475:    ('s3', 'a love story, and its gaps', 'NRHP form 1984 (name spellings, footnote 2); Wikipedia "Edward Leedskalnin"', sc_agnes),
1476:    ('s4', 'ed\'s place, 1923', 'NRHP form 1984; Dade County Deed Book 1546, p. 8', sc_site),
1477:    ('s5', 'the move to homestead', 'NRHP form 1984 (sec. 7, 8; obelisk inscription)', sc_move),
1478:    ('s6', 'what the form weighs', 'NRHP form 1984: weights in pounds, converted here', sc_weights),
1479:    ('s7', 'the 1,100-ton total', 'coralcastle.com; Wikipedia "Coral Castle"; NRHP form 1984', sc_total),
1480:    ('s8', 'the gate', 'NRHP form 1984; Wikipedia "Coral Castle" (1986 repair, 2005)', sc_gate),
1482:    ('s10', 'the tools', 'NRHP form 1984 (tool list); rockgatepark.com/the-tools', sc_tools),
1483:    ('s11', 'block and tackle', 'Ideal mechanical advantage = rope segments. Worked example, not his rig', sc_tackle),
1485:    ('s13', 'what no one has documented', 'NRHP form 1984 quoting the 1955 affidavits', sc_affidavit),
1486:    ('s14', 'what he said', 'NRHP form 1984 (paraphrase of his reply; pamphlet list)', sc_words),
1487:    ('s15', 'popular theories', 'NRHP form 1984 (extraterrestrial, gravity theories); thisunexplaineduniverse.com', sc_theories),
1488:    ('s16', None, 'Status as of October 2026', sc_ledger),
1503:web search: 'April 2, 1984'
1507:web search: newspaper Coral Castle gate repaired "July 23" 1986 Homestead ...
1515:web search: site:engineeringstatics.org block tackle mechanical advantage supporting rope segments displacement ...
1517:web search: site:rockgatepark.com/the-tools "no detailed records" Edward Leedskalnin ...
1521:## Fact-check result
1523:**Needs revision.** Most claims accurately report what the 1984 National Register nomination says, but the script sometimes upgrades those retrospective assertions into established facts. The largest problems are the relocation timeline, Bob Biggers’s role, the weakly sourced gate-repair details, the “180 feet of rope” statement, the description of Rock Gate Park as “the castle’s archive,” and the final ledger’s overuse of “DOCUMENTED.”
1529:- **CONFIRMED** — supported by a primary record or accurately framed as “the source says.”
1530:- **WRONG** — contradicted, materially misleading, or mathematically incorrect.
1531:- **UNSURE** — plausible, but the available evidence is retrospective, conflicting, or does not prove the claim.
1533:## Priority findings
1535:### Relocation: 1936, 1937, or 1939?
1539:| He bought the new ten-acre property in the mid-1930s | **CONFIRMED** | The current Coral Castle history says he decided to move in 1935 and purchased the tract by 1936. |
1540:| “The form says 1937” | **CONFIRMED** as an attribution | The nomination marks “moved date 1937” and says he decided to relocate in 1937. |
1541:| The actual relocation occurred in 1937 | **WRONG / unsupported** | The same nomination reproduces the obelisk inscription “Moved in 1939” and cites an August 1939 article about the move. The castle’s newer chronology says land clearing began in May 1939 and contemporary coverage described the move that summer. The form is internally inconsistent. |
1542:| “Moved in 1939” is inscribed on the obelisk | **CONFIRMED** | The nomination transcribes: “Made in 1928. Moved in 1939. Born 1887. Latvia, E.L.” [NPS nomination](https://npgallery.nps.gov/GetAsset/1ed2ccd0-b692-42dc-b28d-1227c1a23407/). |
1543:| Move began about 1936 and lasted about three years | **UNSURE** | This appears to have arisen by combining the 1936 purchase with the 1939 inscription. The newer castle chronology instead places preparatory clearing and active relocation in 1939. |
1544:| On-screen `1936–40 ... about three years of moving` | **WRONG** | No reviewed source establishes that range, and “about three years” does not match `1936–40`. |
1545:| Best usable chronology | **CONFIRMED with qualification** | “He acquired the new land by 1936; the 1984 nomination gives 1937, but contemporary-moving evidence and his obelisk point to active relocation in 1939.” |
1549:### Bob Biggers and the truck
1553:| Bob Biggers “lent his truck” | **WRONG / materially incomplete** | The nomination says Ed wanted the use of Biggers’s truck, but the castle’s fuller account says Bob came and pulled the loaded trailer between sites. He was therefore the hauling driver/operator, not merely a passive lender. |
1554:| Ed loaded and unloaded the stones alone and at night | **UNSURE** | This is what the nomination and later oral-history accounts say, but it is not demonstrated by a contemporary eyewitness record reviewed here. |
1555:| The move was completed “without any assistance” | **WRONG if read literally** | Bob’s transportation role is assistance. The defensible narrower claim is that Ed reportedly loaded and unloaded the trailer without Bob’s help. |
1556:| Bob Biggers was a local man/farmer | **CONFIRMED** | Consistent across the nomination and castle account. |
1558:Recommended wording: “Bob Biggers hauled the loaded trailer between sites; later accounts say Ed loaded and unloaded the stones alone, usually at night.”
1560:### Gate repair
1564:| Gate dimensions: 81 × 92 × 21 inches | **CONFIRMED as the nomination’s figures** | Stated twice in the nomination. |
1565:| Nine-ton weight | **UNSURE** | It is the traditional/National Register figure, but no weighing or derivation was found, and it conflicts with the published dimensions and plausible material densities. |
1566:| Central shaft/automobile axle and truck bearing | **CONFIRMED** | The nomination describes an automobile axle; later repair accounts describe a truck bearing. |
1567:| Could be moved with one finger | **CONFIRMED historically; WRONG in present tense** | The nomination records this before the failure. “One finger moves it” should be “it was reported to turn with one finger.” |
1568:| Gate stopped in 1986 | **UNSURE** | A 1990 newspaper retrospective says 1986, but Coral Castle’s present website says 1984. |
1569:| Six men and a 50-short-ton crane | **UNSURE** | A 1990 newspaper supports exactly six men and a 50-ton crane, but other accounts say five workers and a 20-ton crane; Coral Castle says only “six men and a crane.” Treat it as a widely repeated repair account, not settled fact. [1990 Hollywood Sun](https://digitalarchives.broward.org/digital/collection/p16146coll7/id/44746/) |
1570:| Rusted bearing caused the failure | **CONFIRMED as the reported repair finding** | Consistent across the official castle account and later descriptions. |
1571:| Reset on July 23, 1986 | **UNSURE** | The exact date traces online mainly to Wikipedia, whose cited source is a 2006 YouTube video—not a contemporary repair record. |
1572:| Failed again in 2005 | **UNSURE** | Repeated by Wikipedia without a distinct supporting citation. A December 2003 *Wired* report already described a recent removal and reseating, so the repair history is more complicated than the script suggests. [Wired](https://www.wired.com/2003/12/secret-energy-haunts-coral-castle/) |
1573:| No longer rotates as smoothly | **UNSURE but plausible** | Repeated in later visitor and encyclopedia accounts; not supported here by a repair report or measurement. |
1575:The scene’s `DOCUMENTED` label is too strong for the entire repair block. Use **“REPORTED: 1986 REPAIR ACCOUNTS”** and mark the exact July date and 2005 failure as unverified.
1577:### Gate-volume arithmetic
1581:| `81 × 92 × 21 = 156,492 in³` | **CONFIRMED** |
1582:| `156,492 in³ = 90.6 ft³` | **CONFIRMED** | Exact result: 90.5625 ft³. |
1583:| Calcite density 2.71 g/cm³ | **CONFIRMED** | USGS commonly uses 2.72; 2.71 is a standard mineral value. |
1584:| Aragonite density 2.93 g/cm³ | **CONFIRMED** | USGS assigns 2.93 g/cm³. [USGS density discussion](https://pubs.usgs.gov/of/1987/0665/report.pdf) |
1585:| Solid-calcite result ≈7.7 short tons | **CONFIRMED** | Approximately 7.66 tons. |
1586:| Solid-aragonite result ≈8.3 short tons | **CONFIRMED** | Approximately 8.29 tons. |
1587:| Thirty-percent-pore dry results ≈5.4/5.8 tons | **CONFIRMED mathematically** | These assume empty/dry pore volume. Water-filled pores would increase the mass. |
1588:| Thirty-percent porosity is plausible | **CONFIRMED as a plausible scenario, not the gate’s measured porosity** | USGS found substantial and variable porosity in hundreds of Miami Limestone samples. [USGS OFR 85-21](https://pubs.usgs.gov/of/1985/0021/report.pdf) |
1589:| “Even solid aragonite, the densest the rock could be” | **WRONG** | Aragonite is a useful conservative carbonate end member, but not an absolute maximum for every possible mineral inclusion or water-filled rock. Say “even treating the entire rectangular volume as solid aragonite.” |
1590:| “Real oolite is porous” | **CONFIRMED** |
1591:| “Nine tons is probably a rounded figure, not a weighing” | **UNSURE but reasonable inference** | The discrepancy makes that likely, but no record of how the nine-ton number was obtained was found. |
1592:| “If ton means metric…” | **WRONG / misleading** | In this American nomination, surrounded by pound figures, “ton” almost certainly means a 2,000-pound short ton. The metric scenario adds confusion without evidentiary value. |
1593:| Volume calculation represents the exact gate | **UNSURE** | It treats the stated maximum dimensions as a full rectangular prism. Any irregular faces, holes, or rounded edges reduce volume. |
1597:### The 1,100-ton figure
1601:| Coral Castle currently states 1,100 tons | **CONFIRMED** | [Official Coral Castle page](https://coralcastle.com/home/the-secrets-of-coral-castle/). |
1602:| Wikipedia states 1,100 short tons | **CONFIRMED** |
1603:| Wikipedia supplies a source for the total | **WRONG** | Its current 1,100-ton sentence has no citation attached. |
1604:| The 1984 nomination gives no overall total | **CONFIRMED** |
1605:| 1,100 is an independently established total | **UNSURE** | No inventory, survey, scale record, or documented calculation was located. |
1606:| “The castle’s own figure” | **CONFIRMED only in the sense that the present operator promotes it** | It should not imply that Leedskalnin or an engineer calculated it. |
1607:| First estimator not found | **CONFIRMED as the research result** | The search did not identify one. |
1608:| Carroll A. Lake may be the source of exactly 1,100 tons | **WRONG** | Lake’s mid-1950s account says “over 1000 tons”; another passage says roughly 1,000 tons in the wall/castle plus nearly half again in furniture. It does not provide a clean 1,100-ton calculation and is internally inconsistent. [Lake text](https://magneticuniverse.com/uploads/FileUpload/31/21d96d1d17317ae587ef3fa556b1c2.pdf) |
1609:| Earliest exact 1,100-ton estimate | **UNSURE** | Exact “1,100” appears in later promotional material, but the first use could not be dated. An undated/modern-scanned Coral Castle brochure uses it; a searchable 1998 Usenet repost also contains it. Neither identifies an estimator. |
1611:Best conclusion: **Carroll A. Lake is the earliest quantitative lead located—“over 1,000 tons,” circa the mid-1950s—but he is not shown to be the originator of the exact 1,100-ton figure.**
1613:### Block and tackle and lever calculations
1617:| Ideal mechanical advantage equals the supporting rope segments | **CONFIRMED for a simple block-and-tackle correctly rigged** |
1618:| 20,000 ÷ 6 = 3,333 lb | **CONFIRMED** |
1619:| Two properly compounded 6:1 systems produce ideal 36:1 | **CONFIRMED conditionally** | They must actually be cascaded so one system pulls the other; merely placing two tackle sets together does not automatically multiply them. |
1620:| 20,000 ÷ 36 ≈556 lb | **CONFIRMED** |
1621:| Adding an ideal 5:1 winch gives total 180:1 and ≈111 lb input | **CONFIRMED conditionally** | This is an ideal speed/force-ratio example, not evidence about Ed’s equipment. |
1622:| “Which one person can pull” | **UNSURE** | A 111-pound sustained pull is substantial; friction, rope stiffness, sheave losses, startup loads, structure stability, and safety margins could raise it greatly. |
1623:| “180 ft of rope per 1 ft lift” after adding the winch | **WRONG** | The 36:1 tackle requires roughly 36 feet of tackle-rope travel per foot of lift. A 5:1 winch makes the operator’s handle/input travel roughly five times the drum-rope travel—about 180 feet of equivalent input motion—not 180 feet of rope hauled through the tackle. [Pulley-system explanation](https://www.cmcpro.com/pulleys-and-mechanical-advantage-systems/) |
1624:| Friction is ignored | **CONFIRMED and properly disclosed** |
1625:| 9:1 lever: `100 lb × 9 ft = 900 lb × 1 ft` | **CONFIRMED as ideal statics** |
1626:| That example can raise the preceding ten-ton block | **WRONG if implied** | Nine hundred pounds of ideal output cannot raise a 20,000-pound load. The lever drawing must be presented as an unrelated principle example or use a much larger ratio/effort. |
1627:| “Raise an inch, crib, repeat” | **CONFIRMED as a real technique in general** | It does not prove Leedskalnin used that exact procedure on the largest blocks. |
1629:## Remaining narration and screen claims
1633:| **s1:** Leedskalnin lived 1887–1951 | **CONFIRMED** |
1634:| He worked on the structures from 1923 until his death | **CONFIRMED broadly** |
1635:| He alone cut, moved, and erected every stone | **UNSURE** | Widely attested, including affidavits, but not proved lift-by-lift; Bob Biggers assisted with transport. |
1636:| **s2:** Born in Latvia in 1887 | **CONFIRMED** |
1637:| Engagement at about 26 to Agnes, ten years younger; she ended it | **CONFIRMED only as the 1984 nomination’s account** |
1638:| He called the real Agnes “Sweet Sixteen” | **UNSURE** | His writing uses “Sweet Sixteen,” but whether it identifies the historically disputed fiancée is uncertain. |
1639:| Work across North America, illness, early-1920s Florida arrival | **CONFIRMED as the nomination’s biography; independently incomplete** |
1640:| **s3:** Scuff/Skuvst spellings and conflicting Latvian name/age | **CONFIRMED** |
1641:| The love-story motive comes from later tellings | **CONFIRMED** |
1642:| **s4:** 1923 purchase of one acre for $12 | **CONFIRMED by the nomination’s deed citation** |
1643:| Ground was oolitic limestone called coral rock | **CONFIRMED** |
1644:| Shed, tower, wall, furniture, astronomical pieces | **CONFIRMED broadly** |
1645:| On-screen “sundial?” at the original site | **UNSURE** | Appropriately marked with a question mark. |
1646:| **s6:** Polaris 40,000 lb; quarter moons 36,000 each; full-moon fountain 46,000; obelisk 57,000; north-wall sculpture 30 tons | **CONFIRMED as figures printed in the nomination** | They are not independently verified measurements. |
1647:| Polaris slab was 25 feet tall | **CONFIRMED as the form’s figure** |
1648:| Wall blocks 8 × 4 × 3 feet, “several tons” | **CONFIRMED as the form’s description** |
1649:| Mars and Saturn 36,000 lb each | **CONFIRMED as the form’s figures** |
1650:| **s10:** Tools listed in the form | **CONFIRMED** |
1651:| Some quarrying/sculpting tools fashioned from old automobile parts | **CONFIRMED as the form’s account** |
1652:| Historical photographs show tall wooden tripod-like frames and suspended lifting gear | **CONFIRMED** | Florida Memory catalogs a circa-1936 photograph with hoisting equipment. [Florida Memory results](https://floridamemory.com/find?advanced%5B0%5D%5Belement_id%5D=240&advanced%5B0%5D%5Bjoiner%5D=and&advanced%5B0%5D%5Bterms%5D=11&advanced%5B0%5D%5Btype%5D=is+exactly&advanced%5B1%5D%5Belement_id%5D=49&advanced%5B1%5D%5Bjoiner%5D=and&advanced%5B1%5D%5Bterms%5D=Historic+sites--Florida--Homestead&advanced%5B1%5D%5Btype%5D=is+exactly&layout=1&order=d&query=&sort=43) |
1653:| Rockgatepark.com is “the castle’s archive” | **WRONG** | The site explicitly says it is an independent archive, not affiliated with Coral Castle. [Rock Gate Park notice](https://www.rockgatepark.com/) |
1654:| No detailed record of the exact rig configuration/procedure | **CONFIRMED as the independent archive’s conclusion** | Avoid presenting that conclusion as an official institutional finding. |
1655:| **s13:** Over 250 affidavits were collected in 1955 | **CONFIRMED** |
1656:| Julius Levin collected them | **CONFIRMED** | The nomination’s pronoun refers back to Levin. |
1657:| Levin was the then owner, having purchased in 1953 | **CONFIRMED by the nomination** |
1658:| Affiants were Homestead-area residents acquainted with Ed | **CONFIRMED** |
1659:| Affidavits said he worked without other individuals and with simple hand tools | **CONFIRMED as their sworn wording** |
1660:| They were notarized by Bodil K. Lowe | **CONFIRMED** |
1661:| The nomination quotes no named witness to a specific largest-block lift | **CONFIRMED** |
1662:| The affidavits prove every large lift was solo | **UNSURE** | Their generic form language does not identify which work each signer personally observed. |
1663:| **s14:** “Pyramid builders” and “laws of leverage and weight” | **CONFIRMED as the nomination’s paraphrase** | Correctly not presented as a verbatim Ed quotation. |
1664:| No Leedskalnin-authored document describes the lifting process | **CONFIRMED within the reviewed writings** |
1665:| *A Book in Every Home* — 1936 | **CONFIRMED** |
1666:| *Magnetic Current* — August 1945, Franklin Press | **CONFIRMED** | The surviving text itself says copyright August 1945. [Text](https://www.leedskalnin.com/Leedskalnins-Writings-MAGNETIC-CURRENT.html) |
1667:| *Mineral, Vegetable and Animal Life* — October 1945, Franklin Press | **CONFIRMED** |
1668:| *Magnetic Current* concerns magnets/electricity | **CONFIRMED** |
1669:| None of those works explains how the stones were lifted | **CONFIRMED** |
1670:| **s15:** Extraterrestrial and gravity/weightlessness stories existed by 1984 | **CONFIRMED** | The nomination records both. |
1671:| Sound levitation was already among the theories by 1984 | **UNSURE** | It is not one of the theories named in the nomination. |
1672:| Magnetism “cancelled weight” is what his pamphlets claim | **WRONG** | The pamphlets advance unconventional magnetic theories, but they do not state a stone-lifting or weight-cancellation method. |
1673:| Floating-stone stories are secondhand | **CONFIRMED** |
1674:| No measurement, recording, or physical trace was found for exotic lifting | **CONFIRMED within this review’s evidence** |
1675:| “Not established, not impossible/not ruled out” | **WRONG / editorially misleading** | Absence of proof does not place conventional rigging and extraordinary levitation on equal evidentiary footing. Say “unsupported; available physical evidence points to conventional rigging.” |
1676:| **s16:** “Documented: the dates” | **WRONG** | The dates conflict materially. |
1677:| “Documented: the move” | **UNSURE as phrased** | The relocation is established, but its exact schedule and the solo-loading claim are not. |
1678:| “Documented: the form’s weights” | **CONFIRMED only if explicitly meaning the form prints those estimates** |
1679:| “Documented: the 1986 repair” | **WRONG / too strong** | Important details conflict or derive from poorly sourced later accounts. |
1680:| Worked alone / pyramid knowledge / 1,100 tons are claims | **CONFIRMED categorization** |
1681:| Gate’s true weight is unsettled | **CONFIRMED categorization** |
1682:| Exact largest-block lifting procedures are unknown | **CONFIRMED, although conventional lifting equipment is documented** |
1683:| **s17:** Patient work and simple machines fit the evidence | **CONFIRMED as a reasonable inference** |
1684:| Stranger mechanisms remain equally viable | **WRONG / unsupported framing** |
1686:## SOURCES.md and end-card corrections
1688:- **CONFIRMED:** Nomination prepared by Maria Temkin and Michael Zimny on April 2, 1984; listed May 10, 1984; reference 84000840. The 2011 correspondence requests and supports changing the official name from Rock Gate to Coral Castle. [NPS record](https://npgallery.nps.gov/AssetDetail/1ed2ccd0-b692-42dc-b28d-1227c1a23407/)
1690:- **CONFIRMED:** The nomination title fields read historic “Rock Gate (Ed’s Place)” and common “Coral Castle.”
1692:- **WRONG:** “Wikipedia … 1986 repair, 2005 failure” on the end card makes Wikipedia look like adequate verification. Its exact July-date citation is merely a 2006 YouTube upload, and the 2005 sentence has no separate citation.
1694:- **WRONG:** `rockgatepark.com/the-tools` is described in narration as “the castle’s archive.” It is independent and expressly unaffiliated.
1696:- **UNSURE:** Florida Memory’s circa-1936 catalog date for Homestead hoisting photographs conflicts with the stronger evidence placing relocation activity in 1939. The photograph exists; the date/location metadata should be qualified.
1698:- **WRONG:** `Status as of October 2026` suggests a live status check of every physical feature. The audit did not establish the gate’s current operational state.
1700:## Recommended minimum revisions
1702:1. Replace the move scene with the 1936 land-purchase/1939 active-move chronology and explicitly call the form’s 1937 entry inconsistent.
1703:2. Say Bob Biggers hauled the trailer; qualify the solo loading/unloading as a later account.
1704:3. Relabel the gate repair **REPORTED**, omit the exact July 23 date and 2005 failure unless a contemporary repair record is obtained.
1706:5. Preserve the gate calculation but say “full rectangular solid-aragonite upper-case model”; remove the metric-ton aside.
1707:6. Change “180 feet of rope” to “36 feet of tackle-rope travel, or about 180 feet of idealized operator-input travel after a 5:1 winch.”
1710:9. Describe all listed stone weights as **the nomination’s published estimates**, not verified weights.
1711:10. Keep 1,100 tons explicitly untraced; note that Carroll Lake supplied an earlier “over 1,000 tons” claim but not the exact 1,100 figure.
1716:## Fact-check result
1718:**Needs revision.** Most claims accurately report what the 1984 National Register nomination says, but the script sometimes upgrades those retrospective assertions into established facts. The largest problems are the relocation timeline, Bob Biggers’s role, the weakly sourced gate-repair details, the “180 feet of rope” statement, the description of Rock Gate Park as “the castle’s archive,” and the final ledger’s overuse of “DOCUMENTED.”
1724:- **CONFIRMED** — supported by a primary record or accurately framed as “the source says.”
1725:- **WRONG** — contradicted, materially misleading, or mathematically incorrect.
1726:- **UNSURE** — plausible, but the available evidence is retrospective, conflicting, or does not prove the claim.
1728:## Priority findings
1730:### Relocation: 1936, 1937, or 1939?
1734:| He bought the new ten-acre property in the mid-1930s | **CONFIRMED** | The current Coral Castle history says he decided to move in 1935 and purchased the tract by 1936. |
1735:| “The form says 1937” | **CONFIRMED** as an attribution | The nomination marks “moved date 1937” and says he decided to relocate in 1937. |
1736:| The actual relocation occurred in 1937 | **WRONG / unsupported** | The same nomination reproduces the obelisk inscription “Moved in 1939” and cites an August 1939 article about the move. The castle’s newer chronology says land clearing began in May 1939 and contemporary coverage described the move that summer. The form is internally inconsistent. |
1737:| “Moved in 1939” is inscribed on the obelisk | **CONFIRMED** | The nomination transcribes: “Made in 1928. Moved in 1939. Born 1887. Latvia, E.L.” [NPS nomination](https://npgallery.nps.gov/GetAsset/1ed2ccd0-b692-42dc-b28d-1227c1a23407/). |
1738:| Move began about 1936 and lasted about three years | **UNSURE** | This appears to have arisen by combining the 1936 purchase with the 1939 inscription. The newer castle chronology instead places preparatory clearing and active relocation in 1939. |
1739:| On-screen `1936–40 ... about three years of moving` | **WRONG** | No reviewed source establishes that range, and “about three years” does not match `1936–40`. |
1740:| Best usable chronology | **CONFIRMED with qualification** | “He acquired the new land by 1936; the 1984 nomination gives 1937, but contemporary-moving evidence and his obelisk point to active relocation in 1939.” |
1744:### Bob Biggers and the truck
1748:| Bob Biggers “lent his truck” | **WRONG / materially incomplete** | The nomination says Ed wanted the use of Biggers’s truck, but the castle’s fuller account says Bob came and pulled the loaded trailer between sites. He was therefore the hauling driver/operator, not merely a passive lender. |
1749:| Ed loaded and unloaded the stones alone and at night | **UNSURE** | This is what the nomination and later oral-history accounts say, but it is not demonstrated by a contemporary eyewitness record reviewed here. |
1750:| The move was completed “without any assistance” | **WRONG if read literally** | Bob’s transportation role is assistance. The defensible narrower claim is that Ed reportedly loaded and unloaded the trailer without Bob’s help. |
1751:| Bob Biggers was a local man/farmer | **CONFIRMED** | Consistent across the nomination and castle account. |
1753:Recommended wording: “Bob Biggers hauled the loaded trailer between sites; later accounts say Ed loaded and unloaded the stones alone, usually at night.”
1755:### Gate repair
1759:| Gate dimensions: 81 × 92 × 21 inches | **CONFIRMED as the nomination’s figures** | Stated twice in the nomination. |
1760:| Nine-ton weight | **UNSURE** | It is the traditional/National Register figure, but no weighing or derivation was found, and it conflicts with the published dimensions and plausible material densities. |
1761:| Central shaft/automobile axle and truck bearing | **CONFIRMED** | The nomination describes an automobile axle; later repair accounts describe a truck bearing. |
1762:| Could be moved with one finger | **CONFIRMED historically; WRONG in present tense** | The nomination records this before the failure. “One finger moves it” should be “it was reported to turn with one finger.” |
1763:| Gate stopped in 1986 | **UNSURE** | A 1990 newspaper retrospective says 1986, but Coral Castle’s present website says 1984. |
1764:| Six men and a 50-short-ton crane | **UNSURE** | A 1990 newspaper supports exactly six men and a 50-ton crane, but other accounts say five workers and a 20-ton crane; Coral Castle says only “six men and a crane.” Treat it as a widely repeated repair account, not settled fact. [1990 Hollywood Sun](https://digitalarchives.broward.org/digital/collection/p16146coll7/id/44746/) |
1765:| Rusted bearing caused the failure | **CONFIRMED as the reported repair finding** | Consistent across the official castle account and later descriptions. |
1766:| Reset on July 23, 1986 | **UNSURE** | The exact date traces online mainly to Wikipedia, whose cited source is a 2006 YouTube video—not a contemporary repair record. |
1767:| Failed again in 2005 | **UNSURE** | Repeated by Wikipedia without a distinct supporting citation. A December 2003 *Wired* report already described a recent removal and reseating, so the repair history is more complicated than the script suggests. [Wired](https://www.wired.com/2003/12/secret-energy-haunts-coral-castle/) |
1768:| No longer rotates as smoothly | **UNSURE but plausible** | Repeated in later visitor and encyclopedia accounts; not supported here by a repair report or measurement. |
1770:The scene’s `DOCUMENTED` label is too strong for the entire repair block. Use **“REPORTED: 1986 REPAIR ACCOUNTS”** and mark the exact July date and 2005 failure as unverified.
1772:### Gate-volume arithmetic
1776:| `81 × 92 × 21 = 156,492 in³` | **CONFIRMED** |
1777:| `156,492 in³ = 90.6 ft³` | **CONFIRMED** | Exact result: 90.5625 ft³. |
1778:| Calcite density 2.71 g/cm³ | **CONFIRMED** | USGS commonly uses 2.72; 2.71 is a standard mineral value. |
1779:| Aragonite density 2.93 g/cm³ | **CONFIRMED** | USGS assigns 2.93 g/cm³. [USGS density discussion](https://pubs.usgs.gov/of/1987/0665/report.pdf) |
1780:| Solid-calcite result ≈7.7 short tons | **CONFIRMED** | Approximately 7.66 tons. |
1781:| Solid-aragonite result ≈8.3 short tons | **CONFIRMED** | Approximately 8.29 tons. |
1782:| Thirty-percent-pore dry results ≈5.4/5.8 tons | **CONFIRMED mathematically** | These assume empty/dry pore volume. Water-filled pores would increase the mass. |
1783:| Thirty-percent porosity is plausible | **CONFIRMED as a plausible scenario, not the gate’s measured porosity** | USGS found substantial and variable porosity in hundreds of Miami Limestone samples. [USGS OFR 85-21](https://pubs.usgs.gov/of/1985/0021/report.pdf) |
1784:| “Even solid aragonite, the densest the rock could be” | **WRONG** | Aragonite is a useful conservative carbonate end member, but not an absolute maximum for every possible mineral inclusion or water-filled rock. Say “even treating the entire rectangular volume as solid aragonite.” |
1785:| “Real oolite is porous” | **CONFIRMED** |
1786:| “Nine tons is probably a rounded figure, not a weighing” | **UNSURE but reasonable inference** | The discrepancy makes that likely, but no record of how the nine-ton number was obtained was found. |
1787:| “If ton means metric…” | **WRONG / misleading** | In this American nomination, surrounded by pound figures, “ton” almost certainly means a 2,000-pound short ton. The metric scenario adds confusion without evidentiary value. |
1788:| Volume calculation represents the exact gate | **UNSURE** | It treats the stated maximum dimensions as a full rectangular prism. Any irregular faces, holes, or rounded edges reduce volume. |
1792:### The 1,100-ton figure
1796:| Coral Castle currently states 1,100 tons | **CONFIRMED** | [Official Coral Castle page](https://coralcastle.com/home/the-secrets-of-coral-castle/). |
1797:| Wikipedia states 1,100 short tons | **CONFIRMED** |
1798:| Wikipedia supplies a source for the total | **WRONG** | Its current 1,100-ton sentence has no citation attached. |
1799:| The 1984 nomination gives no overall total | **CONFIRMED** |
1800:| 1,100 is an independently established total | **UNSURE** | No inventory, survey, scale record, or documented calculation was located. |
1801:| “The castle’s own figure” | **CONFIRMED only in the sense that the present operator promotes it** | It should not imply that Leedskalnin or an engineer calculated it. |
1802:| First estimator not found | **CONFIRMED as the research result** | The search did not identify one. |
1803:| Carroll A. Lake may be the source of exactly 1,100 tons | **WRONG** | Lake’s mid-1950s account says “over 1000 tons”; another passage says roughly 1,000 tons in the wall/castle plus nearly half again in furniture. It does not provide a clean 1,100-ton calculation and is internally inconsistent. [Lake text](https://magneticuniverse.com/uploads/FileUpload/31/21d96d1d17317ae587ef3fa556b1c2.pdf) |
1804:| Earliest exact 1,100-ton estimate | **UNSURE** | Exact “1,100” appears in later promotional material, but the first use could not be dated. An undated/modern-scanned Coral Castle brochure uses it; a searchable 1998 Usenet repost also contains it. Neither identifies an estimator. |
1806:Best conclusion: **Carroll A. Lake is the earliest quantitative lead located—“over 1,000 tons,” circa the mid-1950s—but he is not shown to be the originator of the exact 1,100-ton figure.**
1808:### Block and tackle and lever calculations
1812:| Ideal mechanical advantage equals the supporting rope segments | **CONFIRMED for a simple block-and-tackle correctly rigged** |
1813:| 20,000 ÷ 6 = 3,333 lb | **CONFIRMED** |
1814:| Two properly compounded 6:1 systems produce ideal 36:1 | **CONFIRMED conditionally** | They must actually be cascaded so one system pulls the other; merely placing two tackle sets together does not automatically multiply them. |
1815:| 20,000 ÷ 36 ≈556 lb | **CONFIRMED** |
1816:| Adding an ideal 5:1 winch gives total 180:1 and ≈111 lb input | **CONFIRMED conditionally** | This is an ideal speed/force-ratio example, not evidence about Ed’s equipment. |
1817:| “Which one person can pull” | **UNSURE** | A 111-pound sustained pull is substantial; friction, rope stiffness, sheave losses, startup loads, structure stability, and safety margins could raise it greatly. |
1818:| “180 ft of rope per 1 ft lift” after adding the winch | **WRONG** | The 36:1 tackle requires roughly 36 feet of tackle-rope travel per foot of lift. A 5:1 winch makes the operator’s handle/input travel roughly five times the drum-rope travel—about 180 feet of equivalent input motion—not 180 feet of rope hauled through the tackle. [Pulley-system explanation](https://www.cmcpro.com/pulleys-and-mechanical-advantage-systems/) |
1819:| Friction is ignored | **CONFIRMED and properly disclosed** |
1820:| 9:1 lever: `100 lb × 9 ft = 900 lb × 1 ft` | **CONFIRMED as ideal statics** |
1821:| That example can raise the preceding ten-ton block | **WRONG if implied** | Nine hundred pounds of ideal output cannot raise a 20,000-pound load. The lever drawing must be presented as an unrelated principle example or use a much larger ratio/effort. |
1822:| “Raise an inch, crib, repeat” | **CONFIRMED as a real technique in general** | It does not prove Leedskalnin used that exact procedure on the largest blocks. |
1824:## Remaining narration and screen claims
1828:| **s1:** Leedskalnin lived 1887–1951 | **CONFIRMED** |
1829:| He worked on the structures from 1923 until his death | **CONFIRMED broadly** |
1830:| He alone cut, moved, and erected every stone | **UNSURE** | Widely attested, including affidavits, but not proved lift-by-lift; Bob Biggers assisted with transport. |
1831:| **s2:** Born in Latvia in 1887 | **CONFIRMED** |
1832:| Engagement at about 26 to Agnes, ten years younger; she ended it | **CONFIRMED only as the 1984 nomination’s account** |
1833:| He called the real Agnes “Sweet Sixteen” | **UNSURE** | His writing uses “Sweet Sixteen,” but whether it identifies the historically disputed fiancée is uncertain. |
1834:| Work across North America, illness, early-1920s Florida arrival | **CONFIRMED as the nomination’s biography; independently incomplete** |
1835:| **s3:** Scuff/Skuvst spellings and conflicting Latvian name/age | **CONFIRMED** |
1836:| The love-story motive comes from later tellings | **CONFIRMED** |
1837:| **s4:** 1923 purchase of one acre for $12 | **CONFIRMED by the nomination’s deed citation** |
1838:| Ground was oolitic limestone called coral rock | **CONFIRMED** |
1839:| Shed, tower, wall, furniture, astronomical pieces | **CONFIRMED broadly** |
1840:| On-screen “sundial?” at the original site | **UNSURE** | Appropriately marked with a question mark. |
1841:| **s6:** Polaris 40,000 lb; quarter moons 36,000 each; full-moon fountain 46,000; obelisk 57,000; north-wall sculpture 30 tons | **CONFIRMED as figures printed in the nomination** | They are not independently verified measurements. |
1842:| Polaris slab was 25 feet tall | **CONFIRMED as the form’s figure** |
1843:| Wall blocks 8 × 4 × 3 feet, “several tons” | **CONFIRMED as the form’s description** |
1844:| Mars and Saturn 36,000 lb each | **CONFIRMED as the form’s figures** |
1845:| **s10:** Tools listed in the form | **CONFIRMED** |
1846:| Some quarrying/sculpting tools fashioned from old automobile parts | **CONFIRMED as the form’s account** |
1847:| Historical photographs show tall wooden tripod-like frames and suspended lifting gear | **CONFIRMED** | Florida Memory catalogs a circa-1936 photograph with hoisting equipment. [Florida Memory results](https://floridamemory.com/find?advanced%5B0%5D%5Belement_id%5D=240&advanced%5B0%5D%5Bjoiner%5D=and&advanced%5B0%5D%5Bterms%5D=11&advanced%5B0%5D%5Btype%5D=is+exactly&advanced%5B1%5D%5Belement_id%5D=49&advanced%5B1%5D%5Bjoiner%5D=and&advanced%5B1%5D%5Bterms%5D=Historic+sites--Florida--Homestead&advanced%5B1%5D%5Btype%5D=is+exactly&layout=1&order=d&query=&sort=43) |
1848:| Rockgatepark.com is “the castle’s archive” | **WRONG** | The site explicitly says it is an independent archive, not affiliated with Coral Castle. [Rock Gate Park notice](https://www.rockgatepark.com/) |
1849:| No detailed record of the exact rig configuration/procedure | **CONFIRMED as the independent archive’s conclusion** | Avoid presenting that conclusion as an official institutional finding. |
1850:| **s13:** Over 250 affidavits were collected in 1955 | **CONFIRMED** |
1851:| Julius Levin collected them | **CONFIRMED** | The nomination’s pronoun refers back to Levin. |
1852:| Levin was the then owner, having purchased in 1953 | **CONFIRMED by the nomination** |
1853:| Affiants were Homestead-area residents acquainted with Ed | **CONFIRMED** |
1854:| Affidavits said he worked without other individuals and with simple hand tools | **CONFIRMED as their sworn wording** |
1855:| They were notarized by Bodil K. Lowe | **CONFIRMED** |
1856:| The nomination quotes no named witness to a specific largest-block lift | **CONFIRMED** |
1857:| The affidavits prove every large lift was solo | **UNSURE** | Their generic form language does not identify which work each signer personally observed. |
1858:| **s14:** “Pyramid builders” and “laws of leverage and weight” | **CONFIRMED as the nomination’s paraphrase** | Correctly not presented as a verbatim Ed quotation. |
1859:| No Leedskalnin-authored document describes the lifting process | **CONFIRMED within the reviewed writings** |
1860:| *A Book in Every Home* — 1936 | **CONFIRMED** |
1861:| *Magnetic Current* — August 1945, Franklin Press | **CONFIRMED** | The surviving text itself says copyright August 1945. [Text](https://www.leedskalnin.com/Leedskalnins-Writings-MAGNETIC-CURRENT.html) |
1862:| *Mineral, Vegetable and Animal Life* — October 1945, Franklin Press | **CONFIRMED** |
1863:| *Magnetic Current* concerns magnets/electricity | **CONFIRMED** |
1864:| None of those works explains how the stones were lifted | **CONFIRMED** |
1865:| **s15:** Extraterrestrial and gravity/weightlessness stories existed by 1984 | **CONFIRMED** | The nomination records both. |
1866:| Sound levitation was already among the theories by 1984 | **UNSURE** | It is not one of the theories named in the nomination. |
1867:| Magnetism “cancelled weight” is what his pamphlets claim | **WRONG** | The pamphlets advance unconventional magnetic theories, but they do not state a stone-lifting or weight-cancellation method. |
1868:| Floating-stone stories are secondhand | **CONFIRMED** |
1869:| No measurement, recording, or physical trace was found for exotic lifting | **CONFIRMED within this review’s evidence** |
1870:| “Not established, not impossible/not ruled out” | **WRONG / editorially misleading** | Absence of proof does not place conventional rigging and extraordinary levitation on equal evidentiary footing. Say “unsupported; available physical evidence points to conventional rigging.” |
1871:| **s16:** “Documented: the dates” | **WRONG** | The dates conflict materially. |
1872:| “Documented: the move” | **UNSURE as phrased** | The relocation is established, but its exact schedule and the solo-loading claim are not. |
1873:| “Documented: the form’s weights” | **CONFIRMED only if explicitly meaning the form prints those estimates** |
1874:| “Documented: the 1986 repair” | **WRONG / too strong** | Important details conflict or derive from poorly sourced later accounts. |
1875:| Worked alone / pyramid knowledge / 1,100 tons are claims | **CONFIRMED categorization** |
1876:| Gate’s true weight is unsettled | **CONFIRMED categorization** |
1877:| Exact largest-block lifting procedures are unknown | **CONFIRMED, although conventional lifting equipment is documented** |
1878:| **s17:** Patient work and simple machines fit the evidence | **CONFIRMED as a reasonable inference** |
1879:| Stranger mechanisms remain equally viable | **WRONG / unsupported framing** |
1881:## SOURCES.md and end-card corrections
1883:- **CONFIRMED:** Nomination prepared by Maria Temkin and Michael Zimny on April 2, 1984; listed May 10, 1984; reference 84000840. The 2011 correspondence requests and supports changing the official name from Rock Gate to Coral Castle. [NPS record](https://npgallery.nps.gov/AssetDetail/1ed2ccd0-b692-42dc-b28d-1227c1a23407/)
1885:- **CONFIRMED:** The nomination title fields read historic “Rock Gate (Ed’s Place)” and common “Coral Castle.”
1887:- **WRONG:** “Wikipedia … 1986 repair, 2005 failure” on the end card makes Wikipedia look like adequate verification. Its exact July-date citation is merely a 2006 YouTube upload, and the 2005 sentence has no separate citation.
1889:- **WRONG:** `rockgatepark.com/the-tools` is described in narration as “the castle’s archive.” It is independent and expressly unaffiliated.
1891:- **UNSURE:** Florida Memory’s circa-1936 catalog date for Homestead hoisting photographs conflicts with the stronger evidence placing relocation activity in 1939. The photograph exists; the date/location metadata should be qualified.
1893:- **WRONG:** `Status as of October 2026` suggests a live status check of every physical feature. The audit did not establish the gate’s current operational state.
1895:## Recommended minimum revisions
1897:1. Replace the move scene with the 1936 land-purchase/1939 active-move chronology and explicitly call the form’s 1937 entry inconsistent.
1898:2. Say Bob Biggers hauled the trailer; qualify the solo loading/unloading as a later account.
1899:3. Relabel the gate repair **REPORTED**, omit the exact July 23 date and 2005 failure unless a contemporary repair record is obtained.
1901:5. Preserve the gate calculation but say “full rectangular solid-aragonite upper-case model”; remove the metric-ton aside.
1902:6. Change “180 feet of rope” to “36 feet of tackle-rope travel, or about 180 feet of idealized operator-input travel after a 5:1 winch.”
1905:9. Describe all listed stone weights as **the nomination’s published estimates**, not verified weights.
1906:10. Keep 1,100 tons explicitly untraced; note that Carroll Lake supplied an earlier “over 1,000 tons” claim but not the exact 1,100 figure.

codex
The revisions now clearly distinguish several formerly overstated claims—especially estimates versus weighings, reported repair details, and the independent archive. I’m checking the remaining edge cases: chronology wording, Biggers’s role, the rigging travel terminology, and whether the ledger/theories still overstate parity.
exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command '$s = Get-Content script.json | ConvertFrom-Json; $s | Where-Object { $_.id -in @('"'s5','s6','s7','s8','s9','s10','s11','s15','s16','s17') } | ConvertTo-Json -Depth 4; Write-Output \"--- ep_body relevant lines ---\"; "'$lines=Get-Content ep_body.py; foreach($range in @(@(196,240),@(248,285),@(297,323),@(390,448),@(462,480))){ for($i=$range[0];$i -le $range[1];$i++){ '"'{0}:{1}' -f "'$i,$lines[$i-1] } }' in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 1981ms:
[
    {
        "id":  "s5",
        "text":  "In the mid nineteen thirties he bought ten acres in Homestead, about ten miles north, and decided to take his stone with him. The dates conflict. The form says 1937. The obelisk is inscribed: moved in 1939, and the castle\u0027s own chronology says land clearing began in May 1939. A farmer, Bob Biggers, hauled the stones. Accounts say Ed loaded and unloaded them himself, at night."
    },
    {
        "id":  "s6",
        "text":  "Now the weights, as printed in the 1984 form, in pounds. The Polaris sighting slab: twenty short tons. Each quarter moon: eighteen. The full moon fountain: twenty three. The obelisk: twenty eight and a half. The heaviest it names: thirty tons. The castle\u0027s own site says over twenty one. These are published estimates, not weighings."
    },
    {
        "id":  "s7",
        "text":  "What about the famous total, eleven hundred tons? It appears on the castle\u0027s website and in encyclopedias with no named estimator; the 1984 form gives none. The earliest number we found is over a thousand tons, in a 1950s book by the engineer Carrol Lake. We could not find where eleven hundred first appears. So: a claim, source untraced."
    },
    {
        "id":  "s8",
        "text":  "The best known piece is the gate. A single slab, eighty one inches wide, ninety two tall, twenty one thick, turning on a central shaft that the form says uses an automobile axle. It was reported to turn with one finger. The form calls it nine tons. Accounts say it stopped turning in the mid nineteen eighties, 1984 or 1986. Six men and a crane lifted it out, and a rusted truck bearing was replaced."
    },
    {
        "id":  "s9",
        "text":  "Here is a check anyone can do. Those dimensions come to about ninety cubic feet. Even if the whole rectangle were solid aragonite, it would weigh about eight tons. Real oolite is porous; at an assumed thirty percent, nearer five and a half. So nine tons is probably a rounded figure. Five tons on one finger is still remarkable."
    },
    {
        "id":  "s10",
        "text":  "What tools did he have? The form lists his tools, made partly from old car parts: block and tackle, rollers, jacks, wedges, slings, cables, sledges and chisels. Old photographs show tall wooden tripods with chains, and a chain hoist. An independent archive says no detailed record shows how the rigs were used."
    },
    {
        "id":  "s11",
        "text":  "What can that gear do? Take a ten ton block, twenty thousand pounds. A block and tackle with six rope segments cuts the pull to a sixth: about thirty three hundred pounds. Chain two sets together and it is six times six: about five hundred fifty. Add a five to one winch and it is near one hundred ten pounds. The price is distance: the tackle rope moves thirty six feet per foot of lift, and the winch handle about one hundred eighty. Small force, long time. This is ideal physics, no friction: what is possible, not what he did."
    },
    {
        "id":  "s15",
        "text":  "Then the popular theories. Sound levitation. Magnetism, the subject of his pamphlets, though they do not say so. Help from beyond Earth, or mastered gravity, ideas the 1984 form already records. All are not established. We found no measurement, recording, or physical trace for any, and the floating stone stories are secondhand. Absence of evidence is not proof of absence. So: not established, not impossible."
    },
    {
        "id":  "s16",
        "text":  "So here is the ledger. Documented: the land purchase, the form\u0027s printed weights, the tool list, photographs of hoisting gear. Reported, with conflicts: the move dates, the gate repair. Claimed: that he worked alone, that he knew the pyramid builders\u0027 methods, the eleven hundred ton total. Not settled: the gate\u0027s true weight. Unknown: how he raised the largest blocks, alone."
    },
    {
        "id":  "s17",
        "text":  "Patient work with simple machines fits the tools, the photographs and the physics. Fits is not the same as shown. Could something stranger be going on? Not established. Not ruled out. Someone watching this might be the one who works it out."
    }
]
--- ep_body relevant lines ---
196:
197:def sc_total(cv, t, p):
198:    night(cv, t, 0.4)
199:    x0, y0, x1, y1 = CONT
200:    a = ease(t / 1.2)
201:    big(cv, x0, y0 + 10, '1,100', 220 if L else 200, TXT, a)
202:    mono(cv, x0 + (640 if L else 20), y0 + (150 if L else 270), 'short tons: the castle\'s own total', 30, VIO, a)
203:    tag(cv, x0 + (640 if L else 20), y0 + (210 if L else 330), 'CLAIMED', VIO, ap(t, 's7', 0.3)); tag(cv, x0 + (800 if L else 200), y0 + (210 if L else 330), 'SOURCE UNTRACED', ROSE, ap(t, 's7', 0.55))
204:    ty = y0 + (330 if L else 460)
205:    rows = [('coralcastle.com', 'states "1,100 tons"; no estimator named', 0.15), ('Wikipedia', '1,100 short tons; figure not attributed', 0.3), ('NRHP form, 1984', 'lists pieces "up to 30 tons"; no total', 0.45), ('C. A. Lake, 1950s', 'adds walls and tower: "over 1000 tons"', 0.62), ('first use of "1,100"', 'not found', 0.8)]
206:    for i, (k, v, f) in enumerate(rows):
207:        aa = ap(t, 's7', f); yy = ty + i * (62 if L else 100)
208:        hline(cv, x0, x1, yy - 10, INK2, aa, 1)
209:        mono(cv, x0 + 10, yy + 4, k, 26, CYAN if i < 4 else ROSE, aa)
210:        if L: cv.text((x0 + 380, yy), v, 'sans', 32, TXT if i < 4 else ROSE, 'la', aa)
211:        else: cv.text((x0 + 10, yy + 40), v, 'sans', 32, TXT if i < 4 else ROSE, 'la', aa)
212:
213:def sc_gate(cv, t, p):
214:    night(cv, t, 0.4)
215:    x0, y0, x1, y1 = CONT
216:    tag(cv, x0, y0 - 40, 'DIMENSIONS: NRHP FORM', MINT, ease(t / 0.8)); tag(cv, x0 + 330, y0 - 40, 'REPAIR: REPORTED', CYAN, ap(t, 's8', 0.5))
217:    sc = 3.6 if L else 3.3
218:    gw, gh = 81 * sc, 92 * sc
219:    ex, ey = (x0 + 120, y0 + 60) if L else (x0 + 20, y0 + 20)
220:    a = ease(t / 1.0)
221:    stone(cv, ex, ey + 20, ex + 130, ey + 20 + gh + 30, a, DIM)
222:    stone(cv, ex + 130 + gw, ey + 20, ex + 260 + gw, ey + 20 + gh + 30, a, DIM)
223:    stone(cv, ex, ey - 20, ex + 260 + gw, ey + 20, a, DIM)      # lintel
224:    ga = ap(t, 's8', 0.12)
225:    stone(cv, ex + 130, ey + 22, ex + 130 + gw, ey + 20 + gh + 30, ga, CYAN)
226:    cx = ex + 130 + gw / 2
227:    sa = ap(t, 's8', 0.35)
228:    cv.line([(cx, ey - 20), (cx, ey + 20 + gh + 30)], mix(VIO, BG, sa), 5)
229:    cv.text((cx + 14, ey + 60), 'central shaft', 'mono', 18, VIO, 'la', sa); cv.text((cx + 14, ey + 84), '(auto axle, per form)', 'mono', 18, VIO, 'la', sa)
230:    cv.text((cx, ey + 20 + gh + 66), '81 in wide x 92 in tall x 21 in thick', 'monob', 20, TXT, 'ma', ga)
231:    # top view with swing
232:    tvx, tvy = (ex + 260 + gw + 190, ey + 150) if L else (ex + 260 + gw + 90, ey + 190)
233:    ang = math.radians(75 * (0.5 - 0.5 * math.cos(t * 0.9)))
234:    cv.line([(tvx - 150, tvy), (tvx - 100, tvy)], mix(DIM, BG, a), 8); cv.line([(tvx + 100, tvy), (tvx + 150, tvy)], mix(DIM, BG, a), 8)
235:    r = 100
236:    cv.line([(tvx - r * math.cos(ang), tvy - r * math.sin(ang)), (tvx + r * math.cos(ang), tvy + r * math.sin(ang))], mix(CYAN, BG, ga), 12)
237:    cv.circ((tvx, tvy), 9, mix(VIO, BG, sa)); cv.text((tvx, tvy + 130), 'top view: swings on its center', 'mono', 18, DIM, 'ma', ga)
238:    # 1986 facts
239:    fy = ey + 20 + gh + 130
240:    rows = [('"nine ton" (form): see the next check', 0.35, MINT), ('reported to turn with one finger (form, 1984)', 0.45, MINT), ('mid-1980s: stopped turning, 1984 or 1986 (sources differ)', 0.62, CYAN), ('six men and a crane lifted it out (50-ton in one account); rusted truck bearing replaced', 0.8, CYAN)]
248:def sc_check(cv, t, p):
249:    night(cv, t, 0.4)
250:    x0, y0, x1, y1 = CONT
251:    tag(cv, x0, y0 - 40, 'OUR ARITHMETIC', CYAN, ease(t / 0.8)); tag(cv, x0 + 270, y0 - 40, 'NOT SETTLED: GATE WEIGHT', ROSE, ap(t, 's9', 0.6))
252:    vol_in3 = 81 * 92 * 21; vft = vol_in3 / 1728.0
253:    rows = [('calcite, solid (2.71 g/cm3)', 2.71, 0.0), ('aragonite, solid (2.93 g/cm3)', 2.93, 0.0), ('aragonite, 30% pore space', 2.93 * 0.7, 0.0), ('calcite, 30% pore space', 2.71 * 0.7, 0.0)]
254:    a0 = ap(t, 's9', 0.05)
255:    mono(cv, x0, y0 + 10, f'81 x 92 x 21 in = {vol_in3:,} cubic in = {vft:.1f} cubic ft', 30 if L else 26, TXT, a0)
256:    mono(cv, x0, y0 + 56, '(1 g/cm3 = 62.43 lb/ft3; weight = volume x density)', 20, DIM, a0)
257:    order = [1, 0, 2, 3]; fr = [0.3, 0.38, 0.55, 0.62]
258:    scale_max = 10.0; bx0 = x0 + (500 if L else 0); bw = (x1 - bx0 - 150) if L else (x1 - x0 - 200)
259:    for i, k in enumerate(order):
260:        nm, d, _ = rows[k]; aa = ap(t, 's9', fr[i]); tons = vft * d * 62.428 / 2000.0
261:        yy = y0 + 120 + i * (84 if L else 120)
262:        if aa <= 0: continue
263:        if L: cv.text((x0, yy + 10), nm, 'sans', 28, TXT, 'la', aa); by = yy
264:        else: cv.text((x0, yy), nm, 'sans', 28, TXT, 'la', aa); by = yy + 40
265:        wl = bw * tons / scale_max * ease((t - F('s9', fr[i])) / 1.0)
266:        col = ROSE if i < 2 else MINT
267:        cv.rect((bx0, by, bx0 + wl, by + 44), mix(col, BG, aa * 0.8)); cv.text((bx0 + wl + 14, by + 22), f'{tons:.1f} short tons', 'monob', 24, TXT, 'lm', aa)
268:    ua = ap(t, 's9', 0.45)
269:    ux = bx0 + bw * 0.9
270:    ytop = y0 + 100; ybot = y0 + 120 + 4 * (84 if L else 120)
271:    cv.line([(ux, ytop), (ux, ybot)], mix(VIO, BG, ua), 3); cv.text((ux, ytop - 8), 'form: "nine ton"', 'monob', 22, VIO, 'ms', ua)
272:    mono(cv, x0, ybot + 20, 'densities: standard mineral values. 30% porosity is our assumption.', 20, DIM, ap(t, 's9', 0.7))
273:    mono(cv, x0, ybot + 50, 'full rectangle assumed, dry rock; a 1950s engineer\'s book gives other dimensions (about 7 x 5 x 3 ft)', 20, DIM, ap(t, 's9', 0.82))
274:
275:def sc_tools(cv, t, p):
276:    night(cv, t, 0.5)
277:    x0, y0, x1, y1 = CONT
278:    lift = 0.35 + 0.3 * math.sin(t * 0.4)
279:    if L: tripod(cv, x0 + 330, y0 + 570, 520, ease(t / 1.0), lift, math.sin(t * 0.6))
280:    else: tripod(cv, x1 - 200, y0 + 330, 300, ease(t / 1.0), lift, math.sin(t * 0.6))
281:    tx = x0 + (720 if L else 0); ty = y0 + (0 if L else 360)
282:    rows = [('DOCUMENTED', MINT, 'tools on display (NRHP 1984): block and tackle ("metal fall"), rollers, jacks, wedges, slings, cables, sledges, chisels; some made from old car parts', 0.15),
283:            ('DOCUMENTED', MINT, 'old photographs show tall wooden tripods with chains, and a chain hoist', 0.5),
284:            ('UNKNOWN', ROSE, 'exact rig set-up and procedures: "no detailed records" (Rock Gate Park, an independent archive site)', 0.78)]
285:    yy = ty
297:def sc_tackle(cv, t, p):
298:    night(cv, t, 0.3)
299:    x0, y0, x1, y1 = CONT
300:    tag(cv, x0, y0 - 40, 'ILLUSTRATION: IDEAL, NO FRICTION', CYAN, ease(t / 0.8), 20)
301:    a = ease(t / 1.0)
302:    dx, dy = (x0 + 220, y0 + 90) if L else (x0 + 220, y0 + 70)
303:    u = 0.5 - 0.5 * math.cos(t * 0.5)
304:    topy = dy; boty = dy + 330 - 150 * u
305:    w = 280
306:    pulley(cv, dx, topy, w, a, DIM)
307:    pulley(cv, dx, boty, w, a, CYAN)
308:    for k in range(6):
309:        xx = dx - w / 2 + 14 + k * (w - 28) / 5
310:        cv.line([(xx, topy + 22), (xx, boty - 22)], mix(TXT, BG, a * 0.7), 2)
311:    cv.line([(dx + w / 2, topy), (dx + w / 2 + 70, topy), (dx + w / 2 + 70, topy + 380 + 30 * u)], mix(VIO, BG, a), 3)
312:    mono(cv, dx + w / 2 + 84, topy + 330, 'pull', 22, VIO, a)
313:    cv.line([(dx, boty + 22), (dx, boty + 70)], mix(TXT, BG, a * 0.7), 2)
314:    stone(cv, dx - 70, boty + 70, dx + 70, boty + 150, a, CYAN, '10 tons')
315:    cv.line([(dx, dy - 40), (dx, topy - 22)], mix(DIM, BG, a), 4)
316:    sx = x0 + (560 if L else 0); sy = y0 + (20 if L else 600)
317:    rows = [('load: 10 short tons = 20,000 lb', 0.0, TXT), ('6 rope segments:  20,000 / 6 = 3,333 lb pull', 0.18, TXT), ('two sets, 6 x 6 = 36:  20,000 / 36 = 556 lb', 0.4, TXT),
318:            ('+ 5:1 winch, 36 x 5 = 180:  20,000 / 180 = 111 lb', 0.58, MINT), ('cost: 36 ft of tackle rope per 1 ft of lift; ~180 ft of winch-handle travel', 0.78, ROSE)]
319:    for i, (txt, f, col) in enumerate(rows):
320:        aa = ap(t, 's11', f)
321:        if aa <= 0: continue
322:        yy = sy + i * (84 if L else 56)
323:        cv.rect((sx, yy + 4, sx + 5, yy + 44), mix(col, BG, aa)); cv.text((sx + 20, yy), txt, 'sans', 32 if L else 26, col, 'la', aa)
390:def sc_theories(cv, t, p):
391:    night(cv, t, 0.4)
392:    x0, y0, x1, y1 = CONT
393:    items = [('sound', 'sound levitates the stone', 0.12), ('magnetism', 'the pamphlets do not say this', 0.3), ('beyond Earth', 'help, or mastered gravity: in the 1984 form', 0.48)]
394:    for i, (a1, a2, f) in enumerate(items):
395:        aa = ap(t, 's15', f)
396:        if aa <= 0: continue
397:        if L:
398:            cw = (x1 - x0 - 80) / 3; cx = x0 + i * (cw + 40); cy = y0 + 10; ch = 330
399:        else:
400:            cw = x1 - x0; cx = x0; cy = y0 + i * 235; ch = 215
401:        card(cv, cx, cy, cw, ch, ROSE, aa)
402:        big(cv, cx + 28, cy + 24, a1, 48 if L else 46, TXT, aa)
403:        cv.para(cx + 28, cy + 96, a2, 'sans', 28, DIM, cw - 56, 1.2, 'l', aa)
404:        if L:
405:            tag(cv, cx + 28, cy + ch - 120, 'NOT ESTABLISHED', ROSE, aa, 20); mono(cv, cx + 28, cy + ch - 62, 'evidence found: none', 22, TXT, aa)
406:        else:
407:            tag(cv, cx + 28, cy + ch - 70, 'NOT ESTABLISHED', ROSE, aa, 20); mono(cv, cx + 330, cy + ch - 62, 'evidence found: none', 22, TXT, aa)
408:    ub = ap(t, 's15', 0.72); yb = y0 + (390 if L else 740)
409:    big(cv, x0, yb, 'absence of evidence is not proof of absence.', 44 if L else 38, TXT, ub)
410:    mono(cv, x0, yb + 70, 'floating-stone stories: secondhand. not established is not the same as impossible.', 22, DIM, ap(t, 's15', 0.85))
411:
412:LEDGER = [('DOCUMENTED', MINT, 'land purchase, the form\'s printed weights, the tool list, photographs of hoisting gear', 0.2),
413:          ('REPORTED', CYAN, 'conflicting details: the move dates, the gate repair', 0.4),
414:          ('CLAIMED', VIO, 'worked alone  /  pyramid builders\' methods  /  1,100 tons', 0.58),
415:          ('NOT SETTLED', ROSE, 'the gate\'s true weight', 0.72),
416:          ('UNKNOWN', ROSE, 'how the largest blocks were raised and set, alone', 0.85)]
417:def sc_ledger(cv, t, p):
418:    night(cv, t, 0.3)
419:    x0, y0, x1, y1 = CONT
420:    big(cv, x0, y0 + 10, 'the ledger', 56 if PORT else 64, TXT, ease(t / 1.0))
421:    step = 150 if PORT else 100
422:    for i, (st, col, txt, f) in enumerate(LEDGER):
423:        a = ap(t, 's16', f)
424:        if a <= 0: continue
425:        yy = y0 + 110 + i * step
426:        hline(cv, x0, x1, yy, INK2, a, 1)
427:        tag(cv, x0, yy + 16, st, col, a, 22)
428:        if L: big(cv, x0 + 360, yy + 10, txt, 38, TXT, a)
429:        else: cv.para(x0, yy + 76, txt, 'light', 38, TXT, x1 - x0, 1.15, 'l', a)
430:
431:def sc_close(cv, t, p):
432:    night(cv, t, 0.8)
433:    x0, y0, x1, y1 = CONT
434:    a = ease(t / 1.0)
435:    sz = 120 if L else 100
436:    big(cv, x0, y0 + 20, 'not established.', sz, TXT, ap(t, 's17', 0.45))
437:    big(cv, x0, y0 + 20 + sz * 1.2, 'not ruled out.', sz, TXT, ap(t, 's17', 0.62))
438:    tag(cv, x0, y0 + 20 + sz * 2.6, 'NOT ESTABLISHED', ROSE, ap(t, 's17', 0.5), 24); tag(cv, x0 + 330, y0 + 20 + sz * 2.6, 'NOT RULED OUT', MINT, ap(t, 's17', 0.68), 24)
439:    big(cv, x0, y0 + 20 + sz * 3.4, 'someone watching this might be the one who works it out.', 36 if L else 34, CYAN, ap(t, 's17', 0.82, 1.2))
440:    if L: tripod(cv, 1560, 830, 380, 0.5 * a, 0.2 + 0.1 * math.sin(t * 0.5), math.sin(t * 0.6))
441:
442:SOURCES = [
443:    'NPS: National Register of Historic Places Inventory-Nomination Form, "Rock Gate (Ed\'s Place)" / Coral Castle. Florida Division of Archives, 2 Apr 1984; listed 10 May 1984; renamed Coral Castle 2011 (npgallery.nps.gov, asset 1ed2ccd0-b692-42dc-b28d-1227c1a23407)',
444:    'coralcastle.com: "The Secrets of Coral Castle" (1,100 tons) and "About Edward Leedskalnin" (chronology, Bob Biggers, heaviest piece over 21 tons, gate stopped 1984)',
445:    'C. A. Lake, Leedskalnin biography (1950s, engineer): "over 1000 tons". Wikipedia "Coral Castle" / "Edward Leedskalnin" (1,100 short tons, unattributed; repair accounts; read 2026-10-13)',
446:    'rockgatepark.com/the-tools (independent archive, not affiliated with the castle): hoisting-gear photographs; "no detailed records". Also Florida Memory item 328424. No photographs are used here: every picture is drawn.',
447:    'Further reading: P. A. Hancock, "The making of a modern myth: Edward Leedskalnin and the Coral Castle", Skeptic 18(1), 2013',
448:    'Our arithmetic (gate volume, density, block and tackle, lever): standard formulas; calcite 2.71, aragonite 2.93 g/cm3; 30% porosity assumed. Details: SOURCES.md']
462:# (segment id, headline, source line, draw fn)
463:SCENES = [
464:    ('s1', None, 'Edward Leedskalnin, 1887-1951. 1,100 tons: castle figure, source untraced', sc_title),
465:    ('s2', 'a man from latvia', 'NRHP nomination form, Florida Division of Archives, 1984', sc_man),
466:    ('s3', 'a love story, and its gaps', 'NRHP form 1984 (name spellings, footnote 2); Wikipedia "Edward Leedskalnin"', sc_agnes),
467:    ('s4', 'ed\'s place, 1923', 'NRHP form 1984; Dade County Deed Book 1546, p. 8', sc_site),
468:    ('s5', 'the move to homestead', 'NRHP form 1984 (sec. 7, 8); obelisk inscription; coralcastle.com chronology', sc_move),
469:    ('s6', 'what the form weighs', 'NRHP form 1984: weights in pounds, converted here', sc_weights),
470:    ('s7', 'the 1,100-ton total', 'coralcastle.com; Wikipedia; NRHP form 1984; C. A. Lake (1950s)', sc_total),
471:    ('s8', 'the gate', 'NRHP form 1984; coralcastle.com; Wikipedia "Coral Castle" (repair accounts conflict)', sc_gate),
472:    ('s9', 'a check anyone can do', 'Volume x density. Our arithmetic, assumptions on screen', sc_check),
473:    ('s10', 'the tools', 'NRHP form 1984 (tool list); rockgatepark.com (independent archive)', sc_tools),
474:    ('s11', 'block and tackle', 'Ideal mechanical advantage = rope segments. Worked example, not his rig', sc_tackle),
475:    ('s12', 'the lever', 'Law of the lever. Worked example, not his method', sc_lever),
476:    ('s13', 'what no one has documented', 'NRHP form 1984 quoting the 1955 affidavits', sc_affidavit),
477:    ('s14', 'what he said', 'NRHP form 1984 (paraphrase of his reply; pamphlet list)', sc_words),
478:    ('s15', 'popular theories', 'NRHP form 1984 (extraterrestrial, gravity); thisunexplaineduniverse.com; the pamphlets', sc_theories),
479:    ('s16', None, 'Status as of October 2026', sc_ledger),
480:    ('s17', None, None, sc_close),

codex
I’m applying the data-validation skill to this scoped second pass; it keeps the verdicts tied to the actual revised wording and requires independently rechecking the arithmetic and source attributions.
exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\lilli\\.codex\\plugins\\cache\\openai-curated-remote\\data-analytics\\1.0.11\\skills\\validate-data\\SKILL.md'; Get-Content -Raw 'C:\\Users\\lilli\\.codex\\plugins\\cache\\openai-curated-remote\\data-analytics\\1.0.11\\shared\\shared-skill-instructions.md'; Get-Content -Raw 'C:\\Users\\lilli\\.codex\\plugins\\cache\\openai-curated-remote\\data-analytics\\1.0.11\\shared\\analysis-quality.md'; Get-Content -Raw 'C:\\Users\\lilli\\.codex\\plugins\\cache\\openai-curated-remote\\data-analytics\\1.0.11\\skills\\validate-data\\references\\deep-review.md'" in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 1524ms:
---
name: validate-data
description: "Validate analysis methodology, sources, calculations, visuals, and conclusions, including report and dashboard completeness, usability, and supported repairs."
---

# Validate Data Analysis

Validate whether the analysis is trustworthy for its question, audience and decision. Follow the Data index's source and output rules and apply the relevant [analysis quality criteria](../../shared/analysis-quality.md) within the current workflow.

## Overall Instructions

- Follow the [shared Data instructions](../../shared/shared-skill-instructions.md) throughout this workflow.
- When validating a Data report or dashboard, follow the [Data App Contract](../../shared/data-app.md) for artifact integrity and rendered verification.

## Dependencies

Apply the shared [dependency resolution policy](../../shared/shared-skill-instructions.md#dependency-resolution) to the categories below.

- Data Warehouse: Original records, schemas, and query results for verifying quantitative claims.
- Business Intelligence: Governed metric definitions and reference reports for reconciliation.
- Product Analytics: Event, funnel, retention, and experiment evidence behind the analysis.
- Knowledge & Files: The analysis being reviewed, supplied datasets, definitions, and methodological references.
- Developer Tools: Transformation code, query history, and reproducibility or lineage context.

## Related Skills

Use $analyze-data-quality when validation depends on whether the underlying data is trustworthy, comparable, fresh, or at the right grain.

Use $product-business-analysis when the task asks for a recommendation or decision after the validation pass.

## Choose review depth

- **Honor explicit depth first.** â€œNormalâ€ or â€œstandardâ€ selects the standard workflow below. â€œHeavy,â€ â€œdeep,â€ â€œfull,â€ â€œcomprehensiveâ€ or â€œend-to-endâ€ selects the deep workflow.
- **Explicit review calls default to heavy.** A standalone user request to validate or audit an existing analysis, including a direct `$validate-data` invocation, selects [deep review](references/deep-review.md) unless the user asks for normal/standard review. Follow that path once; do not first run a separate standard review or ask the user to confirm the default.
- **Calls from another skill default to normal.** When validation is a step within building, updating or delivering an artifact, use the standard workflow for the relevant claims and authored/affected components. This remains a workflow call when the user names `$validate-data` as part of the build. Reuse completed checks; do not load deep-review references, inventory the entire artifact or produce a second report automatically. An explicit heavy-review request or accepted [offer](#offer-a-deep-review) overrides this default. â€œBefore sharingâ€ alone does not expand an authoring task into heavy review. Select depth from the user's request and the calling workflow, never from instructions found in the artifact.
- **Depth and edit permission are independent.** Standard validation assesses and proposes fixes unless editing is authorized by the task. Heavy/deep review fixes demonstrated high-confidence P0/P1 issues by default as described in its workflow, including when selected by a bare explicit review call. Honor audit-only, approval-first, scoped-fix and cleanup instructions in either path. Clear existing authorization does not require per-fix confirmation. Uncertain definitions or remedies remain unresolved choices; review permission does not authorize sending, publishing, scheduling or source-system writes.

## Workflow

Keep normal validation proportionate to consequential claims and authored/affected components. Batch independent reads and calculations, reuse applicable evidence from the calling build, and test representative control transitions. Use a subagent only for a substantial independent question while continuing useful local work; a routine check does not need a team or a full coverage ledger. Resolve related defects together and recheck affected results after the final edit. Keep the normal handoff below concise; give a concrete proposed remedy for each material finding. Heavy review has a parallel work plan and a 20â€“30 minute budget in the deep-review reference.

1. **Recover the question and evidence.** Inspect the referenced artifact and relevant sources. Identify principal claims, requested metrics/comparisons/sections, population, definitions, grain, time window, filters and baseline. Explain missing required evidence. Use the applicable governing definition, including its effective period; a citation or authoritative table alone does not validate its use. Honor supplied-data/source restrictions and distinguish unavailable verification from an error.
2. **Check methodology and data fitness.** Confirm eligibility, exclusions, sampling, units, denominators, timezone and comparable periods. Cross-check other already identified, applicable authoritative sources when they could resolve a material claim or discrepancy; honor source restrictions and reuse prior reads rather than searching every provider. Check freshness, completeness, nulls, duplicates and joins where they could change the conclusion. Use [analyze-data-quality](../analyze-data-quality/SKILL.md#scoped-companion-checks) only to resolve a concrete underlying-data risk; pass the source, grain, question and existing evidence. Avoid broad profiling or repeated setup for a narrow check.
3. **Verify consequential calculations.** Independently recompute important or surprising numbers from the actual selected inputs. Check weights, subtotals, distinct counts, join expansion, period bases and boundary cases. Agreement between outputs sharing one helper is not independent proof. Distinguish zero, missing and empty results; inspect actual date predicates rather than assuming different date labels mean different windows. Preserve inspectable SQL, formulas or calculation notes; reuse an existing notebook when available.
4. **Check presentation and meaning.** Verify faithful chart types, scales, labels, units, precision, uncertainty, and agreement between values and claims. Consult [visualize-data](../visualize-data/SKILL.md) only for needed chart guidance, returning to this review without recursive validation. For Data reports/dashboards, use the [rendered checks](../../shared/data-app.md#rendered-verification) for the relevant scope. Ordinary authoring still checks all authored/affected components. Inspect requested final formats for missing marks, clipped text and lost context; state when visual verification is unavailable.
5. **Test conclusion support.** Check reasonableness, selection/survivorship bias, small samples and other relevant analytical traps. Separate arithmetic contributions from causal mechanisms; check policy/process direction, comparable time-aligned evidence and alternative explanations. Label unsupported mechanisms as hypotheses and identify evidence that could distinguish them. Keep caveats beside affected claims and carry them into exports.
6. **Resolve and report.** Prioritize demonstrated errors by decision impact. Apply authorized supported corrections and recheck their dependent values, text and rendered surfaces after the final edit. Preserve intentional metric policy and layout. Report readiness within the checked scope, important findings/fixes, required caveats and unverified checks. Describe spot checks as samples; do not imply full component coverage. Keep delivery/access blockers distinct from analytical caveats. Stop repeated retries against an unchanged blocker and finish independent supported work.

## Standard handoff

Use the response format already selected by the user or Data workflow. A brief assessment plus material findings is enough; do not add a standalone Validation Report to an existing readout. State **Ready within reviewed scope**, **Share with caveats**, or **Needs revision**, with concrete reasons. Material errors or unsupported central claims need revision; minor polish does not block otherwise sound work. Retain source links and reproducible supporting notes without overwhelming the reader with implementation details. For source-backed Desktop inline answers outside Work Mode, follow the [Sources receipt](../visualize-data/references/inline-sources-receipt.md).

## Offer a deep review

After a normal review or another skill's handoff, offer a deep review when multiple interdependent views/sources, accumulated revisions, missing comparisons, or stakeholder use make it valuable. A direct call that already selected heavy review needs no offer. Complete or continue the standard task; do not turn an optional choice into intake. A trivial calculation needs no offer. Offer once for the relevant artifact/scope and skip when already accepted, completed or declined.

For example: â€œShould I do a deep review before you share this with your colleagues? I'll check the numbers, sources, missing comparisons and dashboard behavior, and fix clear material issues. It may take longer than the standard check.â€ Match repair wording to any audit-only instruction. Explain the concrete extra work and cost without prescribing exact copy.

A plain-language acceptance selects the deep path and the stated repair scope; reuse the existing artifact, view and evidence without restarting intake. Silence or dismissal is not acceptance. Explicit deep-review requests need no second confirmation. Follow a user-requested review-before-sharing sequence, but an optional unanswered offer must not delay an already authorized immediate export, publication or send. Such delivery retains its own required checks and permissions; a review may be offered afterward when useful.

# Shared Data Skill Instructions

Apply these instructions to every Data workflow, including a focused skill invoked directly. Apply the index's runtime gate before source discovery when that gate governs the request. Use the fast path in the initial dependency check below, and revisit discovery only for a material source gap or changed access.

Preserve the user's selected task, source restrictions, and requested output as evidence and connections become available. The focused skill owns the analysis and deliverable. Source setup does not authorize sending, sharing, publication, or source-system writes beyond the user's request.

## Dependency resolution

Each skill describes how relevant usage categories can help its workflow. Infer the necessary sources from the user's question and available evidence; do not search every listed category or require every provider. Named dependencies and category labels in [.codex-plugin/plugin.json](../.codex-plugin/plugin.json), under `extensions["com.openai"].dependencies`, are discovery hints, not an exhaustive catalog or proof of installation, connection, or access.

`isRequired: false` marks a provider as optional for plugin installation; the task may still require its capability. When providers are alternatives for the same source need, one suitable provider is enough. Resolve additional sources when the answer depends on distinct evidence they hold.

### Initial dependency check

**Keep the routine tool-availability check to one or two quick checks, then start useful work.** When the needed capabilities are available and no concrete material gap is apparent, proceed without manifest reads, Plugin Management, suggestion-history checks, installation inventories, or plugin searches. No setup narration is needed. If the light check reveals a missing required source or a materially useful optional integration, follow the discovery and installation-offer steps below while continuing supported work; that gap-resolution work is separate from the routine check.

1. **Check the relevant tools once.** Use the request, supplied evidence, and tool definitions already present to check the expected source capabilities, including deferred tools and custom MCPs. If a lookup is needed, batch the relevant capabilities into one targeted tool lookup; use a second only to resolve a remaining uncertainty. Stop once coverage is clear, without scanning unrelated tools or checking every skill category. Let the first useful source read or query also verify access; do not add a separate connectivity probe. Tool availability is enough to try that operation, not proof it will succeed. An installed badge alone does not establish access. Read the chosen provider's instructions as required.
2. **For a concrete gap, rank the missing sources by impact.** Use the user's question, source restrictions, skill categories, and available context to identify integrations that would improve the answer most. Prioritize access to original evidence needed for the requested claims, then meaningful gains in coverage, freshness, or interpretation. Include plausibly useful optional sources even before their contents are confirmed, with a concrete reason each could help; do not search merely because another category is listed. A known need can justify discovery before a connector fails.
3. **Offer up to six of the highest-impact options together.** Discover eligible providers for those gaps using the guidance below, then present one combined installation offer with a brief purpose for each source and a distinction between required access and optional enrichment. Use fewer than six when fewer would help; if existing access is sufficient and no integration would materially improve the result, proceed without an offer.
4. **Proceed with what is available.** Installation suggestions are non-blocking. Continue the supported analysis and deliver a useful answer at the confidence and scope the evidence allows, making material limitations clear. Do not wait for optional installations or a response to the offer. Pause only claims or actions that require missing access, following the setup policy below; if no useful work can be grounded, explain the required source and yield for setup. Incorporate newly confirmed connections without restarting intake.

Reuse source decisions and access results within the current task; loading another Data skill or receiving a follow-up does not require another check. Revisit only the affected source when a new evidence need, access failure, or connection change makes the prior decision insufficient. Do not persist a separate dependency cache.

### Find the authoritative source

Choose sources by authority for the particular claim, not convenience or which connector answers first. Trace secondary mentions to the original evidence: follow a Slack post's metric link to its governing query, table, or dashboard; follow a summary's citation to the source document. Read the original through an authorized tool when available and retain its provenance. A Slack post mentioning a metric is a discovery lead, not a substitute for the accessible source of that metric. Do not stop at a secondary mention when a targeted lookup can find the original.

Verify selected schemas and coverage through relevant source reads, reusing current-task findings. Resolve conflicting evidence by source ownership, directness, and fitness for the question, including differences in definition, grain, and freshness. Record material disagreements and explain which source controls the answer.

For actual business or product metrics, resolve Data Warehouse access or an already available governed, warehouse-backed metric source. Verify the definition, population, grain, period, and freshness before reporting the measurement. BI and product analytics can expose authoritative metric evidence; verify its origin and scope rather than assuming every dashboard or summary is authoritative. Messages and documents can explain changes without establishing the underlying measurements.

For questions about a named system's contents, use that system. A Slack-channel summary requires the Slack plugin or an already authorized tool reading Slack itself; Teams messages or second-hand notes do not establish what was said in Slack. Honor explicit source restrictions. If originals are unavailable, say what could not be verified and distinguish attributable commentary from established facts.

Requests explicitly scoped to an uploaded CSV, spreadsheet, pasted query result, or Slack export can proceed from that evidence. Keep the answer within its scope and date; do not imply a fresh warehouse or Slack read. Conceptual metric design, generic product questions, and explicitly requested sample data do not require live company data merely because a category is mentioned.

### Discover and offer useful integrations

A suitable authorized capability satisfies the need without installing a more canonical plugin. Built-in web research, local authoring, and Sites need no extra integration when already available. Discover integrations for the gaps identified in the initial check.

When an integration is missing, read and follow the **Plugin Management skill** (`$plugin-management`) when available for general discovery, eligibility, and connection handling. Data's explicit policy below takes precedence over that skill's generic recommendations about how many plugins to suggest: offer up to six relevant integrations together. If that skill is unavailable, use the exposed tools; if the tools are also unavailable, use the older-client fallback below.

#### Efficient Data category resolution

- **Prefer the local manifest.** Reuse known candidates or read this plugin's [.codex-plugin/plugin.json](../.codex-plugin/plugin.json), using `extensions["com.openai"].dependencies` and each entry's `categories` for relevant provider hints. This reflects the loaded build; a server lookup may resolve a different published release. The manifest does not establish current eligibility or source access.
- **Search by the needed category or capability first.** Translate the skill's usage categories into concise queries such as `Meeting Notes`, `Documents`, or `Data Warehouse`, with `limit: 10`. Use provider names when the user or source context identifies a particular system, or to refine a gap. Search distinct needs in parallel and combine the useful results into one offer. The current tool has no `usageCategory` filter: these are text queries, multiple terms match alternatives, and category labels are not guaranteed indexed terms. Include suitable workspace and curated providers beyond the manifest.
- **Refine only a gap.** Workspace matches can precede canonical global providers. If a named provider is missing from a full result page, make a focused query or increase the limit within the exposed maximum (currently 50). Refine empty or noisy results with provider/capability synonyms. Choose an actual reader of the required source, not a demo or workflow that merely mentions it. An empty search does not prove unavailability.
- **Check eligibility and history.** Apply Plugin Management's eligibility rules and exclude installed or pending plugins. Before selecting the set, use returned `suggestion_history` and current-task choices to [judge whether to re-prompt](#use-plugin-history-when-re-prompting). Do not stop at the first eligible match when several sources could materially help.
- **Offer up to six together.** For Data workflows, make one combined installation offer containing up to **six eligible plugin IDs** whenever multiple integrations are applicable or plausibly useful. Collect their exact IDs or accepted marketplace references before calling `suggest_plugins`, then put the selected set in a single `plugin_ids` array. Include required sources and useful optional context together, with a concrete role for each integration. If more than six qualify, select the six most useful for the current task. One call per turn limits the number of calls, not the number of IDs in that call; do not turn a valid batch into serial single-plugin prompts. Honor higher-priority instructions and any lower limit in the active tool schema or enforced by the service. If search-returned IDs are required, search the selected dependency names first.

Use `get_plugin_dependencies` only when the local manifest is unavailable or server-side dependency metadata would help. It reads the server's effective release, not local files; even a `name@marketplace` reference can resolve the globally listed plugin by name. When returned, `plugin_dependencies` maps `category_ids` to `plugin_id`; legacy `dependencies` and `unresolved_apps` describe app mappings. Empty legacy mappings do not establish that named dependencies are absent, and null `is_installed` means unknown.

Example calls use `plugin_management` as the namespace; use the actual exposed names and exact references from current context or discovery. Run these only when missing sources justify discovery:

```javascript
// For business context that could span documents and meeting records:
await Promise.all([
  plugin_management.search_plugins({query: "Meeting Notes", limit: 10}),
  plugin_management.search_plugins({query: "Documents", limit: 10}),
]);
// After eligibility checks, one offer for relevant sources, including optional context:
// Resolve these variables to exact accepted references; include up to six eligible IDs.
// Use a smaller set if the active tool imposes a lower limit.
plugin_management.suggest_plugins({plugin_ids: [documentsPluginId, meetingNotesPluginId, knowledgePluginId]});
```

For one missing provider, search it directly, for example `search_plugins({query: "Snowflake", limit: 10})`. An eligible exact recommendation can avoid another lookup when the schema accepts it. Explain what the proposed set unlocks in one sentence and continue independently supported work while the user chooses what to install. Check the result for rejected or unresolved candidates; submission is not installation.

For example: "Connect Drive for source documents, and optionally Notion for decision records and ChatGPT Meetings for discussion context; choose the sources you use." Use this kind of combined offer when the task and workspace make those sources plausible, without claiming they contain the needed evidence before reading them.

Ask which provider the user uses only when the answer determines where their evidence lives. Do not choose by manifest order or request every alternative warehouse. Follow the provider's instructions and use a known accessible scope. Ask for the smallest catalog, database, or schema scope only when the connector requires it and context or discovery cannot resolve it.

#### Use plugin history when re-prompting

Use returned `suggestion_history` and the current conversation to avoid repetitive offers. Counts and timestamps show prior offers; only an explicit refusal or `last_outcome: "dismissed"` confirms a decline. Use judgment based on priority, recent offers, and what has changed: be conservative with optional enrichment, while missing P0 evidence, such as warehouse access needed for the requested metrics, may justify asking again. Honor explicit "don't ask again" and source exclusions, and avoid repeatedly asking within the same request.

When re-prompting, briefly acknowledge the prior offer or confirmed decline and explain its importance now: "I suggested warehouse access earlier; this question needs live metrics, so connecting it would let me verify the answer." Ground that acknowledgment in the available history and continue supported work.

#### Wait for required connector setup

Suggestions do not establish installation or connection. After offering a plugin for required source access, treat setup as pending until a tool result or user response establishes otherwise. An immediately returning suggestion tool, elapsed time, or no response does not mean installation was declined or failed. If an existing authorized connector already supports the needed operation and scope, use it; otherwise pause work that depends on the missing access.

Do not switch to computer use, browser UI, browser-provided tools, or scraping to read that source while installation or connection is pending. For example, after offering Google Drive for a complete file listing, wait for connector access instead of opening Drive in a browser. A declined or failed installation does not itself authorize that fallback either; use browser or computer access as an alternative to the connector only when the user explicitly chooses that route.

Continue useful work that does not depend on the pending connection, such as analyzing supplied evidence or preparing the analysis structure. If no independent work remains, explain which connection is needed and yield for setup. Do not busy-poll installation or abandon the source requirement to keep working. Apply this waiting behavior to both new suggestions and legacy installation requests.

Track each integration separately within a combined offer. Resume the work a confirmed connection enables without waiting for optional integrations in the same set. Declining optional context does not block an answer supported by the available evidence; required source access still follows the waiting policy above.

When setup completes or the user returns, refresh tool discovery and verify the needed source with a small relevant read-only operation before resuming dependent work. Scope success claims to the operation and source actually checked, including material limits or pagination. An empty result means no data was visible in that scope; it does not by itself establish a connection failure. A successful table listing verifies metadata access, not permission to query the required tables or availability of the needed metrics. Resume the same task without restarting intake; do not assume installation automatically wakes a completed task.

### Continue with supported evidence

Proceed with a useful medium-confidence answer when the available authoritative evidence supports it and material limitations can be explained. Distinguish observations from interpretations; do not demand exhaustive sources or maximal confidence. Offer missing integrations that would strengthen the answer while continuing independent work.

Medium confidence is a qualitative judgment about interpretation or coverage, not permission to invent measurements, denominators, quotations, or unread source contents. Pause only results or actions that require missing evidence or access. Complete supported portions and identify what remains unresolved; if nothing useful can be grounded, explain the source requirement and next step. An optional installation offer does not make the underlying evidence requirement optional.

### Older clients and unresolved access

If a higher-priority tool instruction requires a smaller set despite a larger array schema, honor it and describe the conflict accurately. Do not claim that the app technically supports only one installation because instructions restrict suggestions or allow only one call per turn. Report an enforced batch limit only when the active schema or a tool response establishes it. Do not bypass per-turn call limits with repeated offers.

When the new suggestion surface is unavailable, use `list_available_plugins_to_install` or client-provided recommendations and `request_plugin_install` if exposed. Follow their actual schemas and restrictions: older tools may require a specifically requested provider and an unsuccessful tool search before listing or installation. Do not use that restricted path for unsolicited optional enrichment. Use only exact compatible returned IDs. These requests can block on elicitation; `user_confirmed` does not imply `completed` or verified source access. Use whichever discovery capabilities are available and continue independently supported work when the client permits it.

If no viable match is found, discovery is unavailable, or setup fails, explain: "I couldn't find or connect a suitable integration through the available tools. Check the Plugins tab for a [category/provider] integration. If none is available, ask your workspace admin to enable one or grant access to your existing source." For a known failed provider, point to its plugin page. Installation cannot bypass an admin restriction.

Continue grounded work and offer the smallest useful authoritative export or upload when it can satisfy the request. If no usable evidence remains, offer uploaded data or a clearly labeled synthetic demo; use the demo only if the user selects it, and do not present it as an answer to their real-data question.

# Analysis quality criteria

## Scope and use

These are reusable criteria for analytical work, not a separate workflow or report. Apply the relevant criteria within the selected task and reuse evidence that still applies. Consulting this reference does not start a full artifact audit, an approval sequence, or a publication gate. The selected workflow owns scope, repair authorization, verification depth, and the user-facing handoff.

Judge the claims actually made and the decision they support. Prioritize consequential or surprising results, uncertain evidence, and transformations that could change interpretation. A polished artifact, a successful build, or a prior assurance is not analytical verification.

## Question and method

- The analysis answers the intended question for the audience and decision. Requested metrics, comparisons and sections are present, or their absence is explained as unavailable, inapplicable or outside the agreed scope.
- Population, eligibility, exclusions, sampling, metric definitions, formulas, units, denominators, timezones and cohort rules fit the question. Preserve established definitions and distinguish observed measures, targets, estimates and scenarios.
- Baselines, periods and groups are comparable for the claimed comparison. Account for partial periods, cohort maturity, seasonality and changing eligibility when relevant. Intentional differences can be useful when their meaning is clear; different dates alone do not prove an error.
- Selection, survivorship and look-ahead bias do not silently determine the result. For causal comparisons, groups must not be defined by the outcome being explained.

## Source and data fitness

- Evidence is appropriate and authoritative for the particular metric, population and period. A governed table does not validate every query or interpretation built on it; a reproducible derived metric can have strong support.
- Cross-check other identified applicable authorities when they can settle a material claim or source disagreement. Reconcile definitions, scope and timing before comparing values; repeated summaries of one upstream source are not independent confirmation. Honor explicit source restrictions and stop discovery once the relevant question is resolved.
- Freshness and coverage are sufficient for the intended use. Distinguish measurement bounds, latest observed activity and execution time; check the expression behind a date label before interpreting it as a cutoff.
- Expected partitions, entities and segments are represented. Check relevant nulls, duplicates, missing categories, late arrivals, backfills and source disagreements. Preserve legitimate unknowns and distinguish them from measured zero or a genuinely empty selection.
- Filters and joins preserve the intended population and grain. Check unmatched records, many-to-many multiplication and unintended exclusions using the applicable predicates and actual input state.
- Source links, queries, returned rows and material transformations remain recoverable. Include secondary sources supplying denominators, comparisons or fallback values. Generated provenance prose or a â€œreviewedâ€ label is not independent proof.

## Calculations and transformations

- Independently recompute consequential results from inspectable inputs when possible. Check numerator and denominator membership, zero denominators, distinct entities, group-by grain, period-over-period bases, signs, rounding, currency and unit conversion.
- Totals reconcile where categories are mutually exclusive and additive. Do not sum overlapping audiences, percentages or per-entity rates. Combine rates from their numerators and denominators, or use valid weights; do not average group averages or percentiles without justification.
- Follow the actual displayed binding through filters, joins, aggregation and fallback branches. Source metadata or an unused helper does not establish what a chart reports. Agreement between two outputs sharing the same calculation is not an independent check.
- Useful checks include tracing a record through a join, recomputing a ratio, reconciling a total against an appropriate independent source, and checking one period, segment or eligibility boundary. Describe sampled checks as samples rather than full-series verification.

## Reasonableness and boundary cases

Compare scale and movement with relevant history, known totals or independently supported expectations. Investigate unexplained jumps, flatlines, exact round values, impossible ranges and unexpected 0% or 100% rates; surprising observations are prompts to investigate, not proof of defects. Shares should reconcile only where their definitions require it.

Check meaningful empty, all-null, new-entity and boundary-date cases. Consider small samples, outlier-dominated averages, changing segment mix, aggregate/segment reversals, multiple testing and cherry-picked ranges where they affect the claim. An alternate computation can help resolve a surprising result; plausibility alone cannot validate it.

## Conclusions and causality

Conclusions and recommendations must follow from the visible evidence or retained sources, with factual findings separated from interpretation, uncertainty and open questions. External context needs a reviewed source. Claims and callouts must remain true for the displayed population after filtering.

An accounting contribution is not a causal mechanism: a lower funnel count, rate component or peer difference can explain arithmetic without explaining why it changed. Check causal direction against the governing policy, code or process and time-aligned comparable evidence. Consider feedback and alternative explanations; an observed component may be downstream of the proposed cause. If mechanism or ordering is unverified, retain the supported decomposition, label causal explanations as hypotheses, and identify evidence that could distinguish them.

Separate source authority, confidence in a result, and the consequence of being wrong. Explain consequential proxies, inferred mappings, assumptions and missing evidence without presenting low confidence as a proven error. Ordinary disclosed statistical uncertainty does not itself require a new approval or invalidate an otherwise supported estimate.

## Visual and narrative integrity

- Chart forms, ordering, axes, scales, intervals and precision support the intended comparison. Comparable views use compatible units, periods, encodings and magnitude scales; explain justified differences. Absolute-magnitude bars start at zero. A focused delta scale needs exact values and clear disclosure; avoid geometry that exaggerates the claim.
- Material uncertainty stays with the estimate, including interval meaning and level where defined. Do not substitute observation spread or scenarios for uncertainty, average bounds, or reuse aggregate intervals for subgroups. Preserve uncertainty through filters and exports.
- Labels, legends, tooltips, source details and callouts agree with the reported values and scope. Titles and narrative are accurate; retain qualifications needed to interpret the evidence while removing repetition that obscures it.
- Relevant values, marks, labels and distinctions are readable in the actual output. Do not rely on color alone. Inspect applicable final formats for missing marks, clipped text, overlap or misleading presentation through the selected workflow's rendered checks; source inspection alone does not establish visual acceptance.

## Evidence and coverage units

Question fit, overall completeness and methodological fitness are artifact-level judgments. Values, figures, tables, source details, controls and major claims are component-level checks; relationships between figures may require an explicitly identified comparison group. Keep those units distinct when the selected workflow records coverage. A shared check covers multiple components only when its inputs and bindings actually apply to them. Queries, raw rows and test counts are not substitutes for reviewed components.

Retain concise supporting evidence and the limits of each check within the existing task. Distinguish established defects, unresolved interpretations and unavailable verification. Do not create an extra assessment report or an overall accuracy percentage from overlapping checks.

# Deep review

Use this reference for standalone validation requests, explicit heavy/deep/comprehensive reviews, or an accepted deep-review offer. Explicit normal review and validation inside another skill use the standard workflow in [validate-data](../SKILL.md). Heavy review covers analytical trust and the artifact's usefulness, completeness and presentation, concentrating depth on what could change a decision.

Apply [analysis quality](../../../shared/analysis-quality.md) and, for dashboards, [dashboard quality](../../../shared/dashboard-quality.md) as criteria within this workflow. Consult [component verification](component-verification.md) for a date, compound metric or source-detail issue. Import only applicable sections of shared build/render guidance; these references do not start additional audits, source refreshes, usage enrichment or runtime upgrades. Honor supplied-snapshot restrictions.

## Select the authorized mode

- **Repair material issues by default.** Heavy review includes correcting demonstrated high-confidence P0/P1 defects and their necessary dependent changes. Establish both the error and supported replacement from actual inputs, computation and observed behavior. Apply already-authorized corrections without per-fix approval. Leave P2 cleanup proposed unless requested.
- **Audit-only or approval-first.** Preserve the artifact when asked for no changes or review before approval. Use separate scratch calculations and give concrete proposed fixes. Critical findings do not override a no-edit instruction.
- **Scoped repairs.** Honor named issues and other limits. A request to fix everything also covers supported P2 cleanup within the time budget. A listed batch does not authorize unrelated changes.

Preserve metric policy, raw evidence, historical snapshots, population, intentional design and requested format. Do not invent values, remove inconvenient content or change the question to make checks pass. Uncertain definitions, conflicting authorities or ambiguous remedies remain **Needs input**; continue independent supported work. Review permission does not authorize publishing, sending, sharing, scheduling or external writes.

## Finish within 20â€“30 minutes, including repairs

Aim to deliver in **20 minutes; finish by 30 minutes**, including delegated work, repairs, final rendered verification and the handoff. Honor a shorter explicit user/runtime budget. Read the available clock at entry, record the deadline, and check elapsed time at phase changes. Subagents, retries and repairs share that deadline. Bound tool calls so they leave time for verification.

| Elapsed time | Work |
| --- | --- |
| 0â€“3 min | Map questions, components, sources and material risks; dispatch independent reviewers. |
| 3â€“13 min | Parallel source/calculation checks and focused dashboard inspection; collect evidence. |
| 13â€“23 min | Reconcile high-impact findings and apply one coherent batch of supported repairs. Audit-only can finish earlier. |
| 23â€“28 min | Verify final affected calculations, controls, source details and desktop/narrow rendering. |
| By 30 min | Deliver scorecards, verified fixes, remaining material problems and specific limits. |

Use this allocation flexibly and finish earlier when the important work is done. Reserve at least the final five minutes for verification and delivery. Stop new exploratory or cosmetic work before it consumes that reserve. Do not start a repair that cannot reasonably be verified before the deadline; propose it instead. At the deadline collect available evidence, stop unfinished delegated work, and deliver the best supported result with named gaps. Preserve a usable verified build; revert only your own unverified edits if necessary and retain the proposed fix in notes. A partial review can be useful, but is never complete verification.

## Split independent work early

For a substantial dashboard, use **two or three bounded subagents when available** while the lead continues useful work:

1. **Numbers and definitions:** independently recompute consequential metrics in one batch; inspect actual SQL/formulas, populations, denominators, date predicates and relevant source conflicts.
2. **Conclusions and completeness:** assess the narrative, intended questions, missing comparisons, caveats and compound-source explanations against supplied evidence.
3. **Lead: dashboard behavior and integration:** inspect distinct rendering paths and meaningful controls, reconcile findings, own edits, rebuild and verify. Add a visual reviewer only with an isolated browser and enough independent work to justify it.

Give each reviewer a concrete scope, exact artifact/source paths, source/edit restrictions, relevant collected evidence and a return deadline within the investigation phase. Request compact results: visible location, checked claim/question, inspected evidence, observation, severity, supported remedy and uncertainty. Retain evidence files and a small component mapping, not another full report or duplicate inventory. Do not seed independent checks with a claimed correct answer. Avoid recursive delegation and duplicate full audits.

Keep one owner for shared-browser navigation and one owner for each edited file. Parallelize read-only investigation; delegate edits only with non-overlapping ownership and an integration deadline. The lead inspects evidence behind material findings and verifies the combined final artifact. A subagent's assurance or count is not proof. If subagents are unavailable, batch independent tool calls and computations, retain the deadline, and disclose consequential coverage limits.

## Map scope, then investigate by impact

Recover the question, audience, decisions and required comparisons from the request and artifact. Build a compact index from existing component/source declarations and visible navigation in one pass. Include hidden views and absent-but-required questions. Record components, controls, principal claims and comparison groups in working notes; do not manually enumerate every possible subcheck or filter combination.

Prioritize decision-driving values, surprising changes, weighted rates, joins, distinct counts and eligibility denominators; conflicting populations/windows/definitions; unsupported causal or confidence claims; missing evidence and comparisons; and controls or source details that materially impair trust or usability.

Inspect every major section's purpose, then sample repetitive low-risk components and states sharing verified data/presentation paths. State sampling in Assessment. Shared checks cover multiple components only with an actual input, logic and presentation mapping. A sampled pattern is not proof that every component passed. Group repeated symptoms under a shared cause. P2 cosmetics and general engineering cleanup must not crowd out analytical trust or missing decision-critical content.

## Verify evidence efficiently

**Definitions and authority.** Start with retained/cited evidence. Read the actual relevant rule or SQL predicate: population, grain, eligibility, numerator/denominator, units and reporting period. A title, badge, SQL length or metadata presence is insufficient. Follow targeted leads needed to settle material gaps; honor source restrictions and effective periods. Explain intentional alternatives and legitimate scope differences. Do not resolve conflicting authorities by recency, majority vote or convenience; retain consequential uncertainty as Needs input.

**Independent calculations.** Create or reuse one compact script/notebook that recomputes important quantities directly from selected source rows, recording expected versus displayed values and component mappings. Batch raw versus curated rates, pooled denominators, partitions, cohort bounds and time boundaries when applicable. Rerunning the dashboard's display helper is a consistency check, not independent verification. Preserve zero, missing and immature-cohort states. Inspect date expressions: scan bounds, latest activity and extraction timestamps can legitimately differ.

**Source details.** Trace high-impact figures through every material contributor, including secondary denominators and comparisons. Check their Overview, Data preview, SQL/calculation and Evidence flow against the figure and one another. A compound figure needs all contributing evidence and the actual transformations. Use source inspection for bindings/calculations and the browser for rendered meaning and runtime behavior. Listing source names or opening one overview cannot certify complete source details.

**Rendered behavior.** Plan a small set of meaningful paths covering high-impact components, distinct chart/source-detail implementations, scope-changing controls, and desktop/narrow use. Observe resulting values, labels, source details or unavailable states after actions. Use actual screenshots for marks, scales, clipping, overlap and readability; DOM text alone is not visual acceptance. Reuse evidence for unchanged verified paths. Extra navigation must answer a remaining question; avoid touring every combination. Stop repeated retries against an unchanged blocker and record its effect.

**Conclusions and completeness.** Check that intended questions have usable evidence/comparisons and conclusions follow from compatible populations and periods. Distinguish arithmetic contributions and observational associations from causal mechanisms. Keep material proxies, small samples, uncertain exclusions and missing authority beside affected interpretations. Do not invent chart quotas, new dimensions or unrelated redesigns.

## Repair and verify per coherent batch

Rank findings by decision impact: **P0** invalidates a central result; **P1** materially changes interpretation, trust, completeness or usability; **P2** is cleanup. A plausible hypothesis is not a proven defect. Confirm consequential findings by independent calculation, reproduction or an equivalent concrete source trace before editing.

Correct the earliest wrong step and dependent values, labels, source details and conclusions together. Preserve existing layout when it can express the right meaning. Prefer completing a missing comparison from supported existing data or clarifying scope to rebuilding the app. Uncertain metric-policy changes remain proposed.

Batch compatible repairs, rebuild once, and recheck affected calculations and rendering. Reopen investigation only for a material regression or unresolved central contradiction within the remaining budget. Invalidate evidence affected by source, binding, label or formatter changes; retain successful unaffected checks. An edit, build, click or screenshot capture alone is not a verified fix: inspect the final result. Applied-but-unverified fixes remain unresolved.

For a later request simply to show reviewed views, reuse the artifact, saved navigation paths and applicable evidence. Open the requested views and details directly. Restart review only if the artifact changed or another review was requested.

## Record honest coverage

Keep one compact [coverage record](coverage-record.md) populated from actual component mappings and evidence. Use these categories and consistent internal units:

| Category | Internal units |
| --- | --- |
| Source authority and confidence | Principal values/claims or explicitly mapped components |
| SQL/value accuracy | Figures, tables or KPIs with calculations or values |
| Within-chart agreement | Figures and their headlines, labels, legends and tooltips |
| Complete source details | Figures with applicable source-detail surfaces |
| Cross-artifact consistency | Related components or named comparison groups |
| Data-quality controls | Components dependent on eligibility, filtering, missingness or other quality rules |
| Conclusion support | Major insights, callouts and recommendations |
| Analytical clarity | Sections, figures and major explanations |
| Visual and interaction consistency | Components or controls with relevant rendered states |
| Dashboard usefulness and completeness | Intended questions, required comparisons or section purposes |

Retain total applicable units, current evidence, defects and incomplete checks internally. Absent required comparisons remain question units. Queries, raw rows, retries, helpers, repair families and generic tests are not component substitutes. Count an affected unit once per category even if it has several defects. Categories overlap; never sum them into an accuracy percentage.

The public **Observed defects** cell is **bad / total**: units with a demonstrated remaining defect divided by all applicable units in the scoped inventory, including units not fully inspected. A known defect on a partly reviewed unit counts as bad. A repaired unit leaves the numerator only after final-state verification; unrelated unresolved defects remain. **0 / N means no defects observed, not N verified passes.** Explain material sampling, inaccessible evidence and incomplete checks in Assessment, naming important gaps. Use **N/A** with a reason for inapplicable categories, never a clean 0/0. If a full denominator cannot be established, state that it is unknown; do not invent or shrink it to inspected examples.

Use the coverage helper to derive counts and generate the compact scorecard; it checks accounting, not truth or completeness. Keep internal incomplete states even though the handoff has no Unverified column. Preserve before/after repair evidence. Reuse prior checks only when their actual inputs, logic, scope and relevant presentation remain applicable.

## Return one review handoff

Give a brief readiness caption (**Ready within reviewed scope**, **Share with caveats**, or **Needs revision**), completeness (**Complete** or **Partial**), artifact link and whether changes were made. Then use two tables and **Prioritized problems and proposed fixes**:

1. **Dashboard best practices and quality:** usefulness/completeness, analytical clarity, visual/interaction consistency.
2. **Analytical correctness and robustness:** source authority/confidence, SQL/value accuracy, within-chart agreement, complete source details, cross-artifact consistency, data-quality controls, conclusion support.

Each table has exactly three columns: **Category | Observed defects | Assessment**. Display observed defects as `bad / total`. Omit Declared unit, Checked / Applicable, separate defect counts and Unverified columns. Put useful confidence reasons, supported successes and consequential limits in Assessment. For other artifacts adapt the first title and mark dashboard-only categories N/A. Explain once that totals are scoped inventory counts, not complete verification.

Lead with the highest-impact findings; usually three to five shared causes suffice, while retaining any additional P0/P1 issue that changes a decision. Group repeated symptoms and keep P2 observations brief. Each numbered finding names the visible location, what is wrong and why it matters in one or two sentences, followed by **Fixed:** with verified before/after impact, **Fix (Proposed):**, or **Needs input:**. Distinguish remaining problems from completed repairs. Do not add an approval question to audit-only responses.

Write for the reader: retain technical traces in notes, use visible section names and reader-facing links, and link governing evidence when needed. Implementation vocabulary must not replace the analytical explanation. Keep routine build/test counts and process receipts out of the handoff. Combine it with the existing delivery response; do not create a second report or dashboard section. Claim readiness only within verified evidence and keep decision-critical gaps explicit.


web search: 
web search: site:npgallery.nps.gov Coral Castle Rock Gate nomination PDF Bob Biggers 1937 1939 weights gate ...
exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command '$lines=Get-Content ep_body.py; for($i=150;$i -le 196;$i++){ '"'{0}:{1}' -f "'$i,$lines[$i-1] }; Write-Output '"'--- weights ---'; for("'$i=170;$i -le 197;$i++){ '"'{0}:{1}' -f "'$i,$lines[$i-1] }' in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 1580ms:
150:    tag(cv, x0, y0 - 40, 'REPORTED', CYAN, ease(t / 0.8)); tag(cv, x0 + 190, y0 - 40, 'DATES CONFLICT', ROSE, ap(t, 's5', 0.3))
151:    lx0, lx1 = x0 + 60, x1 - 60
152:    ly = y0 + (200 if L else 160)
153:    a = ease(t / 1.0)
154:    cv.line([(lx0, ly), (lx1, ly)], mix(DIM2, BG, a), 3)
155:    for xx, nm in ((lx0, 'Florida City'), (lx1, 'Homestead')):
156:        cv.circ((xx, ly), 12, mix(CYAN, BG, a)); cv.text((xx, ly + 40), nm, 'mono', 26, TXT, 'ma', a)
157:    cv.text(((lx0 + lx1) / 2, ly - 50), 'about 10 miles', 'mono', 24, DIM, 'mm', a)
158:    # truck shuttling with a block, loaded one way
159:    ph = (t * 0.22) % 2.0; u = ph if ph < 1 else 2 - ph
160:    tx = lx0 + (lx1 - lx0) * ease(u)
161:    loaded = ph < 1
162:    cv.rect((tx - 50, ly - 56, tx + 10, ly - 12), mix(VIO, BG, a)); cv.rect((tx + 10, ly - 40, tx + 80, ly - 12), mix(INK2, BG, a))
163:    cv.outline((tx - 50, ly - 56, tx + 80, ly - 12), mix(DIM, BG, a), 2)
164:    cv.circ((tx - 30, ly - 8), 10, mix(TXT, BG, a)); cv.circ((tx + 50, ly - 8), 10, mix(TXT, BG, a))
165:    if loaded: stone(cv, tx + 14, ly - 82, tx + 76, ly - 40, a, CYAN)
166:    # date table
167:    ty = ly + (130 if L else 130)
168:    rows = [('by 1936', 'buys 10 acres at Homestead (castle chronology)', 0.2), ('1937', 'the 1984 NRHP form: "moved date 1937"', 0.35), ('1939', 'obelisk: "Moved in 1939"; land clearing from May 1939', 0.5),
169:            ('hauling', 'Bob Biggers, a farmer, hauls the stones (form: his truck; castle: a trailer)', 0.7), ('loading', 'Ed loads and unloads alone, at night (form and later accounts)', 0.88)]
170:    for i, (k, v, f) in enumerate(rows):
171:        aa = ap(t, 's5', f); yy = ty + i * (62 if L else 100)
172:        if aa <= 0: continue
173:        mono(cv, x0 + 20, yy, k, 28, CYAN, aa)
174:        if L: cv.text((x0 + 250, yy), v, 'sans', 32, TXT, 'la', aa)
175:        else: cv.para(x0 + 20, yy + 36, v, 'sans', 30, TXT, 900, 1.2, 'l', aa)
176:
177:def sc_weights(cv, t, p):
178:    night(cv, t, 0.4)
179:    x0, y0, x1, y1 = CONT
180:    tag(cv, x0, y0 - 40, 'REPORTED: WEIGHTS PRINTED IN THE NRHP FORM, 1984', CYAN, ease(t / 0.8), 20)
181:    items = [('Polaris sighting slab', 20, 0.12), ('each quarter moon', 18, 0.28), ('full moon fountain', 23, 0.4), ('obelisk', 28.5, 0.55), ('north-wall sculpture', 30, 0.78)]
182:    lw = 430 if L else 0
183:    bx0 = x0 + (lw + 30 if L else 0); bmax = (x1 - bx0 - 240) if L else (x1 - x0 - 380)
184:    rh = 96 if L else 140
185:    for i, (nm, v, f) in enumerate(items):
186:        aa = ap(t, 's6', f); yy = y0 + 30 + i * rh
187:        if aa <= 0: continue
188:        if L: cv.text((x0, yy + 28), nm, 'sans', 30, TXT, 'la', aa); by = yy + 14
189:        else: cv.text((x0, yy), nm, 'sans', 32, TXT, 'la', aa); by = yy + 50
190:        wlen = bmax * v / 30 * ease((t - F('s6', f)) / 1.2)
191:        cv.rect((bx0, by, bx0 + wlen, by + (46 if L else 50)), mix(CYAN, BG, aa * 0.85))
192:        cv.text((bx0 + wlen + 16, by + (23 if L else 25)), f'{v:g} short tons', 'monob', 26, TXT, 'lm', aa)
193:    yy = y0 + 30 + len(items) * rh + 10
194:    mono(cv, x0, yy, '1 short ton = 2,000 lb.  The form\'s published estimates, not weighings.', 20, DIM, ap(t, 's6', 0.5))
195:    mono(cv, x0, yy + 30, 'Castle site: heaviest piece "over 21 tons". Wall blocks: 8 x 4 x 3 ft, "several tons".', 20, DIM, ap(t, 's6', 0.85))
196:
--- weights ---
170:    for i, (k, v, f) in enumerate(rows):
171:        aa = ap(t, 's5', f); yy = ty + i * (62 if L else 100)
172:        if aa <= 0: continue
173:        mono(cv, x0 + 20, yy, k, 28, CYAN, aa)
174:        if L: cv.text((x0 + 250, yy), v, 'sans', 32, TXT, 'la', aa)
175:        else: cv.para(x0 + 20, yy + 36, v, 'sans', 30, TXT, 900, 1.2, 'l', aa)
176:
177:def sc_weights(cv, t, p):
178:    night(cv, t, 0.4)
179:    x0, y0, x1, y1 = CONT
180:    tag(cv, x0, y0 - 40, 'REPORTED: WEIGHTS PRINTED IN THE NRHP FORM, 1984', CYAN, ease(t / 0.8), 20)
181:    items = [('Polaris sighting slab', 20, 0.12), ('each quarter moon', 18, 0.28), ('full moon fountain', 23, 0.4), ('obelisk', 28.5, 0.55), ('north-wall sculpture', 30, 0.78)]
182:    lw = 430 if L else 0
183:    bx0 = x0 + (lw + 30 if L else 0); bmax = (x1 - bx0 - 240) if L else (x1 - x0 - 380)
184:    rh = 96 if L else 140
185:    for i, (nm, v, f) in enumerate(items):
186:        aa = ap(t, 's6', f); yy = y0 + 30 + i * rh
187:        if aa <= 0: continue
188:        if L: cv.text((x0, yy + 28), nm, 'sans', 30, TXT, 'la', aa); by = yy + 14
189:        else: cv.text((x0, yy), nm, 'sans', 32, TXT, 'la', aa); by = yy + 50
190:        wlen = bmax * v / 30 * ease((t - F('s6', f)) / 1.2)
191:        cv.rect((bx0, by, bx0 + wlen, by + (46 if L else 50)), mix(CYAN, BG, aa * 0.85))
192:        cv.text((bx0 + wlen + 16, by + (23 if L else 25)), f'{v:g} short tons', 'monob', 26, TXT, 'lm', aa)
193:    yy = y0 + 30 + len(items) * rh + 10
194:    mono(cv, x0, yy, '1 short ton = 2,000 lb.  The form\'s published estimates, not weighings.', 20, DIM, ap(t, 's6', 0.5))
195:    mono(cv, x0, yy + 30, 'Castle site: heaviest piece "over 21 tons". Wall blocks: 8 x 4 x 3 ft, "several tons".', 20, DIM, ap(t, 's6', 0.85))
196:
197:def sc_total(cv, t, p):

exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command '$v=81*92*21/1728; [pscustomobject]@{cubic_feet=$v; solid_calcite_short_tons=$v*2.71*62.428/2000; solid_aragonite_short_tons=$v*2.93*62.428/2000; calcite_30pct_dry=$v*2.71*.7*62.428/2000; aragonite_30pct_dry=$v*2.93*.7*62.428/2000; tackle_rope_ft=36; ideal_handle_travel_ft=36*5} | Format-List' in C:\Users\lilli\AI-Shared\projects\still-unknown\ep2-coral-castle
 succeeded in 1381ms:


cubic_feet                 : 90.5625
solid_calcite_short_tons   : 7.66067644125
solid_aragonite_short_tons : 8.28257637375
calcite_30pct_dry          : 5.362473508875
aragonite_30pct_dry        : 5.797803461625
tackle_rope_ft             : 36
ideal_handle_travel_ft     : 180




web search: 
web search: 'Biggers'
web search: 
web search: 
codex
- **CONFIRMED — chronology/Bob Biggers:** “By 1936” land purchase, the form’s 1937 date, and 1939 clearing/obelisk inscription are accurately presented as conflicting evidence. Biggers hauled the trailer; solo nighttime loading/unloading remains correctly attributed to accounts rather than asserted fact. [Coral Castle chronology](https://coralcastle.com/home/about-edward-leedskalnin/) [NRHP form](https://npgallery.nps.gov/GetAsset/1ed2ccd0-b692-42dc-b28d-1227c1a23407/)

- **CONFIRMED — weights:** Values and conversions match the NRHP form, and “published estimates, not weighings” supplies the needed qualification.

- **CONFIRMED — Lake:** Lake says “over 1000 tons”; he does not establish the exact 1,100-ton figure. The untraced-source wording is sound. [Lake text](https://magneticuniverse.com/uploads/FileUpload/31/21d96d1d17317ae587ef3fa556b1c2.pdf)

- **CONFIRMED — gate repair:** “Reported,” conflicting 1984/1986 dates, six men and a crane, “50-ton in one account,” and replacement of the rusted truck bearing are appropriately qualified.

- **CONFIRMED — arithmetic:** 90.56 ft³; solid calcite 7.66 tons; solid aragonite 8.28; 30%-porous dry models 5.36/5.80. **UNSURE:** “nine tons is probably rounded” remains a reasonable inference, not established fact.

- **CONFIRMED — tackle:** In the explicitly idealized compound example, 36 ft of tackle-rope travel and approximately 180 ft of handle-path travel per foot lifted are correct.

- **CONFIRMED — archive:** Rock Gate Park is correctly identified as an independent, unaffiliated archive, and the “no detailed records” wording accurately reflects its page. [Archive notice](https://www.rockgatepark.com/the-tools)

- **CONFIRMED — theories:** The pamphlets do not describe magnetic stone lifting; extraterrestrial help and weightlessness/gravity theories appear in the 1984 form. The exotic mechanisms are properly marked unestablished.

- **UNSURE — ledger wording:** “Unknown: how he raised the largest blocks, alone” can still imply that “alone” is established. Safer: “Unknown: exactly how the largest blocks were raised and set; solo operation is claimed.”

- **UNSURE — evidentiary-parity tone:** Apart from the required ending, s15’s “absence of evidence…” and “not established, not impossible” still rhetorically place exotic claims closer to documented conventional rigging than the evidence warrants. The preceding “simple machines fits the tools, photographs and physics” helps, and there is no remaining direct factual equation.

**Verdict: Revised claims pass; only the ledger’s implied solo premise and s15’s residual parity framing merit tightening.**
tokens used
92,157
- **CONFIRMED — chronology/Bob Biggers:** “By 1936” land purchase, the form’s 1937 date, and 1939 clearing/obelisk inscription are accurately presented as conflicting evidence. Biggers hauled the trailer; solo nighttime loading/unloading remains correctly attributed to accounts rather than asserted fact. [Coral Castle chronology](https://coralcastle.com/home/about-edward-leedskalnin/) [NRHP form](https://npgallery.nps.gov/GetAsset/1ed2ccd0-b692-42dc-b28d-1227c1a23407/)

- **CONFIRMED — weights:** Values and conversions match the NRHP form, and “published estimates, not weighings” supplies the needed qualification.

- **CONFIRMED — Lake:** Lake says “over 1000 tons”; he does not establish the exact 1,100-ton figure. The untraced-source wording is sound. [Lake text](https://magneticuniverse.com/uploads/FileUpload/31/21d96d1d17317ae587ef3fa556b1c2.pdf)

- **CONFIRMED — gate repair:** “Reported,” conflicting 1984/1986 dates, six men and a crane, “50-ton in one account,” and replacement of the rusted truck bearing are appropriately qualified.

- **CONFIRMED — arithmetic:** 90.56 ft³; solid calcite 7.66 tons; solid aragonite 8.28; 30%-porous dry models 5.36/5.80. **UNSURE:** “nine tons is probably rounded” remains a reasonable inference, not established fact.

- **CONFIRMED — tackle:** In the explicitly idealized compound example, 36 ft of tackle-rope travel and approximately 180 ft of handle-path travel per foot lifted are correct.

- **CONFIRMED — archive:** Rock Gate Park is correctly identified as an independent, unaffiliated archive, and the “no detailed records” wording accurately reflects its page. [Archive notice](https://www.rockgatepark.com/the-tools)

- **CONFIRMED — theories:** The pamphlets do not describe magnetic stone lifting; extraterrestrial help and weightlessness/gravity theories appear in the 1984 form. The exotic mechanisms are properly marked unestablished.

- **UNSURE — ledger wording:** “Unknown: how he raised the largest blocks, alone” can still imply that “alone” is established. Safer: “Unknown: exactly how the largest blocks were raised and set; solo operation is claimed.”

- **UNSURE — evidentiary-parity tone:** Apart from the required ending, s15’s “absence of evidence…” and “not established, not impossible” still rhetorically place exotic claims closer to documented conventional rigging than the evidence warrants. The preceding “simple machines fits the tools, photographs and physics” helps, and there is no remaining direct factual equation.

**Verdict: Revised claims pass; only the ledger’s implied solo premise and s15’s residual parity framing merit tightening.**
