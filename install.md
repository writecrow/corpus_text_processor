
# Windows Build

1. Set the GUI to PySimpleGUI instead of PySimpleGUIQt in CorpusTextProcessor.py
(This GUI is lighter weight; the latter is required only for correct display on MacOS)

2. Build the executable

```
rm -r build; rm -r dist; pyinstaller --onefile -wF --noconsole CorpusTextProcessor.py --icon=crow.ico --log-level=WARN
```

3. Sign the executable
We currently use a certificate purchased through DigiCert. The certificate is owned by John Mark Fullmer, and must be shared by that account if another computer is to be used for digital signing. Once the certificate is installed on a computer, you can then easily sign the executable using DigiCert's own [DigiCertUtil application](https://www.digicert.com/util/).

# MacOS Build

References:
- https://github.com/The-Nicholas-R-Barrow-Company-LLC/python3-pyinstaller-base-app-codesigning
- https://gist.github.com/txoof/0636835d3cc65245c6288b2374799c43
- https://github.com/pyinstaller/pyinstaller/wiki/How-to-Report-Bugs#make-sure-everything-is-packaged-correctly

Here is my brief mental model for signing & notarization for MacOS: You have an application. You want to bundle it into an installable package on Mac. For security reasons, Mac wants you to be able to identify who created the application, as well as the installer. The way this is done, first, is through certificates. One certificate is bundled with the application, another with the installer. Finally, you need to notarize the application, in which the actual code is uploaded to Apple. This can only be done through the Apple Developer account, using an application-specific password.

1. You can create certificates in the Apple Developer portal, https://developer.apple.com/account/resources/certificates/list .
2. Then you need to be able to have those certificates available on your local machine for the build. You can do this by downloading the certificate and then double-clicking on it, which adds it to your keychain. You can verify it is there by finding it in the "Keychain Access" application, and verify it is valid by running `security find-identity -p basic` on the command line. You can also import these certificates into XCode, though you don't need to for the method described below. The advantage of importing them in XCode is you can see additional information about the certificate validity (under "Accounts" > "Manage Certificates").

## Build steps, MacOS

1. Update the Info.plist version
- https://pythonhosted.org/PyInstaller/spec-files.html#spec-file-options-for-a-mac-os-x-bundle

2. Create a distributable application

```
rm -rf build/ dist/ && pyinstaller --onefile --windowed --noupx --osx-bundle-identifier=org.writecrow.corpustextprocessor -n "Corpus Text Processor" --icon=crow.icns CorpusTextProcessor.py && cp Info.plist dist/Corpus\ Text\ Processor.app/Contents/
```

3. Add a certificate to the application
-  https://github.com/pyinstaller/pyinstaller/issues/4629)
- Hash can be found with `security find-identity -p basic`
- This will prompt you for your **system/computer** password

```
codesign --deep --force --options=runtime --entitlements ./entitlements.plist --sign "HASH OF Developer ID Installer" --timestamp dist/Corpus\ Text\ Processor.app/
```

4. Verify the signature

```
codesign --verify --deep --strict --verbose=2 dist/Corpus\ Text\ Processor.app/
```

Expected output:
```
dist/Corpus Text Processor.app/: valid on disk
dist/Corpus Text Processor.app/: satisfies its Designated Requirement
```

5. Build the .pkg (change version below!)

```
rm -rf Mac/ && mkdir Mac/ && mv dist/Corpus\ Text\ Processor.app Mac/ && pkgbuild --root Mac --identifier "org.writecrow.corpustextprocessor" --version 1.0.10 --install-location /Applications CorpusTextProcessor.pkg && rm -rf build/ dist/ Mac/
```

6. Embed a certificate in the package
- https://simplemdm.com/certificate-sign-macos-packages/)
- Hash can be found with `security find-identity -p basic`

```
productsign --sign "HASH OF Developer ID Installer: John Fullmer" CorpusTextProcessor.pkg MAC_CorpusTextProcessor.pkg
```

Expected output:
```
productsign: using timestamp authority for signature
productsign: adding certificate "Developer ID Certification Authority"
productsign: adding certificate "Apple Root CA"
productsign: Wrote signed product archive to MAC_CorpusTextProcessor.pkg
```

7. Notarize the .pkg (takes a few minutes to run)

- https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution
- **Note:** altool has been deprecated and, starting in fall 2023, will no longer be supported by the Apple notary service. You should start using notarytool to notarize your software.
- The password is app-specific, locatable at https://appleid.apple.com/account/manage. If there is a 1048 error, see https://developer.apple.com/forums/thread/117351
- You should get an email within a few minutes if it was successfully notarized.

```
xcrun altool --notarize-app --primary-bundle-id "org.writecrow.corpustextprocessor" --username "mfullmer@gmail.com" --password "" --file MAC_CorpusTextProcessor.pkg
```

8. Check notarization
xcrun altool --notarization-history 0 --username "mfullmer@gmail.com" --password ""

9. Get failed notification debug URL:
xcrun altool --notarization-info NNN -u "mfullmer@gmail.com"
