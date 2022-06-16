class Extra:
    def get_list_of_dict(self,data):
        list_of_dict = []
        for i in data:
            di = dict(i)
            list_of_dict.append(di)
        return list_of_dict
        