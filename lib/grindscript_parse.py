import json
from sys import stderr
from lib.utils import get_dict_value
from lib.exceptions import\
  gs_excepts_failstr,\
  GSP_CouldNotLoadJSON,\
  GSP_JSONParseError
from lib.exit_codes import\
  EXIT_PARSER_FAIL,\
  EXIT_JSON_FAIL

class GrindScript_Parser:
  class GrindScript_Suite:
    class GrindScript_Test:
        def __init__(self, suite_dat: tuple[str, int], data: dict):
          try:
            self.t_name: str = data["name"]
            self.t_desc: str = data["description"]
            self.e_name: str = data["executable"]
            self.e_args: list[str] = data["args"]
          except KeyError as e:
            message = f"Missing mandatory key '{e.args[0]}' in Suite {suite_dat[0]} Test n°{suite_dat[1]}"
            print(gs_excepts_failstr(message), file = stderr)
            exit(EXIT_JSON_FAIL)
          self.e_infile: str | None = get_dict_value(data, "input_file")

    def __init__(self, n: int, data: str):
      try:
        self.s_name: str = data["name"]
        self.s_tests: dict = data["tests"]
        self.s_tests_len = len(self.s_tests)
      except KeyError as e:
        message = f"Missing mandatory key '{e.args[0]}' in Suite n°{n}"
        print(gs_excepts_failstr(message), file = stderr)
        exit(EXIT_JSON_FAIL)
      self.cmpl_tests: list[GrindScript_Parser.GrindScript_Suite.GrindScript_Test] = []

      if (len(self.s_tests) <= 0):
        message = f"No tests in Suite n°{n}"
        print(gs_excepts_failstr(message), file = stderr)
        exit(EXIT_JSON_FAIL)
      for i in range(len(self.s_tests)):
        self.cmpl_tests.append(self.GrindScript_Test((self.s_name, i + 1), self.s_tests[i]))


  def __init__(self, filename: str):
    self.json: object = None
    self.n_suites: int = 0
    self.suites: list[GrindScript_Parser.GrindScript_Suite] = []

    try:
      file = open(filename, "r")
      contents = file.read()
      self.json = json.loads(contents)
    except FileNotFoundError:
      print(GSP_CouldNotLoadJSON(f"Script file does not exist: '{filename}'"), file = stderr)
      exit(EXIT_PARSER_FAIL)

    try:
      for i in range(len(self.json["suites"])):
        self.suites.append(self.GrindScript_Suite(i, self.json["suites"][i], ))
      self.n_suites = len(self.suites)
    except KeyError:
      print(GSP_JSONParseError(f"No suites in script: '{filename}'"), file = stderr)
      exit(EXIT_PARSER_FAIL)
