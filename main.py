import sys
from pathlib import Path

from rich import print

from src import Parser, evaluate, scan

LISP_SNIPPET_DIR = Path("lisp_snippets")


def process_snippet(snippet_name: str, snippet_dir: Path):
    raw_source_text = (snippet_dir / snippet_name).read_text()
    print(f"Source:\n{raw_source_text}")

    tokens = scan(raw_source_text)

    ast = Parser(tokens=tokens).parse()
    print(f"Final AST for {snippet_name}:")
    print(ast)

    val = evaluate(ast)
    print("Value:", val)


def main():
    if len(sys.argv) > 1:
        snippet_path = Path(sys.argv[1])
        process_snippet(snippet_path.name, snippet_path.parent)
    else:
        for snippet_path in LISP_SNIPPET_DIR.glob("*.lisp"):
            process_snippet(snippet_path.name, LISP_SNIPPET_DIR)


if __name__ == "__main__":
    main()
