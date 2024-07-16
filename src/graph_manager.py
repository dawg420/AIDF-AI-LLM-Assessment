# src/graph_manager.py
import re
from neo4j import GraphDatabase

class GraphManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def node_exists(self, name, source):
        with self.driver.session() as session:
            result = session.run("MATCH (n {name: $name, source: $source}) RETURN n", name=name, source=source)
            return result.single() is not None

    def update_or_insert(self, nodes, edges):
        with self.driver.session() as session:
            for node in nodes:
                if not self.node_exists(node['properties']['name'], node['properties']['source']):
                    session.write_transaction(self._create_node, node['label'], node['properties'])
            for edge in edges:
                session.write_transaction(self._create_edge, edge['node1'], edge['node2'], edge['relationship_type'])

    @staticmethod
    def _create_node(tx, label, properties):
        query = f"CREATE (n:{label} {{name: $name, source: $source}})"
        tx.run(query, name=properties['name'], source=properties['source'])

    @staticmethod
    def _create_edge(tx, node1_name, node2_name, relationship_type):
        formatted_relationship_type = re.sub(r'[^A-Z]', '_', relationship_type.upper())
        query = (
            f"MATCH (a {{name: $node1_name}}), (b {{name: $node2_name}}) "
            f"MERGE (a)-[r:{formatted_relationship_type}]->(b)"
        )
        tx.run(query, node1_name=node1_name, node2_name=node2_name)

    def delete_all_nodes(self):
        with self.driver.session() as session:
            session.write_transaction(self._delete_all_nodes)

    @staticmethod
    def _delete_all_nodes(tx):
        query = "MATCH (n) DETACH DELETE n"
        tx.run(query)