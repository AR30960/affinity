' Script de lancement d'arriere-plan 100% silencieux et autonome pour Affinity
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = scriptDir

' 1. Verifier si le port 8765 est deja en ecoute
Dim netstatCmd, checkPort
netstatCmd = "cmd /c netstat -ano | findstr /R /C:" & Chr(34) & ":8765 .*LISTENING" & Chr(34)
checkPort = WshShell.Run(netstatCmd, 0, True)

If checkPort <> 0 Then
    ' 2. Identifier l'interpreteur Python approprie (priorite pythonw sans console)
    Dim pythonExe
    If fso.FileExists(scriptDir & "\.venv\Scripts\pythonw.exe") Then
        pythonExe = scriptDir & "\.venv\Scripts\pythonw.exe"
    ElseIf fso.FileExists(scriptDir & "\.venv\Scripts\python.exe") Then
        pythonExe = scriptDir & "\.venv\Scripts\python.exe"
    Else
        pythonExe = "pythonw"
    End If

    ' 3. Lancement silencieux et completement detache
    Dim startCmd
    startCmd = Chr(34) & pythonExe & Chr(34) & " " & Chr(34) & scriptDir & "\server.py" & Chr(34)
    WshShell.Run startCmd, 0, False
End If

Set fso = Nothing
Set WshShell = Nothing
