import argparse
import json
from pathlib import Path

from app.db.seed import seed_database


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Importa EPS, usuarios de demostración "
            "y pacientes desde un archivo ODS."
        )
    )

    parser.add_argument(
        "--file",
        type=Path,
        default=None,
        help=(
            "Ruta opcional del archivo ODS. "
            "Si se omite, se utiliza SEED_FILE."
        ),
    )

    return parser


def main() -> None:
    parser = build_parser()
    arguments = parser.parse_args()

    result = seed_database(
        arguments.file
    )

    print(
        json.dumps(
            result.to_dict(),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()