# Script de mise à jour d'Affinity-Full.mdb pour la Classe 8 et l'Option B
$ErrorActionPreference = "Stop"

$srcDb = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full.mdb"
$backupDb = "C:\_AR\Antigravity\_Devia\ARP001\Affinity-Full_BACKUP_20260905.mdb"
$jsonFile = "C:\_AR\Antigravity\_Devia\ARP001\classe8_questions.json"
$pwd = "quest1234"

Write-Host ">>> 1. Sauvegarde préalable de la base Access..."
Copy-Item -Path $srcDb -Destination $backupDb -Force
Write-Host "Sauvegarde créée : $backupDb"

Write-Host "`n>>> 2. Connexion à Affinity-Full.mdb..."
$connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$srcDb;Jet OLEDB:Database Password=$pwd;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

function Execute-Sql($sql) {
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = $sql
    return $cmd.ExecuteNonQuery()
}

function Execute-Scalar($sql) {
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = $sql
    return $cmd.ExecuteScalar()
}

Write-Host "`n>>> 3. Vérification / Insertion de T_THEMA et T_SUJET pour la Classe 8 (Identité)..."
$themaCount = Execute-Scalar "SELECT COUNT(*) FROM [T_THEMA] WHERE N_THEMA = 8"
if ($themaCount -eq 0) {
    Execute-Sql "INSERT INTO [T_THEMA] (N_THEMA, LB_THEMA) VALUES (8, 'Identité')"
    Write-Host "  -> Thématique 8 (Identité) créée dans T_THEMA."
} else {
    Write-Host "  -> Thématique 8 déjà présente dans T_THEMA."
}

$sujetCount = Execute-Scalar "SELECT COUNT(*) FROM [T_SUJET] WHERE N_THEMA = 8 AND N_SUJET = 1"
if ($sujetCount -eq 0) {
    Execute-Sql "INSERT INTO [T_SUJET] (N_THEMA, N_SUJET, LB_SUJET) VALUES (8, 1, 'Identité')"
    Write-Host "  -> Sujet (8, 1) créé dans T_SUJET."
} else {
    Write-Host "  -> Sujet (8, 1) déjà présent dans T_SUJET."
}

# S'assurer que LB_CLASSE pour la classe 8 est bien 'Identité'
Execute-Sql "UPDATE [T_CLASSE] SET LB_CLASSE = 'Identité' WHERE N_CLASSE = 8"
# S'assurer que LB_CLASSE pour la classe 5 est bien 'A caractère sexuel' (sans accent)
Execute-Sql "UPDATE [T_CLASSE] SET LB_CLASSE = 'A caractère sexuel' WHERE N_CLASSE = 5"

Write-Host "`n>>> 4. Création des tables relationnelles dédiées pour les questions de Classe 8 (Option B)..."
# Vérifier si T_QUEST_IDENTITE existe
$tables = $conn.GetSchema("Tables") | Where-Object { $_.TABLE_NAME -eq "T_QUEST_IDENTITE" }
if (-not $tables) {
    $createTableSql = @"
CREATE TABLE [T_QUEST_IDENTITE] (
    [N_QUEST] LONG PRIMARY KEY,
    [TP_QUEST] TEXT(1),
    [MODE_REPONSE] TEXT(20),
    [DIMENSION] TEXT(100),
    [VAL_MIN] DOUBLE,
    [VAL_MAX] DOUBLE,
    [PAS_VAL] DOUBLE,
    [UNITE] TEXT(20),
    [DEFAULT_MIN] DOUBLE,
    [DEFAULT_MAX] DOUBLE,
    [TOLERANCE_INDIFFERENT] YESNO,
    [LISTE_OPTIONS] MEMO
)
"@
    Execute-Sql $createTableSql
    Write-Host "  -> Table T_QUEST_IDENTITE créée avec succès."
} else {
    Write-Host "  -> Table T_QUEST_IDENTITE existe déjà."
}

# Table relationnelle pour les options individuelles
$tablesOpt = $conn.GetSchema("Tables") | Where-Object { $_.TABLE_NAME -eq "T_QUEST_IDENTITE_OPT" }
if (-not $tablesOpt) {
    $createOptSql = @"
CREATE TABLE [T_QUEST_IDENTITE_OPT] (
    [N_QUEST] LONG,
    [NUM_OPT] INTEGER,
    [LB_OPT] TEXT(255),
    PRIMARY KEY ([N_QUEST], [NUM_OPT])
)
"@
    Execute-Sql $createOptSql
    Write-Host "  -> Table relationnelle T_QUEST_IDENTITE_OPT créée avec succès."
} else {
    Write-Host "  -> Table relationnelle T_QUEST_IDENTITE_OPT existe déjà."
}

Write-Host "`n>>> 5. Chargement des données des 32 questions de classe 8..."
$jsonContent = Get-Content $jsonFile -Raw -Encoding UTF8
$questions = $jsonContent | ConvertFrom-Json

# Nettoyage préalable des éventuelles entrées précédentes pour idempotence
Execute-Sql "DELETE FROM [T_QUEST_IDENTITE_OPT] WHERE N_QUEST IN (SELECT N_QUEST FROM [T_QUEST] WHERE N_CLASSE = 8)"
Execute-Sql "DELETE FROM [T_QUEST_IDENTITE] WHERE N_QUEST IN (SELECT N_QUEST FROM [T_QUEST] WHERE N_CLASSE = 8)"
Execute-Sql "DELETE FROM [T_QUEST] WHERE N_CLASSE = 8"

