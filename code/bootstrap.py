from GeneticAlgorithm import GeneticAlgorithm

idealString             = "This may be a test string"
populationSize          = 1024
mutationProbability     = 0.15
crossoverProbability    = 0.70
reproductionProbability = 0.05
maximumGenerations      = 10000
ga = GeneticAlgorithm( idealString, populationSize, mutationProbability, crossoverProbability, reproductionProbability )

ga.start( maximumGenerations )
