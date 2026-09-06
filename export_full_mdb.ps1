$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$pwd = "quest1234"
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

$result = @{}
$tables = @("T_CLASSE", "T_JEU", "T_PRF", "T_QUEST", "T_REPA", "T_REPD", "T_REPG", "T_REPP", "T_REPV", "T_SUJET", "T_THEMA", "T_CIBLE", "M_REP")

foreach ($t in $tables) {
    try {
        $cmd = $conn.CreateCommand()
        $cmd.CommandText = "SELECT * FROM [$t]"
        $ad = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
        $dt = New-Object System.Data.DataTable
        [void]$ad.Fill($dt)
        
        $rows = @()
        foreach ($row in $dt.Rows) {
            $r = @{}
            foreach ($col in $dt.Columns) {
                $r[$col.ColumnName] = $row[$col.ColumnName]
            }
            $rows += $r
        }
        $result[$t] = $rows
    } catch {
        Write-Host "Table non trouvée ou ignorée : $t ($($_.Exception.Message))"
    }
}

$conn.Close()

$json = $result | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText("C:\_AR\Antigravity\_Devia\ARP001\mdb_full_data.json", $json, [System.Text.Encoding]::UTF8)
Write-Host "Export mdb_full_data.json terminé avec succès !"
