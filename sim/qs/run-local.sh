#!/usr/bin/env bash
# Run the mock Queueserver of the IOS profile collection on this machine, against the simulated
# IOCs, for development and tests. Everything listens on 127.0.0.1 on non-default ports; the
# guard (sim/qs/guard.py) refuses to load the profile if the simulated IOC is not what it talks to.
#
#   sim/qs/run-local.sh [state-dir]        # stop with Ctrl-C
#
# Settings (environment): IOS_SIM_CA_PORT (5864), IOS_SIM_REDIS_PORT (60592), QS_HTTP_PORT (60612),
# QSERVER_HTTP_SERVER_SINGLE_USER_API_KEY (generated and printed to stdout if not set),
# REDIS_SERVER (command that starts redis; default: redis-server from conda-forge through pixi).
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE="${1:-/tmp/ios-mock-qs}"
export IOS_SIM_CA_PORT="${IOS_SIM_CA_PORT:-5864}"
export IOS_SIM_REDIS_PORT="${IOS_SIM_REDIS_PORT:-60592}"
export IOS_SIM_REPO="$REPO"
QS_HTTP_PORT="${QS_HTTP_PORT:-60612}"
export QSERVER_HTTP_SERVER_SINGLE_USER_API_KEY="${QSERVER_HTTP_SERVER_SINGLE_USER_API_KEY:-$(head -c 24 /dev/urandom | base64 | tr -d '/+=')}"
REDIS_SERVER="${REDIS_SERVER:-pixi exec --spec redis-server redis-server}"

# Nothing may reach real networks: loopback addresses only, from the first process on.
export EPICS_CA_ADDR_LIST=127.0.0.1 EPICS_CA_AUTO_ADDR_LIST=NO
export EPICS_CA_SERVER_PORT="$IOS_SIM_CA_PORT" EPICS_CA_REPEATER_PORT="$((IOS_SIM_CA_PORT + 1))"
export EPICS_PVA_ADDR_LIST=127.0.0.1 EPICS_PVA_AUTO_ADDR_LIST=NO
unset EPICS_CA_NAME_SERVERS EPICS_PVA_NAME_SERVERS
export MPLBACKEND=agg QT_QPA_PLATFORM=offscreen
export IOS_SIM_DATA_DIR="${IOS_SIM_DATA_DIR:-$STATE/xspress3_data}"
export IOS_SIM_FALLBACK=1 IOS_SIM_FALLBACK_LOG="${IOS_SIM_FALLBACK_LOG:-$STATE/log/fabricated-pvs.txt}"
export IOS_SIM_DOC_LOG="${IOS_SIM_DOC_LOG:-$STATE/documents.jsonl}"

mkdir -p "$STATE"/{startup,log,sockets}
mkdir -p "${IOS_SIM_DATA_DIR:-$STATE/xspress3_data}"
"$REPO/.pixi/envs/qs-sim/bin/python" "$REPO/sim/qs/make_startup_dir.py" "$STATE/startup" >/dev/null

cat > "$STATE/queueserver.yml" <<YAML
network:
  zmq_control_addr: ipc://$STATE/sockets/ctrl.sock
  zmq_info_addr: ipc://$STATE/sockets/info.sock
  zmq_publish_console: true
  redis_addr: 127.0.0.1:$IOS_SIM_REDIS_PORT
startup:
  keep_re: true
  startup_dir: $STATE/startup
  existing_plans_and_devices_path: $STATE/startup
  user_group_permissions_path: $STATE/startup
worker:
  use_ipython_kernel: false
operation:
  print_console_output: true
  console_logging_level: NORMAL
YAML
cat > "$STATE/httpserver.yml" <<YAML
qserver_zmq_configuration:
  control_address: ipc://$STATE/sockets/ctrl.sock
  info_address: ipc://$STATE/sockets/info.sock
authentication:
  allow_anonymous_access: false
YAML

PIDS=()
cleanup() { kill "${PIDS[@]}" 2>/dev/null || true; }
trap cleanup EXIT INT TERM
run() { local name="$1"; shift; "$@" > "$STATE/log/$name.log" 2>&1 & PIDS+=("$!"); }

ENVBIN="$REPO/.pixi/envs/qs-sim/bin"   # the same executables the systemd units use
export PATH="$ENVBIN:$PATH"
run redis $REDIS_SERVER --port "$IOS_SIM_REDIS_PORT" --bind 127.0.0.1 --save "" --appendonly no
run ioc "$ENVBIN/python" "$REPO/sim/run_iocs.py"
sleep 6
run manager "$ENVBIN/start-re-manager" --config "$STATE/queueserver.yml"
QSERVER_HTTP_SERVER_CONFIG="$STATE/httpserver.yml" run http \
  "$ENVBIN/uvicorn" --host 127.0.0.1 --port "$QS_HTTP_PORT" bluesky_httpserver.server:app

echo "mock Queueserver: http://127.0.0.1:$QS_HTTP_PORT  api key: $QSERVER_HTTP_SERVER_SINGLE_USER_API_KEY"
echo "logs: $STATE/log; stop with Ctrl-C"
wait
