from pathlib import Path
import subprocess

out = Path('/mnt/data/universal-tracking-technical-book/assets/diagrams')
out.mkdir(parents=True, exist_ok=True)

COMMON = '''
graph [bgcolor="transparent", fontname="DejaVu Sans", fontsize=18, pad=0.25, nodesep=0.55, ranksep=0.7];
node [shape=box, style="rounded,filled", fontname="DejaVu Sans", fontsize=16, color="#1c5961", fillcolor="#eef8f6", fontcolor="#102a2e", penwidth=1.8, margin="0.16,0.10"];
edge [fontname="DejaVu Sans", fontsize=13, color="#3f6d72", fontcolor="#355d61", penwidth=1.8, arrowsize=0.8];
'''

diagrams = {
'system-context': f'''digraph G {{
{COMMON}
rankdir=LR;
users [label="Operators, dispatchers,\nmanagers, viewers"];
tracked [label="Drivers, couriers, runners,\ncyclists, field workers"];
devices [label="Phones, watches, vehicle\ntrackers, asset beacons"];
platform [label="Universal Tracking Platform", fillcolor="#d6f2ed", penwidth=3];
integrations [label="Customer systems,\nwebhooks, reporting tools"];
users -> platform [label="dashboard / API"];
tracked -> platform [label="mobile app"];
devices -> platform [label="HTTPS / TCP / UDP"];
platform -> integrations [label="REST / webhooks / exports"];
}}''',
'runtime-topology': f'''digraph G {{
{COMMON}
rankdir=TB;
subgraph cluster_clients {{ label="Clients"; color="#9bc9c4"; style="rounded";
 dashboard [label="Angular dashboard"];
 public [label="Public tracking"];
 mobile [label="Capacitor mobile app"];
 gps [label="Physical GPS devices"];
}}
proxy [label="Nginx\nTLS, HTTP, WebSocket, TCP/UDP", fillcolor="#dceef8"];
subgraph cluster_go {{ label="Go application roles"; color="#9bc9c4"; style="rounded";
 api [label="api"];
 worker [label="worker"];
 scheduler [label="scheduler"];
 gateway [label="gps-gateway"];
}}
pg [label="PostgreSQL + PostGIS\nonly mandatory infrastructure", shape=cylinder, fillcolor="#e9e2f8", color="#65508d", penwidth=2.5];
dashboard -> proxy; public -> proxy; mobile -> proxy; gps -> proxy;
proxy -> api; proxy -> gateway; api -> pg; worker -> pg; scheduler -> pg; gateway -> pg;
}}''',
'domain-model': f'''digraph G {{
{COMMON}
rankdir=LR;
org [label="Organization"];
subject [label="TrackingSubject\nperson, vehicle, package, asset"];
profile [label="Typed profile\nperson / vehicle / asset"];
device [label="TrackingDevice\nphone, tracker, watch"];
assignment [label="DeviceAssignment\nvalid_from / valid_until"];
session [label="TrackingSession\nactivity, privacy, shift/task"];
point [label="LocationPoint\nimmutable observation"];
org -> subject [label="owns"];
subject -> profile [label="describes"];
subject -> assignment [label="tracked by"];
device -> assignment [label="assigned through"];
subject -> session [label="participates"];
device -> session [label="produces"];
session -> point [label="contains"];
}}''',
'location-ingestion': f'''digraph G {{
{COMMON}
rankdir=LR;
client [label="Mobile or device\noffline batch"];
auth [label="Device authentication\nand assignment check"];
validate [label="Validate, normalize,\nclassify quality"];
tx [label="Single PostgreSQL transaction\nbatch + points + latest + outbox"];
notify [label="NOTIFY event identifier"];
ws [label="WebSocket fan-out"];
client -> auth -> validate -> tx -> notify -> ws;
}}''',
'postgres-async': f'''digraph G {{
{COMMON}
rankdir=LR;
write [label="Business transaction"];
outbox [label="outbox_events", shape=cylinder, fillcolor="#e9e2f8", color="#65508d"];
jobs [label="jobs\nSKIP LOCKED", shape=cylinder, fillcolor="#e9e2f8", color="#65508d"];
notify [label="LISTEN / NOTIFY\nwake-up only"];
worker [label="Go workers\nlease, retry, dead-letter"];
side [label="Email, webhook, report,\nretention, derived data"];
write -> outbox [label="same commit"];
outbox -> notify [label="identifier"];
notify -> worker;
outbox -> worker [label="reconciliation"];
worker -> jobs [dir=both, label="claim / complete"];
worker -> side;
}}''',
'websocket-realtime': f'''digraph G {{
{COMMON}
rankdir=LR;
rest [label="REST snapshot\nlatest_locations"];
client [label="Angular live map"];
ws [label="Go WebSocket gateway\nauth + subscriptions"];
listen [label="PostgreSQL NOTIFY"];
outbox [label="Durable outbox event", shape=cylinder, fillcolor="#e9e2f8", color="#65508d"];
rest -> client [label="initial state"];
client -> ws [dir=both, label="subscribe / deltas"];
listen -> ws [label="wake-up"];
outbox -> ws [label="load durable event"];
}}''',
'mobile-offline': f'''digraph G {{
{COMMON}
rankdir=LR;
os [label="Native location engine\nKotlin or Swift"];
sqlite [label="SQLite queue\nsequence + sync state", shape=cylinder, fillcolor="#fff2d7", color="#a36c16"];
sync [label="Batch synchronizer\nretry + backoff"];
api [label="Go ingest API"];
ack [label="Accepted / duplicate / rejected\nsequence acknowledgement"];
os -> sqlite [label="append first"];
sqlite -> sync;
sync -> api;
api -> ack -> sqlite [label="delete only acknowledged"];
}}''',
'geofence-processing': f'''digraph G {{
{COMMON}
rankdir=LR;
point [label="Accepted location"];
candidates [label="Candidate geofences\nspatial index + tenant scope"];
state [label="Previous membership state"];
decide [label="Enter / exit / dwell\nalgorithm version"];
event [label="Geofence event + alert"];
point -> candidates -> decide;
state -> decide;
decide -> state [label="update"];
decide -> event;
}}''',
'gps-gateway': f'''digraph G {{
{COMMON}
rankdir=LR;
devices [label="Teltonika, GT06, OsmAnd,\ncustom trackers"];
listeners [label="Bounded TCP / UDP / HTTP\nlisteners"];
framing [label="Protocol framing\nsize and timeout limits"];
decoders [label="Versioned decoders\nCRC and field validation"];
envelope [label="Canonical LocationEnvelope"];
ingest [label="Shared ingestion service"];
devices -> listeners -> framing -> decoders -> envelope -> ingest;
}}''',
'deployment': f'''digraph G {{
{COMMON}
rankdir=TB;
internet [label="Internet / private device networks"];
nginx [label="Nginx\nTLS, static files, WebSocket, streams", fillcolor="#dceef8"];
subgraph cluster_apps {{ label="Application hosts"; color="#9bc9c4"; style="rounded";
 api1 [label="Go api + realtime A"];
 api2 [label="Go api + realtime B"];
 worker [label="Go workers + scheduler"];
 gateway [label="Go GPS gateway"];
}}
primary [label="PostgreSQL primary\nPostGIS + WAL", shape=cylinder, fillcolor="#e9e2f8", color="#65508d"];
standby [label="Optional hot standby", shape=cylinder, fillcolor="#f2eff8", color="#65508d"];
backup [label="Encrypted off-site backups\nand restore drills", fillcolor="#fff2d7", color="#a36c16"];
internet -> nginx; nginx -> api1; nginx -> api2; nginx -> gateway;
api1 -> primary; api2 -> primary; worker -> primary; gateway -> primary;
primary -> standby [label="streaming replication"];
primary -> backup [label="base backup + WAL"];
}}''',
'security-boundaries': f'''digraph G {{
{COMMON}
rankdir=LR;
human [label="Human identity\nuser session + MFA"];
device [label="Device identity\nseparate credentials"];
api [label="API client identity\nscoped token"];
public [label="Public-share identity\nrevocable capability"];
policy [label="Authorization policy\nRBAC + ABAC + tenant scope", fillcolor="#d6f2ed"];
data [label="Tenant data\nGo filters + PostgreSQL RLS", shape=cylinder, fillcolor="#e9e2f8", color="#65508d"];
human -> policy; device -> policy; api -> policy; public -> policy; policy -> data;
}}''',
'backup-restore': f'''digraph G {{
{COMMON}
rankdir=LR;
primary [label="PostgreSQL primary", shape=cylinder, fillcolor="#e9e2f8", color="#65508d"];
base [label="Encrypted base backup"];
wal [label="Continuous WAL archive"];
offsite [label="Off-site immutable copy"];
restore [label="Isolated restore environment"];
verify [label="Integrity checks + smoke tests\nRPO/RTO evidence"];
primary -> base; primary -> wal; base -> offsite; wal -> offsite; offsite -> restore -> verify;
}}''',
}

for name, dot in diagrams.items():
    dot_path = out / f'{name}.dot'
    svg_path = out / f'{name}.svg'
    png_path = out / f'{name}.png'
    dot_path.write_text(dot, encoding='utf-8')
    subprocess.run(['dot','-Tsvg',str(dot_path),'-o',str(svg_path)], check=True)
    subprocess.run(['dot','-Tpng','-Gdpi=180',str(dot_path),'-o',str(png_path)], check=True)
print(f'generated {len(diagrams)} diagrams')
