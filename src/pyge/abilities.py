#abilities script en lieu of db



from character import Skill
from charcater import Action



#Slash, basic attack, no prerequisite, no use requirements
slash = Skill( 'name' : 'slash',
               'level': 1,
               'threshold': 2,
               'damagetype': 'cut',
               'effect': Action.actype['attack'] )
thrust = Skill( 'name' : 'thrust',
                'level': 1,
                'threshold': 2,
                'damagetype': 'pierce',
                'effect': Action.actype['attack'] )

