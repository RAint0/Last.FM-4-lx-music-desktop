dim wsh
set wsh=wscript.createobject("wscript.shell")
wsh.run "你的LX-music目录\lx-music-desktop.exe"
wsh.run "pythonw pyw脚本所在目录\LastFM4LX.pyw"
