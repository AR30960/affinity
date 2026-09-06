$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$pwd = "quest1234"
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

Write-Host "=== T_CLASSE ==="
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT * FROM [T_CLASSE] ORDER BY N_CLASSE"
$ad = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
[void]$ad.Fill($dt)
foreach ($row in $dt.Rows) {
    Write-Host "  N_CLASSE=$($row['N_CLASSE']) | LB_CLASSE=$($row['LB_CLASSE'])"
}

Write-Host "`n=== T_THEMA ==="
$cmd.CommandText = "SELECT * FROM [T_THEMA] ORDER BY N_THEMA"
$dt = New-Object System.Data.DataTable
[void]$ad.Fill($dt)
foreach ($row in $dt.Rows) {
    Write-Host "  N_THEMA=$($row['N_THEMA']) | LB_THEMA=$($row['LB_THEMA'])"
}

Write-Host "`n=== T_SUJET ==="
$cmd.CommandText = "SELECT * FROM [T_SUJET] ORDER BY N_THEMA, N_SUJET"
$dt = New-Object System.Data.DataTable
[void]$ad.Fill($dt)
foreach ($row in $dt.Rows) {
    Write-Host "  N_THEMA=$($row['N_THEMA']) | N_SUJET=$($row['N_SUJET']) | LB_SUJET=$($row['LB_SUJET'])"
}

$conn.Close()
