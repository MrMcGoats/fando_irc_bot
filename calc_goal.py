import datetime
from pytz import timezone


est=timezone("Canada/Eastern") #AlttpFando hates the west and east coasts. They also hate central NA and all of Europe and Asia, among many other places

def calc_goal(day=datetime.datetime.now(est).day,month=datetime.datetime.now(est).month,year=datetime.datetime.now(est).year):
    #fix any fuckery from subtracting the day by 1
    if day<1:
        month-=1
        year-=1
        if month<1:
            month=12
        if month in [4,6,9,11]:
            day=30
        elif month==2:
            if year%4==0: #leap year
                day=29
            else:
                day=28
        else:
            day=31

    today=datetime.date(year,month,day).weekday()
    if today==3: #Inverted
        return -2
    elif today==6: #Spoiler Log Sunday
        return -1
    else: #Alright…fuck. So, the easiest way I can think to do this is to just hardcode the mode on a specific date, then do recursive calls until we find that fucker

        #NOTE: this method is super shitty and should be replaced eventually, although I doubt it will be
        if today==0 or today==4: #It's not wednesday or sunday, so skip those days
            return calc_goal(day=day-2)

        if year==2018 and month==11 and day==3:
            return 1 #Standard

        return (calc_goal(day=day-1)+1)%2
    
if __name__=="__main__":
    print("This is not an executable")
