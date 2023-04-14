from ceo.adapter import CEOAdapter
from program import Program

adapter = CEOAdapter()
program = Program(adapter)
results = program.run('examples/pizza.json')

print(results)
