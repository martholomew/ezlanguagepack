#!/bin/python

import os
import sys
import json
import random
from os import listdir
from os.path import isfile, join
from pprint import pprint
import xml.etree.ElementTree as et


#popupKeyboard="@xml/popup_16keys_abc"


with open("lang_acc.json", "r") as f:
    langs = json.load(f)

pretty_language = sys.argv[1]
language = sys.argv[2]
language_short = sys.argv[3]

assert language in langs.keys()
print("noice")

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
    with open(keyboard, 'r') as f:
        xml = et.parse(f).getroot()
        for alpha in accents:
            for key in xml.iter('Key'):
                if key.attrib[codes] == alpha:
                    key.attrib[popup] = f"@xml/popup_{alpha}"
        try:
            os.mkdir(language)
        except OSError:
            pass
        new_keyboard = language + "/pack/src/main/res/xml/" + language + "_" + keyboard_type + ".xml"
        tree = et.ElementTree(xml)
        tree.write(new_keyboard, xml_declaration=True, encoding='utf-8')
        with open(new_keyboard, "r+") as s:
            data = s.read().replace("ns0", "android")
            s.seek(0)
            s.write(data)
            s.truncate()
    
    lang_short = language_short
    md5 = hex(random.getrandbits(128))[2:]
    md5 = md5[:8] + "-" + md5[8:12] + "-" + md5[12:16] + "-" + md5[16:20] + "-" + md5[20:]
    keyboard_xml = et.SubElement(keyboards_xml, 'Keyboard')
    keyboard_xml.set("nameResId", pretty_language + " " + keyboard_type)
    keyboard_xml.set("iconResId", "@drawable/ic_status_" + language)
    keyboard_xml.set("layoutResId", "@xml/" + language + "_" + keyboard_type)
    keyboard_xml.set("id", md5)
    keyboard_xml.set("defaultDictionaryLocale", lang_short)
    keyboard_xml.set("description", pretty_language + " " + keyboard_type)
    keyboard_xml.set("index", str(index))

    index += 1
new_keyboards = language + "/pack/src/main/res/xml/" + language + "_" + "keyboards.xml"
tree = et.ElementTree(keyboards_xml)
tree.write(new_keyboards, xml_declaration=True, encoding='utf-8')

for alpha in accents:
    xml = et.Element('Keyboard')
    xml.set("xmlns:android", "http://schemas.android.com/apk/res/android")
    row = et.SubElement(xml, 'Row')
    for accent in accents[alpha]:
        et.SubElement(row, 'Key').set("android:codes", accent)
    new_popup = language + "/pack/src/main/res/xml/" + "popup_" + alpha + ".xml"
    tree = et.ElementTree(xml)
    tree.write(new_popup, xml_declaration=True, encoding='utf-8')
