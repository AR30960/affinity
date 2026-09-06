// Helpers pour calcul d'âge et validation de cohérence
function calculateAgeFromBirthDate(birthDateStr) {
  if (!birthDateStr || !String(birthDateStr).trim()) return { age: null, error: null };
  const str = String(birthDateStr).trim();
  let bdate;
  if (str.includes('/')) {
    const parts = str.split('/');
    if (parts.length === 3) {
      bdate = new Date(parseInt(parts[2], 10), parseInt(parts[1], 10) - 1, parseInt(parts[0], 10));
    }
  } else {
    const parts = str.split('-');
    if (parts.length === 3) {
      bdate = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
    }
  }
  if (!bdate || isNaN(bdate.getTime())) return { age: null, error: 'Date invalide.' };
  const today = new Date();
  if (bdate > today) return { age: null, error: '⚠️ La date de naissance ne peut pas être dans le futur.' };
  let age = today.getFullYear() - bdate.getFullYear();
  const m = today.getMonth() - bdate.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < bdate.getDate())) {
    age--;
  }
  if (age < 18) return { age, error: '⚠️ Âge minimum requis : 18 ans pour s\'inscrire.' };
  if (age > 120) return { age, error: '⚠️ Date de naissance incohérente (âge > 120 ans).' };
  return { age, error: null };
}

function updateDateInputAgeFeedback(inputEl, badgeEl, feedbackEl) {
  if (!inputEl) return;
  const res = calculateAgeFromBirthDate(inputEl.value);
  if (!inputEl.value) {
    if (badgeEl) badgeEl.style.display = 'none';
    if (feedbackEl) {
      feedbackEl.style.display = 'none';
      feedbackEl.textContent = '';
    }
    return;
  }
  if (res.error) {
    if (badgeEl) badgeEl.style.display = 'none';
    if (feedbackEl) {
      feedbackEl.style.display = 'block';
      feedbackEl.textContent = res.error;
    }
  } else {
    if (badgeEl) {
      badgeEl.style.display = 'inline-block';
      badgeEl.textContent = `🎂 ${res.age} ans`;
    }
    if (feedbackEl) {
      feedbackEl.style.display = 'none';
      feedbackEl.textContent = '';
    }
  }
}

function setupBirthDateValidation() {
  const ckpBirth = document.getElementById('ckpInputBirth');
  const ckpBadge = document.getElementById('ckpAgeBadge');
  const ckpFeed = document.getElementById('ckpAgeFeedback');
  if (ckpBirth) {
    ckpBirth.addEventListener('input', () => updateDateInputAgeFeedback(ckpBirth, ckpBadge, ckpFeed));
    ckpBirth.addEventListener('change', () => updateDateInputAgeFeedback(ckpBirth, ckpBadge, ckpFeed));
  }

  const idBirth = document.getElementById('idDateNaiss');
  const idBadge = document.getElementById('modalAgeBadge');
  const idFeed = document.getElementById('modalAgeFeedback');
  if (idBirth) {
    idBirth.addEventListener('input', () => updateDateInputAgeFeedback(idBirth, idBadge, idFeed));
    idBirth.addEventListener('change', () => updateDateInputAgeFeedback(idBirth, idBadge, idFeed));
  }
}

// Référentiel des départements français
const FRENCH_DEPARTMENTS_LIST = [
  { code: "01", name: "Ain" }, { code: "02", name: "Aisne" }, { code: "03", name: "Allier" },
  { code: "04", name: "Alpes-de-Haute-Provence" }, { code: "05", name: "Hautes-Alpes" },
  { code: "06", name: "Alpes-Maritimes" }, { code: "07", name: "Ardèche" }, { code: "08", name: "Ardennes" },
  { code: "09", name: "Ariège" }, { code: "10", name: "Aube" }, { code: "11", name: "Aude" },
  { code: "12", name: "Aveyron" }, { code: "13", name: "Bouches-du-Rhône" }, { code: "14", name: "Calvados" },
  { code: "15", name: "Cantal" }, { code: "16", name: "Charente" }, { code: "17", name: "Charente-Maritime" },
  { code: "18", name: "Cher" }, { code: "19", name: "Corrèze" }, { code: "2A", name: "Corse-du-Sud" },
  { code: "2B", name: "Haute-Corse" }, { code: "21", name: "Côte-d'Or" }, { code: "22", name: "Côtes-d'Armor" },
  { code: "23", name: "Creuse" }, { code: "24", name: "Dordogne" }, { code: "25", name: "Doubs" },
  { code: "26", name: "Drôme" }, { code: "27", name: "Eure" }, { code: "28", name: "Eure-et-Loir" },
  { code: "29", name: "Finistère" }, { code: "30", name: "Gard" }, { code: "31", name: "Haute-Garonne" },
  { code: "32", name: "Gers" }, { code: "33", name: "Gironde" }, { code: "34", name: "Hérault" },
  { code: "35", name: "Ille-et-Vilaine" }, { code: "36", name: "Indre" }, { code: "37", name: "Indre-et-Loire" },
  { code: "38", name: "Isère" }, { code: "39", name: "Jura" }, { code: "40", name: "Landes" },
  { code: "41", name: "Loir-et-Cher" }, { code: "42", name: "Loire" }, { code: "43", name: "Haute-Loire" },
  { code: "44", name: "Loire-Atlantique" }, { code: "45", name: "Loiret" }, { code: "46", name: "Lot" },
  { code: "47", name: "Lot-et-Garonne" }, { code: "48", name: "Lozère" }, { code: "49", name: "Maine-et-Loire" },
  { code: "50", name: "Manche" }, { code: "51", name: "Marne" }, { code: "52", name: "Haute-Marne" },
  { code: "53", name: "Mayenne" }, { code: "54", name: "Meurthe-et-Moselle" }, { code: "55", name: "Meuse" },
  { code: "56", name: "Morbihan" }, { code: "57", name: "Moselle" }, { code: "58", name: "Nièvre" },
  { code: "59", name: "Nord" }, { code: "60", name: "Oise" }, { code: "61", name: "Orne" },
  { code: "62", name: "Pas-de-Calais" }, { code: "63", name: "Puy-de-Dôme" }, { code: "64", name: "Pyrénées-Atlantiques" },
  { code: "65", name: "Hautes-Pyrénées" }, { code: "66", name: "Pyrénées-Orientales" }, { code: "67", name: "Bas-Rhin" },
  { code: "68", name: "Haut-Rhin" }, { code: "69", name: "Rhône" }, { code: "70", name: "Haute-Saône" },
  { code: "71", name: "Saône-et-Loire" }, { code: "72", name: "Sarthe" }, { code: "73", name: "Savoie" },
  { code: "74", name: "Haute-Savoie" }, { code: "75", name: "Paris" }, { code: "76", name: "Seine-Maritime" },
  { code: "77", name: "Seine-et-Marne" }, { code: "78", name: "Yvelines" }, { code: "79", name: "Deux-Sèvres" },
  { code: "80", name: "Somme" }, { code: "81", name: "Tarn" }, { code: "82", name: "Tarn-et-Garonne" },
  { code: "83", name: "Var" }, { code: "84", name: "Vaucluse" }, { code: "85", name: "Vendée" },
  { code: "86", name: "Vienne" }, { code: "87", name: "Haute-Vienne" }, { code: "88", name: "Vosges" },
  { code: "89", name: "Yonne" }, { code: "90", name: "Territoire de Belfort" }, { code: "91", name: "Essonne" },
  { code: "92", name: "Hauts-de-Seine" }, { code: "93", name: "Seine-Saint-Denis" }, { code: "94", name: "Val-de-Marne" },
  { code: "95", name: "Val-d'Oise" }, { code: "971", name: "Guadeloupe" }, { code: "972", name: "Martinique" },
  { code: "973", name: "Guyane" }, { code: "974", name: "La Réunion" }, { code: "976", name: "Mayotte" }
];

const FRENCH_CITIES_MAP = {
  "paris": "75", "marseille": "13", "lyon": "69", "toulouse": "31", "nice": "06",
  "nantes": "44", "montpellier": "34", "strasbourg": "67", "bordeaux": "33", "lille": "59",
  "rennes": "35", "reims": "51", "toulon": "83", "saint-etienne": "42", "le havre": "76",
  "grenoble": "38", "dijon": "21", "angers": "49", "nimes": "30", "villeurbanne": "69",
  "clermont-ferrand": "63", "le mans": "72", "aix-en-provence": "13", "brest": "29", "tours": "37",
  "amiens": "80", "limoges": "87", "annecy": "74", "perpignan": "66", "boulogne-billancourt": "92",
  "metz": "57", "besancon": "25", "orleans": "45", "saint-denis": "93", "argenteuil": "95",
  "rouen": "76", "montreuil": "93", "mulhouse": "68", "caen": "14", "nancy": "54",
  "tourcoing": "59", "roubaix": "59", "nanterre": "92", "vitry-sur-seine": "94", "creteil": "94",
  "avignon": "84", "poitiers": "86", "courbevoie": "92", "versailles": "78", "colombes": "92",
  "asnieres-sur-seine": "92", "aulnay-sous-bois": "93", "saint-maur-des-fosses": "94", "rueil-malmaison": "92",
  "champigny-sur-marne": "94", "aubervilliers": "93", "antibes": "06", "la rochelle": "17", "cannes": "06",
  "calais": "62", "saint-nazaire": "44", "colmar": "68", "dunkerque": "59", "bourges": "18",
  "valence": "26", "quimper": "29", "ajaccio": "2A", "bastia": "2B", "cayenne": "973",
  "fort-de-france": "972", "saint-denis-de-la-reunion": "974", "mamoudzou": "976",
  "neuilly-sur-seine": "92", "levallois-perret": "92", "issy-les-moulineaux": "92", "antony": "92",
  "clichy": "92", "pantin": "93", "bobigny": "93", "bondy": "93", "fontenay-sous-bois": "94",
  "ivry-sur-seine": "94", "villejuif": "94", "maisons-alfort": "94", "cergy": "95", "sarcelles": "95",
  "evry": "91", "corbeil-essonnes": "91", "massy": "91", "meaux": "77", "cheles": "77", "melun": "77",
  "pau": "64", "bayonne": "64", "tarbes": "65", "montauban": "82", "albi": "81", "rodez": "12",
  "carcassonne": "11", "narbonne": "11", "beziers": "34", "sete": "34", "arles": "13",
  "hyeres": "83", "frejus": "83", "grasse": "06", "cagnes-sur-mer": "06", "gap": "05", "digne-les-bains": "04",
  "chambery": "73", "vienne": "38", "roanne": "42", "bourg-en-bresse": "01",
  "auxerre": "89", "nevers": "58", "macon": "71", "chalon-sur-saone": "71", "belfort": "90",
  "vesoul": "70", "lons-le-saunier": "39", "dole": "39", "epinal": "88", "thionville": "57",
  "bar-le-duc": "55", "verdun": "55", "charleville-mezieres": "08", "troyes": "10", "chalons-en-champagne": "51",
  "chaumont": "52", "beauvais": "60", "compiegne": "60", "creil": "60", "laon": "02", "saint-quentin": "02",
  "soissons": "02", "arras": "62", "boulogne-sur-mer": "62", "lens": "62", "douai": "59", "valenciennes": "59",
  "evreux": "27", "dieppe": "76", "cherbourg": "50", "saint-lo": "50", "alencon": "61",
  "chartres": "28", "dreux": "28", "blois": "41", "chateauroux": "36",
  "saint-brieuc": "22", "lorient": "56", "vannes": "56", "saint-malo": "35", "laval": "53",
  "cholet": "49", "la roche-sur-yon": "85", "niort": "79", "angouleme": "16", "saintes": "17",
  "chatellerault": "86", "gueret": "23", "tulle": "19", "brive-la-gaillarde": "19", "perigueux": "24",
  "bergerac": "24", "agen": "47", "villeneuve-sur-lot": "47", "mont-de-marsan": "40", "dax": "40", "auch": "32"
};

function stripAccents(str) {
  if (!str) return '';
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

function checkHabiteCommuneCoherence() {
  const paysEl = document.getElementById('ckpHabitePays');
  const selDeptEl = document.getElementById('ckpHabiteRegionSelect');
  const communeEl = document.getElementById('ckpHabiteCommune');
  const feedbackEl = document.getElementById('ckpCommuneFeedback');

  if (!feedbackEl) return;

  const pays = paysEl ? paysEl.value : 'France';
  if (pays !== 'France') {
    feedbackEl.style.display = 'none';
    feedbackEl.textContent = '';
    return;
  }

  const deptVal = selDeptEl ? selDeptEl.value : '';
  const communeVal = communeEl ? communeEl.value.trim() : '';

  if (!deptVal || !communeVal) {
    feedbackEl.style.display = 'none';
    feedbackEl.textContent = '';
    return;
  }

  const deptCodeMatch = deptVal.match(/^(\d{2,3}|2A|2B)/i);
  const deptCode = deptCodeMatch ? deptCodeMatch[1].toUpperCase() : '';

  // 1. Code postal dans la commune
  const cpMatch = communeVal.match(/\b(\d{5})\b/);
  if (cpMatch) {
    const cp = cpMatch[1];
    const cpDept = (cp.startsWith('97') || cp.startsWith('98')) ? cp.substring(0, 3) : cp.substring(0, 2);
    if (cpDept.startsWith('20')) {
      if (deptCode !== '2A' && deptCode !== '2B') {
        feedbackEl.style.display = 'block';
        feedbackEl.className = 'ckp-commune-feedback warning';
        feedbackEl.textContent = `⚠️ Incohérence : le code postal ${cp} correspond à la Corse (2A/2B), or vous avez sélectionné ${deptVal}.`;
        return;
      }
    } else if (cpDept !== deptCode) {
      const targetDept = FRENCH_DEPARTMENTS_LIST.find(d => d.code === cpDept);
      const targetName = targetDept ? `${targetDept.code} - ${targetDept.name}` : cpDept;
      feedbackEl.style.display = 'block';
      feedbackEl.className = 'ckp-commune-feedback warning';
      feedbackEl.textContent = `⚠️ Incohérence : le code postal ${cp} correspond au département ${targetName}, or vous avez sélectionné ${deptVal}.`;
      return;
    }
  }

  // 2. Ville connue dans le dictionnaire
  const cleanCommune = stripAccents(communeVal);
  for (const [cityName, cityDept] of Object.entries(FRENCH_CITIES_MAP)) {
    if (cleanCommune === cityName || cleanCommune.startsWith(cityName + " ") || cleanCommune.endsWith(" " + cityName)) {
      if (cityDept !== deptCode) {
        const realDept = FRENCH_DEPARTMENTS_LIST.find(d => d.code === cityDept);
        const realName = realDept ? `${realDept.code} - ${realDept.name}` : cityDept;
        feedbackEl.style.display = 'block';
        feedbackEl.className = 'ckp-commune-feedback warning';
        feedbackEl.textContent = `⚠️ Incohérence : la commune '${communeVal}' est rattachée au département ${realName}, or vous avez sélectionné ${deptVal}.`;
        return;
      } else {
        feedbackEl.style.display = 'block';
        feedbackEl.className = 'ckp-commune-feedback success';
        feedbackEl.textContent = `✓ Commune cohérente avec le département ${deptVal}.`;
        return;
      }
    }
  }

  feedbackEl.style.display = 'block';
  feedbackEl.className = 'ckp-commune-feedback success';
  feedbackEl.textContent = `✓ Commune enregistrée pour le département ${deptVal}.`;
}

function checkProfileCompleteness() {
  const banner = document.getElementById('ckpCompletenessStatus');
  const titleEl = document.getElementById('ckpStatusTitle');
  const descEl = document.getElementById('ckpMissingFieldsDesc');
  const iconEl = document.getElementById('ckpStatusIcon');
  const tooltipWrap = document.getElementById('ckpTooltipContainer');
  const fullNameEl = document.getElementById('myProfileFullName');

  if (!banner) return;

  const pseudo = document.getElementById('ckpInputPseudo')?.value.trim();
  const prenom = document.getElementById('ckpInputPrenom')?.value.trim();
  const nom = document.getElementById('ckpInputNom')?.value.trim();
  const sexeVal = document.getElementById('ckpSelectSexe')?.value;
  const sexe = (sexeVal === '1' || sexeVal === '2');
  const birth = document.getElementById('ckpInputBirth')?.value.trim();
  const habPays = document.getElementById('ckpHabitePays')?.value.trim();
  const habDept = (document.getElementById('ckpHabiteRegionSelect')?.value.trim() || document.getElementById('ckpHabiteRegionText')?.value.trim() || document.getElementById('ckpHabiteRegion')?.value.trim());
  const habCommune = document.getElementById('ckpHabiteCommune')?.value.trim();
  const rechercheDe = document.getElementById('ckpSelectRecherche')?.value.trim();
  const bio = document.getElementById('ckpInputBio')?.value.trim();

  // Mise à jour en direct du nom complet affiché dans l'en-tête du cockpit
  if (fullNameEl) {
    const computedName = `${prenom || ''} ${nom || ''}`.trim();
    fullNameEl.textContent = computedName || 'Non renseigné';
  }

  const missing = [];
  if (!pseudo) missing.push("Pseudo");
  if (!prenom) missing.push("Prénom");
  if (!nom) missing.push("Nom");
  if (!sexe) missing.push("Sexe");
  if (!birth) missing.push("Date de naissance");
  if (!habPays || !habDept || !habCommune) {
    const sub = [];
    if (!habPays) sub.push("Pays");
    if (!habDept) sub.push("Département");
    if (!habCommune) sub.push("Commune");
    missing.push(`J'habite ici (${sub.join(', ')})`);
  }
  if (!rechercheDe) missing.push("À la recherche de");
  if (!bio) missing.push("Présentation");

  // Condition stricte : 100% dans "+ sur vous" ET 100% dans "+ sur l'autre" (Classe 0 - Identité)
  const curProf = getActiveProfile();
  let identityComplete = true;
  const selfPct = state.selfCompletionPct ?? 0;
  const partnerPct = state.partnerCompletionPct ?? 0;

  if (curProf && curProf.role !== 'admin') {
    if (selfPct < 100 || partnerPct < 100) {
      identityComplete = false;
    }
  }

  if (missing.length === 0 && identityComplete) {
    banner.className = 'ckp-completeness-status complete';
    if (iconEl) iconEl.textContent = '✅';
    if (titleEl) titleEl.textContent = 'Profil complété';
    if (descEl) {
      descEl.textContent = '';
      descEl.style.display = 'none'; // Pas de texte superflu sous Profil complété
    }
    if (tooltipWrap) tooltipWrap.style.display = 'none';
  } else {
    banner.className = 'ckp-completeness-status incomplete';
    if (iconEl) iconEl.textContent = '⚠️';
    if (titleEl) titleEl.textContent = 'Profil à compléter';
    if (tooltipWrap) tooltipWrap.style.display = 'inline-flex';
    if (descEl) {
      descEl.style.display = 'block';
      const reasons = [];
      if (missing.length > 0) reasons.push(`Champs obligatoires manquants : ${missing.join(', ')}`);
      if (selfPct < 100) reasons.push(`Questionnaire "+ sur vous" incomplet (${selfPct}%)`);
      if (partnerPct < 100) reasons.push(`Questionnaire "+ sur l'autre" incomplet (${partnerPct}%)`);
      descEl.textContent = reasons.join(' - ');
    }
  }
}

function onHabitePaysChange() {
  const paysEl = document.getElementById('ckpHabitePays');
  const selDeptEl = document.getElementById('ckpHabiteRegionSelect');
  const txtDeptEl = document.getElementById('ckpHabiteRegionText');
  const hiddenDeptEl = document.getElementById('ckpHabiteRegion');

  if (!paysEl) return;
  const isFrance = paysEl.value === 'France';

  if (selDeptEl && txtDeptEl) {
    if (isFrance) {
      selDeptEl.style.display = 'block';
      txtDeptEl.style.display = 'none';
      if (hiddenDeptEl) hiddenDeptEl.value = selDeptEl.value;
    } else {
      selDeptEl.style.display = 'none';
      txtDeptEl.style.display = 'block';
      if (hiddenDeptEl) hiddenDeptEl.value = txtDeptEl.value;
    }
  }
  checkHabiteCommuneCoherence();
  checkProfileCompleteness();
}

function setupGeographicAndCompletenessListeners() {
  const paysEl = document.getElementById('ckpHabitePays');
  const selDeptEl = document.getElementById('ckpHabiteRegionSelect');
  const txtDeptEl = document.getElementById('ckpHabiteRegionText');
  const hiddenDeptEl = document.getElementById('ckpHabiteRegion');
  const communeEl = document.getElementById('ckpHabiteCommune');

  if (paysEl) paysEl.addEventListener('change', onHabitePaysChange);

  if (selDeptEl) {
    selDeptEl.addEventListener('change', () => {
      if (hiddenDeptEl) hiddenDeptEl.value = selDeptEl.value;
      checkHabiteCommuneCoherence();
      checkProfileCompleteness();
    });
  }

  if (txtDeptEl) {
    txtDeptEl.addEventListener('input', () => {
      if (hiddenDeptEl) hiddenDeptEl.value = txtDeptEl.value;
      checkProfileCompleteness();
    });
  }

  if (communeEl) {
    communeEl.addEventListener('input', () => {
      checkHabiteCommuneCoherence();
      checkProfileCompleteness();
    });
    communeEl.addEventListener('change', () => {
      checkHabiteCommuneCoherence();
      checkProfileCompleteness();
    });
  }

  const reqIds = ['ckpInputPseudo', 'ckpInputPrenom', 'ckpInputNom', 'ckpSelectSexe', 'ckpInputBirth', 'ckpSelectSituationFamille', 'ckpSelectRecherche', 'ckpInputBio'];
  reqIds.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', checkProfileCompleteness);
      el.addEventListener('change', checkProfileCompleteness);
    }
  });
}

// ==========================================================================
// MODULE IDENTITÉ & CARACTÉRISTIQUES (CLASSE 0 : + SUR VOUS & + SUR L'AUTRE)
// ==========================================================================

async function loadIdentityAnswers(profileId) {
  if (!profileId) return;
  try {
    const res = await fetch(`${API_BASE}/api/profiles/${profileId}/identity-answers`);
    if (!res.ok) return;
    const data = await res.json();
    state.identityQuestionsSelf = data.questions_self || data.questions || [];
    state.identityQuestionsPartner = data.questions_partner || data.questions || [];
    state.identityQuestions = state.identityQuestionsSelf;
    state.identityAnswersSelf = data.self || {};
    state.identityAnswersPartner = data.partner || {};
    state.selfCompletionPct = data.self_completion_pct || 0;
    state.partnerCompletionPct = data.partner_completion_pct || 0;

    updateIdentityCompletionBadge();
  } catch (err) {
    console.error("Erreur chargement identité :", err);
  }
}

function updateIdentityCompletionBadge() {
  const badgeTopSelf = document.getElementById('ckpIdentityCompletionTop');
  const badgeTopPartner = document.getElementById('ckpPartnerCompletionTop');
  const deckBadgeSelf = document.getElementById('deckBadgeSelf');
  const deckBadgePartner = document.getElementById('deckBadgePartner');

  const sPct = state.selfCompletionPct ?? 0;
  const pPct = state.partnerCompletionPct ?? 0;

  if (badgeTopSelf) badgeTopSelf.textContent = `${sPct}%`;
  if (badgeTopPartner) badgeTopPartner.textContent = `${pPct}%`;
  if (deckBadgeSelf) deckBadgeSelf.textContent = `${sPct}%`;
  if (deckBadgePartner) deckBadgePartner.textContent = `${pPct}%`;

  // Synchronisation bannière de complétude de la fiche
  checkProfileCompleteness();
}

async function openIdentityDeck(mode = 'self', targetProfileId = null) {
  const curProf = getActiveProfile();
  const ckpVal = document.getElementById('ckpProfileId')?.value;
  const ckpId = ckpVal ? Number(ckpVal) : null;
  const profId = targetProfileId || (ckpId && !isNaN(ckpId) ? ckpId : null) || (curProf ? curProf.id : state.activeProfileId) || 1;

  state.identityDeckMode = mode || 'self';
  const modal = document.getElementById('modalIdentityDeck');
  if (!modal) {
    console.error("modalIdentityDeck introuvable dans le DOM");
    return;
  }

  // Fermer les autres modales pour éviter les chevauchements
  closeModals();
  modal.style.display = 'flex';

  // Affichage d'un état de chargement propre si les questions ne sont pas encore prêtes
  const container = document.getElementById('identityDeckQuestionsContainer');
  if (container && (!state.identityQuestionsSelf || state.identityQuestionsSelf.length === 0)) {
    container.innerHTML = `
      <div style="text-align:center; padding:40px 20px; color:var(--text-dim);">
        <div style="font-size:28px; margin-bottom:10px;">⏳</div>
        <p>Chargement des caractéristiques personnelles...</p>
      </div>
    `;
  }

  // Rechargement systématique pour avoir l'état frais du profil actif
  await loadIdentityAnswers(profId);

  switchIdentityDeckTab(state.identityDeckMode);
}

function switchIdentityDeckTab(mode) {
  state.identityDeckMode = mode;
  const btnSelf = document.getElementById('btnTabIdentitySelf');
  const btnPartner = document.getElementById('btnTabIdentityPartner');
  const titleEl = document.getElementById('identityDeckTitle');
  const bannerEl = document.getElementById('deckIntroBanner');

  if (btnSelf) btnSelf.classList.toggle('active', mode === 'self');
  if (btnPartner) btnPartner.classList.toggle('active', mode === 'partner');

  if (mode === 'self') {
    if (titleEl) titleEl.innerHTML = `💎 Vos Caractéristiques Personnelles &bull; <em>+ sur moi</em>`;
    if (bannerEl) bannerEl.innerHTML = `<span>👤</span> Renseignez votre valeur exacte ou sélectionnez l'option qui vous correspond le mieux pour chaque caractéristique.`;
  } else {
    if (titleEl) titleEl.innerHTML = `💎 Critères & Tolérances chez l'Autre &bull; <em>+ sur l'autre</em>`;
    if (bannerEl) bannerEl.innerHTML = `<span>👥</span> Définissez vos tolérances chez l'autre (plage Min/Max ou options cochées). Cochez <strong>« Indifférent »</strong> si ce critère n'a pas d'importance pour vous.`;
  }

  renderIdentityDeckQuestions();
}

