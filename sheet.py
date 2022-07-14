from asyncio.log import logger
import gspread
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

sa = gspread.service_account()
sh = sa.open("Доступ в К006")
wks = sh.worksheet("Расписание К006")
people = sh.worksheet("Список студентов с доступом")

class Sheet:
    days = {'Mon': 'B', 'Tue': 'C', 'Wed': 'D', 'Thu':'E', 'Fri': 'F', 'Sat': 'G', 'Sun': 'H'}
    times = {9: '3', 10: '4', 11: '5', 12: '6', 13: '7', 14: '8', 15: '9', 16: '10', 17: '11', 18: '12', 19: '13', 20: '14', 21: '15', 22: '16'}
    
    @classmethod
    def isOverLimit(self, name):
        reps = 0
        listed = wks.get('B3:H16')
        for rows in listed:
            for cells in rows:
                if cells.lower() == name.lower():
                    reps += 1
        if reps >= 3:
            return True
        return False
    
    @classmethod
    def isListed(self, name):
        listed = people.col_values(2)
        print(listed)
        for person in listed:
            if person.lower() == name.lower():
                return True
        return False

    @classmethod
    def add(self, name, day, time):
        if not self.isOverLimit(name):
            slot = ''
            if day in self.days and time in self.times:
                slot = self.days[day] + self.times[time]
            if wks.acell(slot).value:
                return 'This time slot is already booked'
            arr = name.split()
            name = arr[0].lower().capitalize() + ' ' + arr[1].lower().capitalize()

            wks.update(slot, name)
            logger.info("Time slot added by %s on %s at %s:00", name, day, time)
            return 'Success'
        
        return 'You are you have booked more than 3 slots'

    @classmethod
    def delete(self, name, day, time):
        slot = ''
        if day in self.days and time in self.times:
            slot = self.days[day] + self.times[time]
        if wks.acell(slot).value == '':
            return 'It is empty'
        if wks.acell(slot).value.lower() != name.lower():
            return 'You can not delete time slots of others'
        wks.update(slot, '')
        logger.info("Time slot deleted by %s on %s at %s:00", name, day, time)
        return 'Success'
    
    @classmethod
    def get_list_day(self, day):
        listed = wks.get(self.days[day] + '3:'+ self.days[day] + '16') 
        output = '{}:\n'.format(day)
        for i in range(14):
            output += '{}:00 - {}:00  '.format(i + 9, i + 10)
            if i < len(listed):
                if not listed[i]:
                    output += ''
                else:
                    list_per = listed[i]
                    output += str(list_per[0])
            output += '\n'
        return output
    
    @classmethod
    def get_all_list(self):
        output = ''
        for day in self.days.keys():
            output += self.get_list_day(day)
            output += '\n'
        return output