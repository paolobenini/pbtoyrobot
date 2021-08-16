from classes import Robot

def execute_command(command):
  args = command.split()    
  r = Robot(config_file = "config.yaml")
  print(args)
  r.execute(args)

def test1():
#
# The first command must be a PLACE
# Any other commands must be rejected
#
  execute_command("REPORT")
  print("----")

  execute_command("MOVE")
  print("----")

  execute_command("LEFT")
  print("----")

  execute_command("RIGHT")
  print("----")

def test2():
#
# Test PLACE and boundaries
#

# Valid inputs
  execute_command("PLACE 1,1,NORTH")
  execute_command("REPORT")
  print("----")

  execute_command("PLACE 0,5,NORTH")
  execute_command("REPORT")
  print("----")

  execute_command("PLACE 5,0,NORTH")
  execute_command("REPORT")
  print("----")

  execute_command("PLACE 5,5,NORTH")
  execute_command("REPORT")
  print("----")

  execute_command("PLACE 0,0,NORTH")
  execute_command("REPORT")
  print("----")

# Invalid inputs
  execute_command("PLACE 1,6,NORTH")
  execute_command("REPORT")
  print("----")

  execute_command("PLACE -1,0,NORTH")
  execute_command("REPORT")
  print("----")

  execute_command("PLACE 1,-2,NORTH")
  execute_command("REPORT")
  print("----")

  execute_command("PLACE 6,1,NORTH")
  execute_command("REPORT")
  print("----")

  execute_command("PLACE 0.5,3,NORTH")
  execute_command("REPORT")
  print("----")

  execute_command("PLACE 3,0.5,NORTH")
  execute_command("REPORT")
  print("----")

def test3():
#
# Test MOVE and boundaries
#   
  execute_command("PLACE 2,2,NORTH")
  execute_command("REPORT")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("REPORT")
  execute_command("MOVE")
  execute_command("REPORT")
  print("----")

  execute_command("RIGHT")
  execute_command("RIGHT")
  execute_command("REPORT")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("REPORT")
  execute_command("MOVE")
  execute_command("REPORT")
  print("----")

  execute_command("LEFT")
  execute_command("REPORT")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("REPORT")
  execute_command("MOVE")
  execute_command("REPORT")
  print("----")

  execute_command("RIGHT")
  execute_command("RIGHT")
  execute_command("REPORT")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("MOVE")
  execute_command("REPORT")
  execute_command("MOVE")
  execute_command("REPORT")
  print("----")


def test4():
#
# Test LEFT
#   
  execute_command("REPORT")
  execute_command("LEFT")
  execute_command("REPORT")
  execute_command("LEFT")
  execute_command("REPORT")
  execute_command("LEFT")
  execute_command("REPORT")
  execute_command("LEFT")
  execute_command("REPORT")

def test5():
#
# Test RIGHT
#   
  execute_command("REPORT")
  execute_command("RIGHT")
  execute_command("REPORT")
  execute_command("RIGHT")
  execute_command("REPORT")
  execute_command("RIGHT")
  execute_command("REPORT")
  execute_command("RIGHT")
  execute_command("REPORT")

def test6():
#
# Test upper/lower case
#
  execute_command("place 2,3,north")
  execute_command("Report")
  execute_command("Right")
  execute_command("report")
  execute_command("left")
  execute_command("report")
  execute_command("move")
  execute_command("report")
  execute_command("Move")
  execute_command("REPORT")

def test7():
#
# Test command syntax
#
  execute_command("PLACE 2 3 NORTH")
  execute_command("PLACE 2;3;NORTH")
  execute_command("PLACE 2,3 NORTH")
  execute_command("PLACE 2, 3, NORTH")
  execute_command("")

test7()