function renderIdentityDeckQuestions() {
  const container = document.getElementById('identityDeckQuestionsContainer');
  const summaryEl = document.getElementById('deckFooterSummary');
  if (!container) return;

  const mode = state.identityDeckMode || 'self';
  const questions = (mode === 'self')
    ? (state.identityQuestionsSelf && state.identityQuestionsSelf.length > 0 ? state.identityQuestionsSelf : state.identityQuestions)
    : (state.identityQuestionsPartner && state.identityQuestionsPartner.length > 0 ? state.identityQuestionsPartner : state.identityQuestions);

  if (!Array.isArray(questions) || questions.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:40px 20px; color:var(--text-dim);">
        <div style="font-size:24px; margin-bottom:8px;">💎</div>
        <p>Chargement des caractéristiques d'identité en cours...</p>
      </div>
    `;
    if (summaryEl) summaryEl.textContent = '0 / 0 question renseignée';
    return;
  }

  const selfAns = state.identityAnswersSelf || {};
  const partnerAns = state.identityAnswersPartner || {};

  let answeredCount = 0;

  container.innerHTML = questions.map((q, idx) => {
    const qid = q.id;
    const isNumeric = q.kind === 'numeric';

    if (mode === 'self') {
      const a = selfAns[qid] || selfAns[String(qid)] || {};
      const hasAnswer = (a.valeur_num !== null && a.valeur_num !== undefined) || (a.valeur_text && a.valeur_text.trim().length > 0);
      if (hasAnswer) answeredCount++;

      let inputHtml = '';
      const minVal = (q.min !== undefined && q.min !== null) ? q.min : 0;
      const maxVal = (q.max !== undefined && q.max !== null) ? q.max : 100;
      const stepVal = q.step || 1;
      const unitVal = q.unit || '';
      const optsList = Array.isArray(q.options) ? q.options : [];

      if (isNumeric) {
        inputHtml = `
          <div class="id-numeric-input-group">
            <input type="number" class="id-numeric-input" id="self_q_${qid}" 
                   value="${a.valeur_num ?? ''}" min="${minVal}" max="${maxVal}" step="${stepVal}"
                   placeholder="${minVal}-${maxVal}"
                   onchange="handleSelfAnswerChange(${qid}, 'numeric')">
            <span class="id-numeric-unit">${unitVal}</span>
          </div>
        `;
      } else {
        const opts = optsList.map(opt => {
          const sel = (a.valeur_text === opt) ? 'selected' : '';
          return `<option value="${opt}" ${sel}>${opt}</option>`;
        }).join('');
        inputHtml = `
          <select class="id-select-input" id="self_q_${qid}" onchange="handleSelfAnswerChange(${qid}, 'select')">
            <option value="">-- Sélectionner une option --</option>
            ${opts}
          </select>
        `;
      }

      return `
        <div class="id-deck-card" id="card_id_q_${qid}">
          <div class="id-deck-card-header">
            <div class="id-card-title-wrap">
              <span class="id-card-badge-num">#${idx + 1}</span>
              <span class="id-card-theme-tag">${q.thematique} &bull; ${q.sujet}</span>
              <span class="badge-tag type" style="background:rgba(56,189,248,0.15); border-color:#38bdf8; color:#7dd3fc; font-size:10px;">Type P &bull; Précis</span>
            </div>
            <span class="id-card-status-badge ${hasAnswer ? 'answered' : 'empty'}">
              ${hasAnswer ? '✓ Renseigné' : 'À renseigner'}
            </span>
          </div>
          <div class="id-card-question-text">${q.texte}</div>
          <div class="id-answer-self-wrap">
            ${inputHtml}
          </div>
        </div>
      `;
    } else {
      // Mode partner (Type T - Tolérance)
      const p = partnerAns[qid] || partnerAns[String(qid)] || {};
      const isIndifferent = !!p.indifferent;
      const optsAllowed = Array.isArray(p.options) ? p.options : [];
      const hasAnswer = isIndifferent || (isNumeric ? (p.min_val !== null && p.max_val !== null) : optsAllowed.length > 0);
      if (hasAnswer) answeredCount++;

      let contentHtml = '';
      const minBound = (q.min !== undefined && q.min !== null) ? q.min : 0;
      const maxBound = (q.max !== undefined && q.max !== null) ? q.max : 100;
      const stepVal = q.step || 1;
      const unitVal = q.unit || '';
      const optsList = Array.isArray(q.options) ? q.options : [];

      if (isNumeric) {
        const curMinVal = (p.min_val !== null && p.min_val !== undefined) ? p.min_val : minBound;
        const curMaxVal = (p.max_val !== null && p.max_val !== undefined) ? p.max_val : maxBound;

        contentHtml = `
          <div class="id-range-inputs-row ${isIndifferent ? 'is-disabled' : ''}" id="partner_bounds_${qid}">
            <span style="font-size:12px; font-weight:600; color:#cbd5e1;">Tolérance :</span>
            <div class="id-range-bound">
              <span style="font-size:12.5px; color:#a855f7; font-weight:700;">de</span>
              <div class="id-numeric-input-group">
                <input type="number" class="id-numeric-input" id="partner_min_${qid}"
                       value="${curMinVal}" min="${minBound}" max="${maxBound}" step="${stepVal}"
                       onchange="handlePartnerRangeChange(${qid})">
              </div>
            </div>
            <div class="id-range-bound">
              <span style="font-size:12.5px; color:#a855f7; font-weight:700;">à</span>
              <div class="id-numeric-input-group">
                <input type="number" class="id-numeric-input" id="partner_max_${qid}"
                       value="${curMaxVal}" min="${minBound}" max="${maxBound}" step="${stepVal}"
                       onchange="handlePartnerRangeChange(${qid})">
                <span class="id-numeric-unit">${unitVal}</span>
              </div>
            </div>
          </div>
        `;
      } else {
        const checkboxes = optsList.map(opt => {
          const checked = (!isIndifferent && optsAllowed.includes(opt)) ? 'checked' : '';
          return `
            <label class="id-checkbox-pill ${checked}">
              <input type="checkbox" value="${opt}" ${checked}
                     onchange="handlePartnerCheckChange(${qid}, this)">
              <span>${opt}</span>
            </label>
          `;
        }).join('');

        contentHtml = `
          <div class="id-checkboxes-grid ${isIndifferent ? 'is-disabled' : ''}" id="partner_checks_${qid}">
            ${checkboxes}
          </div>
        `;
      }

      return `
        <div class="id-deck-card" id="card_partner_q_${qid}">
          <div class="id-deck-card-header">
            <div class="id-card-title-wrap">
              <span class="id-card-badge-num">#${idx + 1}</span>
              <span class="id-card-theme-tag">${q.thematique} &bull; ${q.sujet}</span>
              <span class="badge-tag type" style="background:rgba(168,85,247,0.18); border-color:#a855f7; color:#f3e8ff; font-size:10px;">Type T &bull; Tolérance</span>
            </div>
            <span class="id-card-status-badge ${hasAnswer ? 'answered' : 'empty'}">
              ${hasAnswer ? (isIndifferent ? '✓ Indifférent' : '✓ Tolérances définies') : 'Non défini'}
            </span>
          </div>
          <div class="id-card-question-text">${q.texte}</div>
          <div class="id-partner-wrap">
            <div class="id-indifferent-row">
              <input type="checkbox" id="indiff_${qid}" ${isIndifferent ? 'checked' : ''} 
                     onchange="handlePartnerIndifferentToggle(${qid})">
              <label for="indiff_${qid}" class="id-indifferent-label">Indifférent (Toutes options / valeurs tolérées)</label>
            </div>
            ${contentHtml}
          </div>
        </div>
      `;
    }
  }).join('');

  if (summaryEl) {
    const total = questions.length;
    const pct = total > 0 ? Math.round((answeredCount / total) * 100) : 0;
    summaryEl.innerHTML = `<strong>${answeredCount} / ${total}</strong> questions renseignées (${pct}%) dans cet onglet`;
  }
}

async function handleSelfAnswerChange(qid, kind) {
  const curProf = getActiveProfile();
  if (!curProf) return;

  let valNum = null;
  let valText = null;

  if (kind === 'numeric') {
    const inp = document.getElementById(`self_q_${qid}`);
    if (inp && inp.value !== '') {
      valNum = parseFloat(inp.value);
    }
  } else {
    const sel = document.getElementById(`self_q_${qid}`);
    if (sel && sel.value) {
      valText = sel.value;
    }
  }

  try {
    const res = await fetch(`${API_BASE}/api/profiles/${curProf.id}/identity-answers/self`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_id: qid, valeur_num: valNum, valeur_text: valText })
    });
    const data = await res.json();
    if (data.ok) {
      if (!state.identityAnswersSelf) state.identityAnswersSelf = {};
      state.identityAnswersSelf[qid] = { valeur_num: valNum, valeur_text: valText };
      state.selfCompletionPct = data.self_completion_pct;
      updateIdentityCompletionBadge();

      // Mise à jour badge de la carte
      const card = document.getElementById(`card_id_q_${qid}`);
      if (card) {
        const hasAnswer = (valNum !== null) || (valText && valText.trim().length > 0);
        const badge = card.querySelector('.id-card-status-badge');
        if (badge) {
          badge.className = `id-card-status-badge ${hasAnswer ? 'answered' : 'empty'}`;
          badge.textContent = hasAnswer ? '✓ Renseigné' : 'À renseigner';
        }
      }
      showToast('Enregistré');
    }
  } catch (err) {
    console.error('Erreur sauvegarde réponse self :', err);
  }
}

async function handlePartnerIndifferentToggle(qid) {
  const curProf = getActiveProfile();
  if (!curProf) return;

  const cb = document.getElementById(`indiff_${qid}`);
  const isIndiff = cb ? cb.checked : false;

  const q = (state.identityQuestions || []).find(item => item.id === qid);
  let minVal = null;
  let maxVal = null;
  let options = [];

  if (q && q.kind === 'numeric') {
    const minInp = document.getElementById(`partner_min_${qid}`);
    const maxInp = document.getElementById(`partner_max_${qid}`);
    minVal = minInp ? parseFloat(minInp.value) : q.min;
    maxVal = maxInp ? parseFloat(maxInp.value) : q.max;

    const boundsRow = document.getElementById(`partner_bounds_${qid}`);
    if (boundsRow) boundsRow.classList.toggle('is-disabled', isIndiff);
  } else if (q) {
    const checksContainer = document.getElementById(`partner_checks_${qid}`);
    if (checksContainer) {
      checksContainer.classList.toggle('is-disabled', isIndiff);
      const checkedBoxes = checksContainer.querySelectorAll('input[type="checkbox"]:checked');
      options = Array.from(checkedBoxes).map(b => b.value);
    }
  }

  await savePartnerAnswer(qid, minVal, maxVal, options, isIndiff);
}

async function handlePartnerRangeChange(qid) {
  const minInp = document.getElementById(`partner_min_${qid}`);
  const maxInp = document.getElementById(`partner_max_${qid}`);
  let minVal = minInp && minInp.value !== '' ? parseFloat(minInp.value) : null;
  let maxVal = maxInp && maxInp.value !== '' ? parseFloat(maxInp.value) : null;

  await savePartnerAnswer(qid, minVal, maxVal, [], false);
}

async function handlePartnerCheckChange(qid, checkboxEl) {
  if (checkboxEl && checkboxEl.parentElement) {
    checkboxEl.parentElement.classList.toggle('checked', checkboxEl.checked);
  }

  const checksContainer = document.getElementById(`partner_checks_${qid}`);
  let options = [];
  if (checksContainer) {
    const checkedBoxes = checksContainer.querySelectorAll('input[type="checkbox"]:checked');
    options = Array.from(checkedBoxes).map(b => b.value);
  }

  await savePartnerAnswer(qid, null, null, options, false);
}

async function savePartnerAnswer(qid, minVal, maxVal, options, indifferent) {
  const curProf = getActiveProfile();
  if (!curProf) return;

  try {
    const res = await fetch(`${API_BASE}/api/profiles/${curProf.id}/identity-answers/partner`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_id: qid, min_val: minVal, max_val: maxVal, options: options, indifferent: indifferent })
    });
    const data = await res.json();
    if (data.ok) {
      if (!state.identityAnswersPartner) state.identityAnswersPartner = {};
      state.identityAnswersPartner[qid] = { min_val: minVal, max_val: maxVal, options: options, indifferent: indifferent };
      state.partnerCompletionPct = data.partner_completion_pct;
      updateIdentityCompletionBadge();

      // Mise à jour badge de la carte
      const card = document.getElementById(`card_partner_q_${qid}`);
      if (card) {
        const hasAnswer = indifferent || (minVal !== null && maxVal !== null) || (options && options.length > 0);
        const badge = card.querySelector('.id-card-status-badge');
        if (badge) {
          badge.className = `id-card-status-badge ${hasAnswer ? 'answered' : 'empty'}`;
          badge.textContent = hasAnswer ? (indifferent ? '✓ Indifférent' : '✓ Tolérances définies') : 'Non défini';
        }
      }
      showToast('Tolérances enregistrées');
    }
  } catch (err) {
    console.error('Erreur sauvegarde réponse partner :', err);
  }
}

// AFFINITY - Client Web/Desktop

const API_BASE = (window.location.origin && window.location.origin.startsWith('http'))
  ? window.location.origin 
  : 'http://localhost:8765';

// Intercepteur global pour ajouter le token d'authentification à toutes les requêtes API
const originalFetch = window.fetch;
window.fetch = function(url, options = {}) {
  const token = localStorage.getItem('affinity_token');
  if (token && typeof url === 'string' && url.includes('/api/')) {
    options = options || {};
    options.headers = options.headers || {};
    if (options.headers instanceof Headers) {
      if (!options.headers.has('Authorization')) {
        options.headers.set('Authorization', `Bearer ${token}`);
      }
    } else if (Array.isArray(options.headers)) {
      options.headers.push(['Authorization', `Bearer ${token}`]);
    } else {
      if (!options.headers['Authorization']) {
        options.headers['Authorization'] = `Bearer ${token}`;
      }
    }
  }
  return originalFetch(url, options);
};

function getAuthToken() {
  return localStorage.getItem('affinity_token');
}

function setAuthToken(token) {
  if (token) localStorage.setItem('affinity_token', token);
  else localStorage.removeItem('affinity_token');
}

function removeAuthToken() {
  localStorage.removeItem('affinity_token');
}

let state = {
  profiles: [],
  activeProfileId: null,
  realAdminId: null, // ID du profil administrateur connecté
  simulatedRole: null, // Mode test administrateur : null, 'subscriber', 'guest'
  simulatedProfileId: null, // ID du profil incarné lors du test
  currentUser: null,
  currentCatalog: [],
  questions: [],
  pendingQuestions: [],
  packs: [],
  answersMap: {}, // key: "qid_axis" -> value
  identityDeckMode: 'self', // 'self' ou 'partner'
  identityQuestions: [],
  identityAnswersSelf: {},
  identityAnswersPartner: {},
  selfCompletionPct: 0,
  partnerCompletionPct: 0,
  stats: {},
  lastAffinityResult: null
};

// Initialisation au chargement du DOM
document.addEventListener('DOMContentLoaded', () => {
  initEventListeners();
  loadInitialData();
  startLiveClock();
});

function initEventListeners() {
  setupBirthDateValidation();
  setupGeographicAndCompletenessListeners();
  setupAuthListeners();
  // Navigation par onglets
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabName = btn.getAttribute('data-tab');
      switchTab(tabName);
    });
  });

  // Boutons rapides du Header
  document.getElementById('btnNewProfileModal').addEventListener('click', () => openCreateProfileModal());
  document.getElementById('btnOpenAddProfile').addEventListener('click', () => openCreateProfileModal());
  document.getElementById('btnQuickMatch').addEventListener('click', () => {
    switchTab('affinity');
  });
  document.getElementById('btnSwitchProfileQuick').addEventListener('click', () => switchTab('profiles'));

  // Fermeture des modales sur clic extérieur (backdrop) ou touche Escape
  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) {
        // Empêcher la fermeture de la modale d'authentification si non connecté
        if (backdrop.id === 'authModal' && !state.activeProfileId) return;
        closeModals();
      }
    });
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (!state.activeProfileId) return;
      closeModals();
    }
  });

  // Formulaire Création Profil
  document.getElementById('formCreateProfile').addEventListener('submit', async (e) => {
    e.preventDefault();
    const pseudo = document.getElementById('inputPseudo').value.trim();
    if (!pseudo) return;
    try {
      const res = await fetch(`${API_BASE}/api/profiles`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pseudo })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Erreur lors de la création');
      showToast(`Profil "${pseudo}" créé avec succès !`);
      closeModals();
      await loadProfiles();
      setActiveProfile(data.id);
      openIdentityCardModal(data.id);
    } catch (err) {
      alert(err.message);
    }
  });

  // Formulaire Fiche d'Identité enrichie
  document.getElementById('formIdentityCard').addEventListener('submit', async (e) => {
    e.preventDefault();
    const profileId = document.getElementById('idProfileId').value;
    const tp = document.getElementById('idPoitrine')?.value ? parseFloat(document.getElementById('idPoitrine').value) : null;
    const tt = document.getElementById('idTailleTour')?.value ? parseFloat(document.getElementById('idTailleTour').value) : null;
    const th = document.getElementById('idHanches')?.value ? parseFloat(document.getElementById('idHanches').value) : null;
    const mens = (tp || tt || th) ? `${tp || '-'}-${tt || '-'}-${th || '-'}` : (document.getElementById('idMensurations')?.value.trim() || '');

    const bodyData = {
      pseudo: document.getElementById('idPseudo')?.value.trim() || undefined,
      email: document.getElementById('idEmail')?.value.trim() || '',
      prenom: document.getElementById('idPrenom')?.value.trim() || '',
      nom: document.getElementById('idNom')?.value.trim() || '',
      sexe: parseInt(document.getElementById('idSexe')?.value, 10) || 0,
      date_naissance: document.getElementById('idDateNaiss')?.value || '',
      pays_naissance: document.getElementById('idPaysNaissance')?.value.trim() || '',
      habite_pays: document.getElementById('idHabitePays')?.value.trim() || '',
      habite_region_dept: document.getElementById('idHabiteRegion')?.value.trim() || '',
      habite_commune: document.getElementById('idHabiteCommune')?.value.trim() || '',
      ville: document.getElementById('idHabiteCommune')?.value.trim() || document.getElementById('idVille')?.value.trim() || '',
      statut: document.getElementById('idStatut')?.value.trim() || '',
      taille: document.getElementById('idTaille')?.value ? parseFloat(document.getElementById('idTaille').value) : null,
      poids: document.getElementById('idPoids')?.value ? parseFloat(document.getElementById('idPoids').value) : null,
      pointure: document.getElementById('idPointure')?.value ? parseFloat(document.getElementById('idPointure').value) : null,
      tour_poitrine: tp,
      tour_taille: tt,
      tour_hanches: th,
      mensurations: mens,
      origines: document.getElementById('idOrigines')?.value || '',
      couleur_cheveux: document.getElementById('idCouleurCheveux')?.value || '',
      style: document.getElementById('idStyle')?.value || '',
      bio: document.getElementById('idBio')?.value.trim() || '',
      aime_chez_moi: document.getElementById('idAimeChezMoi')?.value.trim() || '',
      aime_pas_chez_moi: document.getElementById('idAimePasChezMoi')?.value.trim() || ''
    };

    try {
      const res = await fetch(`${API_BASE}/api/profiles/${profileId}/identity`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyData)
      });
      if (!res.ok) { const errD = await res.json().catch(() => ({})); throw new Error(errD.error || 'Erreur lors de la sauvegarde du profil'); }
      showToast('Profil mis à jour avec succès !');
      closeModals();
      await loadProfiles();
      updateActiveProfileWidget();
      updateAffinitySelectors();
      if (!isCurrentAdmin()) {
        renderSingleUserProfile();
      }
    } catch (err) {
      alert(err.message);
    }
  });

  // Formulaire Mon Profil Direct (Boutons Enregistrer en haut et en bas)
  const formDirect = document.getElementById('formDirectCockpit');
  if (formDirect) {
    formDirect.addEventListener('submit', async (e) => {
      e.preventDefault();
      const profileId = document.getElementById('ckpProfileId')?.value || state.activeProfileId;
      if (!profileId) return;

      const btnSave = document.getElementById('btnSaveDirectCockpit');
      const btnSaveTop = document.getElementById('btnSaveDirectCockpitTop');
      const feedback = document.getElementById('ckpSaveFeedback');
      if (btnSave) btnSave.disabled = true;
      if (btnSaveTop) btnSaveTop.disabled = true;

      const sitFamille = document.getElementById('ckpSelectSituationFamille')?.value.trim() || '';
      const rechercheDe = document.getElementById('ckpSelectRecherche')?.value.trim() || '';
      const habPays = document.getElementById('ckpHabitePays')?.value.trim() || 'France';
      const habDept = (document.getElementById('ckpHabiteRegionSelect')?.value.trim() || document.getElementById('ckpHabiteRegionText')?.value.trim() || document.getElementById('ckpHabiteRegion')?.value.trim() || '');
      const userEmail = (document.getElementById('ckpInputEmail')?.value || '').trim();

      const bodyData = {
        pseudo: document.getElementById('ckpInputPseudo')?.value.trim() || undefined,
        email: userEmail,
        prenom: document.getElementById('ckpInputPrenom')?.value.trim() || '',
        nom: document.getElementById('ckpInputNom')?.value.trim() || '',
        sexe: parseInt(document.getElementById('ckpSelectSexe')?.value, 10) || 0,
        date_naissance: document.getElementById('ckpInputBirth')?.value || '',
        pays_naissance: document.getElementById('ckpInputPaysNaissance')?.value.trim() || '',
        situation_famille: sitFamille,
        statut: sitFamille,
        recherche_de: rechercheDe,
        habite_pays: habPays,
        habite_region_dept: habDept,
        habite_commune: document.getElementById('ckpHabiteCommune')?.value.trim() || '',
        ville: document.getElementById('ckpHabiteCommune')?.value.trim() || '',
        bio: document.getElementById('ckpInputBio')?.value.trim() || '',
        aime_chez_moi: document.getElementById('ckpInputAimeChezMoi')?.value.trim() || '',
        aime_pas_chez_moi: document.getElementById('ckpInputAimePasChezMoi')?.value.trim() || ''
      };

      try {
        const res = await fetch(`${API_BASE}/api/profiles/${profileId}/identity`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(bodyData)
        });
        if (!res.ok) { const errD = await res.json().catch(() => ({})); throw new Error(errD.error || 'Erreur lors de la sauvegarde du profil'); }
        
        showToast('✔ Mon Profil enregistré avec succès !');
        if (feedback) {
          feedback.textContent = '✔ Modifications enregistrées avec succès !';
          setTimeout(() => { feedback.textContent = ''; }, 3500);
        }
        await loadProfiles();
        updateActiveProfileWidget();
        updateAffinitySelectors();
        checkProfileCompleteness();
      } catch (err) {
        alert('Erreur : ' + err.message);
      } finally {
        if (btnSave) btnSave.disabled = false;
        if (btnSaveTop) btnSaveTop.disabled = false;
      }
    });
  }

  // Sélecteur de profil dans l'onglet questionnaire
  document.getElementById('qSelectProfile').addEventListener('change', (e) => {
    setActiveProfile(parseInt(e.target.value, 10));
  });

  // Filtres questionnaire
  document.getElementById('qFilterThematique')?.addEventListener('change', renderQuestionsDeck);
  document.getElementById('qFilterPack')?.addEventListener('change', renderQuestionsDeck);
  document.getElementById('qFilterClasse')?.addEventListener('change', renderQuestionsDeck);
  document.getElementById('qFilterStatus')?.addEventListener('change', renderQuestionsDeck);
  document.getElementById('qFilterHierarchie')?.addEventListener('change', renderQuestionsDeck);

  // Recherche Profils
  document.getElementById('profileSearchInput').addEventListener('input', (e) => {
    renderProfilesGrid(e.target.value.toLowerCase());
  });

  // Calculateur et Demande de Match
  document.getElementById('btnComputeAffinity').addEventListener('click', handleAffinityOrMatchAction);
  document.getElementById('affProfile1').addEventListener('change', () => {
    updateAffinitySelectorsStatus();
    updateTargetProfilePreview();
  });
  document.getElementById('affProfile2').addEventListener('change', () => {
    updateAffinitySelectorsStatus();
    updateTargetProfilePreview();
  });
  document.getElementById('btnFixCards').addEventListener('click', () => switchTab('profiles'));

  // Boutons Modifier ma fiche d'identité depuis la vue profil unique
  const btnEditMyId = document.getElementById('btnEditMyIdentity');
  if (btnEditMyId) {
    btnEditMyId.addEventListener('click', () => {
      if (state.activeProfileId) openIdentityCardModal(state.activeProfileId);
    });
  }
  const btnEditMyProf = document.getElementById('btnEditMyProfile');
  if (btnEditMyProf) {
    btnEditMyProf.addEventListener('click', () => {
      if (state.activeProfileId) openIdentityCardModal(state.activeProfileId);
    });
  }

  // Onglets du gestionnaire de demandes de match (Reçues / Envoyées)
  const tabReqReceived = document.getElementById('btnTabRequestsReceived');
  const tabReqSent = document.getElementById('btnTabRequestsSent');
  if (tabReqReceived && tabReqSent) {
    tabReqReceived.addEventListener('click', () => {
      tabReqReceived.classList.add('active');
      tabReqSent.classList.remove('active');
      document.getElementById('requestsReceivedPanel')?.classList.add('active');
      document.getElementById('requestsSentPanel')?.classList.remove('active');
    });
    tabReqSent.addEventListener('click', () => {
      tabReqSent.classList.add('active');
      tabReqReceived.classList.remove('active');
      document.getElementById('requestsSentPanel')?.classList.add('active');
      document.getElementById('requestsReceivedPanel')?.classList.remove('active');
    });
  }

  // Bouton Ajouter une Question (Admin) : ouvre la modale complète
  const btnAddQ = document.getElementById('btnOpenAddQuestion');
  if (btnAddQ) {
    btnAddQ.addEventListener('click', openAddQuestionModal);
  }

  // Filtres et Recherche dans la banque de questions (Thématique, Sujet, Classe, Cible, Texte)
  document.getElementById('bankSearchInput')?.addEventListener('input', () => renderQuestionsTable());
  document.getElementById('pendingSearchInput')?.addEventListener('input', () => renderPendingQuestionsTable());
  document.getElementById('pendingFilterClasse')?.addEventListener('change', () => renderPendingQuestionsTable());
  document.getElementById('pendingFilterType')?.addEventListener('change', () => renderPendingQuestionsTable());
  document.getElementById('pendingFilterCible')?.addEventListener('change', () => renderPendingQuestionsTable());
  document.getElementById('bankFilterThematique')?.addEventListener('change', () => {
    updateBankSujetsDropdown();
    renderQuestionsTable();
  });
  document.getElementById('bankFilterSujet')?.addEventListener('change', () => renderQuestionsTable());
  document.getElementById('bankFilterClasse')?.addEventListener('change', () => renderQuestionsTable());
  document.getElementById('bankFilterCible')?.addEventListener('change', () => renderQuestionsTable());
  document.getElementById('bankFilterHierarchie')?.addEventListener('change', () => renderQuestionsTable());
  document.getElementById('btnResetBankFilters')?.addEventListener('click', resetBankFilters);

  // Formulaire Création & Modification Question (Admin)
  document.getElementById('formEditQuestion').addEventListener('submit', async (e) => {
    e.preventDefault();
    const qidRaw = document.getElementById('editQId').value.trim();
    const isNew = !qidRaw;
    const qid = isNew ? null : parseInt(qidRaw, 10);

    const classeVal = parseInt(document.getElementById('editQClasse').value, 10);
    const typeVal = document.getElementById('editQType').value;

    let configReponses = null;
    if (classeVal === 8 || typeVal === 'P' || typeVal === 'T') {
      const isNumeric = document.getElementById('modeReponseNumeric').checked;
      if (isNumeric) {
        configReponses = {
          mode: 'numeric',
          unit: document.getElementById('cfgNumericUnit').value.trim(),
          min: parseFloat(document.getElementById('cfgNumericMin').value) || 0,
          max: parseFloat(document.getElementById('cfgNumericMax').value) || 100,
          step: parseFloat(document.getElementById('cfgNumericStep').value) || 1,
          default_min: parseFloat(document.getElementById('cfgNumericMin').value) || 0,
          default_max: parseFloat(document.getElementById('cfgNumericMax').value) || 100
        };
      } else {
        const rawOpts = document.getElementById('cfgSelectOptions').value.split('\n');
        const optionsList = rawOpts.map(o => o.trim()).filter(o => o.length > 0);
        configReponses = {
          mode: 'select',
          options: optionsList
        };
      }
    }

    const thSel = document.getElementById('editQThematiqueSelect');
    const thVal = (thSel && thSel.value === '__NEW__')
      ? document.getElementById('editQThematiqueCustom').value.trim()
      : (thSel ? thSel.value : document.getElementById('editQThematique').value.trim());

    const sjSel = document.getElementById('editQSujetSelect');
    const sjVal = (sjSel && (sjSel.style.display === 'none' || sjSel.value === '__NEW__'))
      ? document.getElementById('editQSujetCustom').value.trim()
      : (sjSel ? sjSel.value : document.getElementById('editQSujet').value.trim());

    const qData = {
      thematique: thVal || (classeVal === 8 ? 'Identité' : 'Divers'),
      sujet: sjVal || (classeVal === 8 ? 'Identité' : 'Général'),
      classe: classeVal,
      type: typeVal,
      cible: parseInt(document.getElementById('editQCible').value, 10),
      texte: document.getElementById('editQTexte').value.trim(),
      n_quest_lie: parseInt(document.getElementById('editQNQuestLie')?.value || 0, 10),
      config_reponses: configReponses
    };

    try {
      const url = isNew ? `${API_BASE}/api/questions` : `${API_BASE}/api/questions/${qid}`;
      const method = isNew ? 'POST' : 'PUT';

      const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(qData)
      });
      if (!res.ok) throw new Error(isNew ? 'Erreur lors de la création de la question' : 'Erreur lors de la modification de la question');
      
      const resJson = await res.json();
      const savedId = isNew ? resJson.id : qid;
      showToast(isNew ? `Question #${savedId} créée avec succès !` : `Question #${qid} modifiée avec succès !`);
      closeModals();
      await loadQuestions();
      await loadPendingQuestions();
      renderQuestionsTable();
      renderQuestionsDeck();
      if (state.activeProfileId) {
        await loadIdentityAnswers(state.activeProfileId);
      }
    } catch (err) {
      alert(err.message);
    }
  });

  // Suppression Question
  document.getElementById('btnDeleteQuestion').addEventListener('click', async () => {
    const qid = parseInt(document.getElementById('editQId').value, 10);
    if (!qid) return;
    if (confirm(`Confirmez-vous la suppression définitive de la question #${qid} ?`)) {
      try {
        const res = await fetch(`${API_BASE}/api/questions/${qid}`, { method: 'DELETE' });
        if (!res.ok) throw new Error('Erreur lors de la suppression');
        showToast(`Question #${qid} supprimée.`);
        closeModals();
        await loadQuestions();
        await loadPendingQuestions();
        renderQuestionsTable();
        renderQuestionsDeck();
      } catch (err) {
        alert(err.message);
      }
    }
  });

  // Les boutons d'accès aux Questions d'Identité (+ sur moi et + sur l'autre) sont déclenchés directement via onclick="openIdentityDeck(...)"
}

// Bascule d'onglets
function switchTab(tabName) {
  // Sécurité d'accès : Banque de questions réservée exclusivement aux Administrateurs
  if (tabName === 'questions-bank' && !isCurrentAdmin()) {
    showToast('⚠️ Accès restreint : La banque de questions est réservée aux administrateurs.');
    return;
  }
  // Sécurité d'accès : Console d'administration réservée aux Administrateurs
  if (tabName === 'admin' && !isCurrentAdmin()) {
    showToast('⚠️ Accès restreint : La console d\'administration est réservée aux administrateurs.');
    return;
  }

  document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

  const targetPane = document.getElementById(`tab-${tabName}`);
  const targetNav = document.querySelector(`.nav-item[data-tab="${tabName}"]`);

  if (targetPane) targetPane.classList.add('active');
  if (targetNav) targetNav.classList.add('active');

  const titles = {
    'dashboard': { title: 'Tableau de bord', sub: 'Aperçu global, dynamique des profils et affinités calculées' },
    'profiles': { 
      title: isCurrentAdmin() ? 'Gestion des Profils' : 'Mon Profil', 
      sub: isCurrentAdmin() ? 'Supervisez et gérez les comptes membres' : 'Consultez et complétez votre profil, vos informations et vos questions autorisées' 
    },
    'questionnaire': { title: 'Questionnaires', sub: 'Axes Vécu (V), Actuel (A), Découverte (D), Partage (P) et Goûts (G)' },
    'affinity': { title: 'Demande de Match & Radar d\'Affinité', sub: 'Calcul multidimensionnel, synergie croisée et points de fusion' },
    'questions-bank': { title: 'Banque de Questions', sub: 'Gestion des jeux, des classes et des thématiques' },
    'devices-preview': { title: 'Multi-Plateforme (Mobile & Montre)', sub: 'Simulation en direct sur Smartphone et Smartwatch' },
    'admin': { title: 'Administration & Rôles', sub: 'Supervision des privilèges : Administrateur, Abonné, Invité' },
    'roles-guide': { title: 'Guide des Rôles & Protocole de Match', sub: 'Documentation détaillée des fonctionnalités pour Invités, Abonnés et Administrateurs' }
  };

  if (titles[tabName]) {
    document.getElementById('pageTitle').textContent = titles[tabName].title;
    document.getElementById('pageSubtitle').textContent = titles[tabName].sub;
  }

  if (tabName === 'profiles') {
    if (!isCurrentAdmin()) {
      renderSingleUserProfile();
    } else {
      renderProfilesGrid();
    }
  } else if (tabName === 'questionnaire') {
    renderQuestionsDeck();
  } else if (tabName === 'affinity') {
    updateAffinityAccessUi();
    updateAffinitySelectors();
    updateTargetProfilePreview();
    loadMatchRequests();
  } else if (tabName === 'questions-bank') {
    populateBankFilters();
    renderQuestionsTable();
  } else if (tabName === 'devices-preview') {
    updateDevicesPreview();
  } else if (tabName === 'admin') {
    renderAdminUsersTable();
    loadAdminAccessRequests();
  }
}

