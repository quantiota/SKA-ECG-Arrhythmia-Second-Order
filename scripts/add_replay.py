"""Add a real-time replay (play / pause / speed / position) to a second-order label cube HTML.
Same as SKA-ECG-Pathology/ska-ecg-engine/add_replay.py; the timing is already in the cube:
D.dt = Δt₂ (ms, time between two cycles) and D.k = the cycle of every point.
Usage: python add_replay.py cube.html out.html"""
import sys, json
src, out = sys.argv[1:3]
s = open(src).read()
i = s.find("const D ="); e = s.find("};", i) + 1
D = json.loads(s[i + 9:e]); assert len(D["dt"]) == len(D["p"]) == len(D["k"]) == len(D["lb"])

# 1. player style + markup
css = """  #player { position:absolute; left:50%; transform:translateX(-50%); bottom:72px; display:flex; align-items:center; gap:8px; background:rgba(18,19,23,.9); border:1px solid var(--line); border-radius:10px; padding:8px 12px; font-size:12px; width:min(620px, calc(100% - 32px)); box-sizing:border-box; }
  #player button, #player select { background:#22232a; color:var(--ink); border:1px solid var(--line); border-radius:6px; padding:4px 8px; font-size:12px; cursor:pointer; }
  #player input[type=range] { flex:1; min-width:60px; accent-color:#e87ba4; }
  #player .clock { color:var(--ink2); white-space:nowrap; font-variant-numeric:tabular-nums; min-width:150px; text-align:right; }
  #hint { bottom:128px !important; }
"""
s = s.replace("</style>", css + "</style>", 1)
player = """<div id="player">
  <button id="restart" title="Start again">⏮</button>
  <button id="play" title="Play / pause">▶ Play</button>
  <select id="speed" title="Replay speed"><option value="0.1">0.1×</option><option value="0.25">0.25×</option><option value="0.5">0.5×</option><option value="1">1×</option><option value="5">5×</option><option value="20" selected>20×</option><option value="60">60×</option></select>
  <input id="pos" type="range" min="1" max="1" value="1" title="Position in the recording">
  <span class="clock" id="clock"></span>
</div>
"""
s = s.replace('<div id="hint">', player + '<div id="hint">', 1)
s = s.replace("Desktop: drag to rotate", "Replay: ▶ plays the recording at the heart's own pace (1× = real time). Desktop: drag to rotate", 1)

# 2. replay logic
js = """
// ---- real-time replay: the points appear cycle by cycle, at the recorded timing ----
const Tcum = new Float64Array(N); { let t = 0; for (let i = 0; i < N; i++) { t += D.dt[i] / 1000; Tcum[i] = t; } }
const TEND = Tcum[N - 1];
let shownN = N, playing = false, simT = TEND, last = performance.now();
const head = new THREE.Mesh(new THREE.SphereGeometry(0.018, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffffff }));
head.visible = false; plot.add(head);
const posEl = document.getElementById('pos'), playEl = document.getElementById('play'),
      speedEl = document.getElementById('speed'), clockEl = document.getElementById('clock');
posEl.max = N; posEl.value = N;
const fmt = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
function setShown(n) {
  shownN = Math.max(1, Math.min(N, n));
  geo.setDrawRange(0, shownN);
  const j = shownN - 1;
  head.position.set(pos[3*j], toY(D.p[j]), pos[3*j+2]); head.visible = shownN < N || playing;
  posEl.value = shownN;
  clockEl.textContent = `cycle ${D.k[j]} · ${D.lb[j]} · ${fmt(Tcum[j])} / ${fmt(TEND)}`;
}
function setPlaying(v) { playing = v; playEl.textContent = v ? '❚❚ Pause' : '▶ Play'; last = performance.now(); }
playEl.onclick = () => {
  if (!playing && shownN >= N) { simT = 0; setShown(1); }          // finished: play again from the start
  else simT = Tcum[shownN - 1];
  setPlaying(!playing);
};
document.getElementById('restart').onclick = () => { simT = 0; setShown(1); setPlaying(true); };
posEl.oninput = () => { setPlaying(false); setShown(+posEl.value); simT = Tcum[shownN - 1]; };
function tick() {
  const now = performance.now(), dt = (now - last) / 1000; last = now;
  if (!playing) return;
  simT += dt * +speedEl.value;
  let lo = shownN - 1; while (lo < N - 1 && Tcum[lo + 1] <= simT) lo++;
  setShown(lo + 1);
  if (shownN >= N) { setPlaying(false); head.visible = false; }
}
setShown(N);
"""
anchor = "recolor();\naddEventListener('resize'"
assert anchor in s
s = s.replace(anchor, js + anchor, 1)
s = s.replace("renderer.setAnimationLoop(() => { controls.update();", "renderer.setAnimationLoop(() => { tick(); controls.update();", 1)
s = s.replace("<title>Second-Order SKA VR</title>", "<title>Second-Order SKA VR — replay</title>", 1)
for k in ("tick(); controls.update();", "— replay</title>", 'id="player"'):
    assert k in s, k
open(out, "w").write(s)
print("saved", out, "| points", len(D["p"]), "| recording", round(sum(D["dt"]) / 1000, 1), "s")
