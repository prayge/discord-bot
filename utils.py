import pandas as pd

keito = [
    "Man fuck you I'll see you at work",
    "Your mother",
    "Just bought another tub of Sneak ",
    "At least two and a half before any permanent damage",
    "Just as a snack",
    "Poggers my dude",
    "Bishmallah",
    "Kanye",
    "Donda",
    "Kendrick is goated man",
    "Circle kick your balls",
    "What does batman like in his drinks",
    "That's a fuck you angle",
    "Sleeping schedule is so op man",
    "Shut the fuck up",
    "Cope",
    "Hold on guys I need to go cook some dinner",
    "That's a fuck you I'll see you at work angle",
    "https://media.discordapp.net/attachments/836408580944035881/1002301332599885874/FaceApp_1659030905335.jpg?width=503&height=676",
    "https://cdn.discordapp.com/attachments/836408580944035881/1002274706910625912/FaceApp_1659031305373.jpg",
    "https://cdn.discordapp.com/attachments/929078295327285308/987277939441795072/unknown.png",
    "https://cdn.discordapp.com/attachments/929078295327285308/987277939836084234/unknown.png",
    "https://cdn.discordapp.com/attachments/896806359075536987/1002396217407455272/unknown.png",
    "https://cdn.discordapp.com/attachments/896806359075536987/1002396368603729971/unknown.png",
    "https://cdn.discordapp.com/attachments/896806359075536987/1002397019547127828/unknown.png",
    "https://cdn.discordapp.com/attachments/896806359075536987/1002397109498155028/unknown.png",
    "https://cdn.discordapp.com/attachments/896806359075536987/1002397140003332187/unknown.png",
    "https://cdn.discordapp.com/attachments/896806359075536987/1002397171062165564/unknown.png",
    "https://cdn.discordapp.com/attachments/896806359075536987/1002397193434562560/unknown.png",
    "https://cdn.discordapp.com/attachments/929078295327285308/1003235340905086976/keito.jpg",
    "Forgor 💀",
    "E-E-E-E-E-E-E-E-E-",
    "Relax!",
    "Ba-boom",
    "Farting on my roommates door"
]

df = pd.DataFrame(keito)
df.to_csv('phrases.csv', index=False)
