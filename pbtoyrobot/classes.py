""" This module contain all the classes used by the pbroyrobot CLI. """
from abc import ABC, abstractmethod
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

class RobotWorld(ABC):
  """ 
  This is an abstract class defining our toy robot's world.
  
  It can be modified in the future, for instance, to define 
  a three dimensional space, or a two dimensional surface in 
  space.
  """
  @abstractmethod
  def is_within_boundaries(self):
    """ 
    Abstract method.

    Checks is given coordinates are within boundaries. """
    pass

  @abstractmethod
  def next_position(self):
    """ 
    Abstract method.

    Returns the next position, depending on boundaries and 
    other constraints. 
    """
    pass

class TableTop(RobotWorld):
  """ This class defines a rectangular table top. """
  def __init__(self, width, length):
    self.__width = width
    self.__length = length
  
  # PROPERTIES
  #
  @property
  def width(self):
    """ Width property. """
    return self.__width

  @width.setter
  def width(self, value):
    """ Sets the width property to a given value. """
    if value <= 0:
      raise ValueError("Width cannot be negative or zero.")
    self.__width = value

  @property
  def length(self):
    """ Length property. """ 
    return self.__length

  @length.setter
  def length(self, value):
    """ Sets the length property to a given value. """
    if value <= 0:
      raise ValueError("Length cannot be negative or zero.")
    self.__length = value

  # METHODS
  #
  def is_within_boundaries(self, x, y):
    """ 
    Checks if the given coordinates are within boundaries. 
    
    Parameters:
      x (int): x coordinate.
      y (int): y coordinate.

    Returns:
      True if the given coordinates are within boundaries.
    """
    return (0 <= x <= self.width and 0 <= y <= self.length)

  def next_position(self, x, y, direction_angle, step = 1):
    """ 
    Returns the next position depending on the current direction and coordinates. 
    
    Movements are multiples of step.
    """
    if direction_angle == 0:
      new_x = x + step
    elif direction_angle == 180:
      new_x = x - step
    else:
      new_x = x
    
    if direction_angle == 90:
      new_y = y + step
    elif direction_angle == 270:
      new_y = y - step
    else:
      new_y = y

    if not self.is_within_boundaries(new_x, new_y):
      return (x, y)
    else:
      return (new_x, new_y)

