#!/usr/bin/env python3
"""Calculate basic statistics for DNA sequences stored in a FASTA file."""

import argparse
from collections import Counter
from pathlib import Path

DNA_BASES = "ACGT"


def parse_fasta(file_path):
    """Read FASTA records and return (header, sequence) pairs."""
    records = []
    header = None
    sequence_parts = []

    with open(file_path, "r", encoding="utf-8") as fasta_file:
        for line_number, line in enumerate(fasta_file, start=1):
            line = line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if header is not None:
                    records.append((header, "".join(sequence_parts).upper()))
                header = line[1:].strip()
                if not header:
                    raise ValueError(f"Empty FASTA header at line {line_number}.")
                sequence_parts = []
            else:
                if header is None:
                    raise ValueError(
                        f"Sequence data found before the first FASTA header "
                        f"(line {line_number})."
                    )
                sequence_parts.append("".join(line.split()))

    if header is not None:
        records.append((header, "".join(sequence_parts).upper()))

    if not records:
        raise ValueError("No FASTA sequences were found.")

    for record_header, sequence in records:
        if not sequence:
            raise ValueError(f"Sequence is empty: {record_header}")

    return records


def analyse_sequence(sequence):
    """Return length, GC percentage, and nucleotide composition."""
    counts = Counter(sequence)
    length = len(sequence)
    canonical_count = sum(counts[base] for base in DNA_BASES)
    gc_count = counts["G"] + counts["C"]

    # GC% is calculated over A/C/G/T bases only; ambiguous symbols are excluded.
    gc_percent = (gc_count / canonical_count * 100) if canonical_count else 0.0

    composition = {
        base: (counts[base] / length * 100) for base in "ACGTN"
    }
    other_count = length - sum(counts[base] for base in "ACGTN")
    composition["Other"] = other_count / length * 100

    return length, gc_percent, counts, composition


def build_report(records, input_name):
    lines = [
        "DNA SEQUENCE ANALYSIS REPORT",
        "=" * 30,
        f"Input file: {input_name}",
        f"Number of sequences: {len(records)}",
        "",
    ]

    for index, (header, sequence) in enumerate(records, start=1):
        length, gc_percent, counts, composition = analyse_sequence(sequence)
        lines.extend([
            f"Sequence {index}: {header}",
            "-" * (12 + len(str(index)) + len(header)),
            f"Length: {length} bp",
            f"GC content: {gc_percent:.2f}%",
            "Nucleotide composition (count and percentage):",
        ])

        for base in "ACGTN":
            lines.append(
                f"  {base}: {counts[base]} "
                f"({composition[base]:.2f}%)"
            )

        if composition["Other"] > 0:
            lines.append(
                f"  Other: {sum(counts.values()) - sum(counts[b] for b in 'ACGTN')} "
                f"({composition['Other']:.2f}%)"
            )
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyse length, GC content, and composition of FASTA sequences."
    )
    parser.add_argument("input", help="Path to a DNA FASTA file")
    parser.add_argument(
        "-o", "--output",
        help="Optional path to save the report as a text file"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        parser.error(f"Input file not found: {input_path}")

    try:
        records = parse_fasta(input_path)
        report = build_report(records, input_path.name)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(report)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report + "\n", encoding="utf-8")
        print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
