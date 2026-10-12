export function releaseManifest(artifacts) {
  if (!Array.isArray(artifacts)) throw new Error('Expected an artifact list');
  const names = new Set();
  const files = artifacts.map(file => {
    if (!file || typeof file.name !== 'string' || !/^[a-zA-Z0-9][a-zA-Z0-9._-]{0,79}$/.test(file.name) || names.has(file.name)) throw new Error('Invalid or duplicate artifact name');
    if (typeof file.sha256 !== 'string' || !/^[a-fA-F0-9]{64}$/.test(file.sha256) || !Number.isSafeInteger(file.size) || file.size < 1) throw new Error('Invalid artifact evidence');
    names.add(file.name);
    return { name: file.name, sha256: file.sha256.toLowerCase(), size: file.size };
  }).sort((a, b) => a.name < b.name ? -1 : a.name > b.name ? 1 : 0);
  return { version: 1, files };
}
