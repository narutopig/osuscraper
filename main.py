import os, sys, time, shutil

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

songsDir = os.path.join(sys.argv[1], "Songs")

if os.path.isdir(songsDir) == False:
    print("Songs folder not found")
    sys.exit(1)

result = "" # folder where songs will be

if len(sys.argv) >= 3 and os.path.isdir(sys.argv[2]):
    result = sys.argv[2]
    print("Result folder found")
else:
    temp = os.path.join(os.getcwd(), "Songs " + str(time.time()))
    print("Result folder not found, creating new one")
    if os.path.isdir(temp):
        print("New result folder already exists, exiting")
        sys.exit(1)
    result = temp
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
