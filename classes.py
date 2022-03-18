
import cryptonator
from price import *
class Token:
    def __init__(self,coco,symbol,price,mcap,supply,lp):
        self.name = symbol
        self.supply = supply
        self.lp = lp
        self.mcap = mcap
        self.price = price
        self.sss = coco
        
        
    def check(self):
        bnb = "${0:,.4f}".format(float(bnbprice()))
        sup = "{0:,.4f}".format(float(self.supply))
        reply = f"{self.name}\n" \
                f"<b>{self.sss}: ${self.price}\n" \
                f"BNB: {bnb}\n" \
                f"🐱MCap: ${self.mcap}\n\n" \
                f"Supply: {sup}</b>\n" \
                f"<b>🦋LP:</b> {self.lp}\n" 
        print(reply)
        return reply
        
        
        
        
    