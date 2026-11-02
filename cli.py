"""
Command-Line Interface for Unbotify Engine.
Tagline: "Less formula. More expression."
Supports batch document processing, fine-grained stage disabling,
max aggressiveness overrides, and telemetry reporting.
"""

import sys
import os
import argparse
import time

# Ensure src is on python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from unbotify.config import UnbotifyConfig
from unbotify.core.modifier import TextModifier
from unbotify.core.doc_processor import DocumentProcessor

BANNER = r"""
  _   _ _   _ ____   ___ _____ ___ _______   __
 | | | | \ | | __ ) / _ \_   _|_ _|  ___\ \ / /
 | | | |  \| |  _ \| | | || |  | || |_   \ V / 
 | |_| | |\  | |_) | |_| || |  | ||  _|   | |  
  \___/|_| \_|____/ \___/ |_| |___|_|     |_|  
  Less formula. More expression.
"""

def main():
    parser = argparse.ArgumentParser(
        description="Unbotify — Less formula. More expression. (Deterministic Humanization & Structural Expression Suite)"
    )
    parser.add_argument("input", nargs="?", default=None, help="Input file path or plain text string")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout or modified filename)")
    parser.add_argument("--intensity", type=float, default=75.0, help="Aggressiveness intensity (10.0 to 100.0, default: 75.0)")
    parser.add_argument("--style", default="academic", choices=["academic", "conversational", "casual", "technical"], help="Writing style register")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing output files")
    parser.add_argument("--verbose", action="store_true", help="Print detailed modification logs")
    parser.add_argument("--disable-stages", type=str, default="", help="Comma-separated stages to disable (e.g. voice,fusion,transition,nominal)")
    parser.add_argument("--max-aggressiveness", action="store_true", help="Override all fire rates to maximum (0.95)")
    parser.add_argument("--zero-expansion", action="store_true", help="Enforce strict 1:1 token count parity (0 added words)")
    parser.add_argument("--persona", default="intermediate", choices=["beginner", "intermediate", "senior"], help="Developer skill persona for code comments")
    parser.add_argument("--convert-docstrings", action="store_true", help="Convert AI triple-quote docstrings to # comments")
    parser.add_argument("--citations", action="store_true", help="Enable inline academic citation insertion")
    parser.add_argument("--max-citations", type=int, default=2, help="Max citations to insert")
    parser.add_argument("--citation-format", default="IEEE [1]", help=r"Citation format ('IEEE [1]', 'APA', 'LaTeX \cite{}')")

    args = parser.parse_args()

    print(BANNER)

    if not args.input:
        parser.print_help()
        sys.exit(1)

    config = UnbotifyConfig(
        INTENSITY=args.intensity,
        STYLE=args.style,
        ZERO_EXPANSION=args.zero_expansion,
        DEVELOPER_PERSONA=args.persona,
        CONVERT_DOCSTRINGS=args.convert_docstrings,
        ENABLE_CITATIONS=args.citations,
        MAX_CITATIONS=args.max_citations,
        CITATION_FORMAT=args.citation_format
    )

    if args.disable_stages:
        stage_map = {
            "voice": "ENABLE_VOICE_TRANSFORM",
            "fusion": "ENABLE_SENTENCE_FUSION",
            "transition": "ENABLE_TRANSITION_INJECT",
            "reorder": "ENABLE_CLAUSE_REORDER",
            "nominal": "ENABLE_NOMINALIZATION",
            "appositive": "ENABLE_APPOSITIVE",
            "discourse": "ENABLE_DISCOURSE_ROTATE",
            "synonyms": "ENABLE_SYNONYMS",
            "phrases": "ENABLE_PHRASE_REWRITE",
            "determiner": "ENABLE_DETERMINER_SWAP"
        }
        for stg in args.disable_stages.split(","):
            s_clean = stg.strip().lower()
            if s_clean in stage_map:
                setattr(config, stage_map[s_clean], False)
                print(f"  [Stage Disabled] {s_clean}")

    if args.max_aggressiveness:
        config.SYNONYM_AGGRESSIVENESS = 0.95
        config.VOICE_TRANSFORM_RATE = 0.90
        config.SENTENCE_FUSION_RATE = 0.80
        config.TRANSITION_INJECT_RATE = 0.80
        config.WORD_REORDER_RATE = 0.75
        config.NOMINALIZATION_RATE = 0.70
        config.APPOSITIVE_RATE = 0.85
        config.DISCOURSE_ROTATE_RATE = 0.95
        print("  [MAX AGGRESSIVENESS] All transformation rates maximized")

    start_time = time.time()

    # Check if input is an existing file
    if os.path.exists(args.input):
        print(f"[*] Processing document file: {args.input}")
        processor = DocumentProcessor(config)
        with open(args.input, "rb") as f:
            raw_bytes = f.read()

        lower_in = args.input.lower()
        if lower_in.endswith(".zip"):
            processed_bytes, out_name = processor.process_zip_package(raw_bytes)
        else:
            processed_bytes, _ = processor.process_file_bytes(os.path.basename(args.input), raw_bytes)
            base_root, ext = os.path.splitext(args.input)
            out_name = f"{base_root}_unbotified{ext}"

        target_out = args.output or out_name

        if args.dry_run:
            print(f"[!] DRY RUN — Generated {len(processed_bytes)} bytes. No files written.")
        else:
            with open(target_out, "wb") as f:
                f.write(processed_bytes)
            print(f"[✓] Output written to: {target_out}")

        telemetry = processor.modifier.get_telemetry()
    else:
        # Plain text processing
        modifier = TextModifier(config)
        transformed = modifier.modify_text(args.input)

        if args.dry_run:
            print("\n--- [DRY RUN TRANSFORMED OUTPUT] ---")
            print(transformed)
        elif args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(transformed)
            print(f"[✓] Output written to: {args.output}")
        else:
            print("\n--- [TRANSFORMED OUTPUT] ---")
            print(transformed)

        telemetry = modifier.get_telemetry()

    elapsed = (time.time() - start_time) * 1000.0
    print("\n" + "="*50)
    print(f" UNBOTIFY EXECUTION TELEMETRY ({elapsed:.2f} ms)")
    print("="*50)
    for k, v in telemetry.items():
        print(f"  {k.replace('_', ' ').title():<28}: {v}")
    print("="*50)

if __name__ == "__main__":
    main()
