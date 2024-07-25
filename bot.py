import discord
from discord.ext import commands
from datetime import datetime
from db import Journal_DB
from dotenv import load_dotenv
import os

db = Journal_DB()
load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True  
intents.messages = True  
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

@bot.command()
async def timekeeper(ctx, args=None):
    if args is None:
        await ctx.send('Please provide a number.')
        return
    try:
        loops = int(args)
        for i in range(loops):
            while True:
                await ctx.send(f'Entry {i+1}:\nDate:(MM/DD/YY)\nMinutes:\nDescription:\nCategory:1(HEALTH), 2(WORK), 3(Project), 4(EDUCATION), 5(READING), 6(HOBBY), 7(NETWORKING), 8(OTHER)\n(Comma Separated)')
                response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                data = response.content.split(',')
                
                # Validate input
                if len(data) != 4:
                    await ctx.send('Incomplete data. Please provide all required fields in the format: Date, Minutes, Description, Category.')
                    continue
                
                try:
                    date = datetime.strptime(data[0].strip(), "%m/%d/%y")
                    minutes = int(data[1].strip())
                    description = data[2].strip()
                    category = int(data[3].strip())
                    
                    # Ensure category is within the expected range
                    if category not in range(1, 9):
                        await ctx.send('Invalid category. Please provide a category number between 1 and 8.')
                        continue

                    data_entry = {
                        'date': date,
                        'minutes': minutes,
                        'description': description,
                        'category': category
                    }

                    db.insert('timekeeper', **data_entry)
                    await ctx.send(f'Entry {i+1} successfully added.')
                    break  # Exit the while loop to move to the next entry

                except ValueError as e:
                    await ctx.send(f'Invalid data format: {e}. Please ensure that date is in MM/DD/YY format and numbers are correctly provided.')
                    continue

    except ValueError:
        await ctx.send('Invalid argument. Please provide a number.')
        return
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')
        return
    
@bot.command()
async def journal(ctx, args=None):
    if args is None:
        await ctx.send('Please provide a number.')
        return
    try:
        loops = int(args)
        for i in range(loops):
            while True:
                await ctx.send(f'Entry{i+1}: Date:(MM/DD/YY)\nProductivity:(1-10)\nJournal:\n(Comma Separated)')
                response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                data = response.content
                data = data.split(',')

                if len(data) != 3:
                    await ctx.send('Incomplete data. Please provide all required fields in the format: Date, Productivity, Journal.')
                    continue

                try:
                    date = datetime.strptime(data[0].strip(), "%m/%d/%y")
                    productivity = int(data[1].strip())
                    journal = data[2].strip()

                    if productivity not in range(1, 11):
                        await ctx.send('Invalid productivity. Please provide a number between 1 and 10.')
                        continue
                    data_entry = {
                        'date': date,
                        'productivity': productivity,
                        'journal': journal
                    }
                    db.insert('journal', **data_entry)
                    await ctx.send(f'Entry {i+1} successfully added.')
                    break
                except ValueError as e:
                    await ctx.send(f'Invalid data format: {e}. Please ensure that date is in MM/DD/YY format and numbers are correctly provided.')
                    continue

    except ValueError:
        await ctx.send('Invalid argument. Please provide a number.')
        return
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')
        return

@bot.command()
async def sleep(ctx, args=None):
    if args is None:
        await ctx.send('Please provide a number.')
        return
    try:
        loops = int(args)
        for i in range(loops):
            while True:
                await ctx.send(f'Entry{i+1}: Date Start:(MM/DD/YY)\nTime Start:(HH:MM)\nDate End:(MM/DD/YY)\nTime End(HH:MM)\nQuality:(1-10)\nNap:(Y/N)\n(Comma Separated)')
                response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                data = response.content
                data = data.split(',')

                if len(data) != 6:
                    await ctx.send('Incomplete data. Please provide all required fields in the format: Date Start, Time Start, Date End, Time End, Quality, Nap.')
                    continue

                try:
                    start_date = datetime.strptime(data[0].strip(), "%m/%d/%y")
                    start_time = datetime.strptime(data[1].strip(), "%H:%M")
                    combined_start = datetime.combine(start_date, start_time.time())
                    end_date = datetime.strptime(data[2].strip(), "%m/%d/%y")
                    end_time = datetime.strptime(data[3].strip(), "%H:%M")
                    combined_end = datetime.combine(end_date, end_time.time())

                    data_entry = {
                        'time_start': combined_start,
                        'time_end': combined_end,
                        'hours': (combined_end - combined_start).total_seconds() / 3600,
                        'quality': int(data[4].strip()),
                        'nap': data[5].strip()
                    }
                    db.insert('sleep', **data_entry)
                    await ctx.send(f'Entry {i+1} successfully added.')
                    break
                except ValueError as e:
                    await ctx.send(f'Invalid data format: {e}. Please ensure that date is in MM/DD/YY format and numbers are correctly provided.')
                    continue

    except ValueError:
        await ctx.send('Invalid argument. Please provide a number.')
        return
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')
        return

