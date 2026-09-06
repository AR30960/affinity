$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$pwd = "quest1234"
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

$tables = @('T_CLASSE', 'T_CIBLE', 'T_THEMA', 'T_SUJET', 'T_QUEST', 'T_JEU')
foreach ($t in $tables) {
    Write-Host "================== TABLE: $t =================="
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = "SELECT * FROM [$t]"
    $ad = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
    $dt = New-Object System.Data.DataTable
    [void]$ad.Fill($dt)
    Write-Host "Nombre total d'enregistrements: $($dt.Rows.Count)"
    foreach ($col in $dt.Columns) {
        Write-Host "  Col: $($col.ColumnName) ($($col.DataType.Name))"
    }
    Write-Host "  Exemples de lignes :"
    $limit = [Math]::Min(5, $dt.Rows.Count)
    for ($i = 0; $i -lt $limit; $i++) {
        $row = $dt.Rows[$i]
        $vals = @()
        foreach ($col in $dt.Columns) {
            $vals += "$($col.ColumnName)=$($row[$col.ColumnName])"
        }
        Write-Host ("    -> " + ($vals -join ' | '))
    }
}

$conn.Close()
