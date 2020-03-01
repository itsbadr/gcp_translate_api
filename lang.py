from google.cloud import vision, translate_v2 as translate

import io
import json
import requests

import discord
from discord.ext import commands

client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
bot = commands.Bot(command_prefix='`')

# languages.json file with key (countries) and their value (ISO-3166 country codes) pairs.

def iso(lang):
    with open('languages.json', 'r') as file:
        languages = json.load(file)
        for language in languages:
            if language.get('code') == lang:
                return language.get('name')
    return None
    

@bot.command()
async def lang(ctx):

    """          Gets the text and detects language        """
    
    text = ctx.message.content[5:]
    lang = translate_client.detect_language(text)
    language = lang.get('language')
    
    
    """          Translates the language back to target_language (English)      """
    
    
    await ctx.send(f'ISO 639-1 code: `{language}`\nLanguage name: `{iso(language)}`')
    translated = translate_client.translate(text, target_language='en')
    translated_language = translated.get('translatedText')
    await ctx.send('Translated text: \n```{translated_language}```')
    

@bot.command()
async def get_image(ctx):
        messages = await ctx.channel.history(limit=5).flatten()
        for message in messages:
                if message.attachments:
                        request = requests.get(message.attachments[0].url, allow_redirects=False)
                        image = vision.types.Image(content=request.content)
                        response = client.label_detection(image=image)
                        labels = response.label_annotations
                        
                        features = []
                        
                        for label in labels:
                                features.append(label.description)
                        else:
                                pass
        await ctx.send('\n'.join(features))
        
bot.run('')