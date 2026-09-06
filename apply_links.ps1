$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$pwd = "quest1234"
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

Write-Host "Mise à jour des liaisons miroir Type P (80001..80016) <-> Type T (85001..85016)..."
for ($i = 0; $i -lt 16; $i++) {
    $idP = 80001 + $i
    $idT = 85001 + $i
    
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = "UPDATE [T_QUEST] SET N_QUEST_LIE = $idT WHERE N_QUEST = $idP"
    $cmd.ExecuteNonQuery()

    $cmd.CommandText = "UPDATE [T_QUEST] SET N_QUEST_LIE = $idP WHERE N_QUEST = $idT"
    $cmd.ExecuteNonQuery()
}

Write-Host ">>> Succès ! Vérification des liaisons :"
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT N_QUEST, N_QUEST_LIE, LB_QUEST FROM [T_QUEST] WHERE N_CLASSE = 8 ORDER BY N_QUEST"
$ad = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
[void]$ad.Fill($dt)
foreach ($r in $dt.Rows) {
    Write-Host "  N_QUEST=$($r['N_QUEST']) -> lié à N_QUEST_LIE=$($r['N_QUEST_LIE']) | $($r['LB_QUEST'].Substring(0, [Math]::Min(35, $r['LB_QUEST'].Length)))..."
}

$conn.Close()
