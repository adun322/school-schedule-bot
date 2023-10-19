import sqlite3
import xlrd

DayOfWeek = {0: '!&', 1: 'Пн', 2: 'Вт', 3: 'Ср', 4: 'Чт', 5: 'Пт'}


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor() 
    def adduser(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES(?)", (user_id,))
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
    def set_class(self, user_id, classid):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `classid` = ? WHERE `user_id` = ?", (classid, user_id,))
    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            signup = ''
            for row in result:                
                signup = str(row[0])
            return signup
    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))

    def get_users(self, t=5):
        with self.connection:
            if t == 1:
                return self.cursor.execute("SELECT `user_id` FROM `users` WHERE `signup` = ?", ('setclass',)).fetchall()
            elif t == 2:
                return self.cursor.execute("SELECT `user_id` FROM `users` WHERE `classid` = ?", ('8Д',)).fetchall()
            else:
                return self.cursor.execute("SELECT `user_id` FROM `users`").fetchall()

    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `active` = ? WHERE `user_id` = ?", (active, user_id))
        

    def shedule(self, user_id, dw, week = False):
        with self.connection:                
                
            res = self.cursor.execute("SELECT `classid` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            kl = (res[0])
            kl = str(kl)


            if len(kl) > 2:
                x = int(kl[0])*10+int(kl[1])
            else:
                x = int(kl[0])                
            x -= 5
        
            inputWorkbook = xlrd.open_workbook('raspisanie.xls')                
            inputWorksheet = inputWorkbook.sheet_by_index(x)
            r = inputWorksheet.nrows
            ras = ''

            if 'А' in kl:
                buk = 2
            elif 'Б' in kl:
                buk = 4
            elif 'В' in kl:
                buk = 6
            elif 'Г' in kl:
                buk = 8
            elif 'Д' in kl:
                buk = 10
            elif 'Е' in kl:
                buk = 12
            elif 'И' in kl:
                buk = 14
            
            f = False
            for i in range(r):
                a = inputWorksheet.cell_value(i,buk)
                kab = inputWorksheet.cell_value(i,buk+1)                
                n = inputWorksheet.cell_value(i,1)
                dwt = inputWorksheet.cell_value(i,0)

                if week:
                    if dwt!='':
                        if week or dwt == DayOfWeek[dw]:
                            if week and dwt != '' and 'а' not in dwt and 'e' not in dwt:
                                ras += '\n'
                            f = True
                        else:
                            f = False
                            break
                else:
                    if DayOfWeek[dw] == dwt:
                        f = True
                    elif f and dwt != '': 
                        f = False
                        break

                if f:
                    if n != '#' and n != '' and a != '':
                        try:
                            chzha = int(kab)                                    
                            ras += str(int(n))+ '. '+str(a) + ' ('+str(kab)[:len(str(kab))-2]+')' + '\n'
                        except:
                            ras += str(int(n))+ '. '+str(a) + ' ('+str(kab)+')' + '\n'                                          
            return(ras)
