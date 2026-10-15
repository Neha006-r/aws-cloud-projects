from flask import Flask, jsonify
import psutil, time

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>System Monitor</title>
<style>
body{font-family:Arial,sans-serif;background:#0f172a;color:#e2e8f0;text-align:center;padding:40px}
.card{display:inline-block;background:#1e293b;border-radius:12px;padding:24px;margin:12px;width:280px}
.bar{background:#334155;border-radius:8px;height:22px;overflow:hidden;margin-top:10px}
.fill{height:100%;background:#22c55e;width:0%;transition:width .5s}
.big{font-size:40px;font-weight:bold}
small{color:#94a3b8}
</style></head><body>
<h1>EC2 System Monitor</h1>
<div class="card"><h2>CPU</h2><div class="big" id="cpu">0%</div><div class="bar"><div class="fill" id="cpubar"></div></div></div>
<div class="card"><h2>Memory</h2><div class="big" id="mem">0%</div><div class="bar"><div class="fill" id="membar"></div></div><small id="memtxt"></small></div>
<div class="card"><h2>Disk</h2><div class="big" id="disk">0%</div><div class="bar"><div class="fill" id="diskbar"></div></div></div>
<p><small id="up"></small></p>
<script>
async function update(){
  const r = await fetch('/api/stats');
  const d = await r.json();
  document.getElementById('cpu').textContent = d.cpu + '%';
  document.getElementById('cpubar').style.width = d.cpu + '%';
  document.getElementById('mem').textContent = d.mem + '%';
  document.getElementById('membar').style.width = d.mem + '%';
  document.getElementById('memtxt').textContent = d.mem_used + ' MB of ' + d.mem_total + ' MB used';
  document.getElementById('disk').textContent = d.disk + '%';
  document.getElementById('diskbar').style.width = d.disk + '%';
  document.getElementById('up').textContent = 'Server uptime: ' + d.uptime;
}
setInterval(update, 2000);
update();
</script></body></html>"""

@app.route("/")
def home():
    return PAGE

@app.route("/api/stats")
def stats():
    mem = psutil.virtual_memory()
    secs = int(time.time() - psutil.boot_time())
    return jsonify(
        cpu=psutil.cpu_percent(interval=0.5),
        mem=mem.percent,
        mem_used=round(mem.used / 1024 / 1024),
        mem_total=round(mem.total / 1024 / 1024),
        disk=psutil.disk_usage("/").percent,
        uptime=str(secs // 3600) + "h " + str((secs % 3600) // 60) + "m",
    )
