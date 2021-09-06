import pyautogui as pg
import keyboard as kb
import cv2
import configparser as cp
from time import sleep
import enlighten
import sys

print("Good luck")

def captureCursorPos(item):
  countdown = 3
  print("Hover Mouse Over The", item, "Slot")
  while countdown > 0:
    print("Capturing Mouse Position in", countdown, "seconds")
    sleep(1)
    countdown -= 1
  return pg.position()

pg.FAILSAFE = True

click = False
click_only = False
click_only_pbar = None

goldenCookies = False

new_game = input("New Game? (y/n)") == "y"
print("New Game: ", new_game)

main_img = cv2.imread("./images/main_cookie.png", cv2.IMREAD_UNCHANGED)
golden_img = cv2.imread("./images/golden_cookie.png", cv2.IMREAD_UNCHANGED)

config = cp.ConfigParser(allow_no_value=True)
config.read("./config.ini")

calibrate = config.getboolean("calibrate", "need")
print("Calibrate", calibrate)

if calibrate:
  print("Calibration Required")

main_cookie_pos = eval(config["calibrate"]["main_cookie_pos"])
if calibrate:
  main_cookie_pos = None
  main_cookie_input = input("Hover Mouse over Main Cookie and Press Any Key or Press Enter to auto-find: ")
  if main_cookie_input == "":
    try:
      print("Looking for Main Cookie")
      main_cookie_pos = pg.locateCenterOnScreen("./images/main_cookie.png")
    except:
      print("Could not find Main Cookie")

  if main_cookie_pos is None:
    main_cookie_pos = captureCursorPos("Main Cookie")

  config["calibrate"]["main_cookie_pos"] = str([main_cookie_pos[0], main_cookie_pos[1]])
print("Main Cookie Pos", main_cookie_pos)

config_delay = config.getint("calibrate", "buy_delay")
if not new_game:
  if calibrate:
    config_delay = input("Enter buy delay (press Enter for default): ")
    if config_delay and config_delay.isdigit() and int(config_delay) > 0:
      config_delay = int(config_delay)
      config["calibrate"]["buy_delay"] = str(config_delay)
    else:
      if config_delay == "":
        print("Using default buy delay")
      else:
        print("Invalid input; defaulting Buy Delay")
      config_delay = 100

add_delay = config.getboolean("calibrate", "add_delay")
delay_amount = 1

buy_delay = config_delay if not new_game else 15
current_delay = 0

click_speed = config.getfloat("calibrate", "click_speed")
if calibrate:
  click_speed = input("Enter a Click Speed (press Enter for default): ")
  if click_speed and click_speed.isdigit() and float(click_speed) > 0:
    click_speed = float(click_speed)
    config["calibrate"]["click_speed"] = str(click_speed)
  else:
    if click_speed == "":
      print("Using default click speed")
    else:
      print("Invalid input; defaulting Click Speed")
    click_speed = 0.015
pg.PAUSE = click_speed

buy_upgrades = config.getboolean("upgrades", "buy_upgrades")
if calibrate:
  buy_upgrades = input("Buy Upgrades? (y/n)") == "y"
  print("Buy Upgrades: ", buy_upgrades)
  config["upgrades"]["buy_upgrades"] = str(buy_upgrades)

buy_upgrades_pos = None

if buy_upgrades:
  if calibrate:
    buy_upgrades_pos = captureCursorPos("Upgrade")
    config["upgrades"]["buy_upgrades_pos"] = str([buy_upgrades_pos[0], buy_upgrades_pos[1]])
  else:
    buy_upgrades_pos = eval(config["upgrades"]["buy_upgrades_pos"])
  print("Upgrade Position", buy_upgrades_pos)

buy_buildings = config.getboolean("buildings", "buy_buildings")
if calibrate:
  buy_buildings = input("Buy Buildings? (y/n)") == "y"
  print("Buy Buildings: ", buy_buildings)
  config["buildings"]["buy_buildings"] = str(buy_buildings)

