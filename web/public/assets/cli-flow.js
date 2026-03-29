(function () {
  var e = document.querySelector(".cli-code-shell"),
    t = e && e.querySelector(".cli-login-source-dot"),
    o = e && e.querySelector(".cli-login-target-dot"),
    i = e && e.querySelector("#cliFlowPath"),
    n = e && e.querySelector("#cliFlowPathGlow"),
    r = e && e.querySelector(".cli-flow-svg");
  if (!e || !t || !o || !i || !n || !r) return;
  var s = function () {
    var s = e.getBoundingClientRect(),
      a = t.getBoundingClientRect(),
      l = o.getBoundingClientRect(),
      c = Math.max(1, Math.round(e.clientWidth)),
      d = Math.max(1, Math.round(e.clientHeight));
    r.setAttribute("viewBox", "0 0 " + c + " " + d);
    var h = a.left - s.left - 1 + a.width / 2,
      m = a.top - s.top - 1 + a.height / 2,
      p = l.left - s.left - 1 + l.width / 2,
      u = l.top - s.top - 1 + l.height / 2,
      g = h + (p - h) * 0.72,
      rad = Math.min(16, Math.abs(u - m) / 2),
      cv = Math.sign(u - m) * rad,
      sx = Math.sign(p - h) * Math.min(16, Math.abs(p - h)),
      y =
        window.innerWidth <= 980
          ? "M " +
            h +
            " " +
            m +
            " L " +
            (p - sx) +
            " " +
            m +
            " Q " +
            p +
            " " +
            m +
            " " +
            p +
            " " +
            (m + cv) +
            " L " +
            p +
            " " +
            u
          : "M " +
            h +
            " " +
            m +
            " L " +
            (g - rad) +
            " " +
            m +
            " Q " +
            g +
            " " +
            m +
            " " +
            g +
            " " +
            (m + cv) +
            " L " +
            g +
            " " +
            (u - cv) +
            " Q " +
            g +
            " " +
            u +
            " " +
            (g + rad) +
            " " +
            u +
            " L " +
            p +
            " " +
            u;
    i.setAttribute("d", y);
    n.setAttribute("d", y);
    var len = i.getTotalLength();
    i.style.setProperty("--len", len);
    n.style.setProperty("--len", len);
  };
  s();
  var a;
  window.addEventListener("resize", function () {
    clearTimeout(a);
    a = setTimeout(s, 120);
  });
})();