// Helpers Rôles & Privilèges
function getActiveProfile() {
  return state.profiles.find(p => p.id === state.activeProfileId);
}

function getLoggedInAdmin() {
  if (state.realAdminId) {
    return state.profiles.find(p => p.id === state.realAdminId);
  }
  return state.profiles.find(p => p.role === 'admin');
}

function isRealAdmin() {
  if (state.currentUser && state.currentUser.role === 'admin') {
    return true;
  }
  if (state.realAdminId) {
    const me = state.profiles.find(p => p.id === state.realAdminId);
    return me?.role === 'admin';
  }
  return false;
}

function getActiveRole() {
  if (state.simulatedRole) {
    return state.simulatedRole;
  }
  const p = getActiveProfile();
  return p?.role || 'guest';
}

function isCurrentAdmin() {
  return getActiveRole() === 'admin';
}

function isCurrentSubscriberOrAdmin() {
  const r = getActiveRole();
  return r === 'subscriber' || r === 'admin';
}

// Remplissage dynamique des menus déroulants de profil de test
function populateSimulatedProfileDropdowns(role, selectedProfileId) {
  const headerSelect = document.getElementById('selectSimulatedProfile');
  const bannerSelect = document.getElementById('bannerSimulatedProfileSelect');
  if (!headerSelect && !bannerSelect) return;

  const currentRole = role || 'subscriber';
  const matching = state.profiles.filter(p => p.role === currentRole);
  const others = state.profiles.filter(p => p.role !== currentRole && p.role !== 'admin');

  let optionsHtml = '';

  if (matching.length > 0) {
    const groupTitle = currentRole === 'subscriber' ? '⭐ Abonnés disponibles' : '👤 Invités disponibles';
    optionsHtml += `<optgroup label="${groupTitle}">` + matching.map(p => {
      const isSel = (p.id === selectedProfileId) ? 'selected' : '';
      return `<option value="${p.id}" ${isSel}>${p.pseudo} (${formatAffId(p.id)})</option>`;
    }).join('') + `</optgroup>`;
  }

  if (others.length > 0) {
    const groupTitle = currentRole === 'subscriber' ? '👤 Autres profils (Invités)' : '⭐ Autres profils (Abonnés)';
    optionsHtml += `<optgroup label="${groupTitle}">` + others.map(p => {
      const isSel = (p.id === selectedProfileId) ? 'selected' : '';
      const roleTag = p.role === 'subscriber' ? '⭐' : '👤';
      return `<option value="${p.id}" ${isSel}>${roleTag} ${p.pseudo} (${formatAffId(p.id)})</option>`;
    }).join('') + `</optgroup>`;
  }

  if (headerSelect) {
    headerSelect.innerHTML = optionsHtml;
    headerSelect.value = selectedProfileId;
  }
  if (bannerSelect) {
    bannerSelect.innerHTML = optionsHtml;
    bannerSelect.value = selectedProfileId;
  }
}

// Activation ou changement de vue de simulation pour l'administrateur
function setSimulatedRole(role, targetProfileId = null) {
  if (!isRealAdmin()) return;
  if (!role || role === 'none' || role === 'admin') {
    exitRoleSimulation();
    return;
  }

  // Mémoriser l'administrateur d'origine si pas encore fait
  if (!state.realAdminId && state.activeProfileId) {
    const curr = state.profiles.find(p => p.id === state.activeProfileId);
    if (curr && curr.role === 'admin') {
      state.realAdminId = curr.id;
    }
  }

  state.simulatedRole = role;

  // Déterminer le profil à incarner
  let chosenId = targetProfileId;
  if (!chosenId) {
    const matching = state.profiles.filter(p => p.role === role);
    chosenId = matching.length > 0 ? matching[0].id : state.activeProfileId;
  }
  state.simulatedProfileId = chosenId;

  // Afficher et remplir les sélecteurs de profil
  populateSimulatedProfileDropdowns(role, chosenId);

  const headerBox = document.getElementById('headerSimProfileBox');
  if (headerBox) headerBox.style.display = 'inline-flex';

  const banner = document.getElementById('roleSimulationBanner');
  const label = document.getElementById('simulatedRoleLabel');
  if (banner && label) {
    banner.style.display = 'flex';
    label.className = `sim-role-name ${role}`;
    label.textContent = (role === 'subscriber') ? '⭐ Abonné' : '👤 Invité';
  }

  const selectRole = document.getElementById('selectSimulatedRole');
  if (selectRole) selectRole.value = role;

  // Appliquer le profil incarné
  const prof = state.profiles.find(p => p.id === chosenId);
  setActiveProfile(chosenId);
  applyRolePermissionsUi();

  showToast(`👁️ Mode Test : Vue ${role === 'subscriber' ? 'Abonné' : 'Invité'} activée sous le profil « <strong>${prof ? prof.pseudo : '#' + chosenId}</strong> »`);

  // Si l'utilisateur est sur l'onglet Profil, rafraîchir sa fiche
  const currentTab = document.querySelector('.nav-item.active')?.getAttribute('data-tab');
  if (currentTab === 'profiles') {
    renderSingleUserProfile();
  }
}

// Changement du profil incarné pendant la simulation
function changeSimulatedProfile(profileId) {
  const pid = parseInt(profileId, 10);
  const prof = state.profiles.find(p => p.id === pid);
  if (!prof) return;

  state.simulatedProfileId = pid;

  // Synchronisation du rôle simulé si le profil choisi a un statut différent
  const profRole = (prof.role === 'subscriber') ? 'subscriber' : 'guest';
  if (prof.role !== 'admin' && state.simulatedRole !== profRole) {
    state.simulatedRole = profRole;
    const selectRole = document.getElementById('selectSimulatedRole');
    if (selectRole) selectRole.value = profRole;

    const label = document.getElementById('simulatedRoleLabel');
    if (label) {
      label.className = `sim-role-name ${profRole}`;
      label.textContent = (profRole === 'subscriber') ? '⭐ Abonné' : '👤 Invité';
    }
  }

  const headerSelect = document.getElementById('selectSimulatedProfile');
  const bannerSelect = document.getElementById('bannerSimulatedProfileSelect');
  if (headerSelect) headerSelect.value = pid;
  if (bannerSelect) bannerSelect.value = pid;

  setActiveProfile(pid);
  applyRolePermissionsUi();

  showToast(`👁️ Profil incarné : <strong>${prof.pseudo}</strong> (${formatAffId(pid)}) [${profRole === 'subscriber' ? 'Abonné' : 'Invité'}]`);

  const currentTab = document.querySelector('.nav-item.active')?.getAttribute('data-tab');
  if (currentTab === 'profiles') {
    renderSingleUserProfile();
  }
}

// Tester immédiatement la vue sous un profil précis depuis la liste admin
function testViewAsProfile(profileId) {
  const prof = state.profiles.find(p => p.id === profileId);
  if (!prof) return;

  const targetRole = (prof.role === 'admin') ? 'none' : (prof.role || 'guest');
  if (targetRole === 'none') {
    exitRoleSimulation();
    setActiveProfile(profileId);
  } else {
    setSimulatedRole(targetRole, profileId);
    switchTab('profiles');
  }
}

function exitRoleSimulation() {
  state.simulatedRole = null;
  state.simulatedProfileId = null;

  const banner = document.getElementById('roleSimulationBanner');
  if (banner) banner.style.display = 'none';

  const headerBox = document.getElementById('headerSimProfileBox');
  if (headerBox) headerBox.style.display = 'none';

  const select = document.getElementById('selectSimulatedRole');
  if (select) select.value = 'none';

  // Rétablir le compte administrateur réel
  if (state.realAdminId) {
    setActiveProfile(state.realAdminId);
  }

  showToast('👑 Retour à la vue Administrateur');
  applyRolePermissionsUi();

  const currentTab = document.querySelector('.nav-item.active')?.getAttribute('data-tab');
  if (currentTab === 'profiles') {
    renderProfilesGrid();
  }
}

// Fermeture de la fiche individuelle et retour immédiat à la liste de gestion des profils
function exitToProfilesList() {
  exitRoleSimulation();
  const profilesAdminView = document.getElementById('profilesAdminView');
  const singleProfileUserView = document.getElementById('singleProfileUserView');
  if (profilesAdminView && singleProfileUserView) {
    profilesAdminView.style.display = 'block';
    singleProfileUserView.style.display = 'none';
  }
  const exitBar = document.getElementById('ckpAdminExitBar');
  if (exitBar) exitBar.style.display = 'none';
  switchTab('profiles');
  renderProfilesGrid();
}

function applyRolePermissionsUi() {
  const effectiveRole = getActiveRole();

  // 1. Badge dans le widget profil
  const roleBadge = document.getElementById('activeRoleBadge');
  if (roleBadge) {
    roleBadge.className = `role-badge ${effectiveRole}`;
    if (state.simulatedRole) {
      roleBadge.innerHTML = (effectiveRole === 'subscriber') ? '⭐ Abonné (Test)' : '👤 Invité (Test)';
    } else {
      if (effectiveRole === 'admin') {
        roleBadge.innerHTML = '👑 Admin';
      } else if (effectiveRole === 'subscriber') {
        roleBadge.innerHTML = '⭐ Abonné';
      } else {
        roleBadge.innerHTML = '👤 Invité';
      }
    }
  }

  // 2. Renommer l'onglet Profil dans la sidebar : "Mon Profil" pour Invité/Abonné, "Gestion des Profils" pour Admin
  const navProfilesLabel = document.getElementById('navProfilesLabel');
  if (navProfilesLabel) {
    navProfilesLabel.textContent = isCurrentAdmin() ? 'Gestion des Profils' : 'Mon Profil';
  }

  // 2b. Cloisonnement de la vue Profils :
  // - Les Invités et Abonnés ne voient et n'interviennent que sur leur propre profil (singleProfileUserView)
  // - L'Administrateur a accès à la vue complète (profilesAdminView)
  const profilesAdminView = document.getElementById('profilesAdminView');
  const singleProfileUserView = document.getElementById('singleProfileUserView');
  if (profilesAdminView && singleProfileUserView) {
    if (isCurrentAdmin()) {
      profilesAdminView.style.display = 'block';
      singleProfileUserView.style.display = 'none';
      renderProfilesGrid();
    } else {
      profilesAdminView.style.display = 'none';
      singleProfileUserView.style.display = 'block';
      renderSingleUserProfile();
    }
  }

  // 3. Onglet Admin dans la sidebar
  const navAdmin = document.getElementById('navAdminItem');
  if (navAdmin) {
    if (isCurrentAdmin()) {
      navAdmin.style.display = 'flex';
    } else {
      navAdmin.style.display = 'none';
      const currentActivePane = document.querySelector('.tab-pane.active');
      if (currentActivePane && currentActivePane.id === 'tab-admin') {
        switchTab('dashboard');
      }
    }
  }

  // 3b. Onglet Banque de questions dans la sidebar (Réservé exclusivement à l'Admin)
  const navBank = document.getElementById('navQuestionsBankItem');
  if (navBank) {
    if (isCurrentAdmin()) {
      navBank.style.display = 'flex';
    } else {
      navBank.style.display = 'none';
      const currentActivePane = document.querySelector('.tab-pane.active');
      if (currentActivePane && currentActivePane.id === 'tab-questions-bank') {
        switchTab('dashboard');
      }
    }
  }

  // 4. Sélecteur de simulation dans le header (accessible pour un vrai admin)
  const simSwitchBox = document.getElementById('simulationSwitchBox');
  if (simSwitchBox) {
    simSwitchBox.style.display = isRealAdmin() ? 'flex' : 'none';
  }

  // 5. Calculateur d'Affinité (Verrouillé si Invité)
  updateAffinityAccessUi();

  // 5b. Adaptation du bouton et du gestionnaire de match
  const btnMatch = document.getElementById('btnComputeAffinity');
  if (btnMatch) {
    if (effectiveRole === 'subscriber') {
      btnMatch.innerHTML = '<span>💌</span> Demande de Match';
    } else if (effectiveRole === 'admin') {
      btnMatch.innerHTML = '<span>⚡</span> Lancer un Match Direct';
    } else {
      btnMatch.innerHTML = '<span>🔒</span> Réservé aux Abonnés';
    }
  }

  // 5c. Section des demandes de match (Abonnés et Admins)
  const mrSection = document.getElementById('matchRequestsSection');
  if (mrSection) {
    if (effectiveRole === 'subscriber' || effectiveRole === 'admin') {
      mrSection.style.display = 'block';
      loadMatchRequests();
    } else {
      mrSection.style.display = 'none';
    }
  }

  // 6. Banque de questions (Bouton d'ajout et boutons d'édition)
  const btnAddQ = document.getElementById('btnOpenAddQuestion');
  if (btnAddQ) {
    btnAddQ.style.display = isCurrentAdmin() ? 'inline-flex' : 'none';
  }

  // 7. Bouton Nouveau Profil dans le header (Visible exclusivement pour l'Administrateur)
  const btnNewProfile = document.getElementById('btnNewProfileModal');
  if (btnNewProfile) {
    btnNewProfile.style.display = isCurrentAdmin() ? 'inline-flex' : 'none';
  }

  renderQuestionsTable();
}

function updateAffinityAccessUi() {
  const role = getActiveRole();
  const guestLock = document.getElementById('affinityGuestLock');
  const calcContent = document.getElementById('affinityCalculatorContent');
  
  if (guestLock && calcContent) {
    if (role === 'guest') {
      guestLock.style.display = 'block';
      calcContent.style.display = 'none';
    } else {
      guestLock.style.display = 'none';
      calcContent.style.display = 'block';
    }
  }
}

function openAuthModal() {
  const modal = document.getElementById('authModal');
  if (modal) {
    modal.style.display = 'flex';
    document.getElementById('loginInput')?.focus();
  }
}

function closeAuthModal() {
  const modal = document.getElementById('authModal');
  if (modal) {
    modal.style.display = 'none';
  }
}

function switchAuthView(view) {
  const btnToggleLogin = document.getElementById('btnToggleLogin');
  const btnToggleRegister = document.getElementById('btnToggleRegister');
  const formLogin = document.getElementById('formLogin');
  const formRegister = document.getElementById('formRegister');
  const formForgot = document.getElementById('formForgotPassword');
  const formReset = document.getElementById('formResetPassword');
  const tabsContainer = document.querySelector('.auth-tabs-toggle');
  const subtitle = document.getElementById('authSubtitle');

  // Cacher tous les formulaires
  if (formLogin) formLogin.style.display = 'none';
  if (formRegister) formRegister.style.display = 'none';
  if (formForgot) formForgot.style.display = 'none';
  if (formReset) formReset.style.display = 'none';

  if (view === 'login') {
    if (tabsContainer) tabsContainer.style.display = 'flex';
    if (btnToggleLogin) btnToggleLogin.classList.add('active');
    if (btnToggleRegister) btnToggleRegister.classList.remove('active');
    if (formLogin) formLogin.style.display = 'block';
    if (subtitle) subtitle.textContent = 'Accès sécurisé à votre espace relationnel';
    document.getElementById('loginInput')?.focus();
  } else if (view === 'register') {
    if (tabsContainer) tabsContainer.style.display = 'flex';
    if (btnToggleRegister) btnToggleRegister.classList.add('active');
    if (btnToggleLogin) btnToggleLogin.classList.remove('active');
    if (formRegister) formRegister.style.display = 'block';
    if (subtitle) subtitle.textContent = 'Création instantanée de votre profil Invité';
    document.getElementById('regPseudo')?.focus();
  } else if (view === 'forgot') {
    if (tabsContainer) tabsContainer.style.display = 'none';
    if (formForgot) formForgot.style.display = 'block';
    if (subtitle) subtitle.textContent = 'Récupération de mot de passe';
    document.getElementById('forgotLoginInput')?.focus();
  } else if (view === 'reset') {
    if (tabsContainer) tabsContainer.style.display = 'none';
    if (formReset) formReset.style.display = 'block';
    if (subtitle) subtitle.textContent = 'Définir un nouveau mot de passe';
    document.getElementById('resetCodeInput')?.focus();
  }
}
window.switchAuthView = switchAuthView;

function setupAuthListeners() {
  const btnToggleLogin = document.getElementById('btnToggleLogin');
  const btnToggleRegister = document.getElementById('btnToggleRegister');
  const formLogin = document.getElementById('formLogin');
  const formRegister = document.getElementById('formRegister');
  const formForgot = document.getElementById('formForgotPassword');
  const formReset = document.getElementById('formResetPassword');
  const btnLogout = document.getElementById('btnLogout');

  if (btnToggleLogin) {
    btnToggleLogin.addEventListener('click', () => switchAuthView('login'));
  }
  if (btnToggleRegister) {
    btnToggleRegister.addEventListener('click', () => switchAuthView('register'));
  }

  // Connexion
  if (formLogin) {
    formLogin.addEventListener('submit', async (e) => {
      e.preventDefault();
      const login = document.getElementById('loginInput').value.trim();
      const password = document.getElementById('loginPassword').value.trim();
      const feedback = document.getElementById('loginFeedback');
      const btnSubmit = document.getElementById('btnSubmitLogin');

      if (!login || !password) return;
      btnSubmit.disabled = true;
      btnSubmit.textContent = 'Connexion en cours...';
      feedback.style.display = 'none';

      try {
        const res = await fetch(`${API_BASE}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ login, password })
        });
        const data = await res.json();
        if (!res.ok) {
          feedback.textContent = data.error || 'Erreur lors de la connexion.';
          feedback.style.display = 'block';
          feedback.style.background = 'rgba(239, 68, 68, 0.15)';
          feedback.style.color = '#ef4444';
          feedback.style.border = '1px solid rgba(239, 68, 68, 0.3)';
        } else {
          setAuthToken(data.token);
          state.currentUser = data.profile;
          state.activeProfileId = data.profile.id;
          if (data.profile.role === 'admin') state.realAdminId = data.profile.id;
          closeAuthModal();
          showToast(`Bienvenue ${data.profile.pseudo} !`, 'success');
          await loadInitialData();
        }
      } catch (err) {
        feedback.textContent = 'Erreur réseau, veuillez réessayer.';
        feedback.style.display = 'block';
      } finally {
        btnSubmit.disabled = false;
        btnSubmit.innerHTML = '<span>🔐</span> Se connecter';
      }
    });
  }

  // Inscription rapide (pseudo et mot de passe uniquement)
  if (formRegister) {
    formRegister.addEventListener('submit', async (e) => {
      e.preventDefault();
      const pseudo = document.getElementById('regPseudo').value.trim();
      const password = document.getElementById('regPassword').value.trim();
      const feedback = document.getElementById('registerFeedback');
      const btnSubmit = document.getElementById('btnSubmitRegister');

      if (!pseudo || !password) return;
      btnSubmit.disabled = true;
      btnSubmit.textContent = 'Création en cours...';
      feedback.style.display = 'none';

      try {
        const res = await fetch(`${API_BASE}/api/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pseudo, password })
        });
        const data = await res.json();
        if (!res.ok) {
          feedback.textContent = data.error || 'Erreur lors de l\'inscription.';
          feedback.style.display = 'block';
          feedback.style.background = 'rgba(239, 68, 68, 0.15)';
          feedback.style.color = '#ef4444';
          feedback.style.border = '1px solid rgba(239, 68, 68, 0.3)';
        } else {
          setAuthToken(data.token);
          state.currentUser = data.profile;
          state.activeProfileId = data.profile.id;
          closeAuthModal();
          showToast(`Compte créé avec succès ! Bienvenue ${data.profile.pseudo}`, 'success');
          await loadInitialData();
        }
      } catch (err) {
        feedback.textContent = 'Erreur réseau, veuillez réessayer.';
        feedback.style.display = 'block';
      } finally {
        btnSubmit.disabled = false;
        btnSubmit.innerHTML = '<span>✨</span> Créer mon profil Invité';
      }
    });
  }

  // Mot de passe oublié - Étape 1 : Demande de code
  if (formForgot) {
    formForgot.addEventListener('submit', async (e) => {
      e.preventDefault();
      const login_or_email = document.getElementById('forgotLoginInput').value.trim();
      const feedback = document.getElementById('forgotFeedback');
      const btnSubmit = document.getElementById('btnSubmitForgot');

      if (!login_or_email) return;
      btnSubmit.disabled = true;
      btnSubmit.textContent = 'Vérification en cours...';
      feedback.style.display = 'none';

      try {
        const res = await fetch(`${API_BASE}/api/auth/forgot-password`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ login_or_email })
        });
        const data = await res.json();
        if (!res.ok) {
          feedback.textContent = data.error || 'Impossible de traiter la demande.';
          feedback.style.display = 'block';
          feedback.style.background = 'rgba(239, 68, 68, 0.15)';
          feedback.style.color = '#ef4444';
          feedback.style.border = '1px solid rgba(239, 68, 68, 0.3)';
        } else {
          state.lastForgotIdentifier = login_or_email;
          const targetNotice = document.getElementById('resetTargetIdentifier');
          if (targetNotice) targetNotice.textContent = data.email_masked ? `${data.pseudo} (${data.email_masked})` : data.pseudo;
          
          // Préremplir le code de réinitialisation pour une expérience directe et fluide
          const codeInput = document.getElementById('resetCodeInput');
          if (codeInput && data.reset_code) {
            codeInput.value = data.reset_code;
          }
          
          switchAuthView('reset');
          const resetFeed = document.getElementById('resetFeedback');
          if (resetFeed) {
            resetFeed.innerHTML = `✅ <strong>Code généré avec succès !</strong><br><span style="font-size:12px;">Votre code à 6 chiffres est : <strong style="color:#38bdf8; font-size:15px; letter-spacing:1px;">${data.reset_code}</strong> (valable 15 minutes). Saisissez votre nouveau mot de passe ci-dessous.</span>`;
            resetFeed.style.display = 'block';
            resetFeed.style.background = 'rgba(16, 185, 129, 0.15)';
            resetFeed.style.color = '#34d399';
            resetFeed.style.border = '1px solid rgba(16, 185, 129, 0.3)';
          }
        }
      } catch (err) {
        feedback.textContent = 'Erreur réseau, veuillez réessayer.';
        feedback.style.display = 'block';
      } finally {
        btnSubmit.disabled = false;
        btnSubmit.innerHTML = '<span>📨</span> Obtenir un code de réinitialisation';
      }
    });
  }

  // Mot de passe oublié - Étape 2 : Validation du nouveau mot de passe
  if (formReset) {
    formReset.addEventListener('submit', async (e) => {
      e.preventDefault();
      const login_or_email = state.lastForgotIdentifier || document.getElementById('forgotLoginInput')?.value.trim();
      const reset_code = document.getElementById('resetCodeInput').value.trim();
      const new_password = document.getElementById('resetNewPassword').value.trim();
      const confirm_password = document.getElementById('resetConfirmPassword').value.trim();
      const feedback = document.getElementById('resetFeedback');
      const btnSubmit = document.getElementById('btnSubmitReset');

      if (!reset_code || !new_password) return;
      if (new_password !== confirm_password) {
        feedback.textContent = 'Les mots de passe ne correspondent pas.';
        feedback.style.display = 'block';
        feedback.style.background = 'rgba(239, 68, 68, 0.15)';
        feedback.style.color = '#ef4444';
        feedback.style.border = '1px solid rgba(239, 68, 68, 0.3)';
        return;
      }

      btnSubmit.disabled = true;
      btnSubmit.textContent = 'Réinitialisation en cours...';
      feedback.style.display = 'none';

      try {
        const res = await fetch(`${API_BASE}/api/auth/reset-password`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ login_or_email, reset_code, new_password })
        });
        const data = await res.json();
        if (!res.ok) {
          feedback.textContent = data.error || 'Erreur lors de la réinitialisation.';
          feedback.style.display = 'block';
          feedback.style.background = 'rgba(239, 68, 68, 0.15)';
          feedback.style.color = '#ef4444';
          feedback.style.border = '1px solid rgba(239, 68, 68, 0.3)';
        } else {
          showToast('Mot de passe réinitialisé avec succès ! Veuillez vous connecter.', 'success');
          switchAuthView('login');
          const loginIn = document.getElementById('loginInput');
          if (loginIn && login_or_email) loginIn.value = login_or_email;
          const loginPwd = document.getElementById('loginPassword');
          if (loginPwd) {
            loginPwd.value = '';
            loginPwd.focus();
          }
        }
      } catch (err) {
        feedback.textContent = 'Erreur réseau, veuillez réessayer.';
        feedback.style.display = 'block';
      } finally {
        btnSubmit.disabled = false;
        btnSubmit.innerHTML = '<span>🔒</span> Valider le nouveau mot de passe';
      }
    });
  }

  // Déconnexion
  if (btnLogout) {
    btnLogout.addEventListener('click', async () => {
      if (confirm('Voulez-vous vraiment vous déconnecter ?')) {
        try {
          await fetch(`${API_BASE}/api/auth/logout`, { method: 'POST' });
        } catch (e) {}
        removeAuthToken();
        state.currentUser = null;
        state.activeProfileId = null;
        state.realAdminId = null;
        openAuthModal();
        showToast('Vous avez été déconnecté.', 'info');
      }
    });
  }
}

// Chargement initial
async function loadInitialData() {
  const token = getAuthToken();
  if (!token) {
    openAuthModal();
    return;
  }

  try {
    const meRes = await fetch(`${API_BASE}/api/auth/me`);
    if (!meRes.ok) {
      removeAuthToken();
      openAuthModal();
      return;
    }
    const meData = await meRes.json();
    state.currentUser = meData.user;
    state.activeProfileId = meData.user.id;
    if (meData.user.role === 'admin') {
      state.realAdminId = meData.user.id;
    } else {
      state.realAdminId = null;
    }
    closeAuthModal();
  } catch (err) {
    console.error('Erreur vérification session:', err);
    openAuthModal();
    return;
  }

  try {
    await loadProfiles();
    if (state.activeProfileId) {
      setActiveProfile(state.activeProfileId);
    }
  } catch (err) {
    console.error('Erreur chargement profil initial:', err);
  }

  // Chargements complémentaires protégés
  try { await loadPacks(); } catch (e) { console.warn(e); }
  try { await loadQuestions(); } catch (e) { console.warn(e); }
  try { await loadPendingQuestions(); } catch (e) { console.warn(e); }
  try { await loadStats(); } catch (e) { console.warn(e); }
}

// Profils
async function loadProfiles() {
  try {
    const res = await fetch(`${API_BASE}/api/profiles`);
    const data = await res.json();
    state.profiles = data.profiles || [];
    
    // Mémoriser l'administrateur système connecté
    if (!state.realAdminId) {
      const adm = state.profiles.find(p => p.role === 'admin');
      if (adm) state.realAdminId = adm.id;
    }

    renderProfilesGrid();
    renderDashboardProfiles();
    updateProfileDropdowns();
    if (document.getElementById('tab-admin')?.classList.contains('active')) {
      renderAdminUsersTable();
    }
  } catch (err) {
    console.error('Erreur chargement profils:', err);
  }
}

function setActiveProfile(id) {
  state.activeProfileId = id;
  
  // Si l'administrateur sélectionne un profil hors simulation, enregistrer son ID
  if (!state.simulatedRole) {
    const curr = state.profiles.find(p => p.id === id);
    if (curr && curr.role === 'admin') {
      state.realAdminId = curr.id;
    }
  }

  // Si on n'est pas un admin réel et qu'aucune simulation n'est en cours
  if (!isRealAdmin() && !state.simulatedRole) {
    const banner = document.getElementById('roleSimulationBanner');
    if (banner) banner.style.display = 'none';
    const select = document.getElementById('selectSimulatedRole');
    if (select) select.value = 'none';
    const headerBox = document.getElementById('headerSimProfileBox');
    if (headerBox) headerBox.style.display = 'none';
  }

  const prof = state.profiles.find(p => p.id === id);
  if (prof) {
    document.getElementById('activePseudo').textContent = prof.pseudo;
    document.getElementById('activeAvatar').textContent = prof.pseudo.charAt(0).toUpperCase();

    // Statut de la fiche d'identité (Non requis pour un Administrateur)
    const statusPill = document.getElementById('activeStatusPill');
    if (statusPill) {
      if (prof.role === 'admin') {
        statusPill.innerHTML = '<span class="status-dot cyan"></span> Superviseur Système';
      } else if (prof.has_identity) {
        statusPill.innerHTML = '<span class="status-dot success"></span> Profil complété';
      } else {
        statusPill.innerHTML = '<span class="status-dot warning"></span> Profil à compléter';
      }
    }

    applyRolePermissionsUi();
  }

  const qSelect = document.getElementById('qSelectProfile');
  if (qSelect) qSelect.value = id;
  updateQuestionnaireFilters();
  loadActiveProfileAnswers();
  loadIdentityAnswers(id);
}

