pip3 install -r requirements.txt
$(cat settings.env | awk '{ printf("export %s ", $0) }')
./locator.py
