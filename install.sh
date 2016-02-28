brew install p7zip

cd vendor
curl -o ffmpeg.7z https://evermeet.cx/ffmpeg/ffmpeg-78833-g67f8a0b.7z
curl -o sip.tar.gz http://sourceforge.net/projects/pyqt/files/sip/sip-4.17/sip-4.17.tar.gz
curl -o pyqt.tar.gz http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt-gpl-5.5.1.tar.gz

7z e ffmpeg.7z
tar -xzvf sip.tar.gz
tar -xzvf pyqt.tar.gz

cd sip-4.17
python configure.py
make
sudo make install
cd ..

cd PyQt-gpl-5.5.1
python configure.py --disable QtPositioning --confirm-license -q ~/Qt/5.5/clang_64/bin/qmake
make
sudo make install
cd ../..

git submodule init
git submodule update

cd vendor/gentle
git submodule init
git submodule update

sh install.sh

cd ../..

python vendor/pyinstaller/pyinstaller.py --windowed -y gentle.spec
