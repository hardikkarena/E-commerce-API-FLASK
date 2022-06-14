import os,re

class Validator:
    
    def validate_input(self,input):
        _flag=True
        for i in input:
            if i=='':
                _flag=False
        return _flag

    def validate_password(self,password):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
        match_re = re.compile(reg)
        res = re.search(match_re, password)
        if res:
            return True
        else:
            return False