import urllib

"""
Ideas:

  * zbMath

To be implemented:

  * more error handling

"""

filename = "test.aux"

# list of known citation commands
commands = ["citation", "abx@aux@cite"]
# path for the API (add key at the end)
path = "http://www.ams.org/msnmain?fn=130&fmt=bibtex&pg1=MR&s1="

# check whether a key refers to a MathSciNet entry
def isMSC(key):
  return key[0:2] == "MR" and key[2:].isdigit()


class KeyNotFoundException(Exception):
  def __init__(self, key):
    self.key = key
  
  def __str__(self):
    return key + " was not found"


def getBibTeX(key):
  assert isMSC(key)

  inCodeBlock = False
  code = ""

  for line in urllib.urlopen(path + key):
    if "No publications results for" in line:
      raise KeyNotFoundException(key)


    if line.strip() == "</pre>": inCodeBlock = False

    if inCodeBlock:
      code = code + line

    if line.strip() == "<pre>": inCodeBlock = True

  return code


with open(filename) as f:
  keys = []

  for line in f:
    command = line[1:].split("{")[0]
    if command in commands:
      key = line.split("{")[1].split("}")[0]

      if isMSC(key):
        keys.append(key)

  keys = sorted(set(keys))
  print "Found " + str(len(keys)) + " keys:"
  print "\t", keys, "\n"

  print "Downloading the BibTeX code\n"

  g = open("mr.bib", "w")
  for key in keys:
    print "\tRetrieving " + key + "...",

    try:
      g.write(getBibTeX(key))
    except KeyNotFoundException as e:
      print "Not found!"
    else:
      print "Done!"

  g.close()

  print "\nDone!\n"




  # \citation
  # \abx@aux@cite


