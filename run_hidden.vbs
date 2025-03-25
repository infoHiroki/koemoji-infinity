Set WshShell = CreateObject("WScript.Shell")
CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = CurrentDirectory
WshShell.Run "pythonw main.py", 0, False 