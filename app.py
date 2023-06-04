from flask import Flask, render_template, request, session, redirect, url_for
import pygame as pg
import time
from pathlib import Path

app = Flask(__name__)
# to create cookie need to cryptographically sign cookie - ensures user can't change content of cookie
app.secret_key = "chase"

GONG_PATH = Path(r"C:\Users\User\Desktop\workspaces\local\PYTHON\HIT_APP\sound_files\gong.wav")
BEEP_PATH = Path(r"C:\Users\User\Desktop\workspaces\local\PYTHON\HIT_APP\sound_files\beep.wav")
EXERCISES = ["Jumping Jacks", "Burpees", "Mountain Climbers", "Push ups", "Lunges", "Squats", "Plank", "Bicycle kicks", "Leg Thrusts", "High knees"]
beep_track = ""
gong_track = ""

pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(50)

def play(_path): 
    track = pg.mixer.Sound(_path)
    track.play()


def beep(start):
    # TODO add docstring, typing
    play(BEEP_PATH)
    print("3")
    time.sleep(1)
    play(BEEP_PATH)
    print("2")
    time.sleep(1)
    play(BEEP_PATH)
    print("1")
    time.sleep(1)
    play(GONG_PATH)

@app.route("/", methods=["GET", "POST"]) # endpoints, on where to point to page - define in Flask
def home():
    if request.method == "POST":
        exercise = int(request.form["exercise"])
        rest = int(request.form["rest"])
        sets = int(request.form["sets"])
    
        
        # stores data of what user inputs into COOKIE as dictionary
        # this will allow us to see data entered by user
        session["exercise"] = exercise
        session["rest"] = rest
        session["sets"] = sets
        # set counter stores how much sets user has done
        session["set_counter"] = 0
        
        # take rest func, constructs endpoint and sends browser redirect to rest page
        return redirect(url_for("rest"))
    return render_template("home.html")


@app.route("/rest")
def rest():
    return render_template("rest.html", rest=session["rest"])


@app.route("/exercise")
def exercise():
    if session["set_counter"] == session["sets"]:
        return redirect(url_for("completed"))
    session["set_counter"] += 1
    return render_template("exercise.html", exercise=session["exercise"])

@app.route("/complete")
def completed():
    return render_template("complete.html", sets=session["set_counter"])
    