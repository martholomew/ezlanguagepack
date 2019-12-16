#!/bin/python

import os
import sys
import json
import random
from os import listdir
from os.path import isfile, join
from pprint import pprint
import xml.etree.ElementTree as et


with open("lang_acc.json", "r") as f:
    langs = json.load(f)

language = sys.argv[1]
pretty_language = language.title()
language_short = sys.argv[2]

assert language in langs.keys()

accents = langs[language]

latin_dir = "latin_keyboards"
keyboards = [join(latin_dir, f) for f in listdir(latin_dir) if isfile(join(latin_dir, f))]

schema = '{http://schemas.android.com/apk/res/android}'
codes = schema + "codes"
popup = schema + "popupKeyboard"
index = 1
keyboards_xml = et.Element('Keyboards')
for keyboard in keyboards:
    keyboard_type = keyboard.split('/')[1].split('_')[1].split('.')[0]
    keyboard_type_pretty = keyboard_type.title()
    with open(keyboard, 'r') as f:
        xml = et.parse(f).getroot()
        for alpha in accents:
            for key in xml.iter('Key'):
                if key.attrib[codes] == alpha:
                    key.attrib[popup] = f"@xml/popup_{alpha}"

        new_keyboard = f"{language}/pack/src/main/res/xml/{language}_{keyboard_type}.xml"
        tree = et.ElementTree(xml)
        tree.write(new_keyboard, xml_declaration=True, encoding='utf-8')
        with open(new_keyboard, "r+") as s:
            data = s.read().replace("ns0", "android")
            s.seek(0)
            s.write(data)
            s.truncate()
    
    lang_short = language_short
    md5 = hex(random.getrandbits(128))[2:]
    md5 = f"{md5[:8]}-{md5[8:12]}-{md5[12:16]}-{md5[16:20]}-{md5[20:]}"
    keyboard_xml = et.SubElement(keyboards_xml, 'Keyboard')
    keyboard_xml.set("nameResId", f"{pretty_language} {keyboard_type_pretty}")
    keyboard_xml.set("iconResId", f"@drawable/ic_status_{language}")
    keyboard_xml.set("layoutResId", f"@xml/{language}_{keyboard_type}")
    keyboard_xml.set("id", md5)
    keyboard_xml.set("defaultDictionaryLocale", lang_short)
    keyboard_xml.set("description", f"{pretty_language} {keyboard_type_pretty}")
    keyboard_xml.set("index", str(index))

    index += 1

new_keyboards = f"{language}/pack/src/main/res/xml/{language}_keyboards.xml"
tree = et.ElementTree(keyboards_xml)
tree.write(new_keyboards, xml_declaration=True, encoding='utf-8')

for alpha in accents:
    xml = et.Element('Keyboard')
    xml.set("xmlns:android", "http://schemas.android.com/apk/res/android")
    row = et.SubElement(xml, 'Row')
    for accent in accents[alpha]:
        et.SubElement(row, 'Key').set("android:codes", accent)
    new_popup = language + f"/pack/src/main/res/xml/{language}_popup_{alpha}.xml"
    tree = et.ElementTree(xml)
    tree.write(new_popup, xml_declaration=True, encoding='utf-8')

md5 = hex(random.getrandbits(128))[2:]
md5 = md5[:8] + "-" + md5[8:12] + "-" + md5[12:16] + "-" + md5[16:20] + "-" + md5[20:]
dictionaries_xml = et.Element('Dictionaries')
dicitonary_xml = et.SubElement(dictionaries_xml, "Dictionary")
dicitonary_xml.set("autoTextResourceId", f"@xml/{language}_autotext")
dicitonary_xml.set("description", f"{pretty_language} Dictionary")
dicitonary_xml.set("dictionaryResourceId", f"@array/{language}_words_dict_array")
dicitonary_xml.set("id", md5)
dicitonary_xml.set("locale", language_short)
dicitonary_xml.set("nameResId", f"{pretty_language} Dictionary")
dicitonary_xml.set("type", "binary_resource")
new_dictionaries = f"{language}/pack/src/main/res/xml/{language}_dictionaries.xml"
tree = et.ElementTree(dictionaries_xml)
tree.write(new_dictionaries, xml_declaration=True, encoding='utf-8')
