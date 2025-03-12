source ./venv/bin/activate
sudo rm -rf build dist
# to generate setup.py file:
# py2applet --make-setup WorkLog.py
sudo python3 setup.py py2app -A
sudo mv ./dist/WorkLog.app /Applications