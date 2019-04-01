# import os


class Monitor:

    def __init__(self, files):   # конструктор создает фаилы
        self.files = files
        self.myfiles = {}
        for i in files:
            self.myfiles[i] = open(self.to_file_name(i), "w")
            self.add_str('free', i)
            self.myfiles[i].close()
  
    def monitor_check(self, f_name):  # если свободен - true иначе - false
        self.myfiles[f_name] = open(self.to_file_name(f_name), "r")
        s = self.myfiles[f_name].read()
        self.myfiles[f_name].close()
        if(s):
            if s.split(":")[1] == "free":
                return True
            else:
                return False
        else:
            return True

    def monitor_close(self, t_name, f_name):  # ставит метку что файл открыт на чтение
        while not self.monitor_check(f_name):
            pass
        self.add_str(t_name, f_name)
        
    def monitor_open(self, f_name):  # ставит метку что файл освободился и любой поток может получить к нему доступ
        self.add_str('free', f_name)
       
    def add_str(self, t_name, f_name):
        to_file = f_name + ":" + t_name
        self.myfiles[f_name] = open(self.to_file_name(f_name), "w")
        self.myfiles[f_name].write(to_file)
        self.myfiles[f_name].close()

    def to_file_name(self, f_name):
        return "monitor_" + f_name + ".txt"

    #def __del__(self):

    #    for i in self.files:
    #        try:
    #            os.remove(self.to_file_name(i))
    #        except PermissionError: 
    #            print("Монитор фаилы не были удалены")
    #    print("deleted")
