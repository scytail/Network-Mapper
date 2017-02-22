'DOES NOT WORK!!! WILL PERMANENTLY CHANGE THE PATH VAR

If WScript.Arguments.length =0 Then
Set objShell = CreateObject("Shell.Application")

objShell.ShellExecute "wscript.exe", Chr(34) & _
WScript.ScriptFullName & Chr(34) & " uac", "", "runas", 1
Else
'Administrative Code Here
strComputer = "."
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\cimv2")

Set colItems = objWMIService.ExecQuery("Select * From Win32_Environment Where Name = 'Path'")

For Each objItem in colItems

    strPath = objItem.VariableValue & ";C:\Program Files (x86)\Graphviz2.38\bin"
    objItem.VariableValue = strPath
    objItem.Put_

Next

x=msgbox("Graphviz has been added to the System Path." ,0, "AddGraphvizToPath.vbs")

End If
