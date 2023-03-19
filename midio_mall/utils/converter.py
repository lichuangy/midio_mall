
######定义转换器#######
class UserNameConvert:
    regex = '[a-zA-Z0-9_-]{5,50}'

    def to_pathon(self,value):
        return value