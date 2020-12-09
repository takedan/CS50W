def announce(f):
  def wrapper():
    print('about to run the funciont')
    f()
    print('done with the fucniont')
  return wrapper

@announce
def hello():
  print('hello world')

hello()
