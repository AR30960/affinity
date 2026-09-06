$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$pwd = "quest1234"
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

$tables = @('T_CLASSE', 'T_REPG', 'T_REPV', 'T_REPA', 'T_REPD', 'T_REPP', 'M_REP')
foreach ($t in $tables) {
    Write-Host "================== TABLE: $t =================="
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = "SELECT * FROM [$t]"
    $ad = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
    $dt = New-Object System.Data.DataTable
    [void]$ad.Fill($dt)
    Write-Host "Nombre total: $($dt.Rows.Count)"
    foreach ($col in $dt.Columns) {
        Write-Host "  Col: $($col.ColumnName) ($($col.DataType.Name))"
    }
    foreach ($row in $dt.Rows) {
        $vals = @()
        foreach ($col in $dt.Columns) {
            $vals += "$($col.ColumnName)=$($row[$col.ColumnName])"
        }
        Write-Host ("    -> " + ($vals -join ' | '))
    }
}

$conn.Close()
