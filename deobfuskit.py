#!/usr/bin/env python3
"""Restore identifiers using an ObfusKit mapping JSON."""
from __future__ import annotations
import argparse
import io
import json
import tokenize
from pathlib import Path

def deobfuscate(source: str, mapping: dict[str, str]) -> str:
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    out = []
    for tok in tokens:
        if tok.type == tokenize.NAME and tok.string in mapping:
            tok = tok._replace(string=mapping[tok.string])
        out.append(tok)
    result = tokenize.untokenize(out)
    compile(result, "<restored>", "exec")
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description="Restore names using an ObfusKit mapping.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--map", dest="map_path", type=Path, required=True)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    mapping = json.loads(args.map_path.read_text(encoding="utf-8"))
    if not isinstance(mapping, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in mapping.items()):
        parser.error("mapping must be a JSON object of string keys and values")
    result = deobfuscate(args.source.read_text(encoding="utf-8"), mapping)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    print(f"Wrote restored source: {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
