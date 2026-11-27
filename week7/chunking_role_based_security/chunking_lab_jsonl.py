"""Testleaf FDE Week 7 — Compare four document chunking strategies on Kubernetes docs.

Reads from kube_documents.jsonl and applies 4 chunking methods to each document.
Produces a CSV comparison table and detailed JSON analysis.

Install: python -m pip install -r requirements.txt
Run:     python chunking_lab_jsonl.py
Config:  Edit chunking_config.json to adjust parameters
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

STRATEGIES = ("fixed", "recursive", "structure", "semantic")


def load_config(config_file: str = "chunking_config.json") -> dict:
    """Load chunking configuration from JSON file."""
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def fixed_size(text: str, size: int, overlap: int) -> list[dict[str, Any]]:
    """Split mechanically every N characters."""
    chunks: list[dict[str, Any]] = []
    step = size - overlap
    for start in range(0, len(text), step):
        end = min(start + size, len(text))
        chunks.append({
            "text": text[start:end],
            "metadata": {"start": start, "end": end, "size": end - start}
        })
        if end == len(text):
            break
    return chunks


def recursive(text: str, size: int, overlap: int) -> list[dict[str, Any]]:
    """Try paragraph, line, space, then character boundaries."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )
    return [
        {
            "text": piece,
            "metadata": {"size": len(piece)}
        }
        for piece in splitter.split_text(text)
    ]


def structure_aware(text: str) -> list[dict[str, Any]]:
    """Split on Markdown headings; preserve heading path."""
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "H1"),
            ("##", "H2"),
            ("###", "H3"),
        ],
        strip_headers=False,
    )
    documents = splitter.split_text(text)
    return [
        {
            "text": doc.page_content,
            "metadata": {**dict(doc.metadata), "size": len(doc.page_content)}
        }
        for doc in documents
    ]


def semantic(text: str, threshold: float) -> list[dict[str, Any]]:
    """Split at semantic change points using embeddings."""
    from langchain_experimental.text_splitter import SemanticChunker
    from langchain_huggingface import HuggingFaceEmbeddings

    embedder = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    splitter = SemanticChunker(
        embedder,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=threshold,
    )
    return [
        {
            "text": doc.page_content,
            "metadata": {**dict(doc.metadata), "size": len(doc.page_content)}
        }
        for doc in splitter.create_documents([text])
    ]


def run_method(
    name: str, text: str, size: int, overlap: int, threshold: float
) -> list[dict[str, Any]]:
    """Run specified chunking method."""
    if name == "fixed":
        return fixed_size(text, size, overlap)
    if name == "recursive":
        return recursive(text, size, overlap)
    if name == "structure":
        return structure_aware(text)
    return semantic(text, threshold)


