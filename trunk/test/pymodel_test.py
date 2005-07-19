import os

from Modeling.PyModel import *

Entity.defaults['properties']= [
  APrimaryKey ('id', isClassProperty=1, isRequired=1, doc='Primary key!')
]

_connDict= {
    'database': 'deleteme.db',
}

model= Model ('Tester', adaptorName='SQLite', connDict=_connDict)
model.version='0.1'

model.entities= [
    Entity ('aProduct',
            properties= [
                AString ('code', width=20),
                AString ('name', width=80),
            ],
    ),
    Entity ('aStock',
            properties= [
                AInteger ('level'),
            ],
    ),
]

model.associations = [ Association('aStock', 'aProduct',
                                   relations=['product', 'stocks']),
                       ]

