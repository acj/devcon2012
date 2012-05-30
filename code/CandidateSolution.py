import random
import string

class CandidateSolution:
    """A representation of one solution"""

    def __init__( self, vocabulary, chromosomeLength, chromosome=None ):
        self.vocabulary = vocabulary
        if chromosome == None:
            self.chromosome = [ random.choice( self.vocabulary ) for n in range( 0, chromosomeLength ) ]
        else:
            self.chromosome = chromosome

    def pointMutation( self, mutationProbability ):
        geneIndex = random.randint( 0, len( self.chromosome ) ) - 1
        self.chromosome[ geneIndex ] = random.choice( self.vocabulary )

    def getChromosome( self ):
        return self.chromosome

    def setChromosome( self, chromosome ):
        self.chromosome = list( chromosome )
