"""List or reconstruct the November D0 releases using Python's standard library."""
import argparse
import functools
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile


HERE = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or str(path) != name or "\\" in name:
        raise ValueError("Unsafe manifest path: " + repr(name))
    return path


class Releases:
    def __init__(self, repo, historical):
        self.manifest = json.loads((HERE / "manifest.json").read_bytes())
        self.stages = {s["id"]: s for s in self.manifest["stages"]}
        self.repo = repo
        self.historical = historical
        self.private_report = None
        if historical:
            entry = self.manifest["privacy"]
            if zipfile.is_zipfile(historical):
                with zipfile.ZipFile(historical) as bundle:
                    self.private_report = bundle.read(entry["report"])
            else:
                self.private_report = historical.read_bytes()
            if sha(self.private_report) != entry["historical_sha256"]:
                raise ValueError("The supplied historical report does not match the pinned SHA-256.")

    @functools.lru_cache(maxsize=None)
    def git_bytes(self, name):
        path = str(safe_path(name))
        ref = self.manifest["git_revision"] + ":" + path
        r = subprocess.run(["git", "-C", str(self.repo), "cat-file", "blob", ref],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if r.returncode:
            raise ValueError("The pinned Git object is unavailable. Use --repo with a checkout containing "
                             + self.manifest["git_revision"] + ".")
        return r.stdout

    @functools.lru_cache(maxsize=None)
    def blob(self, digest):
        entry = self.manifest["blobs"][digest]
        if "archive" in entry:
            data = self.archive(entry["archive"])
        elif "git" in entry:
            data = self.git_bytes(entry["git"])
            if "offset" in entry:
                start = entry["offset"]
                data = data[start:start+entry["length"]]
        else:
            data = (HERE / safe_path(entry["file"])).read_bytes()
        if "portable_sha256" in entry:
            privacy = self.manifest["privacy"]
            if self.historical:
                if digest == privacy["historical_sha256"]:
                    data = self.private_report
                elif digest == privacy["inventory_sha256"]:
                    data = data.replace(privacy["public_sha256"].encode(), privacy["historical_sha256"].encode())
        expected = digest if self.historical else entry.get("portable_sha256", digest)
        if sha(data) != expected:
            raise ValueError("Incorrect member SHA-256 for " + digest)
        return data

    @functools.lru_cache(maxsize=None)
    def archive(self, key):
        stage = self.stages[key]
        result = io.BytesIO()
        with zipfile.ZipFile(result, "w") as writer:
            for name, digest, stamp, *attrs in stage["members"]:
                when = tuple(map(int, (stamp[:4], stamp[4:6], stamp[6:8], stamp[8:10], stamp[10:12], stamp[12:14])))
                info = zipfile.ZipInfo(str(safe_path(name)), when)
                info.create_system = 3
                info.external_attr = attrs[0] if attrs else stage["external_attr"]
                writer.writestr(info, self.blob(digest), compress_type=zipfile.ZIP_DEFLATED,
                                compresslevel=stage["deflate_level"])
        data = result.getvalue()
        expected = stage["sha256"] if self.historical else stage.get("portable_sha256", stage["sha256"])
        if sha(data) != expected:
            raise ValueError("ZIP SHA-256 mismatch for " + key + ". The recorded archives used "
                             "zlib 1.2.12. Check the compressor when member hashes pass.")
        return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=HERE, help="Git checkout with the pinned primary objects")
    parser.add_argument("--historical-calibration", type=Path, metavar="FILE",
                        help="private historical calibration ZIP or diagnostics/TESTS.json for exact historical replay")
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="list releases or all original names in one release")
    listing.add_argument("stage", nargs="?")
    commands.add_parser("verify", help="verify member hashes and reconstruct/hash all seven ZIP streams in memory")
    for command in ("extract", "zip"):
        p = commands.add_parser(command)
        p.add_argument("stage")
        p.add_argument("destination", type=Path, help="new directory or new ZIP file")
    args = parser.parse_args()
    releases = Releases(args.repo.resolve(), args.historical_calibration)
    if getattr(args, "stage", None) and args.stage not in releases.stages:
        parser.error("unknown stage; use list")
    if args.command == "list":
        if args.stage:
            for member in releases.stages[args.stage]["members"]:
                print(member[0])
        else:
            for key, stage in releases.stages.items():
                print(f"{key:23s} {len(stage['members']):3d}  {stage['filename']}")
        return
    if args.command == "verify":
        for key in releases.stages:
            print(sha(releases.archive(key)), key)
        return
    if args.destination.exists() or args.destination.is_symlink():
        parser.error("destination already exists; choose a new path")
    if args.command == "zip":
        data = releases.archive(args.stage)
        with args.destination.open("xb") as stream:
            stream.write(data)
        return
    stage = releases.stages[args.stage]
    files = [(safe_path(name), releases.blob(digest)) for name, digest, *_ in stage["members"]]
    args.destination.mkdir(parents=True)
    for name, data in files:
        target = args.destination / name
        target.parent.mkdir(exist_ok=True, parents=True)
        with target.open("xb") as stream:
            stream.write(data)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        sys.exit(str(exc))
