# Script de mise à jour de frontend/app.js pour Suivi-ARP001
import os

def run_update():
    app_js_path = os.path.join(os.path.dirname(__file__), 'frontend', 'app.js')
    with open(app_js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    helper_block = '''// Helpers pour calcul d'âge et validation de cohérence
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
  if (age < 18) return { age, error: '⚠️ Âge minimum requis : 18 ans pour s\\'inscrire.' };
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

function updateIdentityCompletionBadge() {
  const badgeCockpit = document.getElementById('ckpIdentityCompletion');
  const badgeModal = document.getElementById('modalIdentityCompletion');
  const curProf = getActiveProfile();

  if (!curProf || curProf.role === 'admin') {
    if (badgeCockpit) badgeCockpit.textContent = 'Admin (Non requis)';
    if (badgeModal) badgeModal.textContent = 'Admin (Non requis)';
    return;
  }

  const identityQuestions = state.questions.filter(q => q.classe === 0 || q.classe === '0');
  if (identityQuestions.length === 0) {
    if (badgeCockpit) badgeCockpit.textContent = '100%';
    if (badgeModal) badgeModal.textContent = '100%';
    return;
  }

  let answeredCount = 0;
  identityQuestions.forEach(q => {
    let answered = false;
    if (q.type === 'G') {
      if (state.answersMap[`${q.id}_G`] !== undefined && state.answersMap[`${q.id}_G`] !== 0) answered = true;
    } else {
      ['V', 'A', 'D', 'P'].forEach(ax => {
        if (state.answersMap[`${q.id}_${ax}`] !== undefined && state.answersMap[`${q.id}_${ax}`] !== 0) answered = true;
      });
    }
    if (answered) answeredCount++;
  });

  const pct = Math.round((answeredCount / identityQuestions.length) * 100);
  const text = `${answeredCount}/${identityQuestions.length} (${pct}%)`;
  if (badgeCockpit) badgeCockpit.textContent = text;
  if (badgeModal) badgeModal.textContent = text;
}

function openIdentityQuestions() {
  const curProf = getActiveProfile();
  if (curProf && curProf.role === 'admin') {
    showToast("👑 En tant qu'administrateur, vous supervisez le système et ne répondez pas aux questionnaires personnels.");
    return;
  }
  closeModals();
  switchTab('questionnaire');
  const filterClasse = document.getElementById('qFilterClasse');
  if (filterClasse) {
    filterClasse.value = '0';
  }
  const qProfSelect = document.getElementById('qSelectProfile');
  if (qProfSelect && state.activeProfileId) {
    qProfSelect.value = state.activeProfileId;
  }
  renderQuestionsDeck();
  const deck = document.getElementById('questionsDeck');
  if (deck) {
    deck.scrollIntoView({ behavior: 'smooth' });
  }
  showToast("📋 Questionnaire de Classe 0 - Identité activé.");
}
'''

    if 'function calculateAgeFromBirthDate' not in content:
        content = helper_block + '\n' + content
        print('Added helper functions block')

    if 'setupBirthDateValidation();' not in content:
        content = content.replace('function initEventListeners() {', 'function initEventListeners() {\n  setupBirthDateValidation();')
        print('Added setupBirthDateValidation call in initEventListeners')

    old_modal_submit_body = """      date_naissance: document.getElementById('idDateNaiss')?.value || '',
      ville: document.getElementById('idVille')?.value.trim() || '',"""

    new_modal_submit_body = """      date_naissance: document.getElementById('idDateNaiss')?.value || '',
      pays_naissance: document.getElementById('idPaysNaissance')?.value.trim() || '',
      habite_pays: document.getElementById('idHabitePays')?.value.trim() || '',
      habite_region_dept: document.getElementById('idHabiteRegion')?.value.trim() || '',
      habite_commune: document.getElementById('idHabiteCommune')?.value.trim() || '',
      travail_pays: document.getElementById('idTravailPays')?.value.trim() || '',
      travail_region_dept: document.getElementById('idTravailRegion')?.value.trim() || '',
      travail_commune: document.getElementById('idTravailCommune')?.value.trim() || '',
      ville: document.getElementById('idHabiteCommune')?.value.trim() || document.getElementById('idVille')?.value.trim() || '',"""

    if old_modal_submit_body in content:
        content = content.replace(old_modal_submit_body, new_modal_submit_body)
        print('Updated formIdentityCard submit fields')

    old_cockpit_submit_body = """        date_naissance: document.getElementById('ckpInputBirth')?.value || '',
        ville: document.getElementById('ckpInputCity')?.value.trim() || '',"""

    new_cockpit_submit_body = """        date_naissance: document.getElementById('ckpInputBirth')?.value || '',
        pays_naissance: document.getElementById('ckpInputPaysNaissance')?.value.trim() || '',
        habite_pays: document.getElementById('ckpHabitePays')?.value.trim() || '',
        habite_region_dept: document.getElementById('ckpHabiteRegion')?.value.trim() || '',
        habite_commune: document.getElementById('ckpHabiteCommune')?.value.trim() || '',
        travail_pays: document.getElementById('ckpTravailPays')?.value.trim() || '',
        travail_region_dept: document.getElementById('ckpTravailRegion')?.value.trim() || '',
        travail_commune: document.getElementById('ckpTravailCommune')?.value.trim() || '',
        ville: document.getElementById('ckpHabiteCommune')?.value.trim() || document.getElementById('ckpInputCity')?.value.trim() || '',"""

    if old_cockpit_submit_body in content:
        content = content.replace(old_cockpit_submit_body, new_cockpit_submit_body)
        print('Updated formDirectCockpit submit fields')

    old_res_err = "if (!res.ok) throw new Error('Erreur lors de la sauvegarde de la fiche d\\'identité');"
    new_res_err = "if (!res.ok) { const errD = await res.json().catch(() => ({})); throw new Error(errD.error || 'Erreur lors de la sauvegarde de la fiche d\\'identité'); }"
    content = content.replace(old_res_err, new_res_err)

    old_pop_cockpit = """  if (fBirth) fBirth.value = p.date_naissance || '';
  if (fCity) fCity.value = p.ville || '';"""

    new_pop_cockpit = """  if (fBirth) {
    fBirth.value = p.date_naissance || '';
    updateDateInputAgeFeedback(fBirth, document.getElementById('ckpAgeBadge'), document.getElementById('ckpAgeFeedback'));
  }
  const fPaysNaiss = document.getElementById('ckpInputPaysNaissance');
  const fHabPays = document.getElementById('ckpHabitePays');
  const fHabReg = document.getElementById('ckpHabiteRegion');
  const fHabCom = document.getElementById('ckpHabiteCommune');
  const fTravPays = document.getElementById('ckpTravailPays');
  const fTravReg = document.getElementById('ckpTravailRegion');
  const fTravCom = document.getElementById('ckpTravailCommune');

  if (fPaysNaiss) fPaysNaiss.value = p.pays_naissance || '';
  if (fHabPays) fHabPays.value = p.habite_pays || (p.habite_commune || p.ville ? 'France' : '');
  if (fHabReg) fHabReg.value = p.habite_region_dept || '';
  if (fHabCom) fHabCom.value = p.habite_commune || p.ville || '';
  if (fTravPays) fTravPays.value = p.travail_pays || '';
  if (fTravReg) fTravReg.value = p.travail_region_dept || '';
  if (fTravCom) fTravCom.value = p.travail_commune || '';
  if (fCity) fCity.value = p.habite_commune || p.ville || '';
  updateIdentityCompletionBadge();"""

    if old_pop_cockpit in content:
        content = content.replace(old_pop_cockpit, new_pop_cockpit)
        print('Updated renderSingleUserProfile population')

    old_pop_modal = """    document.getElementById('idDateNaiss').value = card.date_naissance || '';
    document.getElementById('idVille').value = card.ville || '';"""

    new_pop_modal = """    const modBirth = document.getElementById('idDateNaiss');
    if (modBirth) {
      modBirth.value = card.date_naissance || '';
      updateDateInputAgeFeedback(modBirth, document.getElementById('modalAgeBadge'), document.getElementById('modalAgeFeedback'));
    }
    const mPaysNaiss = document.getElementById('idPaysNaissance');
    const mHabPays = document.getElementById('idHabitePays');
    const mHabReg = document.getElementById('idHabiteRegion');
    const mHabCom = document.getElementById('idHabiteCommune');
    const mTravPays = document.getElementById('idTravailPays');
    const mTravReg = document.getElementById('idTravailRegion');
    const mTravCom = document.getElementById('idTravailCommune');

    if (mPaysNaiss) mPaysNaiss.value = card.pays_naissance || '';
    if (mHabPays) mHabPays.value = card.habite_pays || (card.habite_commune || card.ville ? 'France' : '');
    if (mHabReg) mHabReg.value = card.habite_region_dept || '';
    if (mHabCom) mHabCom.value = card.habite_commune || card.ville || '';
    if (mTravPays) mTravPays.value = card.travail_pays || '';
    if (mTravReg) mTravReg.value = card.travail_region_dept || '';
    if (mTravCom) mTravCom.value = card.travail_commune || '';
    const mCity = document.getElementById('idVille');
    if (mCity) mCity.value = card.habite_commune || card.ville || '';
    updateIdentityCompletionBadge();"""

    if old_pop_modal in content:
        content = content.replace(old_pop_modal, new_pop_modal)
        print('Updated openIdentityCardModal population')

    old_cl_filter = "const clOk = allClasses || allowedClassIds.includes(q.classe);"
    new_cl_filter = "const clOk = allClasses || allowedClassIds.map(String).includes(String(q.classe)) || q.classe === 0 || q.classe === '0';"
    if old_cl_filter in content:
        content = content.replace(old_cl_filter, new_cl_filter)
        print('Updated getActiveProfileEligibleQuestions for classe 0')

    content = content.replace("0: '0 - Non définie'", "0: '0 - Identité'")
    content = content.replace("0: 'Non définie'", "0: 'Identité'")

    content = content.replace('updateProgressBar();', 'updateProgressBar();\n  updateIdentityCompletionBadge();')
    content = content.replace('updateStatsDisplay();', 'updateStatsDisplay();\n    updateIdentityCompletionBadge();')

    with open(app_js_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print('frontend/app.js mis à jour avec succès.')

if __name__ == '__main__':
    run_update()