window.onQProfileChange = function(val) {
  if (!val) return;
  const pid = parseInt(val, 10);
  setActiveProfile(pid);
};

function updateActiveProfileWidget() {
  if (state.activeProfileId) setActiveProfile(state.activeProfileId);
}

function updateProfileDropdowns() {
  const qSelect = document.getElementById('qSelectProfile');
  const aff1 = document.getElementById('affProfile1');
  const aff2 = document.getElementById('affProfile2');

  // Seuls les membres (Abonnés et Invités) sont éligibles aux questionnaires et aux matchs
  const memberProfiles = state.profiles.filter(p => p.role !== 'admin');

  const memberOptionsHtml = memberProfiles.map(p => {
    const roleTag = (p.role === 'subscriber') ? '⭐' : '👤';
    return `<option value="${p.id}">${roleTag} ${p.pseudo} (${p.prenom || 'Profil à compléter'})</option>`;
  }).join('');

  if (qSelect) {
    if (!isRealAdmin() && state.activeProfileId) {
      const myProf = state.profiles.find(p => p.id === state.activeProfileId);
      if (myProf) {
        qSelect.innerHTML = `<option value="${myProf.id}">${myProf.pseudo}</option>`;
        qSelect.value = myProf.id;
        qSelect.disabled = true;
      }
    } else {
      const adminProf = state.profiles.find(p => p.role === 'admin');
      const adminOptionHtml = adminProf 
        ? `<option value="${adminProf.id}">👑 ${adminProf.pseudo} (Mode Superviseur)</option>` 
        : '';
      qSelect.innerHTML = adminOptionHtml + memberOptionsHtml;
      qSelect.disabled = false;
      const activeExists = state.profiles.some(p => p.id === state.activeProfileId);
      if (activeExists) {
        qSelect.value = state.activeProfileId;
      } else if (adminProf) {
        qSelect.value = adminProf.id;
      } else if (memberProfiles.length > 0) {
        qSelect.value = memberProfiles[0].id;
      }
    }
  }

  if (aff1) {
    if (!isRealAdmin() && state.activeProfileId) {
      const myProf = state.profiles.find(p => p.id === state.activeProfileId);
      if (myProf) {
        aff1.innerHTML = `<option value="${myProf.id}">⭐ ${myProf.pseudo} (Moi)</option>`;
        aff1.value = myProf.id;
        aff1.disabled = true;
      }
    } else {
      aff1.innerHTML = memberProfiles.length > 0 
        ? memberOptionsHtml 
        : '<option value="">Aucun membre disponible</option>';
      aff1.disabled = false;
    }
  }

  if (aff2) {
    aff2.innerHTML = memberProfiles.length > 0 
      ? memberOptionsHtml 
      : '<option value="">Aucun membre disponible</option>';
    if (memberProfiles.length > 1) {
      aff2.selectedIndex = 1;
    }
  }

  updateAffinitySelectorsStatus();
}

function renderProfilesGrid(filter = '') {
  const container = document.getElementById('profilesGrid');
  if (!container) return;

  const filtered = state.profiles.filter(p => {
    const term = filter.toLowerCase();
    return p.pseudo.toLowerCase().includes(term) ||
           (p.prenom && p.prenom.toLowerCase().includes(term)) ||
           (p.ville && p.ville.toLowerCase().includes(term));
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <p>Aucun profil trouvé. Créez votre premier profil pour commencer !</p>
      </div>`;
    return;
  }

  container.innerHTML = filtered.map(p => {
    const isReady = p.has_identity;
    const role = p.role || 'guest';
    const isAdmin = (role === 'admin');
    const roleBadge = isAdmin 
      ? '<span class="role-badge admin">👑 Administrateur</span>' 
      : (role === 'subscriber' ? '<span class="role-badge subscriber">⭐ Abonné</span>' : '<span class="role-badge guest">👤 Invité</span>');

    return `
      <div class="profile-card ${isAdmin ? 'admin-system-card' : ''}">
        <div class="profile-top">
          <div class="p-avatar-large" style="${isAdmin ? 'background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%); color: #07090E; font-weight:800;' : ''}">
            ${p.pseudo.charAt(0).toUpperCase()}
          </div>
          <div class="p-meta">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
              <h4>${p.pseudo}</h4>
              ${roleBadge}
            </div>
            <p style="${isAdmin ? 'color:var(--accent-cyan); font-weight:500;' : ''}">
              ${isAdmin ? 'Superviseur de la Plateforme Affinity' : (p.prenom ? `${p.prenom} ${p.nom || ''}` : 'Profil non complété')}
            </p>
          </div>
        </div>

        ${!isAdmin ? `
          <div class="profile-stats-row">
            <div>Ville : <strong>${p.ville || 'Non précisée'}</strong></div>
            <div>Questions : <strong>${p.answers_count || 0}</strong></div>
          </div>
          <div class="profile-status-badge" style="margin-bottom: 14px;">
            ${isReady 
              ? '<span class="status-badge-live"><span class="status-dot success"></span> Profil complété</span>' 
              : '<span class="status-badge-live" style="color:var(--accent-amber)"><span class="status-dot warning"></span> Profil à compléter</span>'}
          </div>
        ` : `
          <div class="profile-status-badge" style="margin-bottom: 14px;">
            <span class="status-badge-live" style="color:var(--accent-cyan); background:rgba(0, 242, 254, 0.08); border-color:rgba(0, 242, 254, 0.25);">
              <span class="status-dot cyan"></span> Compte Administrateur
            </span>
          </div>
        `}

        <div class="profile-actions">
          <button class="btn btn-sm btn-primary" onclick="openProfileCockpitDirect(${p.id})" title="Consulter et modifier ce profil">
            <span>👤</span> ${isAdmin ? 'Mon Profil' : 'Voir le Profil'}
          </button>
          <button class="btn btn-sm btn-outline" onclick="openIdentityDeck('self', ${p.id})" title="Répondre à vos caractéristiques personnelles (+ sur moi)">
            <span>👤</span> + sur moi
          </button>
          <button class="btn btn-sm btn-outline partner-btn" onclick="openIdentityDeck('partner', ${p.id})" title="Définir les critères pour l'autre (+ sur l'autre)">
            <span>👥</span> + sur l'autre
          </button>
          ${!isAdmin ? `
            <button class="btn btn-sm btn-secondary" onclick="selectAndGoToQuestionnaire(${p.id})" title="Accéder aux questionnaires généraux">
              <span>✍️</span> Questionnaire
            </button>
          ` : ''}
          ${isRealAdmin() && !isAdmin ? `
            <button class="btn btn-sm btn-outline" onclick="testViewAsProfile(${p.id})" title="Tester l'application comme ce membre" style="border-color:rgba(56,189,248,0.4); color:#38BDF8;">
              <span>👁️</span> Vue
            </button>
          ` : ''}
          ${!isAdmin || state.profiles.filter(pr => pr.role === 'admin').length > 1 ? `
            <button class="btn btn-sm btn-outline" onclick="deleteProfileConfirm(${p.id}, '${p.pseudo}')" title="Supprimer">
              <span>🗑️</span>
            </button>
          ` : ''}
        </div>
      </div>
    `;
  }).join('');
}

// Ouvrir directement la fiche cockpit pour un profil sélectionné
function openProfileCockpitDirect(profileId) {
  setActiveProfile(profileId);
  const profilesAdminView = document.getElementById('profilesAdminView');
  const singleProfileUserView = document.getElementById('singleProfileUserView');
  if (profilesAdminView && singleProfileUserView) {
    profilesAdminView.style.display = 'none';
    singleProfileUserView.style.display = 'block';
  }
  const exitBar = document.getElementById('ckpAdminExitBar');
  if (exitBar) {
    exitBar.style.display = isRealAdmin() ? 'flex' : 'none';
  }
  renderSingleUserProfile();
}

// Helpers Identifiant Unique AFF-XXXX
function formatAffId(profileOrId) {
  if (!profileOrId) return 'AFF-0';
  if (typeof profileOrId === 'object') {
    if (profileOrId.code_profil) return profileOrId.code_profil;
    return (profileOrId.role === 'admin' ? 'ADM-' : 'AFF-') + profileOrId.id;
  }
  const pid = Number(profileOrId);
  const p = state.profiles ? state.profiles.find(x => x.id === pid) : null;
  if (p && p.code_profil) return p.code_profil;
  if (p && p.role === 'admin') return 'ADM-' + pid;
  return (pid === 1 ? 'ADM-' : 'AFF-') + pid;
}

function copyMyAffId() {
  const p = getActiveProfile();
  if (!p) return;
  const affId = formatAffId(p.id);
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(affId).then(() => {
      showToast(`📋 Identifiant membre <strong>${affId}</strong> copié !`);
    }).catch(() => {
      showToast(`Identifiant membre : ${affId}`);
    });
  } else {
    showToast(`Identifiant membre : ${affId}`);
  }
}

// ==========================================================================
// VUE COCKPIT PROFIL INDIVIDUEL COMPACT (INVITÉ & ABONNÉ)
// ==========================================================================
function renderSingleUserProfile() {
  const p = getActiveProfile();
  if (!p) return;

  const affId = formatAffId(p.id);
  const role = p.role || 'guest';
  const isSub = (role === 'subscriber');

  // 1. En-tête profil gauche
  const elAvatar = document.getElementById('myProfileAvatar');
  const elRoleBadge = document.getElementById('myProfileRoleBadge');
  const elAffId = document.getElementById('myProfileAffId');
  const inputProfileId = document.getElementById('ckpProfileId');

  if (inputProfileId) inputProfileId.value = p.id;
  if (elAvatar) elAvatar.textContent = p.pseudo.charAt(0).toUpperCase();
  if (elAffId) elAffId.textContent = affId;
  if (elRoleBadge) {
    elRoleBadge.className = `role-badge ${role}`;
    elRoleBadge.textContent = role === 'admin' ? '👑 Administrateur' : (role === 'subscriber' ? '⭐ Abonné' : '👤 Invité');
  }

  // Barre de fermeture pour l'administrateur consultant la fiche d'un profil
  const exitBar = document.getElementById('ckpAdminExitBar');
  if (exitBar) {
    exitBar.style.display = isRealAdmin() ? 'flex' : 'none';
  }

  // 2. Remplissage direct du Formulaire d'Identité (gauche)
  const elFullName = document.getElementById('myProfileFullName');
  const computedName = `${p.prenom || ''} ${p.nom || ''}`.trim();
  if (elFullName) elFullName.textContent = computedName || 'Non renseigné';

  const fPseudo = document.getElementById('ckpInputPseudo');
  const fPrenom = document.getElementById('ckpInputPrenom');
  const fNom = document.getElementById('ckpInputNom');
  const fSexe = document.getElementById('ckpSelectSexe');
  const fBirth = document.getElementById('ckpInputBirth');
  const fSitFamille = document.getElementById('ckpSelectSituationFamille');
  const fRecherche = document.getElementById('ckpSelectRecherche');
  const fBio = document.getElementById('ckpInputBio');
  const fAime = document.getElementById('ckpInputAimeChezMoi');
  const fAimePas = document.getElementById('ckpInputAimePasChezMoi');

  if (fPseudo) fPseudo.value = p.pseudo || '';
  const fEmail = document.getElementById('ckpInputEmail');
  if (fEmail) fEmail.value = p.email || '';
  if (fPrenom) fPrenom.value = p.prenom || '';
  if (fNom) fNom.value = p.nom || '';
  if (fSexe) fSexe.value = p.sexe ?? 0;
  if (fBirth) {
    fBirth.value = p.date_naissance || '';
    updateDateInputAgeFeedback(fBirth, document.getElementById('ckpAgeBadge'), document.getElementById('ckpAgeFeedback'));
  }
  if (fSitFamille) fSitFamille.value = p.situation_famille || p.statut || '';
  if (fRecherche) fRecherche.value = p.recherche_de || '';

  const fPaysNaiss = document.getElementById('ckpInputPaysNaissance');
  const fHabPays = document.getElementById('ckpHabitePays');
  const fHabReg = document.getElementById('ckpHabiteRegion');
  const fHabRegSel = document.getElementById('ckpHabiteRegionSelect');
  const fHabRegTxt = document.getElementById('ckpHabiteRegionText');
  const fHabCom = document.getElementById('ckpHabiteCommune');

  if (fPaysNaiss) {
    let pNaiss = p.pays_naissance || '';
    if (pNaiss && !['France', 'UE', 'Hors UE'].includes(pNaiss)) {
      pNaiss = 'France';
    }
    fPaysNaiss.value = pNaiss;
  }

  const curPays = p.habite_pays || (p.habite_commune || p.ville ? 'France' : 'France');
  const finalPays = (curPays === 'France' || curPays === 'UE' || curPays === 'Hors UE') ? curPays : 'France';
  if (fHabPays) fHabPays.value = finalPays;

  const regDeptVal = p.habite_region_dept || '';
  if (fHabReg) fHabReg.value = regDeptVal;

  if (finalPays === 'France') {
    if (fHabRegSel) {
      fHabRegSel.style.display = 'block';
      let matched = false;
      if (regDeptVal) {
        for (let opt of fHabRegSel.options) {
          if (opt.value === regDeptVal || opt.value.startsWith(regDeptVal) || opt.value.includes(regDeptVal)) {
            fHabRegSel.value = opt.value;
            matched = true;
            break;
          }
        }
      }
      if (!matched && !regDeptVal) fHabRegSel.value = '';
    }
    if (fHabRegTxt) fHabRegTxt.style.display = 'none';
  } else {
    if (fHabRegSel) fHabRegSel.style.display = 'none';
    if (fHabRegTxt) {
      fHabRegTxt.style.display = 'block';
      fHabRegTxt.value = regDeptVal;
    }
  }

  if (fHabCom) fHabCom.value = p.habite_commune || p.ville || '';
  if (fBio) fBio.value = p.bio || '';
  if (fAime) fAime.value = p.aime_chez_moi || '';
  if (fAimePas) fAimePas.value = p.aime_pas_chez_moi || '';

  checkHabiteCommuneCoherence();
  checkProfileCompleteness();
  updateIdentityCompletionBadge();
  loadIdentityAnswers(p.id);

  // 3. Visibilité de l'onglet Matchs selon le rôle
  const btnMatches = document.getElementById('btnCkpTabMatches');
  if (btnMatches) {
    btnMatches.style.display = isSub ? 'inline-flex' : 'none';
    if (!isSub && document.getElementById('paneCkpMatches')?.classList.contains('active')) {
      switchCockpitSubTab('catalog');
    }
  }

  // 4. Chargement des sous-panneaux
  loadProfileCatalogAccess(p.id);
  loadProfileAdminRequests(p.id);
  if (isSub) {
    loadProfileCockpitMatches(p.id);
  }
}

// Bascule des onglets du cockpit profil
function switchCockpitSubTab(tabName) {
  const tabs = {
    'catalog': { btn: 'btnCkpTabCatalog', pane: 'paneCkpCatalog' },
    'admin-requests': { btn: 'btnCkpTabAdminRequests', pane: 'paneCkpAdminRequests' },
    'matches': { btn: 'btnCkpTabMatches', pane: 'paneCkpMatches' }
  };

  Object.entries(tabs).forEach(([name, def]) => {
    const btn = document.getElementById(def.btn);
    const pane = document.getElementById(def.pane);
    if (btn && pane) {
      if (name === tabName) {
        btn.classList.add('active');
        pane.classList.add('active');
        pane.style.display = 'block';
      } else {
        btn.classList.remove('active');
        pane.classList.remove('active');
        pane.style.display = 'none';
      }
    }
  });
}

// Chargement du Catalogue et des Droits d'Accès du profil avec Rendu Graphique, Packs & Coches Cliquables
async function loadProfileCatalogAccess(profileId) {
  const pid = profileId || state.activeProfileId;
  if (!pid) return;

  try {
    const res = await fetch(`${API_BASE}/api/profiles/${pid}/catalog-access`);
    if (!res.ok) throw new Error('Erreur lors du chargement du catalogue');
    const data = await res.json();

    const packs = data.packs || [];
    const classes = data.classes || [];
    const catalog = data.catalog || data.thematiques || [];

    // Calculs synthétiques pour les cartes KPI
    let totalQuestions = 0;
    let allowedQuestions = 0;
    classes.forEach(cl => {
      totalQuestions += (cl.count || 0);
      if (cl.has_access) {
        allowedQuestions += (cl.count || 0);
      }
    });
    const accessPct = totalQuestions > 0 ? Math.round((allowedQuestions / totalQuestions) * 100) : 0;
    const allowedClassesCount = classes.filter(cl => cl.has_access).length;
    const totalClassesCount = classes.length;

    let totalSubjects = 0;
    let allowedSubjects = 0;
    catalog.forEach(th => {
      (th.sujets || []).forEach(s => {
        totalSubjects++;
        if (s.has_access) allowedSubjects++;
      });
    });

    // Calcul du total des questions répondues pour les KPI
    let totalAnswered = classes.reduce((sum, cl) => sum + (cl.answered_count || 0), 0);

    // Mise à jour des cartes KPI
    const kpiRate = document.getElementById('ckpKpiAccessRate');
    const kpiClasses = document.getElementById('ckpKpiClassesCount');
    const kpiAnswers = document.getElementById('ckpKpiAnswersCount');
    const badgeCatalog = document.getElementById('badgeCountCatalog');

    if (kpiRate) kpiRate.textContent = `${accessPct}%`;
    if (kpiClasses) kpiClasses.textContent = `${allowedClassesCount} / ${totalClassesCount}`;
    if (kpiAnswers) kpiAnswers.textContent = `${totalAnswered} / ${totalQuestions}`;
    if (badgeCatalog) badgeCatalog.textContent = `${accessPct}%`;

    state.currentClasses = classes;
    state.currentPacks = packs;
    state.currentCatalog = catalog;

    // 1. Rendu graphique des Jeux de questions (Packs) avec Retirer, Demander ou En cours
    const packsContainer = document.getElementById('ckpPacksChips');
    if (packsContainer && packs.length > 0) {
      packsContainer.innerHTML = packs.map(pk => {
        const safeNom = (pk.nom || `Jeu #${pk.id}`).replace(/'/g, "\\'");
        
        let actionBtnHtml = '';
        let cardClass = pk.has_access ? 'is-allowed' : 'is-locked';
        let badgeIcon = pk.has_access ? '<div class="ckp-badge-check" title="Accès validé">✓</div>' : '<div class="ckp-badge-lock" title="Jeu verrouillé">🔒</div>';
        let statusSub = pk.has_access ? `${pk.count} questions &bull; Débloqué` : `${pk.count} questions &bull; Bloqué`;

        if (pk.has_pending) {
          actionBtnHtml = `
            <button type="button" class="btn-ckp-pending" onclick="event.stopPropagation(); showToast('⏳ Une demande est en cours d\\'examen par l\\'administrateur pour ce jeu.')" title="Demande en cours auprès de l'administrateur">
              ⏳ En cours
            </button>
          `;
          statusSub = `${pk.count} questions &bull; <span style="color:#FBBF24;">Demande en cours</span>`;
        } else if (pk.has_access) {
          actionBtnHtml = `
            <button type="button" class="btn-ckp-revoke" onclick="event.stopPropagation(); togglePackAccessPrompt(${pid}, ${pk.id}, '${safeNom}', true)" title="Demander le retrait de l'accès">
              Retirer
            </button>
          `;
        } else {
          actionBtnHtml = `
            <button type="button" class="btn-ckp-unlock" onclick="event.stopPropagation(); togglePackAccessPrompt(${pid}, ${pk.id}, '${safeNom}', false)" title="Demander l'accès à l'administrateur">
              Demander
            </button>
          `;
        }

        return `
          <div class="ckp-pack-card ${cardClass}" title="Jeu : ${pk.nom}">
            ${badgeIcon}
            <div class="ckp-class-info">
              <div class="ckp-class-title">${pk.nom} (${pk.code || 'PACK'})</div>
              <div class="ckp-class-sub">${statusSub}</div>
            </div>
            ${actionBtnHtml}
          </div>
        `;
      }).join('');
    }

    // 2. Rendu graphique des Niveaux & Classes : Clic carte -> Consultation Thématiques (sans action), Boutons Retirer / Demander / En cours
    // Règle ARP001 : Ne pas faire apparaître Classe 8 (accessible via + sur moi) et griser Classe 1 (toujours accordée, non retirable)
    const classesContainer = document.getElementById('ckpClassesChips');
    const displayClasses = (classes || []).filter(cl => cl.classe !== 8);
    if (classesContainer && displayClasses.length > 0) {
      classesContainer.innerHTML = displayClasses.map(cl => {
        const safeLabel = (cl.nom || cl.label || `Classe ${cl.classe}`).replace(/'/g, "\\'");
        const answeredCnt = cl.answered_count || 0;
        const totalCnt = cl.count || 0;
        const completionPct = totalCnt > 0 ? Math.round((answeredCnt / totalCnt) * 100) : 0;

        let actionBtnHtml = '';
        let cardClass = cl.has_access ? 'is-allowed' : 'is-locked';
        let badgeIcon = cl.has_access ? '<div class="ckp-badge-check" title="Accès validé">✓</div>' : '<div class="ckp-badge-lock" title="Classe verrouillée">🔒</div>';
        let statusSub = `${answeredCnt}/${totalCnt} répondues (${completionPct}%)`;

        // Règle spécifique : Classe 1 - Standards est grisée car on ne peut la retirer et est toujours accordée
        if (cl.classe === 1) {
          cardClass = 'is-allowed is-standard-locked';
          actionBtnHtml = `
            <span class="badge-fixed-standard" title="La Classe 1 - Standards est le socle permanent commun, toujours accordée et non retirable">
              Accordée
            </span>
          `;
        } else if (cl.has_pending) {
          actionBtnHtml = `
            <button type="button" class="btn-ckp-pending" onclick="event.stopPropagation(); showToast('⏳ Une demande est en cours d\\'examen par l\\'administrateur pour cette classe.')" title="Demande en cours auprès de l'administrateur">
              ⏳ En cours
            </button>
          `;
        } else if (cl.has_access) {
          actionBtnHtml = `
            <button type="button" class="btn-ckp-revoke" onclick="event.stopPropagation(); toggleClassAccessPrompt(${pid}, ${cl.classe}, '${safeLabel}', true)" title="Demander le retrait de l'accès">
              Retirer
            </button>
          `;
        } else {
          actionBtnHtml = `
            <button type="button" class="btn-ckp-unlock" onclick="event.stopPropagation(); toggleClassAccessPrompt(${pid}, ${cl.classe}, '${safeLabel}', false)" title="Demander l'accès à l'administrateur">
              Demander
            </button>
          `;
        }

        const cardTitle = cl.classe === 1
          ? 'Classe 1 - Standards (toujours accordée) : cliquez pour afficher les thématiques'
          : 'Cliquez pour afficher les thématiques et les questions répondues pour cette classe';

        return `
          <div class="ckp-class-card ${cardClass}" onclick="openClasseDetailModal(${cl.classe})" title="${cardTitle}">
            ${badgeIcon}
            <div class="ckp-class-info">
              <div class="ckp-class-title">${cl.nom || cl.label}</div>
              <div class="ckp-class-sub">${statusSub} &bull; <span style="text-decoration:underline; opacity:0.85;">Voir thématiques</span></div>
            </div>
            ${actionBtnHtml}
          </div>
        `;
      }).join('');
    }
  } catch (err) {
    console.error('Erreur chargement catalogue profil:', err);
  }
}

// Modale informative pour un Niveau & Classe de questions (CONSULTATION PURE SANS ACTION)
function openClasseDetailModal(classNum) {
  const classes = state.currentClasses || [];
  const cl = classes.find(c => c.classe === classNum);
  if (!cl) return;

  const titleEl = document.getElementById('mclClasseTitle');
  const badgeEl = document.getElementById('mclClasseStatusBadge');
  const totalEl = document.getElementById('mclTotalQuestions');
  const answeredEl = document.getElementById('mclAnsweredQuestions');
  const pctEl = document.getElementById('mclCompletionPct');
  const listEl = document.getElementById('mclThemesList');

  const total = cl.count || 0;
  const answered = cl.answered_count || 0;
  const pct = total > 0 ? Math.round((answered / total) * 100) : 0;

  if (titleEl) titleEl.textContent = cl.nom || `Classe ${cl.classe}`;

  if (badgeEl) {
    if (cl.has_pending) {
      badgeEl.className = 'badge-tag';
      badgeEl.style.background = 'rgba(245, 158, 11, 0.2)';
      badgeEl.style.color = '#FBBF24';
      badgeEl.textContent = '⏳ Demande en cours';
    } else if (cl.has_access) {
      badgeEl.className = 'badge-tag status-dot success';
      badgeEl.style.background = 'rgba(16, 185, 129, 0.2)';
      badgeEl.style.color = '#34D399';
      badgeEl.textContent = '✓ Accès Actif';
    } else {
      badgeEl.className = 'badge-tag';
      badgeEl.style.background = 'rgba(239, 68, 68, 0.2)';
      badgeEl.style.color = '#F87171';
      badgeEl.textContent = '🔒 Verrouillée';
    }
  }

  if (totalEl) totalEl.textContent = total;
  if (answeredEl) answeredEl.textContent = answered;
  if (pctEl) pctEl.textContent = `${pct}%`;

  if (listEl) {
    const themas = cl.thematiques || [];
    if (themas.length === 0) {
      listEl.innerHTML = '<div class="empty-requests-msg">Aucune thématique recensée dans cette classe.</div>';
    } else {
      listEl.innerHTML = themas.map(th => {
        const thTot = th.total || 0;
        const thAns = th.answered || 0;
        const thPct = thTot > 0 ? Math.round((thAns / thTot) * 100) : 0;

        return `
          <div class="mcl-theme-row">
            <div class="mcl-tr-left">
              <span class="ckp-trc-icon">📁</span>
              <div>
                <strong style="font-size:13px; color:var(--text-main);">${th.thematique}</strong>
                <div style="font-size:11px; color:var(--text-dim); margin-top:2px;">
                  ${thAns} sur ${thTot} questions répondues (${thPct}%)
                </div>
              </div>
            </div>
            <div class="mcl-tr-right">
              <div class="ckp-progress-track" style="width: 100px; margin-bottom: 0;">
                <div class="ckp-progress-bar" style="width: ${thPct}%;"></div>
              </div>
              <span style="font-size:12px; font-weight:700; color:${thAns === thTot && thTot > 0 ? '#34D399' : 'var(--text-main)'}; min-width:38px; text-align:right;">
                ${thPct}%
              </span>
            </div>
          </div>
        `;
      }).join('');
    }
  }

  const modal = document.getElementById('modalClasseDetail');
  if (modal) modal.style.display = 'flex';
}

// Helpers interactifs pour confirmer et transmettre les demandes d'octroi ou de retrait
function togglePackAccessPrompt(profileId, packId, packName, hasAccess) {
  const actionType = hasAccess ? 'revoke' : 'grant';
  const actionLabel = hasAccess ? 'la suppression / le retrait de l\'accès' : 'l\'ouverture / l\'accès';
  const confirmMsg = `Souhaitez-vous envoyer une demande à l'administrateur pour ${actionLabel} au jeu de questions « ${packName} » ?`;
  
  if (!confirm(confirmMsg)) return;
  sendAdminAccessRequest('pack', packId, actionType, `Jeu « ${packName} »`);
}

function toggleClassAccessPrompt(profileId, classNum, className, hasAccess) {
  const actionType = hasAccess ? 'revoke' : 'grant';
  const actionLabel = hasAccess ? 'la suppression / le retrait de l\'accès' : 'l\'ouverture / l\'accès';
  const confirmMsg = `Souhaitez-vous envoyer une demande à l'administrateur pour ${actionLabel} à la classe « ${className} » ?`;
  
  if (!confirm(confirmMsg)) return;
  sendAdminAccessRequest('classe', classNum, actionType, className);
}

function toggleSubjectAccessPrompt(profileId, themeName, subjectName, hasAccess) {
  const actionType = hasAccess ? 'revoke' : 'grant';
  const actionLabel = hasAccess ? 'la suppression / le retrait de l\'accès' : 'l\'ouverture / l\'accès';
  const fullName = `${themeName} - ${subjectName}`;
  const confirmMsg = `Souhaitez-vous envoyer une demande à l'administrateur pour ${actionLabel} au sujet « ${fullName} » ?`;
  
  if (!confirm(confirmMsg)) return;
  sendAdminAccessRequest('thematique', fullName, actionType, fullName);
}

