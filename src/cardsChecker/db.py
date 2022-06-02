#!/usr/bin/env python

"""
Author  :        Thomas Fujise
Date    :        02.06.2022
File    :        db.py
Version :        1.0.0
Brief   :        Database connector
"""

import config
import mysql.connector

db = mysql.connector.connect(
  host=config.DB_HOST,
  user=config.DB_USER,
  password=config.DB_PASSWORD,
  database=config.DB
)

cursor = db.cursor()

def getUserIdByCard(cardId):
    sql = "SELECT id FROM USER WHERE card_id = %s"
    card = (cardId,)

    cursor.execute(sql, card)

    result = cursor.fetchone()

    return result