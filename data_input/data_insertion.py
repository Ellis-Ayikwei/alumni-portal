#!/usr/bin/python3
from ast import Sub
import datetime
import json

from webbrowser import open_new
from colorama import init, Fore, Style

from datetime import date as dt

import sys

from google_crc32c import value
sys.path.append("..")
from models import storage
from models.exercise import Exercise
from models.muscle_group import MuscleGroup
from models.sub_muscle import SubMuscle
from models.workout_plan import WorkoutPlan
from models.workout_level import WorkoutLevel
from models.fitness_goal import FitnessGoal


# "013f6e28-855a-4c9b-8213-1a911aefe22c"

# storage.close()
init(autoreset=True)

storage.reload()




# def add_new_exercises(exercises):
#     new_exercise = Exercise(
#         name=exercises["name"],
#         gif_url=exercises["gifUrl"],
#         muscle_group=exercises["bodyPart"],
#         equipment=exercises["equipment"],
#         body_part=exercises["bodyPart"],
#         target=exercises["target"],
#         metric=exercises["metric"],
#         local_png=exercises["localPng"],
#         local_url=exercises["localUrl"],
#     )
#     new_exercise.save()
#     print(f"{Fore.BLUE}exercises successfully inserted!")

# def add_muscle_groups(mg):
#     new_mg = MuscleGroup(
#         name=mg["muscleGroupName"],
#         description=mg["description"],
#     )
#     new_mg.save()
#     print(f"{Fore.BLUE}muscle groups successfully inserted!")
    

# def add_sub_muscle_group(mg):
#     main_muscle_id = None
#     for main_muscle in storage.all(MuscleGroup).values():
#         if main_muscle.name == mg["mainMuscle"]:
#             main_muscle_id = main_muscle.id
#             break

#     new_sb_mg = SubMuscle(
#         name=mg["subMuscleName"],
#         description=mg["description"],
#         main_muscle_id=main_muscle_id
#     )
#     new_sb_mg.save()
#     print(f"{Fore.BLUE}sub muscle group successfully inserted!")


# def add_workout_level(wl):
#     new_wl = WorkoutLevel(
#         description=wl["Description"],
#         level_name=wl["Level_name"],
#         suitable_for_female=wl["female"],
#         suitable_for_male=wl["male"],
#         image=wl["image"]
#     )
#     new_wl.save()
#     print(f"{Fore.BLUE}workout level successfully inserted!")

def add_fitness_goal(wl):
    new_wl = FitnessGoal(
    definition = wl["Definition"],
    description = wl["Description"],
    diet_recommendations = wl["Diet_Recommendations"],
    name = wl["Goal"],
    workout_recommendations = wl["Workout_Recommendations"]
    )
    new_wl.save()
    print(f"{Fore.BLUE}workout level successfully inserted!")



with open("fitnessGoals.json", "r") as f:
    exercises = json.load(f)
    for ex in exercises:
        add_fitness_goal(ex)












# def add_new_users():
#     for i in range(30):
#         new_user = User(
#             first_name=f"{i}FirstName",
#             last_name=f"{i}LasttName",
#             username=f"userNo.{i}",
#             password="@Toshib123",
#             dob = datetime.datetime.utcnow(),
#             phone_number=f"123{i + 1}567{i}90",
#             role="SUPER_ADMIN",
#             address = f"1{i + 3}{i}3 Main St",
#             occupation = f"{i}Occupation",
#             email=f"userNo.{i}@example.com",
#         )
#         new_user.save()
#     print(f"{Fore.BLUE}users successfully inserted!")
    
    
    
# add_new_users()
