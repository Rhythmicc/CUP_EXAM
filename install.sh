pyinstaller -F main.py
mv dist/* ./
rm *.spec
rm -rf dist/
rm -rf build/
