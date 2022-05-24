import os, sys, time, shutil, configparser

def anyStarts(string, strings): # checks if string starts with any value in strings
    for s in strings:
        if string.startswith(s):
            return True
    return False

def getData(dotosu):
    f = open(dotosu)
    lines = f.readlines()
    pretexts = ["AudioFilename:", "Title:", "Artist:", "Version:"]
    stuffs = [l.replace("/", "_") for l in lines if anyStarts(l, pretexts)]

    # gets the actual data
    for i in range(len(stuffs)):
        stuffs[i] = stuffs[i][len(pretexts[i]):].lstrip().rstrip()

    return stuffs

def alreadyThere(datas, data):
    for d in datas:
        if d[0] == data[0]:
            return True

    return False

def requestYn(msg):
    res = input(msg).lower()
    
    while True:
        if res == "y":
            return True
        elif res == "n":
            return False
        else:
            print("Invalid option")
        res = input(msg).lower() 
     
config = configparser.ConfigParser()
config.read("config.ini")

songsDir = ""
if "OPTIONS" in config and "osu" in config["OPTIONS"] and os.path.exists(config["OPTIONS"]["osu"]):
    usecfg = requestYn("Valid osu! installation found, would you like to use this one? (Y/n) ")
    if usecfg:
        sys.argv = sys.argv[1:]
        songsDir = os.path.join(config["OPTIONS"]["osu"], "Songs")

if songsDir == "":
    try:
        songsDir = os.path.join(sys.argv[1], "Songs")
    except IndexError:
        print("Invalid number of arguments")
        sys.exit(1)

if os.path.isdir(songsDir) == False:
    print("Songs folder not found")
    sys.exit(1)
else:
    print("Songs folder found")

if "OPTIONS" not in config or "osu" not in config["OPTIONS"]:
    save = requestYn("Found osu! Songs folder, would you like to save this for later use? (Y/n) ")
    if save:
        config["OPTIONS"] = {"osu": sys.argv[1]}
        with open("config.ini", "w") as cfgFile:
            config.write(cfgFile)

result = "" # folder where songs will be

if "OPTIONS" in config and "result" in config["OPTIONS"] and os.path.exists(config["OPTIONS"]["result"]):
    usecfg = requestYn("Valid result foulder found, would you like to use this one? (Y/n) ")
    if usecfg:
        result = config["OPTIONS"]["result"]

if result == "":
    result = sys.argv[len(sys.argv) - 1] # last element
print("Result folder found")

save = False

if "OPTIONS" not in config or "result" not in config["OPTIONS"]:
    save = requestYn("Found result folder, would you like to save this for later use? (Y/n) ")

if save:
    config["OPTIONS"]["result"] = result
    with open("config.ini", "w") as cfgFile:
        config.write(cfgFile)

if os.path.isdir(result) == False:
    os.mkdir(result)

for file in os.listdir(songsDir):
    song = os.path.join(songsDir, file)

    if os.path.isdir(song):
        osus = [f for f in os.listdir(song) if f.endswith(".osu")]

        audios = []

        for o in osus:
            data = getData(os.path.join(song, o))
            if alreadyThere(audios, data) == False:
                audios.append(data)

        for a in audios:
            source = os.path.join(song, a[0])
            destination = ""

            if len(audios) == 1:
                destination = os.path.join(result, f"{a[2]} - {a[1]}.mp3")
            else:
                destination = os.path.join(result, f"{a[2]} - {a[1]} [{a[3]}].mp3")

            try:
                shutil.copy(source, destination)
            except FileNotFoundError:
                print(destination + " not found")

            print("Copied file " + source + " to " + destination)

print("Success!")
