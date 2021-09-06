import pyautogui as pg
import keyboard as kb
import cv2
import configparser as cp
from time import sleep
import enlighten

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

goldenCookies = False

main_img = cv2.imread("./images/main_cookie.png", cv2.IMREAD_UNCHANGED)
print("Looking for Main Cookie")
main_cookie_pos = pg.locateCenterOnScreen("./images/main_cookie.png")
print("Found Main Cookie", main_cookie_pos)

golden_img = cv2.imread("./images/golden_cookie.png", cv2.IMREAD_UNCHANGED)

config = cp.ConfigParser(allow_no_value=True)
config.read("./config.ini")

calibrate = config.getboolean("calibrate", "need")
print("Calibrate", calibrate)

if calibrate:
  print("Calibration Required")

config_delay = config.getint("calibrate", "buy_delay")
if calibrate:
  config_delay = input("Enter buy delay:")
  if config_delay and config_delay.isdigit() and int(config_delay) > 0:
    config_delay = int(config_delay)
    config["calibrate"]["buy_delay"] = str(config_delay)
  else:
    print("Invalid input; defaulting Buy Delay")
    config_delay = 10000
  
buy_delay = config_delay
current_delay = 0

click_speed = config.getfloat("calibrate", "click_speed")
if calibrate:
  click_speed = input("Enter a Click Speed:")
  if click_speed and click_speed.isdigit() and float(click_speed) > 0:
    click_speed = float(click_speed)
    config["calibrate"]["click_speed"] = str(click_speed)
  else:
    print("Invalid Input; defaulting Click Speed")
    click_speed = 0.01
pg.PAUSE = click_speed

buy_upgrades = config.getboolean("upgrades", "buy_upgrades")
buy_upgrades_pos = None

if buy_upgrades:
  if calibrate:
    buy_upgrades_pos = captureCursorPos("Upgrade")
    config["upgrades"]["buy_upgrades_pos"] = str([buy_upgrades_pos[0], buy_upgrades_pos[1]])
  else:
    buy_upgrades_pos = eval(config["upgrades"]["buy_upgrades_pos"])
  print("Upgrade Position", buy_upgrades_pos)

buy_buildings = config.getboolean("buildings", "buy_buildings")
buy_buildings_pos = []

