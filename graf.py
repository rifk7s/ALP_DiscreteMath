from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import networkx as nx


Node = Any
Edge = Tuple[Node, Node]


@dataclass(frozen=True)
class DrawOptions:
    with_labels: bool = True
    with_weights: bool = True
    node_size: int = 900
    font_size: int = 10


class Graf:
    """Wrapper sederhana untuk belajar teori graf memakai NetworkX.

    Default: graf tak-berarah berbobot (nx.Graph) dengan atribut edge 'weight'.
    """

    def __init__(self, *, directed: bool = False, multigraph: bool = False):
        self.directed = directed
        self.multigraph = multigraph

        if multigraph and directed:
            self.G: nx.Graph = nx.MultiDiGraph()
        elif multigraph:
            self.G = nx.MultiGraph()
        elif directed:
            self.G = nx.DiGraph()
        else:
            self.G = nx.Graph()

    # ----------------------------
    # Metode dasar (rubrik)
    # ----------------------------
    def add_node(self, node: Node, **attrs: Any) -> None:
        self.G.add_node(node, **attrs)

    def add_nodes(self, nodes: Iterable[Node]) -> None:
        self.G.add_nodes_from(nodes)

    def add_edge(self, u: Node, v: Node, **attrs: Any) -> None:
        # Pastikan weight ada jika user tidak set
        if "weight" not in attrs:
            attrs["weight"] = 1.0
        self.G.add_edge(u, v, **attrs)

    def visualize_graph(
        self,
        *,
        title: str = "Graf",
        pos: Optional[Dict[Node, Tuple[float, float]]] = None,
        layout: str = "spring",
        draw: DrawOptions = DrawOptions(),
    ) -> Dict[Node, Tuple[float, float]]:
        """Visualisasi graf. Mengembalikan posisi node (pos) agar bisa dipakai ulang."""
        if pos is None:
            pos = self._layout(layout)

        plt.figure(figsize=(7.5, 5.5))
        nx.draw(
            self.G,
            pos,
            with_labels=draw.with_labels,
            node_size=draw.node_size,
            font_size=draw.font_size,
        )

        if draw.with_weights:
            edge_labels = self._edge_labels_for_drawing()
            if edge_labels:
                nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)

        plt.title(title)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
        return pos

    def shortest_path(self, source: Node, target: Node, *, weight: str = "weight") -> List[Node]:
        """Mengembalikan list node jalur terpendek (berbobot jika weight ada)."""
        return nx.shortest_path(self.G, source=source, target=target, weight=weight)

    def shortest_path_length(self, source: Node, target: Node, *, weight: str = "weight") -> float:
        """Jarak (total bobot) jalur terpendek dari source ke target."""
        return float(nx.shortest_path_length(self.G, source=source, target=target, weight=weight))

    def visual_shortest_path(
        self,
        source: Node,
        target: Node,
        *,
        weight: str = "weight",
        title: Optional[str] = None,
        pos: Optional[Dict[Node, Tuple[float, float]]] = None,
        layout: str = "spring",
    ) -> List[Node]:
        """Visualisasi graf dengan jalur terpendek disorot. Return path list."""
        path = self.shortest_path(source, target, weight=weight)
        if pos is None:
            pos = self._layout(layout)

        # edges pada path
        path_edges = list(zip(path[:-1], path[1:]))

        plt.figure(figsize=(7.5, 5.5))

        # gambar semua edges (tipis)
        nx.draw(
            self.G,
            pos,
            with_labels=True,
            node_size=900,
            font_size=10,
            width=1.2,
        )

        # sorot edges path
        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=path_edges,
            width=3.2,
        )

        # sorot nodes di path
        nx.draw_networkx_nodes(
            self.G,
            pos,
            nodelist=path,
            node_size=950,
        )

        edge_labels = self._edge_labels_for_drawing()
        if edge_labels:
            # tampilkan label bobot hanya untuk edge yang ada weight
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)

        if title is None:
            title = f"Jalur Terpendek {source} → {target}: {path}"
        plt.title(title)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

        return path

    # ----------------------------
    # Metode tambahan (≥5)
    # ----------------------------
    def nodes(self) -> List[Node]:
        return list(self.G.nodes())

    def edges(self, *, data: bool = False) -> List[Any]:
        return list(self.G.edges(data=data))

    def neighbors(self, node: Node) -> List[Node]:
        self._require_node(node)
        return list(self.G.neighbors(node))

    def degree(self, node: Optional[Node] = None) -> Union[int, Dict[Node, int]]:
        if node is None:
            return {n: int(d) for n, d in self.G.degree()}
        self._require_node(node)
        return int(self.G.degree(node))

    def is_connected(self) -> bool:
        if self.G.number_of_nodes() == 0:
            return True
        if self.directed:
            return nx.is_strongly_connected(self.G)  # type: ignore[arg-type]
        return nx.is_connected(self.G)  # type: ignore[arg-type]

    def connected_components(self) -> List[List[Node]]:
        if self.G.number_of_nodes() == 0:
            return []
        if self.directed:
            comps = nx.strongly_connected_components(self.G)  # type: ignore[arg-type]
        else:
            comps = nx.connected_components(self.G)  # type: ignore[arg-type]
        return [sorted(c, key=str) for c in comps]

    def has_path(self, source: Node, target: Node) -> bool:
        self._require_node(source)
        self._require_node(target)
        return nx.has_path(self.G, source, target)

    def bfs(self, start: Node) -> List[Node]:
        self._require_node(start)
        return list(nx.bfs_tree(self.G, start).nodes())

    def dfs(self, start: Node) -> List[Node]:
        self._require_node(start)
        return list(nx.dfs_preorder_nodes(self.G, source=start))

    def bfs_order(self, start: Node, *, sort_neighbors: bool = True) -> List[Node]:
        """Urutan BFS deterministik.

        Jika `sort_neighbors=True`, tetangga diproses berdasarkan `str(node)` agar
        stabil untuk label alfabet seperti A,B,C,...
        """
        self._require_node(start)
        visited: set[Node] = {start}
        order: list[Node] = []
        queue: list[Node] = [start]

        while queue:
            u = queue.pop(0)
            order.append(u)
            neighbors = list(self.G.neighbors(u))
            if sort_neighbors:
                neighbors.sort(key=str)
            for v in neighbors:
                if v in visited:
                    continue
                visited.add(v)
                queue.append(v)
        return order

    def dfs_recursive(self, start: Node, *, sort_neighbors: bool = True) -> List[Node]:
        """Urutan DFS rekursif deterministik.

        Jika `sort_neighbors=True`, tetangga diproses berdasarkan `str(node)`.
        """
        self._require_node(start)
        visited: set[Node] = set()
        order: list[Node] = []

        def visit(u: Node) -> None:
            visited.add(u)
            order.append(u)
            neighbors = list(self.G.neighbors(u))
            if sort_neighbors:
                neighbors.sort(key=str)
            for v in neighbors:
                if v not in visited:
                    visit(v)

        visit(start)
        return order

    def dijkstra_distances(self, source: Node, *, weight: str = "weight") -> Dict[Node, float]:
        """Jarak minimum dari source ke semua simpul (Dijkstra, graf berbobot non-negatif)."""
        self._require_node(source)
        dist = nx.single_source_dijkstra_path_length(self.G, source=source, weight=weight)
        return {k: float(v) for k, v in dist.items()}

    def dijkstra_path(self, source: Node, target: Node, *, weight: str = "weight") -> List[Node]:
        """Jalur terpendek (Dijkstra) dari source ke target."""
        self._require_node(source)
        self._require_node(target)
        return nx.dijkstra_path(self.G, source=source, target=target, weight=weight)

    def has_cycle(self) -> bool:
        if self.directed:
            return not nx.is_directed_acyclic_graph(self.G)
        try:
            nx.find_cycle(self.G)
            return True
        except nx.exception.NetworkXNoCycle:
            return False

    def cycles(self) -> List[List[Node]]:
        """Daftar cycle pada graf.

        - Undirected: gunakan cycle basis.
        - Directed: gunakan simple_cycles.
        """
        if self.directed:
            return [list(c) for c in nx.simple_cycles(self.G)]  # type: ignore[arg-type]
        return [list(c) for c in nx.cycle_basis(self.G)]  # type: ignore[arg-type]

    def minimum_spanning_tree(self, *, weight: str = "weight") -> "Graf":
        if self.directed:
            raise ValueError("MST hanya untuk graf tak-berarah")
        mst_nx = nx.minimum_spanning_tree(self.G, weight=weight)  # type: ignore[arg-type]
        mst = Graf(directed=False, multigraph=False)
        mst.G = mst_nx
        return mst

    def betweenness_centrality(self) -> Dict[Node, float]:
        return nx.betweenness_centrality(self.G)

    def is_bipartite(self) -> bool:
        try:
            return nx.is_bipartite(self.G)
        except Exception:
            return False

    def adjacency_matrix(self) -> List[List[float]]:
        nodes = self.nodes()
        index = {n: i for i, n in enumerate(nodes)}
        n = len(nodes)
        mat = [[0.0 for _ in range(n)] for _ in range(n)]

        if self.multigraph:
            for u, v, data in self.G.edges(data=True):
                w = float(data.get("weight", 1.0))
                mat[index[u]][index[v]] += w
                if not self.directed:
                    mat[index[v]][index[u]] += w
        else:
            for u, v, data in self.G.edges(data=True):
                w = float(data.get("weight", 1.0))
                mat[index[u]][index[v]] = w
                if not self.directed:
                    mat[index[v]][index[u]] = w

        return mat

    def __repr__(self) -> str:
        kind = "DiGraph" if self.directed else "Graph"
        if self.multigraph:
            kind = "Multi" + kind
        return f"Graf({kind}, |V|={self.G.number_of_nodes()}, |E|={self.G.number_of_edges()})"

    # ----------------------------
    # Helper internal
    # ----------------------------
    def _require_node(self, node: Node) -> None:
        if node not in self.G:
            raise ValueError(f"Node {node!r} tidak ada di graf")

    def _layout(self, layout: str) -> Dict[Node, Tuple[float, float]]:
        layout = layout.lower().strip()
        if layout == "spring":
            return nx.spring_layout(self.G, seed=42)
        if layout == "kamada_kawai":
            return nx.kamada_kawai_layout(self.G)
        if layout == "circular":
            return nx.circular_layout(self.G)
        if layout == "shell":
            return nx.shell_layout(self.G)
        raise ValueError("layout tidak dikenal. Pilih: spring|kamada_kawai|circular|shell")

    def _edge_labels_for_drawing(self) -> Dict[Edge, str]:
        labels: Dict[Edge, str] = {}
        if self.multigraph:
            # MultiGraph: label per (u,v,key) cukup ribet untuk gambar; tampilkan jumlah weight total.
            for u, v in self.G.edges():
                data_dict = self.G.get_edge_data(u, v)
                if not data_dict:
                    continue
                total = 0.0
                for _k, attrs in data_dict.items():
                    total += float(attrs.get("weight", 1.0))
                labels[(u, v)] = f"{total:g}"
            return labels

        for u, v, data in self.G.edges(data=True):
            if "weight" in data:
                labels[(u, v)] = f"{float(data['weight']):g}"
        return labels