// Ouverture de la modale détaillée d'une thématique
function openThematiqueDetailModal(thematiqueName) {
  const pid = state.activeProfileId;
  const catalog = state.currentCatalog || [];
  const theme = catalog.find(t => t.thematique === thematiqueName);
  const safeThema = thematiqueName.replace(/'/g, "\\'");

  const elTitle = document.getElementById('mthThematiqueTitle');
  const elBadge = document.getElementById('mthCoverageBadge');
  const elGrid = document.getElementById('mthSubjectsGrid');
  const btnGo = document.getElementById('mthBtnGoAnswer');
  const btnGoFooter = document.getElementById('mthBtnGoAnswerFooter');

  if (elTitle) elTitle.textContent = thematiqueName;

  if (theme) {
    const sujets = theme.sujets || [];
    const allowed = sujets.filter(s => s.has_access).length;
    const total = sujets.length;
    const pct = total > 0 ? Math.round((allowed / total) * 100) : 0;
    if (elBadge) {
      elBadge.className = `badge-tag ${pct === 100 ? 'status-dot success' : ''}`;
      elBadge.textContent = `${allowed} / ${total} sujets autorisés (${pct}%)`;
    }

    if (elGrid) {
      if (sujets.length === 0) {
        elGrid.innerHTML = '<div class="empty-requests-msg">Aucun sujet recensé dans cette thématique.</div>';
      } else {
        elGrid.innerHTML = sujets.map(s => {
          const safeSujet = s.sujet.replace(/'/g, "\\'");
          const sTot = s.total_questions || 0;
          const sAns = s.answered_questions || 0;
          const sPct = sTot > 0 ? Math.round((sAns / sTot) * 100) : 0;

          let btnHtml = '';
          if (s.has_pending) {
            btnHtml = `
              <button type="button" class="btn-ckp-pending" onclick="event.stopPropagation(); showToast('⏳ Une demande est déjà en cours d\\'examen par l\\'administrateur pour ce sujet.')" title="Demande en cours auprès de l'administrateur">
                ⏳ En cours
              </button>
            `;
          } else if (s.has_access) {
            btnHtml = `
              <button type="button" class="btn-ckp-revoke" onclick="event.stopPropagation(); toggleSubjectAccessPrompt(${pid}, '${safeThema}', '${safeSujet}', true)" title="Demander le retrait de l'accès">
                Retirer
              </button>
            `;
          } else {
            btnHtml = `
              <button type="button" class="btn-ckp-unlock" onclick="event.stopPropagation(); toggleSubjectAccessPrompt(${pid}, '${safeThema}', '${safeSujet}', false)" title="Demander l'accès à l'administrateur">
                Demander
              </button>
            `;
          }

          if (s.has_access) {
            return `
              <div class="mth-subject-card is-allowed" title="Sujet : ${s.sujet}">
                <div class="mth-subj-left">
                  <span class="ckp-mini-check">✓</span>
                  <div>
                    <div class="mth-subj-title">${s.sujet}</div>
                    <div class="mth-subj-classe">${s.classe_label || 'Classe ' + s.classe} &bull; ${sAns}/${sTot} questions répondues (${sPct}%) &bull; <span style="color:#34D399;">Accès actif</span></div>
                  </div>
                </div>
                ${btnHtml}
              </div>
            `;
          } else {
            return `
              <div class="mth-subject-card is-locked" title="Sujet : ${s.sujet}">
                <div class="mth-subj-left">
                  <span class="ckp-mini-lock">🔒</span>
                  <div>
                    <div class="mth-subj-title">${s.sujet}</div>
                    <div class="mth-subj-classe">${s.classe_label || 'Classe ' + s.classe} &bull; ${sAns}/${sTot} questions &bull; <span style="color:${s.has_pending ? '#FBBF24' : 'var(--accent-pink)'};">${s.has_pending ? 'Demande en cours' : 'Verrouillé'}</span></div>
                  </div>
                </div>
                ${btnHtml}
              </div>
            `;
          }
        }).join('');
      }
    }
  }

  // Brancher les boutons d'action vers le questionnaire
  const goAction = () => goToQuestionnaireThematique(thematiqueName);
  if (btnGo) btnGo.onclick = goAction;
  if (btnGoFooter) btnGoFooter.onclick = goAction;

  const modal = document.getElementById('modalThematiqueDetail');
  if (modal) modal.style.display = 'flex';
}

// Débranchement direct vers l'onglet Questionnaire avec filtrage sur la thématique
function goToQuestionnaireThematique(thematiqueName) {
  closeModals();
  switchTab('questionnaire');
  
  // Appliquer le filtre thématique dans le questionnaire
  const selThema = document.getElementById('qFilterThematique');
  if (selThema) {
    // Vérifier si l'option existe, sinon la créer
    const exists = Array.from(selThema.options).some(o => o.value === thematiqueName);
    if (!exists && thematiqueName !== 'ALL') {
      const opt = document.createElement('option');
      opt.value = thematiqueName;
      opt.textContent = thematiqueName;
      selThema.appendChild(opt);
    }
    selThema.value = thematiqueName;
  }

  renderQuestionsDeck();
  showToast(`✍️ Thématique « <strong>${thematiqueName}</strong> » sélectionnée pour la saisie !`);

  // Scroll doux vers le haut des questions
  const deck = document.getElementById('questionsDeck');
  if (deck) deck.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Envoi d'une demande d'accès ou de retrait à l'administrateur
async function sendAdminAccessRequest(targetType, targetValue, actionType = 'grant', displayLabel = '') {
  const p = getActiveProfile();
  if (!p) return;

  const typeDesc = displayLabel || (targetType === 'classe' ? `la Classe ${targetValue}` : `l'élément "${targetValue}"`);
  const isRevoke = (actionType === 'revoke');

  try {
    const res = await fetch(`${API_BASE}/api/access-requests`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        profile_id: p.id,
        target_type: targetType,
        target_value: String(targetValue),
        action_type: actionType
      })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erreur lors de l\'envoi');
    
    if (isRevoke) {
      showToast(`Demande de <strong>retrait</strong> transmise à l'administrateur pour ${typeDesc}.`);
    } else {
      showToast(`Demande d'<strong>accès</strong> transmise à l'administrateur pour ${typeDesc} !`);
    }
    
    loadProfileAdminRequests(p.id);
    loadProfileCatalogAccess(p.id);
  } catch (err) {
    alert(err.message);
  }
}

// Chargement des demandes d'accès envoyées à l'administrateur
async function loadProfileAdminRequests(profileId) {
  const pid = profileId || state.activeProfileId;
  if (!pid) return;

  try {
    const res = await fetch(`${API_BASE}/api/profiles/${pid}/access-requests`);
    if (!res.ok) return;
    const data = await res.json();
    const reqs = data.requests || [];

    const pendingCount = reqs.filter(r => r.status === 'pending').length;
    const badge = document.getElementById('badgeCountAdminRequests');
    if (badge) badge.textContent = pendingCount;

    const container = document.getElementById('ckpAdminRequestsList');
    if (!container) return;

    if (reqs.length === 0) {
      container.innerHTML = `
        <div class="empty-requests-msg">
          ✉️ Vous n'avez envoyé aucune demande d'accès à l'administrateur.<br>
          <span style="font-size:11.5px; opacity:0.8;">Utilisez le bouton "Demander" dans l'onglet Catalogue pour solliciter l'ouverture de nouvelles classes ou thématiques.</span>
        </div>
      `;
      return;
    }

    container.innerHTML = reqs.map(r => {
      const isRevoke = (r.action_type === 'revoke');
      let statusBadge = '';
      if (r.status === 'pending') {
        statusBadge = '<span class="req-status-badge pending">⏳ En attente de validation</span>';
      } else if (r.status === 'approved') {
        statusBadge = isRevoke 
          ? '<span class="req-status-badge approved">✅ Retrait effectué</span>' 
          : '<span class="req-status-badge approved">✅ Accès Accordé</span>';
      } else {
        statusBadge = '<span class="req-status-badge rejected">❌ Refusé</span>';
      }

      const actionBadge = isRevoke
        ? '<span class="req-action-badge revoke">➖ Retrait</span>'
        : '<span class="req-action-badge grant">➕ Accès</span>';

      const targetTypeLabel = r.target_type === 'classe' ? '🏷️ Classe' : (r.target_type === 'pack' ? '📦 Jeu' : '📁 Domaine');
      const dateStr = r.created_at ? new Date(r.created_at).toLocaleString('fr-FR') : '';

      return `
        <div class="ckp-request-card">
          <div class="req-header">
            <div class="req-title" style="display:flex; align-items:center; gap:8px;">
              ${actionBadge}
              <span><strong>${targetTypeLabel}</strong> : ${r.target_value}</span>
            </div>
            ${statusBadge}
          </div>
          <div class="req-meta">
            <span>Envoyée le : ${dateStr}</span>
            ${r.responded_at ? `<span>Traité le : ${new Date(r.responded_at).toLocaleString('fr-FR')}</span>` : ''}
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error('Erreur chargement demandes admin:', err);
  }
}

// Chargement compact des Matchs pour l'Abonné dans son cockpit
async function loadProfileCockpitMatches(profileId) {
  const pid = profileId || state.activeProfileId;
  if (!pid) return;

  try {
    const res = await fetch(`${API_BASE}/api/profiles/${pid}/match-requests`);
    if (!res.ok) return;
    const data = await res.json();

    const received = data.received || [];
    const sent = data.sent || [];
    const pendingReceived = received.filter(r => r.status === 'pending');

    const badge = document.getElementById('badgeCountMyMatches');
    if (badge) badge.textContent = pendingReceived.length;

    const container = document.getElementById('ckpMyMatchesList');
    if (!container) return;

    if (received.length === 0 && sent.length === 0) {
      container.innerHTML = `
        <div class="empty-requests-msg">
          💌 Aucune demande de match pour le moment.<br>
          <span style="font-size:11.5px; opacity:0.8;">Rendez-vous dans l'onglet <strong>Demande de Match</strong> pour solliciter un autre abonné.</span>
        </div>
      `;
      return;
    }

    let html = '';
    if (received.length > 0) {
      html += '<div class="ckp-section-title" style="margin-top:0;">Demandes Reçues</div>';
      html += received.map(req => {
        const isPending = req.status === 'pending';
        const senderPseudo = req.sender_pseudo || `Membre #${req.sender_id}`;
        const affId = formatAffId(req.sender_id);
        return `
          <div class="ckp-request-card">
            <div class="req-header">
              <div class="req-title">
                <strong>${senderPseudo}</strong> (${affId})
              </div>
              <span class="req-status-badge ${req.status}">
                ${req.status === 'pending' ? '⏳ Reçue' : (req.status === 'accepted' ? '✅ Acceptée' : '❌ Refusée')}
              </span>
            </div>
            ${isPending ? `
              <div style="display:flex; gap:8px; margin-top:10px;">
                <button class="btn btn-xs btn-primary" onclick="respondMatchRequestAction(${req.id}, 'accept')">
                  Accepter
                </button>
                <button class="btn btn-xs btn-outline" onclick="respondMatchRequestAction(${req.id}, 'reject')">
                  Refuser
                </button>
              </div>
            ` : (req.status === 'accepted' ? `
              <div style="margin-top:8px;">
                <button class="btn btn-xs btn-outline" onclick="viewAcceptedMatchResult(${JSON.stringify(req.affinity_result).replace(/"/g, '&quot;')})">
                  📊 Voir le résultat
                </button>
              </div>
            ` : '')}
          </div>
        `;
      }).join('');
    }

    if (sent.length > 0) {
      html += '<div class="ckp-section-title" style="margin-top:16px;">Demandes Envoyées</div>';
      html += sent.map(req => {
        const targetPseudo = req.target_pseudo || `Membre #${req.target_id}`;
        const affId = formatAffId(req.target_id);
        return `
          <div class="ckp-request-card">
            <div class="req-header">
              <div class="req-title">
                Vers <strong>${targetPseudo}</strong> (${affId})
              </div>
              <span class="req-status-badge ${req.status}">
                ${req.status === 'pending' ? '⏳ En attente' : (req.status === 'accepted' ? '✅ Acceptée' : '❌ Refusée')}
              </span>
            </div>
            ${req.status === 'accepted' && req.affinity_result ? `
              <div style="margin-top:8px;">
                <button class="btn btn-xs btn-outline" onclick="viewAcceptedMatchResult(${JSON.stringify(req.affinity_result).replace(/"/g, '&quot;')})">
                  📊 Voir le résultat
                </button>
              </div>
            ` : ''}
          </div>
        `;
      }).join('');
    }

    container.innerHTML = html;
  } catch (err) {
    console.error('Erreur chargement matchs cockpit:', err);
  }
}