if buy_buildings:
  if calibrate:
    if config.getboolean("buildings", "buy_temples"):
      buy_buildings_pos.append(captureCursorPos("Temple"))
      print("Temple Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
      config["buildings"]["buy_temples_pos"] = str([buy_buildings_pos[len(buy_buildings_pos) - 1][0], buy_buildings_pos[len(buy_buildings_pos) - 1][1]])
    if config.getboolean("buildings", "buy_banks"):
      buy_buildings_pos.append(captureCursorPos("Bank"))
      print("Bank Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
      config["buildings"]["buy_banks_pos"] = str([buy_buildings_pos[len(buy_buildings_pos) - 1][0], buy_buildings_pos[len(buy_buildings_pos) - 1][1]])
    if config.getboolean("buildings", "buy_factories"):
      buy_buildings_pos.append(captureCursorPos("Factory"))
      print("Factory Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
      config["buildings"]["buy_factories_pos"] = str([buy_buildings_pos[len(buy_buildings_pos) - 1][0], buy_buildings_pos[len(buy_buildings_pos) - 1][1]])
    if config.getboolean("buildings", "buy_mines"):
      buy_buildings_pos.append(captureCursorPos("Mine"))
      print("Mine Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
      config["buildings"]["buy_mines_pos"] = str([buy_buildings_pos[len(buy_buildings_pos) - 1][0], buy_buildings_pos[len(buy_buildings_pos) - 1][1]])
    if config.getboolean("buildings", "buy_farms"):
      buy_buildings_pos.append(captureCursorPos("Farm"))
      print("Farm Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
      config["buildings"]["buy_farms_pos"] = str([buy_buildings_pos[len(buy_buildings_pos) - 1][0], buy_buildings_pos[len(buy_buildings_pos) - 1][1]])
    if config.getboolean("buildings", "buy_grandmas"):
      buy_buildings_pos.append(captureCursorPos("Grandma"))
      print("Grandma Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
      config["buildings"]["buy_grandmas_pos"] = str([buy_buildings_pos[len(buy_buildings_pos) - 1][0], buy_buildings_pos[len(buy_buildings_pos) - 1][1]])
    if config.getboolean("buildings", "buy_cursors"):
      buy_buildings_pos.append(captureCursorPos("Cursor"))
      print("Cursor Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
      config["buildings"]["buy_cursors_pos"] = str([buy_buildings_pos[len(buy_buildings_pos) - 1][0], buy_buildings_pos[len(buy_buildings_pos) - 1][1]])
  else:
    if config.getboolean("buildings", "buy_temples"):
      buy_buildings_pos.append(eval(config["buildings"]["buy_temples_pos"]))
      print("Temple Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
    if config.getboolean("buildings", "buy_banks"):
      buy_buildings_pos.append(eval(config["buildings"]["buy_banks_pos"]))
      print("Bank Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
    if config.getboolean("buildings", "buy_factories"):
      buy_buildings_pos.append(eval(config["buildings"]["buy_factories_pos"]))
      print("Factory Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
    if config.getboolean("buildings", "buy_mines"):
      buy_buildings_pos.append(eval(config["buildings"]["buy_mines_pos"]))
      print("Mine Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
    if config.getboolean("buildings", "buy_farms"):
      buy_buildings_pos.append(eval(config["buildings"]["buy_farms_pos"]))
      print("Farm Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
    if config.getboolean("buildings", "buy_grandmas"):
      buy_buildings_pos.append(eval(config["buildings"]["buy_grandmas_pos"]))
      print("Grandma Position", buy_buildings_pos[len(buy_buildings_pos) - 1])
    if config.getboolean("buildings", "buy_cursors"):
      buy_buildings_pos.append(eval(config["buildings"]["buy_cursors_pos"]))
      print("Cursor Position", buy_buildings_pos[len(buy_buildings_pos) - 1])

if calibrate:
  print("Calibration Complete")
  config["calibrate"]["need"] = "False"
  with open("./config.ini", "w") as configfile:
    config.write(configfile)

def moveMouseToMainCookie():
  pg.moveTo(main_cookie_pos[0], main_cookie_pos[1])

track_clicks = buy_upgrades and buy_buildings
pbar = enlighten.Counter(total=buy_delay, desc='Clicks', unit='click')

last_keydown = None

print("Cookie Clicker AC v0.1")
while True:
  if kb.is_pressed("k"):
    print("Kill Program")
    break

  if kb.is_pressed("s") and last_keydown != "s":
    last_keydown = "s"
    print("Pause Clicking")
    click = False

  if kb.is_pressed("a") and last_keydown != "a":
    last_keydown = "a"
    print("Start Clicking")
    moveMouseToMainCookie()
    click = True

  if kb.is_pressed("g") and last_keydown != "g":
    last_keydown = "g"
    print("Hunting Golden Cookies")
    goldenCookies = True

  if kb.is_pressed("h") and last_keydown != "h":
    last_keydown = "h"
    print("Pause Hunting Golden Cookies")
    goldenCookies = False

  if goldenCookies:
    result = pg.locateCenterOnScreen(golden_img, confidence=0.6)
    if result is not None:
      print("Found Golden Cookie", result)
      pg.moveTo(result[0], result[1])
      pg.click()

  if click:
    if goldenCookies:
      moveMouseToMainCookie()
    pg.click()
    if track_clicks:
      current_delay += 1
      pbar.update()

      if current_delay >= buy_delay:
        if buy_upgrades:
          print("Buying Upgrades")
          pg.moveTo(buy_upgrades_pos[0], buy_upgrades_pos[1])
          pg.click()
          moveMouseToMainCookie()

        if buy_buildings:
          print("Buying Buildings")
          for pos in buy_buildings_pos:
            pg.moveTo(pos[0], pos[1])
            pg.click()
          moveMouseToMainCookie()

        current_delay = 0
        pbar.update()
