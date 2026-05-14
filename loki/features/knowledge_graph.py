"""
KnowledgeGraph — extract entities and relationships from notes/files,
build a simple in-memory graph, and answer graph queries via LLM.
"""

import json
import logging
import re
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

SUPPORTED_EXTS = {".txt", ".md", ".rst", ".py", ".js", ".ts", ".json", ".yaml", ".yml"}


class KnowledgeGraph:
    def __init__(self, brain: Optional["LokiBrain"] = None, graph_path: Optional[str] = None):
        self._brain = brain
        self._graph_path = Path(graph_path) if graph_path else Path.home() / ".loki_knowledge_graph.json"
        self._nodes: dict[str, dict] = {}
        self._edges: list[dict] = []
        self._load()

    def _llm(self, prompt: str) -> str:
        if not self._brain:
            return ""
        return "".join(self._brain.ask(prompt))

    def _load(self):
        if self._graph_path.exists():
            try:
                data = json.loads(self._graph_path.read_text(encoding="utf-8"))
                self._nodes = data.get("nodes", {})
                self._edges = data.get("edges", [])
            except Exception:
                pass

    def _save(self):
        try:
            self._graph_path.write_text(
                json.dumps({"nodes": self._nodes, "edges": self._edges}, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            logger.warning("Could not save knowledge graph: %s", e)

    def _extract_entities(self, text: str, source: str) -> list[dict]:
        """Use LLM to extract entities and relationships from text."""
        if not self._brain:
            # Fallback: extract capitalized multi-word phrases as entities
            entities = re.findall(r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\b", text)
            return [{"entity": e, "type": "concept", "source": source} for e in set(entities)][:20]

        snippet = text[:1200]
        prompt = (
            f"Extract entities and relationships from this text as JSON.\n"
            f"Source: {source}\n\nText:\n{snippet}\n\n"
            f"Return JSON: {{\"entities\": [{{\"name\": str, \"type\": str}}], "
            f"\"relations\": [{{\"from\": str, \"relation\": str, \"to\": str}}]}}\n"
            f"Types: person, place, organization, concept, technology, event, project\n"
            f"Only return valid JSON, no prose."
        )
        raw = self._llm(prompt)
        try:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                return [json.loads(match.group())]
        except Exception:
            pass
        return []

    def ingest_file(self, file_path: str) -> dict:
        """Read a file and add its entities to the graph."""
        fp = Path(file_path).expanduser().resolve()
        if not fp.exists():
            return {"success": False, "message": f"File not found: {file_path}"}
        if fp.suffix.lower() not in SUPPORTED_EXTS:
            return {"success": False, "message": f"Unsupported file type: {fp.suffix}"}

        try:
            text = fp.read_text(encoding="utf-8", errors="replace")[:3000]
        except Exception as e:
            return {"success": False, "message": f"Could not read file: {e}"}

        source = fp.name
        extracted = self._extract_entities(text, source)
        n_added = 0

        for item in extracted:
            if isinstance(item, dict) and "entities" in item:
                for ent in item.get("entities", []):
                    key = ent["name"].lower()
                    if key not in self._nodes:
                        self._nodes[key] = {"name": ent["name"], "type": ent.get("type", "concept"), "sources": [source]}
                        n_added += 1
                    elif source not in self._nodes[key].get("sources", []):
                        self._nodes[key]["sources"].append(source)
                for rel in item.get("relations", []):
                    self._edges.append({
                        "from": rel.get("from", "").lower(),
                        "relation": rel.get("relation", "relates_to"),
                        "to": rel.get("to", "").lower(),
                        "source": source,
                    })

        self._save()
        return {
            "success": True,
            "message": f"Ingested {source}: added {n_added} new entities, {len(self._edges)} total relations.",
            "data": {"entities_added": n_added, "total_nodes": len(self._nodes), "total_edges": len(self._edges)},
        }

    def ingest_directory(self, directory: str) -> dict:
        """Ingest all supported files in a directory."""
        base = Path(directory).expanduser().resolve()
        if not base.exists():
            return {"success": False, "message": f"Directory not found: {directory}"}

        files = [f for f in base.rglob("*") if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS][:30]
        if not files:
            return {"success": False, "message": "No supported files found."}

        total_added = 0
        for f in files:
            result = self.ingest_file(str(f))
            if result["success"]:
                total_added += result["data"].get("entities_added", 0)

        return {
            "success": True,
            "message": f"Ingested {len(files)} files, {total_added} new entities. Graph: {len(self._nodes)} nodes, {len(self._edges)} edges.",
            "data": {"files": len(files), "entities_added": total_added},
        }

    def query(self, question: str) -> dict:
        """Answer a question about the knowledge graph via LLM."""
        if not self._nodes:
            return {"success": False, "message": "Knowledge graph is empty. Ingest some files first."}

        # Build a compact graph summary for the LLM
        nodes_summary = "\n".join(
            f"  {v['name']} ({v['type']}) — from: {', '.join(v.get('sources', [])[:2])}"
            for v in list(self._nodes.values())[:50]
        )
        edges_summary = "\n".join(
            f"  {e['from']} --[{e['relation']}]--> {e['to']}"
            for e in self._edges[:40]
        )

        prompt = (
            f"Answer this question using the knowledge graph below.\n\n"
            f"Question: {question}\n\n"
            f"NODES:\n{nodes_summary}\n\nRELATIONS:\n{edges_summary}\n\n"
            f"Answer concisely. If the graph doesn't contain enough info, say so."
        )
        answer = self._llm(prompt)
        if not answer:
            return {"success": False, "message": "LLM not available for graph queries."}

        return {"success": True, "message": answer, "data": {"question": question}}

    def find_connections(self, entity: str) -> dict:
        """Find all nodes connected to an entity."""
        key = entity.lower()
        if key not in self._nodes:
            # fuzzy match
            matches = [k for k in self._nodes if entity.lower() in k]
            if not matches:
                return {"success": False, "message": f"Entity '{entity}' not found in graph."}
            key = matches[0]

        node = self._nodes[key]
        connected = [
            e for e in self._edges if e["from"] == key or e["to"] == key
        ]
        neighbor_names = []
        for e in connected:
            other = e["to"] if e["from"] == key else e["from"]
            neighbor_names.append(f"{other} ({e['relation']})")

        msg = f"'{node['name']}' ({node['type']}) — {len(connected)} connections:\n"
        msg += "\n".join(f"  • {n}" for n in neighbor_names[:20]) if neighbor_names else "  No connections found."
        return {"success": True, "message": msg, "data": {"node": node, "connections": connected}}

    def get_stats(self) -> dict:
        """Return graph statistics."""
        types: dict[str, int] = {}
        for n in self._nodes.values():
            t = n.get("type", "unknown")
            types[t] = types.get(t, 0) + 1
        msg = f"Knowledge graph: {len(self._nodes)} nodes, {len(self._edges)} edges.\n"
        msg += "\n".join(f"  {t}: {c}" for t, c in sorted(types.items(), key=lambda x: -x[1]))
        return {"success": True, "message": msg, "data": {"nodes": len(self._nodes), "edges": len(self._edges), "types": types}}

    @staticmethod
    def _word_boundary_match(term: str, text_lower: str) -> bool:
        """True if `term` appears as a whole word in `text_lower`."""
        return bool(re.search(r"\b" + re.escape(term.lower()) + r"\b", text_lower))

    def query_entities(self, text: str, max_nodes: int = 6) -> str:
        """
        Fast entity lookup for RAG context fusion — no LLM needed.
        Uses word-boundary regex to avoid false-positive substring hits.
        Called by brain.py on every user message to inject structured
        relational context alongside the ChromaDB semantic chunks.
        """
        if not self._nodes:
            return ""

        text_lower = text.lower()
        matched: list[str] = []
        matched_set: set[str] = set()

        # Pass 1 — exact whole-word match on node key or full name
        for key, node in self._nodes.items():
            if self._word_boundary_match(key, text_lower) or \
               self._word_boundary_match(node["name"], text_lower):
                matched.append(key)
                matched_set.add(key)

        # Pass 2 — fuzzy: each individual word of the node name (len > 4)
        # applied unconditionally so it doesn't skip when pass 1 already matched
        for key, node in self._nodes.items():
            if key in matched_set:
                continue
            for word in node["name"].lower().split():
                if len(word) > 4 and self._word_boundary_match(word, text_lower):
                    matched.append(key)
                    matched_set.add(key)
                    break

        if not matched:
            return ""

        matched = matched[:max_nodes]
        lines = ["## Knowledge Graph — relevant entities:"]
        for key in matched:
            node = self._nodes[key]
            lines.append(f"\n**{node['name']}** ({node.get('type', 'concept')})")
            srcs = node.get("sources", [])[:2]
            if srcs:
                lines.append(f"  Sources: {', '.join(srcs)}")
            edges = [e for e in self._edges if e["from"] == key or e["to"] == key][:5]
            for e in edges:
                other = e["to"] if e["from"] == key else e["from"]
                other_name = self._nodes.get(other, {}).get("name", other)
                lines.append(f"  → {e['relation']} → {other_name}")

        return "\n".join(lines)

    def clear(self) -> dict:
        self._nodes = {}
        self._edges = []
        self._save()
        return {"success": True, "message": "Knowledge graph cleared.", "data": {}}
