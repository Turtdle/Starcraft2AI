import Bot
import os
def test(epoch):
    for i in range(0,100):
        try:
            Bot.run_bot_from_file("saves" + epoch + "/MakeMoney" + str(i) + ".h5", i, epoch)
        except Exception as e:
            Bot.run_bot_from_file("saves" + epoch + "/MakeMoney" + str(i) + ".h5", i, epoch)
            print(e)
            continue

    for i in range(3):
        for i in range(0,100):
            #checks if there is a file saves3/MakeMoneyi.txt
            #if there isnt, it will run the bot and create one
            if not os.path.exists("saves" + epoch + "/MakeMoney" + str(i) + ".txt"):
                Bot.run_bot_from_file("saves" + epoch + "/MakeMoney" + str(i) + ".h5", i, epoch)

