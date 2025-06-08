import neat
from blackjack.game import Blackjack
from blackjack.player import NEATPlayer

#quick fix from ChatGPT
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        score = 0
        for _ in range(100):  # number of games per genome
            game = Blackjack()
            neat_player = NEATPlayer(net=net)
            game.add_player(neat_player)
            game.playRound()
            score += neat_player.get_fitness()
        genome.fitness = score

def run_neat():
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward.txt')
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)
    return winner

run_neat()