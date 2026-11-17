/* PartPro — formulaire en 3 étapes.
   Envoi principal : Formspree (xkoadead → conseil@partpro.fr).
   Copie de secours : Netlify Forms (formulaire "lead-partpro"), visible dans Netlify > Forms
   une fois la détection de formulaires activée. Si l'une des deux voies échoue, l'autre suffit. */
(function () {
  var FORMSPREE = "https://formspree.io/f/xkoadead";

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function init(form) {
    var steps = $all(".fstep", form);
    var bars = $all(".progress span", form);
    var label = $(".steplabel", form);
    var err = $(".ferr", form);
    var prev = $(".js-prev", form);
    var next = $(".js-next", form);
    var send = $(".js-send", form);
    var current = 0;
    var names = ["Votre projet", "Votre logement", "Vos coordonnées"];

    var pre = form.getAttribute("data-projet");
    if (pre) {
      var r = form.querySelector('input[name="projet"][value="' + pre + '"]');
      if (r) r.checked = true;
    }

    function show(i) {
      current = i;
      steps.forEach(function (s, k) { s.hidden = k !== i; });
      bars.forEach(function (b, k) { b.classList.toggle("on", k <= i); });
      label.textContent = "Étape " + (i + 1) + " sur " + steps.length + " · " + names[i];
      prev.hidden = i === 0;
      next.hidden = i === steps.length - 1;
      send.hidden = i !== steps.length - 1;
      err.textContent = "";
    }

    function val(name) {
      var el = form.querySelector('[name="' + name + '"]:checked') || form.querySelector('[name="' + name + '"]:not([type=radio])');
      return el ? (el.value || "").trim() : "";
    }

    function check(i) {
      if (i === 0) {
        if (!val("projet")) return "Choisissez le type de projet.";
        if (!val("statut")) return "Indiquez si vous êtes propriétaire ou locataire.";
      }
      if (i === 1) {
        if (!val("logement")) return "Choisissez maison ou appartement.";
        if (!/^\d{5}$/.test(val("code_postal"))) return "Entrez un code postal à 5 chiffres.";
      }
      if (i === 2) {
        if (!val("prenom")) return "Entrez votre prénom.";
        var tel = val("telephone").replace(/[\s.\-]/g, "");
        if (!/^(\+33|0)[1-9]\d{8}$/.test(tel)) return "Entrez un numéro de téléphone valide (ex. 06 12 34 56 78).";
        var mail = val("email");
        if (mail && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)) return "L'adresse email semble incomplète.";
        if (!form.querySelector('[name="consentement"]').checked) return "Cochez la case pour qu'on puisse vous rappeler.";
      }
      return "";
    }

    $all('input[name="statut"]', form).forEach(function (r) {
      r.addEventListener("change", function () {
        var n = $(".js-locataire", form);
        if (n) n.hidden = val("statut") !== "Locataire";
      });
    });

    next.addEventListener("click", function () {
      var m = check(current);
      if (m) { err.textContent = m; return; }
      show(current + 1);
      form.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    prev.addEventListener("click", function () { show(current - 1); });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector('[name="_gotcha"]').value) return;
      var m = check(2);
      if (m) { err.textContent = m; return; }
      send.disabled = true;
      send.textContent = "Envoi en cours…";

      var data = {
        projet: val("projet"), statut: val("statut"), logement: val("logement"),
        chauffage: val("chauffage"), facture: val("facture"), code_postal: val("code_postal"),
        prenom: val("prenom"), nom: val("nom"), telephone: val("telephone"), email: val("email"),
        creneau: val("creneau"), message: val("message"),
        page: location.pathname, consentement: "oui"
      };
      var fd = new FormData();
      Object.keys(data).forEach(function (k) { fd.append(k, data[k]); });
      fd.append("_subject", "Nouveau lead PartPro : " + data.projet + " (" + data.code_postal + ") " + data.prenom);
      if (data.email) fd.append("_replyto", data.email);

      var nfBody = "form-name=lead-partpro&" + Object.keys(data).map(function (k) {
        return encodeURIComponent(k) + "=" + encodeURIComponent(data[k]);
      }).join("&");

      var p1 = fetch(FORMSPREE, { method: "POST", body: fd, headers: { Accept: "application/json" } })
        .then(function (r) { return r.ok; }).catch(function () { return false; });
      var p2 = fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: nfBody })
        .then(function (r) { return r.ok; }).catch(function () { return false; });

      Promise.all([p1, p2]).then(function (res) {
        if (res[0] || res[1]) {
          form.hidden = true;
          var done = form.parentNode.querySelector(".done");
          done.hidden = false;
          var who = done.querySelector(".js-who");
          if (who) who.textContent = data.prenom;
        } else {
          send.disabled = false;
          send.textContent = "Envoyer ma demande";
          err.textContent = "L'envoi n'a pas marché (connexion ?). Réessayez ou appelez le 06 98 97 71 80.";
        }
      });
    });

    show(0);
  }

  $all("form.ppform").forEach(init);
})();
