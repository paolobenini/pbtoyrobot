## PBTOYROBOT: Toy Robot CLI

A CLI to control a toy robot.

Installation
------------

Install using pip:

    pip install pbtoyrobot


CLI
---

- The application is a simulation of a toy robot moving on a square tabletop, of dimensions 5 units x 5 units.
- There are no other obstructions on the table surface.
- The robot is free to roam around the surface of the table, but must be prevented from falling to destruction. Any movement
  that would result in the robot falling from the table must be prevented, however further valid movement commands must still
  be allowed.
  
```plain
    # Show help
    pbtoyrobot --help

    # PLACE: Places the robot at X, Y with orientation F
    # Possible value for x and y are integers between 0 and 5 included
    # Possible values for F are NORTH, EAST, SOUTH and WEST
    pbtoyrobot PLACE 1,1,NORTH

    # MOVE: Moves the robot of one unit in the current direction
    pbtoyrobot MOVE
    
    # LEFT: Rotates the robot 90 degrees in the specified direction
    pbtoyrobot LEFT

    # RIGHT: Rotates the robot 90 degrees in the specified direction
    pbtoyrobot RIGHT

    # REPORT: will announce the X,Y and orientation of the robot
    pbtoyrobot REPORT
```

Usage
-----

Example Input and Output:

```plain
PLACE 0,0,NORTH
MOVE
REPORT
Output: 0,1,NORTH
```

```plain
PLACE 0,0,NORTH
LEFT
REPORT
Output: 0,0,WEST
```

```plain
PLACE 1,2,EAST
MOVE
MOVE
LEFT
MOVE
REPORT
Output: 3,3,NORTH
```
