brew install p7zip

cd vendor
curl -o ffmpeg.7z https://evermeet.cx/ffmpeg/ffmpeg-3.2.4.7z
curl -L -o sip.tar.gz https://downloads.sourceforge.net/project/pyqt/sip/sip-4.19/sip-4.19.tar.gz
curl -L -o pyqt.tar.gz https://downloads.sourceforge.net/project/pyqt/PyQt5/PyQt-5.7.1/PyQt5_gpl-5.7.1.tar.gz

7z e ffmpeg.7z
tar -xzvf sip.tar.gz
tar -xzvf pyqt.tar.gz

# There seem to be massive, unresolved System Integrity Protection issues on the latest OS X.

cd sip-4.19
python configure.py --bindir=/Users/rmo/Library/Python/2.7/bin \
    --incdir=/usr/local/include
    --sipdir=/Users/rmo/Library/Python/2.7/share/sip \
make
sudo make install
cd ..

# HACK: I needed to put "sip.h" from /usr/local/include in the /Applications/Xcode directory

cd PyQt-gpl-5.7.1
python configure.py --confirm-license --disable QtPositioning -q ~/Qt/5.7/clang_64/bin/qmake \
    --bindir=/Users/rmo/Library/Python/2.7/bin \
    --sipdir=/Users/rmo/Library/Python/2.7/share/sip
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