// ==========================================
// GESTION DE L'ADMINISTRATION DES RÔLES
// ==========================================
function renderAdminUsersTable() {
  const tbody = document.getElementById('adminUsersTableBody');
  if (!tbody) return;

  const admins = state.profiles.filter(p => p.role === 'admin').length;
  const subs = state.profiles.filter(p => p.role === 'subscriber').length;
  const guests = state.profiles.filter(p => p.role === 'guest' || !p.role).length;

  const cAdm = document.getElementById('adminCountAdmins');
  const cSub = document.getElementById('adminCountSubscribers');
  const cGst = document.getElementById('adminCountGuests');
  if (cAdm) cAdm.textContent = admins;
  if (cSub) cSub.textContent = subs;
  if (cGst) cGst.textContent = guests;

  if (state.profiles.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align:center; padding:24px;">Aucun profil enregistré.</td></tr>`;
    return;
  }

  tbody.innerHTML = state.profiles.map(p => {
    const role = p.role || 'guest';
    let roleBadgeHtml = '';
    if (role === 'admin') {
      roleBadgeHtml = '<span class="role-badge admin">👑 Administrateur</span>';
    } else if (role === 'subscriber') {
      roleBadgeHtml = '<span class="role-badge subscriber">⭐ Abonné</span>';
    } else {
      roleBadgeHtml = '<span class="role-badge guest">👤 Invité</span>';
    }

    let quickActionBtn = '';
    if (role === 'guest') {
      quickActionBtn = `<button class="btn btn-sm btn-secondary" onclick="changeProfileRole(${p.id}, 'subscriber')" title="Accorder l'accès au calculateur">⭐ Promouvoir Abonné</button>`;
    } else if (role === 'subscriber') {
      quickActionBtn = `<button class="btn btn-sm btn-outline" onclick="changeProfileRole(${p.id}, 'guest')" title="Passer en invité">Rétrograder Invité</button>`;
    } else {
      quickActionBtn = `<span style="font-size:12px; color:var(--text-dim);">Titulaire Admin</span>`;
    }

    // Résumé du périmètre de questionnaires
    let qaSummary = 'Accès Total';
    const qa = p.question_access;
    if (qa && (qa.allowed_packs !== 'ALL' || qa.allowed_classes !== 'ALL' || qa.allowed_types !== 'ALL')) {
      const parts = [];
      if (qa.allowed_packs !== 'ALL') parts.push(`${qa.allowed_packs.length} jeu${qa.allowed_packs.length > 1 ? 'x' : ''}`);
      if (qa.allowed_classes !== 'ALL') parts.push(`${qa.allowed_classes.length} classe${qa.allowed_classes.length > 1 ? 's' : ''}`);
      if (qa.allowed_types !== 'ALL') parts.push(`${qa.allowed_types.length} type${qa.allowed_types.length > 1 ? 's' : ''}`);
      qaSummary = parts.length > 0 ? parts.join(' &bull; ') : 'Aucun accès';
    }

    return `
      <tr>
        <td>#${p.id}</td>
        <td>
          <div style="display:flex; align-items:center; gap:8px;">
            <div class="ap-avatar" style="width:28px; height:28px; font-size:11px;">${p.pseudo.charAt(0).toUpperCase()}</div>
            <strong>${p.pseudo}</strong>
          </div>
        </td>
        <td>${role === 'admin' ? '<span style="color:var(--accent-cyan); font-weight:600;">👑 Non requise (Admin)</span>' : (p.prenom ? `${p.prenom} ${p.nom || ''}` : '<span style="color:var(--text-dim)">Non renseignée</span>')}</td>
        <td>${p.ville || '-'}</td>
        <td>${role === 'admin' ? '<span style="color:var(--text-dim);">- (Non concerné)</span>' : `<strong>${p.answers_count || 0}</strong> / 172`}</td>
        <td>${roleBadgeHtml}</td>
        <td>
          <button class="badge-pqa-btn" onclick="openProfileQuestionAccessModal(${p.id})" title="Gérer les jeux, classes et types pour ce profil">
            <span>⚙️</span> ${qaSummary}
          </button>
        </td>
        <td>
          <select class="role-select" onchange="changeProfileRole(${p.id}, this.value)">
            <option value="guest" ${role === 'guest' ? 'selected' : ''}>👤 Invité</option>
            <option value="subscriber" ${role === 'subscriber' ? 'selected' : ''}>⭐ Abonné</option>
            <option value="admin" ${role === 'admin' ? 'selected' : ''}>👑 Administrateur</option>
          </select>
        </td>
        <td style="text-align:right;">
          <div style="display:flex; justify-content:flex-end; align-items:center; gap:6px;">
            ${quickActionBtn}
            ${p.role !== 'admin' ? `
              <button class="btn btn-xs btn-outline" onclick="testViewAsProfile(${p.id})" title="Tester l'application en tant que ${p.pseudo}" style="border-color:rgba(56,189,248,0.4); color:#38BDF8; display:inline-flex; align-items:center; gap:4px; padding:4px 8px;">
                <span>👁️</span> Tester
              </button>
            ` : ''}
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

async function changeProfileRole(profileId, newRole) {
  try {
    const res = await fetch(`${API_BASE}/api/profiles/${profileId}/role`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: newRole })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erreur lors de la mise à jour du rôle');

    const roleLabels = { 'admin': 'Administrateur', 'subscriber': 'Abonné', 'guest': 'Invité' };
    showToast(`Rôle de l'utilisateur mis à jour : ${roleLabels[newRole] || newRole}`);
    await loadProfiles();
    if (state.activeProfileId === profileId) {
      setActiveProfile(profileId);
    }
    renderAdminUsersTable();
  } catch (err) {
    alert('Erreur : ' + err.message);
  }
}

// ==========================================================================
// GESTION DES DEMANDES D'ACCÈS REÇUES PAR L'ADMINISTRATEUR
// ==========================================================================
async function loadAdminAccessRequests() {
  const tbody = document.getElementById('adminAccessRequestsTableBody');
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/api/admin/access-requests`);
    if (!res.ok) return;
    const data = await res.json();
    const reqs = data.requests || [];

    if (reqs.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:20px; color:var(--text-dim);">Aucune demande d'accès reçue pour le moment.</td></tr>`;
      return;
    }

    tbody.innerHTML = reqs.map(r => {
      const isPending = r.status === 'pending';
      const isRevoke = (r.action_type === 'revoke');
      const role = r.role || 'guest';
      const roleBadge = role === 'admin' 
        ? '<span class="role-badge admin">👑 Admin</span>' 
        : (role === 'subscriber' ? '<span class="role-badge subscriber">⭐ Abonné</span>' : '<span class="role-badge guest">👤 Invité</span>');
      
      const targetLabel = r.target_type === 'classe' ? `Classe ${r.target_value}` : r.target_value;
      const typeBadge = r.target_type === 'classe' ? '🏷️ Classe' : (r.target_type === 'pack' ? '📦 Jeu' : '📁 Domaine');
      const dateStr = r.created_at ? new Date(r.created_at).toLocaleString('fr-FR') : '-';

      const actionBadge = isRevoke
        ? '<span class="req-action-badge revoke">➖ Retrait d\'accès</span>'
        : '<span class="req-action-badge grant">➕ Demande d\'accès</span>';

      let statusBadge = '';
      if (r.status === 'pending') {
        statusBadge = '<span class="req-status-badge pending">⏳ En attente</span>';
      } else if (r.status === 'approved') {
        statusBadge = isRevoke
          ? '<span class="req-status-badge approved">✅ Retiré</span>'
          : '<span class="req-status-badge approved">✅ Accordé</span>';
      } else {
        statusBadge = '<span class="req-status-badge rejected">❌ Refusé</span>';
      }

      let actionsHtml = '';
      if (isPending) {
        if (isRevoke) {
          actionsHtml = `
            <div style="display:flex; justify-content:flex-end; gap:6px;">
              <button class="btn btn-xs btn-outline" style="border-color:#EF4444; color:#F87171;" onclick="respondAdminAccessRequest(${r.id}, 'approved')" title="Valider le retrait de l'accès">
                Retirer
              </button>
              <button class="btn btn-xs btn-outline" onclick="respondAdminAccessRequest(${r.id}, 'rejected')" title="Refuser le retrait">
                Refuser
              </button>
            </div>
          `;
        } else {
          actionsHtml = `
            <div style="display:flex; justify-content:flex-end; gap:6px;">
              <button class="btn btn-xs btn-primary" onclick="respondAdminAccessRequest(${r.id}, 'approved')" title="Accorder immédiatement l'accès">
                Accorder
              </button>
              <button class="btn btn-xs btn-outline" onclick="respondAdminAccessRequest(${r.id}, 'rejected')" title="Refuser la demande">
                Refuser
              </button>
            </div>
          `;
        }
      } else {
        actionsHtml = `<span style="font-size:11.5px; color:var(--text-dim);">${r.responded_at ? new Date(r.responded_at).toLocaleDateString('fr-FR') : 'Traité'}</span>`;
      }

      return `
        <tr>
          <td>${dateStr}</td>
          <td><strong>${r.pseudo}</strong> <span style="font-size:11px; opacity:0.7;">(#${r.profile_id})</span></td>
          <td>${roleBadge}</td>
          <td>${actionBadge}</td>
          <td><strong>${targetLabel}</strong></td>
          <td>${typeBadge}</td>
          <td>${statusBadge}</td>
          <td style="text-align:right;">${actionsHtml}</td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    console.error('Erreur chargement demandes admin:', err);
  }
}

async function respondAdminAccessRequest(requestId, action) {
  try {
    const res = await fetch(`${API_BASE}/api/access-requests/${requestId}/respond`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erreur lors du traitement');
    showToast(action === 'approved' ? 'Demande approuvée avec succès ! Droits mis à jour.' : 'Demande refusée.');
    await loadProfiles();
    loadAdminAccessRequests();
    if (state.activeProfileId) {
      loadProfileCatalogAccess(state.activeProfileId);
      loadProfileAdminRequests(state.activeProfileId);
    }
  } catch (err) {
    alert('Erreur : ' + err.message);
  }
}

// ==========================================================================
// GESTION ADMINISTRATIVE DU PÉRIMÈTRE DE QUESTIONS PAR PROFIL
// ==========================================================================
function openProfileQuestionAccessModal(profileId) {
  const prof = state.profiles.find(p => p.id === profileId);
  if (!prof) return;

  document.getElementById('pqaProfileId').value = prof.id;
  document.getElementById('pqaModalPseudo').textContent = prof.pseudo;

  const badgeEl = document.getElementById('pqaModalProfileBadge');
  if (badgeEl) {
    const role = prof.role || 'guest';
    badgeEl.className = `role-badge ${role}`;
    badgeEl.textContent = role === 'admin' ? '👑 Admin' : (role === 'subscriber' ? '⭐ Abonné' : '👤 Invité');
  }

  const qa = prof.question_access || { allowed_packs: 'ALL', allowed_classes: 'ALL', allowed_types: 'ALL' };

  // 1. Remplissage des Packs
  const packsContainer = document.getElementById('pqaPacksContainer');
  if (packsContainer) {
    if (state.packs.length === 0) {
      packsContainer.innerHTML = '<p class="text-dim-sm">Aucun jeu / pack répertorié.</p>';
    } else {
      const allPacks = qa.allowed_packs === 'ALL';
      const allowedPackIds = Array.isArray(qa.allowed_packs) ? qa.allowed_packs : [];

      packsContainer.innerHTML = state.packs.map(pk => {
        const isChecked = allPacks || allowedPackIds.includes(pk.id);
        const countQ = state.questions.filter(q => q.pack_id === pk.id).length;
        return `
          <label class="pqa-check-item">
            <input type="checkbox" name="pqaPack" value="${pk.id}" ${isChecked ? 'checked' : ''} onchange="updatePqaPreview()">
            <span class="pqa-check-label">
              <strong style="font-size:13px;">${pk.nom}</strong>
              <span class="pqa-desc-mini">${pk.code} &bull; ${countQ} questions</span>
            </span>
          </label>
        `;
      }).join('');
    }
  }

  // 2. Remplissage des Classes
  const allClasses = qa.allowed_classes === 'ALL';
  const allowedClassIds = Array.isArray(qa.allowed_classes) ? qa.allowed_classes : [];
  document.querySelectorAll('input[name="pqaClasse"]').forEach(cb => {
    const val = parseInt(cb.value, 10);
    cb.checked = allClasses || allowedClassIds.includes(val);
  });

  updatePqaPreview();
  document.getElementById('modalProfileQuestionAccess').style.display = 'flex';
}

function pqaSelectAllPacks(selectAll) {
  document.querySelectorAll('input[name="pqaPack"]').forEach(cb => { cb.checked = selectAll; });
  updatePqaPreview();
}

function pqaSelectAllClasses(selectAll) {
  document.querySelectorAll('input[name="pqaClasse"]').forEach(cb => { cb.checked = selectAll; });
  updatePqaPreview();
}

function pqaSelectStandardsOnly() {
  document.querySelectorAll('input[name="pqaClasse"]').forEach(cb => {
    cb.checked = (cb.value === '1');
  });
  updatePqaPreview();
}

function pqaResetDefaultAccess() {
  pqaSelectAllPacks(true);
  pqaSelectAllClasses(true);
  updatePqaPreview();
  showToast('Configuration réinitialisée : Accès Total');
}

function updatePqaPreview() {
  const packCbs = Array.from(document.querySelectorAll('input[name="pqaPack"]'));
  const classeCbs = Array.from(document.querySelectorAll('input[name="pqaClasse"]'));

  const checkedPacks = packCbs.filter(cb => cb.checked).map(cb => parseInt(cb.value, 10));
  const checkedClasses = classeCbs.filter(cb => cb.checked).map(cb => parseInt(cb.value, 10));

  const allPacks = (packCbs.length > 0 && checkedPacks.length === packCbs.length);
  const allClasses = (classeCbs.length > 0 && checkedClasses.length === classeCbs.length);

  // Compter les questions actives éligibles
  const eligibleCount = state.questions.filter(q => {
    const packOk = (packCbs.length === 0) ? true : (allPacks ? true : checkedPacks.includes(q.pack_id));
    const classeOk = allClasses ? true : checkedClasses.includes(q.classe);
    return packOk && classeOk;
  }).length;

  const counterEl = document.getElementById('pqaCounterNumber');
  if (counterEl) counterEl.textContent = eligibleCount;

  const summaryEl = document.getElementById('pqaSummaryText');
  if (summaryEl) {
    if (allPacks && allClasses) {
      summaryEl.innerHTML = '<span style="color:#34D399; font-weight:600;">Accès intégral à toutes les questions de la banque.</span>';
    } else {
      const details = [];
      details.push(`${checkedPacks.length}/${packCbs.length || 1} jeu(x)`);
      details.push(`${checkedClasses.length}/${classeCbs.length} classe(s)`);
      summaryEl.textContent = `Périmètre personnalisé : ${details.join(' • ')}`;
    }
  }
}

async function saveProfileQuestionAccess() {
  const profileId = parseInt(document.getElementById('pqaProfileId').value, 10);
  if (!profileId) return;

  const packCbs = Array.from(document.querySelectorAll('input[name="pqaPack"]'));
  const classeCbs = Array.from(document.querySelectorAll('input[name="pqaClasse"]'));

  const checkedPacks = packCbs.filter(cb => cb.checked).map(cb => parseInt(cb.value, 10));
  const checkedClasses = classeCbs.filter(cb => cb.checked).map(cb => parseInt(cb.value, 10));

  if (checkedPacks.length === 0) {
    alert('Attention : vous devez sélectionner au moins un jeu de questions.');
    return;
  }
  if (checkedClasses.length === 0) {
    alert('Attention : vous devez sélectionner au moins une classe de questions.');
    return;
  }

  const allPacks = (packCbs.length > 0 && checkedPacks.length === packCbs.length);
  const allClasses = (classeCbs.length > 0 && checkedClasses.length === classeCbs.length);

  const payload = {
    allowed_packs: allPacks ? 'ALL' : checkedPacks,
    allowed_classes: allClasses ? 'ALL' : checkedClasses,
    allowed_types: 'ALL'
  };

  try {
    const res = await fetch(`${API_BASE}/api/profiles/${profileId}/question-access`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erreur lors de l\'enregistrement');

    const prof = state.profiles.find(p => p.id === profileId);
    showToast(`✨ Périmètre de questionnaires mis à jour pour ${prof ? prof.pseudo : '#' + profileId} !`);
    closeModals();
    await loadProfiles();

    if (state.activeProfileId === profileId) {
      renderQuestionsDeck();
      updateProgressBar();
  updateIdentityCompletionBadge();
    }
    renderAdminUsersTable();
  } catch (err) {
    alert('Erreur : ' + err.message);
  }
}

function renderDashboardProfiles() {
  const list = document.getElementById('dashboardProfilesList');
  if (!list) return;
  if (state.profiles.length === 0) {
    list.innerHTML = '<div class="empty-state-mini"><p>Aucun profil créé.</p></div>';
    return;
  }
  list.innerHTML = state.profiles.slice(0, 4).map(p => `
    <div class="profile-compact-item" style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid var(--border-subtle);">
      <div style="display:flex; align-items:center; gap:10px;">
        <div class="ap-avatar" style="width:30px; height:30px; font-size:12px;">${p.pseudo.charAt(0).toUpperCase()}</div>
        <div>
          <div style="font-size:13.5px; font-weight:600;">${p.pseudo}</div>
          <div style="font-size:11px; color:var(--text-dim);">${p.prenom ? `${p.prenom} (${p.ville || 'France'})` : 'Profil à compléter'}</div>
        </div>
      </div>
      <div>
        <button class="btn btn-sm btn-outline" onclick="selectAndGoToQuestionnaire(${p.id})">Saisir</button>
      </div>
    </div>
  `).join('');
}

function selectAndGoToQuestionnaire(id) {
  setActiveProfile(id);
  switchTab('questionnaire');
}

async function deleteProfileConfirm(id, pseudo) {
  if (!isCurrentAdmin() && id !== state.activeProfileId) {
    alert('Seul un administrateur peut supprimer les profils d\'autres membres.');
    return;
  }
  if (confirm(`Confirmez-vous la suppression du profil "${pseudo}" et de toutes ses réponses ?`)) {
    try {
      const res = await fetch(`${API_BASE}/api/profiles/${id}`, { method: 'DELETE' });
      if (res.ok) {
        showToast(`Profil "${pseudo}" supprimé.`);
        await loadProfiles();
        if (state.activeProfileId === id) {
          state.activeProfileId = state.profiles[0]?.id || null;
          updateActiveProfileWidget();
        }
      }
    } catch (err) {
      alert('Erreur suppression : ' + err.message);
    }
  }
}

// Modal Profil
async function openIdentityCardModal(profileId) {
  const prof = state.profiles.find(p => p.id === profileId);
  document.getElementById('idProfileId').value = profileId;
  document.getElementById('modalIdTitle').textContent = `Profil de ${prof?.pseudo || 'ce membre'}`;

  // Remplir pseudo, email et ID calculé
  const elPseudo = document.getElementById('idPseudo');
  if (elPseudo) elPseudo.value = prof?.pseudo || '';
  const elEmail = document.getElementById('idEmail');
  if (elEmail) elEmail.value = prof?.email || '';
  const elAff = document.getElementById('idAffDisplay');
  if (elAff) elAff.value = formatAffId(profileId);

  // Charger les données existantes
  try {
    const res = await fetch(`${API_BASE}/api/profiles/${profileId}/identity`);
    const card = await res.json();
    document.getElementById('idPrenom').value = card.prenom || '';
    document.getElementById('idNom').value = card.nom || '';
    document.getElementById('idSexe').value = card.sexe ?? 0;
    const modBirth = document.getElementById('idDateNaiss');
    if (modBirth) {
      modBirth.value = card.date_naissance || '';
      updateDateInputAgeFeedback(modBirth, document.getElementById('modalAgeBadge'), document.getElementById('modalAgeFeedback'));
    }
    const mPaysNaiss = document.getElementById('idPaysNaissance');
    const mHabPays = document.getElementById('idHabitePays');
    const mHabReg = document.getElementById('idHabiteRegion');
    const mHabCom = document.getElementById('idHabiteCommune');

    if (mPaysNaiss) {
      let pNaiss = card.pays_naissance || '';
      if (pNaiss && !['France', 'UE', 'Hors UE'].includes(pNaiss)) pNaiss = 'France';
      mPaysNaiss.value = pNaiss;
    }
    const curHPays = card.habite_pays || (card.habite_commune || card.ville ? 'France' : 'France');
    if (mHabPays) mHabPays.value = (curHPays === 'France' || curHPays === 'UE' || curHPays === 'Hors UE') ? curHPays : 'France';
    if (mHabReg) mHabReg.value = card.habite_region_dept || '';
    if (mHabCom) mHabCom.value = card.habite_commune || card.ville || '';
    const mCity = document.getElementById('idVille');
    if (mCity) mCity.value = card.habite_commune || card.ville || '';
    updateIdentityCompletionBadge();
    document.getElementById('idStatut').value = card.statut || '';
    
    // Champs Morphologie & Mensurations
    const elTaille = document.getElementById('idTaille');
    if (elTaille) elTaille.value = card.taille ?? '';
    const elPoids = document.getElementById('idPoids');
    if (elPoids) elPoids.value = card.poids ?? '';
    const elPointure = document.getElementById('idPointure');
    if (elPointure) elPointure.value = card.pointure ?? '';

    let cTp = card.tour_poitrine ?? '';
    let cTt = card.tour_taille ?? '';
    let cTh = card.tour_hanches ?? '';
    if ((!cTp && !cTt && !cTh) && card.mensurations && card.mensurations.includes('-')) {
      const parts = card.mensurations.split('-');
      if (parts[0] && parts[0] !== '-') cTp = parts[0];
      if (parts[1] && parts[1] !== '-') cTt = parts[1];
      if (parts[2] && parts[2] !== '-') cTh = parts[2];
    }
    const elPoitrine = document.getElementById('idPoitrine');
    if (elPoitrine) elPoitrine.value = cTp;
    const elTailleTour = document.getElementById('idTailleTour');
    if (elTailleTour) elTailleTour.value = cTt;
    const elHanches = document.getElementById('idHanches');
    if (elHanches) elHanches.value = cTh;
    const elMens = document.getElementById('idMensurations');
    if (elMens) elMens.value = card.mensurations || '';

    // Champs Allure, Style & Origines
    const elOrig = document.getElementById('idOrigines');
    if (elOrig) elOrig.value = card.origines || '';
    const elCheveux = document.getElementById('idCouleurCheveux');
    if (elCheveux) elCheveux.value = card.couleur_cheveux || '';
    const elStyle = document.getElementById('idStyle');
    if (elStyle) elStyle.value = card.style || '';

    document.getElementById('idBio').value = card.bio || '';
    const elAime = document.getElementById('idAimeChezMoi');
    if (elAime) elAime.value = card.aime_chez_moi || '';
    const elAimePas = document.getElementById('idAimePasChezMoi');
    if (elAimePas) elAimePas.value = card.aime_pas_chez_moi || '';
  } catch (err) {
    console.error(err);
  }

  const fId = document.getElementById('formIdentityCard');
  if (fId) fId.scrollTop = 0;
  document.getElementById('modalIdentityCard').style.display = 'flex';
}

function openCreateProfileModal() {
  document.getElementById('inputPseudo').value = '';
  document.getElementById('modalCreateProfile').style.display = 'flex';
}

function closeModals() {
  document.querySelectorAll('.modal-backdrop').forEach(m => m.style.display = 'none');
}

// Questions & Packs
async function loadPacks() {
  try {
    const res = await fetch(`${API_BASE}/api/packs`);
    const data = await res.json();
    state.packs = data.packs || [];
    const filter = document.getElementById('qFilterPack');
    if (filter) {
      filter.innerHTML = `<option value="ALL">Tous les jeux / domaines</option>` +
        state.packs.map(pk => `<option value="${pk.id}">${pk.nom}</option>`).join('');
    }
  } catch (err) {
    console.error(err);
  }
}

async function loadQuestions() {
  try {
    const res = await fetch(`${API_BASE}/api/questions`);
    const data = await res.json();
    state.questions = data.questions || [];
    populateBankFilters();
    renderQuestionsTable();
    updateQuestionnaireFilters();
    renderQuestionsDeck();
    const activeBadge = document.getElementById('badgeActiveQuestionsCount');
    if (activeBadge) activeBadge.textContent = state.questions.length;
    updateStatsDisplay();
    updateIdentityCompletionBadge();
  } catch (err) {
    console.error(err);
  }
}

async function loadActiveProfileAnswers() {
  if (!state.activeProfileId) return;
  try {
    const res = await fetch(`${API_BASE}/api/profiles/${state.activeProfileId}/answers`);
    const data = await res.json();
    state.answersMap = {};
    (data.answers || []).forEach(ans => {
      state.answersMap[`${ans.question_id}_${ans.axis}`] = ans.value;
    });
    renderQuestionsDeck();
    updateProgressBar();
  updateIdentityCompletionBadge();
  } catch (err) {
    console.error(err);
  }
}

function getActiveProfileEligibleQuestions() {
  if (!state.activeProfileId) return state.questions;
  const prof = state.profiles.find(p => p.id === state.activeProfileId);
  if (!prof) return state.questions;

  // L'administrateur en mode superviseur a accès à l'ensemble des questions (hors classe 8 Identité)
  if (prof.role === 'admin') {
    return state.questions.filter(q => q.classe !== 8 && q.classe !== '8' && q.type !== 'P' && q.type !== 'T');
  }

  if (!prof.question_access) return state.questions;

  const qa = prof.question_access;
  const allPacks = qa.allowed_packs === 'ALL';
  const allowedPackIds = Array.isArray(qa.allowed_packs) ? qa.allowed_packs : [];

  const allClasses = qa.allowed_classes === 'ALL';
  const allowedClassIds = Array.isArray(qa.allowed_classes) ? qa.allowed_classes : [];

  const allTypes = qa.allowed_types === 'ALL';
  const allowedTypeVals = Array.isArray(qa.allowed_types) ? qa.allowed_types : [];

  return state.questions.filter(q => {
    // Règle stricte : les questions de classe 8 (Identité) se renseignent uniquement dans '+ sur vous' et '+ sur l'autre'
    if (q.classe === 8 || q.classe === '8' || q.type === 'P' || q.type === 'T') return false;

    // Prise en compte stricte de N_CIBLE selon le sexe du profil actif (0: mixte/tous, 1: homme, 2: femme)
    const profSexe = prof.sexe ?? 0;
    if (profSexe === 1 && q.cible === 2) return false; // Un profil Homme ne reçoit pas les questions réservées aux Femmes
    if (profSexe === 2 && q.cible === 1) return false; // Un profil Femme ne reçoit pas les questions réservées aux Hommes

    const pkOk = allPacks || allowedPackIds.includes(q.pack_id);
    const clOk = allClasses || allowedClassIds.map(String).includes(String(q.classe));
    const tyOk = allTypes || allowedTypeVals.includes(q.type);
    return pkOk && clOk && tyOk;
  });
}

function updateProgressBar() {
  const eligible = getActiveProfileEligibleQuestions();
  const eligibleIds = new Set(eligible.map(q => q.id));

  const answeredQids = new Set();
  Object.keys(state.answersMap).forEach(k => {
    const qid = parseInt(k.split('_')[0], 10);
    if (eligibleIds.has(qid)) {
      answeredQids.add(qid);
    }
  });

  const total = eligible.length;
  const answered = answeredQids.size;
  const pct = total > 0 ? Math.round((answered / total) * 100) : 0;
  document.getElementById('qProgressPct').textContent = `${pct}% (${answered}/${total})`;
  document.getElementById('qProgressFill').style.width = `${pct}%`;
}

function isQuestionAnswered(q) {
  if (!q) return false;
  if (q.type === 'M' || q.type === 'MULTI') {
    return !!(state.answersMap[`${q.id}_V`] || state.answersMap[`${q.id}_A`] || state.answersMap[`${q.id}_D`] || state.answersMap[`${q.id}_P`]);
  } else {
    return !!state.answersMap[`${q.id}_G`];
  }
}

function updateQuestionnaireFilters() {
  const filterThema = document.getElementById('qFilterThematique');
  const filterPack = document.getElementById('qFilterPack');
  const filterClasse = document.getElementById('qFilterClasse');
  const filterStatus = document.getElementById('qFilterStatus');
  if (!filterPack || !filterClasse) return;

  const eligible = getActiveProfileEligibleQuestions();
  const availableThemas = Array.from(new Set(eligible.map(q => q.thematique).filter(Boolean))).sort();
  const availablePackIds = new Set(eligible.map(q => q.pack_id));
  const availableClasses = new Set(eligible.map(q => q.classe));

  if (filterThema) {
    const prevThema = filterThema.value;
    filterThema.innerHTML = `<option value="ALL">Toutes les thématiques (${availableThemas.length})</option>` +
      availableThemas.map(th => `<option value="${th}">${th}</option>`).join('');
    if (prevThema === 'ALL' || availableThemas.includes(prevThema)) {
      filterThema.value = prevThema;
    } else {
      filterThema.value = 'ALL';
    }
  }

  const prevPack = filterPack.value;
  filterPack.innerHTML = `<option value="ALL">Tous les jeux autorisés (${availablePackIds.size})</option>` +
    state.packs
      .filter(pk => availablePackIds.has(pk.id))
      .map(pk => `<option value="${pk.id}">${pk.nom}</option>`).join('');
  if (prevPack === 'ALL' || availablePackIds.has(parseInt(prevPack, 10))) {
    filterPack.value = prevPack;
  } else {
    filterPack.value = 'ALL';
  }

  const prevClasse = filterClasse.value;
  const classeLabels = {
    0: '0 - Non définies', 1: '1 - Standards', 2: '2 - Personnelles', 3: '3 - Intimes',
    4: '4 - Privées', 5: '5 - A caractère sexuel', 9: '9 - Interdits / Fantasmes'
  };
  filterClasse.innerHTML = `<option value="ALL">Toutes les classes autorisées (${availableClasses.size})</option>` +
    Array.from(availableClasses)
      .sort((a, b) => a - b)
      .map(cId => `<option value="${cId}">${classeLabels[cId] || 'Classe ' + cId}</option>`).join('');
  if (prevClasse === 'ALL' || availableClasses.has(parseInt(prevClasse, 10))) {
    filterClasse.value = prevClasse;
  } else {
    filterClasse.value = 'ALL';
  }

  // Filtre par statut de réponse (Toutes, Non répondues uniquement, Répondues uniquement)
  if (filterStatus) {
    const prevStatus = filterStatus.value || 'ALL';
    let unansCount = 0;
    let ansCount = 0;
    eligible.forEach(q => {
      if (isQuestionAnswered(q)) ansCount++;
      else unansCount++;
    });
    filterStatus.innerHTML = `
      <option value="ALL">Toutes les questions (${eligible.length})</option>
      <option value="UNANSWERED">Non répondues uniquement (${unansCount})</option>
      <option value="ANSWERED">Répondues uniquement (${ansCount})</option>
    `;
    if (['ALL', 'UNANSWERED', 'ANSWERED'].includes(prevStatus)) {
      filterStatus.value = prevStatus;
    } else {
      filterStatus.value = 'ALL';
    }
  }
}

function resetQuestionnaireFilters() {
  const fThema = document.getElementById('qFilterThematique');
  if (fThema) fThema.value = 'ALL';
  const fPack = document.getElementById('qFilterPack');
  if (fPack) fPack.value = 'ALL';
  const fClasse = document.getElementById('qFilterClasse');
  if (fClasse) fClasse.value = 'ALL';
  const fStatus = document.getElementById('qFilterStatus');
  if (fStatus) fStatus.value = 'ALL';
  const fHier = document.getElementById('qFilterHierarchie');
  if (fHier) fHier.value = 'ALL';
  renderQuestionsDeck();
}
window.resetQuestionnaireFilters = resetQuestionnaireFilters;

// Rendu du deck de questions (Saisie rapide V-A-D-P & Goûts)
function renderQuestionsDeck() {
  const deck = document.getElementById('questionsDeck');
  if (!deck) return;

  if (!state.activeProfileId) {
    document.getElementById('qNoProfileWarning').style.display = 'block';
    deck.innerHTML = '';
    return;
  }
  document.getElementById('qNoProfileWarning').style.display = 'none';

  const curProf = getActiveProfile();
  let adminBannerHtml = '';
  if (curProf && curProf.role === 'admin') {
    adminBannerHtml = `
      <div style="background: rgba(56,189,248,0.1); border: 1px solid rgba(56,189,248,0.3); border-radius: var(--radius-md); padding: 14px 18px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="font-size: 24px;">👑</span>
          <div>
            <div style="font-size: 14px; color: var(--accent-cyan); font-weight: 700;">
              Mode Superviseur Administrateur (Périmètre complet actif)
            </div>
            <div style="font-size: 12.5px; color: var(--text-dim); margin-top: 2px;">
              Vous visualisez l'ensemble des questions. Vous pouvez filtrer et tester directement les réponses. Pour répondre pour le compte d'un membre précis, changez le profil dans le sélecteur ci-dessus.
            </div>
          </div>
        </div>
      </div>`;
  }

  // Ne PAS appeler updateQuestionnaireFilters() ici pour ne pas écraser les sélecteurs pendant le filtrage utilisateur
  const eligible = getActiveProfileEligibleQuestions();
  if (eligible.length === 0) {
    deck.innerHTML = adminBannerHtml + `
      <div class="empty-state">
        <p>🔒 <strong>Périmètre restreint :</strong> Aucune question n'est autorisée pour ce profil selon la configuration définie par l'administrateur.</p>
      </div>`;
    return;
  }

  const themaFilter = document.getElementById('qFilterThematique')?.value || 'ALL';
  const packFilter = document.getElementById('qFilterPack')?.value || 'ALL';
  const classeFilter = document.getElementById('qFilterClasse')?.value || 'ALL';
  const statusFilter = document.getElementById('qFilterStatus')?.value || 'ALL';
  const hierarchieFilter = document.getElementById('qFilterHierarchie')?.value || 'ALL';

  const filtered = eligible.filter(q => {
    if (themaFilter !== 'ALL' && String(q.thematique) !== String(themaFilter)) return false;
    if (packFilter !== 'ALL' && String(q.pack_id) !== String(packFilter)) return false;
    if (classeFilter !== 'ALL' && String(q.classe) !== String(classeFilter)) return false;
    if (statusFilter === 'UNANSWERED' && isQuestionAnswered(q)) return false;
    if (statusFilter === 'ANSWERED' && !isQuestionAnswered(q)) return false;
    if (hierarchieFilter === 'MAIN') {
      // Question principale : pas de parent ou question de classe 8
      if (q.n_quest_lie && q.n_quest_lie !== 0 && q.n_quest_lie !== q.id && q.classe !== 8) return false;
    } else if (hierarchieFilter === 'SUB') {
      // Sous-question : a un parent distinct et n'est pas de classe 8
      if (!q.n_quest_lie || q.n_quest_lie === 0 || q.n_quest_lie === q.id || q.classe === 8) return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    if (statusFilter === 'UNANSWERED') {
      deck.innerHTML = adminBannerHtml + `
        <div class="empty-state" style="padding: 36px 20px; text-align: center;">
          <span style="font-size: 38px; display: block; margin-bottom: 10px;">🎉</span>
          <h4 style="color: #34D399; margin-bottom: 6px;">Toutes les questions sont répondues !</h4>
          <p style="color: var(--text-dim); font-size: 13px;">Vous avez déjà répondu à l'ensemble des questions correspondant aux critères sélectionnés.</p>
        </div>`;
    } else {
      deck.innerHTML = adminBannerHtml + `<div class="empty-state"><p>Aucune question ne correspond aux filtres sélectionnés.</p></div>`;
    }
    return;
  }

  const classeLabels = {
    0: 'Non définies', 1: 'Standards', 2: 'Personnelles', 3: 'Intimes',
    4: 'Privées', 5: 'A caractère sexuel', 9: 'Interdits / Fantasmes'
  };

  // Échelles de réponse textuelle selon Affinity.docx
  const scalesG = [
    { val: 1, label: 'Un peu' },
    { val: 2, label: 'Moyennement' },
    { val: 3, label: 'Beaucoup' },
    { val: 4, label: 'Passionnément' },
    { val: 5, label: 'À la folie' },
    { val: 9, label: 'Pas du tout' }
  ];

  const scalesVA = [
    { val: 1, label: 'Peu' },
    { val: 2, label: 'Régulièrement' },
    { val: 3, label: 'Souvent' },
    { val: 4, label: 'Très souvent' },
    { val: 5, label: 'Accro' },
    { val: 9, label: 'Jamais' }
  ];

  const scalesDP = [
    { val: 1, label: 'Me gêne' },
    { val: 2, label: 'Faire plaisir' },
    { val: 3, label: 'Ne gêne pas' },
    { val: 4, label: 'J\'en ai envie' },
    { val: 5, label: 'Obligatoire' },
    { val: 9, label: 'Impossible' }
  ];

  deck.innerHTML = adminBannerHtml + filtered.map(q => {
    const isMulti = (q.type === 'M' || q.type === 'MULTI');
    let answersUi = '';

    if (!isMulti) {
      // Type G (Goûts)
      const currentVal = state.answersMap[`${q.id}_G`] || 0;
      answersUi = `
        <div class="axis-row">
          <div class="axis-label-col">
            <span class="axis-tag">G</span> Goûts
          </div>
          <div class="btn-scale-group">
            ${scalesG.map(s => `
              <button class="btn-scale ${currentVal === s.val ? 'selected' : ''}" 
                      onclick="recordAnswer(${q.id}, 'G', ${s.val})">
                ${s.label}
              </button>
            `).join('')}
          </div>
        </div>
      `;
    } else {
      // Type MULTI (V, A, D, P)
      const curV = state.answersMap[`${q.id}_V`] || 0;
      const curA = state.answersMap[`${q.id}_A`] || 0;
      const curD = state.answersMap[`${q.id}_D`] || 0;
      const curP = state.answersMap[`${q.id}_P`] || 0;

      answersUi = `
        <div class="answers-matrix">
          <div class="axis-row">
            <div class="axis-label-col">
              <span class="axis-tag">V</span> (V) Le Vécu (Passé)
            </div>
            <div class="btn-scale-group">
              ${scalesVA.map(s => `
                <button class="btn-scale ${curV === s.val ? 'selected' : ''}" 
                        onclick="recordAnswer(${q.id}, 'V', ${s.val})">
                  ${s.label}
                </button>
              `).join('')}
            </div>
          </div>

          <div class="axis-row">
            <div class="axis-label-col">
              <span class="axis-tag">A</span> (A) Actuel (Présent)
            </div>
            <div class="btn-scale-group">
              ${scalesVA.map(s => `
                <button class="btn-scale ${curA === s.val ? 'selected' : ''}" 
                        onclick="recordAnswer(${q.id}, 'A', ${s.val})">
                  ${s.label}
                </button>
              `).join('')}
            </div>
          </div>

          <div class="axis-row">
            <div class="axis-label-col">
              <span class="axis-tag">D</span> (D) Découverte ou Poursuite (Futur)
            </div>
            <div class="btn-scale-group">
              ${scalesDP.map(s => `
                <button class="btn-scale ${curD === s.val ? 'selected' : ''}" 
                        onclick="recordAnswer(${q.id}, 'D', ${s.val})">
                  ${s.label}
                </button>
              `).join('')}
            </div>
          </div>

          <div class="axis-row">
            <div class="axis-label-col">
              <span class="axis-tag">P</span> Partage (Chez l'autre)
            </div>
            <div class="btn-scale-group">
              ${scalesDP.map(s => `
                <button class="btn-scale ${curP === s.val ? 'selected' : ''}" 
                        onclick="recordAnswer(${q.id}, 'P', ${s.val})">
                  ${s.label}
                </button>
              `).join('')}
            </div>
          </div>
        </div>
      `;
    }

    const isSubquestion = Boolean(q.n_quest_lie && q.n_quest_lie !== 0 && q.n_quest_lie !== q.id && q.classe !== 8);
    const isParent = Boolean(q.subquestions_count && q.subquestions_count > 0);

    let hierBadge = '';
    if (isSubquestion) {
      const parentName = q.parent_texte ? escapeHtml(q.parent_texte) : `#${q.n_quest_lie}`;
      hierBadge = `<span class="badge-tag subquestion-tag" title="Sous-question rattachée à la question #${q.n_quest_lie}">↳ Sous-question de : ${parentName}</span>`;
    } else if (isParent) {
      hierBadge = `<span class="badge-tag parent-tag" title="Cette question regroupe ${q.subquestions_count} sous-question(s)">📂 Question Principale (${q.subquestions_count} s-q)</span>`;
    }

    return `
      <div class="question-card ${isSubquestion ? 'is-subquestion' : ''}" id="qcard-${q.id}">
        <div class="q-card-header">
          <div class="q-badge-group">
            <span class="badge-tag">#${q.id} &bull; ${q.thematique} &bull; ${q.sujet}</span>
            <span class="badge-tag classe">Classe ${q.classe} - ${classeLabels[q.classe] || ''}</span>
            <span class="badge-tag type">${q.type === 'G' ? 'Goût Unique' : 'Matrice 4 Axes'}</span>
            ${hierBadge}
          </div>
          ${isCurrentAdmin() ? `<button class="btn-text-icon" title="Modifier la question" onclick="openEditQuestionModal(${q.id})" style="font-size:14px; padding:4px 8px; border-radius:6px; background:rgba(255,255,255,0.05);">✏️ Modifier</button>` : ''}
        </div>
        <div class="q-text">${isSubquestion ? '<span class="subquestion-indicator">↳</span> ' : ''}${q.texte}</div>
        ${answersUi}
      </div>
    `;
  }).join('');
}

