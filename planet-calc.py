"""
All code for this was written by me. However, suggestions, formulas, and
mathematical equations used were put together in a sort of tutorial which
I referenced, which was created by Paul Schlyter at

https://stjarnhimlen.se/comp/ppcomp.html#12b

"""

#for exiting if there is an error
import sys
#To access functions like sine, cosine, and tangent
import math
#To get latitude and longitude given the name of a city
from astral.geocoder import database, lookup

#getting the input for date, time, and location
x = [int(x) for x in input("Date [DD MM YYYY]: ").split()]
try:
    day = x[0]
    month = x[1]
    year = x[2]
except:
    print("Enter the numbers as integers, not strings.")
    print("Oh, and don't put '/' or '-' between the characters. Just put a single space.")
    sys.exit()
try:
    print("Give times in Universal Time.")
    print("EDT is 4 hours behind UTC. EST is 5 hours behind.")
    print("Use 24 hour time with 00:00 being midnight.")
    time = str(input("specify UTC time in HH:MM format: "))
except:
    print("Please enter correct UTC time in HH:MM format")
    sys.exit()
if ":" not in time:
    print("")
    print("You need to include the ':' when writing the time.")
    print("Restart the program and try again.")
    sys.exit()
try:
    city = input("Please enter your nearest major city: ")
    thing = lookup(city, database())
except KeyError:
    print("The city is not in the database. Try the nearest capital.")
    sys.exit()

lat = thing.latitude
long = thing.longitude
time = time.replace(":",".")
time = float(time)

#This formula only works from March 1900-Feb 2100
d = 367*year - (7*(year + ((month+9)/12)))//4 + (275*month)//9 + day - 730530
d = d + (time/24.0)

class Sun:
    
    """
        this fucntion translated from JavaScript code by J. Geisen at
        http://www.jgiesen.de/kepler/kepler.html
    """
    def ecc_anom(e, M, dp):
    #calculates that BASTARD of a number, the eccentric anomaly
        K = math.pi/180
        maxiter = 30
        i = 0
        delta = 10 ** -dp
        M = M/360.0
        M = 2.0*math.pi*(M-math.floor(M))
        if e < 0.8:
            E = M
        else:
            E = math.pi
        F = E - e*math.sin(math.radians(M)) - M
        while abs(F) > delta and i < maxiter:
            E = E - F/(1.0 - e * math.cos(E))
            F = E - e * math.sin(E) - M
            i = i + 1
        E = E/K
        return round(E*(10 ** dp)/(10 ** dp),5)

    def ecliptic(d):
        global L
        global x
        global y
        global oblecl
        #all angular values are in degrees
        w = 282.9404 + 4.70935E-5 * d        #(longitude of perihelion)
        a = 1.000000                         #(mean distance, a.u.)
        e = 0.016709 - 1.151E-9 * d          #(eccentricity)
        M = 356.0470 + 0.9856002585 * d      #(mean anomaly)
        oblecl = 23.4393 - 3.563E-7 * d      #obliquity of the ecliptic
        M = M % 360
        L = w + M                            #mean longitude
        L = L % 360
        E = Sun.ecc_anom(e,M,5)
        #calculates suns rectangular coordinates
        x = math.cos(math.radians(E)) - e
        y = math.sin(math.radians(E)) * math.sqrt(1 - e*e)
        #convert to true anomaly
        r = math.sqrt((x*x) + (y*y))
        v = math.atan2(y,x)
        v = math.degrees(v)
        #calculates longitude
        lon = v + w
        lon = lon % 360
        #calculates ecliptic rectangular coordinates
        x = r * math.cos(math.radians(lon))
        y = r * math.sin(math.radians(lon))
        z = 0.0
        print("Ecliptic Coordinates:")
        print("x: " + str(x))
        print("y: " + str(y))
        print("z: " + str(z))
        
    def equatorial():
        global RA1
        global Decl
        #rotates coordinates
        xequat = x
        yequat = y * math.cos(math.radians(oblecl)) - 0.0 * math.sin(math.radians(oblecl))
        zequat = y * math.sin(math.radians(oblecl)) + 0.0 * math.cos(math.radians(oblecl))
        #convert to RA and Decl
        r =  math.sqrt(xequat*xequat + yequat*yequat + zequat*zequat)
        RA =  math.atan2(yequat, xequat)
        Decl =  math.atan2(zequat, math.sqrt(xequat*xequat + yequat*yequat))
        RA = math.degrees(RA)
        Decl = math.degrees(Decl)
        RA = RA/15
        RA1 = RA
        hours = int(RA)
        minutes = (RA*60) % 60
        seconds = (RA *3600) % 60
        hours = int(hours)
        minutes = int(minutes)
        seconds = round(seconds, 2)
        RA = (hours, minutes, seconds)
        mnt, sec = divmod(Decl*3600,60)
        deg, mnt = divmod(mnt,60)
        sec = int(sec)
        sec = round(sec, 2)
        print("Equatorial Coordinates:")
        print("RA: " + str(hours) + "h" + " " + str(minutes) + "m" + " " + str(seconds) + "s")
        print("Decl: " + str(deg) + "°" + " " +  str(mnt) + "'" + " " + str(sec) + '"')
        
    def horizontal(time, lat, long):
        GMST0 = L/15 + 12
        SIDTIME = GMST0 + time + long/15
        HA = SIDTIME - RA1
        HA = HA * 15
        x = math.cos(math.radians(HA)) * math.cos(math.radians(Decl))
        y = math.sin(math.radians(HA)) * math.cos(math.radians(Decl))
        z = math.sin(math.radians(Decl))
        xhor = x * math.sin(math.radians(lat)) - z * math.cos(math.radians(lat))
        yhor = y
        zhor = x * math.cos(math.radians(lat)) + z * math.sin(math.radians(lat))
        azimuth = math.degrees(math.atan2(yhor,xhor)) + 180
        altitude = math.asin(zhor)
        azimuth = azimuth % 360
        altitude = math.degrees(altitude)
        print("Horizontal Coordinates:")
        print("Azimuth: " + str(azimuth))
        print("Altitude: " + str(altitude))


print(" ")
print("Sun:")
print("--------------------")
Sun.ecliptic(d)
print(" ")
Sun.equatorial()
print(" ")
Sun.horizontal(time,lat,long)
print("")
print("--------------------")
print("""Note:

Equatorial coordinates and Ecliptic coordinates,
due to their nature, assume an origin point at the center of the Earth.
Therefore, things like the RA and Declination may differ from
topocentric coordinates which assumes an origin point at your location.
The horizontal coordinates do take into account your location.

All measurements are in degrees.
""")
