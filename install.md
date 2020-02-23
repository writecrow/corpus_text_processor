## To build for MacOS:

1. Read first: 'Make sure everything is packaged correctly'
https://github.com/pyinstaller/pyinstaller/wiki/How-to-Report-Bugs#make-sure-everything-is-packaged-correctly

2. Update the Info.plist version
See https://pythonhosted.org/PyInstaller/spec-files.html#spec-file-options-for-a-mac-os-x-bundle

3. Initial build:
```
rm -rf build/ dist/ && pyinstaller --onefile --windowed --noupx --osx-bundle-identifier=CROW -n "Corpus Text Processor" --icon=default_icon.icns CorpusTextProcessor.py && cp Info.plist dist/Corpus\ Text\ Processor.app/Contents/
```

4. Code sign the app:
```
codesign -s "CROW" dist/Corpus\ Text\ Processor.app/
```

5. Build the .pkg
```
rm -rf Mac/ && mkdir Mac/ && mv dist/Corpus\ Text\ Processor.app Mac/ && pkgbuild --root Mac --identifier CROW --version 1.0.beta2 --install-location /Applications MAC_CorpusTextProcessor.pkg --sign "John Fullmer" && rm -rf build/ dist/ Mac/
```

6. Code sign the package
See also: https://simplemdm.com/certificate-sign-macos-packages/
```
productsign --sign "3rd Party Mac Developer Installer: John Fullmer (A57QZ4FF3C)" CorpusTextProcessor-unsigned.pkg CorpusTextProcessor.pkg
```

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
