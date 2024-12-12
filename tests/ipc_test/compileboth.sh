pyinstaller --onefile ./writer.py --distpath . --workpath ./.temp --name=app
gcc reader.c -o reader