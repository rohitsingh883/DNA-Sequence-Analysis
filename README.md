# DNA Sequence Analysis

A beginner-friendly Python bioinformatics project that reads DNA sequences from a FASTA file and reports:

- Sequence length (base pairs)
- GC content
- Nucleotide composition (A, C, G, T, N, and other ambiguous symbols)
- Number of sequences in the input file

The FASTA file is parsed automatically by Python. The script can analyse any valid DNA FASTA file; the included small file is only a demonstration input.

## Project structure

```text
DNA-Sequence-Analysis/
├── data/
│   └── demo_sequences.fasta
├── results/
│   └── demo_report.txt
├── sequence_analysis.py
└── README.md
```

## Requirements

- Python 3.8 or newer
- No external Python packages are required

## How to run

Open a terminal in the project folder.

### 1. Run with the included demonstration FASTA file

```bash
python sequence_analysis.py data/demo_sequences.fasta
```

### 2. Save the report to a text file

```bash
python sequence_analysis.py data/demo_sequences.fasta --output results/report.txt
```

### 3. Analyse another FASTA file

Place your `.fasta` or `.fa` file in the project folder (or use its full path), then run:

```bash
python sequence_analysis.py path/to/your_sequences.fasta --output results/my_report.txt
```

## Public dataset used for the project

For the internship submission, use a public nucleotide record from NCBI:

- **Accession:** U49845
- **Organism:** *Saccharomyces cerevisiae* (baker's yeast)
- **NCBI sample record:** https://www.ncbi.nlm.nih.gov/genbank/samplerecord/
- **FASTA record:** https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=U49845&db=nuccore&report=fasta&retmode=text

Open the FASTA record link, save the page contents as `data/U49845.fasta`, and run:

```bash
python sequence_analysis.py data/U49845.fasta --output results/U49845_report.txt
```

Commit both the downloaded FASTA file and the generated report to your public repository. Keep the accession and source link in this README so the dataset is traceable. The included `demo_sequences.fasta` and `demo_report.txt` are small demonstration files, not the NCBI dataset.

## Method and calculation

- **Length:** total number of sequence characters.
- **GC content:** `(G + C) / (A + C + G + T) × 100`.
- **Composition:** count and percentage of each nucleotide.
- Ambiguous bases such as `N` are included in sequence length and composition, but excluded from the GC-content denominator.

## Notes

- FASTA headers begin with `>` and identify each sequence.
- The script supports multiple sequences in one FASTA file.
- Input is converted to uppercase before analysis.
- Blank lines and wrapped FASTA sequence lines are handled.
- This project analyses nucleotide FASTA data (DNA); protein FASTA files are outside the current scope.

## Author

Rohit Kumar Singh
