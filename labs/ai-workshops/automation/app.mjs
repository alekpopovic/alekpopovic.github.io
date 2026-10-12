export function releaseManifest(artifacts) {
  return { version: 1, generated: Date.now(), files: artifacts };
}
