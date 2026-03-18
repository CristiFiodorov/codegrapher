# A part from this code is from https://github.com/IBM/tree-sitter-codeviews/blob/main/src/comex/__init__.py

import shutil
import tempfile
from tree_sitter import Language
import os
import subprocess


def get_language_map():
    clone_directory = os.path.join(tempfile.gettempdir(), "codegrapher")
    shared_languages = os.path.join(clone_directory, "languages.so")

    grammar_repos = [
        ("https://github.com/tree-sitter/tree-sitter-java", "09d650def6cdf7f479f4b78f595e9ef5b58ce31e"),
        ("https://github.com/tree-sitter/tree-sitter-c-sharp", "3ef3f7f99e16e528e6689eae44dff35150993307"),
        ("https://github.com/tree-sitter/tree-sitter-python", "c01fb4e38587e959b9058b8cd34b9e6a3068c827"),
        ("https://github.com/tree-sitter/tree-sitter-c", "deca017a554045b4c203e7ddff39ae64ff05e071"),
        ("https://github.com/tree-sitter/tree-sitter-cpp", "d0b4e006ca3c4466f834d9a4bf709bfede13d359"),
    ]
    vendor_languages = []

    for url, commit in grammar_repos:
        grammar = url.rstrip("/").split("/")[-1]
        vendor_language = os.path.join(clone_directory, grammar)
        vendor_languages.append(vendor_language)
        if os.path.isfile(shared_languages) and not os.path.exists(vendor_language):
            os.remove(shared_languages)
        elif not os.path.isfile(shared_languages) and os.path.exists(vendor_language):
            shutil.rmtree(vendor_language)
        elif not os.path.isfile(shared_languages) and not os.path.exists(vendor_language):
            pass
        else:
            continue
        print(f"Intial Setup: {grammar}")
        os.makedirs(vendor_language, exist_ok=True)
        subprocess.check_call(["git", "init"], cwd=vendor_language, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.check_call(["git", "remote", "add", "origin", url], cwd=vendor_language, stdout=subprocess.DEVNULL,
                              stderr=subprocess.STDOUT)
        subprocess.check_call(["git", "fetch", "--depth=1", "origin", commit], cwd=vendor_language,
                              stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.check_call(["git", "checkout", "FETCH_HEAD"], cwd=vendor_language, stdout=subprocess.DEVNULL,
                              stderr=subprocess.STDOUT)

    Language.build_library(
        shared_languages,
        vendor_languages,
    )
    
    JAVA_LANGUAGE = Language(shared_languages, "java")
    C_SHARP_LANGUAGE = Language(shared_languages, "c_sharp")
    PYTHON_LANGUAGE = Language(shared_languages, "python")
    C_LANGUAGE = Language(shared_languages, "c")
    CPP_LANGUAGE = Language(shared_languages, "cpp")

    return {
        "java": JAVA_LANGUAGE,
        "cs": C_SHARP_LANGUAGE,
        "python": PYTHON_LANGUAGE,
        "c": C_LANGUAGE,
        "cpp": CPP_LANGUAGE,
    }
