$dbPath = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$pwd = "quest1234"
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

$indexes = $conn.GetSchema("Indexes") | Where-Object { $_.TABLE_NAME -eq "T_QUEST" }
Write-Host "=== INDEXES SUR T_QUEST ==="
foreach ($idx in $indexes) {
    Write-Host "Index: $($idx.INDEX_NAME) | Col: $($idx.COLUMN_NAME) | PrimaryKey: $($idx.PRIMARY_KEY) | Unique: $($idx.UNIQUE)"
}

$conn.Close()
