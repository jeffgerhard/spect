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
