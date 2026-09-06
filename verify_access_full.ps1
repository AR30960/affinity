$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$pwd = "quest1234"
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

Write-Host "=== VÉRIFICATION GLOBALE D'AFFINITY-FULL.MDB ==="
$cmd = $conn.CreateCommand()

$cmd.CommandText = "SELECT COUNT(*) FROM [T_QUEST]"
Write-Host "Total questions dans T_QUEST : $($cmd.ExecuteScalar())"

$cmd.CommandText = "SELECT COUNT(*) FROM [T_QUEST] WHERE N_CLASSE = 8"
Write-Host "Questions de classe 8 dans T_QUEST : $($cmd.ExecuteScalar())"

$cmd.CommandText = "SELECT COUNT(*) FROM [T_QUEST_IDENTITE]"
Write-Host "Lignes dans T_QUEST_IDENTITE : $($cmd.ExecuteScalar())"

$cmd.CommandText = "SELECT COUNT(*) FROM [T_QUEST_IDENTITE_OPT]"
Write-Host "Lignes dans T_QUEST_IDENTITE_OPT : $($cmd.ExecuteScalar())"

Write-Host "`n=== ÉCHANTILLON T_QUEST_IDENTITE (Type P & Type T) ==="
$cmd.CommandText = "SELECT TOP 6 N_QUEST, TP_QUEST, MODE_REPONSE, DIMENSION, VAL_MIN, VAL_MAX, UNITE, TOLERANCE_INDIFFERENT FROM [T_QUEST_IDENTITE] ORDER BY N_QUEST"
$ad = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
[void]$ad.Fill($dt)
foreach ($r in $dt.Rows) {
    Write-Host "  N_QUEST=$($r['N_QUEST']) | Type=$($r['TP_QUEST']) | Mode=$($r['MODE_REPONSE']) | Dim=$($r['DIMENSION']) | Min=$($r['VAL_MIN']) | Max=$($r['VAL_MAX']) $($r['UNITE']) | Indiff=$($r['TOLERANCE_INDIFFERENT'])"
}

Write-Host "`n=== ÉCHANTILLON T_QUEST_IDENTITE_OPT (Options d'une question) ==="
$cmd.CommandText = "SELECT TOP 7 N_QUEST, NUM_OPT, LB_OPT FROM [T_QUEST_IDENTITE_OPT] WHERE N_QUEST = 80003 ORDER BY NUM_OPT"
$dt = New-Object System.Data.DataTable
[void]$ad.Fill($dt)
foreach ($r in $dt.Rows) {
    Write-Host "  N_QUEST=$($r['N_QUEST']) | Option #$($r['NUM_OPT']) : $($r['LB_OPT'])"
}

$conn.Close()
