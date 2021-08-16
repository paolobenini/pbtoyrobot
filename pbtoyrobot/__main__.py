import sys
from .classes import Robot

robot = Robot(config_file = "pbtoyrobot/config.yaml")

def main():
    args = sys.argv[1:]
    robot.execute(args)

if __name__ == '__main__':
    main()
