# Premade Loggers

This library is made to make logging simpler and clearer:
It contains :

* Custom levels
* Custom Formats
* a timer decorator
* A Logger class, allowing to log in color
* The CheckLog class to manage loggers

### Quick Guide

###### Levels

There are 8 levels, accessible with the LEVELS dictionary :

```python
LEVELS = {"1": logging.SPC_DBG,     #Specific Debug 
          "2": logging.DEBUG,       #Classic Debug
          "3": logging.CMN_DBG,     #Common Debug
          "4": logging.SPC_INFO,    #Specific Infos
          "5": logging.INFO,        #Classic Infos, 'success' log is at the same level
          "6": logging.CMN_INFO,    #Common Infos
          "7": logging.ERROR,       #Classic Error, 'exception' log is at the same level
          "8": logging.CRITICAL,    #Classic Critical
          }

```

###### Formats

There are 3 formats, accessible with the FORMATS dictionary :
```python
FORMATS = {
    'classic': ': %(asctime)s:%(levelname)s:%(name)s:%(message)s',
    'light': ': %(message)s',
    'locate': '(%(module)s / %(lineno)d): %(message)s'
}
```



###### Basic Usage

You can find these examples at the end of main.py

```python
import prelog as pog

#Create an instance of CheckLog
log = pog.CheckLog(fmt=pog.FORMATS['locate'])

#Create a custom logger
log.create_logger('results', pog.Fore.BLUE, pog.FORMATS['light'])

#Set logging level for the loggers you need :
log.main.setLevel(pog.LEVELS['1'])
log.results.setLevel(pog.LEVELS['1'])

#Log events, using context manager or simple log message :
def find(x, items):
    with log.cbugCheck(log.results, 'find'):
        for item in items:
            if item == x:
                indice = items.index(item)
                log.main.cmn_dbg(f'{str(item)} = {type(item)}')
        return items.pop(indice)

items = [n for n in range(0, 5)]
with log.sbugCheck(log.main):
    for x in range(0, 6):
        result = find(x, items)
log.main.SDS(f'FINISHED')

#Tou can also use the time context manager :
items = [n for n in range(0, 5)]
results = []
for x in range(0, 6):
    with log.timeCheck(find, x, items) as result:
        results.append(result)
log.main.cmn_dbg(f'{[result for result in results]}')

#You can create one instance of CheckLog in a basic file and import it
#where you need to use it, so your log levels for each logger will be the same
#evrywhere.

#Or you can initiate new instances of CheckLog on each module to change levels
#depending on the file you're working on.

#Or you can also have some class inheriting CheckLog:
class Finder(pog.CheckLog):
    def __init__(self):
        super().__init__(fmt=pog.FORMATS['locate'])
        self.main.setLevel(pog.LEVELS['1'])
        self.display.setLevel(pog.LEVELS['1'])

#You can also add the timer decorator, that will return a tuple
#with the result of the function and the time of execution 
    @pog.timer
    def find(self, x, items):
        with self.cbugCheck(self.main):
            for item in items:
                if item == x:
                    indice = items.index(item)
                    F.dataIO.cmn_dbg(f'{str(item)} = {type(item)}')
            return items.pop(indice)

F = Finder()
items = [n for n in range(0, 5)]
for x in range(0, 6):
    F.find(x, items)
F.main.SDS(f'FINISHED')
```

