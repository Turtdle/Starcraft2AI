import Bot

for i in range(87  ,88):
    try:
        Bot.run_bot(i)
    except Exception as e:
        print(e)
        continue