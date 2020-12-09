people = [
  {'name': 'harry', 'house':'g'},
  {'name': 'cho','house':'s'},
  {'name': 'draco', 'house':'r'}
]

def f(person):
  return person['house']

people.sort(key=f)

print(people)

people.sort(key=lambda person: person['name'])

print(people)
