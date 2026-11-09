"""Make a take with START + END frames in BeefTV.
Usage: btv_startend.py <canvas> <title> <start_png> <end_node_title> <x> <y> <prompt_file> <ref titles...>
The start PNG is uploaded as its own card; connections are made start -> end -> refs, in that order."""
import datetime, json, os, sys, time, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from btv import ops, business, upload
sys.stdout.reconfigure(encoding="utf-8")
CID, TITLE, START, END, X, Y, PFILE = sys.argv[1:8]
REFS = sys.argv[8:]


def canvas():
    return ops("canvas.get", {"canvasId": CID})["result"]["canvas"]


def op(name, params):
    return ops(name, dict(params, canvasId=CID, expectedRevision=canvas()["revision"], operationId=name.split(".")[-1] + "-" + uuid.uuid4().hex[:8]))


def node(title):
    return next(n for n in canvas()["nodes"] if n["title"] == title)["id"]


import subprocess
_wh = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", START],
                     capture_output=True, text=True).stdout.strip().split(",")
res = upload(START)["resource"]
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
aid = "asset-" + uuid.uuid4().hex[:16]
url = f"/api/resources/{res['id']}/file?proxy=1"
stitle = TITLE.replace("VIDEO", "START FRAME")
business("business_put_assets_id", {"path": {"id": aid}, "body": {"asset": {"id": aid, "kind": "image", "title": stitle, "coverUrl": url,
         "tags": ["start-frame"], "status": "confirmed", "source": "Claude Code", "createdAt": now, "updatedAt": now,
         "data": {"dataUrl": url, "storageKey": "resource:" + res["id"], "mimeType": "image/png", "bytes": res["size"],
                  "width": int(_wh[0]), "height": int(_wh[1])}}}}, "asset-" + aid)
sn = op("canvas.nodes.create", {"nodes": [{"title": stitle, "type": "image"}]})["result"]["created"][0]["id"]
op("canvas.node.bind_asset", {"nodeId": sn, "assetId": aid, "resourceId": res["id"]})
op("canvas.node.move", {"nodeId": sn, "position": {"x": int(X) - 780, "y": int(Y)}})
prompt = ("FRAME LOCK: the FIRST connected picture is the exact opening frame at 0.0 s. The SECOND connected picture is the exact final frame at "
          "10.0 s: the take must end matching that picture (same positions, framing and lighting). Everything in between moves continuously "
          "from the first to the second. " + open(PFILE, encoding="utf-8").read())
v = op("canvas.nodes.create", {"nodes": [{"title": TITLE, "type": "video", "prompt": prompt}]})["result"]["created"][0]["id"]
for src in [sn, node(END)] + [node(r) for r in REFS]:
    op("canvas.edge.create", {"fromNodeId": src, "toNodeId": v})
op("canvas.node.configure", {"nodeId": v, "kind": "video", "patch": {"model": "muse::muse-video", "size": os.environ.get("BTV_SIZE", "16:9"), "seconds": "10", "generateAudio": "true", "prompt": prompt}})
op("canvas.node.move", {"nodeId": v, "position": {"x": int(X), "y": int(Y)}})
t0 = time.time()
p = ops("canvas.generation.propose", {"canvasId": CID, "nodeIds": [v], "kind": "video", "note": TITLE})["result"]
mc = business("business_get_workspace_model_config", {})
s = ops("canvas.generation.submit", {"canvasId": CID, "nodeIds": [v], "kind": "video", "proposalId": p["proposalId"], "expectedRevision": canvas()["revision"],
                                      "expectedModelConfigRevision": mc.get("revision"), "operationId": "submit-" + uuid.uuid4().hex[:8]})["result"]
while True:
    time.sleep(20)
    t = ops("task.get", {"taskId": s["taskIds"][0]})["result"]
    t = t.get("task", t)
    if t.get("status") not in ("pending", "queued", "running", "processing", "submitted"):
        break
print(json.dumps({"title": TITLE, "status": t.get("status"), "sec": round(time.time() - t0)}), flush=True)
