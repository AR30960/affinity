$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity.mdb"
$pwd = "quest1234"

# Essai 1: OLEDB ACE 12/16
$oledbProviders = @("Microsoft.ACE.OLEDB.16.0", "Microsoft.ACE.OLEDB.12.0", "Microsoft.Jet.OLEDB.4.0")

$connected = $false
foreach ($prov in $oledbProviders) {
    try {
        $connStr = "Provider=$prov;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
        $conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
        $conn.Open()
        Write-Host ">>> Connecté avec succès via OLEDB: $prov"
        $connected = $true
        break
    } catch {
        # Essayer le suivant
    }
}

if (-not $connected) {
    try {
        $connStr = "Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=$dbPath;PWD=$pwd;"
        $conn = New-Object System.Data.Odbc.OdbcConnection($connStr)
        $conn.Open()
        Write-Host ">>> Connecté avec succès via ODBC"
        $connected = $true
    } catch {
        Write-Host "Erreur connexion ODBC: " $_.Exception.Message
    }
}

if ($connected) {
    Write-Host "`n=== LISTE DES TABLES ==="
    $tables = $conn.GetSchema("Tables")
    $userTables = $tables | Where-Object { $_.TABLE_TYPE -eq "TABLE" }
    $userTables | Select-Object TABLE_NAME | Format-Table -AutoSize
    
    foreach ($tbl in $userTables) {
        $name = $tbl.TABLE_NAME
        Write-Host "`n--- TABLE: $name ---"
        $cmd = $conn.CreateCommand()
        $cmd.CommandText = "SELECT COUNT(*) FROM [$name]"
        $count = $cmd.ExecuteScalar()
        Write-Host "Nombre de lignes : $count"
        
        $cmd.CommandText = "SELECT TOP 5 * FROM [$name]"
        $adapter = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
        $dt = New-Object System.Data.DataTable
        [void]$adapter.Fill($dt)
        $dt | Format-Table -AutoSize
    }
    $conn.Close()
}
