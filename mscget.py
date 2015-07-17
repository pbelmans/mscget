import requests

"""
Ideas:

  * zbMath

"""

filename = "test.aux"

# list of known citation commands
commands = ["citation", "abx@aux@cite"]
# path for the API
path = "http://www.ams.org/msnmain"

# check whether a key refers to a MathSciNet entry
def isMSC(key):
  return key[0:2] == "MR" and key[2:].isdigit()

# check whether we are authenticated by making an empty request
def isAuthenticated():
  # make the request
  payload = {"fn": 130}
  r = requests.get(path, params=payload)

  if r.status_code == 200:
    return True
  elif r.status_code == 401:
    return False
  else:
    raise Exception("Received HTTP status code " + str(r.status_code))


class KeyNotFoundException(Exception):
  def __init__(self, key):
    self.key = key
  
  def __str__(self):
    return key + " was not found"

class AuthenticationException(Exception):
  def __str__(self):
    return "Not authenticated"


# obtain the BibTeX code for `key`
def getBibTeX(key):
  assert isMSC(key)

  # reconstructing the BibTeX code block
  inCodeBlock = False
  code = ""

  # make the request
  payload = {"fn": 130, "fmt": "bibtex", "pg1": "MR", "s1": key}
  r = requests.get(path, params=payload)

  # 401 means not authenticated
  if r.status_code == 401:
    raise AuthenticationException()

  # anything but 200 means something else went wrong
  if not r.status_code == 200:
    raise Exception("Received HTTP status code " + str(r.status_code))

  for line in r.text.split("\n"):
    if "No publications results for" in line:
      raise KeyNotFoundException(key)


    if line.strip() == "</pre>": inCodeBlock = False

    if inCodeBlock:
      code = code + line

    if line.strip() == "<pre>": inCodeBlock = True

  return code


with open(filename) as f:
  keys = []

  # read the .aux file and look for citation commands
  for line in f:
    # the main assumption here is that the .aux file always contains things of the form \citation{key}, where `citation` can differ
    command = line[1:].split("{")[0]
    if command in commands:
      key = line.split("{")[1].split("}")[0]

      if isMSC(key):
        keys.append(key)

  # discard multiples and sort
  keys = sorted(set(keys))

  print "Found " + str(len(keys)) + " keys in " + filename + ":"
  print "\t", keys, "\n"

  # test whether we are authenticated
  if not isAuthenticated():
    print "Not authenticated. Please check whether you are on a connection which allows using MathSciNet."
  else:
    # we can go ahead
    print "Downloading the BibTeX code\n"

    g = open("mr.bib", "w")
    for key in keys:
      print "\tRetrieving " + key + "...",

      try:
        g.write(getBibTeX(key))
      except KeyNotFoundException:
        print "Not found"
      except AuthenticationException as e:
        print "Not authenticated anymore."

      else:
        print "Done."

    g.close()

  print "\nDone.\n"
