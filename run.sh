#!/bin/bash
echo -n "Pretty Name: "
read pretty
echo -n "Un-Pretty Name: "
read language
echo -n "ISO 639-1: "
read short

mv LANGUAGE_NAME $language

find $language/. -type f -exec sed -i "s/PRETTY_NAME/"$pretty"/g" {} +
find $language/. -type f -exec sed -i "s/LANGUAGE_NAME/"$language"/g" {} +
find $language/. -type f -exec sed -i "s/LANGUAGE_SHORT/"$short"/g" {} +

mv $language/pack/src/main/java/com/anysoftkeyboard/languagepack/LANGUAGE_NAME $language/pack/src/main/java/com/anysoftkeyboard/languagepack/$language
mv $language/pack/src/main/res/values/LANGUAGE_NAME_pack_strings.xml $language/pack/src/main/res/values/"$language"_pack_strings.xml
mv $language/pack/src/main/res/values/LANGUAGE_NAME_pack_strings_dont_translate.xml $language/pack/src/main/res/values/"$language"_pack_strings_dont_translate.xml
mv $language/pack/src/main/res/xml/LANGUAGE_NAME_autotext.xml $language/pack/src/main/res/xml/"$language"_autotext.xml
mv $language/pack/src/main/res/xml/LANGUAGE_NAME_dictionaries.xml $language/pack/src/main/res/xml/"$language"_dictionaries.xml
mv $language/pack/src/main/res/xml/LANGUAGE_NAME_keyboards.xml $language/pack/src/main/res/xml/"$language"_keyboards.xml
mv $language/pack/src/main/res/xml/LANGUAGE_NAME_physical.xml $language/pack/src/main/res/xml/"$language"_physical.xml

echo "/apk/flag   add flag"
echo "/pack/dictionary    add dictionaries"
echo "/pack/src/main/res/values    change values(if necessary)"
echo "/pack/src/main/res/xml   add keyboards etc"
echo "/pack/src/main/res/xml/"$language"_dictionaries.xml   https://www.guidgenerator.com/online-guid-generator.aspx"
echo "/pack/src/main/res/xml/"$language"_keyboards.xml  https://www.guidgenerator.com/online-guid-generator.aspx"
echo "Copy the folder into LanguagePack/languages."
echo "Do the commands below:"
echo "./gradlew :languages:$language:pack:generateLanguagePackIcons :languages:$language:apk:generateStoreLogoIcon"
echo "./gradlew :languages:$language:apk:assembleDebug"
echo "Test the keyboard, and get your screenshots to add here:"
echo "/apk/src/main/play/listings/en-US/graphics/screenshots"
echo "Push n Pull."