buy_buildings_pos = []
buildings = [
  "antimatter_condensers",
  "time_machines",
  "portals",
  "alchemy_labs",
  "shipments",
  "wizard_towers",
  "temples",
  "banks",
  "factories",
  "mines",
  "farms",
  "grandmas",
  "cursors",
]

def calibrateBuildings(building):
  if config.getboolean("buildings", "buy_" + building):
    buy_buildings_pos.append(captureCursorPos(building))
    print(building, "Position", buy_buildings_pos[-1])
    config["buildings"]["buy_" + building + "_pos"] = str([buy_buildings_pos[-1][0], buy_buildings_pos[-1][1]])

def getBuildingPos(building):
  if config.getboolean("buildings", "buy_" + building):
    buy_buildings_pos.append(eval(config["buildings"]["buy_" + building + "_pos"]))
    print(building, "Position", buy_buildings_pos[-1])

if buy_buildings:
  if calibrate:
    for building in buildings:
      calibrateBuildings(building)
  else:
    for building in buildings:
      getBuildingPos(building)

if calibrate:
  print("Calibration Complete")
  config["calibrate"]["need"] = "False"
  with open("./config.ini", "w") as configfile:
    config.write(configfile)

def moveMouseToMainCookie():
  pg.moveTo(main_cookie_pos[0], main_cookie_pos[1])

track_clicks = buy_upgrades and buy_buildings
pbar = enlighten.Counter(total=buy_delay, desc='Clicks', unit='clicks')

last_keydown = None

print("Cookie Clicker AC v0.2")
while True:
  if kb.is_pressed("k"):
    print("Kill Program")
    break

  if kb.is_pressed("s") and last_keydown != "s":
    last_keydown = "s"
    print("Pause Clicking")
    click = False
    click_only = False

  if kb.is_pressed("a") and last_keydown != "a":
    last_keydown = "a"
    print("Start Clicking")
    moveMouseToMainCookie()
    click = True
    click_only = False

  if kb.is_pressed("g") and last_keydown != "g":
    last_keydown = "g"
    print("Hunting Golden Cookies")
    goldenCookies = True

  if kb.is_pressed("h") and last_keydown != "h":
    last_keydown = "h"
    print("Pause Hunting Golden Cookies")
    goldenCookies = False

  if kb.is_pressed("c") and last_keydown != "c":
    last_keydown = "c"
    print("Auto Click Only Mode")
    moveMouseToMainCookie()
    click_only_pbar = enlighten.Counter(total=sys.maxsize, desc='Clicks', unit='clicks')
    click_only = True
    click = False

  if kb.is_pressed("x") and last_keydown != "x":
    last_keydown = "x"
    print("Exit Auto Click Only Mode")
    click_only = False
    click = False
    click_only_pbar = None

  if goldenCookies:
    result = pg.locateCenterOnScreen(golden_img, confidence=0.6)
    if result is not None:
      print("Found Golden Cookie", result)
      pg.moveTo(result[0], result[1])
      pg.click()

  if click_only:
    pg.click()
    click_only_pbar.update()

  if click:
    if goldenCookies:
      moveMouseToMainCookie()
    pg.click()
    if track_clicks:
      current_delay += 1
      pbar.update()

      if current_delay >= buy_delay:
        if buy_upgrades:
          pg.moveTo(buy_upgrades_pos[0], buy_upgrades_pos[1])
          pg.click()
          moveMouseToMainCookie()

        if buy_buildings:
          for pos in buy_buildings_pos:
            pg.moveTo(pos[0], pos[1])
            pg.click()
          moveMouseToMainCookie()

        current_delay = 0
        if add_delay and buy_delay < sys.maxsize:
          if buy_delay > (delay_amount * delay_amount):
            delay_amount = delay_amount * 10
          buy_delay += delay_amount
          if buy_delay > sys.maxsize:
            buy_delay = sys.maxsize

        pbar = enlighten.Counter(total=buy_delay, desc='Clicks', unit='clicks')
