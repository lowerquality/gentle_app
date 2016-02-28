python vendor/pyinstaller/pyinstaller.py gentle.spec

# For unknown reasons, pyinstaller is not copying the `data' directory
# HACK: manually insert from the .app bundle

cp -r data dist/gentle.app/Contents/Resources

hdiutil create dist/gentle.dmg -volname "Gentle" -srcfolder dist/gentle.app/
