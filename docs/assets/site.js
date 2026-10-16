(function () {
  "use strict";
  

  // Sidhuvudet får en kant när man scrollat.
  var head = document.querySelector(".head");
  function onScroll() { if (head) head.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobilmenyn
  var btn = document.getElementById("menuBtn");
  var menu = document.getElementById("menu");
  if (btn && menu) {
    var setOpen = function (open) {
      menu.hidden = !open;
      btn.setAttribute("aria-expanded", String(open));
      btn.setAttribute("aria-label", open ? "Stäng menyn" : "Meny");
    };
    btn.addEventListener("click", function () { setOpen(menu.hidden); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !menu.hidden) { setOpen(false); btn.focus(); }
    });
  }

  document.querySelectorAll("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });

  // Bildspelet i startsidans hero (stannar vid prefers-reduced-motion)
  var slides = document.querySelectorAll(".slides .slide");
  if (slides.length > 1 && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var cur = 0;
    setInterval(function () {
      slides[cur].classList.remove("on");
      cur = (cur + 1) % slides.length;
      var im = slides[cur].querySelector("img");
      if (im) im.loading = "eager";
      slides[cur].classList.add("on");
    }, 6000);
  }

  // Bildvisning för projektbilderna (data-lb = grupp)
  var lb = document.getElementById("lb");
  if (lb) {
    var lbImg = lb.querySelector("img"), lbCap = lb.querySelector("figcaption");
    var group = [], idx = 0, opener = null;
    var show = function (i) {
      idx = (i + group.length) % group.length;
      var a = group[idx];
      lbImg.src = a.getAttribute("href");
      lbImg.alt = a.querySelector("img").alt;
      lbCap.textContent = a.getAttribute("data-cap") + "  ·  " + (idx + 1) + " / " + group.length;
    };
    var close = function () { lb.hidden = true; document.body.style.overflow = ""; if (opener) opener.focus(); };
    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-lb]");
      if (!a) return;
      e.preventDefault();
      opener = a;
      group = Array.prototype.slice.call(document.querySelectorAll('[data-lb="' + a.getAttribute("data-lb") + '"]'));
      show(group.indexOf(a));
      lb.hidden = false;
      document.body.style.overflow = "hidden";
      lb.querySelector(".lb-x").focus();
    });
    lb.querySelector(".lb-x").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
    var x0 = null;
    lb.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) show(idx + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  // Offertformuläret: kontrolleras här, skickas via FormSubmit, sedan ett tack i dess ställe.
  var form = document.getElementById("qform");
  if (!form) return;
  var done = document.getElementById("qdone");
  var sendErr = document.getElementById("send-err");
  var f = {
    namn: document.getElementById("f-namn"),
    tel: document.getElementById("f-tel"),
    epost: document.getElementById("f-epost"),
    typ: document.getElementById("f-typ"),
    ort: document.getElementById("f-ort"),
    besk: document.getElementById("f-besk"),
    web: document.getElementById("f-web")
  };

  // "Få offert" från en tjänste- eller projektsida kommer med ?typ=… och den typen vald.
  var typ = new URLSearchParams(location.search).get("typ");
  if (typ) {
    for (var i = 0; i < f.typ.options.length; i++) if (f.typ.options[i].text === typ) f.typ.selectedIndex = i;
  }

  function mark(key, input, bad) {
    document.getElementById("e-" + key).hidden = !bad;
    input.setAttribute("aria-invalid", bad ? "true" : "false");
    if (bad) input.setAttribute("aria-describedby", "e-" + key); else input.removeAttribute("aria-describedby");
  }
  function validate() {
    var bad = [];
    var tel = f.tel.value.trim(), ep = f.epost.value.trim();
    var namnBad = !f.namn.value.trim();
    var contactBad = !tel && !ep;
    var epBad = !!ep && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(ep);
    mark("namn", f.namn, namnBad); if (namnBad) bad.push(f.namn);
    mark("tel", f.tel, contactBad); if (contactBad) bad.push(f.tel);
    mark("epost", f.epost, epBad); if (epBad) bad.push(f.epost);
    return bad;
  }
  form.addEventListener("input", function (e) {
    if (e.target.getAttribute("aria-invalid") === "true" || e.target === f.tel || e.target === f.epost) validate();
  });

  var submit = form.querySelector("button[type=submit]");
  var label = submit.querySelector("span");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var bad = validate();
    if (bad.length) { bad[0].focus(); return; }
    submit.disabled = true;
    label.textContent = "Skickar …";
    sendErr.hidden = true;
    var payload = {
      _subject: "Offertförfrågan från hemsidan – " + f.namn.value.trim(),
      _template: "table",
      _captcha: "false",
      _honey: f.web.value,
      Namn: f.namn.value.trim(),
      Telefon: f.tel.value.trim() || "–",
      "E-post": f.epost.value.trim() || "–",
      "Typ av projekt": f.typ.value || "–",
      Ort: f.ort.value.trim() || "–",
      Beskrivning: f.besk.value.trim() || "–"
    };
    if (f.epost.value.trim()) payload._replyto = f.epost.value.trim();
    fetch(form.getAttribute("data-endpoint"), {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().catch(function () { return null; }).then(function (j) {
        if (!r.ok || !j || String(j.success) !== "true") throw new Error("not sent");
      });
    }).then(function () {
      form.reset();
      form.hidden = true;
      done.hidden = false;
      done.focus();
    }).catch(function () {
      // Kvar som det skrevs, så att det kan skickas igen.
      sendErr.hidden = false;
    }).then(function () {
      submit.disabled = false;
      label.textContent = "Skicka förfrågan";
    });
  });

  document.getElementById("qagain").addEventListener("click", function () {
    done.hidden = true;
    form.hidden = false;
    f.namn.focus();
  });
})();
