echo "Enter the version number for this release:"
read VERSION

rm -rf build/ dist/ && pyinstaller --onefile --windowed --noupx --osx-bundle-identifier=org.writecrow.corpustextprocessor -n "Corpus Text Processor" --icon=crow.icns CorpusTextProcessor.py && cp Info.plist dist/Corpus\ Text\ Processor.app/Contents/

codesign --deep -vvv -s "Developer ID Application: John Fullmer" --entitlements entitlements.plist -o runtime dist/Corpus\ Text\ Processor.app/ --timestamp

codesign -v dist/Corpus\ Text\ Processor.app/

rm -rf Mac/ && mkdir Mac/ && mv dist/Corpus\ Text\ Processor.app Mac/ && pkgbuild --root Mac --identifier "org.writecrow.corpustextprocessor" --version $VERSION --install-location /Applications CorpusTextProcessor.pkg && rm -rf build/ dist/ Mac/

productsign --sign "Developer ID Installer: John Fullmer" CorpusTextProcessor.pkg MAC_CorpusTextProcessor.pkg

xcrun altool --notarize-app --primary-bundle-id "org.writecrow.corpustextprocessor" --username "mfullmer@gmail.com" --password "" --file MAC_CorpusTextProcessor.pkg
