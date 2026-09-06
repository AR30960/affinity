$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$passwords = @("quest1234", "")

$conn = $null
foreach ($pwd in $passwords) {
    try {
        $connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
        $conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
        $conn.Open()
        Write-Host ">>> Connecté avec succès avec le mot de passe : '$pwd'"
        break
    } catch {
        # essayer suivant
    }
}

if ($conn -and $conn.State -eq 'Open') {
    $tables = $conn.GetSchema("Tables") | Where-Object { $_.TABLE_TYPE -eq "TABLE" }
    Write-Host "`n=== TABLES DANS AFFINITY-FULL.MDB ==="
    foreach ($t in $tables) {
        $name = $t.TABLE_NAME
        $cmd = $conn.CreateCommand()
        $cmd.CommandText = "SELECT COUNT(*) FROM [$name]"
        $count = $cmd.ExecuteScalar()
        Write-Host "Table $name : $count enregistrements"
    }
    $conn.Close()
} else {
    Write-Host "Échec de connexion à Affinity-Full.mdb."
}