// Enregistrement d'une réponse
async function recordAnswer(questionId, axis, value) {
  if (!state.activeProfileId) return;

  // Mise à jour optimiste dans l'état local
  state.answersMap[`${questionId}_${axis}`] = value;
  renderQuestionsDeck();
  updateProgressBar();
  updateIdentityCompletionBadge();

  try {
    const res = await fetch(`${API_BASE}/api/answers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        profile_id: state.activeProfileId,
        answers: [{ question_id: questionId, axis, value }]
      })
    });
    if (!res.ok) throw new Error('Erreur enregistrement');
    showToast(`Réponse [${axis}] sauvegardée !`);
    loadStats();
  } catch (err) {
    console.error(err);
  }
}

// ==========================================
// CALCULATEUR & RADAR D'AFFINITÉ
// ==========================================
function updateAffinitySelectors() {
  updateProfileDropdowns();
  updateAffinitySelectorsStatus();
  updateTargetProfilePreview();
}

function updateAffinitySelectorsStatus() {
  const p1Id = parseInt(document.getElementById('affProfile1')?.value, 10);
  const p2Id = parseInt(document.getElementById('affProfile2')?.value, 10);

  const p1 = state.profiles.find(p => p.id === p1Id);
  const p2 = state.profiles.find(p => p.id === p2Id);

  const stat1 = document.getElementById('idStatus1');
  const stat2 = document.getElementById('idStatus2');

  if (p1 && stat1) {
    stat1.innerHTML = p1.has_identity 
      ? '<span class="status-dot success"></span> Profil complété'
      : '<span class="status-dot warning"></span> Profil à compléter (Obligatoire)';
  }
  if (p2 && stat2) {
    stat2.innerHTML = p2.has_identity 
      ? '<span class="status-dot success"></span> Profil complété'
      : '<span class="status-dot warning"></span> Profil à compléter (Obligatoire)';
  }
}

// ==========================================================================
// APERÇU DU PROFIL 2 & DISTANCE KILOMÉTRIQUE
// ==========================================================================
async function updateTargetProfilePreview() {
  const p1Id = parseInt(document.getElementById('affProfile1')?.value, 10);
  const p2Id = parseInt(document.getElementById('affProfile2')?.value, 10);
  const previewCard = document.getElementById('targetProfilePreviewCard');
  if (!previewCard) return;

  const p1 = state.profiles.find(p => p.id === p1Id);
  const p2 = state.profiles.find(p => p.id === p2Id);

  if (!p2 || p1Id === p2Id) {
    previewCard.style.display = 'none';
    return;
  }

  previewCard.style.display = 'block';

  // Remplissage infos profil ciblé
  const elPseudo = document.getElementById('tpcPseudo');
  const elAffId = document.getElementById('tpcAffId');
  const elAvatar = document.getElementById('tpcAvatar');
  const elStatut = document.getElementById('tpcStatut');
  const elVille = document.getElementById('tpcVille');
  const elDist = document.getElementById('tpcDistanceBadge');
  const elBio = document.getElementById('tpcBioText');

  if (elPseudo) elPseudo.textContent = p2.pseudo;
  if (elAffId) elAffId.textContent = formatAffId(p2.id);
  if (elAvatar) elAvatar.textContent = p2.pseudo.charAt(0).toUpperCase();
  if (elStatut) elStatut.textContent = p2.statut || 'Statut non précisé';
  if (elVille) elVille.textContent = p2.ville || 'Ville non renseignée';
  if (elBio) elBio.textContent = p2.bio ? `"${p2.bio}"` : 'Aucune présentation fournie pour le moment.';

  // Calcul et affichage de la distance kilométrique
  if (elDist) {
    if (p1 && p1.ville && p2.ville) {
      if (p1.ville.trim().toLowerCase() === p2.ville.trim().toLowerCase()) {
        elDist.className = 'tpc-distance-badge same-city';
        elDist.innerHTML = `📍 Même ville (${p1.ville}) &bull; 0 km`;
      } else {
        try {
          const res = await fetch(`${API_BASE}/api/distance?ville1=${encodeURIComponent(p1.ville)}&ville2=${encodeURIComponent(p2.ville)}`);
          const dData = await res.json();
          if (dData.distance_km !== null) {
            elDist.className = 'tpc-distance-badge';
            elDist.innerHTML = `🚗 Distance : <strong>${dData.distance_km} km</strong> (${p1.ville} ⇄ ${p2.ville})`;
          } else {
            elDist.className = 'tpc-distance-badge unknown';
            elDist.innerHTML = `📍 ${p1.ville} ⇄ ${p2.ville} (distance non calculée)`;
          }
        } catch {
          elDist.className = 'tpc-distance-badge unknown';
          elDist.innerHTML = `📍 ${p1.ville} ⇄ ${p2.ville}`;
        }
      }
    } else {
      elDist.className = 'tpc-distance-badge unknown';
      elDist.innerHTML = `📍 Ville non renseignée dans le profil`;
    }
  }
}

// ==========================================================================
// SYSTÈME BILATÉRAL DE DEMANDE DE MATCH & CALCUL
// ==========================================================================
async function handleAffinityOrMatchAction() {
  const role = getActiveRole();
  if (role === 'guest') {
    alert('🔒 Fonctionnalité réservée : Les invités ne peuvent pas envoyer de demande de match.');
    return;
  }
  if (role === 'subscriber') {
    await sendMatchRequest();
  } else {
    // Administrateur : calcul d'affinité direct avec option de demande
    await computeAffinityAction();
  }
}

async function sendMatchRequest() {
  const p1Id = parseInt(document.getElementById('affProfile1')?.value, 10);
  const p2Id = parseInt(document.getElementById('affProfile2')?.value, 10);

  if (p1Id === p2Id) {
    alert('Veuillez sélectionner un autre profil que le vôtre pour envoyer une demande de match.');
    return;
  }

  const p1 = state.profiles.find(p => p.id === p1Id);
  const p2 = state.profiles.find(p => p.id === p2Id);

  if (!p1?.has_identity || !p2?.has_identity) {
    alert('Le profil des deux membres doit être complété avant de pouvoir initier une demande de match.');
    return;
  }

  // Classes de questions proposées par le demandeur (par défaut [1, 2] ou son périmètre)
  let proposedClasses = [1, 2];
  if (p1.question_access && Array.isArray(p1.question_access.allowed_classes)) {
    proposedClasses = p1.question_access.allowed_classes;
  }

  try {
    const res = await fetch(`${API_BASE}/api/match-requests`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        sender_id: p1Id,
        receiver_id: p2Id,
        proposed_classes: proposedClasses
      })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erreur lors de l\'envoi de la demande');

    showToast(`💌 Demande de match envoyée à ${p2.pseudo} (${formatAffId(p2.id)}) !`);
    await loadMatchRequests();

    // Basculer sur l'onglet Envoyées
    document.getElementById('btnTabRequestsSent')?.click();
  } catch (err) {
    alert('Erreur : ' + err.message);
  }
}

async function loadMatchRequests() {
  if (!state.activeProfileId) return;
  try {
    const res = await fetch(`${API_BASE}/api/profiles/${state.activeProfileId}/match-requests`);
    if (!res.ok) return;
    const data = await res.json();
    renderMatchRequests(data);
  } catch (err) {
    console.error('Erreur chargement match requests:', err);
  }
}

function switchMatchSubTab(tab) {
  const btnRec = document.getElementById('btnTabReceivedMatches') || document.getElementById('btnTabRequestsReceived');
  const btnSent = document.getElementById('btnTabSentMatches') || document.getElementById('btnTabRequestsSent');
  const paneRec = document.getElementById('paneReceivedMatches') || document.getElementById('requestsReceivedPanel');
  const paneSent = document.getElementById('paneSentMatches') || document.getElementById('requestsSentPanel');

  if (tab === 'received') {
    btnRec?.classList.add('active');
    btnSent?.classList.remove('active');
    if (paneRec) paneRec.style.display = 'block';
    if (paneSent) paneSent.style.display = 'none';
  } else {
    btnSent?.classList.add('active');
    btnRec?.classList.remove('active');
    if (paneSent) paneSent.style.display = 'block';
    if (paneRec) paneRec.style.display = 'none';
  }
}

function renderMatchRequests(data) {
  const receivedList = document.getElementById('listReceivedMatches') || document.getElementById('matchRequestsReceivedList');
  const sentList = document.getElementById('listSentMatches') || document.getElementById('matchRequestsSentList');
  const countReceivedBadge = document.getElementById('badgeCountReceived') || document.getElementById('countRequestsReceivedBadge');
  const countSentBadge = document.getElementById('badgeCountSent') || document.getElementById('countRequestsSentBadge');

  const received = data.received || [];
  const sent = data.sent || [];

  const pendingReceived = received.filter(r => r.status === 'pending');
  if (countReceivedBadge) countReceivedBadge.textContent = pendingReceived.length ? `${pendingReceived.length}` : '0';
  if (countSentBadge) countSentBadge.textContent = sent.length ? `${sent.length}` : '0';

  const classeLabels = {
    1: 'Classe 1 (Standards)', 2: 'Classe 2 (Personnelles)', 3: 'Classe 3 (Intimes)',
    4: 'Classe 4 (Privées)', 5: 'Classe 5 (Hors normes)', 9: 'Classe 9 (Amorales)'
  };

  // 1. Demandes Reçues
  if (receivedList) {
    if (received.length === 0) {
      receivedList.innerHTML = '<div class="empty-requests-msg">📬 Vous n\'avez reçu aucune demande de match pour le moment.</div>';
    } else {
      receivedList.innerHTML = received.map(req => {
        const isPending = req.status === 'pending';
        const isAccepted = req.status === 'accepted';
        const isDeclined = req.status === 'declined';

        const statusLabel = isPending 
          ? '<span class="mrc-status-badge pending">⏳ En attente de votre réponse</span>' 
          : (isAccepted 
              ? '<span class="mrc-status-badge accepted">✅ Match Accepté</span>' 
              : '<span class="mrc-status-badge declined">❌ Refusée</span>');

        const classesToShow = isAccepted ? req.validated_classes : req.proposed_classes;
        const classesHtml = (classesToShow || [1, 2]).map(cl => `
          <label class="mrc-tag ${isAccepted ? 'selected' : ''}">
            ${isPending ? `<input type="checkbox" name="reqClass_${req.id}" value="${cl}" checked style="margin-right:4px;">` : ''}
            ${classeLabels[cl] || `Classe ${cl}`}
          </label>
        `).join('');

        const distText = req.distance_km !== null 
          ? `🚗 ${req.distance_km} km (${req.sender_ville || '?'} ⇄ ${req.my_ville || '?'})`
          : `📍 ${req.sender_ville || 'Ville non renseignée'}`;

        const affResJson = req.affinity_result ? JSON.stringify(req.affinity_result).replace(/'/g, '&#39;') : '';

        return `
          <div class="match-request-card">
            <div class="mrc-top">
              <div class="mrc-user-info">
                <div class="mrc-avatar">${req.sender_pseudo.charAt(0).toUpperCase()}</div>
                <div class="mrc-meta">
                  <h4>${req.sender_pseudo} <span class="tpc-aff-id">${formatAffId(req.sender_id)}</span></h4>
                  <div class="mrc-subtext">${distText} &bull; Demande reçue le ${new Date(req.created_at).toLocaleDateString()}</div>
                </div>
              </div>
              <div>${statusLabel}</div>
            </div>

            <div class="mrc-classes-scope">
              <span class="mrc-scope-lbl">Périmètres de questions considérés :</span>
              <div class="mrc-classes-tags" id="reqClassesBox_${req.id}">
                ${classesHtml}
              </div>
            </div>

            ${isPending ? `
              <div class="mrc-actions-row">
                <button class="btn btn-sm btn-outline" onclick="respondMatchRequestAction(${req.id}, 'declined')">
                  ❌ Décliner
                </button>
                <button class="btn btn-sm btn-gradient" onclick="respondMatchRequestAction(${req.id}, 'accepted')">
                  ✅ Accepter le Match avec ces périmètres
                </button>
              </div>
            ` : ''}

            ${isAccepted && req.affinity_result ? `
              <div class="mrc-actions-row" style="justify-content: space-between; align-items:center;">
                <span style="font-size:13px; color:var(--accent-emerald); font-weight:700;">
                  🎉 Affinité calculée : ${req.affinity_result.score_global}%
                </span>
                <button class="btn btn-sm btn-primary" onclick='viewAcceptedMatchResult(${affResJson})'>
                  📊 Voir le rapport complet
                </button>
              </div>
            ` : ''}
          </div>
        `;
      }).join('');
    }
  }

  // 2. Demandes Envoyées
  if (sentList) {
    if (sent.length === 0) {
      sentList.innerHTML = '<div class="empty-requests-msg">📤 Vous n\'avez envoyé aucune demande de match.</div>';
    } else {
      sentList.innerHTML = sent.map(req => {
        const isPending = req.status === 'pending';
        const isAccepted = req.status === 'accepted';
        const isDeclined = req.status === 'declined';

        const statusLabel = isPending 
          ? '<span class="mrc-status-badge pending">⏳ En attente de validation</span>' 
          : (isAccepted 
              ? '<span class="mrc-status-badge accepted">✅ Accepté par le destinataire</span>' 
              : '<span class="mrc-status-badge declined">❌ Refusée</span>');

        const classesToShow = isAccepted ? req.validated_classes : req.proposed_classes;
        const classesHtml = (classesToShow || [1, 2]).map(cl => `
          <span class="mrc-tag ${isAccepted ? 'selected' : ''}">
            ${classeLabels[cl] || `Classe ${cl}`}
          </span>
        `).join('');

        const distText = req.distance_km !== null 
          ? `🚗 ${req.distance_km} km (${req.my_ville || '?'} ⇄ ${req.receiver_ville || '?'})`
          : `📍 ${req.receiver_ville || 'Ville non renseignée'}`;

        const affResJson = req.affinity_result ? JSON.stringify(req.affinity_result).replace(/'/g, '&#39;') : '';

        return `
          <div class="match-request-card">
            <div class="mrc-top">
              <div class="mrc-user-info">
                <div class="mrc-avatar">${req.receiver_pseudo.charAt(0).toUpperCase()}</div>
                <div class="mrc-meta">
                  <h4>${req.receiver_pseudo} <span class="tpc-aff-id">${formatAffId(req.receiver_id)}</span></h4>
                  <div class="mrc-subtext">${distText} &bull; Envoyée le ${new Date(req.created_at).toLocaleDateString()}</div>
                </div>
              </div>
              <div>${statusLabel}</div>
            </div>

            <div class="mrc-classes-scope">
              <span class="mrc-scope-lbl">${isAccepted ? 'Périmètres validés d\'un commun accord :' : 'Périmètres de questions proposés :'}</span>
              <div class="mrc-classes-tags">
                ${classesHtml}
              </div>
            </div>

            ${isAccepted && req.affinity_result ? `
              <div class="mrc-actions-row" style="justify-content: space-between; align-items:center;">
                <span style="font-size:13px; color:var(--accent-cyan); font-weight:700;">
                  🎉 Match Validé &bull; Score d'affinité : ${req.affinity_result.score_global}%
                </span>
                <button class="btn btn-sm btn-gradient" onclick='viewAcceptedMatchResult(${affResJson})'>
                  📊 Découvrir le rapport de Match
                </button>
              </div>
            ` : ''}
          </div>
        `;
      }).join('');
    }
  }
}

async function respondMatchRequestAction(requestId, action) {
  let validatedClasses = [1, 2];
  if (action === 'accepted') {
    const cbs = Array.from(document.querySelectorAll(`input[name="reqClass_${requestId}"]`));
    const selected = cbs.filter(cb => cb.checked).map(cb => parseInt(cb.value, 10));
    if (selected.length === 0) {
      alert('Veuillez cocher au moins un périmètre (classe) de questions à prendre en compte.');
      return;
    }
    validatedClasses = selected;
  }

  try {
    const res = await fetch(`${API_BASE}/api/match-requests/${requestId}/respond`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action,
        validated_classes: validatedClasses
      })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erreur lors de la réponse');

    showToast(action === 'accepted' ? '🎉 Match accepté avec succès ! Les affinités sont maintenant accessibles.' : 'Demande déclinée.');
    await loadMatchRequests();

    if (action === 'accepted' && data.affinity_result) {
      viewAcceptedMatchResult(data.affinity_result);
    }
  } catch (err) {
    alert('Erreur : ' + err.message);
  }
}

function viewAcceptedMatchResult(affinityResult) {
  const alertBox = document.getElementById('affinityRuleAlert');
  const resultsCard = document.getElementById('affinityResultsContainer');

  if (alertBox) alertBox.style.display = 'none';
  if (resultsCard) resultsCard.style.display = 'flex';

  state.lastAffinityResult = affinityResult;
  renderAffinityResults(affinityResult);

  // Synchroniser les sélecteurs
  if (affinityResult.profile1?.id && affinityResult.profile2?.id) {
    const aff1 = document.getElementById('affProfile1');
    const aff2 = document.getElementById('affProfile2');
    if (aff1) aff1.value = affinityResult.profile1.id;
    if (aff2) aff2.value = affinityResult.profile2.id;
    updateAffinitySelectorsStatus();
    updateTargetProfilePreview();
  }

  resultsCard.scrollIntoView({ behavior: 'smooth' });
}

async function computeAffinityAction() {
  const p1Id = parseInt(document.getElementById('affProfile1')?.value, 10);
  const p2Id = parseInt(document.getElementById('affProfile2')?.value, 10);

  if (!p1Id || !p2Id) {
    alert('Veuillez sélectionner deux membres pour calculer leur affinité.');
    return;
  }

  if (p1Id === p2Id) {
    alert('Veuillez sélectionner deux profils différents pour comparer leurs affinités.');
    return;
  }

  const p1 = state.profiles.find(p => p.id === p1Id);
  const p2 = state.profiles.find(p => p.id === p2Id);
  if (p1?.role === 'admin' || p2?.role === 'admin') {
    alert('Un compte administrateur supervise le système et ne participe pas aux calculs de match.');
    return;
  }

  const alertBox = document.getElementById('affinityRuleAlert');
  const resultsCard = document.getElementById('affinityResultsContainer');

  try {
    const res = await fetch(`${API_BASE}/api/affinity/calculate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        profile1_id: p1Id, 
        profile2_id: p2Id,
        simulated_role: state.simulatedRole 
      })
    });
    const data = await res.json();

    if (!res.ok) {
      if (data.error === 'FICHE_MANQUANTE') {
        alertBox.style.display = 'flex';
        resultsCard.style.display = 'none';
        document.getElementById('affinityRuleAlertText').textContent = data.message;
        return;
      }
      if (data.error === 'ACCES_RESTREINT') {
        alertBox.style.display = 'none';
        resultsCard.style.display = 'none';
        alert('🔒 Accès Restreint : ' + data.message);
        return;
      }
      throw new Error(data.message || data.error);
    }

    // Succès : Afficher le rapport d'affinité
    alertBox.style.display = 'none';
    resultsCard.style.display = 'flex';
    state.lastAffinityResult = data;
    renderAffinityResults(data);

    // Mettre à jour le Hero et la Smartwatch
    document.getElementById('heroMatchRate').textContent = `${data.score_global}%`;
    document.getElementById('watchScore').textContent = `${data.score_global}%`;
    document.getElementById('watchMatchDesc').textContent = `Match ${data.profile1.pseudo} & ${data.profile2.pseudo}`;
  } catch (err) {
    alert('Erreur lors du calcul : ' + err.message);
  }
}

function renderAffinityResults(data) {
  // 1. Jauge Circulaire
  const score = data.score_global;
  const circle = document.getElementById('gaugeScoreCircle');
  const valText = document.getElementById('gaugeValue');
  const verdict = document.getElementById('matchVerdict');

  valText.textContent = `${score}%`;

  // Animation périmètre SVG (circonférence = 2 * PI * 85 ~= 534)
  const offset = 534 - (534 * (score / 100));
  setTimeout(() => {
    circle.style.strokeDashoffset = offset;
  }, 50);

  let verdictText = '';
  if (score >= 80) {
    verdictText = '✨ <strong>Connexion Élective Exceptionnelle</strong> : Forte convergence de valeurs et synergie relationnelle.';
  } else if (score >= 60) {
    verdictText = '🤝 <strong>Belle Complicité</strong> : De nombreux points d\'ancrage avec des complémentarités intéressantes.';
  } else {
    verdictText = '⚡ <strong>Personnalités Différentes</strong> : Diversité d\'opinions et de modes de vie nécessitant des compromis.';
  }

  // Ajout de la distance kilométrique si disponible
  if (data.distance_km !== undefined && data.distance_km !== null) {
    verdictText += `<div style="margin-top:10px; font-size:13px; color:var(--accent-cyan); font-weight:600;">🚗 Distance entre les deux profils : <strong>${data.distance_km} km</strong> (${data.profile1.ville || '?'} ⇄ ${data.profile2.ville || '?'})</div>`;
  }

  verdict.innerHTML = verdictText;

  // 2. Barres des 4 axes
  const setBar = (scoreVal, valId, barId) => {
    const elVal = document.getElementById(valId);
    const elBar = document.getElementById(barId);
    if (scoreVal !== null && scoreVal !== undefined) {
      elVal.textContent = `${scoreVal}%`;
      setTimeout(() => { elBar.style.width = `${scoreVal}%`; }, 100);
    } else {
      elVal.textContent = '--%';
      elBar.style.width = '0%';
    }
  };

  setBar(data.axes.G, 'scoreG', 'barG');
  setBar(data.axes.V, 'scoreV', 'barV');
  setBar(data.axes.A, 'scoreA', 'barA');
  setBar(data.axes.DP_synergy, 'scoreDP', 'barDP');

  // 3. Graphique Radar SVG interactif
  renderRadarChart(data.thematiques);

  // 4. Points de Fusion et Vigilance
  const fusionList = document.getElementById('fusionList');
  const vigilanceList = document.getElementById('vigilanceList');

  if (data.points_de_fusion && data.points_de_fusion.length > 0) {
    fusionList.innerHTML = data.points_de_fusion.map(p => `
      <div class="point-item">
        <span>${p.thematique} &bull; ${p.sujet}</span>
        <span class="point-score">${p.score}%</span>
      </div>
    `).join('');
  } else {
    fusionList.innerHTML = `<div class="empty-state-mini"><p>Aucun point de fusion &ge; 85% identifié.</p></div>`;
  }

  if (data.zones_de_vigilance && data.zones_de_vigilance.length > 0) {
    vigilanceList.innerHTML = data.zones_de_vigilance.map(p => `
      <div class="point-item">
        <span>${p.thematique} &bull; ${p.sujet}</span>
        <span class="point-score">${p.score}%</span>
      </div>
    `).join('');
  } else {
    vigilanceList.innerHTML = `<div class="empty-state-mini"><p>Aucune divergence majeure &le; 35% constatée.</p></div>`;
  }
}

// Générateur de Radar Chart SVG vectoriel
function renderRadarChart(thematiques) {
  const container = document.getElementById('radarContainer');
  if (!container) return;

  const entries = Object.entries(thematiques);
  if (entries.length < 3) {
    container.innerHTML = `<p style="font-size:13px; color:var(--text-dim); text-align:center;">Répondez à au moins 3 thématiques communes pour visualiser le radar complet.</p>`;
    return;
  }

  const size = 260;
  const center = size / 2;
  const radius = 90;
  const total = entries.length;

  let gridPolygons = '';
  [0.25, 0.5, 0.75, 1.0].forEach(rRatio => {
    const points = [];
    for (let i = 0; i < total; i++) {
      const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
      const x = center + Math.cos(angle) * (radius * rRatio);
      const y = center + Math.sin(angle) * (radius * rRatio);
      points.push(`${x},${y}`);
    }
    gridPolygons += `<polygon points="${points.join(' ')}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>`;
  });

  // Points et polygone des valeurs
  const scorePoints = [];
  let labelsSvg = '';

  entries.forEach(([theme, score], i) => {
    const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
    const rVal = radius * (score / 100.0);
    const x = center + Math.cos(angle) * rVal;
    const y = center + Math.sin(angle) * rVal;
    scorePoints.push(`${x},${y}`);

    // Libellés
    const lx = center + Math.cos(angle) * (radius + 22);
    const ly = center + Math.sin(angle) * (radius + 22);
    labelsSvg += `
      <text x="${lx}" y="${ly}" fill="#94A3B8" font-size="10" font-weight="600" text-anchor="middle" dominant-baseline="middle">
        ${theme} (${score}%)
      </text>
    `;
  });

  const svg = `
    <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
      <defs>
        <radialGradient id="radarFillGrad">
          <stop offset="0%" stop-color="#FF3366" stop-opacity="0.5"/>
          <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0.15"/>
        </radialGradient>
      </defs>
      ${gridPolygons}
      <polygon points="${scorePoints.join(' ')}" fill="url(#radarFillGrad)" stroke="#FF3366" stroke-width="2.5"/>
      ${labelsSvg}
    </svg>
  `;

  container.innerHTML = svg;
}

// Remplissage dynamique des filtres de la banque de questions
function populateBankFilters() {
  const themaSelect = document.getElementById('bankFilterThematique');
  if (!themaSelect) return;

  const prevThema = themaSelect.value || 'ALL';
  const thematiques = Array.from(new Set(state.questions.map(q => q.thematique).filter(Boolean))).sort();
  themaSelect.innerHTML = `<option value="ALL">Toutes les thématiques (${thematiques.length})</option>` +
    thematiques.map(th => `<option value="${th}">${th}</option>`).join('');
  if (prevThema === 'ALL' || thematiques.includes(prevThema)) {
    themaSelect.value = prevThema;
  } else {
    themaSelect.value = 'ALL';
  }

  updateBankSujetsDropdown();
}

function updateBankSujetsDropdown() {
  const themaSelect = document.getElementById('bankFilterThematique');
  const sujetSelect = document.getElementById('bankFilterSujet');
  if (!sujetSelect) return;

  const prevSujet = sujetSelect.value || 'ALL';
  const currentThema = themaSelect ? themaSelect.value : 'ALL';
  const filteredQuestions = currentThema === 'ALL'
    ? state.questions
    : state.questions.filter(q => String(q.thematique) === String(currentThema));

  const sujets = Array.from(new Set(filteredQuestions.map(q => q.sujet).filter(Boolean))).sort();
  sujetSelect.innerHTML = `<option value="ALL">Tous les sujets (${sujets.length})</option>` +
    sujets.map(s => `<option value="${s}">${s}</option>`).join('');
  if (prevSujet === 'ALL' || sujets.includes(prevSujet)) {
    sujetSelect.value = prevSujet;
  } else {
    sujetSelect.value = 'ALL';
  }
}

function onBankThematiqueChange() {
  updateBankSujetsDropdown();
  renderQuestionsTable();
}
window.onBankThematiqueChange = onBankThematiqueChange;
window.renderQuestionsTable = renderQuestionsTable;

// Table des Questions avec filtrage multi-critères (Thématique, Sujet, Classe, Cible N_CIBLE, Texte)
function renderQuestionsTable() {
  const tbody = document.getElementById('questionsTableBody');
  if (!tbody) return;

  const searchTerm = (document.getElementById('bankSearchInput')?.value || '').toLowerCase().trim();
  const filterThema = document.getElementById('bankFilterThematique')?.value || 'ALL';
  const filterSujet = document.getElementById('bankFilterSujet')?.value || 'ALL';
  const filterClasse = document.getElementById('bankFilterClasse')?.value || 'ALL';
  const filterCible = document.getElementById('bankFilterCible')?.value || 'ALL';
  const filterHierarchie = document.getElementById('bankFilterHierarchie')?.value || 'ALL';

  const filtered = state.questions.filter(q => {
    if (filterThema !== 'ALL' && String(q.thematique) !== String(filterThema)) return false;
    if (filterSujet !== 'ALL' && String(q.sujet) !== String(filterSujet)) return false;
    if (filterClasse !== 'ALL' && String(q.classe) !== String(filterClasse)) return false;
    if (filterCible !== 'ALL' && String(q.cible) !== String(filterCible)) return false;
    if (filterHierarchie === 'MAIN') {
      if ((q.n_quest_lie && q.n_quest_lie !== 0 && q.n_quest_lie !== q.id) && q.classe !== 8) return false;
    } else if (filterHierarchie === 'PARENT') {
      if (!q.subquestions_count || q.subquestions_count <= 0) return false;
    } else if (filterHierarchie === 'SUB') {
      if (!q.n_quest_lie || q.n_quest_lie === 0 || q.n_quest_lie === q.id || q.classe === 8) return false;
    }
    if (searchTerm) {
      const matchText = (q.texte || '').toLowerCase().includes(searchTerm);
      const matchThema = (q.thematique || '').toLowerCase().includes(searchTerm);
      const matchSujet = (q.sujet || '').toLowerCase().includes(searchTerm);
      if (!matchText && !matchThema && !matchSujet) return false;
    }
    return true;
  });

  const countBadge = document.getElementById('bankQuestionsCountBadge');
  if (countBadge) {
    countBadge.textContent = `${filtered.length} question${filtered.length > 1 ? 's' : ''}`;
  }

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" style="text-align:center; padding: 36px 16px; color: var(--text-dim); font-size: 14px;">
          🔍 Aucune question ne correspond aux filtres sélectionnés.
        </td>
      </tr>`;
    return;
  }

  const classeLabels = {
    0: '0 - Non définies', 1: '1 - Standards', 2: '2 - Personnelles', 3: '3 - Intimes',
    4: '4 - Privées', 5: '5 - A caractère sexuel', 8: '8 - Identité', 9: '9 - Amorales / Interdits'
  };

  tbody.innerHTML = filtered.map(q => {
    let typeBadgeHtml = '<span class="badge-tag type">Multi-Axes (M)</span>';
    if (q.type === 'P') {
      typeBadgeHtml = '<span class="badge-tag type" style="background:#0284c7; color:#fff;">Précis (P)</span>';
    } else if (q.type === 'T') {
      typeBadgeHtml = '<span class="badge-tag type" style="background:#7c3aed; color:#fff;">Tolérance (T)</span>';
    } else if (q.type === 'G') {
      typeBadgeHtml = '<span class="badge-tag type">Goût (G)</span>';
    }

    const cibleBadgeHtml = q.cible === 0 
      ? '<span class="badge-tag" style="background:rgba(148,163,184,0.15); color:#cbd5e1;">Mixte (0)</span>'
      : (q.cible === 1 
          ? '<span class="badge-tag" style="background:rgba(56,189,248,0.15); color:#38bdf8;">Homme (1)</span>'
          : '<span class="badge-tag" style="background:rgba(236,72,153,0.15); color:#f472b6;">Femme (2)</span>');

    const sujetLabel = (q.n_sujet !== undefined && q.n_sujet !== null && q.n_sujet > 0)
      ? `<span class="badge-tag" style="font-size:10px; padding:2px 6px; margin-right:4px; opacity:0.85;">#${q.n_sujet}</span>${q.sujet}`
      : q.sujet;

    let hierHtml = '';
    if (q.subquestions_count && q.subquestions_count > 0) {
      hierHtml = `<div style="margin-top:5px;"><span class="badge-tag parent-tag" style="font-size:10.5px; padding:2px 7px;" title="${q.subquestions_count} sous-question(s) rattachée(s)">📂 Question Principale (${q.subquestions_count} s-q)</span></div>`;
    } else if (q.n_quest_lie && q.n_quest_lie !== 0 && q.classe !== 8) {
      const pTitle = q.parent_texte ? `Sous-question de #${q.n_quest_lie} : ${escapeHtml(q.parent_texte)}` : `Sous-question de #${q.n_quest_lie}`;
      const shortParent = q.parent_texte ? ` (${escapeHtml(q.parent_texte.substring(0, 30))}...)` : '';
      hierHtml = `<div style="margin-top:5px;"><span class="badge-tag subquestion-tag" style="font-size:10.5px; padding:2px 7px;" title="${pTitle}">↳ Sous-question de #${q.n_quest_lie}${shortParent}</span></div>`;
    } else if (q.classe === 8 && q.n_quest_lie) {
      hierHtml = `<div style="margin-top:5px;"><span class="badge-tag" style="font-size:10px; padding:2px 6px; background:rgba(124,58,237,0.15); color:#c084fc; border:1px solid rgba(124,58,237,0.3);" title="Question miroir #${q.n_quest_lie}">↔ Miroir #${q.n_quest_lie}</span></div>`;
    }

    const isSub = Boolean(q.n_quest_lie && q.n_quest_lie !== 0 && q.classe !== 8);

    return `
    <tr class="${isSub ? 'subquestion-table-row' : ''}">
      <td>#${q.id}</td>
      <td><strong>${q.thematique}</strong></td>
      <td>${sujetLabel}</td>
      <td>${classeLabels[q.classe] || `Classe ${q.classe}`}</td>
      <td>${typeBadgeHtml}</td>
      <td>${cibleBadgeHtml}</td>
      <td>
        <div style="${isSub ? 'padding-left:12px; border-left:2px solid var(--accent-cyan);' : ''}">
          ${q.texte}
          ${hierHtml}
        </div>
      </td>
      <td style="text-align:right; white-space:nowrap;">
        ${isCurrentAdmin() ? `
        <button class="btn btn-sm btn-outline" onclick="openEditQuestionModal(${q.id})" title="Modifier cette question">
          ✏️ Modifier
        </button>` : `<span style="font-size:11px; color:var(--text-dim); padding:4px 8px;">Lecture</span>`}
      </td>
    </tr>
  `;
  }).join('');
}

function populateModalThematiques(selectedThema = 'Identité', selectedSujet = 'Identité') {
  const themaSel = document.getElementById('editQThematiqueSelect');
  if (!themaSel) return;

  const thematiques = Array.from(new Set(state.questions.map(q => q.thematique).filter(Boolean))).sort();
  if (!thematiques.includes('Identité')) thematiques.unshift('Identité');

  let optsHtml = thematiques.map(th => `<option value="${th}">${th}</option>`).join('');
  optsHtml += `<option value="__NEW__">+ Autre thématique (saisie libre)...</option>`;
  themaSel.innerHTML = optsHtml;

  const customThemaInput = document.getElementById('editQThematiqueCustom');
  if (selectedThema && thematiques.includes(selectedThema)) {
    themaSel.value = selectedThema;
    if (customThemaInput) customThemaInput.style.display = 'none';
    document.getElementById('editQThematique').value = selectedThema;
  } else if (selectedThema) {
    themaSel.value = '__NEW__';
    if (customThemaInput) {
      customThemaInput.style.display = 'block';
      customThemaInput.value = selectedThema;
    }
    document.getElementById('editQThematique').value = selectedThema;
  } else {
    themaSel.value = thematiques[0] || 'Identité';
    if (customThemaInput) customThemaInput.style.display = 'none';
    document.getElementById('editQThematique').value = themaSel.value;
  }

  updateModalSujetsDropdown(selectedSujet);
}

