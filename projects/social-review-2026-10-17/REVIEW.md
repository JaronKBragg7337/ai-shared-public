# Social page review (Claude Code, 2026-10-17 ~1 PM) - heartbeatobservatory.com/social
Jaron: "my account can see things it shouldn't or do things... it has been slipped on and hasn't really been touched."

## Fixed today (database, live)
1. **Anyone could make themselves an admin.** A signed-in user could update their own profile row, including `is_admin`
   (the row rule allowed "your own row" and every column was open). Checked: only Jaron's two accounts + his partner are admins -
   nobody used it. Fix (migration people_lock_admin_column): users can change only handle, display name, bio, avatar.
2. **Admins could rewrite anyone's post.** `posts_admin_all` allowed edit of other people's words. Now admins can only
   DELETE (moderation, used by /admin); nobody can edit someone else's post. (migration posts_admin_delete_only)
Unchanged and fine: bookmarks are private to their owner; likes/reposts/follows/replies/posts readable by all (normal for a
public feed); writes only "as yourself" and only from real (non-guest) accounts.

## Still open - decisions for Jaron
- Public "ADMIN" badge on every admin post (shows his partner as admin to the world). Options: hide badges for everyone but
  the viewer's own account, or keep one badge only on the official company account.
- Likes are public (who liked what). X made likes private in 2024. Options: show counts only.
- "Engine Events" tab = system logs inside the social feed. Belongs on /live-systems, not the feed.
- The feed is dead: newest human post 7/3/2026. Empty feeds kill new sign-ups - see X-ALGORITHM-NOTES.md for what to show.
- Looks: dark + neon green, the only part of the site not on the warm cream brand (the TV, news card and end cards are cream).
  Raw links show in [brackets]; action row cramped at phone width. Candidate: redo in the cream brand (Claude sets the
  look, Sonnet 5.5 / Sol 6.1 build, WebKit phone check before publish).
