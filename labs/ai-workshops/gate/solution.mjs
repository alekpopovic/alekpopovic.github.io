export function deploymentGate(contract, observation) {
  const deny = reason => ({ allowed: false, reason });
  const text = value => typeof value === 'string' && value.trim().length > 0;
  if (!contract || !text(contract.namespace) || !text(contract.secret) || !Number.isSafeInteger(contract.generation) || contract.generation <= 0) return deny('invalid-contract');
  if (!observation || observation.available !== true) return deny('unknown');
  if (observation.namespace !== contract.namespace || observation.secret !== contract.secret) return deny('wrong-identity');
  if (observation.observedGeneration !== contract.generation || !text(observation.observedResourceVersion) || !text(observation.currentResourceVersion) || observation.observedResourceVersion !== observation.currentResourceVersion) return deny('stale');
  if (observation.satisfied !== true) return deny('unsatisfied');
  return { allowed: true, reason: 'satisfied' };
}
