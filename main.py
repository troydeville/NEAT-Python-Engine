from Engine import Engine
import re

# This project was created for processing a NEAT model on the Raspberry Pi.
# To create a model, use the "NEAT-swift" implementation on github:
#             "https://github.com/troydeville/NEAT-swift"
# Simply load a configuration file, which is generated
#   by printing the Genome's description, and run inputs.

confURL = "model.txt"

engine = Engine(confURL)

# Run engine's expected input
output1 = engine.run([0.0, 0.0])
output2 = engine.run([0.0, 1.0])
output3 = engine.run([1.0, 0.0])
output4 = engine.run([1.0, 1.0])

# Get output
print(output1)
print(output2)
print(output3)
print(output4)
