$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$pwd = "quest1234"
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT COUNT(*) FROM [T_QUEST] WHERE N_CLASSE = 8"
$cnt8 = $cmd.ExecuteScalar()
Write-Host "Nombre de questions de classe 8 dans T_QUEST de Access : $cnt8"

$cmd.CommandText = "SELECT DISTINCT N_CLASSE, COUNT(*) as cnt FROM [T_QUEST] GROUP BY N_CLASSE"
$ad = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
[void]$ad.Fill($dt)
foreach ($row in $dt.Rows) {
    Write-Host "  N_CLASSE=$($row['N_CLASSE']) -> $($row['cnt']) questions"
}

$conn.Close()
