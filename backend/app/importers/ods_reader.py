from pathlib import Path
from typing import Any

from odf.opendocument import load
from odf.table import Table, TableRow
from odf.text import P


class OdsReadError(ValueError):
    """
    Error producido al leer la estructura del ODS.
    """

    pass


def _node_text(node: Any) -> str:
    """
    Extrae recursivamente el texto de un nodo ODF.
    """

    parts: list[str] = []

    if getattr(node, "data", None):
        parts.append(str(node.data))

    for child in getattr(node, "childNodes", []):
        parts.append(_node_text(child))

    return "".join(parts)


def _cell_text(cell: Any) -> str:
    """
    Obtiene el contenido textual completo de una celda.
    """

    paragraphs = [
        _node_text(paragraph)
        for paragraph in cell.getElementsByType(P)
    ]

    return "\n".join(paragraphs).strip()


def read_ods_sheet(
    file_path: Path,
    sheet_name: str,
) -> list[dict[str, str]]:
    """
    Lee una hoja del archivo ODS y retorna sus filas
    como diccionarios.

    La primera fila se utiliza como encabezado.

    También agrega temporalmente el campo:
        __row_number__

    Este campo permite identificar la fila cuando ocurre
    un error de validación.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"No existe el archivo ODS: {file_path}"
        )

    document = load(str(file_path))

    target_table = next(
        (
            table
            for table in document.spreadsheet.getElementsByType(
                Table
            )
            if table.getAttribute("name") == sheet_name
        ),
        None,
    )

    if target_table is None:
        raise OdsReadError(
            f"No existe la hoja '{sheet_name}' "
            f"en el archivo {file_path.name}."
        )

    matrix: list[list[str]] = []

    for row in target_table.getElementsByType(TableRow):
        values: list[str] = []

        row_repeat = int(
            row.getAttribute("numberrowsrepeated") or 1
        )

        for cell in row.childNodes:
            if (
                getattr(cell, "tagName", None)
                != "table:table-cell"
            ):
                continue

            column_repeat = int(
                cell.getAttribute(
                    "numbercolumnsrepeated"
                )
                or 1
            )

            value = _cell_text(cell)

            values.extend(
                [value] * column_repeat
            )

        while values and values[-1] == "":
            values.pop()

        # Evita expandir una cantidad excesiva de filas
        # completamente vacías.
        if not values:
            matrix.append([])
            continue

        for _ in range(row_repeat):
            matrix.append(values.copy())

    while matrix and not matrix[-1]:
        matrix.pop()

    if not matrix:
        return []

    headers = [
        header.strip()
        for header in matrix[0]
    ]

    if not any(headers):
        raise OdsReadError(
            f"La hoja '{sheet_name}' "
            "no contiene encabezados."
        )

    records: list[dict[str, str]] = []

    for row_number, row in enumerate(
        matrix[1:],
        start=2,
    ):
        if not any(
            value.strip()
            for value in row
        ):
            continue

        padded_row = row + [""] * max(
            0,
            len(headers) - len(row),
        )

        record = {
            header: padded_row[index].strip()
            for index, header in enumerate(headers)
            if header
        }

        record["__row_number__"] = str(
            row_number
        )

        records.append(record)

    return records