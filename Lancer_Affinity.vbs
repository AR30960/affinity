Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = scriptDir
WshShell.Run Chr(34) & scriptDir & "\Affinity.bat" & Chr(34), 0
Set fso = Nothing
Set WshShell = Nothing

