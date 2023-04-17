from ceo.adapter import CEOAdapter
from program import Program
from output_analyzers.ranking_analyzer import RankingAnalyzer

adapter = CEOAdapter()
analyzers = RankingAnalyzer()

program = Program(adapter, [analyzers])
results, analysis = program.run('examples/pizza.json')

print(results)
