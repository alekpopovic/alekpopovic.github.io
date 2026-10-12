// Teaching fixture: a green observation may belong to an old contract.
export function deploymentGate(contract, observation) {
  return { allowed: observation?.satisfied === true, reason: 'satisfied' };
}
