#!/usr/bin/env python

"""
Author  :        Thomas Fujise
Date    :        02.06.2022
File    :        accessink.py
Version :        1.0.0
Brief   :        Polar accesslink class to made all request and get the data
"""

from __future__ import print_function

from utils import load_config, save_config, pretty_print_json
from accesslink import AccessLink
from db import cursor
from datetime import datetime
from config import WORKOUT_TYPE

try:
    input = raw_input
except NameError:
    pass


CONFIG_FILENAME = "config.yml"


class PolarAccessLink(object):
    """Polar Open AccessLink v3."""

    def __init__(self):
        self.config = load_config(CONFIG_FILENAME)

        if "access_token" not in self.config:
            print("Authorization is required. Run authorization.py first.")
            return

        self.accesslink = AccessLink(client_id=self.config["client_id"],
                                     client_secret=self.config["client_secret"])

        self.running = True
        #self.get_exercises()

       

    def show_menu(self):
        while self.running:
            print("\nChoose an option:\n" +
                  "-----------------------\n" +
                  "1) Get user information\n" +
                  "2) Check available data\n" +
                  "3) Revoke access token\n" +
                  "4) Exit\n" +
                  "-----------------------")
            self.get_menu_choice()

    def get_menu_choice(self):
        choice = input("> ")
        {
            "1": self.get_user_information,
            "2": self.check_available_data,
            "3": self.revoke_access_token,
            "4": self.exit
        }.get(choice, self.get_menu_choice)()

    def get_user_information(self):
        user_info = self.accesslink.users.get_information(user_id=self.config["user_id"],
                                                          access_token=self.config["access_token"])
        pretty_print_json(user_info)

    def check_available_data(self):
        available_data = self.accesslink.pull_notifications.list()

        if not available_data:
            print("No new data available.")
            return

        print("Available data:")
        pretty_print_json(available_data)

        for item in available_data["available-user-data"]:
            if item["data-type"] == "EXERCISE":
                self.get_exercises()
            elif item["data-type"] == "ACTIVITY_SUMMARY":
                self.get_daily_activity()
            elif item["data-type"] == "PHYSICAL_INFORMATION":
                self.get_physical_info()

    def revoke_access_token(self):
        self.accesslink.users.delete(user_id=self.config["user_id"],
                                     access_token=self.config["access_token"])

        del self.config["access_token"]
        del self.config["user_id"]
        save_config(self.config, CONFIG_FILENAME)

        print("Access token was successfully revoked.")

        self.exit()

    def exit(self):
        self.running = False

    def get_exercises(self, userId):
        sql = "INSERT INTO WORKOUT (workout_type, client_id, date, duration, heart_rate_max, heart_rate_avg, calories, distance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        #Init values
        values = ()

        workout_type = ''
        client_id = userId
        date = ''
        duration = ''
        heart_rate_max = ''
        heart_rate_avg = ''
        calories = ''
        distance = ''

        transaction = self.accesslink.training_data.create_transaction(user_id=self.config["user_id"],
                                                                       access_token=self.config["access_token"])
        if not transaction:
            print("No new exercises available.")
            return

        resource_urls = transaction.list_exercises()["exercises"]
        

        for url in resource_urls:
            exercise_summary = transaction.get_exercise_summary(url)

            print("Exercise summary:")
            pretty_print_json(exercise_summary)
            if WORKOUT_TYPE[exercise_summary['detailed-sport-info']] is not None:
                workout_type = WORKOUT_TYPE[exercise_summary['detailed-sport-info']]

            date = exercise_summary['start_time']
            start = datetime(exercise_summary['start_time'])
            end = datetime(exercise_summary['upload-time'])
            duration = (end-start)
            heart_rate_max = exercise_summary["heart-rate"]["maximum"]
            heart_rate_avg = exercise_summary["heart-rate"]["average"]
            calories = exercise_summary["calories"]

            if exercise_summary['distance'] is not None:
                distance = exercise_summary['distance']
            
            values = (workout_type, client_id, date, duration, heart_rate_max, heart_rate_avg, calories, duration)


        transaction.commit()

    def get_daily_activity(self):
        transaction = self.accesslink.daily_activity.create_transaction(user_id=self.config["user_id"],
                                                                        access_token=self.config["access_token"])
        if not transaction:
            print("No new daily activity available.")
            return

        resource_urls = transaction.list_activities()["activity-log"]

        for url in resource_urls:
            activity_summary = transaction.get_activity_summary(url)

            print("Activity summary:")
            pretty_print_json(activity_summary)

        transaction.commit()

    def get_physical_info(self):
        transaction = self.accesslink.physical_info.create_transaction(user_id=self.config["user_id"],
                                                                       access_token=self.config["access_token"])
        if not transaction:
            print("No new physical information available.")
            return

        resource_urls = transaction.list_physical_infos()["physical-informations"]

        for url in resource_urls:
            physical_info = transaction.get_physical_info(url)

            print("Physical info:")
            pretty_print_json(physical_info)

        transaction.commit()

