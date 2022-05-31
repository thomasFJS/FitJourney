from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.CardType import AnyCardType
from smartcard import util
import time

def get_card_id():
    card_type = AnyCardType()

    request = CardRequest(timeout=30, cardType=card_type)

    card = None

    while card == None:
        time.sleep(0.1)

        service = None
        try:
            service = request.waitforcard()
        except:
            print("ERROR: No card detected")
            break

        conn = service.connection
        conn.connect()

        get_uid = util.toBytes("FF CA 00 00 00")

        data, sw1, sw2 = conn.transmit(get_uid)

        card = ' '.join(str(e) for e in data)
    
    return card