import configparser

from Utils import Utils

class Rankings:
    def __init__(self):
        self.rankings = {}

        self.properties()
        self.populate()

    def properties(self):
        path = Utils.join('properties', 'rankings.properties')

        self.properties = configparser.ConfigParser()
        self.properties.read(path)

    def get_rankings(self):
        return self.rankings

    def populate(self):
        return
#        for key in self.properties['users']:
#            coordinates = (self.properties['users'][key]).split(',')
#            self.add(key, coordinates[0], coordinates[1], coordinates[2])

    def add(self, rank, id, name, power, kp, deaths, t4, t5):
        self.set(rank, id, name, power, kp, deaths, t4, t5)
    
    def contains(self, id):
        if id in self.rankings:
            return True
        else:
            return False

    def get_id(self, id):
        if not self.contains(id):
            return None

        user = {
            'rank' : self.rankings[id]['rank'],
            'id' : id,
            'name' : self.rankings[id]['name'],
            'power' : self.rankings[id]['power'],
            'kp' : self.rankings[id]['kp'],
            'deaths' : self.rankings[id]['deaths'],
            't4' : self.rankings[id]['t4'],
            't5' : self.rankings[id]['t5']             
        }

        return user

    def get_rank(self, rank):
        for id in self.rankings:
            _rank = self.rankings[id]['rank']

            user = {
               'id' : id,
               'name' : self.rankings[id]['name'],
               'power' : self.rankings[id]['power'],
               'kp' : self.rankings[id]['kp'],
               'deaths' : self.rankings[id]['deaths'],
               't4' : self.rankings[id]['t4'],
               't5' : self.rankings[id]['t5']             
            }

            if _rank == rank:
                return user

        return None

    def set(self, rank, id, name, power, kp, deaths, t4, t5):
#        user = {
#            'rank' : rank,
#            'id' : id,
#            'name' : name,
#            'power' : power,
#            'kp' : kp,
#            'deaths' : deaths,
#            't4' : t4,
#            't5' : t5
#        }

        user = {
            'rank' : rank,
            'id' : id,
            'name' : name,
            'power' : f'{int(power):,}',
            'kp' : f'{int(kp):,}',
            'deaths' : f'{int(deaths):,}',
            't4' : f'{int(t4):,}',
            't5' : f'{int(t5):,}'
        }

        self.rankings[id] = user