# Premade Loggers

This library is made to make logging simpler and clearer:
It contains :

* Custom levels
* Custom Formats
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
    with log.bugCheck(log.results, 'find'):
        for item in items:
            if item == x:
                indice = items.index(item)
                log.main.cmn_dbg(f'{str(item)} = {type(item)}')
        return items.pop(indice)

items = [n for n in range(0, 5)]
with log.bugCheck(log.main):
    for x in range(0, 6):
        result = find(x, items)
log.main.SDS(f'FINISHED')
```

You can create one instance of CHeckLog in a basic file and import it
where you need to use it, so your log levels for each logger will be the same
evrywhere.

Or you can initiate new instances of CheckLog on each module to change levels
depending on the file you're working on.

Or you can also have some class inheriting CheckLog:

```python
class Finder(CheckLog):
    def __init__(self):
        super().__init__(fmt=pog.FORMATS['locate'])
        self.main.setLevel(pog.LEVELS['1'])
        self.display.setLevel(pog.LEVELS['1'])

    @timer
    def find(self, x, items):
        with self.sbugCheck(self.main):
            for item in items:
                if item == x:
                    indice = items.index(item)
                    F.dataIO.cmn_dbg(f'{str(item)} = {type(item)}')
            return items.pop(indice)


F = Finder()
```

