"""Build provenance records for every paper listed in research/papers/seed.json.

Authoritative metadata comes from arXiv OAI-PMH (arXiv format for structured authors, arXivRaw for the
version history and license). PDFs are downloaded pinned to an exact version (e.g. 2601.07372v2).
The Markdown text comes from the Papers with Code catalog and is kept only as a searchable copy;
the PDF is the source of truth.

Outputs (in research/papers/):
  registry.json        full machine-readable record per paper
  references.bib       BibTeX, version-pinned
  REFERENCES.md        human-readable reference list with why-we-cite notes and file hashes
  provenance-log.jsonl append-only log of every download (time, URL, sha256)

Re-run after editing seed.json; existing version-pinned files are reused, not re-downloaded.
Non-arXiv papers (a "proceedings" block in seed.json) take metadata from the publisher's BibTeX,
cross-checked with OpenAlex, and the PDF from the publisher.

Stdlib only. Usage:  python research/tools/build_provenance.py [--render-only | --proceedings-only]
"""
import datetime as dt
import email.utils
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "papers"))
PDF_DIR = os.path.join(ROOT, "pdf")
MD_DIR = os.path.join(ROOT, "md")
TXT_DIR = os.path.join(ROOT, "txt")
LOG = os.path.join(ROOT, "provenance-log.jsonl")
UA = "DiaGrad-provenance/0.1 (research reference manager)"
ARXIV_DELAY = 3.1  # arXiv asks for at most one request every 3 seconds

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "raw": "http://arxiv.org/OAI/arXivRaw/",
    "ax": "http://arxiv.org/OAI/arXiv/",
}
DEFAULT_LICENSE = "http://arxiv.org/licenses/nonexclusive-distrib/1.0/"


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def log(entry):
    entry = {"time": now(), **entry}
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def http_get(url, timeout=120, attempts=5):
    """GET with backoff; arXiv intermittently answers 406/429/503 under load."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (406, 429, 500, 502, 503) or i == attempts - 1:
                raise
            time.sleep(ARXIV_DELAY * 2 ** (i + 1))


def oai(aid, prefix):
    url = f"https://oaipmh.arxiv.org/oai?verb=GetRecord&metadataPrefix={prefix}&identifier=oai:arXiv.org:{aid}"
    root = ET.fromstring(http_get(url))
    time.sleep(ARXIV_DELAY)
    return root.find(".//raw:arXivRaw" if prefix == "arXivRaw" else ".//ax:arXiv", NS)


def iso(rfc2822):
    return email.utils.parsedate_to_datetime(rfc2822).astimezone(dt.timezone.utc).isoformat(timespec="seconds")


def arxiv_meta(aid):
    """Metadata from arXiv OAI-PMH: arXivRaw (versions, license, submitter) + arXiv (structured authors).

    Dates come from arXivRaw's version history; the arXiv format's <created> reflects the latest
    version, not v1, so it is not used for dates.
    """
    raw, ax = oai(aid, "arXivRaw"), oai(aid, "arXiv")
    if raw is None or ax is None:
        raise RuntimeError(f"arXiv OAI record unavailable for {aid}")
    txt = lambda el, tag, ns="raw": (" ".join((el.findtext(f"{ns}:{tag}", namespaces=NS) or "").split()) or None)
    versions = [{"version": v.get("version"), "date": iso(v.findtext("raw:date", namespaces=NS)),
                 "size": v.findtext("raw:size", namespaces=NS)} for v in raw.findall("raw:version", NS)]
    authors = []
    for a in ax.findall("ax:authors/ax:author", NS):
        name = " ".join(filter(None, [a.findtext("ax:forenames", namespaces=NS),
                                      a.findtext("ax:keyname", namespaces=NS),
                                      a.findtext("ax:suffix", namespaces=NS)]))
        authors.append({"name": name, "affiliation": [x.text for x in a.findall("ax:affiliation", NS)]})
    cats = (txt(raw, "categories") or "").split()
    lic = txt(raw, "license")
    return {
        "title": txt(raw, "title"), "abstract": txt(raw, "abstract"), "authors": authors,
        "submitter": txt(raw, "submitter"), "versions": versions,
        "latest_version": versions[-1]["version"], "first_published": versions[0]["date"],
        "latest_updated": versions[-1]["date"],
        "primary_category": cats[0] if cats else None, "categories": cats,
        "doi": txt(raw, "doi"), "journal_ref": txt(raw, "journal-ref"), "comment": txt(raw, "comments"),
        "license": lic or DEFAULT_LICENSE,
        "license_note": None if lic else "no explicit license; arXiv default non-exclusive distribution",
    }


def pwc_json(aid):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run(["pwc", "paper", "info", aid, "--json"], capture_output=True, env=env)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout.decode("utf-8"))["data"]


def ensure_md(aid):
    path = os.path.join(MD_DIR, f"{aid}.md")
    if not os.path.exists(path):
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        r = subprocess.run(["pwc", "paper", "read", aid], capture_output=True, env=env)
        if r.returncode != 0:
            return None
        with open(path, "wb") as f:
            f.write(r.stdout)
        log({"action": "download_md", "arxiv": aid, "source": f"pwc paper read {aid}",
             "sha256": sha256(path)})
    elif not logged("md", aid):
        mtime = dt.datetime.fromtimestamp(os.path.getmtime(path), dt.timezone.utc)
        log({"action": "adopt_md", "arxiv": aid, "source": f"pwc paper read {aid}",
             "retrieved": mtime.isoformat(timespec="seconds"), "sha256": sha256(path),
             "note": "downloaded before logging existed"})
    return path


def logged(kind, aid):
    if not os.path.exists(LOG):
        return False
    with open(LOG, encoding="utf-8") as f:
        return any(e.get("arxiv") == aid and e.get("action", "").endswith("_" + kind)
                   for e in map(json.loads, f))


def ensure_txt(pdf):
    """Full text extracted locally from the version-pinned PDF (poppler's pdftotext).

    This is the complete searchable copy. The catalog Markdown can be truncated
    (e.g. DeepSeek-V4.1-Flash's stops mid-sentence), so completeness is checked against it.
    """
    path = os.path.join(TXT_DIR, os.path.basename(pdf)[:-4] + ".txt")
    if not os.path.exists(path):
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", pdf, path], capture_output=True)
        if r.returncode != 0:
            return None
    return path


def ensure_pdf(aid, ver):
    """Download the exact version; remove an older unpinned copy only after success."""
    pinned = os.path.join(PDF_DIR, f"{aid}{ver}.pdf")
    if not os.path.exists(pinned):
        url = f"https://arxiv.org/pdf/{aid}{ver}"
        data = http_get(url, timeout=300)
        if not data.startswith(b"%PDF"):
            raise RuntimeError(f"{url} did not return a PDF")
        with open(pinned, "wb") as f:
            f.write(data)
        log({"action": "download_pdf", "arxiv": aid, "version": ver, "url": url,
             "sha256": sha256(pinned)})
        time.sleep(ARXIV_DELAY)
    unpinned = os.path.join(PDF_DIR, f"{aid}.pdf")
    if os.path.exists(unpinned):
        os.remove(unpinned)
    return pinned


def norm_title(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def parse_bibtex_fields(text):
    """Fields of a single BibTeX entry, one-line (Crossref) or one-field-per-line (publisher exports).

    Values may be {braced} (nested braces allowed), "quoted" or bare (e.g. month=Feb).
    """
    body = text[text.index("{") + 1:text.rindex("}")]
    body = body[body.index(",") + 1:]  # drop the citation key
    fields, i = {}, 0
    while True:
        m = re.compile(r"\s*,?\s*(\w+)\s*=\s*").match(body, i)
        if not m:
            break
        key, i = m.group(1).lower(), m.end()
        if i < len(body) and body[i] == "{":
            depth, j = 0, i
            while j < len(body):
                depth += {"{": 1, "}": -1}.get(body[j], 0)
                if depth == 0:
                    break
                j += 1
            value, i = body[i + 1:j], j + 1
        elif i < len(body) and body[i] == '"':
            j = body.index('"', i + 1)
            value, i = body[i + 1:j], j + 1
        else:
            j = re.compile(r"[,}\s]").search(body, i)
            j = j.start() if j else len(body)
            value, i = body[i:j], j
        fields[key] = " ".join(value.replace("{", "").replace("}", "").split())
    return fields


def openalex_abstract(oa):
    """Rebuild OpenAlex's inverted-index abstract into plain text (None if absent)."""
    inv = oa.get("abstract_inverted_index")
    if not inv:
        return None
    pos = {i: w for w, idx in inv.items() for i in idx}
    return " ".join(pos[i] for i in sorted(pos))


def proceedings_meta(src):
    """Metadata for a paper that is not on arXiv, from two independent sources that must agree:
    the publisher's BibTeX (a proceedings export via `bibtex_url`, or Crossref's for a `doi`) and
    OpenAlex (cross-check).

    A title or author-surname mismatch between the two raises, so the entry is reported
    UNVERIFIED instead of being kept.
    """
    bib_url = src.get("bibtex_url") or f"https://api.crossref.org/works/{src['doi']}/transform/application/x-bibtex"
    bib = parse_bibtex_fields(http_get(bib_url).decode("utf-8"))
    oa = json.loads(http_get(f"https://api.openalex.org/works/{src['openalex']}"))
    authors = []
    for name in bib["author"].split(" and "):
        last, _, first = (x.strip() for x in name.partition(","))
        authors.append({"name": f"{first} {last}".strip(), "affiliation": []})
    oa_last = [unicodedata.normalize("NFKC", a["author"]["display_name"]).replace("‐", "-").split()[-1]
               for a in oa["authorships"]]
    if norm_title(bib["title"]) != norm_title(oa["display_name"]):
        raise RuntimeError(f"title mismatch: publisher {bib['title']!r} vs OpenAlex {oa['display_name']!r}")
    if [a["name"].split()[-1] for a in authors] != oa_last:
        raise RuntimeError(f"author mismatch: publisher {[a['name'] for a in authors]} vs OpenAlex {oa_last}")
    if str(oa["publication_year"]) != bib["year"]:
        raise RuntimeError(f"year mismatch: publisher {bib['year']} vs OpenAlex {oa['publication_year']}")
    journal = bib.get("journal")
    return {
        "title": bib["title"], "abstract": openalex_abstract(oa), "authors": authors, "versions": [],
        "first_published": bib["year"], "venue": journal or bib.get("booktitle"),
        "entry_type": "article" if journal else "inproceedings",
        "volume": bib.get("volume"), "number": bib.get("number"), "pages": bib.get("pages"),
        "publisher": bib.get("publisher"), "doi": oa.get("doi"),
        "license": None, "license_note": "publisher version; no open licence stated",
        "cross_check": {"openalex": oa["id"], "agrees_on": ["title", "author surnames", "year"]},
    }


def ensure_proceedings_pdf(pid, url):
    pinned = os.path.join(PDF_DIR, f"{pid}.pdf")
    if not os.path.exists(pinned):
        data = http_get(url, timeout=300)
        if not data.startswith(b"%PDF"):
            raise RuntimeError(f"{url} did not return a PDF")
        with open(pinned, "wb") as f:
            f.write(data)
        log({"action": "download_pdf", "paper": pid, "url": url, "sha256": sha256(pinned)})
    return pinned


def non_arxiv_source(p):
    """The source block of a non-arXiv seed entry ('proceedings' or 'publication'), or None."""
    return p.get("proceedings") or p.get("publication")


def proceedings_record(p):
    src = non_arxiv_source(p)
    meta = proceedings_meta(src)
    rec = {
        "id": p["id"], "arxiv": None, "kind": "proceedings",
        **{k: p[k] for k in ("topics", "items", "role", "why", "reviewed")},
        **meta, "source": src, "files": {}, "metadata_retrieved": now(),
    }
    if src.get("pdf_url"):
        pdf = ensure_proceedings_pdf(p["id"], src["pdf_url"])
        rec["files"]["pdf"] = {"path": os.path.relpath(pdf, ROOT).replace(os.sep, "/"), "sha256": sha256(pdf),
                               "bytes": os.path.getsize(pdf), "source": src["pdf_url"]}
        txt = ensure_txt(pdf)
        if txt:
            rec["files"]["txt"] = {
                "path": os.path.relpath(txt, ROOT).replace(os.sep, "/"), "sha256": sha256(txt),
                "bytes": os.path.getsize(txt), "source": f"pdftotext of {os.path.basename(pdf)}",
                "note": "complete text of the publisher PDF; layout and math may be garbled"}
    elif meta["abstract"]:
        # No open PDF: keep the abstract as the only searchable text, and say so.
        path = os.path.join(TXT_DIR, f"{p['id']}.abstract.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{meta['title']}\n\nAbstract (OpenAlex {meta['cross_check']['openalex']}):\n{meta['abstract']}\n")
        rec["files"]["txt"] = {
            "path": os.path.relpath(path, ROOT).replace(os.sep, "/"), "sha256": sha256(path),
            "bytes": os.path.getsize(path), "source": "OpenAlex abstract_inverted_index",
            "note": "ABSTRACT ONLY: no open full text; claims about this paper are limited to its abstract"}
    rec["bibkey"] = bib_key(rec)
    return rec


def ascii_slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]", "", s)


def bib_key(rec):
    last = rec["authors"][0]["name"].split()[-1] if rec["authors"] else "anon"
    word = next((w for w in re.findall(r"[A-Za-z]+", rec["title"])
                 if w.lower() not in {"a", "an", "the", "on", "of", "can", "you"}), "paper")
    return f"{ascii_slug(last).lower()}{rec['first_published'][:4]}{word.lower()}"


def bib_escape(s):
    return s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")


BIB_MAX_AUTHORS = 10  # registry.json keeps every author; the .bib lists the first 10, then "et al."


def bib_authors(authors):
    names = [a["name"] for a in authors]
    if len(names) > BIB_MAX_AUTHORS:
        names = names[:BIB_MAX_AUTHORS] + ["others"]  # BibTeX renders "and others" as "et al."
    return " and ".join(names)


def to_bibtex(rec):
    if rec.get("kind") == "proceedings":
        article = rec.get("entry_type") == "article"
        doi = (rec.get("doi") or "").replace("https://doi.org/", "")
        fields = {
            "title": "{" + bib_escape(rec["title"]) + "}",
            "author": bib_authors(rec["authors"]),
            ("journal" if article else "booktitle"): rec["venue"],
            "volume": rec["volume"],
            "number": rec.get("number") if article else None,
            "pages": (rec.get("pages") or "").replace("–", "--") if article else None,
            "publisher": rec["publisher"],
            "year": rec["first_published"][:4],
            "doi": doi if article else None,
            "url": rec["source"].get("pdf_url") or (f"https://doi.org/{doi}" if doi else None),
        }
        body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items() if v)
        return f"@{'article' if article else 'inproceedings'}{{{rec['bibkey']},\n{body}\n}}\n"
    fields = {
        "title": "{" + bib_escape(rec["title"]) + "}",
        "author": bib_authors(rec["authors"]),
        "year": rec["first_published"][:4],
        "eprint": rec["arxiv"],
        "archivePrefix": "arXiv",
        "primaryClass": rec["primary_category"],
        "url": f"https://arxiv.org/abs/{rec['arxiv']}{rec['pinned_version']}",
        "note": f"Cited version {rec['pinned_version']} ({rec['pinned_version_date']})",
    }
    if rec.get("doi"):
        fields["doi"] = rec["doi"]
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items())
    return f"@misc{{{rec['bibkey']},\n{body}\n}}\n"


