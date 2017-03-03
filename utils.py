import json

# per https://www.blog.pythonlibrary.org/2014/02/14/python-101-how-to-change-a-dict-into-a-class/
########################################################################
class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """
 
    #----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])
 
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<Dict2Obj: %s>" % self.__dict__
 
#----------------------------------------------------------------------

def savejson(dump, location):
    with open(location, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(dump, indent=2, sort_keys=True))


def cleanDates(x):
    ''' return text date and then a yyyy-mm-dd date '''
    d = parse(x)
    cleandate = '{dt:%B} {dt.day}, {dt.year}'.format(dt=d.date())
    return cleandate, str(d.date())
    

def input_yn(x):
    phrase = x.strip() + ' (y/n) '
    _ = input(phrase).lower()
    if _ == 'y':
        return True
    elif _ == 'n':
        return False
    else:
        print('\nSay what?')
        return input_yn(x)