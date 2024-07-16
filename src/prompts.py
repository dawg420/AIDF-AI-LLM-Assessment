# src/prompts.py
EXTRACT_PROMPT = """
You are given an investment report. Extract the key factors and their causal relationships. 
Please format the output as JSON with two keys: "nodes" and "edges". 

Consider the following node types:
- CauseNode: Represents a factor that causes something to happen.
- ViewNode: Represents an author's view or opinion based on reasoning.
- EffectNode: Represents an outcome or effect of a cause.
- ActionNode: Represents an action taken by the company or external entities.

Nodes should be an array of objects with the following structure:
{{
    "label": "NodeType",  # NodeType should be one of: "CauseNode", "ViewNode", "EffectNode", "ActionNode"
    "properties": {{
        "name": "Node Name"
    }}
}}

Edges should be an array of objects with the following structure:
{{
    "node1": "Node Name",  # Use the "name" property of the node
    "node2": "Node Name",  # Use the "name" property of the node
    "relationship_type": "Relationship Type"  # Relationship Type should be one of: "CAUSE", "MAY_CAUSE", "CONTRIBUTES_TO", "ASSOCIATED_WITH", "TRIGGERS", "INFLUENCES", "SUPPORTS", "DRIVES", "MITIGATES"
}}

Ensure that all edges use the "name" property of the nodes to reference them.

Report:
{document}
"""
