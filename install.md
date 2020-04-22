## To build for MacOS:

1. Read first: 'Make sure everything is packaged correctly'
https://github.com/pyinstaller/pyinstaller/wiki/How-to-Report-Bugs#make-sure-everything-is-packaged-correctly

2. Update the Info.plist version
See https://pythonhosted.org/PyInstaller/spec-files.html#spec-file-options-for-a-mac-os-x-bundle

3. Initial build:
```
rm -rf build/ dist/ && pyinstaller --onefile --windowed --noupx --osx-bundle-identifier=org.writecrow.corpustextprocessor -n "Corpus Text Processor" --icon=default_icon.icns CorpusTextProcessor.py && cp Info.plist dist/Corpus\ Text\ Processor.app/Contents/
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
rm -rf Mac/ && mkdir Mac/ && mv dist/Corpus\ Text\ Processor.app Mac/ && pkgbuild --root Mac --identifier "org.writecrow.corpustextprocessor" --version 1.0.1 --install-location /Applications CorpusTextProcessor.pkg && rm -rf build/ dist/ Mac/
```

6. Code sign the package (see https://simplemdm.com/certificate-sign-macos-packages/)
```
productsign --sign "Developer ID Installer: John Fullmer" CorpusTextProcessor.pkg MAC_CorpusTextProcessor.pkg
```

7. Notarize the .pkg (password is app-specific, at https://appleid.apple.com/account/manage)
xcrun altool --notarize-app --primary-bundle-id "org.writecrow.corpustextprocessor" --username "mfullmer@gmail.com" --password "" --file MAC_CorpusTextProcessor.pkg

8. Check notarization
xcrun altool --notarization-history 0 --username "mfullmer@gmail.com" --password ""

9. Get failed notification debug URL:
xcrun altool --notarization-info NNN -u "mfullmer@gmail.com"

## To build for Windows

```
rm -r build; rm -r dist; pyinstaller --onefile -wF --noconsole CorpusTextProcessor.py --icon=default_icon.ico
```

See https://docs.microsoft.com/en-us/windows/uwp/packaging/create-certificate-package-signing

```
New-SelfSignedCertificate -Type Custom -Subject "CN=WriteCrow, O=WriteCrow, C=US" -KeyUsage DigitalSignature -FriendlyName "Crow, the corpus & repository of writing" -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

$pwd = ConvertTo-SecureString -String <PASSWORD> -Force -AsPlainText
Export-PfxCertificate -cert "Cert:\CurrentUser\My\E47982D297DB2BD3A412B3FD3C96094A02F9202F" -FilePath C:\Users\mark\writecrow-cert.pfx -Password $pwd

SignTool sign /fd SHA256 /a /f C:\Users\mark\writecrow-cert.pfx /p <PASSWORD> dist\gui.exe
```