@bot.command()
async def exercise(ctx, args):
    if args is None:
        await ctx.send('Please provide a number.')
        return
    try:
        loops = int(args)
        for i in range(loops):
            while True: 
                await ctx.send(f'Entry{i+1}:\nDate\nExercise_Type:1(),2(),3(),4(),5(),6(),7(),8()\nDuration:\nEffort:\nReps:\nWeight:\nDistance:\nDescription\n(Comma Separated)')
                response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                data = response.content
                data = data.split(',')

                if len(data) != 8:
                    await ctx.send('Incomplete data. Please provide all required fields in the format: Date, Exercise_Type, Duration, Effort, Reps, Weight, Distance, Description.')
                    continue
                
                try:
                    date = datetime.strptime(data[0].strip(), "%m/%d/%y")
                    exercise_type = int(data[1].strip())
                    duration = data[2].strip()
                    effort = int(data[3].strip())
                    reps = int(data[4].strip())
                    weight = float(data[5].strip())
                    distance = float(data[6].strip())
                    description = data[7].strip()

                    data_entry = {
                        'date': date,
                        'exercise_type': exercise_type,
                        'duration': duration,
                        'effort': effort,
                        'reps': reps,
                        'weight': weight,
                        'distance': distance,
                        'description': description
                    }
                    db.insert('exercise', **data_entry)
                    await ctx.send(f'Entry {i+1} successfully added.')
                    break
                except ValueError as e:
                    await ctx.send(f'Invalid data format: {e}. Please ensure that date is in MM/DD/YY format and numbers are correctly provided.')
                    continue

    except ValueError:
        await ctx.send('Invalid argument. Please provide a number.')
        return
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')
        return
    
@bot.command()
async def nutrition(ctx, args):
    if args is None:
        await ctx.send('Please provide a number.')
        return
    try:
        loops = int(args)
        for i in range(loops):
            while True:
                await ctx.send(f'Entry{i+1}: Date:(MM/DD/YY)\nCalories:\nProtein:\nCarbs:\nFat:\nPints:\nAlcohol:\nFood Type:1(Small Meal), 2(Large Meal), 3(Snack), 4(Dessert), 5(Drink)\n(Comma Separated)')
                response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                data = response.content
                data = data.split(',')

                if len(data) != 8:
                    await ctx.send('Incomplete data. Please provide all required fields in the format: Date, Calories, Protein, Carbs, Fat, Pints, Alcohol, Food Type.')
                    continue
                
                try:
                    date = datetime.strptime(data[0].strip(), "%m/%d/%y")
                    calories = int(data[1].strip())
                    protein = int(data[2].strip())
                    carbs = int(data[3].strip())
                    fat = int(data[4].strip())
                    pints = int(data[5].strip())
                    alcohol = int(data[6].strip())
                    food_type = int(data[7].strip())

                    if food_type not in range(1, 6):
                        await ctx.send('Invalid food type. Please provide a number between 1 and 5.')
                        continue

                    data_entry = {
                        'date': date,
                        'calories': calories,
                        'protein': protein,
                        'carbs': carbs,
                        'fat': fat,
                        'pints': pints,
                        'alcohol': alcohol,
                        'food_type': food_type
                    }

                    db.insert('nutrition', **data_entry)
                    await ctx.send(f'Entry {i+1} successfully added.')
                    break
                except ValueError as e:
                    await ctx.send(f'Invalid data format: {e}. Please ensure that date is in MM/DD/YY format and numbers are correctly provided.')
                    continue

    except ValueError:
        await ctx.send('Invalid argument. Please provide a number.')
        return
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')
        return
    
@bot.command()
async def view(ctx, table):
    data = db.view(table)
    if data:
        for entry in data:
            entry_str = ', '.join([f'{key}: {value}' for key, value in zip(['id', 'date', 'minutes', 'description', 'category'], entry)])
            await ctx.send(entry_str)
    else:
        await ctx.send('No data found.')

@bot.command()
async def delete(ctx, table, id):
    db.delete(table, id)
    await ctx.send(f'Entry {id} deleted successfully.')


@bot.command()
async def update(ctx, table, id, **kwargs):
    db.update(table, id, **kwargs)
    await ctx.send(f'Entry {id} updated successfully.')

@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.event
async def on_message(message):
    if message.content == 'help':
        await message.channel.send('''Hello! I am the Ultimate Journal bot. 
                                   \nI am here to help you keep track of your time and activities. 
                                   \nHere are the commands you can use:
                                   \n$timekeeper #(number of entries): Use this command to keep track of your time and activities.
                                   \n$journal #(number of entries): Use this command to keep track of your daily journal entries.
                                   \n$sleep #(number of entries): Use this command to keep track of your sleep schedule.
                                   \n$exercise #(number of entries): Use this command to keep track of your exercise routine.
                                   \n$nutrition #(number of entries): Use this command to keep track of your nutrition intake.
                                   \n$view (table_name): Use this command to view the last 5 entries in a table.
                                   \n$clear #(number of messages): Use this command to clear the channel of messages.
                                   ''')

    await bot.process_commands(message)

bot.run(TOKEN)
