import datetime
data = b't20h72p101081co21142.9nh315.33ch40.00no20.67b100*1010811142.90.67'
data = data.decode(encoding = "utf-8")
dt = datetime.datetime.today()
year = str(dt.year)
print(year[2:])
print(dt.hour)