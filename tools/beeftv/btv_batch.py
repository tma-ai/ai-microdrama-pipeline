"""Build and generate a list of shots INSIDE BeefTV, one at a time: create node -> connect reference nodes -> Muse model -> move into
its row -> propose/submit -> wait. Usage: btv_batch.py spec.json  (spec: [{title, prompt, refs:[node titles], x, y, kind}])"""
import os, json, sys, time, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from btv import ops, business
sys.stdout.reconfigure(encoding="utf-8")
CID = ""  # set "canvas" in the spec JSON


def canvas():
    return ops("canvas.get", {"canvasId": CID})["result"]["canvas"]


def op(name, params):
    c = canvas()
    return ops(name, dict(params, canvasId=CID, expectedRevision=c["revision"], operationId=name.split(".")[-1] + "-" + uuid.uuid4().hex[:8]))


def move(title, x, y):
    n = next(n for n in canvas()["nodes"] if n["title"] == title)
    op("canvas.node.move", {"nodeId": n["id"], "position": {"x": x, "y": y}})


spec = json.load(open(sys.argv[1], encoding="utf-8-sig"))
CID = spec.get("canvas", CID)
for layout in spec.get("moves", []):
    try:
        move(layout["title"], layout["x"], layout["y"])
    except Exception as e:  # noqa
        print("move failed", layout["title"], e)
for s in spec["shots"]:
    t0 = time.time()
    kind = s.get("kind", "image")
    have = [n for n in canvas()["nodes"] if n["title"] == s["title"]]
    if any(n.get("metadata", {}).get("storageKey") for n in have):
        print(json.dumps({"title": s["title"], "status": "skipped (already done)"}), flush=True)
        continue
    for n in have:  # half-made card from an interrupted run
        op("canvas.node.delete", {"nodeId": n["id"]})
    try:
        nid = op("canvas.nodes.create", {"nodes": [{"title": s["title"], "type": kind, "prompt": s["prompt"]}]})["result"]["created"][0]["id"]
        nodes = {n["title"]: n for n in canvas()["nodes"]}
        for ref in s["refs"]:
            op("canvas.edge.create", {"fromNodeId": nodes[ref]["id"], "toNodeId": nid})
        patch = {"model": "muse::muse-" + kind, "prompt": s["prompt"], "size": s.get("size", spec.get("size", "9:16"))}
        if kind == "video":
            patch.update({"seconds": str(s.get("seconds", 10)), "generateAudio": "true"})
        op("canvas.node.configure", {"nodeId": nid, "kind": kind, "patch": patch})
        op("canvas.node.move", {"nodeId": nid, "position": {"x": s["x"], "y": s["y"]}})
        p = ops("canvas.generation.propose", {"canvasId": CID, "nodeIds": [nid], "kind": kind, "note": s["title"]})["result"]
        mc = business("business_get_workspace_model_config", {})
        sub = ops("canvas.generation.submit", {"canvasId": CID, "nodeIds": [nid], "kind": kind, "proposalId": p["proposalId"],
                                                "expectedRevision": canvas()["revision"], "expectedModelConfigRevision": mc.get("revision"),
                                                "operationId": "submit-" + uuid.uuid4().hex[:8]})["result"]
        tid = sub["taskIds"][0]
        while True:
            time.sleep(15)
            task = ops("task.get", {"taskId": tid})["result"]
            task = task.get("task", task)
            if task.get("status") not in ("pending", "queued", "running", "processing", "submitted"):
                break
        res = (task.get("outputs") or [{}])[0].get("resourceId")
        print(json.dumps({"title": s["title"], "status": task.get("status"), "sec": round(time.time() - t0), "resource": res}), flush=True)
    except SystemExit as e:
        print(json.dumps({"title": s["title"], "status": "error", "sec": round(time.time() - t0), "error": str(e)[:400]}), flush=True)