Write-Host "`n>>> 6. Insertion des 32 questions dans T_QUEST, T_QUEST_IDENTITE et T_QUEST_IDENTITE_OPT..."
$count = 0
$nowStr = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

# Mapping des questions liées miroir (80001..80016 <-> 80017..80032)
$linkedMap = @{}
for ($i = 0; $i -lt 16; $i++) {
    $idP = 80001 + $i
    $idT = 80017 + $i
    $linkedMap[$idP] = $idT
    $linkedMap[$idT] = $idP
}

foreach ($q in $questions) {
    $nQuest = [int]$q.id
    $nJeu = [int]$q.pack_id
    if ($nJeu -le 0) { $nJeu = 1 }
    $nClasse = [int]$q.classe
    $nCible = [int]$q.cible
    $nPorteeThema = 8
    $nPorteeSujet = 1
    $lbQuest = $q.texte.Replace("'", "''")
    $linkedId = if ($linkedMap.ContainsKey($nQuest)) { $linkedMap[$nQuest] } else { 0 }
    
    # 1. Insertion dans T_QUEST avec N_QUEST_LIE=0 pour respecter la contrainte auto-référencée
    $sqlQuest = "INSERT INTO [T_QUEST] (N_JEU, N_CLASSE, N_CIBLE, N_THEMA, N_SUJET, N_QUEST, LB_QUEST, N_QUEST_LIE, DT_CRE, AUTOR) " +
                "VALUES ($nJeu, $nClasse, $nCible, $nPorteeThema, $nPorteeSujet, $nQuest, '$lbQuest', 0, '$nowStr', 'ADM')"
    Execute-Sql $sqlQuest

    # 2. Préparation des détails pour T_QUEST_IDENTITE
    $cfg = $q.config
    $tpQuest = $q.type
    $mode = if ($cfg.mode) { $cfg.mode } else { "select" }
    $dim = if ($cfg.dimension) { $cfg.dimension.Replace("'", "''") } else { "" }
    $minVal = if ($cfg.min -ne $null) { [double]$cfg.min } else { 0.0 }
    $maxVal = if ($cfg.max -ne $null) { [double]$cfg.max } else { 0.0 }
    $stepVal = if ($cfg.step -ne $null) { [double]$cfg.step } else { 1.0 }
    $unite = if ($cfg.unit) { $cfg.unit.Replace("'", "''") } else { "" }
    $defMin = if ($cfg.default_min -ne $null) { [double]$cfg.default_min } else { 0.0 }
    $defMax = if ($cfg.default_max -ne $null) { [double]$cfg.default_max } else { 0.0 }
    $tolIndiff = if ($cfg.allow_indifferent) { 1 } else { 0 }
    
    $optsStr = ""
    if ($cfg.options) {
        $optsStr = ($cfg.options -join " | ").Replace("'", "''")
    }

    $sqlIdent = "INSERT INTO [T_QUEST_IDENTITE] " +
                "(N_QUEST, TP_QUEST, MODE_REPONSE, DIMENSION, VAL_MIN, VAL_MAX, PAS_VAL, UNITE, DEFAULT_MIN, DEFAULT_MAX, TOLERANCE_INDIFFERENT, LISTE_OPTIONS) " +
                "VALUES ($nQuest, '$tpQuest', '$mode', '$dim', $minVal, $maxVal, $stepVal, '$unite', $defMin, $defMax, $tolIndiff, '$optsStr')"
    Execute-Sql $sqlIdent

    # 3. Insertion des options individuelles si mode select
    if ($cfg.options) {
        $optIdx = 1
        foreach ($opt in $cfg.options) {
            $safeOpt = $opt.Replace("'", "''")
            $sqlOpt = "INSERT INTO [T_QUEST_IDENTITE_OPT] (N_QUEST, NUM_OPT, LB_OPT) VALUES ($nQuest, $optIdx, '$safeOpt')"
            Execute-Sql $sqlOpt
            $optIdx++
        }
    }

    $count++
}

Write-Host ">>> $count questions de classe 8 insérées avec succès dans T_QUEST et T_QUEST_IDENTITE !"

Write-Host "`n>>> Mise à jour des liaisons miroir (N_QUEST_LIE) entre Type P et Type T..."
foreach ($nQuest in $linkedMap.Keys) {
    $linkedId = $linkedMap[$nQuest]
    Execute-Sql "UPDATE [T_QUEST] SET N_QUEST_LIE = $linkedId WHERE N_QUEST = $nQuest"
}
Write-Host ">>> 32 liaisons Type P <-> Type T mises à jour avec succès !"

Write-Host "`n>>> 7. Vérifications finales..."
$totalQuest = Execute-Scalar "SELECT COUNT(*) FROM [T_QUEST]"
$totalClasse8 = Execute-Scalar "SELECT COUNT(*) FROM [T_QUEST] WHERE N_CLASSE = 8"
$totalIdent = Execute-Scalar "SELECT COUNT(*) FROM [T_QUEST_IDENTITE]"
$totalOpt = Execute-Scalar "SELECT COUNT(*) FROM [T_QUEST_IDENTITE_OPT]"

Write-Host "Total questions dans T_QUEST : $totalQuest (172 initiales + $totalClasse8 classe 8)"
Write-Host "Total dans T_QUEST_IDENTITE : $totalIdent"
Write-Host "Total options dans T_QUEST_IDENTITE_OPT : $totalOpt"

$conn.Close()
Write-Host "`n>>> SUCCÈS : Mise à jour de la base Access Affinity-Full.mdb terminée avec succès !"
