# Provider terms check for Sapling (60M model), 2026-10-16

This reports what the texts say. It is not legal advice. "Unverified" means I could not open the official page myself (several OpenAI and xAI pages blocked my fetch tool with 403), so I used mirrors or third-party trackers.

Two different questions are mixed up in "may I use it": (1) using a coding helper to WRITE code for Sapling, and (2) using a provider's OUTPUTS as TRAINING DATA for Sapling. Most clauses are about (2) or about "competing". None of the pages I read mentions "helping write code for your own model" as a use at all.

## Table

| Provider | Helps write code for / run training of own model? | Outputs as training data? | Clarity | Source |
|---|---|---|---|---|
| Anthropic, Consumer (Claude app, Pro/Max, Claude Code on a subscription) | Not addressed. Ban is on using the Services "to develop any products or services that compete" and to "develop or train any ... models". Plain reading reaches even writing code, so unclear for a small non-competing model. | No. Help article: allowed only for models that "don't compete"; general chatbots / open-ended text generation are listed as banned. | Wording is broad and has no exceptions. "Compete" is not defined in the terms; only the help article explains it. | https://www.anthropic.com/legal/consumer-terms and https://support.claude.com/en/articles/12326764-can-i-use-my-outputs-to-train-an-ai-model |
| Anthropic, Commercial / API | Not addressed. Ban is narrower: "build a competing product or service, including to train competing AI models". | Same help article: non-competing small task models OK, competitors not. | Better than consumer (needs "competing"), still undefined. Exception: "except as expressly approved by Anthropic" (per a secondary quote). | https://www.anthropic.com/legal/commercial-terms |
| OpenAI, ChatGPT / Codex (consumer Terms of Use) | Not addressed (no Codex-specific clause found). The ban is on Output: "Use Output to develop models that compete with OpenAI." Writing code is not "Output used to train". | Banned only if the model "competes with OpenAI". | Short and clear in wording, but "compete" undefined. UNVERIFIED on the live page (403); text confirmed from a Dec 2024 mirror. | https://open.windriver.com/info/uni-license-list/licenses/openai-tou-20241211.html ; live page https://openai.com/policies/terms-of-use/ |
| OpenAI, Business / API | Not addressed. Output may not be used to "develop artificial intelligence models that compete with OpenAI's products and services", with a "Permitted Exception" (not defined in my source). | Same, with the exception. | UNVERIFIED (third-party tracker only). | https://conductatlas.com/platform/openai/openai-business-terms/provision/CA-P-059973/prohibition-on-using-output-to-develop-competing-ai-models/ ; live https://openai.com/policies/business-terms/ |
| xAI (Grok, Grok Build, SuperGrok, API) | UNVERIFIED. No clause found about helping write code. | Consumer terms reportedly bar using Service or Output to build competing models (and distillation). Enterprise/API terms reportedly bar using Output to train AI models at all. Second-hand only. | Could not read either page. Treat as restrictive until read. | https://x.ai/terms-of-service ; https://x.ai/legal/terms-of-service-enterprise |
| Moonshot Kimi app / Kimi Code | Not addressed. App terms bar "develop, train, or improve algorithms, models, etc., that are in direct or indirect competition with us". | App terms: only competing models. Kimi Code Community Guidelines (a guideline, not a contract) say not to use outputs for distillation (per secondary report; the guideline page I opened did not show it). | "Direct or indirect competition" is broad. Terms page shows "Effective date: January 5, 2024". Kimi Code guideline page says subscriptions are "personal interactive use only" and gives "data annotation pipelines" as an example of non-interactive use beyond normal. | https://www.kimi.com/user/agreement/en/modelUse ; https://www.kimi.com/code/docs/en/kimi-code/community-guidelines.html |
| Kimi K3 open weights | Yes. Weights you run yourself: license allows run, fine-tune, modify, derivative works. | License does not mention training other models on outputs. | Clear. "Kimi K3 License" (custom, not MIT). Limits only for model-as-a-service over $20M/12 months and 100M users / $20M monthly revenue display rule; internal use is exempt from both. | https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE (K2 was "Modified MIT": https://huggingface.co/moonshotai/Kimi-K2-Instruct/blob/main/LICENSE) |
| DeepSeek API / Open Platform | Yes. No "compete" clause in the terms. | Yes, stated. Section 4.2 lists "training other models (such as model distillation)". | Very clear. Effective April 29, 2026. | https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html |
| DeepSeek open weights | Yes. V4 weights and code are MIT per the official model card (Hugging Face LICENSE file not opened by me). Older V3 used the DeepSeek License (use-based restrictions, derivatives inherit them). | MIT: no restriction. Old DeepSeek License: model-generated synthetic data used to train another model makes that model a "Derivative" carrying the restrictions (military use etc.). | Clear for MIT models. Check which model Jaron uses. | https://fe-static.deepseek.com/chat/transparency/deepseek-V4-model-card-EN.pdf ; https://github.com/deepseek-ai/DeepSeek-V3/blob/main/LICENSE-MODEL |
| Alibaba Qwen open weights (run locally via Ollama) | Yes. Qwen3.5 repo checked is Apache 2.0. | Apache 2.0 has no output restriction. | Clear for that repo. A third-party site claimed some bigger tiers differ (contradicts the official README). Check the LICENSE of the exact model Ollama pulled. Older Qwen models (e.g. Qwen1.5 110B) used the Qwen license, not Apache. | https://huggingface.co/Qwen/Qwen3.5-9B |
| Alibaba Qwen Chat / Model Studio API | UNVERIFIED. Could not find the service terms. | UNVERIFIED. | Unknown. | none found |
| Google Gemini API (and Google AI Studio) | Not addressed. Only: "You may not use the Services to develop models that compete with the Services (e.g., Gemini API or Google AI Studio)." | No general ban. Exceptions: you may not train on Grounding with Google Search results or Google Maps data. | Clear text, "compete" undefined. Page shows "Last updated 2026-04-28 UTC". | https://ai.google.dev/gemini-api/terms |
| Google Gemini app (consumer) | UNVERIFIED for the current consumer terms. The older Generative AI Additional Terms said "You may not use the Services to develop machine learning models or related technology" (no "compete" word), but that page says it no longer applies as of May 22, 2024. | UNVERIFIED. | Current consumer wording not read. | https://policies.google.com/terms/generative-ai |

## Notes per provider

### 1. Anthropic

Consumer Terms, Section 3 (page says "Effective October 8, 2025"; I did not find a newer version, but this fetch may be a cached copy). Lead-in: "You may not access or use, or help another person to access or use, our Services in the following ways:" Item 2: "To develop any products or services that compete with our Services, including to develop or train any artificial intelligence or machine learning algorithms or models or resell the Services." No exception is listed for this item. Outputs: "we assign to you all of our right, title, and interest—if any—in Outputs."

Commercial Terms, D.4 (effective June 17, 2025): Customer may not "access the Services to build a competing product or service, including to train competing AI models". A secondary quote adds "except as expressly approved by Anthropic". Customer "owns its Outputs."

Official guidance on "compete": yes, a help-center article. Quotes: "We prohibit customers from using our services to train or develop AI models without our written permission." "You can use Claude's Outputs to train models that don't compete with Anthropic's own models." Examples allowed: sentiment analysis, content categorization, summarization, information extraction, semantic search, anomaly detection. "Our Terms do not allow the use of Outputs to train models that are competitive with Anthropic's own." Examples banned: general-purpose chatbots, models for open-ended text generation, using Outputs as training targets, reverse engineering training methods.
What this means for Sapling: the article is about OUTPUTS as training data. A 60M model that is a general text generator would sit on the banned side if trained on Claude outputs. The article does not say whether using Claude to write the training code or run jobs is fine; that is the gap. Note the two statements in the article are slightly in tension (first quote says "without our written permission"). If it matters, ask Anthropic in writing.

### 2. OpenAI

Terms of Use "What you cannot do": "Use Output to develop models that compete with OpenAI." (Confirmed from a Dec 11, 2024 mirror only; a third-party tracker says the current Terms of Use were updated May 5, 2026 with the same bullet. I could not open openai.com.) OpenAI also says users own Output. Business Terms (tracker says dated Jan 1, 2026 / updated May 2026): "except for a Permitted Exception," no use of Output to "develop artificial intelligence models that compete with OpenAI's products and services". I found no Codex-specific term about building your own model. The clause is about Output, so code written for a model you train from scratch on licensed data does not obviously fall under it, but that is my reading, not OpenAI's statement.

### 3. xAI

I could not open the consumer or enterprise terms (403). Search snippets say the consumer terms (updated May 5, 2026 per a tracker) bar using the Service or Output to build competing models and distilling, and the enterprise terms (May 12, 2026) bar using Output to train AI models. All UNVERIFIED. Nothing found on Grok Build specifically.

### 4. Moonshot

Kimi app terms (page shows effective January 5, 2024): "you may not use our Services to develop products or services that compete with us." and a misuse item "By using Kimi to develop, train, or improve algorithms, models, etc., that are in direct or indirect competition with us". Ownership: "The ownership of the content generated based on Kimi is maintained by you". The newer 2026 version of the terms was not readable. Kimi Code: no formal training-on-outputs clause found; a guideline reportedly asks users not to distill. K3 weights: "Kimi K3 License" (Copyright 2026 Moonshot AI), grants use, fine-tune, derivatives; two business conditions (MaaS over $20M revenue needs a separate agreement; 100M MAU or $20M monthly revenue needs "Kimi K3" shown); both exempt "internal use that doesn't make the Software, its outputs, or its capabilities available to third parties". It does not mention training other models. Press said "Modified MIT" at launch; the actual file says "Kimi K3 License".

### 5. DeepSeek

Open Platform Terms (effective April 29, 2026), Section 4.2: you may apply Inputs and Outputs to a wide range of uses including "training other models (such as model distillation)"; "We assign any rights, title, and interests—if any—in the Outputs of the Services to you". No competing clause found. Open weights: V4 is MIT per the official model card (assets "licensed under the MIT License"). DeepSeek-V3 (Oct 2023 license) is the older DeepSeek License with use-based restrictions.

### 6. Qwen

Hugging Face page for Qwen/Qwen3.5-9B shows Apache License 2.0. The Qwen3.5 README is reported to say all open-weight models are Apache 2.0 (via a mirror). Running locally via Ollama is open-weights use. I could not find the hosted Qwen Chat or Alibaba Model Studio terms.

### 7. Google

Gemini API Additional Terms (last updated 2026-04-28): "You may not use the Services to develop models that compete with the Services (e.g., Gemini API or Google AI Studio)." Also bars attempts to "reverse engineer, extract or replicate any component of the Services". No general ban on training on outputs; carve-outs: "analyze, train on, or otherwise learn from Grounded Results or Search Suggestions" and "train on any Google Maps Data" are banned. Unpaid tier: Google may use your inputs and outputs to develop its ML; paid tier: it does not. The Gemini consumer app terms were not verified.

## Plain summary

- Open-weight models you run yourself (Qwen Apache 2.0, DeepSeek MIT, Kimi K3 license) and the DeepSeek API: nothing in the texts I read blocks using them to help build Sapling, including training on outputs (DeepSeek API says so outright).
- Anthropic, OpenAI, Google, Moonshot app, xAI: all bar using the service or its outputs to build a model that "competes". None defines "compete" except Anthropic's help article, which says general-purpose chatbots and open-ended text generation count. None of them says anything about using the tool only to write code or run jobs for your own model. That question is open, not answered either way.
- Biggest unverified pieces: live OpenAI pages, both xAI pages, Qwen hosted terms, Gemini consumer terms, DeepSeek V4 LICENSE file, Anthropic consumer terms version date (may be stale).

## Claude's own read of the Anthropic help article (fetched 10/16 11:36 AM)
"Can I use my Outputs to train an AI model?" (updated March 16, 2026, support.claude.com/en/articles/12326764):
- "We prohibit customers from using our services to train or develop AI models without our written permission."
- Allowed (non-competing): sentiment analysis, content categorization, summarization, information extraction, semantic search, anomaly detection.
- Prohibited: "General purpose chatbots", "Models designed for open-ended text generation".
Read honestly: Sapling (a model that chats and generates open text) sits on the PROHIBITED side of these examples, and the first
line asks for Anthropic's written permission to use its services to train/develop AI models at all. So Claude stays off Sapling
model work unless Anthropic gives written permission.
