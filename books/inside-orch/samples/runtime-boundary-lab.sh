set -euo pipefail
book_tmp=$(mktemp -d)
book_server_pid=
book_port=18080

cleanup() {
  if [ -n "$book_server_pid" ]; then
    kill -TERM "$book_server_pid" 2>/dev/null || true
    wait "$book_server_pid" 2>/dev/null || true
  fi
  rm -rf "$book_tmp"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

go build -o "$book_tmp/orch-server" ./cmd/orch-server

book_curl() {
  curl --noproxy '*' --connect-timeout 1 --max-time 2 -fsS "$@"
}

start_server() {
  if (exec 3<>"/dev/tcp/127.0.0.1/$book_port") 2>/dev/null; then
    printf 'Local port %s is in use; choose a free port.\n' "$book_port" >&2
    return 1
  fi
  env -i PATH="$PATH" ORCH_SCHEMA_CHECK=false \
    "$book_tmp/orch-server" \
    --addr="127.0.0.1:$book_port" \
    --database-url='postgres://lab:lab@127.0.0.1:1/lab?sslmode=disable' \
    --secret-key='disposable-book-lab-key' \
    >"$book_tmp/server.log" 2>&1 &
  book_server_pid=$!
  for attempt in {1..50}; do
    kill -0 "$book_server_pid" 2>/dev/null || {
      cat "$book_tmp/server.log"
      return 1
    }
    if book_curl "http://127.0.0.1:$book_port/readyz" >/dev/null 2>&1; then
      sleep 0.1
      if kill -0 "$book_server_pid" 2>/dev/null; then
        return 0
      fi
      cat "$book_tmp/server.log"
      return 1
    fi
    sleep 0.1
  done
  cat "$book_tmp/server.log"
  return 1
}

start_server
book_curl -X POST "http://127.0.0.1:$book_port/v1/namespaces" \
  -H 'Content-Type: application/json' \
  --data '{"name":"book-restart-lab"}'
book_curl "http://127.0.0.1:$book_port/v1/namespaces" \
  >"$book_tmp/before.json"

kill -TERM "$book_server_pid"
wait "$book_server_pid" || true
book_server_pid=
start_server
book_curl "http://127.0.0.1:$book_port/v1/namespaces" \
  >"$book_tmp/after.json"

cat "$book_tmp/before.json"
cat "$book_tmp/after.json"
