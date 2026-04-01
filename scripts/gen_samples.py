import os
import subprocess
import sys

_ROOT = os.path.join(os.path.dirname(__file__), "..")
MAIN = os.path.join(_ROOT, "src", "main.py")

LANGUAGES = {
    "c":      ("sample.c",   "c"),
    "cpp":    ("sample.cpp", "cpp"),
    "python": ("sample.py",  "py"),
    "java":   ("sample.java","java"),
    "cs":     ("sample.cs",  "cs"),
}

MODES = ["ast", "dfg", "ast+dfg"]

DIRS = ["samples", "samples_harder"]


def generate(sample_dir):
    base = os.path.join(_ROOT, sample_dir)
    if not os.path.isdir(base):
        print(f"Skipping {sample_dir}/ (directory not found)")
        return

    for lang, (src_file, prefix) in LANGUAGES.items():
        src_path = os.path.join(base, src_file)
        if not os.path.isfile(src_path):
            print(f"  skip {src_file} (not found)")
            continue

        for mode in MODES:
            for norm in (False, True):
                suffix = f"_norm" if norm else ""
                out_name = f"{prefix}_{mode}{suffix}.dot"
                out_path = os.path.join(base, out_name)

                cmd = [
                    sys.executable, MAIN, src_path,
                    "--lang", lang,
                    "--mode", mode,
                    "--output", "dot",
                    "--out-file", out_path,
                    "--png",
                ]
                if norm:
                    cmd.append("--normalize")

                print(f"  {out_name}")
                subprocess.run(cmd, check=True)

    print()


if __name__ == "__main__":
    for d in DIRS:
        print(f"=== {d}/ ===")
        generate(d)
    print("Done.")
