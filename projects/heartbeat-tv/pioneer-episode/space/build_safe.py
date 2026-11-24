# wrapper: run build.py; on any Python error log it and quit the editor (an unattended run has nobody to close it)
import traceback, unreal
try:
    exec(compile(open("C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode/space/build.py").read(), "build.py", "exec"), {"__name__": "__build__"})
except Exception:
    unreal.log_error("PIONEER | BUILD FAILED\n" + traceback.format_exc()); unreal.SystemLibrary.quit_editor()
