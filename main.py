import discord
import translators as ts
import pprint

pp = pprint.PrettyPrinter(indent=4)

pp.pprint(ts.google('teacher', from_language='en', to_language='es', is_detail_result=False))

pp.pprint(ts.google('the teacher', from_language='en', to_language='es', is_detail_result=False))

# pp.pprint(ts.deepl('teacher', from_language='en', to_language='es', is_detail_result=False))