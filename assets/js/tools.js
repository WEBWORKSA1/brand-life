/* Brand.Life — free brand tools. Everything runs in the visitor's browser; nothing is sent anywhere
   unless the visitor submits a form. Each tool initialises only when its container is on the page. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var cap = function (s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : s; };
  var pick = function (a) { return a[Math.floor(Math.random() * a.length)]; };
  var shuffle = function (a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; };
  var store = window.BL_STORE || { get: function () { return null; }, set: function () {} };
  var clean = function (s) { return String(s || "").toLowerCase().replace(/[^a-z]/g, ""); };

  /* ---------- Name scoring (shared by generator + tester) ---------- */
  function syllables(w) {
    w = clean(w); if (!w) return 0; if (w.length <= 3) return 1;
    w = w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, "").replace(/^y/, "");
    var m = w.match(/[aeiouy]{1,2}/g); return m ? m.length : 1;
  }
  function scoreName(name) {
    var w = clean(name), notes = [], s = 100;
    var raw = String(name || "");
    if (!w) return { score: 0, notes: ["Type a name to test."], parts: {} };
    var len = w.length, syl = syllables(w);
    var lenPts = len >= 4 && len <= 9 ? 25 : len <= 12 ? 17 : len < 4 ? 15 : 8;
    if (len > 12) notes.push("Long names are harder to remember and to type — aim for 4–9 letters.");
    if (len < 4) notes.push("Very short names are memorable but almost always taken as .com domains and trademarks.");
    var sylPts = syl <= 3 ? 20 : syl === 4 ? 12 : 6;
    if (syl > 3) notes.push("More than three syllables tends to get shortened by customers — decide the nickname before they do.");
    var spell = 25, hard = [];
    if (/(ph|ck|ae|ough|eigh|kn|wr|gh)/.test(w)) { spell -= 7; hard.push("spellings that sound different from how they look"); }
    if (/([a-z])\1\1/.test(w)) { spell -= 8; hard.push("triple letters"); }
    if (/q(?!u)/.test(w) || /[xzq]{2,}/.test(w)) { spell -= 6; hard.push("unusual letter clusters"); }
    if (/[^aeiouy]{4,}/.test(w)) { spell -= 8; hard.push("four or more consonants in a row"); }
    if (/[0-9\-_]/.test(raw)) { spell -= 8; hard.push("numbers or hyphens"); }
    if (hard.length) notes.push("Radio test risk: " + hard.join(", ") + ". If you said it on a podcast, would people type it right?");
    spell = Math.max(spell, 0);
    var v = (w.match(/[aeiouy]/g) || []).length / len;
    var flow = v >= 0.3 && v <= 0.6 ? 15 : v >= 0.2 ? 9 : 4;
    if (v < 0.25) notes.push("Few vowels make a name hard to say. Try adding an open vowel sound.");
    var punch = /^[bcdgkptv]/.test(w) ? 15 : /^[fjlmnrsz]/.test(w) ? 11 : 8;
    if (/^[bcdgkptv]/.test(w)) notes.push("Opens on a hard consonant (b, d, g, k, p, t) — these tend to sound confident and stick.");
    s = lenPts + sylPts + spell + flow + punch;
    if (!notes.length) notes.push("Clean, sayable and easy to spell. Next: check the .com and run a trademark search.");
    return { score: Math.min(100, s), notes: notes, parts: { Length: lenPts / 25, Rhythm: sylPts / 20, Spelling: spell / 25, Flow: flow / 15, Punch: punch / 15 } };
  }
  window.BL_scoreName = scoreName;

  /* ---------- 1. Brand Name Generator ---------- */
  var ng = $("#name-gen");
  if (ng) {
    var SUF = ["ly", "ify", "io", "hub", "lab", "loop", "nest", "forge", "wise", "kit", "stack", "flow", "ster", "able", "verse", "craft", "works", "base", "mint", "spark"];
    var PRE = ["go", "get", "my", "try", "up", "re", "true", "bright", "bold", "neo", "omni", "one", "pure", "every", "pro"];
    var SYL1 = ["ka", "zo", "lu", "ve", "ri", "no", "ta", "mi", "sa", "do", "be", "fi", "ra", "lo", "ne", "vi", "ko", "pa"];
    var SYL2 = ["ra", "lin", "vo", "na", "ro", "ta", "lex", "mo", "via", "ly", "rix", "ten", "sa", "ri", "vo", "no", "za", "on"];
    var IND = {
      tech: ["byte", "node", "grid", "pixel", "logic", "cloud", "signal", "core"], food: ["crumb", "spoon", "harvest", "pantry", "zest", "ember", "basil", "olive"],
      wellness: ["bloom", "breathe", "calm", "glow", "vital", "root", "sage", "pulse"], fashion: ["thread", "seam", "loom", "velvet", "atelier", "stitch", "drape", "hue"],
      finance: ["ledger", "vault", "mint", "coin", "summit", "anchor", "yield", "north"], creative: ["canvas", "studio", "ink", "frame", "muse", "palette", "draft", "lens"],
      home: ["hearth", "nook", "haven", "oak", "brick", "nest", "porch", "lumen"], services: ["bridge", "harbor", "keystone", "compass", "beacon", "craft", "path", "guild"]
    };
    var fav = []; try { fav = JSON.parse(store.get("bl-fav-names") || "[]"); } catch (e) {}
    function blend(a, b) { if (a.length < 3 || b.length < 3) return a + b; return a.slice(0, Math.ceil(a.length * 0.6)) + b.slice(Math.floor(b.length * 0.4)); }
    function invent() { return pick(SYL1) + pick(SYL2) + (Math.random() < 0.3 ? pick(["a", "o", "i", ""]) : ""); }
    function gen() {
      var kws = ($("#ng-kw").value || "").split(/[,\s]+/).map(clean).filter(Boolean);
      var ind = IND[$("#ng-ind").value] || [];
      var styles = $$("#name-gen input[name=style]:checked").map(function (x) { return x.value; });
      if (!styles.length) styles = ["compound", "blend", "invented", "prefix"];
      var pool = kws.concat(ind).filter(Boolean); if (!pool.length) pool = ["brand", "life", "spark", "north"];
      var out = {};
      var tries = 0;
      while (Object.keys(out).length < 24 && tries < 400) {
        tries++;
        var st = pick(styles), a = pick(pool), b = pick(pool), n = "";
        if (st === "compound") n = a === b ? a + pick(SUF) : (Math.random() < 0.5 ? a + b : a + pick(SUF));
        else if (st === "blend") n = blend(a, b === a ? pick(ind.length ? ind : SUF) : b);
        else if (st === "invented") n = Math.random() < 0.5 ? invent() : a.slice(0, 3) + pick(SYL2);
        else if (st === "prefix") n = pick(PRE) + a;
        else if (st === "real") n = a.length > 3 ? a + pick(["", "", " & Co", " House", " Supply", " Studio"]) : a + pick(SUF);
        n = n.replace(/\s+/g, " ").trim();
        if (n.length < 3 || n.length > 16) continue;
        out[cap(n)] = 1;
      }
      render(Object.keys(out));
    }
    function render(names) {
      var box = $("#ng-out");
      box.innerHTML = names.map(function (n) {
        var sc = scoreName(n).score, slug = clean(n);
        return '<div class="pill-out"><span><b>' + esc(n) + '</b> <small class="muted">score ' + sc + '</small></span><span>' +
          '<a class="copy" href="https://www.namecheap.com/domains/registration/results/?domain=' + slug + '.com" target="_blank" rel="noopener nofollow">Check .com</a> ' +
          '<button class="copy" type="button" data-fav="' + esc(n) + '">★ Save</button></span></div>';
      }).join("");
    }
    function renderFav() {
      var f = $("#ng-fav"); if (!f) return;
      f.innerHTML = fav.length ? fav.map(function (n) { return '<span class="tag">' + esc(n) + "</span>"; }).join("") + ' <button class="copy" type="button" id="ng-clear">Clear</button>' : '<span class="muted">Tap ★ Save on names you like — they stay on this device.</span>';
    }
    ng.addEventListener("submit", function (e) { e.preventDefault(); gen(); });
    document.addEventListener("click", function (e) {
      var b = e.target.closest("[data-fav]"); if (b) { var n = b.getAttribute("data-fav"); if (fav.indexOf(n) < 0) fav.push(n); store.set("bl-fav-names", JSON.stringify(fav)); renderFav(); b.textContent = "★ Saved"; }
      if (e.target.id === "ng-clear") { fav = []; store.set("bl-fav-names", "[]"); renderFav(); }
    });
    renderFav(); gen();
  }

  /* ---------- 2. Name Tester ---------- */
  var nt = $("#name-test");
  if (nt) {
    var run = function () {
      var r = scoreName($("#nt-name").value);
      $("#nt-score").textContent = r.score;
      $("#nt-meter").style.width = r.score + "%";
      $("#nt-parts").innerHTML = Object.keys(r.parts).map(function (k) { return '<div><small>' + k + '</small><div class="meter"><i style="width:' + Math.round(r.parts[k] * 100) + '%"></i></div></div>'; }).join("");
      $("#nt-notes").innerHTML = r.notes.map(function (n) { return "<li>" + esc(n) + "</li>"; }).join("");
      var slug = clean($("#nt-name").value);
      $("#nt-links").innerHTML = slug ? '<a class="btn small alt" target="_blank" rel="noopener nofollow" href="https://www.namecheap.com/domains/registration/results/?domain=' + slug + '.com">Check ' + slug + '.com</a> <a class="btn small alt" target="_blank" rel="noopener" href="https://tmsearch.uspto.gov/search/search-information">US trademark search</a> <a class="btn small alt" target="_blank" rel="noopener" href="https://www.wipo.int/branddb/en/">WIPO Global Brand Database</a>' : "";
    };
    nt.addEventListener("input", run); nt.addEventListener("submit", function (e) { e.preventDefault(); run(); }); run();
  }

  /* ---------- 3. Tagline Generator ---------- */
  var tg = $("#tagline-gen");
  if (tg) {
    var T = {
      bold: ["{B}. Built to {V}.", "Stop settling. Start {V}.", "The {N} {A} deserve.", "{V} harder. {V} smarter.", "No compromises. Just {N}.", "Made for {A} who {V}."],
      warm: ["{N}, made with care.", "Here for every {A}.", "Where {A} feel at home.", "A little {N}, every day.", "Because {A} deserve {N}.", "{B}: {N} that feels like you."],
      clever: ["{N}? Consider it handled.", "Less fuss. More {N}.", "{V} now. Thank us later.", "The secret to {N} isn't a secret anymore.", "Your {N}, minus the headache.", "We sweat the {N} so you don't."],
      premium: ["{N}, refined.", "The art of {N}.", "Crafted for {A} who expect more.", "Quietly exceptional {N}.", "{B}. Nothing less.", "Where {N} becomes an experience."],
      simple: ["{N} made simple.", "{N} for {A}.", "Better {N}. Every day.", "{V} with {B}.", "Simply {N}.", "{N}, done right."]
    };
    var runT = function (e) {
      if (e) e.preventDefault();
      var B = $("#tg-brand").value.trim() || "Your brand", N = ($("#tg-benefit").value.trim() || "great results").toLowerCase(), A = ($("#tg-aud").value.trim() || "people").toLowerCase(), V = ($("#tg-verb").value.trim() || "grow").toLowerCase();
      var tone = $("#tg-tone").value; var list = tone === "mix" ? shuffle([].concat(T.bold, T.warm, T.clever, T.premium, T.simple)).slice(0, 12) : T[tone];
      $("#tg-out").innerHTML = list.map(function (t) {
        var s = t.replace(/\{B\}/g, B).replace(/\{N\}/g, N).replace(/\{A\}/g, A).replace(/\{V\}/g, V);
        s = s.charAt(0).toUpperCase() + s.slice(1);
        return '<div class="pill-out"><b>' + esc(s) + '</b><button class="copy" type="button" data-copy="' + esc(s) + '">Copy</button></div>';
      }).join("");
    };
    tg.addEventListener("submit", runT); runT();
  }

  /* ---------- 4. Color Palette Generator + contrast check ---------- */
  function hexToHsl(h) {
    h = h.replace("#", ""); if (h.length === 3) h = h.split("").map(function (c) { return c + c; }).join("");
    var r = parseInt(h.substr(0, 2), 16) / 255, g = parseInt(h.substr(2, 2), 16) / 255, b = parseInt(h.substr(4, 2), 16) / 255;
    var mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, s = 0, hh = 0, d = mx - mn;
    if (d) { s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn); hh = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; hh *= 60; }
    return [hh, s * 100, l * 100];
  }
  function hslToHex(h, s, l) {
    h = ((h % 360) + 360) % 360; s = Math.max(0, Math.min(100, s)) / 100; l = Math.max(0, Math.min(100, l)) / 100;
    var k = function (n) { return (n + h / 30) % 12; }, a = s * Math.min(l, 1 - l);
    var f = function (n) { return Math.round(255 * (l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1))))).toString(16).padStart(2, "0"); };
    return "#" + f(0) + f(8) + f(4);
  }
  function lum(hex) {
    var c = hex.replace("#", "").match(/../g).map(function (x) { x = parseInt(x, 16) / 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  }
  function contrast(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
  window.BL_contrast = contrast;
  var pal = $("#palette");
  if (pal) {
    var buildPal = function () {
      var base = $("#pl-base").value, mode = $("#pl-mode").value, hsl = hexToHsl(base), h = hsl[0], s = hsl[1], l = hsl[2], cols;
      if (mode === "analogous") cols = [[h - 30, s, l], [h - 15, s, l + 8], [h, s, l], [h + 15, s, l - 8], [h + 30, s, l]];
      else if (mode === "complementary") cols = [[h, s, Math.min(l + 30, 94)], [h, s, l], [h, s, Math.max(l - 22, 10)], [h + 180, s, l], [h + 180, s * 0.4, 94]];
      else if (mode === "triadic") cols = [[h, s, l], [h + 120, s, l], [h + 240, s, l], [h, s * 0.25, 95], [h, s * 0.4, 12]];
      else if (mode === "split") cols = [[h, s, l], [h + 150, s, l], [h + 210, s, l], [h, 20, 96], [h, 25, 14]];
      else cols = [[h, s, 95], [h, s, 78], [h, s, l], [h, s, Math.max(l - 20, 14)], [h, s, Math.max(l - 38, 7)]];
      var hexes = cols.map(function (c) { return hslToHex(c[0], c[1], c[2]); });
      var names = ["Background", "Soft", "Primary", "Accent", "Deep"];
      $("#pl-out").innerHTML = hexes.map(function (x, i) {
        var tc = contrast(x, "#ffffff") > contrast(x, "#111111") ? "#fff" : "#111";
        return '<div class="sw" style="background:' + x + ';color:' + tc + '" data-copy="' + x + '" title="Click to copy">' + names[i] + "<br>" + x.toUpperCase() + "</div>";
      }).join("");
      $("#pl-contrast").innerHTML = "<tr><th>Color</th><th>On white</th><th>On black</th><th>Body text (AA 4.5)</th></tr>" + hexes.map(function (x) {
        var w = contrast(x, "#ffffff"), k = contrast(x, "#000000");
        return "<tr><td><code>" + x.toUpperCase() + "</code></td><td>" + w.toFixed(2) + "</td><td>" + k.toFixed(2) + "</td><td>" + (w >= 4.5 ? "✓ on white" : k >= 4.5 ? "✓ on black" : "Headlines only") + "</td></tr>";
      }).join("");
      var css = ":root{\n" + hexes.map(function (x, i) { return "  --brand-" + names[i].toLowerCase() + ": " + x + ";"; }).join("\n") + "\n}";
      $("#pl-css").textContent = css; $("#pl-copy").setAttribute("data-copy", css);
    };
    pal.addEventListener("input", buildPal);
    $("#pl-random").addEventListener("click", function () { $("#pl-base").value = hslToHex(Math.random() * 360, 55 + Math.random() * 35, 38 + Math.random() * 20); buildPal(); });
    buildPal();
  }

  /* ---------- 5. Font Pairing Explorer ---------- */
  var fp = $("#fonts");
  if (fp) {
    var PAIRS = [
      ["Playfair Display", "Source Sans 3", "Editorial, luxury, hospitality"], ["Fraunces", "Manrope", "Warm modern, lifestyle, food"],
      ["Space Grotesk", "Inter", "Tech, SaaS, fintech"], ["DM Serif Display", "DM Sans", "Agencies, consultancies"],
      ["Bricolage Grotesque", "Public Sans", "Creators, startups"], ["Cormorant Garamond", "Montserrat", "Fashion, beauty, weddings"],
      ["Archivo Black", "Archivo", "Sports, fitness, bold retail"], ["Libre Baskerville", "Lato", "Law, finance, education"],
      ["Syne", "Work Sans", "Art, culture, events"], ["Outfit", "Nunito Sans", "Wellness, kids, community"],
      ["Bebas Neue", "Roboto", "Entertainment, media, events"], ["Lora", "Open Sans", "Nonprofits, publishing, health"]
    ];
    var loaded = {};
    var load = function (f) { if (loaded[f]) return; loaded[f] = 1; var l = document.createElement("link"); l.rel = "stylesheet"; l.href = "https://fonts.googleapis.com/css2?family=" + f.replace(/ /g, "+") + ":wght@400;700&display=swap"; document.head.appendChild(l); };
    var sel = $("#fp-pair");
    sel.innerHTML = PAIRS.map(function (p, i) { return '<option value="' + i + '">' + p[0] + " + " + p[1] + " — " + p[2] + "</option>"; }).join("");
    var show = function () {
      var p = PAIRS[sel.value]; load(p[0]); load(p[1]);
      var txt = $("#fp-text").value || "Brands live in the details";
      $("#fp-h").style.fontFamily = '"' + p[0] + '",serif'; $("#fp-h").textContent = txt;
      $("#fp-b").style.fontFamily = '"' + p[1] + '",sans-serif';
      var embed = '<link href="https://fonts.googleapis.com/css2?family=' + p[0].replace(/ /g, "+") + ':wght@400;700&family=' + p[1].replace(/ /g, "+") + ':wght@400;700&display=swap" rel="stylesheet">';
      $("#fp-code").textContent = embed + "\nh1,h2,h3{font-family:'" + p[0] + "',serif}\nbody{font-family:'" + p[1] + "',sans-serif}";
      $("#fp-copy").setAttribute("data-copy", $("#fp-code").textContent);
    };
    fp.addEventListener("input", show); fp.addEventListener("change", show); show();
  }

  /* ---------- 6. Brand Archetype Quiz ---------- */
  var AR = {
    innocent: ["The Innocent", "Optimism, simplicity, honesty.", "Clear, positive, reassuring.", "Whites, soft pastels, sky blue", "Natural food, baby care, wholesome wellness brands"],
    sage: ["The Sage", "Truth, expertise, understanding.", "Measured, evidence-led, generous with knowledge.", "Navy, deep green, parchment", "Research firms, education, news and search tools"],
    explorer: ["The Explorer", "Freedom, discovery, self-reliance.", "Adventurous, candid, outward-looking.", "Earth tones, forest, sunset orange", "Outdoor gear, travel, off-road vehicles"],
    outlaw: ["The Outlaw", "Disruption, rebellion, liberation.", "Provocative, unfiltered, defiant.", "Black, blood red, chrome", "Motorcycles, challenger brands, streetwear"],
    magician: ["The Magician", "Transformation, vision, wonder.", "Inspiring, mysterious, future-focused.", "Deep purple, midnight, iridescent", "Entertainment, beauty, breakthrough tech"],
    hero: ["The Hero", "Mastery, courage, achievement.", "Direct, motivating, confident.", "Bold red, black, high-contrast primaries", "Sportswear, fitness, logistics, defense"],
    lover: ["The Lover", "Intimacy, indulgence, beauty.", "Sensual, warm, devoted.", "Burgundy, blush, gold", "Fragrance, chocolate, fashion, hospitality"],
    jester: ["The Jester", "Joy, play, living in the moment.", "Witty, irreverent, fun.", "Bright yellow, orange, candy colors", "Snacks, games, casual dining, social apps"],
    everyperson: ["The Everyperson", "Belonging, realism, fairness.", "Friendly, plain-spoken, down-to-earth.", "Denim blue, warm neutrals", "Value retail, family brands, everyday banking"],
    caregiver: ["The Caregiver", "Service, protection, compassion.", "Gentle, supportive, trustworthy.", "Soft blue, sage green, warm white", "Healthcare, insurance, nonprofits, education"],
    ruler: ["The Ruler", "Control, stability, leadership.", "Authoritative, polished, exclusive.", "Black, gold, royal blue", "Luxury, finance, premium automotive"],
    creator: ["The Creator", "Innovation, self-expression, craft.", "Imaginative, expressive, detail-loving.", "Vivid multicolor, ochre, teal", "Design tools, arts supplies, maker brands"]
  };
  var AQ = [
    ["When customers think of you, the feeling you want first is…", [["Safe and uplifted", "innocent"], ["Smarter", "sage"], ["Free", "explorer"], ["Fired up", "hero"]]],
    ["Your brand would rather be…", [["Respected for expertise", "sage"], ["Loved for its warmth", "caregiver"], ["Admired for its taste", "lover"], ["Feared by incumbents", "outlaw"]]],
    ["Pick the sentence closest to your mission.", [["Make the impossible feel possible", "magician"], ["Give people tools to make their own thing", "creator"], ["Bring order and excellence", "ruler"], ["Make everyday life a bit more fun", "jester"]]],
    ["Your ideal customer is mostly…", [["Ambitious and competitive", "hero"], ["Practical and value-minded", "everyperson"], ["Curious and restless", "explorer"], ["Discerning and status-aware", "ruler"]]],
    ["Which compliment would you frame?", [["“You always tell it straight.”", "everyperson"], ["“You changed how I see things.”", "magician"], ["“You make me laugh.”", "jester"], ["“You took care of me.”", "caregiver"]]],
    ["Your visual style leans…", [["Clean, light and simple", "innocent"], ["Rich, sensual and lush", "lover"], ["Raw, gritty and loud", "outlaw"], ["Original and handmade-feeling", "creator"]]],
    ["In a crisis, your brand…", [["Steps in and protects people", "caregiver"], ["Leads with a calm plan", "ruler"], ["Explains what's really going on", "sage"], ["Rallies people to fight back", "hero"]]],
    ["Which word do you want to own?", [["Wonder", "magician"], ["Freedom", "explorer"], ["Belonging", "everyperson"], ["Desire", "lover"]]],
    ["Your marketing would never…", [["Be cynical", "innocent"], ["Be boring", "jester"], ["Play it safe", "outlaw"], ["Be generic or templated", "creator"]]],
    ["Choose a product launch event.", [["A summit hike at sunrise", "explorer"], ["A candlelit private dinner", "lover"], ["A black-tie gala", "ruler"], ["A street party with a DJ", "jester"]]],
    ["People should leave an interaction with you feeling…", [["Informed", "sage"], ["Capable", "hero"], ["Comforted", "caregiver"], ["Inspired to make something", "creator"]]],
    ["If your brand were a person at a party, it would be…", [["The kind host checking on everyone", "caregiver"], ["The friend everyone relates to", "everyperson"], ["The one doing card tricks", "magician"], ["The one with the purest heart", "innocent"]]]
  ];
  var aq = $("#archetype");
  if (aq) {
    aq.querySelector(".qs").innerHTML = AQ.map(function (q, i) {
      return '<div class="q"><p>' + (i + 1) + ". " + esc(q[0]) + '</p><div class="checks">' + q[1].map(function (o) {
        return '<label><input type="radio" name="aq' + i + '" value="' + o[1] + '" required> ' + esc(o[0]) + "</label>";
      }).join("") + "</div></div>";
    }).join("");
    aq.addEventListener("submit", function (e) {
      e.preventDefault();
      var tally = {}; Object.keys(AR).forEach(function (k) { tally[k] = 0; });
      $$("input:checked", aq).forEach(function (x) { tally[x.value]++; });
      var ranked = Object.keys(tally).sort(function (a, b) { return tally[b] - tally[a]; });
      var p = AR[ranked[0]], s = AR[ranked[1]];
      var res = $("#aq-result"); res.hidden = false;
      res.innerHTML = '<span class="eyebrow">Your primary archetype</span><h2>' + p[0] + "</h2><p><b>Core drive:</b> " + p[1] + "</p><p><b>Voice:</b> " + p[2] + "</p><p><b>Color cues:</b> " + p[3] + "</p><p><b>You'll often see it in:</b> " + p[4] +
        '</p><p class="muted">Secondary influence: <b>' + s[0] + "</b> — " + s[1] + ' Most strong brands blend one primary and one supporting archetype.</p><p><a class="btn" href="../audit.html?service=Brand%20strategy%20%26%20positioning">Get a free brand audit</a> <a class="btn alt" href="../guides/brand-archetypes.html">Read the archetypes guide</a></p>';
      res.scrollIntoView({ behavior: "smooth", block: "start" });
      store.set("bl-archetype", p[0]);
    });
  }

  /* ---------- 7. Brand Health Score (lead magnet) ---------- */
  var HQ = [
    ["Clarity", "I can explain what my brand does, for whom, and why it's different in one sentence."],
    ["Clarity", "My team (or I) describe the brand the same way every time."],
    ["Clarity", "We have a written positioning statement and brand promise."],
    ["Clarity", "We know exactly which customer segment we serve best."],
    ["Identity", "Our logo works at small sizes, in one color and on dark backgrounds."],
    ["Identity", "We have a defined color palette and type system that we actually use."],
    ["Identity", "Our name is easy to say, spell and search."],
    ["Identity", "We own the matching .com (or best-fit) domain and core social handles."],
    ["Consistency", "Our website, social profiles and packaging look like the same brand."],
    ["Consistency", "We have a brand or style guide that others can follow."],
    ["Consistency", "Our tone of voice is documented with do's and don'ts."],
    ["Consistency", "New marketing goes through a quick on-brand check before it ships."],
    ["Visibility", "People find us when they search for our category in our area or niche."],
    ["Visibility", "We publish useful content on a regular schedule."],
    ["Visibility", "Our name is searched directly (branded search) and that number is growing."],
    ["Visibility", "We have reviews, press or testimonials that prove our claims."],
    ["Loyalty", "Customers recommend us without being asked."],
    ["Loyalty", "We collect and act on customer feedback at least quarterly."],
    ["Loyalty", "Repeat customers make up a healthy share of revenue."],
    ["Loyalty", "Our brand experience after purchase is as good as before it."]
  ];
  var ACT = {
    Clarity: "Write a one-line positioning statement with our Positioning Builder, then test it on five customers.",
    Identity: "Run your name through the Name Tester and rebuild your palette with contrast-checked colors.",
    Consistency: "Create a one-page style guide with the Style Guide Builder and share it with everyone who makes content.",
    Visibility: "Pick one channel, publish weekly for 90 days, and track branded search in Google Search Console.",
    Loyalty: "Add a two-question feedback email after every purchase and close the loop on what you learn."
  };
  var hs = $("#health");
  if (hs) {
    var lbl = ["Not true", "Rarely", "Partly", "Mostly", "Fully"];
    hs.querySelector(".qs").innerHTML = HQ.map(function (q, i) {
      return '<div class="q"><p><span class="tag">' + q[0] + "</span>" + esc(q[1]) + '</p><div class="scale">' + lbl.map(function (l, v) {
        return '<label><input type="radio" name="h' + i + '" value="' + v + '" required>' + l + "</label>";
      }).join("") + "</div></div>";
    }).join("");
    var last = null;
    hs.addEventListener("submit", function (e) {
      e.preventDefault();
      var dims = {}, tot = 0;
      HQ.forEach(function (q, i) { var v = +((hs.querySelector('input[name="h' + i + '"]:checked') || {}).value || 0); dims[q[0]] = (dims[q[0]] || 0) + v; tot += v; });
      var score = Math.round(tot / 80 * 100);
      var weakest = Object.keys(dims).sort(function (a, b) { return dims[a] - dims[b]; });
      var band = score >= 80 ? "Thriving" : score >= 60 ? "Growing" : score >= 40 ? "Fragile" : "At risk";
      var res = $("#hs-result"); res.hidden = false;
      $("#hs-score").textContent = score; $("#hs-band").textContent = band;
      $("#hs-dims").innerHTML = Object.keys(dims).map(function (k) { var pct = Math.round(dims[k] / 16 * 100); return '<div><small>' + k + " · " + pct + '%</small><div class="meter"><i style="width:' + pct + '%"></i></div></div>'; }).join("");
      $("#hs-actions").innerHTML = weakest.slice(0, 3).map(function (k) { return "<li><b>" + k + ":</b> " + ACT[k] + "</li>"; }).join("");
      last = { score: score, band: band, dims: dims, weakest: weakest.slice(0, 3).join(", ") };
      res.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    var lf = $("#hs-lead");
    if (lf) lf._extra = function () { return last ? { brand_health_score: last.score + "/100 (" + last.band + ")", weakest_areas: last.weakest, dimension_scores: JSON.stringify(last.dims) } : {}; };
  }

  /* ---------- 8. Style Guide Builder ---------- */
  var sg = $("#guide-builder");
  if (sg) {
    var upd = function () {
      var g = function (id) { return ($("#" + id) || {}).value || ""; };
      var p = $("#sg-preview");
      var cols = [g("sg-c1"), g("sg-c2"), g("sg-c3"), g("sg-c4")];
      p.innerHTML = '<div style="border-bottom:6px solid ' + cols[0] + ';padding-bottom:14px;margin-bottom:18px"><small class="muted">BRAND GUIDELINES · v1</small><h2 style="margin:.2em 0;font-family:\'' + esc(g("sg-hf")) + '\',serif">' + esc(g("sg-name") || "Your Brand") + "</h2><p><i>" + esc(g("sg-tag")) + "</i></p></div>" +
        "<h3>Mission</h3><p>" + esc(g("sg-mission")) + "</p><h3>Audience</h3><p>" + esc(g("sg-aud")) + "</p>" +
        '<h3>Color</h3><div class="swatches" style="grid-template-columns:repeat(4,1fr)">' + cols.map(function (c, i) { return '<div class="sw" style="min-height:90px;background:' + c + ';color:' + (contrast(c, "#fff") > 3 ? "#fff" : "#111") + '">' + ["Primary", "Secondary", "Accent", "Neutral"][i] + "<br>" + c.toUpperCase() + "</div>"; }).join("") + "</div>" +
        "<h3>Typography</h3><p><b>Headlines:</b> " + esc(g("sg-hf")) + " · <b>Body:</b> " + esc(g("sg-bf")) + "</p>" +
        "<h3>Voice</h3><p><b>We are:</b> " + esc(g("sg-voice")) + "</p><p><b>We are not:</b> " + esc(g("sg-not")) + "</p>" +
        "<h3>Logo rules</h3><ul><li>Keep clear space equal to the height of the logo's first letter on all sides.</li><li>Minimum size: 24 px tall on screen, 10 mm in print.</li><li>Never stretch, recolor outside the palette, add effects, or place on busy photos without a solid backing.</li></ul>" +
        '<p class="fine">Made with the free Style Guide Builder at Brand.Life</p>';
    };
    sg.addEventListener("input", upd); upd();
    $("#sg-print").addEventListener("click", function () { window.print(); });
  }

  /* ---------- 9. Personal Brand Bio Generator ---------- */
  var bg = $("#bio-gen");
  if (bg) {
    var runB = function (e) {
      if (e) e.preventDefault();
      var g = function (id) { return ($("#" + id).value || "").trim(); };
      var n = g("bg-name") || "Alex Rivera", r = g("bg-role") || "brand strategist", w = g("bg-who") || "founders", res = g("bg-result") || "build brands people remember", proof = g("bg-proof"), fun = g("bg-fun"), cta = g("bg-cta");
      var first = n.split(" ")[0];
      var out = [
        ["Social (under 160 characters)", cap(r) + " helping " + w + " " + res + "." + (proof ? " " + proof + "." : "") + (cta ? " " + cta : "")],
        ["Short — first person", "I'm " + n + ", a " + r + " who helps " + w + " " + res + "." + (proof ? " " + proof + "." : "") + (fun ? " Off the clock: " + fun + "." : "")],
        ["Medium — third person", n + " is a " + r + " who helps " + w + " " + res + ". " + (proof ? proof + ". " : "") + first + " is known for turning fuzzy ideas into clear, confident brands." + (fun ? " When not working, " + first + " is probably " + fun + "." : "") + (cta ? " " + cta : "")],
        ["Speaker / press", n + " is a " + r + " and adviser to " + w + ". " + (proof ? proof + ". " : "") + "Their work focuses on one question: how do you " + res.replace(/^(help|helping)\s+/i, "") + " without losing what makes you different? " + first + " speaks on positioning, identity and brand growth."]
      ];
      $("#bg-out").innerHTML = out.map(function (o) { return '<div class="card"><small class="muted">' + o[0] + " · " + o[1].length + " chars</small><p style=\"color:inherit;margin:.4em 0\">" + esc(o[1]) + '</p><button class="copy" type="button" data-copy="' + esc(o[1]) + '">Copy</button></div>'; }).join("");
    };
    bg.addEventListener("submit", runB); bg.addEventListener("input", runB); runB();
  }

  /* ---------- 10. Positioning Statement Builder ---------- */
  var ps = $("#positioning");
  if (ps) {
    var runP = function () {
      var g = function (id) { return ($("#" + id).value || "").trim() || $("#" + id).placeholder; };
      var s = "For " + g("ps-aud") + " who " + g("ps-need") + ", " + g("ps-brand") + " is the " + g("ps-cat") + " that " + g("ps-ben") + ". Unlike " + g("ps-comp") + ", we " + g("ps-diff") + ".";
      $("#ps-out").textContent = s; $("#ps-copy").setAttribute("data-copy", s);
      var words = s.split(/\s+/).length;
      $("#ps-check").innerHTML = "<li>" + words + " words — " + (words <= 55 ? "tight enough to remember." : "trim it; under 55 words is easier to rally a team around.") + "</li><li>" + (/(best|leading|quality|innovative|world-class)/i.test(s) ? "Contains generic claims (best, leading, quality…). Replace them with something only you can prove." : "No generic filler words detected.") + "</li><li>Test: would a competitor be embarrassed to copy this sentence? If not, sharpen the “Unlike…” part.</li>";
    };
    ps.addEventListener("input", runP); runP();
  }
})();
