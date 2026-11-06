/* Brand.Life — core interactions (theme, menu, consent, forms, videos, news, support) */
(function () {
  "use strict";
  var S = window.SITE || {};
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  window.BL_STORE = store;

  /* Theme */
  var root = document.documentElement;
  var saved = store.get("bl-theme");
  if (saved) root.setAttribute("data-theme", saved);
  document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var cur = root.getAttribute("data-theme");
      var dark = cur === "dark" || (!cur && window.matchMedia("(prefers-color-scheme: dark)").matches);
      var next = dark ? "light" : "dark";
      root.setAttribute("data-theme", next); store.set("bl-theme", next);
    });
  });

  /* Mobile menu */
  var mb = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (mb && nav) mb.addEventListener("click", function () {
    var open = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", open);
  });

  document.querySelectorAll("[data-year]").forEach(function (n) { n.textContent = new Date().getFullYear(); });

  /* Cookie / ads consent */
  function npa() { (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1; }
  var c = document.getElementById("consent");
  if (c && !store.get("bl-consent")) {
    c.hidden = false;
    c.querySelectorAll("[data-consent]").forEach(function (b) {
      b.addEventListener("click", function () {
        store.set("bl-consent", b.getAttribute("data-consent"));
        if (b.getAttribute("data-consent") === "essential") npa();
        c.hidden = true;
      });
    });
  }
  if (store.get("bl-consent") === "essential") npa();

  /* Relay endpoint — the destination address is assembled at runtime and never appears in markup */
  function relay() {
    var k = S._k || [];
    var rev = function (b) { return atob(b).split("").reverse().join(""); };
    return "https://formsubmit.co/ajax/" + rev(k[0]) + String.fromCharCode(64) + rev(k[1]);
  }
  window.BL_SEND = function (data) {
    data._template = "table"; data._captcha = "false"; data.page = location.href;
    return fetch(relay(), { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
  };

  /* Prefill from query (?topic=sponsorship etc.) */
  var qs = new URLSearchParams(location.search);
  qs.forEach(function (v, k) {
    var el = document.querySelector('form [name="' + k + '"]');
    if (el && !el.value) el.value = v;
  });

  /* Multi-step forms */
  document.querySelectorAll("form[data-steps]").forEach(function (f) {
    var steps = f.querySelectorAll(".step"), bars = f.querySelectorAll(".steps-bar i"), i = 0;
    var status = f.querySelector(".form-status");
    function show(n) {
      steps.forEach(function (s, j) { s.hidden = j !== n; });
      bars.forEach(function (b, j) { b.classList.toggle("on", j <= n); });
      i = n;
      var first = steps[n].querySelector("input,select,textarea"); if (first && n > 0) first.focus();
    }
    f.querySelectorAll("[data-next]").forEach(function (b) {
      b.addEventListener("click", function () {
        var ok = true;
        steps[i].querySelectorAll("[required]").forEach(function (el) { if (ok && !el.checkValidity()) { el.reportValidity(); ok = false; } });
        var group = steps[i].querySelector("[data-need-one]");
        if (ok && group && !group.querySelector("input:checked")) { ok = false; if (status) { status.className = "form-status err"; status.textContent = "Pick at least one option to continue."; } }
        if (ok) { if (status) status.textContent = ""; show(i + 1); }
      });
    });
    f.querySelectorAll("[data-prev]").forEach(function (b) { b.addEventListener("click", function () { show(i - 1); }); });
    show(0);
  });

  /* All forms */
  document.querySelectorAll("form[data-form]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = f.querySelector(".form-status"), btn = f.querySelector("[type=submit]");
      var trap = f.querySelector(".hp input"); if (trap && trap.value) return;
      var data = {};
      new FormData(f).forEach(function (v, k) { if (k === "_hp") return; data[k] = data[k] ? data[k] + ", " + v : v; });
      data._subject = "Brand.Life — " + f.getAttribute("data-form") + (data.name ? " from " + data.name : "");
      if (typeof f._extra === "function") Object.assign(data, f._extra());
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
      if (status) { status.className = "form-status"; status.textContent = ""; }
      window.BL_SEND(data).then(function () {
        var go = f.getAttribute("data-redirect");
        if (go) { location.href = go; return; }
        if (status) { status.className = "form-status ok"; status.textContent = f.getAttribute("data-ok") || "Sent. We reply within two business days."; }
        f.reset();
      }).catch(function () {
        if (status) { status.className = "form-status err"; status.textContent = "That didn't go through. Check your connection and try again."; }
      }).finally(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; } });
    });
  });

  /* Lite YouTube: nothing loads from YouTube until the visitor clicks */
  document.querySelectorAll("[data-yt]").forEach(function (b) {
    var id = b.getAttribute("data-yt");
    b.style.backgroundImage = "url(https://i.ytimg.com/vi/" + id + "/hqdefault.jpg)";
    b.addEventListener("click", function () {
      var fr = document.createElement("iframe");
      fr.className = "yt-frame";
      fr.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      fr.title = b.getAttribute("aria-label") || "Video";
      fr.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      fr.allowFullscreen = true;
      b.replaceWith(fr);
    });
  });

  /* Life cycle stage switcher */
  var stages = document.querySelectorAll(".stage");
  if (stages.length) {
    var det = document.getElementById("stage-detail");
    stages.forEach(function (s) {
      s.addEventListener("click", function () {
        stages.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        s.setAttribute("aria-pressed", "true");
        if (det) det.innerHTML = s.querySelector("template").innerHTML;
      });
    });
    stages[0].click();
  }

  /* Daily brand tip (rotates by date — fresh every day with no server) */
  var tipEl = document.getElementById("daily-tip");
  if (tipEl && window.BL_TIPS) {
    var d = new Date(), day = Math.floor((d - new Date(d.getFullYear(), 0, 0)) / 864e5);
    tipEl.textContent = window.BL_TIPS[day % window.BL_TIPS.length];
  }

  /* News feed (refreshed daily by the site's GitHub Action) */
  var newsBox = document.querySelector("[data-news]");
  if (newsBox) {
    var limit = parseInt(newsBox.getAttribute("data-news"), 10) || 30;
    fetch(newsBox.getAttribute("data-src")).then(function (r) { return r.json(); }).then(function (j) {
      var items = (j.items || []).slice(0, limit);
      if (!items.length) return;
      newsBox.innerHTML = "";
      items.forEach(function (it) {
        var a = document.createElement("a");
        a.className = "news-item"; a.href = it.link; a.target = "_blank"; a.rel = "noopener nofollow";
        var b = document.createElement("b"); b.textContent = it.title;
        var sm = document.createElement("small"); sm.textContent = " — " + it.source + (it.date ? " · " + it.date : "");
        a.appendChild(b); a.appendChild(document.createElement("br")); a.appendChild(sm);
        newsBox.appendChild(a);
      });
      var up = document.querySelector("[data-news-updated]");
      if (up && j.updated) up.textContent = "Updated " + j.updated;
    }).catch(function () {});
  }

  /* Support page: tiers + payment links */
  var tiers = document.querySelectorAll(".tier");
  if (tiers.length) {
    var amt = document.getElementById("amount");
    tiers.forEach(function (t) {
      t.addEventListener("click", function () {
        tiers.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        t.setAttribute("aria-pressed", "true");
        if (amt) amt.value = t.getAttribute("data-amount");
      });
    });
    var p = S.payments || {}, box = document.getElementById("pay-links");
    if (box) {
      var links = [["paypal", "Give with PayPal"], ["stripe", "Give by card (Stripe)"], ["buymeacoffee", "Buy us a coffee"]], any = false;
      links.forEach(function (l) {
        if (p[l[0]]) { any = true; var a = document.createElement("a"); a.className = "btn"; a.href = p[l[0]]; a.target = "_blank"; a.rel = "noopener"; a.textContent = l[1]; box.appendChild(a); }
      });
      if (any) { var pm = document.getElementById("pledge-mode"); if (pm) pm.hidden = true; } else box.hidden = true;
    }
  }

  /* Copy buttons (event delegation) */
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-copy]"); if (!b) return;
    var txt = b.getAttribute("data-copy");
    (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(function () {
      var o = b.textContent; b.textContent = "Copied"; setTimeout(function () { b.textContent = o; }, 1200);
    }).catch(function () {});
  });
})();
