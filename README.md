# Wimkit
Wimkit is a fantastic GUI WIM backup&restore tool which based on wimlib.

# Supported systems
Windows 7 ~ Windows 11(maybe Linux and macOS are supported,I haven't tried that), highly recommend 64 bit systems.

# How to build
Makesure that you've installed [Python 3.8+](https://python.org) and [Git](https://github.com/git-for-windows/git/releases/download/v2.52.0.windows.1/Git-2.52.0-64-bit.exe)

1.Build wimlib([Guide](https://github.com/chris1111/Wimlib-Imagex-Package))
```bash
mkdir -p WimlibDev && cd WimlibDev && git clone https://github.com/chris1111/Wimlib-Imagex-Package.git && ./Wimlib-Imagex-Package/Build-Package.tool
```

2.Rename "WimlibDev" to "wimlib"

3.Clone Wimkit project
```bash
git clone https://github.com/Infinity-Explorer/Wimkit.git
cd Wimkit
```

4.Install require Python packages
```bash
pip install pyqt6,psutil
```

5.Run mainUI.py and enjoy it :)

(Note: settings.py has got issuses, settings.txt created by it can't be identified by mainUI.py, it'll crash, I would fix that later.)

