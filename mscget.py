import urllib

"""
1. get citations from .aux
2. get references from MathSciNet
3. write to mr.bib

also do this for zbMath?
"""
# TODO what is the canonical word for "key"?
# TODO find out the correct format for MR keys
# TODO error detection code...


filename = "test.aux"

# list of known citation commands
commands = ["citation", "abx@aux@cite"]
# path for the API (add key at the end)
path = "http://www.ams.org/msnmain?fn=130&fmt=bibtex&pg1=MR&s1="

# check whether a key refers to a MathSciNet entry
def isMSC(key):
  return key[0:2] == "MR"

def getBibTeX(key):
  assert isMSC(key)

  inCodeBlock = False
  code = ""

  for line in urllib.urlopen(path + key):
    if line.strip() == "</pre>":
      inCodeBlock = False

    if inCodeBlock:
      code = code + line

    if line.strip() == "<pre>":
      inCodeBlock = True

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
    print "\tRetrieving " + key
    g.write(getBibTeX(key))

  g.close()

  print "\nDone!\n"




  # \citation
  # \abx@aux@cite


