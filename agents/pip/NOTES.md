# Pip's notes (company Grok Bot on @HeartbeatObserv) - newest at the bottom

## Who Pip is
- Pip = Heartbeat Observatory LLC's company assistant (a Grok Bot set up by Jaron 10/24 on the @HeartbeatObserv X Premium account).
- Company Gmail: <email> (connected 10/24).
- Jobs:
  1. Inbox watch: weekdays 7 AM / noon / 5 PM Fort Wayne time, plus right away when something urgent comes in. Emails a short update to
     <email> and <email> (both given by Jaron) only when something is new. Also flags outreach replies to Jaron.
  2. Fort Wayne website outreach (brief: projects/company-grok-bot/PIP-BRIEF.md). Signed "Pip, Jaron's AI assistant (Grok Bot)", never as Jaron.
  3. Lead tracker Google Sheet + company calendar reminders.
- Connectors: Gmail, Google Calendar/Sheets/Drive/Docs, Postiz, Vercel, GitHub (@JaronKBragg7337), X, and the MSI connector (added 10/25 with Jaron's OK).
- Hard limits: never signs anything for the LLC; money requests go to Pips Twin via REQUESTS.md, never contacts Jaron's family, never writes as Jaron.
- On the MSI Pip only reads/writes AI-Shared notes unless Jaron asks for more in chat.

---

# HANDOFF - Pip setup + Fort Wayne outreach round 1

- **Date/time:** 2026-10-25 12:40 AM ET (04:40 UTC)
- **From:** Pip (company Grok Bot)
- **Project:** company inbox + Fort Wayne sites  |  **Repo/branch:** n/a (Gmail, Google Sheets/Calendar)  |  **Live URL:** lead tracker below

## What I did
- First crew inbox update sent 10/25 (night of 10/24 ET) to <email> + <email>.
- Fort Wayne outreach round 1 SENT 10/25 ~04:05 UTC (12:05 AM ET) from <email> to 6 businesses: Dyer And Son,
  Willie's Cafe, Chips Auto Repair, George's Auto Repair, Tint Masters, UNIQ BBQ & Shabu. Jaron sent the first one (Dyer) himself from a
  draft card; Pip sent the other 5 the same way. Signed as Pip, CAN-SPAM postal address <address>, Fort Wayne, IN 46835,
  "Reply STOP and I won't email again."
- Rule kept: no follow-ups to any business without a reply. Inbox watch now also flags replies to Jaron (prices / yes answers go to him;
  STOP honored; simple questions answered).
- 10 phone/Facebook-only leads NOT contacted (no company Facebook yet - Jaron 10/25). Nolt's has a preview.
- Lead tracker: "Fort Wayne Website Leads" https://docs.google.com/spreadsheets/d/1ahhijmtqHWuVIiqdpXNdQmVgfdjSwz127JISV7jk91c/edit
  33 leads: the original 16 + 17 round-2 leads found 10/25 (rows 18-34, all "Not contacted"; 9 have emails). Jose Auto Repair and Elite
  Automotive already have another builder's previews - likely skip. Strongest new: Ward Stevens Automotive, 1&Done Maintenance, FullBloom
  Tattoos, Castro Auto Repair, ANK Electric, The Painted Lady; Something Different Hair Salon + Red Wolf Roofing have Google listings
  pointing at the wrong company's site.
- Only 3 preview sites exist (Dyer, Nolt's, Willie's). Sams Twin would need previews before round 2 is pitched. Nobody in round 2 gets
  an email until Jaron approves the round.
- Company calendar reminders (all-day): TuneCore ticket #7006533 check 10/27; Runpod SDK 2.0 change 10/29; X Premium cancel-by 11/16;
  X Premium renews 11/17 ($30).
- Postiz: connected to YouTube, TikTok, X. 60 of last 61 posts fine. 1 failed: "We wrote our own render engine tonight" on YouTube,
  10/20 8:33 PM (YouTube daily upload limit after 4 uploads). It went out on X + TikTok. Waiting on Jaron's OK to reschedule to YouTube.
- Vercel: all 75 deploys in the past week READY; heartbeatobservatory.com up (latest deploy 10/24 11:20 PM); 3 previews live.
- Website repo (JaronKBragg7337/heartbeat-observatory), read only, nothing changed: repo is PUBLIC and includes admin pages +
  api/site-edit - worth verifying they check login server-side; TODO.md untouched since June (real list lives here in AI-Shared);
  an analytics PR from June is still open and looks abandoned.

## Where it lives (exact)
- Local: AI-Shared\agents\pip\NOTES.md (this file); drafts/leads source: projects\fw-sites\
- Remote: Gmail <email> (Sent), the lead tracker Sheet above, the company Google Calendar.

## Verified vs assumed
- Verified: all 6 outreach emails returned Gmail message ids / show in Sent; Sheet rows written; calendar events created;
  Postiz + Vercel status read from their APIs.
- Assumed: none of the 6 has replied yet (as of 12:40 AM ET 10/25).

## Blocked / needs a human
- Company calendar is set to UTC, so all-day reminders fire a few hours early - needs Jaron: Google Calendar > Settings > Time zone > Eastern.
- Postiz YouTube reschedule of the 10/20 render-engine post - needs Jaron's OK.
- Round-2 outreach - needs Jaron's OK + Sams Twin previews.
- Whether to keep <email> on the updates - Jaron hasn't said (Pip kept it because he gave it directly).

## Exact next step for the next AI
- Nothing for the MSI side right now. If a business replies with a yes or a price question, Pip brings it to Jaron; whoever builds the
  real site after a yes should start from that business's preview (fw-preview-*.vercel.app).

## 2026-10-25 ~12:45 UTC (8:45 AM ET): Round 2 sent
- Sent from company Gmail, signed "Jaron's AI assistant (Pip)", with CAN-SPAM address and STOP line: Ward Stevens Automotive
  (<email>), 1&Done Maintenance (<email>), FullBloom Tattoos (<email>),
  Castro Auto Repair (<email>), The Painted Lady (<email>). Each links its
  heartbeatobservatory.com/preview/ page. No payment info in any email.
- ANK Electric on hold.
- No second email to anyone without a reply. Inbox routine watches for replies/STOP.
- Standing fixes done: calendar reminders moved to 9 AM Eastern (4 new timed events 9:00-9:15 AM America/Indiana/Indianapolis, 1-day
  popup + email reminder: TuneCore #7006533 check 10/27, Runpod SDK 2.0 10/29, X Premium cancel-by 11/16, X Premium renews $30 11/17;
  old all-day UTC copies deleted). The calendar's own time zone setting is still UTC - the connector can't change it, so Jaron would set
  it in Google Calendar > Settings > Time zone. Lead tracker rows for the 5 round-2 businesses set to "Emailed - waiting for reply"
  2026-10-25 with preview links; ANK Electric note added (on hold: state registration surrendered 4/2024, Jaron deciding).
  From now on approved outreach is sent directly, no cards.
- Money rule updated: Pip no longer "never sends money"; money moves go through Pips Twin via agents/pip/REQUESTS.md.

## 2026-10-25 ~12:51 UTC: Sender name fix - BLOCKED
- Goal: change company Gmail From name 'Jaron Bragg' to 'Heartbeat Observatory' (Gmail Settings > Accounts and Import > Send mail as > edit info).
- Gmail connector has no send-as edit tool (only list_send_as). Pip's box browser has no Google session: mail.google.com redirects to accounts.google.com sign-in.
- Step needing a login: sign in to <email> in Pip's box browser (password + likely 2FA), or Jaron/Claude changes it in Gmail web settings on the MSI. After that the change takes 30 seconds.

## 2026-10-25 ~13:05 UTC: Sender name FIXED
- Jaron renamed the Google account to 'Heartbeat Observatory' (and set the HO logo). Gmail send-as has no custom display name, so outgoing mail now shows 'Heartbeat Observatory <<email>>'. The earlier BLOCKED entry is resolved.
- Calendar: Jaron set the phone app to Eastern, but the calendar's own time zone (API) still reads UTC. Events Pip creates carry an explicit America/Indiana/Indianapolis time zone, so reminders are right either way. Web setting still needs changing at calendar.google.com > Settings > General > Time zone.

## 2026-10-25 ~13:45 UTC: D&B legal form fix (Corporation -> LLC)
- D-U-N-S 149995648 was created Oct 19 (Case # 11120303, Tracking ID 11061893). The record lists Legal Form: Corporation. It should be LLC (Indiana).
- Reply drafted to <email> in the Case # 11120303 thread, asking them to change the legal form to LLC. Signed "Jaron's AI assistant (Pip)". Waiting on Jaron's tap.
- If D&B says it needs a form or a login instead:
  1. Form: the Oct 16 "Just a Nudge" email has BIR_FORM_USA.docx attached. Fill it with Heartbeat Observatory LLC, <address>, Fort Wayne, IN 46835, D-U-N-S 149995648, legal form LLC. Reply in that same thread with the form and 1-2 docs showing the name and address (Indiana SOS Articles of Organization / business entity record, or the IRS EIN letter CP575). Jaron has to sign the form himself; Pip never signs for the LLC.
  2. Login: go to dnb.com, then D-U-N-S Number lookup / "Update your D&B business information" (D&B Business Directory, also called iUpdate). Look up D-U-N-S 149995648, sign in or create a free account as <email>, verify through the email code, then edit Company Profile and set Legal Structure to Limited Liability Company with State of Incorporation Indiana, and save. Updates usually show in 24-48 hours.
  3. Phone fallback: call D&B customer service and give D-U-N-S 149995648 and case 11120303.

## 2026-10-26 ~17:40 UTC: TuneCore answered ticket #7006533 - NOT replied, waiting for Claude
- Lee (TuneCore Artist Support) replied Oct 26, 1:34 PM EDT to the Oct 24 question about synthesized / rule-based music from the beat tool.
- Gist: TuneCore supports GenAI music only where the underlying models rely on fully licensed datasets. Artists should look for clear info on how a tool is trained, explicit licensing/rights-clearance of training data, and transparent ToS on ownership/usage. Links FAQ: https://support.tunecore.com/hc/en-us/articles/46914166185236-TuneCore-s-GenAI-Music-Content-Framework
- It's a template answer; it does NOT directly say yes/no for math-synthesized, rule-based music with no trained model or dataset.
- Pip's read: no training data means the licensing concern shouldn't apply, but it's unconfirmed. Possible follow-up: ask Lee for a plain yes/no.
- Jaron wants Claude to review before anyone replies (missing flow context). Pip will not reply until Jaron or Claude says so.
- Also unanswered: the YouTube Content ID question (whether a beat used in only one song can be registered).
- Proposed follow-up for Claude to review (reply in ticket thread 1a16ff5f4d298a27, to TuneCore support, signed as Pip): "Hi Lee, thanks for the reply. To clarify, our beat engine doesn't use any trained AI model or dataset at all. Every sound is synthesized with math, and the beats come from music-theory rules plus randomness, with no samples and no training on recordings. Since there's no training data to license, could you confirm with a yes or no whether tracks made this way are eligible for TuneCore distribution, and whether a beat used in only one song can be registered for YouTube Content ID? Thank you. Pip, Jaron's AI assistant, for Heartbeat Observatory LLC"
- Context from Jaron (10/26): the beat is used in one song for now, but artists from his past music era have finished albums waiting. Releasing those through Heartbeat is a planned revenue line, so TuneCore/Content ID rules for beats shared across multiple artists' songs will matter later.
