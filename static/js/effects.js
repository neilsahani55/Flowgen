/* Flowgen Button Effects - JS Layer (Ripple + Interaction)
   Implementation Details:
     - Attaches ripple effect to .btn-primary and [data-action="primary"] buttons
     - Uses requestAnimationFrame and transforms for 60fps
   Usage Guidelines:
     - Include this script after DOM is ready (defer attribute recommended)
     - Opt out per-button with data-ripple="false"
     - Customize color via CSS variables in effects.css
   Customization Options:
     - Change ripple duration by editing RIPPLE_MS
     - Modify easing by updating ease function
   Dependencies:
     - None (vanilla JS)
*/

(function () {
  const RIPPLE_MS = 600;

  function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
  }

  function createRipple(e, btn) {
    if (btn.dataset.ripple === "false") return;

    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const maxDim = Math.max(rect.width, rect.height);
    const size = maxDim * 2; // overshoot for full coverage

    const ripple = document.createElement("span");
    ripple.className = "fg-ripple";
    ripple.style.left = x + "px";
    ripple.style.top = y + "px";
    ripple.style.width = "0px";
    ripple.style.height = "0px";
    btn.appendChild(ripple);

    const start = performance.now();
    function animate(now) {
      const elapsed = now - start;
      const t = Math.min(1, elapsed / RIPPLE_MS);
      const k = easeOutQuart(t);
      const currentSize = size * k;

      ripple.style.width = currentSize + "px";
      ripple.style.height = currentSize + "px";
      ripple.style.opacity = String(0.6 * (1 - t));

      if (t < 1) {
        requestAnimationFrame(animate);
      } else {
        ripple.remove();
      }
    }
    requestAnimationFrame(animate);
  }

  function attachInteractions(btn) {
    btn.addEventListener("mousedown", (e) => createRipple(e, btn));
    btn.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        const rect = btn.getBoundingClientRect();
        // keyboard ripple at center
        createRipple({ clientX: rect.left + rect.width / 2, clientY: rect.top + rect.height / 2 }, btn);
      }
    });
    // aria pressed on click for accessibility
    btn.addEventListener("click", () => {
      const pressed = btn.getAttribute("aria-pressed") === "true";
      btn.setAttribute("aria-pressed", (!pressed).toString());
      // reset after short time for non-toggle buttons
      setTimeout(() => btn.removeAttribute("aria-pressed"), 300);
    });
  }

  function init() {
    const buttons = document.querySelectorAll(".btn-primary, button[data-action='primary']");
    buttons.forEach(attachInteractions);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
