# src/main.py
import os
import argparse
from document_agent import DocumentAgent
from graph_manager import GraphManager
from llm_utils import initialize_llm
from prompts import EXTRACT_PROMPT

def main():
    parser = argparse.ArgumentParser(description="Process PDF reports and update the graph database.")
    parser.add_argument('reports', metavar='R', type=str, nargs='+', help='PDF report files to process')
    args = parser.parse_args()
    
    api_key = os.getenv('OPENAI_API_KEY')
    llm = initialize_llm(api_key)
    
    document_agent = DocumentAgent(llm, EXTRACT_PROMPT)
    graph_manager = GraphManager(uri="bolt://localhost:7687", user="neo4j", password="password")

    for report_path in args.reports:
        report_text = document_agent.read_pdf(report_path)
        nodes, edges = document_agent.extract_nodes_and_edges(report_text)

        document_name = os.path.basename(report_path)
        for node in nodes:
            node['properties']['source'] = document_name

        graph_manager.update_or_insert(nodes, edges)

    graph_manager.close()

if __name__ == "__main__":
    main()
