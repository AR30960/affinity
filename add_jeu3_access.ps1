$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$pwd = "quest1234"
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT COUNT(*) FROM [T_JEU] WHERE N_JEU = 3"
$cnt = $cmd.ExecuteScalar()
if ($cnt -eq 0) {
    $cmd.CommandText = "INSERT INTO [T_JEU] (N_JEU, LB_JEU) VALUES (3, 'Jeu 3')"
    $cmd.ExecuteNonQuery()
    Write-Host "Jeu 3 inséré avec succès dans T_JEU de Access."
} else {
    Write-Host "Jeu 3 est déjà présent dans T_JEU de Access."
}

$conn.Close()
