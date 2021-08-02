## To build for MacOS:

1. Read first: 'Make sure everything is packaged correctly'
https://github.com/pyinstaller/pyinstaller/wiki/How-to-Report-Bugs#make-sure-everything-is-packaged-correctly

2. Update the Info.plist version
See https://pythonhosted.org/PyInstaller/spec-files.html#spec-file-options-for-a-mac-os-x-bundle

3. Initial build:
```
rm -rf build/ dist/ && pyinstaller --onefile --windowed --noupx --osx-bundle-identifier=org.writecrow.corpustextprocessor -n "Corpus Text Processor" --icon=crow.icns CorpusTextProcessor.py && cp Info.plist dist/Corpus\ Text\ Processor.app/Contents/
```

4. Code sign the app (see https://github.com/pyinstaller/pyinstaller/issues/4629)
```
codesign --deep -vvv -s "Developer ID Application: John Fullmer" --entitlements entitlements.plist -o runtime dist/Corpus\ Text\ Processor.app/ --timestamp

```

5. Verify the code signature (empty output = okay)
```
codesign -v dist/Corpus\ Text\ Processor.app/
```

5. Build the .pkg (change version below!)
```
rm -rf Mac/ && mkdir Mac/ && mv dist/Corpus\ Text\ Processor.app Mac/ && pkgbuild --root Mac --identifier "org.writecrow.corpustextprocessor" --version 1.0.4 --install-location /Applications CorpusTextProcessor.pkg && rm -rf build/ dist/ Mac/
```

6. Code sign the package (see https://simplemdm.com/certificate-sign-macos-packages/)
```
productsign --sign "Developer ID Installer: John Fullmer" CorpusTextProcessor.pkg MAC_CorpusTextProcessor.pkg
```

7. Notarize the .pkg (password is app-specific, at https://appleid.apple.com/account/manage; if there is a 1048 error, see https://developer.apple.com/forums/thread/117351)
xcrun altool --notarize-app --primary-bundle-id "org.writecrow.corpustextprocessor" --username "mfullmer@gmail.com" --password "" --file MAC_CorpusTextProcessor.pkg

8. Check notarization
xcrun altool --notarization-history 0 --username "mfullmer@gmail.com" --password ""

9. Get failed notification debug URL:
xcrun altool --notarization-info NNN -u "mfullmer@gmail.com"

## To build for Windows

0. Set the GUI to PySimpleGUI instead of PySimpleGUIQt in CorpusTextProcessor.py
(This GUI is lighter weight; the latter is required only for correct display on MacOS)

1. Build the executable

```
rm -r build; rm -r dist; pyinstaller --onefile -wF --noconsole CorpusTextProcessor.py --icon=crow.ico --log-level=WARN
```

2. Sign the executable
We currently use a certificate purchased through DigiCert. The certificate is owned by John Mark Fullmer, and must be shared by that account if another computer is to be used for digital signing. Once the certificate is installed on a computer, you can then easily sign the executable using DigiCert's own [DigiCertUtil application](https://www.digicert.com/util/).
