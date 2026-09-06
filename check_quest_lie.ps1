$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$pwd = "quest1234"
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT DISTINCT N_QUEST_LIE FROM [T_QUEST] WHERE N_QUEST_LIE <> 0"
$ad = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
[void]$ad.Fill($dt)
Write-Host "Valeurs de N_QUEST_LIE existantes (différentes de 0):"
foreach ($r in $dt.Rows) {
    Write-Host "  N_QUEST_LIE = $($r['N_QUEST_LIE'])"
}

$conn.Close()
