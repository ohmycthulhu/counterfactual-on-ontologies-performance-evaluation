import owlready2 as owl
import json
from datetime import datetime
from performance_evaluation_ohmycthulhu.program import Program
from performance_evaluation_ohmycthulhu.output_analyzer import OutputAnalyzerResult
from performance_evaluation_ohmycthulhu.ranking_analyzer import RankingAnalyzer
from performance_evaluation_ohmycthulhu.performance_analyzer import PerformanceAnalyzer
from adapter import CEOAdapter

adapter = CEOAdapter()
analyzers = [
    PerformanceAnalyzer(),
    RankingAnalyzer(),
]

ontology = owl.get_ontology('file://examples/pizza.owl').load()

with open('examples/pizza.json') as file:
    examples = json.load(file)


current_time = datetime.now()
log_file_name = current_time.isoformat().replace(':', '_')


def get_save_progress():
    with open(f'output/{log_file_name}-tmp.log', 'w') as file:
        file.write(f"Program run at {current_time}\n")

    def save_progress(output: list[OutputAnalyzerResult]):
        with open(f'output/{log_file_name}-tmp.log', 'a') as file:
            for analysis in output:
                file.write(str(analysis) + "\n\n\n\n")
                print(analysis, end="\n\n\n\n")

    return save_progress


callbacks = [
    get_save_progress()
]
program = Program(adapter, analyzers, callbacks=callbacks)

results, analysis_results = program.run(examples, ontology)

with open(f"output/{log_file_name}.log", 'w') as file:
    file.write(f"Program run at {current_time}\n")
    for analysis in analysis_results:
        file.write(str(analysis) + "\n\n\n\n")
        print(analysis, end="\n\n\n\n")

print(results)
