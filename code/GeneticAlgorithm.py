import difflib
import random
import string
import sys

from CandidateSolution import CandidateSolution

class GeneticAlgorithm:
    """A simple genetic algorithm supporting mutation and crossover"""

    def __init__( self, idealString, populationSize, mutationProbability, crossoverProbability, reproduceProbability ):
        self.idealString          = idealString
        self.populationSize       = populationSize
        self.chromosomeSize       = len( idealString )
        self.mutationProbability  = mutationProbability
        self.crossoverProbability = crossoverProbability
        self.reproduceProbability = reproduceProbability
        #self.vocabulary           = string.ascii_uppercase + ' '
        self.vocabulary           = string.ascii_letters + ' '

    def start( self, numberOfGenerations ):
        # Start with a new (and random) population
        population = [ CandidateSolution( self.vocabulary, self.chromosomeSize ) for x in range( 0, self.populationSize ) ]

        for n in range( 0, numberOfGenerations ):
            ( currentFitnesses, avgFitness, bestFitness ) = self.evaluatePopulation( population )
            print ''.join( bestFitness[ 1 ].getChromosome() ),
            print "\t # F = %f (avg. %f)" % ( bestFitness[ 0 ], avgFitness ) 
            if bestFitness[ 0 ] == 1.0:
                print "Optimal solution found after %d generations" % n
                sys.exit( 0 )
            population = self.constructNextPopulation( currentFitnesses, population )

    def constructNextPopulation( self, currentFitnesses, currentPopulation ):
        newPopulation = []
        while len( newPopulation ) < self.populationSize:
            candidate = self.selectCandidateBasedOnFitness( currentFitnesses )

            newCandidate = CandidateSolution( self.vocabulary, self.chromosomeSize )
            newCandidate.setChromosome( candidate.getChromosome() )

            if random.random() < self.mutationProbability:
                newCandidate.pointMutation( self.mutationProbability )
                newPopulation.append( newCandidate )
            elif random.random() < self.crossoverProbability:
                # One-point crossover
                #( offspring1, offspring2 ) = self.recombineTwoCandidates_OnePivot( newCandidate, random.choice( currentPopulation ) )
                #newPopulation.append( offspring1 )
                #newPopulation.append( offspring2 )

                # Two-point crossover
                ( offspring1, offspring2, offspring3 ) = self.recombineTwoCandidates_TwoPivots( newCandidate, random.choice( currentPopulation ) )
                newPopulation.append( offspring1 )
                newPopulation.append( offspring2 )
                newPopulation.append( offspring3 )
            elif random.random() < self.reproduceProbability:
                newPopulation.append( candidate )

        return newPopulation

    def evaluatePopulation( self, population ):
        fitnesses = []
        totalFitness = 0.0
        for candidate in population:
            candidateFitness = ( self.computeFitnessForCandidate( candidate ), candidate )
            totalFitness += candidateFitness[ 0 ]
            fitnesses.append( candidateFitness )
        fitnesses.sort()

        averageFitness = totalFitness / len( population )
        bestFitness = ( fitnesses[ -1: ][ 0 ][ 0 ], fitnesses[ -1: ][ 0 ][ 1 ] )
        return ( fitnesses, averageFitness, bestFitness )

    def recombineTwoCandidates_OnePivot( self, candidateOne, candidateTwo ):
        pivotIndex = random.randint( 0, self.chromosomeSize - 1 )

        offspringChromosome1 = candidateOne.getChromosome()[ 0:pivotIndex ]
        offspringChromosome1 += candidateTwo.getChromosome()[ pivotIndex: ]
        offspringChromosome2 = candidateTwo.getChromosome()[ 0:pivotIndex ]
        offspringChromosome2 += candidateOne.getChromosome()[ pivotIndex: ]

        offspring1 = CandidateSolution( self.vocabulary, self.chromosomeSize )
        offspring2 = CandidateSolution( self.vocabulary, self.chromosomeSize )
        offspring1.setChromosome( offspringChromosome1 )
        offspring2.setChromosome( offspringChromosome2 )

        return ( offspring1, offspring2 )

    def recombineTwoCandidates_TwoPivots( self, candidateOne, candidateTwo ):
        firstPivot = 0
        secondPivot = 0

        while abs( secondPivot - firstPivot ) <= 1:
            firstPivot = random.randint( 0, self.chromosomeSize - 1 )
            secondPivot = random.randint( 0, self.chromosomeSize - 1 )

            if firstPivot > secondPivot:
                temp = firstPivot
                firstPivot = secondPivot
                secondPivot = temp

        offspringChromosome1 = candidateTwo.getChromosome()[ 0:firstPivot ]
        offspringChromosome1 += candidateOne.getChromosome()[ firstPivot:secondPivot ]
        offspringChromosome1 += candidateOne.getChromosome()[ secondPivot: ]

        offspringChromosome2 = candidateOne.getChromosome()[ 0:firstPivot ]
        offspringChromosome2 += candidateTwo.getChromosome()[ firstPivot:secondPivot ]
        offspringChromosome2 += candidateOne.getChromosome()[ secondPivot: ]

        offspringChromosome3 = candidateOne.getChromosome()[ 0:firstPivot ]
        offspringChromosome3 += candidateOne.getChromosome()[ firstPivot:secondPivot ]
        offspringChromosome3 += candidateTwo.getChromosome()[ secondPivot: ]
        
        offspring1 = CandidateSolution( self.vocabulary, self.chromosomeSize, offspringChromosome1 )
        offspring2 = CandidateSolution( self.vocabulary, self.chromosomeSize, offspringChromosome2 )
        offspring3 = CandidateSolution( self.vocabulary, self.chromosomeSize, offspringChromosome3 )

        return ( offspring1, offspring2, offspring3 )
        
    def computeFitnessForCandidate( self, candidate ):
        chromosome = candidate.getChromosome()
        matches = 0
        for n in range( 0, len( chromosome ) ):
            if chromosome[ n ] == self.idealString[ n ]:
                matches += 1

        return float( matches ) / len( chromosome )
            
    def selectCandidateBasedOnFitness( self, fitnesses ):
        fitnessTotal = sum( pair[0] for pair in fitnesses )
        n = random.uniform( 0, fitnessTotal )
        for ndx in range( 1, len( fitnesses ) ):
            if n < fitnesses[ ndx ][ 0 ]:
                return fitnesses[ ndx ][ 1 ]
            else:
                n = n - fitnesses[ ndx ][ 0 ]
        
        # Fail-safe in case we fail to select a candidate
        randomCandidateIndex = random.randint( 0, len( fitnesses ) - 1 )
        return fitnesses[ randomCandidateIndex ][ 1 ]
