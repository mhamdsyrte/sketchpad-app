[app]
title = دفتر الرسم
package.name = sketchpad
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3,kivy

orientation = portrait
fullscreen = 0

# الصلاحيات اللازمة لحفظ الصورة
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# armeabi-v7a فقط حالياً (32 بت)
android.archs = armeabi-v7a

android.api = 33
android.minapi = 21
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
