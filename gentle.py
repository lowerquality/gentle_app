#!/usr/bin/env python

import multiprocessing

multiprocessing.freeze_support()

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

import logging
import os
import tarfile
import tempfile
import threading
from twisted.internet import reactor
import urllib
import webbrowser
import sys

from gentle.__version__ import __version__
from gentle.util.paths import get_resource
import serve

def get_open_port(desired=0):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("",desired))
    except socket.error:
        return get_open_port(0)
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

PORT = get_open_port(8765)

# Start a thread for the web server.
webthread = threading.Thread(target=serve.serve, args=(PORT,))
webthread.start()

def open_browser():
    webbrowser.open("http://localhost:%d/" % (PORT))

def open_about():
    webbrowser.open("https://lowerquality.com/gentle")

dl = None
progress = None
fstpath = get_resource('exp/tdnn_7b_chain_online/graph_pp/HCLG.fst')

def download_full_language_model():
    global progress, dl

    fstdir = os.path.dirname(fstpath)

    try:
        os.makedirs(fstdir)
    except OSError:
        pass

    progress = QtWidgets.QProgressBar()
    progress.setRange(0, 100)
    
    trans.hide()
    layout.removeWidget(trans)

    dltxt = QtWidgets.QLabel('Downloading language model...')
    layout.addWidget(dltxt)
    
    layout.addWidget(progress)

    dl = DLThread()
    dl.start()

    dl.percent.connect(progress.setValue)
    dl.finished.connect(prompt_to_relaunch)

def prompt_to_relaunch():
    msg = QtWidgets.QMessageBox()
    msg.setText("Success! Relaunch Gentle to finish enabling transcription.")
    msg.exec_()
    quit_server()

class DLThread(QtCore.QThread):

    percent = pyqtSignal(int)
    
    def run(self):
        url = "https://lowerquality.com/gentle/aspire-hclg.tar.gz"
        CHUNK = 128 * 1024
        with tempfile.NamedTemporaryFile(suffix=".tar.gz") as fp:
            dl = urllib.request.urlopen(url)
            size = int(dl.headers['content-length'])
            cur_size = 0
            while True:
                buf = dl.read(CHUNK)
                if not buf:
                    break
                fp.write(buf)
                cur_size += len(buf)

                self.percent.emit(int(100 * (cur_size / float(size))))

            fp.seek(0)

            # done! uncompress to final location
            with open(fstpath, 'wb') as fstout:
                tar = tarfile.open(fp.name, 'r:gz')
                hclg = tar.extractfile("exp/tdnn_7b_chain_online/graph_pp/HCLG.fst")
                hclg_info = tar.getmember("exp/tdnn_7b_chain_online/graph_pp/HCLG.fst")
                cur_size = 0
                
                while True:
                    buf = hclg.read(CHUNK)
                    if not buf:
                        break
                    fstout.write(buf)

                    cur_size += len(buf)
                    self.percent.emit(int(100 * (cur_size / float(hclg_info.size)))) # !!!


app = QtWidgets.QApplication(sys.argv)

w = QtWidgets.QWidget()
w.resize(250, 150)
w.setWindowTitle('Gentle')

def quit_server():
    app.exit()

layout = QtWidgets.QVBoxLayout()
w.setLayout(layout)

txt = QtWidgets.QLabel('''Gentle v%s

A robust yet lenient forced-aligner built on Kaldi.''' % (__version__))
layout.addWidget(txt)

btn = QtWidgets.QPushButton('Open in browser')
btn.setStyleSheet("font-weight: bold;")
layout.addWidget(btn)
btn.clicked.connect(open_browser)

abt = QtWidgets.QPushButton('About Gentle')
layout.addWidget(abt)
abt.clicked.connect(open_about)

if not os.path.exists(fstpath):
    trans = QtWidgets.QPushButton('Enable full transcription')
    layout.addWidget(trans)
    trans.clicked.connect(download_full_language_model)

quitb = QtWidgets.QPushButton('Quit')
layout.addWidget(quitb)
quitb.clicked.connect(quit_server)

w.show()

w.raise_()
w.activateWindow()
 
app.exec_()

logging.info("Waiting for server to quit.")
reactor.callFromThread(reactor.stop)
webthread.join()
