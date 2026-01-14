    function closeFlash(){
        const overlay = document.getElementById("flashOverlay");
        if (!overlay) return;
        overlay.style.opacity = "0";
        setTimeout(() => overlay.remove(), 200);

        // Nettoie l’URL
        const url = new URL(window.location.href);
        url.searchParams.delete("activated");
        window.history.replaceState({}, "", url);
    }

document.addEventListener("DOMContentLoaded", () => {
  // =========================
  // 1) TOGGLE CONNEXION / INSCRIPTION
  // =========================
  const tabs = document.querySelectorAll(".tab-header .tab");
  const connexionForm = document.getElementById("connexionForm");
  const inscriptionForm = document.getElementById("inscriptionForm");

    (function () {
        const params = new URLSearchParams(window.location.search);
        if (params.get("activated") === "1") {
        // active l’onglet connexion
        const tabConn = document.querySelector('.tab[data-target="#inscriptionForm"]');
        if (tabConn) tabConn.click();
        }
    })();

  function showForm(targetSelector) {
    if (!connexionForm || !inscriptionForm) return;

    const showConnexion = targetSelector === "#connexionForm";
    connexionForm.style.display = showConnexion ? "block" : "none";
    inscriptionForm.style.display = showConnexion ? "none" : "block";

    tabs.forEach((t) => t.classList.remove("active"));
    const activeTab = Array.from(tabs).find((t) => t.dataset.target === targetSelector);
    if (activeTab) activeTab.classList.add("active");
  }

  // État initial: tab.active sinon connexion
  const initialTab = document.querySelector(".tab-header .tab.active");
  showForm(initialTab?.dataset.target || "#connexionForm");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => showForm(tab.dataset.target));
  });

  // =========================
  // 2) INSCRIPTION: VALIDATIONS + AVAILABILITY
  // =========================
  if (!inscriptionForm) return;

  const API_BASE = "https://api.budgoapp.com";
  const AVAIL_URL = `${API_BASE}/auth/availability`;
  const REGISTER_URL = `${API_BASE}/auth/register`;

  const usernameInput = inscriptionForm.querySelector("#username");
  const emailInput = inscriptionForm.querySelector("#email");
  const passwordInput = inscriptionForm.querySelector("#password");
  const confirmInput = inscriptionForm.querySelector("#password_confirm");
  const submitBtn = inscriptionForm.querySelector("button[type='submit']");

  // Sécurité si un élément manque
  if (!usernameInput || !emailInput || !passwordInput || !confirmInput || !submitBtn) return;

  // Utilise TES spans .error-msg déjà présents
  function errorSpanFor(inputEl) {
    const group = inputEl.closest(".input-group");
    if (!group) return null;
    return group.querySelector(".error-msg");
  }

  const usernameErr = errorSpanFor(usernameInput);
  const emailErr = errorSpanFor(emailInput);
  const passwordErr = errorSpanFor(passwordInput);
  const confirmErr = errorSpanFor(confirmInput);

  function setError(span, msg) {
    if (!span) return;
    span.textContent = msg || "";
    span.style.display = msg ? "block" : "none";
  }

  function isEmailValid(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function hasErrors() {
    return Boolean(
      (usernameErr && usernameErr.textContent) ||
      (emailErr && emailErr.textContent) ||
      (passwordErr && passwordErr.textContent) ||
      (confirmErr && confirmErr.textContent)
    );
  }

  function refreshSubmit() {
    const filled =
      usernameInput.value.trim().length >= 3 &&
      isEmailValid(emailInput.value.trim()) &&
      passwordInput.value.length >= 8 &&
      confirmInput.value.length >= 8 &&
      passwordInput.value === confirmInput.value;

    submitBtn.disabled = !filled || hasErrors();
  }

  // Cache tous les messages au load
  [usernameErr, emailErr, passwordErr, confirmErr].forEach((s) => setError(s, ""));

  // Validations locales
  function validateLocal() {
    const u = usernameInput.value.trim();
    const e = emailInput.value.trim();
    const p = passwordInput.value;
    const c = confirmInput.value;

    // Username
    if (u.length === 0) setError(usernameErr, "");
    else if (u.length < 3) setError(usernameErr, "Pseudo trop court (min 3)");
    else setError(usernameErr, ""); // l’API décidera si pris

    // Email
    if (e.length === 0) setError(emailErr, "");
    else if (!isEmailValid(e)) setError(emailErr, "Email invalide");
    else setError(emailErr, ""); // l’API décidera si pris

    // Password
    if (p.length === 0) setError(passwordErr, "");
    else if (p.length < 8) setError(passwordErr, "Mot de passe trop court (min 8)");
    else setError(passwordErr, "");

    // Confirm
    if (c.length === 0) setError(confirmErr, "");
    else if (c !== p) setError(confirmErr, "Les mots de passe ne matchent pas");
    else setError(confirmErr, "");

    refreshSubmit();
  }

  // Availability API avec debounce + abort
  let debounceTimer = null;
  let controller = null;

    async function checkAvailability() {
    const u = usernameInput.value.trim();
    const e = emailInput.value.trim();

    const canCheckUsername = u.length >= 3;
    const canCheckEmail = isEmailValid(e);

    // Si rien n'est checkable, on ne tape pas l'API
    if (!canCheckUsername && !canCheckEmail) {
        // Nettoie les erreurs si champ vide (optionnel mais agréable)
        if (u.length === 0) setError(usernameErr, "");
        if (e.length === 0) setError(emailErr, "");

        refreshSubmit();
        return;
    }

    // Abort requête précédente
    if (controller) controller.abort();
    controller = new AbortController();

    try {
        const params = new URLSearchParams();
        if (canCheckUsername) params.set("username", u);
        if (canCheckEmail) params.set("email", e);

        const res = await fetch(`${AVAIL_URL}?${params.toString()}`, {
        method: "GET",
        signal: controller.signal,
        headers: { "Accept": "application/json" },
        });

        if (!res.ok) throw new Error(`availability_http_${res.status}`);

        const data = await res.json();

        // N'affiche une erreur que pour ce qui a été checké
        if (canCheckUsername) {
        setError(usernameErr, data.username_available ? "" : "Pseudo déjà utilisé");
        } else if (u.length === 0) {
        setError(usernameErr, "");
        }

        if (canCheckEmail) {
        setError(emailErr, data.email_available ? "" : "Email déjà utilisé");
        } else if (e.length === 0) {
        setError(emailErr, "");
        }

        refreshSubmit();
    } catch (err) {
        if (err.name === "AbortError") return;

        if (canCheckUsername) setError(usernameErr, "Erreur vérification");
        if (canCheckEmail) setError(emailErr, "Erreur vérification");
        submitBtn.disabled = true;
    }
    }


  function debounceAvailability() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(checkAvailability, 300);
  }

  // Listeners
  usernameInput.addEventListener("input", () => {
    validateLocal();
    debounceAvailability();
  });

  emailInput.addEventListener("input", () => {
    validateLocal();
    debounceAvailability();
  });

  passwordInput.addEventListener("input", validateLocal);
  confirmInput.addEventListener("input", validateLocal);

  // =========================
  // 3) SUBMIT INSCRIPTION: POST /auth/register
  // =========================
    inscriptionForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    validateLocal();
    if (submitBtn.disabled) return;
    if (hasErrors()) return;

    submitBtn.disabled = true;

    const payload = {
        username: usernameInput.value.trim(),
        email: emailInput.value.trim(),
        password: passwordInput.value,
    };

    try {
        const res = await fetch(REGISTER_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        body: JSON.stringify(payload),
        });

        const data = await res.json().catch(() => ({}));

        if (res.ok && data && (data.ok === true || data.success === true)) {
        window.location.href = "log.php?registered=1";
        return;
        }

        let msg = "Erreur inscription";

        if (res.status === 409) {
        if (data?.detail?.errors) {
            msg = Object.values(data.detail.errors).join(" • ");
        } else {
            msg = (data && (data.detail || data.message)) || "Pseudo ou email déjà utilisé";
        }
        } else if (res.status === 422) {
        msg = "Champs invalides. Vérifie le formulaire.";
        } else {
        msg = (data && (data.detail || data.message)) || "Erreur inscription";
        }

        window.location.href = "log.php?regerr=" + encodeURIComponent(msg);
        return;

    } catch (err) {
        window.location.href = "log.php?regerr=" + encodeURIComponent("Erreur réseau. Réessaie.");
        return;
    } finally {
        refreshSubmit();
    }
    });


  // Init
  validateLocal();
});