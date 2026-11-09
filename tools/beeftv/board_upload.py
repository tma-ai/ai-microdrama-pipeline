import os
"""Join 3 approved 9:16 panels into one storyboard (black gutters) and place it on a BeefTV canvas as an image node.
Usage: board_upload.py <canvasId> <title> <x> <y> <out.png> <panel1> <panel2> <panel3>"""
import datetime, json, subprocess, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from btv import ops, upload, business
sys.stdout.reconfigure(encoding="utf-8")

cid, title, x, y, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
panels = sys.argv[6:12]
PW, PH, G = 720, 1280, 24
n = len(panels); cols = 3 if n > 3 else n; rows = (n + cols - 1) // cols
W, H = cols * PW + (cols + 1) * G, rows * PH + (rows + 1) * G
fc = ";".join(f"[{i}]scale={PW}:{PH}:force_original_aspect_ratio=increase,crop={PW}:{PH}[p{i}]" for i in range(n))
fc += f";color=black:s={W}x{H}[bg0]"
for i in range(n):
    r, c = divmod(i, cols)
    fc += f";[bg{i}][p{i}]overlay={G + c * (PW + G)}:{G + r * (PH + G)}" + (f"[bg{i+1}]" if i < n - 1 else "")
fc += ",format=rgb24"
cmd = ["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", p_] for p_ in panels], []) + ["-filter_complex", fc, "-frames:v", "1", out]
subprocess.run(cmd, check=True)

res = upload(out)["resource"]
key = "resource:" + res["id"]
url = f"/api/resources/{res['id']}/file?proxy=1"
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
aid = "asset-" + uuid.uuid4().hex[:16]
asset = {"id": aid, "kind": "image", "title": title, "coverUrl": url, "tags": ["storyboard"], "status": "confirmed",
         "source": "Claude Code", "createdAt": now, "updatedAt": now,
         "data": {"dataUrl": url, "storageKey": key, "width": W, "height": H, "bytes": res["size"], "mimeType": "image/png"}}
business("business_put_assets_id", {"path": {"id": aid}, "body": {"asset": asset}}, "asset-" + aid)
def canvas():
    return ops("canvas.get", {"canvasId": cid})["result"]["canvas"]


def op(name, params):
    return ops(name, dict(params, canvasId=cid, expectedRevision=canvas()["revision"],
                          operationId=name.split(".")[-1] + "-" + uuid.uuid4().hex[:8]))


def http_op(name, params):
    """Same op as the CLI, but over the local HTTP API (no Windows command-line length limit)."""
    import glob, os, urllib.request
    rt = json.load(open(glob.glob(os.path.expanduser(r"~\.beeftv\runtime\*.json"))[0], encoding="utf-8"))
    op_id = params.get("operationId", "op-" + uuid.uuid4().hex[:8])
    req = urllib.request.Request(rt["baseUrl"] + "/ops/" + name + "?opId=" + op_id, data=json.dumps({"opId": op_id, "params": params}).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "X-Beeftv-Client": os.environ["BEEFTV_CLIENT_ID"],
                                          "X-Op-Id": op_id, "Idempotency-Key": op_id,
                                          "Authorization": "Bearer " + os.environ["BEEFTV_CLIENT_TOKEN"]})
    try:
        out = json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} on {name}: {e.read().decode('utf-8', 'replace')[:600]}")
    if out.get("code") != 0:
        raise SystemExit(f"HTTP op {name} failed: {json.dumps(out, ensure_ascii=False)[:600]}")
    return out["data"]


for n in [n for n in canvas()["nodes"] if n["title"] == title]:  # replace an older board with the same title
    op("canvas.node.delete", {"nodeId": n["id"]})
c = canvas()
nid = "n" + uuid.uuid4().hex[:10]
node = {"id": nid, "type": "image", "title": title, "position": {"x": x, "y": y}, "width": 700, "height": round(700 * H / W),
        "metadata": {"content": url, "storageKey": key, "assetId": aid, "mimeType": "image/png", "bytes": res["size"],
                     "naturalWidth": W, "naturalHeight": H, "status": "success", "locked": True}}
doc = dict(c)
doc["nodes"] = list(c["nodes"]) + [node]
http_op("canvas.document.commit", {"canvasId": cid, "expectedRevision": c["revision"], "document": doc,
                                   "operationId": "board-" + uuid.uuid4().hex[:8]})
got = next((n for n in canvas()["nodes"] if n["id"] == nid), {})
print(json.dumps({"title": title, "node": nid, "storageKey": got.get("metadata", {}).get("storageKey")}))
