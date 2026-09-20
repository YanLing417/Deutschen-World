# -*- coding: utf-8 -*-
"""
安装 Electron 二进制到 DSH profile 的 electron 包内
=====================================================
背景：dsh-builtin-browser 的 Electron provider 只有在找到
      <ancestor>/node_modules/electron/dist/electron.exe 时才会注册；
      而 npm 的 electron 包在此机器上缺少 postinstall 下载（无 Node/npm 可用），
      故 dist/ 与 path.txt 均缺失，导致所有 browser_* 工具报
      "no usable browser provider is registered"。

本脚本用已下载的 electron-v<ver>-win32-x64.zip 补齐 dist/ 与 path.txt。
运行： python tools/install_electron.py
"""
import os
import shutil
import sys
import zipfile

VER = "44.4.3"
_TMP = os.environ.get("TEMP", "/tmp")
# 兼容两种镜像命名（npmmirror 用 electron-<ver>-...，GitHub 用 electron-v<ver>-...）
_CANDS = [os.path.join(_TMP, f"electron-v{VER}-win32-x64.zip"),
          os.path.join(_TMP, f"electron-{VER}-win32-x64.zip")]
ZIP = next((p for p in _CANDS if os.path.exists(p)), _CANDS[0])
PROFILE = r"C:\Users\11763\.dsh\profiles\desktop"
PKG = os.path.join(PROFILE, "node_modules", "electron")
DIST = os.path.join(PKG, "dist")


def main():
    if not os.path.exists(ZIP):
        print(f"!! 未找到下载的 zip：{ZIP}")
        return 1
    size = os.path.getsize(ZIP) / 1024 / 1024
    print(f"zip: {ZIP}  ({size:.1f} MB)")

    if not os.path.isdir(PKG):
        print(f"!! electron 包不存在：{PKG}")
        return 1

    # 校验 zip 完整性
    try:
        with zipfile.ZipFile(ZIP) as z:
            bad = z.testzip()
            if bad:
                print(f"!! zip 损坏（首个坏条目：{bad}）")
                return 1
            names = z.namelist()
    except Exception as ex:
        print(f"!! 无法读取 zip：{ex}")
        return 1
    print(f"zip 条目数：{len(names)}，完整性校验通过")

    if not any(n.lower().endswith("electron.exe") for n in names):
        print("!! zip 内未找到 electron.exe")
        return 1

    # 解包到 dist/
    if os.path.isdir(DIST):
        print(f"dist/ 已存在，清理：{DIST}")
        shutil.rmtree(DIST)
    os.makedirs(DIST, exist_ok=True)
    with zipfile.ZipFile(ZIP) as z:
        z.extractall(DIST)
    print(f"已解包到 {DIST}")

    # npm electron 包用 path.txt 记录相对可执行文件名（供 require('electron') 使用）
    with open(os.path.join(PKG, "path.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("electron.exe")
    print("已写入 path.txt = electron.exe")

    # 校验
    exe = os.path.join(DIST, "electron.exe")
    if not os.path.exists(exe):
        print(f"!! 解包后仍未找到 {exe}")
        return 1
    mb = os.path.getsize(exe) / 1024 / 1024
    print(f"\n✅ electron.exe 就绪：{exe} ({mb:.1f} MB)")

    # 插件探测的标记文件
    res = os.path.join(DIST, "resources")
    if os.path.isdir(res):
        marks = [x for x in os.listdir(res) if x.endswith(".asar")]
        print(f"   resources/*.asar 标记：{marks}")
    ver_file = os.path.join(DIST, "version")
    if os.path.exists(ver_file):
        print(f"   dist/version = {open(ver_file).read().strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
