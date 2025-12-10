from agent.analysis_agent import AnalysisComparisonAgent

agent = AnalysisComparisonAgent()

result = agent.analyze_change(
    old_path="v1_doc1.txt",
    new_path="v2_doc1.txt",
    keyword="capital requirements"
)

print(result)
