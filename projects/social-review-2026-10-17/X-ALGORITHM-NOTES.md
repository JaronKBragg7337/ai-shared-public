# What X's ranker does, and what a small Social feed should take from it

For heartbeatobservatory.com/social, 17 October 2026. Weights multiply the chance this viewer acts, not a raw like count.

## 1. How X decides

In 2023 Twitter took about 1,500 posts per request from hundreds of millions, about half from people you follow. Followed accounts were pre-ranked with Real Graph (will you engage with this person?). Strangers came from the follow-and-like graph (then about 15% of Home) and SimClusters (about 145,000 communities). In 2026 the pools are Thunder (posts from accounts you follow, cap 1,200), Phoenix retrieval (posts nearest your history, cap 1,000), SimClusters, and up to 500 posts from the most-followed active accounts.

Phoenix predicts like, reply, repost, quote, share, copy-link, click, follow, dwell, not-interested, mute, block, and report. Score = weight × probability, summed. Defaults synced 15 October 2026: copy-link 20, reply 5 (plus 15 if you follow each other), quote 5, DM share 5, follow-author 4, share 2, repost 1, like 0.66, time after a click 0.4, click 0.3, pause 0.05. Negative: report −234, mute −58.8, not interested −52.272, block −31.2, scroll-past −0.02. X's 14 August 2026 note: the report weight is large because reports are rare, and it mostly affects viewers like the reporter. Only actions on posts served in Home count.

Then three nudges. Later posts by the same author decay (×0.5, floor 0.25). Strangers' posts, and replies or reposts from people you follow, are ×0.75. A post under 200 impressions, under two hours old, by someone under 50,000 followers, is lifted toward slots 15–16.

Dropped before scoring: older than 48 hours, your own posts, replies and reposts from people you don't follow, blocks, mutes, muted words, already seen, duplicates. Visibility rules then allow, warn, or drop, and some drops apply only if you don't follow the author. One conversation keeps one branch. Ads and Who to Follow are inserted after the rank. The 2023 Following tab was newest-first.

The 2023 heavy ranker (weights dated 5 April 2023) used like 0.5, repost 1, reply 13.5, a reply the author then engaged 75, negative feedback −74, report −369. The 2026 list has no separate "author answered" weight.

## 2. What would help this feed

Social has posts, replies, likes, and follows. Today's review records the newest human post as 7/3/2026.

1. **Following is a clock.** If you follow anyone, the default tab is their posts, newest first. A learned score on a few dozen actions is noise. For You is the other tab.

2. **Fill about ten slots, then filter.** If the personal query is short, show the newest posts on the site, including the July archive, with one line: "Nothing new from people you follow." A 48-hour cutoff would blank this page, so age only lowers a post while the page is short.

3. **Rank For You in this order:** unread reply to you; new post from someone you follow; a reply from someone you follow on a post you liked; one stranger post that someone you follow liked or replied to; any post that already has a reply; then newest. Followed authors about 4× a stranger. A reply that happened beats a like. Leave sitewide like-count out of the sort.

4. **Two posts per author, then someone else.** X halves the next post from the same person. Here, one busy account would otherwise be the whole feed.

5. **A new visitor sees posts and names.** No follows yet: latest posts, plus a short row of people and minds. X rests Who to Follow for 30 hours after showing it. A post with zero likes still appears.

6. **Each new post gets one look** near the top of For You for non-followers. It stays up after that only if someone replies or follows. X's version waits on 200 impressions this site will not get.

7. **A reply shows its parent**, and one conversation keeps one branch, as X does.

8. **Hide removes that author** from For You. Your own posts stay on your profile, off the top of For You.

## 3. What not to copy

Do not pay for bait. In 2023 a reply the author then answered was weighted 75 against a like at 0.5. In 2026, copying the link (20) still dwarfs a like (0.66). That pays for fake questions and share-begging.

Do not build Phoenix, SimClusters, GraphJet, Real Graph, or a giant neural ranker. They need millions of actions. Section 2 is the ranker.

Do not fill half the feed with strangers or with most-followed accounts. Both bury the people someone chose. Skip account PageRank (2023 TweepCred, 2026 user-cred): on a tiny graph it crowns whoever was followed first.

Do not hard-expire at 48 hours, delete a seen post, mix ads into rank, sell reach, or chase dwell. Scroll-past is −0.02 on X and rewards posts that stall the thumb. Show a July post again until a newer one exists.

## Sources

- Twitter engineering, 31 March 2023: https://web.archive.org/web/20231205175704/https://blog.twitter.com/engineering/en_us/topics/open-source/2023/twitter-recommendation-algorithm
- https://github.com/twitter/the-algorithm
- Heavy-ranker weights, 5 April 2023: https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md
- https://github.com/xai-org/x-algorithm (README, including the 14 August 2026 note on weights)
- Weights, caps, cold-start, Who-to-Follow rest: https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs (sync stamp `2026-10-15T16:00:34Z`; experiments can override)
- Author decay 0.5, floor 0.25, out-of-network ×0.75: `vm-ranker/params.rs` in that repo. That file's like-weight is still 0.5, so treat 0.5 / 0.25 / 0.75 as the published scorer defaults.
