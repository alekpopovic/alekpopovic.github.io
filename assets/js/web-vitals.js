// Core metrics only. Never collect attribution, element selectors or user content.
(() => {
  const config = document.querySelector('script[data-vitals-host]');
  if (!config || location.hostname !== config.dataset.vitalsHost || location.protocol !== 'https:' || navigator.doNotTrack === '1' || navigator.globalPrivacyControl || typeof window.gtag !== 'function') return;
  import(new URL('../vendor/web-vitals.js', config.src).href).then(({ onLCP, onINP, onCLS }) => {
    const send = metric => {
      if (!['LCP', 'INP', 'CLS'].includes(metric.name) || !Number.isFinite(metric.value) || metric.value < 0 || !['good', 'needs-improvement', 'poor'].includes(metric.rating)) return;
      window.gtag('event', 'web_vital', {
        metric_name: metric.name,
        metric_value: Math.round(metric.value * 1000) / 1000,
        metric_rating: metric.rating,
        non_interaction: true
      });
    };
    onLCP(send); onINP(send); onCLS(send);
  }).catch(() => { /* Reading remains available if performance reporting fails. */ });
})();
