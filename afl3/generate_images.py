"""Script untuk generate visualisasi graf AFL-3."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
import networkx as nx

from graf import Graf

IMG_DIR = Path(__file__).parent / "images"
IMG_DIR.mkdir(exist_ok=True)


def save_graf_soal1() -> None:
    """Generate visualisasi graf Soal 1."""
    g = Graf()
    g.add_nodes(["A", "B", "C", "D", "E", "F"])
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("D", "E"), ("E", "F"), ("C", "F")]
    for u, v in edges:
        g.add_edge(u, v, weight=1)

    pos = g._layout("spring")
    plt.figure(figsize=(8, 6))

    nx.draw(
        g.G,
        pos,
        with_labels=True,
        node_size=1200,
        font_size=14,
        node_color="lightblue",
        edge_color="gray",
        width=2,
    )
    edge_labels = {(u, v): "" for u, v in g.G.edges()}
    nx.draw_networkx_edge_labels(g.G, pos, edge_labels=edge_labels)
    plt.title("AFL-3 Soal 1 — Graf Tak Berarah", fontsize=16, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    out = IMG_DIR / "soal1_graph.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ Saved: {out}")


def save_graf_soal3() -> None:
    """Generate visualisasi graf Soal 3 (normal & dengan jalur terpendek)."""
    g = Graf()
    g.add_nodes(["A", "B", "C", "D", "E", "F", "G"])
    edges = [
        ("A", "B", 2),
        ("A", "C", 5),
        ("B", "D", 4),
        ("B", "E", 6),
        ("C", "F", 3),
        ("D", "G", 2),
        ("E", "F", 4),
        ("F", "G", 1),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, weight=w)

    pos = g._layout("spring")

    # Graf biasa
    plt.figure(figsize=(8, 6))
    nx.draw(
        g.G,
        pos,
        with_labels=True,
        node_size=1200,
        font_size=14,
        node_color="lightgreen",
        edge_color="gray",
        width=2,
    )
    edge_labels = g._edge_labels_for_drawing()
    nx.draw_networkx_edge_labels(g.G, pos, edge_labels=edge_labels, font_size=11)
    plt.title("AFL-3 Soal 3 — Graf Berbobot", fontsize=16, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    out1 = IMG_DIR / "soal3_graph.png"
    plt.savefig(out1, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ Saved: {out1}")

    # Graf dengan jalur terpendek A→G
    path = g.shortest_path("A", "G")
    path_edges = list(zip(path[:-1], path[1:]))

    plt.figure(figsize=(8, 6))
    nx.draw(
        g.G,
        pos,
        with_labels=True,
        node_size=1200,
        font_size=14,
        node_color="lightgreen",
        edge_color="gray",
        width=1.5,
    )
    nx.draw_networkx_edges(g.G, pos, edgelist=path_edges, width=4, edge_color="red")
    nx.draw_networkx_nodes(g.G, pos, nodelist=path, node_size=1300, node_color="yellow")
    nx.draw_networkx_edge_labels(g.G, pos, edge_labels=edge_labels, font_size=11)
    plt.title(f"AFL-3 Soal 3 — Jalur Terpendek A → G: {path}", fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    out2 = IMG_DIR / "soal3_shortest_path.png"
    plt.savefig(out2, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ Saved: {out2}")


def print_soal1_terminal() -> None:
    """Print hasil analisis Soal 1 ke terminal."""
    g = Graf()
    g.add_nodes(["A", "B", "C", "D", "E", "F"])
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("D", "E"), ("E", "F"), ("C", "F")]
    for u, v in edges:
        g.add_edge(u, v, weight=1)

    degrees = g.degree()
    cycles = g.cycles()
    connected = g.is_connected()

    print("=" * 60)
    print("AFL-3 SOAL 1 — Graf Tak Berarah, Derajat, dan Konektivitas")
    print("=" * 60)
    print("\nb) Derajat setiap simpul:")
    for node in sorted(degrees.keys(), key=str):  # type: ignore
        print(f"   {node}: {degrees[node]}")  # type: ignore

    print("\nc) Apakah graf memiliki cycle?")
    print(f"   {bool(cycles)}")
    if cycles:
        print("   Contoh cycle (cycle basis):")
        for c in cycles:
            print(f"     - {c}")

    print("\nd) Apakah graf terhubung (connected)?")
    print(f"   {connected}")
    print("=" * 60)


def print_soal3_terminal() -> None:
    """Print hasil analisis Soal 3 ke terminal."""
    g = Graf()
    g.add_nodes(["A", "B", "C", "D", "E", "F", "G"])
    edges = [
        ("A", "B", 2),
        ("A", "C", 5),
        ("B", "D", 4),
        ("B", "E", 6),
        ("C", "F", 3),
        ("D", "G", 2),
        ("E", "F", 4),
        ("F", "G", 1),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, weight=w)

    bfs = g.bfs_order("A", sort_neighbors=True)
    dfs = g.dfs_recursive("A", sort_neighbors=True)
    dists = g.dijkstra_distances("A")
    path_a_g = g.dijkstra_path("A", "G")
    dist_a_g = g.shortest_path_length("A", "G")

    print("=" * 60)
    print("AFL-3 SOAL 3 — BFS, DFS, dan Dijkstra")
    print("=" * 60)

    print("\nb) Urutan BFS dari A (tetangga diurutkan alfabet):")
    print(f"   {' -> '.join(bfs)}")

    print("\nc) Urutan DFS rekursif dari A (tetangga diurutkan alfabet):")
    print(f"   {' -> '.join(dfs)}")

    print("\nd) Algoritma Dijkstra dari A:")
    print("   1. Jarak minimum dari A ke seluruh simpul:")
    for node in sorted(dists.keys(), key=str):
        print(f"      A -> {node}: {dists[node]:g}")

    print("\n   2. Jalur terpendek dari A ke G:")
    print(f"      Jalur: {' -> '.join(path_a_g)}")
    print(f"      Total bobot: {dist_a_g:g}")
    print("=" * 60)


def main() -> None:
    print("Generating AFL-3 visualizations...\n")
    save_graf_soal1()
    save_graf_soal3()

    print("\n" + "=" * 60)
    print("Terminal Output - Soal 1")
    print("=" * 60 + "\n")
    print_soal1_terminal()

    print("\n\n" + "=" * 60)
    print("Terminal Output - Soal 3")
    print("=" * 60 + "\n")
    print_soal3_terminal()

    print(f"\n\n✓ All images generated successfully in: {IMG_DIR}")


if __name__ == "__main__":
    main()
