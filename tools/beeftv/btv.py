"""Small BeefTV helper over the CLI (uses BEEFTV_* env from the caller). Usage: btv.py business <tool> '<json>' [opid] | ops <op> '<json>' [opid] | upload <file>"""
import json, subprocess, sys, os
sys.stdout.reconfigure(encoding="utf-8")
CLI = os.path.expandvars(r"%LOCALAPPDATA%\Programs\BeefTV\cli\beeftv.exe")


def run(args):
    r = subprocess.run([CLI] + args, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(f"ERROR {r.returncode}: {r.stderr[:1500]} {r.stdout[:1500]}")
    try:
        return json.loads(r.stdout)
    except Exception:
        return r.stdout


def business(tool, params, op=None):
    a = ["business", "call", "--tool", tool, "--params", json.dumps(params)]
    return run(a + (["--operation-id", op] if op else []))


def ops(op, params):
    return run(["ops", "call", op, "--params", json.dumps(params), "--json"])


def upload(path, params=None):
    a = ["business", "upload", "--file", path]
    if params:
        a += ["--params", json.dumps(params)]
    return run(a)


if __name__ == "__main__":
    kind = sys.argv[1]
    if kind == "business":
        out = business(sys.argv[2], json.loads(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else None)
    elif kind == "ops":
        out = ops(sys.argv[2], json.loads(sys.argv[3]))
    else:
        out = upload(sys.argv[2])
    print(json.dumps(out, ensure_ascii=False)[:6000] if not isinstance(out, str) else out[:6000])
