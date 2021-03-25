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

# Using this to store the original Enligsh Translation
class English_translation:
    english_translation = ''
    def __init__(self, english_translation):
        self.english_translation = english_translation
        print(self.english_translation)
    def get_english_translation(self):
        return self.english_translation
    def set_english_translation(self, english_translation):
        self.english_translation = english_translation

english_translation = English_translation('')


def translate(original_text:str, to_lang:str, from_lang:str = 'auto') -> dict:
    translated_text = ts.google(original_text, from_language=from_lang, to_language=to_lang)
    return {'lang' : to_lang, 'text' : translated_text}

@client.event
async def on_message(message):

    author = str(message.author)
    channel = message.channel
    msg =  message.content.strip().lower()
    msg_tokens = msg.split()

    if author == str(client.user):
        await message.add_reaction('🇪🇸')
        await message.add_reaction('🇨🇳')
        await message.add_reaction('🇯🇵')
        await message.add_reaction('🇺🇸')
        return
    
    if msg_tokens[0] == '!ts':
        original_text = msg[len(msg_tokens)+1:]

        english_translation.set_english_translation = translate(original_text=original_text, to_lang='en')['text']

        if not enchant.check(original_text):
            translated_text_json = translate(original_text=original_text, to_lang='en')
        else:
            if author in user_default_lang_map.keys():
                translated_text_json = translate(original_text, user_default_lang_map[author])
            else:
                translated_text_json = translate(original_text=original_text, to_lang='es')
            
        translated_text = translated_text_json['text']
        lang = translated_text_json['lang'].upper()

        await channel.send(f"{lang} - {translated_text}")
        
@client.event
async def on_reaction_add(reaction, user):
    print(english_translation.english_translation())
    if str(user) != 'Translator#5638' and str(reaction.message.author) == str(client.user):
        message = reaction.message.content.strip()
        msg_tokens = message.split('-')
        _text = msg_tokens[1].strip()
        lang = msg_tokens[0].strip().lower()

        translated_text_json = translate(original_text=english_translation.english_translation, to_lang=lang_map[str(reaction)], from_lang='en')

        translated_text = translated_text_json['text']
        lang = translated_text_json['lang'].upper()
        message = f"{lang} - {translated_text}"

        await reaction.message.remove_reaction(reaction, user)
        await reaction.message.edit(content=message)
        # print(lang_map[str(reaction)])


@client.event
async def on_ready():
    global _connected_guilds
    # bot_controls.start_bots()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# client.run(token)

client.run(token)