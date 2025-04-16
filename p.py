from tools import debug_new

# log = log_obj("tmp.log")

debug = debug_new(
  'none',
  # 'all',
  # 'log',
  )

if debug.flag('log'):
    print("log")

if debug.flag('hello'):
    print("hello")

if debug.flag():
    print("default")