def analyze_chunks(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    """Generate statistics about chunks."""
    if not chunks:
        return {"total": 0}
    
    sizes = [chunk["metadata"].get("size", len(chunk["text"])) for chunk in chunks]
    
    return {
        "total": len(chunks),
        "total_chars": sum(sizes),
        "avg_size": statistics.mean(sizes),
        "min_size": min(sizes),
        "max_size": max(sizes),
        "median_size": statistics.median(sizes),
        "stdev": statistics.stdev(sizes) if len(sizes) > 1 else 0,
    }


def has_heading_preservation(chunks: list[dict[str, Any]]) -> bool:
    """Check if chunks contain heading metadata."""
    return any(
        any(key.startswith("H") for key in chunk.get("metadata", {}).keys())
        for chunk in chunks
    )


def get_boundary_examples(text: str, chunks: list[dict[str, Any]], num_examples: int = 3) -> dict:
    """Find good and poor chunk boundaries."""
    examples = {
        "first_chunks": [],
        "last_chunks": [],
        "incomplete_sentences": [],
        "good_boundaries": []
    }
    
    # First and last chunks
    for chunk in chunks[:num_examples]:
        examples["first_chunks"].append({
            "text": chunk["text"][:100] + "..." if len(chunk["text"]) > 100 else chunk["text"],
            "complete": chunk["text"].strip().endswith(('.', '!', '?', ':', '\n'))
        })
    
    for chunk in chunks[-num_examples:]:
        examples["last_chunks"].append({
            "text": chunk["text"][-100:] if len(chunk["text"]) > 100 else chunk["text"],
            "complete": chunk["text"].strip().endswith(('.', '!', '?', ':', '\n'))
        })
    
    # Find incomplete sentences (poor boundaries)
    for i, chunk in enumerate(chunks[:-1]):
        chunk_text = chunk["text"].strip()
        if chunk_text and not chunk_text.endswith(('.', '!', '?', ':', '\n')) and not chunk_text.endswith('#'):
            next_start = chunks[i+1]["text"][:50]
            examples["incomplete_sentences"].append({
                "chunk_ending": chunk_text[-80:],
                "next_start": next_start,
                "index": i
            })
            if len(examples["incomplete_sentences"]) >= num_examples:
                break
    
    # Find good boundaries (complete sentences)
    good_count = 0
    for chunk in chunks:
        chunk_text = chunk["text"].strip()
        if chunk_text.endswith(('.', '!', '?')):
            examples["good_boundaries"].append({
                "text": chunk_text[-100:],
                "ends_properly": True
            })
            good_count += 1
            if good_count >= num_examples:
                break
    
    return examples


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare four RAG chunking methods on Kubernetes docs from JSONL"
    )
    parser.add_argument(
        "--jsonl",
        default=r"C:\min\tech\FDE\week7\chunking_role_based_security\data\kube_documents.jsonl",
        help="Path to kube_documents.jsonl"
    )
    parser.add_argument(
        "--config",
        default="chunking_config.json",
        help="Path to configuration JSON file"
    )
    parser.add_argument(
        "--out",
        default=r"C:\min\tech\FDE\week7\chunking_role_based_security\results",
        help="Output directory for results"
    )
    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config(args.config)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    jsonl_path = Path(args.jsonl)
    if not jsonl_path.exists():
        print(f"Error: JSONL file not found: {args.jsonl}")
        return

    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load documents
    documents = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                documents.append(json.loads(line))

    print(f"\n📄 Loaded {len(documents)} documents from {jsonl_path.name}")
    print(f"📊 Processing all 4 chunking strategies...\n")

    # Store results for comparison
    comparison_data = []
    detailed_results = []

    # Process each document with each strategy
    for doc_idx, doc in enumerate(documents, 1):
        doc_id = doc.get("document_id", f"DOC-{doc_idx}")
        title = doc.get("title", "Untitled")
        content = doc.get("content", "")

        if not content.strip():
            print(f"⚠️  Skipping {doc_id}: empty content")
            continue

        print(f"[{doc_idx}/{len(documents)}] Processing: {doc_id} — {title[:60]}")
        print(f"      Content length: {len(content)} characters")

        doc_results = {
            "document_id": doc_id,
            "title": title,
            "content_length": len(content),
            "strategies": {}
        }

        for strategy in STRATEGIES:
            try:
                # Run chunking strategy
                if strategy == "structure" and "#" not in content:
                    print(f"      ⚠️  {strategy}: No headings found, skipping")
                    continue

                chunks = run_method(
                    strategy,
                    content,
                    config["fixed_size"]["chunk_size"],
                    config["fixed_size"]["overlap"],
                    config["semantic"]["semantic_percentile"],
                )

                stats = analyze_chunks(chunks)
                has_headings = has_heading_preservation(chunks)
                boundary_examples = get_boundary_examples(content, chunks)

                strategy_result = {
                    "strategy": strategy,
                    "statistics": stats,
                    "has_heading_metadata": has_headings,
                    "boundary_analysis": boundary_examples,
                    "sample_chunks": {
                        "first": chunks[0]["text"][:150] if chunks else "",
                        "last": chunks[-1]["text"][-150:] if chunks else ""
                    }
                }

                doc_results["strategies"][strategy] = strategy_result

                # Add to comparison
                comparison_data.append({
                    "document_id": doc_id,
                    "title": title[:40],
                    "strategy": strategy.upper(),
                    "total_chunks": stats["total"],
                    "avg_size": f"{stats['avg_size']:.1f}",
                    "min_size": stats["min_size"],
                    "max_size": stats["max_size"],
                    "has_headings": "Yes" if has_headings else "No",
                    "complete_boundaries": len(boundary_examples["good_boundaries"]),
                    "incomplete_boundaries": len(boundary_examples["incomplete_sentences"]),
                })

                print(f"      ✓ {strategy}: {stats['total']} chunks (avg {stats['avg_size']:.0f} chars)")

            except Exception as e:
                print(f"      ✗ {strategy}: {str(e)[:60]}")

        detailed_results.append(doc_results)

    # Write detailed JSON results
    details_file = output_dir / "chunking_analysis_detailed.json"
    with open(details_file, 'w', encoding='utf-8') as f:
        json.dump(detailed_results, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Detailed results: {details_file}")

    # Write comparison CSV
    if comparison_data:
        csv_file = output_dir / "chunking_comparison.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=comparison_data[0].keys())
            writer.writeheader()
            writer.writerows(comparison_data)
        print(f"✓ Comparison table: {csv_file}")

    # Generate markdown summary
    markdown_file = output_dir / "CHUNKING_ANALYSIS.md"
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write("# Kubernetes Documentation Chunking Strategy Comparison\n\n")
        f.write(f"**Analysis Date:** {Path(markdown_file).stat().st_mtime}\n")
        f.write(f"**Documents Analyzed:** {len(documents)}\n\n")

        f.write("## Strategy Overview\n\n")
        for strategy in STRATEGIES:
            if strategy in config:
                f.write(f"### {strategy.upper()}\n")
                f.write(f"{config[strategy]['description']}\n\n")

        f.write("## Results Summary\n\n")

        # Aggregate statistics
        f.write("### Aggregate Statistics by Strategy\n\n")
        f.write("| Strategy | Avg Chunks | Avg Size | Min Size | Max Size | Heading Preservation |\n")
        f.write("|----------|-----------|----------|----------|----------|----------------------|\n")

        strategy_stats = {}
        for row in comparison_data:
            strategy = row["strategy"]
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {
                    "chunks": [],
                    "sizes": [],
                    "headings": 0,
                    "count": 0
                }
            strategy_stats[strategy]["chunks"].append(int(row["total_chunks"]))
            strategy_stats[strategy]["sizes"].append(float(row["avg_size"]))
            strategy_stats[strategy]["headings"] += (1 if row["has_headings"] == "Yes" else 0)
            strategy_stats[strategy]["count"] += 1

        for strategy, stats_list in sorted(strategy_stats.items()):
            avg_chunks = statistics.mean(stats_list["chunks"]) if stats_list["chunks"] else 0
            avg_size = statistics.mean(stats_list["sizes"]) if stats_list["sizes"] else 0
            heading_pct = (stats_list["headings"] / stats_list["count"] * 100) if stats_list["count"] > 0 else 0

            f.write(f"| {strategy.upper()} | {avg_chunks:.1f} | {avg_size:.0f} | ")
            f.write(f"{min(stats_list['chunks']) if stats_list['chunks'] else 0} | ")
            f.write(f"{max(stats_list['chunks']) if stats_list['chunks'] else 0} | {heading_pct:.0f}% |\n")

        f.write("\n## Detailed Findings\n\n")
        for doc_result in detailed_results:
            f.write(f"### {doc_result['document_id']}: {doc_result['title']}\n\n")
            for strategy, result in doc_result["strategies"].items():
                stats = result["statistics"]
                f.write(f"**{strategy.upper()}**\n")
                f.write(f"- Total Chunks: {stats['total']}\n")
                f.write(f"- Average Size: {stats['avg_size']:.1f} chars\n")
                f.write(f"- Min/Max: {stats['min_size']}/{stats['max_size']} chars\n")
                f.write(f"- Heading Preservation: {'Yes' if result['has_heading_metadata'] else 'No'}\n")
                f.write(f"- Good Boundaries: {result['boundary_analysis']['good_boundaries'].__len__()}\n")
                f.write(f"- Incomplete Boundaries: {result['boundary_analysis']['incomplete_sentences'].__len__()}\n\n")

        f.write("\n## Recommendation\n\n")
        f.write("### Best Strategy for Kubernetes Documentation: **STRUCTURE-AWARE CHUNKING**\n\n")
        f.write("**Why:**\n")
        f.write("1. **Preserves Context**: Maintains heading hierarchy, keeping related content together\n")
        f.write("2. **Respects Semantics**: Splits at logical boundaries (sections) rather than arbitrary character limits\n")
        f.write("3. **Improves Retrieval**: Semantic search can more easily match user queries to relevant sections\n")
        f.write("4. **Maintains Coherence**: Avoids splitting in the middle of concepts or procedures\n")
        f.write("5. **Flexible Size**: Works regardless of content length, unlike fixed-size chunking\n\n")
        f.write("**When to use alternatives:**\n")
        f.write("- **Fixed-size**: When you have strict token/embedding limits\n")
        f.write("- **Recursive**: When markdown structure is inconsistent or absent\n")
        f.write("- **Semantic**: When you want to combine semantic + size constraints (use with structure-aware)\n")

    print(f"✓ Markdown summary: {markdown_file}")
    print(f"\n✅ Analysis complete! Check the results/ directory for all outputs.")


if __name__ == "__main__":
    main()
