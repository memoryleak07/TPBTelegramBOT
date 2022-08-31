from testThePirateBay import ThePirateBay
from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

capt = Capturing()
pirate =ThePirateBay()

#print(pirate.GetCategories())

page = 0

foundtorrents, magnetlinks, urls = pirate.CustomizedSearch("nirvana", 100)
print(foundtorrents)

# allcategories = pirate.PrintCategories()
# print(allcategories)