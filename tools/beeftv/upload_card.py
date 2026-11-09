"""Upload ONE local image as a locked image card on a BeefTV canvas (via the local HTTP API; no command-line length limit).
Usage: upload_card.py <canvasId> <title> <x> <y> <image_path>"""
import datetime, glob, json, os, sys, urllib.error, urllib.request, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from btv import ops, upload, business
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
cid, title, x, y, path = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
W, H = Image.open(path).size


def http_op(name, params):
    rt = json.load(open(glob.glob(os.path.expanduser(r"~\.beeftv\runtime\*.json"))[0], encoding="utf-8"))
    op_id = params.get("operationId", "op-" + uuid.uuid4().hex[:8])
    req = urllib.request.Request(rt["baseUrl"] + "/ops/" + name + "?opId=" + op_id, data=json.dumps({"opId": op_id, "params": params}).encode("utf-8"),
                                 method="POST", headers={"Content-Type": "application/json", "X-Beeftv-Client": os.environ["BEEFTV_CLIENT_ID"],
                                                         "Authorization": "Bearer " + os.environ["BEEFTV_CLIENT_TOKEN"]})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} on {name}: {e.read().decode('utf-8', 'replace')[:600]}")


res = upload(path)["resource"]
key, url = "resource:" + res["id"], f"/api/resources/{res['id']}/file?proxy=1"
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
aid = "asset-" + uuid.uuid4().hex[:16]
mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
business("business_put_assets_id", {"path": {"id": aid}, "body": {"asset": {
    "id": aid, "kind": "image", "title": title, "coverUrl": url, "tags": ["reference"], "status": "confirmed", "source": "Claude Code",
    "createdAt": now, "updatedAt": now, "data": {"dataUrl": url, "storageKey": key, "width": W, "height": H, "bytes": res["size"], "mimeType": mime}}}}, "asset-" + aid)
c = ops("canvas.get", {"canvasId": cid})["result"]["canvas"]
for n in [n for n in c["nodes"] if n["title"] == title]:
    ops("canvas.node.delete", {"canvasId": cid, "nodeId": n["id"], "expectedRevision": ops("canvas.get", {"canvasId": cid})["result"]["canvas"]["revision"], "operationId": "del-" + uuid.uuid4().hex[:8]})
    c = ops("canvas.get", {"canvasId": cid})["result"]["canvas"]
nid = "n" + uuid.uuid4().hex[:10]
node = {"id": nid, "type": "image", "title": title, "position": {"x": x, "y": y}, "width": 360, "height": round(360 * H / W),
        "metadata": {"content": url, "storageKey": key, "assetId": aid, "mimeType": mime, "bytes": res["size"], "naturalWidth": W, "naturalHeight": H, "status": "success", "locked": True}}
doc = dict(c); doc["nodes"] = list(c["nodes"]) + [node]
r = http_op("canvas.document.commit", {"canvasId": cid, "expectedRevision": c["revision"], "document": doc, "operationId": "card-" + uuid.uuid4().hex[:8]})
print(json.dumps({"title": title, "node": nid, "ok": r.get("code") == 0}))
