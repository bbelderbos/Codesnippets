import sys
MAX_LEN = 15

def file2list(fname):
  with open(fname) as f:
    lines = [li.strip() for li in f.readlines()]
  return lines 

def line_is_comment(li):
  if li.startswith("#"):
    return True
  return False

def get_method_name(li):
  return li.split("(")[0].replace("def ", "")

def count_method_len(lines):
  methods = {}
  method_name = None
  for li in lines:
    if not li.strip():
      method_name = None
    elif line_is_comment(li):
      continue
    elif li.startswith("def "):
      method_name = get_method_name(li)
      methods[method_name] = 0
    else:
      if method_name in methods:
        methods[method_name] += 1 
  return methods

def print_line(method, score):
  if score <= MAX_LEN:
    print "v) ",
  else:
    print "x) ",
  print "%-25s | %d" % (method, score)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    sys.exit("Provide input file please")
  fname = sys.argv[1]
  lines = file2list(fname)
  methods = count_method_len(lines)
  for method, count in methods.items():
    print_line(method, count)
