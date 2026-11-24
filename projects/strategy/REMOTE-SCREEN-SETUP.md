# Remote screen setup (local build, not yet deployed)

1. Review and apply `projects/strategy/remote-signals.sql` in the Supabase SQL editor. Do not apply it until ready to test.
2. Push the site branch `remote-tool` and deploy it using the site's normal workflow. The branch is based on the existing local main; check its divergence from origin before merging.
3. On the MSI, run `powershell -ExecutionPolicy Bypass -File tools/install-remote-task.ps1` in the signed-in desktop account. This only installs the task.
4. To enable it, create the empty file `state/remote.enable`, make sure `state/remote.disable` does not exist, then run `Start-ScheduledTask -TaskName 'HB Remote Screen'`. The interactive Windows desktop must be signed in and unlocked.
5. Open `/admin/remote/` as an admin and tap Start. To block immediately, create `state/remote.disable` or remove `state/remote.enable`. The agent checks the files during a session.

The signaling table stores a short-lived Supabase access token until the MSI processes the offer or the phone clears it. Restrict service-role access and remove stale rows. The agent verifies that token with Supabase and checks `is_admin` before answering. A failed or closed phone page may leave an expired token/row behind. No TURN relay is configured; some networks will not connect. Sessions time out after 30 minutes without input. Screen capture is the primary monitor. Windows protected/elevated desktops may not accept input from this unelevated task. Phone, database policies, notifications, and full end-to-end operation have not yet been verified.
