import Bot

for i in range(0,100):
    try:
        Bot.run_bot_from_file("saves3/MakeMoney" + str(i) + ".h5", i)
    except Exception as e:
        Bot.run_bot_from_file("saves3/MakeMoney" + str(i) + ".h5", i)
        print(e)
        continue