def short_authors(authors, n=3):
    names = [a["name"] for a in authors]
    return ", ".join(names[:n]) + (f", et al. ({len(names)} authors)" if len(names) > n else "")


def write_markdown(records):
    roles = ["foundation", "closest-relative", "related", "evaluation", "background"]
    lines = [
        "# References",
        "",
        f"Generated by `research/tools/build_provenance.py` on {now()[:10]}. Do not edit by hand:",
        "edit `seed.json` and re-run. Metadata is from arXiv; the PDF of the listed version is the",
        "source of truth, and `md/` holds a Papers with Code text copy for searching only.",
        "",
        "`why` notes were drafted from abstracts and are unreviewed unless marked reviewed.",
        "PDFs are local copies for private research. Check each license before redistributing.",
        "",
    ]
    for role in roles:
        group = [r for r in records if r["role"] == role]
        if not group:
            continue
        lines += [f"## {role.replace('-', ' ').title()}", ""]
        for r in group:
            if r.get("kind") == "proceedings":
                lines += [
                    f"### {r['title']}",
                    f"- **Authors:** {short_authors(r['authors'])}",
                    f"- **Published:** {r['venue']}, vol. {r['volume']} ({r['first_published'][:4]}) · "
                    + (f"[PDF]({r['source']['pdf_url']}) · " if r['source'].get('pdf_url') else f"{r.get('doi')} · ")
                    + "not on arXiv; metadata from the publisher's BibTeX, "
                    f"cross-checked with OpenAlex {r['cross_check']['openalex'].rsplit('/', 1)[-1]}",
                    f"- **License:** {r['license_note']}",
                    f"- **Serves items:** {', '.join(map(str, r['items']))} · topics: {', '.join(r['topics'])}",
                    f"- **Why we cite it{'' if r['reviewed'] else ' (unreviewed)'}:** {r['why']}",
                    "- **Files:** "
                    + (f"`pdf/{os.path.basename(r['files']['pdf']['path'])}` sha256 `{r['files']['pdf']['sha256'][:16]}…` · "
                       if r['files'].get('pdf') else "no open PDF · ")
                    + (f"`{r['files']['txt']['path']}` "
                       f"({'abstract only' if 'ABSTRACT ONLY' in r['files']['txt']['note'] else 'full text'})"
                       if r['files'].get('txt') else ""),
                    f"- **BibTeX key:** `{r['bibkey']}`",
                    "",
                ]
                continue
            lic = r["license"].rstrip("/").split("/licenses/")[-1]
            lines += [
                f"### {r['title']}",
                f"- **Authors:** {short_authors(r['authors'])}",
                f"- **arXiv:** [{r['arxiv']}{r['pinned_version']}](https://arxiv.org/abs/{r['arxiv']}{r['pinned_version']})"
                f" · {r['primary_category']} · first posted {r['first_published'][:10]}"
                f" · cited version {r['pinned_version']} of {len(r['versions']) or '?'} ({r['pinned_version_date']})",
                f"- **License:** {lic}" + (f" ({r['license_note']})" if r.get("license_note") else ""),
                f"- **Serves items:** {', '.join(map(str, r['items']))} · topics: {', '.join(r['topics'])}",
                f"- **Why we cite it{'' if r['reviewed'] else ' (unreviewed)'}:** {r['why']}",
                f"- **Files:** `pdf/{os.path.basename(r['files']['pdf']['path'])}` sha256 `{r['files']['pdf']['sha256'][:16]}…`"
                + (f" · `md/{r['arxiv']}.md` sha256 `{r['files']['md']['sha256'][:16]}…`" if r['files'].get('md') else "")
                + (f" · `{r['files']['txt']['path']}` (full text)" if r['files'].get('txt') else "")
                + (" · **catalog text truncated; use txt/**" if r['files'].get('md', {}).get('warning') else ""),
                f"- **BibTeX key:** `{r['bibkey']}`",
                "",
            ]
    with open(os.path.join(ROOT, "REFERENCES.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(MD_DIR, exist_ok=True)
    os.makedirs(TXT_DIR, exist_ok=True)
    with open(os.path.join(ROOT, "seed.json"), encoding="utf-8") as f:
        seed = json.load(f)["papers"]
    records, failed = [], []
    for p in seed:
        if non_arxiv_source(p):
            add_proceedings(p, records, failed)
            continue
        aid = p["arxiv"]
        try:
            meta = arxiv_meta(aid)
        except Exception as e:  # unverifiable IDs are reported, never silently kept
            failed.append((aid, str(e)))
            log({"action": "unverified", "arxiv": aid, "error": str(e)})
            print(f"UNVERIFIED {aid}: {e}")
            continue
        ver = meta["latest_version"]
        ver_date = meta["latest_updated"]
        pdf = ensure_pdf(aid, ver)
        md = ensure_md(aid)
        txt = ensure_txt(pdf)
        pwc = pwc_json(aid) or {}
        rec = {
            "arxiv": aid, **{k: p[k] for k in ("topics", "items", "role", "why", "reviewed")},
            **meta, "pinned_version": ver, "pinned_version_date": ver_date,
            "files": {
                "pdf": {"path": os.path.relpath(pdf, ROOT).replace(os.sep, "/"), "sha256": sha256(pdf),
                        "bytes": os.path.getsize(pdf), "source": f"https://arxiv.org/pdf/{aid}{ver}"},
            },
            "catalog": {"source": "paperswithcode.co API v1", "pwc_id": pwc.get("id"),
                        "abs_url": pwc.get("url_abs")},
            "metadata_retrieved": now(),
        }
        if md:
            rec["files"]["md"] = {
                "path": os.path.relpath(md, ROOT).replace(os.sep, "/"), "sha256": sha256(md),
                "bytes": os.path.getsize(md), "source": f"pwc paper read {aid}",
                "note": "catalog text conversion; the catalog does not state which arXiv version it converted"}
        if txt:
            rec["files"]["txt"] = {
                "path": os.path.relpath(txt, ROOT).replace(os.sep, "/"), "sha256": sha256(txt),
                "bytes": os.path.getsize(txt), "source": f"pdftotext of {os.path.basename(pdf)}",
                "note": "complete text of the pinned PDF; layout and math may be garbled"}
            if md:
                ratio = os.path.getsize(md) / max(os.path.getsize(txt), 1)
                rec["files"]["md"]["coverage_vs_pdf_text"] = round(ratio, 2)
                if ratio < 0.7:
                    rec["files"]["md"]["warning"] = "catalog Markdown looks truncated; search txt/ instead"
        rec["bibkey"] = bib_key(rec)
        records.append(rec)
        print(f"{aid}{ver}\t{len(rec['authors'])} authors\t{rec['title'][:70]}")

    write_all(records, failed, "build")


def add_proceedings(p, records, failed):
    try:
        rec = proceedings_record(p)
    except Exception as e:  # unverifiable entries are reported, never silently kept
        failed.append((p["id"], str(e)))
        log({"action": "unverified", "paper": p["id"], "error": str(e)})
        print(f"UNVERIFIED {p['id']}: {e}")
        return
    records.append(rec)
    print(f"{p['id']}\t{len(rec['authors'])} authors\t{rec['title'][:70]}")


def write_all(records, failed, action):
    keys = [r["bibkey"] for r in records]
    for k in {k for k in keys if keys.count(k) > 1}:
        for i, r in enumerate([r for r in records if r["bibkey"] == k]):
            r["bibkey"] = k + "abcdefghij"[i]

    with open(os.path.join(ROOT, "registry.json"), "w", encoding="utf-8") as f:
        json.dump({"generated": now(), "papers": records}, f, ensure_ascii=False, indent=2)
    with open(os.path.join(ROOT, "references.bib"), "w", encoding="utf-8") as f:
        f.write("".join(to_bibtex(r) + "\n" for r in records))
    write_markdown(records)
    log({"action": action, "papers": len(records), "unverified": [a for a, _ in failed]})
    if failed:
        sys.exit(f"{len(failed)} seed entries could not be verified: {[a for a, _ in failed]}")


def proceedings_only():
    """Refresh only the non-arXiv entries; arXiv records are kept from registry.json as they are."""
    with open(os.path.join(ROOT, "seed.json"), encoding="utf-8") as f:
        seed = json.load(f)["papers"]
    with open(os.path.join(ROOT, "registry.json"), encoding="utf-8") as f:
        records = [r for r in json.load(f)["papers"] if r.get("kind") != "proceedings"]
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(TXT_DIR, exist_ok=True)
    failed = []
    for p in seed:
        if non_arxiv_source(p):
            add_proceedings(p, records, failed)
    write_all(records, failed, "build_proceedings_only")


def render_only():
    """Regenerate references.bib and REFERENCES.md from registry.json without contacting arXiv."""
    with open(os.path.join(ROOT, "registry.json"), encoding="utf-8") as f:
        records = json.load(f)["papers"]
    with open(os.path.join(ROOT, "references.bib"), "w", encoding="utf-8") as f:
        f.write("".join(to_bibtex(r) + "\n" for r in records))
    write_markdown(records)
    log({"action": "render", "papers": len(records)})
    print(f"rendered {len(records)} papers from registry.json")


if __name__ == "__main__":
    if "--render-only" in sys.argv:
        render_only()
    elif "--proceedings-only" in sys.argv:
        proceedings_only()
    else:
        main()
