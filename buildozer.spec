[app]
title = ColorGamePredictor
package.name = colorgamehack
package.domain = org.mj.hacks
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,pillow,plyer,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, SYSTEM_ALERT_WINDOW, VIBRATE, WAKE_LOCK, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = ./bin
