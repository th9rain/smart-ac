#!/usr/bin/env python3
"""Initialize dataset repositories and report payload availability."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FASHION_MNIST_FILES = {
    "t10k-images-idx3-ubyte.gz": "bef4ecab320f06d8554ea6380940ec79",
    "t10k-labels-idx1-ubyte.gz": "bb300cfdad3c16e7a12a480ee83cd310",
    "train-images-idx3-ubyte.gz": "8d4fb7e6c68d591d4c3dfef9ec88bf0d",
    "train-labels-idx1-ubyte.gz": "25c81989df183df01b3e8a0aad5dffbe",
}

DEEPFASHION2_DRIVE = "https://drive.google.com/drive/folders/125F48fsMBz2EF0Cpqk6aaHet5VH399Ok"
DEEPFASHION2_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeIoGaFfCQILrtIZPykkr8q_h9qQ5BoTYbjvf95aXbid0v2Bw/viewform"


def run(*command: str, cwd: Path = PROJECT_ROOT) -> bool:
    try:
        subprocess.run(command, cwd=cwd, check=True)
        return True
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"[ERROR] {' '.join(command)}: {error}", file=sys.stderr)
        return False


def md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def initialize_submodules() -> bool:
    print("Initializing dataset submodules...")
    return run("git", "submodule", "sync", "--recursive") and run(
        "git", "submodule", "update", "--init", "--recursive"
    )


def check_fashion_mnist() -> bool:
    data_dir = PROJECT_ROOT / "datasets" / "fashion-mnist" / "data" / "fashion"
    valid = True
    print("\nFashion-MNIST")
    for name, expected in FASHION_MNIST_FILES.items():
        path = data_dir / name
        if not path.is_file():
            print(f"  [MISSING] {path.relative_to(PROJECT_ROOT)}")
            valid = False
            continue
        actual = md5(path)
        status = "OK" if actual == expected else f"BAD (expected {expected}, got {actual})"
        print(f"  [{status}] {path.relative_to(PROJECT_ROOT)}")
        valid &= actual == expected
    return valid


def check_deepfashion2() -> bool:
    data_dir = PROJECT_ROOT / "data" / "deepfashion2"
    expected = {
        "train/image": "training images",
        "train/annos": "training annotations",
        "validation/image": "validation images",
        "validation/annos": "validation annotations",
        "test/image": "test images",
    }
    present = [name for name in expected if (data_dir / name).is_dir()]

    print("\nDeepFashion2")
    if len(present) == len(expected):
        print(f"  [OK] Dataset found at {data_dir.relative_to(PROJECT_ROOT)}")
        return True

    print("  [ACTION REQUIRED] The official dataset is gated and is not redistributed here.")
    print(f"  1. Request the extraction password: {DEEPFASHION2_FORM}")
    print(f"  2. Download the official archives: {DEEPFASHION2_DRIVE}")
    print(f"  3. Extract them into: {data_dir}")
    for name, description in expected.items():
        marker = "OK" if name in present else "MISSING"
        print(f"     [{marker}] {name} ({description})")
    return False


def check_modanet() -> bool:
    repository = PROJECT_ROOT / "datasets" / "modanet"
    annotations = repository / "annotations"
    expected = {
        "modanet2018_instances_train.json": "96478657d20e322e9d3282c6d73c0c4c",
        "modanet2018_instances_val.json": "900b24b7d6c0c48203e6244f45d65499",
    }

    print("\nModaNet")
    if shutil.which("git-lfs") or run("git", "lfs", "version", cwd=repository):
        run("git", "lfs", "pull", cwd=repository)
    else:
        print("  [WARNING] Git LFS is unavailable; annotation files may remain pointers.")

    valid = True
    for name, expected_md5 in expected.items():
        path = annotations / name
        if not path.is_file():
            print(f"  [MISSING] {path.relative_to(PROJECT_ROOT)}")
            valid = False
            continue
        actual = md5(path)
        status = "OK" if actual == expected_md5 else f"BAD (expected {expected_md5}, got {actual})"
        print(f"  [{status}] {path.relative_to(PROJECT_ROOT)}")
        valid &= actual == expected_md5

    print("  [INFO] These are COCO-format labels only. The source RGB images are not")
    print("         redistributed by this project; see DATASETS.md for provenance.")
    return valid


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize Smart AC dataset repositories and verify available payloads."
    )
    parser.add_argument(
        "--dataset",
        choices=("all", "fashion-mnist", "deepfashion2", "modanet"),
        default="all",
        help="dataset to verify (default: all)",
    )
    parser.add_argument(
        "--skip-submodules",
        action="store_true",
        help="do not initialize or update Git submodules",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.skip_submodules and not initialize_submodules():
        return 1

    checks = {
        "fashion-mnist": check_fashion_mnist,
        "deepfashion2": check_deepfashion2,
        "modanet": check_modanet,
    }
    selected = checks if args.dataset == "all" else {args.dataset: checks[args.dataset]}
    results = {name: check() for name, check in selected.items()}

    print("\nSummary")
    for name, available in results.items():
        print(f"  {name}: {'ready' if available else 'not ready / action required'}")

    corrupted_public_payload = any(
        not available for name, available in results.items() if name in {"fashion-mnist", "modanet"}
    )
    return 1 if corrupted_public_payload else 0


if __name__ == "__main__":
    raise SystemExit(main())
