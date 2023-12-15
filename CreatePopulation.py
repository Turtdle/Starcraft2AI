import Bot

for i in range(0,100):
    try:
        Bot.run_bot(i)
    except Exception as e:
        print(e)
        continue