function updateModalSujetsDropdown(selectedSujet = null) {
  const themaSel = document.getElementById('editQThematiqueSelect');
  const sujetSel = document.getElementById('editQSujetSelect');
  const customSujetInput = document.getElementById('editQSujetCustom');
  if (!sujetSel) return;

  const curThema = themaSel ? themaSel.value : 'Identité';
  if (curThema === '__NEW__') {
    sujetSel.style.display = 'none';
    if (customSujetInput) {
      customSujetInput.style.display = 'block';
      customSujetInput.value = selectedSujet || '';
    }
    document.getElementById('editQSujet').value = customSujetInput ? customSujetInput.value : '';
    return;
  }

  sujetSel.style.display = 'block';
  const filtered = state.questions.filter(q => q.thematique === curThema);
  const sujets = Array.from(new Set(filtered.map(q => q.sujet).filter(Boolean))).sort();
  if (curThema === 'Identité' && !sujets.includes('Identité')) sujets.unshift('Identité');

  let optsHtml = sujets.map(s => `<option value="${s}">${s}</option>`).join('');
  optsHtml += `<option value="__NEW__">+ Autre sujet (saisie libre)...</option>`;
  sujetSel.innerHTML = optsHtml;

  if (selectedSujet && sujets.includes(selectedSujet)) {
    sujetSel.value = selectedSujet;
    if (customSujetInput) customSujetInput.style.display = 'none';
    document.getElementById('editQSujet').value = selectedSujet;
  } else if (selectedSujet) {
    sujetSel.value = '__NEW__';
    if (customSujetInput) {
      customSujetInput.style.display = 'block';
      customSujetInput.value = selectedSujet;
    }
    document.getElementById('editQSujet').value = selectedSujet;
  } else {
    sujetSel.value = sujets[0] || (curThema === 'Identité' ? 'Identité' : '');
    if (customSujetInput) customSujetInput.style.display = 'none';
    document.getElementById('editQSujet').value = sujetSel.value;
  }
}

function onEditQThematiqueSelectChange() {
  const themaSel = document.getElementById('editQThematiqueSelect');
  const customThemaInput = document.getElementById('editQThematiqueCustom');
  const isCustom = (themaSel.value === '__NEW__');
  if (customThemaInput) customThemaInput.style.display = isCustom ? 'block' : 'none';

  if (!isCustom) {
    document.getElementById('editQThematique').value = themaSel.value;
    if (themaSel.value === 'Identité') {
      document.getElementById('editQClasse').value = '8';
      const curType = document.getElementById('editQType').value;
      if (curType !== 'P' && curType !== 'T') {
        document.getElementById('editQType').value = 'P';
      }
    }
  } else {
    document.getElementById('editQThematique').value = customThemaInput ? customThemaInput.value.trim() : '';
  }

  updateModalSujetsDropdown(themaSel.value === 'Identité' ? 'Identité' : null);
  toggleConfigReponsesSection();
}

function onEditQSujetSelectChange() {
  const sujetSel = document.getElementById('editQSujetSelect');
  const customSujetInput = document.getElementById('editQSujetCustom');
  const isCustom = (sujetSel.value === '__NEW__');
  if (customSujetInput) customSujetInput.style.display = isCustom ? 'block' : 'none';

  if (!isCustom) {
    document.getElementById('editQSujet').value = sujetSel.value;
  } else {
    document.getElementById('editQSujet').value = customSujetInput ? customSujetInput.value.trim() : '';
  }
}

function populateEditQNQuestLieSelect(currentQid = null, selectedParentId = 0) {
  const sel = document.getElementById('editQNQuestLie');
  if (!sel) return;
  sel.innerHTML = '<option value="0">0 - Aucune (Question principale indépendante)</option>';

  const candidates = state.questions.filter(q => q.id !== currentQid);
  candidates.sort((a, b) => (a.thematique || '').localeCompare(b.thematique || '') || a.id - b.id);

  candidates.forEach(q => {
    const opt = document.createElement('option');
    opt.value = q.id;
    const subCountTxt = q.subquestions_count > 0 ? ` [${q.subquestions_count} s-q]` : '';
    const cleanText = (q.texte || '').substring(0, 45) + ((q.texte || '').length > 45 ? '...' : '');
    opt.textContent = `#${q.id} [${q.thematique}] ${cleanText}${subCountTxt}`;
    if (q.id === selectedParentId) {
      opt.selected = true;
    }
    sel.appendChild(opt);
  });
}

function openAddQuestionModal() {
  document.getElementById('editQId').value = '';
  document.getElementById('editQModalTitle').textContent = 'Créer une nouvelle question';
  document.getElementById('editQIdBadge').textContent = 'Nouveau';

  // Initialisation des listes déroulantes de thématique et sujet
  populateModalThematiques('Identité', 'Identité');
  populateEditQNQuestLieSelect(null, 0);
  document.getElementById('editQClasse').value = '8';
  document.getElementById('editQType').value = 'P';
  document.getElementById('editQCible').value = '0';
  document.getElementById('editQTexte').value = '';

  // Configuration par défaut en mode sélection
  document.getElementById('modeReponseSelect').checked = true;
  document.getElementById('modeReponseNumeric').checked = false;
  document.getElementById('cfgSelectOptions').value = '';
  document.getElementById('cfgNumericUnit').value = '';
  document.getElementById('cfgNumericMin').value = '';
  document.getElementById('cfgNumericMax').value = '';
  document.getElementById('cfgNumericStep').value = '1';

  switchReponseMode('select');
  toggleConfigReponsesSection();

  const delBtn = document.getElementById('btnDeleteQuestion');
  if (delBtn) delBtn.style.display = 'none';

  const submitBtn = document.getElementById('btnSubmitQuestionForm');
  if (submitBtn) submitBtn.textContent = 'Créer la question';

  document.getElementById('modalEditQuestion').style.display = 'flex';
}

function openEditQuestionModal(qid) {
  const q = state.questions.find(item => item.id === qid) || (state.pendingQuestions || []).find(item => item.id === qid);
  if (!q) return;

  document.getElementById('editQId').value = q.id;
  document.getElementById('editQModalTitle').textContent = 'Modifier la question';
  document.getElementById('editQIdBadge').textContent = `#${q.id}`;

  populateModalThematiques(q.thematique, q.sujet);
  populateEditQNQuestLieSelect(q.id, q.n_quest_lie || 0);
  document.getElementById('editQClasse').value = q.classe ?? 1;
  document.getElementById('editQType').value = (q.type === 'MULTI' ? 'M' : (q.type || 'M'));
  document.getElementById('editQCible').value = q.cible ?? 0;
  document.getElementById('editQTexte').value = q.texte;

  // Configuration des réponses si existante
  let cfg = null;
  if (q.config_reponses) {
    try {
      cfg = typeof q.config_reponses === 'string' ? JSON.parse(q.config_reponses) : q.config_reponses;
    } catch (e) {
      console.warn("Erreur parsing config_reponses:", e);
    }
  }

  if (cfg && cfg.mode === 'numeric') {
    document.getElementById('modeReponseNumeric').checked = true;
    document.getElementById('modeReponseSelect').checked = false;
    document.getElementById('cfgNumericUnit').value = cfg.unit || '';
    document.getElementById('cfgNumericMin').value = cfg.min ?? '';
    document.getElementById('cfgNumericMax').value = cfg.max ?? '';
    document.getElementById('cfgNumericStep').value = cfg.step ?? '1';
    document.getElementById('cfgSelectOptions').value = '';
    switchReponseMode('numeric');
  } else {
    document.getElementById('modeReponseSelect').checked = true;
    document.getElementById('modeReponseNumeric').checked = false;
    const opts = (cfg && Array.isArray(cfg.options)) ? cfg.options.join('\n') : '';
    document.getElementById('cfgSelectOptions').value = opts;
    document.getElementById('cfgNumericUnit').value = '';
    document.getElementById('cfgNumericMin').value = '';
    document.getElementById('cfgNumericMax').value = '';
    document.getElementById('cfgNumericStep').value = '1';
    switchReponseMode('select');
  }

  toggleConfigReponsesSection();

  const delBtn = document.getElementById('btnDeleteQuestion');
  if (delBtn) delBtn.style.display = 'inline-flex';

  const submitBtn = document.getElementById('btnSubmitQuestionForm');
  if (submitBtn) submitBtn.textContent = 'Enregistrer les modifications';

  document.getElementById('modalEditQuestion').style.display = 'flex';
}

function toggleConfigReponsesSection() {
  const tp = document.getElementById('editQType').value;
  let cl = parseInt(document.getElementById('editQClasse').value, 10);
  const infoMulti = document.getElementById('infoTypeMulti');
  const infoGouts = document.getElementById('infoTypeGouts');
  const boxIdentity = document.getElementById('boxConfigIdentityAnswers');
  const iconId = document.getElementById('configIdentityIcon');
  const titleId = document.getElementById('configIdentityTitle');
  const lblNum = document.getElementById('labelModeNumeric');
  const lblSel = document.getElementById('labelModeSelect');
  const hintT = document.getElementById('hintModeSelectT');

  // Ajustement de cohérence entre le type et la classe
  if (tp === 'P' || tp === 'T') {
    document.getElementById('editQClasse').value = '8';
    cl = 8;
    const themaSel = document.getElementById('editQThematiqueSelect');
    if (themaSel && themaSel.value !== 'Identité' && themaSel.value !== '__NEW__') {
      themaSel.value = 'Identité';
      onEditQThematiqueSelectChange();
    }
  } else if (cl === 8 && (tp === 'M' || tp === 'G')) {
    document.getElementById('editQClasse').value = '1';
    cl = 1;
  }

  // Adaptation de la section des réponses selon le type
  if (tp === 'M') {
    if (infoMulti) infoMulti.style.display = 'block';
    if (infoGouts) infoGouts.style.display = 'none';
    if (boxIdentity) boxIdentity.style.display = 'none';
  } else if (tp === 'G') {
    if (infoMulti) infoMulti.style.display = 'none';
    if (infoGouts) infoGouts.style.display = 'block';
    if (boxIdentity) boxIdentity.style.display = 'none';
  } else if (tp === 'P') {
    if (infoMulti) infoMulti.style.display = 'none';
    if (infoGouts) infoGouts.style.display = 'none';
    if (boxIdentity) boxIdentity.style.display = 'block';
    if (iconId) iconId.textContent = '👤';
    if (titleId) titleId.textContent = 'Gestion des Réponses Précises : Type P (+ sur moi)';
    if (lblNum) lblNum.textContent = 'Valeur numérique exacte';
    if (lblSel) lblSel.textContent = 'Liste de choix fermée';
    if (hintT) hintT.style.display = 'none';
  } else if (tp === 'T') {
    if (infoMulti) infoMulti.style.display = 'none';
    if (infoGouts) infoGouts.style.display = 'none';
    if (boxIdentity) boxIdentity.style.display = 'block';
    if (iconId) iconId.textContent = '👥';
    if (titleId) titleId.textContent = 'Gestion des Réponses Tolérances : Type T (+ sur l\'autre)';
    if (lblNum) lblNum.textContent = 'Plage de tolérance (Min/Max)';
    if (lblSel) lblSel.textContent = 'Options multiples à cocher';
    if (hintT) hintT.style.display = 'block';
  }
}

function switchReponseMode(mode) {
  const numBox = document.getElementById('configModeNumeric');
  const selBox = document.getElementById('configModeSelect');
  if (numBox && selBox) {
    if (mode === 'numeric') {
      numBox.style.display = 'block';
      selBox.style.display = 'none';
    } else {
      numBox.style.display = 'none';
      selBox.style.display = 'block';
    }
  }
}

window.onEditQThematiqueSelectChange = onEditQThematiqueSelectChange;
window.onEditQSujetSelectChange = onEditQSujetSelectChange;

// Statistiques
async function loadStats() {
  try {
    const res = await fetch(`${API_BASE}/api/stats`);
    const data = await res.json();
    state.stats = data;
    updateStatsDisplay();
    updateIdentityCompletionBadge();
  } catch (err) {
    console.error(err);
  }
}

function updateStatsDisplay() {
  const pCount = document.getElementById('statProfilesCount');
  const qCount = document.getElementById('statQuestionsCount');
  const aCount = document.getElementById('statAnswersCount');
  const cCount = document.getElementById('statCardsCount');

  if (pCount) pCount.textContent = state.profiles.length;
  if (qCount) qCount.textContent = state.questions.length;
  if (aCount) aCount.textContent = state.stats.answers_count || 0;
  if (cCount) {
    const ready = state.profiles.filter(p => p.has_identity).length;
    cCount.textContent = ready;
  }
}

// Live Clock pour la Montre
function startLiveClock() {
  setInterval(() => {
    const d = new Date();
    const h = String(d.getHours()).padStart(2, '0');
    const m = String(d.getMinutes()).padStart(2, '0');
    const el = document.getElementById('watchClock');
    if (el) el.textContent = `${h}:${m}`;
  }, 1000);
}

function updateDevicesPreview() {
  const active = state.profiles.find(p => p.id === state.activeProfileId);
  const nameEl = document.getElementById('phoneActiveName');
  if (nameEl && active) {
    nameEl.textContent = active.prenom || active.pseudo;
  }
}

function triggerPhoneSync() {
  showToast('📱 Synchronisation Mobile & Windows effectuée avec succès !');
}

// Toast
function showToast(message) {
  const toast = document.getElementById('toastNotification');
  if (!toast) return;
  toast.innerHTML = `<span>✨</span> ${message}`;
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3500);
}


// ============================================================================
// GESTION DE L'ESPACE D'ARBITRAGE DU JEU 3 (PROPOSITIONS EN ATTENTE)
// ============================================================================

async function switchBankView(view) {
  const activeContainer = document.getElementById('bankViewActiveContainer');
  const arbitrageContainer = document.getElementById('bankViewArbitrageContainer');
  const btnActive = document.getElementById('btnViewBankActive');
  const btnArbitrage = document.getElementById('btnViewBankArbitrage');

  if (view === 'active') {
    if (activeContainer) activeContainer.style.display = 'block';
    if (arbitrageContainer) arbitrageContainer.style.display = 'none';
    if (btnActive) {
      btnActive.classList.add('active');
      btnActive.style.background = 'rgba(56,189,248,0.12)';
      btnActive.style.borderColor = 'rgba(56,189,248,0.3)';
      btnActive.style.color = 'var(--text-main)';
    }
    if (btnArbitrage) {
      btnArbitrage.classList.remove('active');
      btnArbitrage.style.background = 'rgba(245,158,11,0.08)';
      btnArbitrage.style.borderColor = 'rgba(245,158,11,0.3)';
      btnArbitrage.style.color = '#f59e0b';
    }
    await loadQuestions();
    resetBankFilters();
  } else if (view === 'arbitrage') {
    if (activeContainer) activeContainer.style.display = 'none';
    if (arbitrageContainer) arbitrageContainer.style.display = 'block';
    if (btnActive) {
      btnActive.classList.remove('active');
      btnActive.style.background = 'transparent';
      btnActive.style.borderColor = 'transparent';
      btnActive.style.color = 'var(--text-muted)';
    }
    if (btnArbitrage) {
      btnArbitrage.classList.add('active');
      btnArbitrage.style.background = 'rgba(245,158,11,0.2)';
      btnArbitrage.style.borderColor = '#f59e0b';
      btnArbitrage.style.color = '#fbbf24';
    }
    // Par défaut afficher toutes les questions à arbitrer sans filtre résiduel
    const s = document.getElementById('pendingSearchInput');
    if (s) s.value = '';
    const fc = document.getElementById('pendingFilterClasse');
    if (fc) fc.value = 'ALL';
    const ft = document.getElementById('pendingFilterType');
    if (ft) ft.value = 'ALL';
    const fcb = document.getElementById('pendingFilterCible');
    if (fcb) fcb.value = 'ALL';

    await loadPendingQuestions();
  }
}

function resetBankFilters() {
  const sInput = document.getElementById('bankSearchInput');
  if (sInput) sInput.value = '';
  const bThema = document.getElementById('bankFilterThematique');
  if (bThema) bThema.value = 'ALL';
  updateBankSujetsDropdown();
  const bSujet = document.getElementById('bankFilterSujet');
  if (bSujet) bSujet.value = 'ALL';
  const bClasse = document.getElementById('bankFilterClasse');
  if (bClasse) bClasse.value = 'ALL';
  const bCible = document.getElementById('bankFilterCible');
  if (bCible) bCible.value = 'ALL';
  const bHier = document.getElementById('bankFilterHierarchie');
  if (bHier) bHier.value = 'ALL';
  renderQuestionsTable();
}

function resetPendingFilters() {
  const s = document.getElementById('pendingSearchInput');
  if (s) s.value = '';
  const fc = document.getElementById('pendingFilterClasse');
  if (fc) fc.value = 'ALL';
  const ft = document.getElementById('pendingFilterType');
  if (ft) ft.value = 'ALL';
  const fcb = document.getElementById('pendingFilterCible');
  if (fcb) fcb.value = 'ALL';
  renderPendingQuestionsTable();
}
window.resetPendingFilters = resetPendingFilters;

async function loadPendingQuestions() {
  try {
    const res = await fetch(`${API_BASE}/api/admin/questions/pending`);
    if (!res.ok) return;
    const data = await res.json();
    state.pendingQuestions = data.pending_questions || data.questions || [];

    // Mise à jour des KPI et badges
    const badgePending = document.getElementById('badgePendingQuestionsCount');
    if (badgePending) {
      badgePending.textContent = `${data.total} en attente`;
      if (data.total === 0) {
        badgePending.style.background = 'rgba(16,185,129,0.2)';
        badgePending.style.color = '#34d399';
        badgePending.style.borderColor = 'rgba(16,185,129,0.3)';
        badgePending.textContent = '✅ À jour (0)';
      } else {
        badgePending.style.background = 'rgba(245,158,11,0.25)';
        badgePending.style.color = '#fbbf24';
        badgePending.style.borderColor = 'rgba(245,158,11,0.4)';
      }
    }

    const kpiContainer = document.getElementById('kpiArbitrageContainer');
    if (kpiContainer) {
      const counts = data.counts_by_class || {};
      const classeNames = {
        '1': 'Cl. 1 (Standards)',
        '2': 'Cl. 2 (Personnelles)',
        '3': 'Cl. 3 (Intimes)',
        '4': 'Cl. 4 (Privées)',
        '5': 'Cl. 5 (Sexuel)',
        '9': 'Cl. 9 (Fantasmes)'
      };
      let kpiHtml = `
        <div style="background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3); border-radius: var(--radius-sm); padding: 10px 14px; text-align: center; min-width: 90px;">
          <div style="font-size: 20px; font-weight: 800; color: #fbbf24;" id="kpiPendingTotal">${data.total}</div>
          <div style="font-size: 11px; color: var(--text-muted); font-weight: 600;">Total en attente</div>
        </div>
      `;
      for (const [cl, cnt] of Object.entries(counts)) {
        kpiHtml += `
          <div style="background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.3); border-radius: var(--radius-sm); padding: 10px 14px; text-align: center; min-width: 90px;">
            <div style="font-size: 20px; font-weight: 800; color: #c084fc;">${cnt}</div>
            <div style="font-size: 11px; color: var(--text-muted); font-weight: 600;">${classeNames[cl] || 'Classe ' + cl}</div>
          </div>
        `;
      }
      kpiContainer.innerHTML = kpiHtml;
    }

    const btnBatchAll = document.getElementById('btnBatchValidateAll');
    if (btnBatchAll) btnBatchAll.textContent = `🌟 Tout valider (${data.total} questions)`;

    renderPendingQuestionsTable();
  } catch (err) {
    console.error("Erreur chargement questions en attente:", err);
  }
}

function renderPendingQuestionsTable() {
  const tbody = document.getElementById('pendingQuestionsTableBody');
  if (!tbody) return;

  const searchTerm = (document.getElementById('pendingSearchInput')?.value || '').toLowerCase().trim();
  const filterClasse = document.getElementById('pendingFilterClasse')?.value || 'ALL';
  const filterType = document.getElementById('pendingFilterType')?.value || 'ALL';
  const filterCible = document.getElementById('pendingFilterCible')?.value || 'ALL';

  const filtered = (state.pendingQuestions || []).filter(q => {
    if (filterClasse !== 'ALL' && String(q.classe) !== String(filterClasse)) return false;
    if (filterType !== 'ALL' && String(q.type).toUpperCase() !== String(filterType).toUpperCase()) return false;
    if (filterCible !== 'ALL' && String(q.cible) !== String(filterCible)) return false;
    if (searchTerm) {
      const matchText = (q.texte || '').toLowerCase().includes(searchTerm);
      const matchSujet = (q.sujet || '').toLowerCase().includes(searchTerm);
      const matchThema = (q.thematique || '').toLowerCase().includes(searchTerm);
      const matchId = String(q.id).includes(searchTerm);
      if (!matchText && !matchSujet && !matchThema && !matchId) return false;
    }
    return true;
  });

  const countBadge = document.getElementById('pendingFilteredCountBadge');
  if (countBadge) {
    countBadge.textContent = `${filtered.length} proposition${filtered.length > 1 ? 's' : ''}`;
  }

  if (filtered.length === 0) {
    const emptyMsg = state.pendingQuestions.length === 0
      ? '🎉 <strong>Toutes les propositions ont été arbitrées !</strong><br><span style="font-size:12.5px; opacity:0.8;">Aucune question en attente de révision. Elles sont désormais actives dans la banque officielle.</span>'
      : '🔍 Aucune proposition ne correspond aux filtres sélectionnés.';
    tbody.innerHTML = `
      <tr>
        <td colspan="8" style="text-align:center; padding: 48px 16px; color: var(--text-dim); font-size: 14.5px;">
          ${emptyMsg}
        </td>
      </tr>`;
    return;
  }

  tbody.innerHTML = filtered.map(q => {
    // Badge de classe
    let classeBadgeHtml = '';
    if (q.classe === 1) {
      classeBadgeHtml = `<span class="badge-tag" style="background: rgba(56,189,248,0.22); color: #38bdf8; border: 1px solid rgba(56,189,248,0.4); font-weight:600;">1 - Standards</span>`;
    } else if (q.classe === 2) {
      classeBadgeHtml = `<span class="badge-tag" style="background: rgba(16,185,129,0.22); color: #34d399; border: 1px solid rgba(16,185,129,0.4); font-weight:600;">2 - Personnelles</span>`;
    } else if (q.classe === 3) {
      classeBadgeHtml = `<span class="badge-tag" style="background: rgba(245,158,11,0.22); color: #fbbf24; border: 1px solid rgba(245,158,11,0.4); font-weight:600;">3 - Intimes</span>`;
    } else if (q.classe === 4) {
      classeBadgeHtml = `<span class="badge-tag" style="background: rgba(236,72,153,0.22); color: #f472b6; border: 1px solid rgba(236,72,153,0.4); font-weight:600;">4 - Privées</span>`;
    } else if (q.classe === 5) {
      classeBadgeHtml = `<span class="badge-tag" style="background: rgba(139,92,246,0.22); color: #c084fc; border: 1px solid rgba(139,92,246,0.4); font-weight:600;">5 - Sexuel</span>`;
    } else if (q.classe === 9) {
      classeBadgeHtml = `<span class="badge-tag" style="background: rgba(244,63,94,0.22); color: #fb7185; border: 1px solid rgba(244,63,94,0.4); font-weight:600;">9 - Fantasmes</span>`;
    } else {
      classeBadgeHtml = `<span class="badge-tag">Classe ${q.classe}</span>`;
    }

    // Badge de type
    const typeBadgeHtml = q.type === 'M'
      ? `<span class="badge-tag type" title="Question à 4 axes (V, A, D, P)">Multi-Axes (M)</span>`
      : `<span class="badge-tag type" style="background: rgba(56,189,248,0.18); color: #38bdf8;" title="Question à échelle unique d'accord (Goût)">Goût (G)</span>`;

    // Badge de cible
    const cibleBadgeHtml = q.cible === 0 
      ? '<span class="badge-tag" style="background:rgba(148,163,184,0.15); color:#cbd5e1;">Mixte (0)</span>'
      : (q.cible === 1 
          ? '<span class="badge-tag" style="background:rgba(56,189,248,0.15); color:#38bdf8;">Homme (1)</span>'
          : '<span class="badge-tag" style="background:rgba(236,72,153,0.15); color:#f472b6;">Femme (2)</span>');

    const sujetLabel = (q.n_sujet !== undefined && q.n_sujet !== null && q.n_sujet > 0)
      ? `<span class="badge-tag" style="font-size:10px; padding:2px 6px; margin-right:4px; opacity:0.85;">#${q.n_sujet}</span>${q.sujet}`
      : q.sujet;

    return `
      <tr id="row-pending-${q.id}">
        <td><strong style="color: var(--accent-amber);">#${q.id}</strong></td>
        <td>${classeBadgeHtml}</td>
        <td>${typeBadgeHtml}</td>
        <td>${cibleBadgeHtml}</td>
        <td><span style="font-size:12.5px; color: var(--text-main);">${sujetLabel}</span></td>
        <td style="line-height: 1.45; font-weight: 500;">${q.texte}</td>
        <td>
          <span class="badge-soft" style="background: rgba(245,158,11,0.15); color: #fbbf24; font-size: 11px; padding: 3px 8px; border: 1px solid rgba(245,158,11,0.3); border-radius: 4px;">
            ⏳ En attente
          </span>
        </td>
        <td style="text-align:right; white-space:nowrap;">
          <div style="display: inline-flex; gap: 6px; align-items: center;">
            <select id="select-pack-${q.id}" class="custom-select" style="padding: 4px 6px; font-size: 11px; font-weight: 600; min-width: 76px; background: rgba(255,255,255,0.06);" title="Choisir le Jeu auquel affecter la question">
              <option value="3" ${q.pack_id === 3 ? 'selected' : ''}>Jeu 3</option>
              <option value="1" ${q.pack_id === 1 ? 'selected' : ''}>Jeu 1</option>
              <option value="2" ${q.pack_id === 2 ? 'selected' : ''}>Jeu 2</option>
            </select>
            <button class="btn btn-sm" onclick="validatePendingQuestion(${q.id})" style="background: #10b981; color: #fff; border: none; padding: 5px 10px; font-weight: 600; cursor: pointer; border-radius: 6px;" title="Valider dans le jeu sélectionné">
              ✅ Valider
            </button>
            <button class="btn btn-sm btn-outline" onclick="openEditQuestionModal(${q.id})" style="padding: 5px 8px; border-radius: 6px;" title="Modifier le libellé, le sujet ou la cible avant validation">
              ✏️
            </button>
            <button class="btn btn-sm" onclick="deletePendingQuestion(${q.id})" style="background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.35); padding: 5px 8px; cursor: pointer; border-radius: 6px;" title="Supprimer définitivement cette proposition">
              🗑️
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

async function validatePendingQuestion(qid) {
  const packSelect = document.getElementById(`select-pack-${qid}`);
  const packId = packSelect ? parseInt(packSelect.value, 10) : 3;
  try {
    const res = await fetch(`${API_BASE}/api/admin/questions/${qid}/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pack_id: packId })
    });
    if (!res.ok) throw new Error('Erreur lors de la validation de la question');
    const data = await res.json();
    showToast(`✅ Question #${qid} validée et affectée au Jeu ${packId} !`);
    await loadPendingQuestions();
    await loadQuestions();
  } catch (err) {
    alert(err.message);
  }
}

async function deletePendingQuestion(qid) {
  if (confirm(`Confirmez-vous la suppression définitive de la proposition #${qid} ?`)) {
    try {
      const res = await fetch(`${API_BASE}/api/questions/${qid}`, {
        method: 'DELETE'
      });
      if (!res.ok) throw new Error('Erreur lors de la suppression');
      showToast(`🗑️ Proposition #${qid} supprimée.`);
      await loadPendingQuestions();
    } catch (err) {
      alert(err.message);
    }
  }
}

async function handleBatchValidation(action) {
  const batchPackSelect = document.getElementById('selectBatchTargetPack');
  const targetPack = batchPackSelect ? parseInt(batchPackSelect.value, 10) : 3;

  let confirmMsg = `Confirmez-vous la validation de l'ensemble des ${state.pendingQuestions.length} questions en attente dans le Jeu ${targetPack} ?`;
  if (!confirm(confirmMsg)) return;

  try {
    const res = await fetch(`${API_BASE}/api/admin/questions/validate-batch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'all', pack_id: targetPack })
    });
    if (!res.ok) throw new Error('Erreur lors de la validation par lot');
    const data = await res.json();
    const countVal = (data.count !== undefined) ? data.count : (data.validated_count || 0);
    showToast(`🎉 ${countVal} question(s) validée(s) et activée(s) avec succès !`);
    await loadPendingQuestions();
    await loadQuestions();
  } catch (err) {
    alert(err.message);
  }
}

// Exposition globale sur window pour accessibilité universelle
window.openIdentityDeck = openIdentityDeck;
window.switchIdentityDeckTab = switchIdentityDeckTab;
window.renderIdentityDeckQuestions = renderIdentityDeckQuestions;
window.handleSelfAnswerChange = handleSelfAnswerChange;
window.handlePartnerIndifferentToggle = handlePartnerIndifferentToggle;
window.handlePartnerRangeChange = handlePartnerRangeChange;
window.handlePartnerCheckChange = handlePartnerCheckChange;
window.openProfileCockpitDirect = openProfileCockpitDirect;
window.exitToProfilesList = exitToProfilesList;
window.copyMyAffId = copyMyAffId;
window.closeModals = closeModals;
window.openAddQuestionModal = openAddQuestionModal;
window.openEditQuestionModal = openEditQuestionModal;
window.toggleConfigReponsesSection = toggleConfigReponsesSection;
window.switchReponseMode = switchReponseMode;
window.onEditQThematiqueSelectChange = onEditQThematiqueSelectChange;
window.onEditQSujetSelectChange = onEditQSujetSelectChange;


window.switchBankView = switchBankView;
window.loadPendingQuestions = loadPendingQuestions;
window.renderPendingQuestionsTable = renderPendingQuestionsTable;
window.validatePendingQuestion = validatePendingQuestion;
window.deletePendingQuestion = deletePendingQuestion;
window.handleBatchValidation = handleBatchValidation;
window.resetPendingFilters = resetPendingFilters;
window.renderQuestionsDeck = renderQuestionsDeck;
window.resetBankFilters = resetBankFilters;

