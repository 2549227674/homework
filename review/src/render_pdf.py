# -*- coding: utf-8 -*-
"""用 LibreOffice（UNO）打开 docx、刷新目录等索引后导出 PDF 预览。

Word 打开 docx 时会提示“更新域”以生成目录；LibreOffice 的命令行转换不会自动刷新目录，
因此这里通过 UNO 接口显式更新全部索引再导出，便于检查排版。
用法：python3 render_pdf.py 输入.docx 输出.pdf
"""
import os
import subprocess
import sys
import tempfile
import time

import uno
from com.sun.star.beans import PropertyValue


def prop(name, value):
    p = PropertyValue()
    p.Name, p.Value = name, value
    return p


def main(src, dst):
    src, dst = os.path.abspath(src), os.path.abspath(dst)
    profile = tempfile.mkdtemp(prefix="lo_profile_")
    env = dict(os.environ, SAL_USE_VCLPLUGIN="svp")
    port = 2083
    proc = subprocess.Popen(
        ["soffice", f"-env:UserInstallation=file://{profile}", "--headless", "--invisible", "--norestore",
         "--nologo", f"--accept=socket,host=127.0.0.1,port={port};urp;"],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        ctx = None
        for _ in range(120):
            try:
                ctx = resolver.resolve(f"uno:socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext")
                break
            except Exception:
                time.sleep(0.5)
        if ctx is None:
            raise RuntimeError("无法连接 LibreOffice")
        desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(src), "_blank", 0, (prop("Hidden", True),))
        for _ in range(2):  # 两次刷新，保证页码稳定
            idx = doc.getDocumentIndexes()
            for i in range(idx.getCount()):
                idx.getByIndex(i).update()
        doc.storeToURL(uno.systemPathToFileUrl(dst), (prop("FilterName", "writer_pdf_Export"),))
        doc.close(True)
        print("PDF 已导出：", dst)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
