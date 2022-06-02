"""
Author  :        Thomas Fujise
Date    :        02.06.2022
File    :        main.py
Version :        1.0.0
Brief   :        Python script to check if card scanned are allowed (if they are assign to a client) and to save exercise data with Polar API 
"""
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.CardType import AnyCardType
from smartcard import util
from accesslink_polar import PolarAccessLink
import time

from db import cursor, getUserIdByCard

if __name__ == '__main__':

    #Init Polar class
    polar = PolarAccessLink()

    #Query to get the card id from user
    selectQuery = "SELECT name, surname, card_id FROM USER"


    cursor.execute(selectQuery)

    myresult = cursor.fetchall()
    # respond to the insertion of any type of smart card
    card_type = AnyCardType()
    
    # create the request. Wait for up to x seconds for a card to be attached
    request = CardRequest(timeout=None, cardType=card_type)

    entry = False
    while True:
                time.sleep(0.1)
                # listen for the card
                service = None
                try:
                    service = request.waitforcard()
                except CardRequestTimeoutException:
                    print("ERROR: No card detected")
                    exit(-1)

                # when a card is attached, open a connection
                conn = service.connection
                conn.connect()

                # get and print the ATR and UID of the card
                get_uid = util.toBytes("FF CA 00 00 00")

                data, sw1, sw2 = conn.transmit(get_uid)

                print(data)
                card_scanned = ' '.join(str(e) for e in data)
                print(card_scanned)
                card_found = False
                
                for client in myresult:
                    
                    if client[2] == card_scanned:
                        card_found = True
                        if entry:
                            print("-------------GOODBYE " + client[0] + " " + client[1]+ "---------------")
                            polar.get_exercises(getUserIdByCard(client[2]))
                            entry = False
                        else:
                            print("-------------WELCOME " + client[0] + " " + client[1]+ "---------------")
                            entry = True

                                                        
                if not card_found:
                    print("ENTRY REFUSED")      

                time.sleep(2)
        