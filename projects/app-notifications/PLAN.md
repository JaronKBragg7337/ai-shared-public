# Notifications + app badge (Jaron 10/25 10:51: "build it"; his plan already included a settings page)

Works today for home-screen web apps on iPhone (iOS 16.4+ Web Push + Badging API) - no App Store, no ID. Same backend
carries into the store app later.

1. /settings/notifications/ - one page, plain toggles, everything OFF until the person turns it on:
   - Daily news is live (default suggestion: on)
   - New episode on channels I pick (per-channel)
   - Replies to me on Social
   - Loft messages / calls
   - Quiet hours (e.g. 10 PM - 7 AM)
   - "Turn off everything" one tap
   Not signed in: settings stored with the push subscription itself (no login required - Jaron hates logins).
2. "Turn on notifications" button (Apple requires a tap inside the installed app before asking).
3. Red number on the icon = unseen items (navigator.setAppBadge), cleared when viewed.
4. Sender: Supabase table push_subscriptions (+ prefs) + edge function with VAPID keys; news pipeline calls it on publish.
Order: after the standalone back-button fixes land (same stamped scripts). First slice: news alert + badge + settings page.
