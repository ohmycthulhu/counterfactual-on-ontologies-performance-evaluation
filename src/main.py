from ceo.adapter import CEOAdapter
from program import Program
from output_analyzers.ranking_analyzer import RankingAnalyzer
from datetime import datetime

adapter = CEOAdapter()
analyzers = RankingAnalyzer()

program = Program(adapter, [analyzers])
results, analysis_results = program.run('examples/pizza.json')

current_time = datetime.now()
log_file_name = current_time.isoformat().replace(':', '_')

with open(f"output/{log_file_name}.log", 'w') as file:
    file.write(f"Program run at {current_time}\n")
    for analysis in analysis_results:
        file.write(str(analysis) + "\n")
        print(analysis)

print(results)
