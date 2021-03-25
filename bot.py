import discord
import translators as ts
import enchant
import json

with open('/home/ec2-user/creds/creds.json') as file:
    creds = json.load(file)

token = creds['Credentials']['Translator Bot']['Token']

enchant = enchant.Dict("en_US")

bot_owner = "LiquidLuck#9488"

client = discord.Client()

lang_map = {
    '🇪🇸' : 'es',
    '🇨🇳' : 'zh',
    '🇯🇵' : 'ja',
    '🇺🇸' : 'en'
}
user_default_lang_map = {
    'TheDenzel#2847'    : 'ja',
    'LiquidLuck#9488'   : 'es'
}

def translate(original_text:str, to_lang:str, from_lang:str = 'auto') -> dict:
    translated_text = ts.google(original_text, from_language=from_lang, to_language=to_lang)
    return {'lang' : to_lang, 'text' : translated_text}

def temp_error_handle() -> dict:
    return {'lang' : 'ES?', 'text' : 'Error translating to this language, likely gender-specific. Please check one of the others.'}

# Persist translation. Will not work across multiple instances.... Refactor.
def store_english_translation(english_text):
    data = {
        'english_translation' : english_text
    }
    with open('english_translation.json', 'w') as outfile:
        json.dump(data, outfile)
    outfile.close()

@client.event
async def on_message(message):

    author = str(message.author)
    channel = message.channel
    msg =  message.content.strip().lower()
    msg_tokens = msg.split()

    if author == str(client.user) and message.content != 'Please include a word after \'!ts\'.':
        await message.add_reaction('🇪🇸')
        await message.add_reaction('🇨🇳')
        await message.add_reaction('🇯🇵')
        await message.add_reaction('🇺🇸')
        return

    # Delete Error Message
    if message.content == 'Please include a word after \'!ts\'.':
        await message.delete(delay=5)

    if msg_tokens[0] == '!ts':

        if len(msg_tokens) == 1:
            await channel.send("Please include a word after \'!ts\'.")
        else:
            original_text = msg[len(msg_tokens)+1:]

            store_english_translation(translate(original_text=original_text, to_lang='en')['text']) 

            if not enchant.check(original_text):
                translated_text_json = translate(original_text=original_text, to_lang='en')
            else:
                try:
                    if author in user_default_lang_map.keys():
                        translated_text_json = translate(original_text, user_default_lang_map[author])
                    else:
                        translated_text_json = translate(original_text=original_text, to_lang='es')
                except:

            translated_text = translated_text_json['text']
            lang = translated_text_json['lang'].upper()

            await channel.send(f"{lang} - {translated_text}")
        
@client.event
async def on_reaction_add(reaction, user):
    if str(user) != 'Translator#5638' and str(reaction.message.author) == str(client.user):
        message = reaction.message.content.strip()
        msg_tokens = message.split('-')
        _text = msg_tokens[1].strip()
        lang = msg_tokens[0].strip().lower()

        english_text = ''
        with open('english_translation.json') as json_file:
            data = json.load(json_file)
            english_text = data['english_translation']
        json_file.close()

        translated_text_json = translate(original_text=english_text, to_lang=lang_map[str(reaction)], from_lang='en')

        translated_text = translated_text_json['text']
        lang = translated_text_json['lang'].upper()
        message = f"{lang} - {translated_text}"

        await reaction.message.remove_reaction(reaction, user)
        await reaction.message.edit(content=message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# client.run(token)

client.run(token)