#!/bin/bash

language="$1"
short="$2"

pretty=$(echo -n "${language^}")

cp -R LANGUAGE_NAME/ $language/

find $language/. -type f -exec sed -i "s/PRETTY_NAME/"$pretty"/g" {} +
find $language/. -type f -exec sed -i "s/LANGUAGE_NAME/"$language"/g" {} +
find $language/. -type f -exec sed -i "s/LANGUAGE_SHORT/"$short"/g" {} +

mv $language/pack/src/main/java/com/anysoftkeyboard/languagepack/LANGUAGE_NAME $language/pack/src/main/java/com/anysoftkeyboard/languagepack/$language
mv $language/pack/src/main/res/values/LANGUAGE_NAME_pack_strings.xml $language/pack/src/main/res/values/"$language"_pack_strings.xml
mv $language/pack/src/main/res/values/LANGUAGE_NAME_pack_strings_dont_translate.xml $language/pack/src/main/res/values/"$language"_pack_strings_dont_translate.xml
mv $language/pack/src/main/res/xml/LANGUAGE_NAME_autotext.xml $language/pack/src/main/res/xml/"$language"_autotext.xml

echo "/apk/flag   add flag"
echo "/pack/dictionary    add dictionaries"
echo "/pack/src/main/res/values    change values(if necessary)"
echo "If not using the python script:"
echo "Replace MD5SUMHERE in /pack/src/main/res/xml/"$language"_keyboards"
echo "Replace MD5SUMHERE in /pack/src/main/res/xml/"$language"_dictionaries"
echo "Copy the folder into addons/languages."
echo "Add language to the end of settings.gradle."
echo "Do the commands below:"
echo "./gradlew :languages:$language:pack:generateLanguagePackIcons :languages:$language:apk:generateStoreLogoIcon"
echo "./gradlew :languages:$language:apk:assembleDebug"
echo "Test the keyboard, and get your screenshots to add here:"
echo "/apk/src/main/play/listings/en-US/graphics/screenshots"
echo "Push n Pull."
