/*
 * Contributing footer for the Dify docs.
 *
 * Mintlify auto-includes any .js file in the content directory on every page,
 * after the page becomes interactive. This script injects an
 * "Edit this page | Report an issue" bar just above the site footer, deriving
 * the GitHub edit URL from the current path at runtime. It replaces the
 * per-page sections previously baked in by tools/contributing_in_page.py.
 */
(function () {
  var REPO = "https://github.com/langgenius/dify-docs";
  var BRANCH = "main";
  var ISSUE_URL = REPO + "/issues/new?template=docs.yml";
  var FOOTER_ID = "dify-contributing-footer";

  var LABELS = {
    en: { edit: "Edit this page", report: "Report an issue" },
    zh: { edit: "编辑此页面", report: "提交问题" },
    ja: { edit: "このページを編集する", report: "問題を報告する" }
  };

  // Derive language + GitHub edit URL from the current path, or null to skip.
  function pathInfo() {
    var clean = window.location.pathname.replace(/^\/+|\/+$/g, "");
    if (!clean) return null;
    var segs = clean.split("/");
    if (segs.length < 2) return null; // need a language segment plus a page
    if (clean.indexOf("/api-reference/") !== -1) return null; // generated pages
    var lang = LABELS[segs[0]] ? segs[0] : "en";
    return { lang: lang, editUrl: REPO + "/edit/" + BRANCH + "/" + clean + ".mdx" };
  }

  function link(href, text) {
    var a = document.createElement("a");
    a.href = href;
    a.textContent = text;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.style.cssText = "color:inherit;text-decoration:underline;";
    return a;
  }

  function buildFooter(info) {
    var labels = LABELS[info.lang];
    var bar = document.createElement("div");
    bar.id = FOOTER_ID;
    bar.setAttribute("data-path", window.location.pathname);
    bar.style.cssText =
      "margin:2rem 0 1rem;" +
      "display:flex;align-items:center;gap:0.6rem;font-size:0.875rem;font-weight:600;";
    var sep = document.createElement("span");
    sep.textContent = "|";
    sep.style.cssText = "opacity:0.35;font-weight:400;";
    bar.appendChild(link(info.editUrl, labels.edit));
    bar.appendChild(sep);
    bar.appendChild(link(ISSUE_URL, labels.report));
    return bar;
  }

  // Idempotent: ensure exactly one bar exists for the current page.
  function ensureFooter() {
    var info = pathInfo();
    var existing = document.getElementById(FOOTER_ID);

    if (!info) {
      if (existing && existing.parentNode) existing.parentNode.removeChild(existing);
      return;
    }
    // Already placed for this path? Leave it (prevents observer loops).
    if (existing && existing.getAttribute("data-path") === window.location.pathname) return;
    if (existing && existing.parentNode) existing.parentNode.removeChild(existing);

    // Anchor just above the site footer: present on every page, so placement
    // is consistent and does not depend on per-page content structure.
    var footer = document.querySelector("footer");
    if (footer && footer.parentNode) {
      footer.parentNode.insertBefore(buildFooter(info), footer);
      return;
    }
    // Fallback if no <footer> is found yet (observer will retry on next change).
    var main = document.querySelector("main");
    if (main) main.appendChild(buildFooter(info));
  }

  function debounce(fn, ms) {
    var t;
    return function () {
      clearTimeout(t);
      t = setTimeout(fn, ms);
    };
  }

  function start() {
    ensureFooter();
    // Re-run on any DOM change: covers the initial async render and Mintlify's
    // client-side (SPA) navigation between pages.
    var run = debounce(ensureFooter, 150);
    new MutationObserver(run).observe(document.body, { childList: true, subtree: true });
    // Backup: catch route changes even if they don't trigger a large mutation.
    var lastPath = window.location.pathname;
    setInterval(function () {
      if (window.location.pathname !== lastPath) {
        lastPath = window.location.pathname;
        ensureFooter();
      }
    }, 500);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
