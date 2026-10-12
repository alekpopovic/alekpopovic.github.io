// Loaded as text into a Blob worker inside an opaque-origin sandboxed frame.
// Cases come from the canonical Node test.mjs files.
self.onmessage = async ({ data }) => {
  const send = self.postMessage.bind(self), cases = [];
  const test = (name, check) => cases.push({ name, check });
  const equal = (a, b) => Object.is(a, b);
  const deep = (a, b) => {
    if (equal(a, b)) return true;
    if (!a || !b || typeof a !== 'object' || typeof b !== 'object' || Array.isArray(a) !== Array.isArray(b)) return false;
    const keys = Object.keys(a), other = Object.keys(b);
    return keys.length === other.length && keys.every(key => Object.hasOwn(b, key) && deep(a[key], b[key]));
  };
  const inspect = value => { try { return JSON.stringify(value) ?? String(value); } catch { return String(value); } };
  const check = (ok, a, b) => { if (!ok) throw new Error(`Expected ${inspect(b)}; received ${inspect(a)}`); };
  const assert = {
    equal: (a, b) => check(equal(a, b), a, b),
    notEqual: (a, b) => { if (equal(a, b)) throw new Error('Expected a different value or array reference.'); },
    deepEqual: (a, b) => check(deep(a, b), a, b),
    throws: callback => { let threw = false; try { callback(); } catch { threw = true; } if (!threw) throw new Error('Expected the invalid input to throw.'); },
  };
  let applicationUrl, testsUrl;
  try {
    applicationUrl = URL.createObjectURL(new Blob([data.source], { type: 'text/javascript' }));
    // Separate modules keep submitted code outside the harness's lexical scope.
    testsUrl = URL.createObjectURL(new Blob([`export default async function(test, assert, applicationUrl) {\n${data.tests}\n}`], { type: 'text/javascript' }));
    await (await import(testsUrl)).default(test, assert, applicationUrl);
    const results = [];
    for (const entry of cases) {
      try { await entry.check(); results.push({ name: entry.name, passed: true }); }
      catch (error) { results.push({ name: entry.name, passed: false, message: String(error?.message || error).slice(0, 500) }); }
    }
    send({ type: 'result', results });
  } catch (error) { send({ type: 'error', message: String(error?.message || error).slice(0, 500) }); }
  finally { if (applicationUrl) URL.revokeObjectURL(applicationUrl); if (testsUrl) URL.revokeObjectURL(testsUrl); }
  self.close();
};