class Robot:
  """ This class defines our robot """
  def __init__(self, config_file):
    # Read config file to load inital position
    #
    path = Path(config_file)
    if path.exists():
      try:
        with open(config_file) as f:
          self.__config = yaml.load(f, Loader = SafeLoader)
          self.__config_file = config_file
      except:
        return print("Config file missing")
    else:
      try:
        import importlib.resources as pkg_resources
      except ImportError:
        # Try backported to PY<37 `importlib_resources`.
        import importlib_resources as pkg_resources
      try:
        with pkg_resources.open_text(__package__, path.name) as f:
          self.__config = yaml.load(f, Loader = SafeLoader)
          self.__config_file = path.name
      except:
        return print("Config file missing")
    
    self.__x = self.__config["X"]
    self.__y = self.__config["Y"]
    self.__facing = self.__config["F"]
    self.__place_command_executed = self.__config["PlaceCommandExecuted"]
    self.__parameter_separator = self.__config["ParameterSeparator"]
    self.__directions = {
      "0": "EAST", 
      "90": "NORTH", 
      "180": "WEST", 
      "270": "SOUTH"
    }
    self.__directions_inv = {v : k for k, v in self.__directions.items()}
    self.__angle = int(self.__directions_inv[self.__facing])
    self.__world = TableTop(5, 5)

  # METHODS
  #
  def __get_cardinal_directions(self):
    return list(self.__directions.values())

  def __get_angles(self):
    return list(self.__directions.keys())

  def __get_cardinal_direction(self, angle):
    return self.__directions[str(angle)]

  def __is_first_command_executed(self):
    return self.__place_command_executed

  def __set_first_command_executed(self):
    self.__place_command_executed = True

  def __save_config(self, X, Y, F):
    config = {
      "X": X,
      "Y": Y,
      "F": F,
      "ParameterSeparator": self.__parameter_separator,
      "PlaceCommandExecuted": self.__is_first_command_executed()
    }
    path = Path(self.__config_file)
    if path.exists():
      try:
        with open(path, "w") as f:
          yaml.dump(config, f, sort_keys=False, default_flow_style=False)
      except:
        return print("Config file missing")
    else:
      try:
        import importlib.resources as pkg_resources
      except ImportError:
        # Try backported to PY<37 `importlib_resources`.
        import importlib_resources as pkg_resources
      try:
        with pkg_resources.path(__package__, self.__config_file) as path:
          with open(path, "w") as f:
            yaml.dump(config, f, sort_keys=False, default_flow_style=False)
      except:
        return print("Config file missing")

  def move(self, args):
    """ Moves the robot by step units in the current direction. Default step value is 1. """
    if not self.__is_first_command_executed():
      # Error
      return print("The first command must be a PLACE X,Y,F")

    angle = int(self.__directions_inv[self.__facing])
    (new_x, new_y) = self.__world.next_position(self.__x, self.__y, angle)

    if new_x != self.__x or new_y != self.__y:
      self.__x = new_x
      self.__y = new_y
      self.__save_config(X = new_x, Y = new_y, F = self.__facing)

  def place(self, args):
    """ 
    Places the robot at the given coordinates, with the given direction.
    
    Parameters:
      args (list): list of arguments. This list should include coordinates and direction.
    """
    #
    # Parse arguments
    arg_len = len(args)
    new_coordinates = []
    if arg_len != 2:
      # Error
      return print("Wrong command arguments")
    command_arguments = args[1].split(self.__parameter_separator)
    if len(command_arguments) != 3:
      # Error
      return print("Wrong command arguments")
    for i in range(2):
      try:
        new_coordinates.append(int(command_arguments[i]))
      except:
        # Error
        return print("The first two arguments must be integers")
    if not command_arguments[2].upper() in self.__get_cardinal_directions():
      # Error
      return print("Valid directions are NORTH, SOUTH, EAST and WEST")
    
    if self.__world.is_within_boundaries(new_coordinates[0], new_coordinates[1]):
      self.__x = new_coordinates[0]
      self.__y = new_coordinates[1]
      self.__set_first_command_executed()
      self.__save_config(X = self.__x, Y = self.__y, F = command_arguments[2].upper())

  def rotate_left(self, args):
    """ Rotates the robot to the left. """
    if not self.__is_first_command_executed():
      # Error
      return print("The first command must be a PLACE X,Y,F")
    self.__angle = (self.__angle + 90) % 360
    self.__facing = self.__get_cardinal_direction(self.__angle)
    self.__save_config(X = self.__x, Y = self.__y, F = self.__facing)

  def rotate_right(self, args):
    """ Rotates the robot to the right. """
    if not self.__is_first_command_executed():
      # Error
      return print("The first command must be a PLACE X,Y,F")
    self.__angle = (self.__angle - 90) % 360
    self.__facing = self.__get_cardinal_direction(self.__angle)
    self.__save_config(X = self.__x, Y = self.__y, F = self.__facing)

  def report(self, args):
    """ Print the current coordinates and direction of the robot. """
    if not self.__is_first_command_executed():
      # Error
      return print("The first command must be a PLACE X,Y,F")
    print(f"{self.__x},{self.__y},{self.__facing}")

  # ATTRIBUTES
  #
  commands = {
    "MOVE" : move,
    "PLACE": place,
    "LEFT": rotate_left,
    "RIGHT": rotate_right,
    "REPORT": report
  }

  def execute(self, args):
    """ Executes a CLI command. """
    if len(args) > 0:
      command = args[0].upper()
      if command in self.commands:
        self.commands[command](self, args)
    else:
      print("No commands specified")
