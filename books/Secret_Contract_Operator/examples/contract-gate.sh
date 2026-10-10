#!/usr/bin/env bash
set -euo pipefail

NS="${NS:-payments}"
CONTRACT="${CONTRACT:-payments-preflight}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-120}"
[[ "$TIMEOUT_SECONDS" =~ ^[1-9][0-9]*$ ]] || exit 2

initial="$(kubectl -n "$NS" get scn "$CONTRACT" -o json)"
uid="$(jq -er '.metadata.uid' <<<"$initial")"
gen="$(jq -er '.metadata.generation' <<<"$initial")"
deadline=$((SECONDS + TIMEOUT_SECONDS))

while (( SECONDS < deadline )); do
  if object="$(kubectl -n "$NS" get scn "$CONTRACT" -o json)"; then
    if jq -e --arg uid "$uid" --argjson gen "$gen" '
      .metadata.uid == $uid and
      .metadata.generation == $gen and
      .status.observedGeneration == $gen and
      (.status.observedSecret.uid | length) > 0 and
      any(.status.conditions[]?;
        .type == "Ready" and
        .status == "True" and
        .observedGeneration == $gen)
    ' <<<"$object" >/dev/null; then
      echo "Secret contract accepted for expected generation."
      exit 0
    fi
  fi
  sleep 2
done

echo "Secret contract gate timed out." >&2
exit 1
