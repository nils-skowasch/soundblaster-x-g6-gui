# SoundBlaster X G6 GUI

This project provides a Graphical User Interface (GUI) built with [wxPython](https://wxpython.org/) to control
the [SoundBlaster X G6](https://de.creative.com/p/sound-blaster/sound-blasterx-g6) device from Linux.
It uses the [hidapi](https://github.com/trezor/cython-hidapi) library and [libusb](https://github.com/libusb/libusb) to
communicate with the device.

![SoundBlaster X G6 GUI](https://raw.githubusercontent.com/nils-skowasch/soundblaster-x-g6-gui/main/doc/screenshot-gui.png)

## Features

- **Playback Control**: Toggle between Speakers and Headphones, set Direct Mode, and configure playback filters.
- **Audio Settings**: Adjust volume and mute status for playback and various mixer inputs (Line-In, External Mic,
  SPDIF-In).
- **SBX Effects**: Enable and configure Surround, Crystalizer, Bass, Smart Volume, and Dialog Plus effects.
- **Recording Settings**: Manage microphone boost, voice clarity features (Noise Reduction, AEC, Smart Volume), and Mic
  EQ.
- **Lighting Control**: Customize the RGB lighting or disable it entirely.
- **Decoder Settings**: Switch between Normal, Full, and Night decoder modes.

## Important Disclaimer

I developed this GUI to the best of my belief, and I use it myself to control my G6, and it works fine for me.
I read pretty often that you are able to damage or brick a USB device if you send faulty data to it.

That's why I want to point out, that you **USE THIS GUI AT YOUR OWN RISK**! I am not responsible for any damage to your
system or your device!

## Firmware version

This software is tested with a G6 having the **Firmware version:** `2.1.250903.1324`.

Make sure that you have the same version, since I do not know whether the USB specification may differ between the
versions. You are able to update your Firmware with
[SoundBlaster Command](https://support.creative.com/Products/ProductDetails.aspx?prodID=21383&prodName=Sound%20Blaster)
in Windows by using a [QEMU/KVM VM](https://virt-manager.org/) and the USB Redirection feature.

## System requirements

### Linux: Create udev-rule

In `/etc/udev/rules.d/` create a rule file as root (e.q. with name `50-soundblaster-x-g6.rules`) having the
following content:

```text
SUBSYSTEM=="usb", ATTRS{idVendor}=="041e", ATTRS{idProduct}=="3256", TAG+="uaccess"
```

```shell
# Add udev rule:
sudo cat > /etc/udev/rules.d/50-soundblaster-x-g6.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="041e", ATTRS{idProduct}=="3256", TAG+="uaccess"
EOF
```

This allows you (and the application) to access the USB device directly and is mandatory for the application to be  
able to send data to the device.

Apply the udev rules by issuing:

```shell
# Reload udev rules:
sudo udevadm trigger
```

### Linux: Create sudoers entry for reloading ALSA

To use the application with the `--reload-audio-services` option (if applicable, though primarily used by the CLI
backend), you may need to add the following line to your sudoers file:

```shell
# Add sudoers entry:
sudo cat > /etc/sudoers.d/50-soundblaster-x-g6 << EOF
<username> ALL=(ALL:ALL) NOPASSWD: /usr/sbin/alsa force-reload
EOF
```

Replace `<username>` with your actual username. This allows the application (on your behalf) to reload the ALSA services
without entering your password.

### Linux: Install libusb1

The following libusb packages are required:

```txt
libusb-1.0-0-dev/jammy-updates,now 2:1.0.25-1ubuntu2 amd64 [installed]
libusb-1.0-0/jammy-updates,now 2:1.0.25-1ubuntu2 amd64 [installed]
```

```shell
sudo apt-get -y install libusb-1.0-0-dev libusb-1.0-0 
```

### Windows: Add libusb-1.0.dll to %PATH%

Download the package [libusb](https://pypi.org/project/libusb/#files) from Pypi (version `1.0.27`) and add the
following DLL file to your `%PATH%` variable:
`/libusb-1.0.27/src/libusb/_platform/_windows/x64/libusb-1.0.dll`

This is required to let the application use libusb in the backend.

## Installation

### Via pipx package (recommended)

To install the GUI tool using `pipx`, run:

```shell
pipx install soundblaster-x-g6-gui
```

The soundblaster-x-g6-gui package is installed in `~/.local/share/pipx/venvs/soundblaster-x-g6-gui/`.

The command `soundblaster-x-g6-gui` should now be available in your shell, otherwise you may have to add the
directory `~/.local/share/pipx/venvs/soundblaster-x-g6-gui/bin/` to your `$PATH` variable.

Note that you still need to create the **udev rule** and create a **sudoers entry** as described above!

#### Conclusion

The installation is complete, and you can start the GUI by running:

```shell
soundblaster-x-g6-gui
```

### Manual installation (from source)

This section describes how to use the program from source. It contains the following steps:

- clone the repository
- install Python 3.12
- install wxPython
- create a venv and download dependencies using pip

#### Clone repository:

Select a directory of your choice and clone the repository into it:

```shell
(cd $HOME; git clone git@github.com:nils-skowasch/soundblaster-x-g6-gui.git)
```

This should create the directory `~/soundblaster-x-g6-gui`, containing all files.

#### Install Python 3.12:

Install Python3.12. The application has been tested with **Python3.12** (LinuxMint 22.1).

```shell
sudo apt-get install Python3.12
```

#### Install wxPython

[Homepage](https://wxpython.org/pages/overview/#hello-world)
|
[API-Reference](https://docs.wxpython.org/)

```shell
# install wxPython dependencies
sudo apt install libgtk-3-dev libpython3.12-dev
# install wxPython via pip
source ~/development/workspaces/soundblaster-x-g6-gui/venv/bin/activate
## On work laptop, execute:
~/development/workspaces/soundblaster-x-g6-gui/venv/bin/python ~/development/pycharm-2024.3.5/plugins/python-ce/helpers/packaging_tool.py install wxPython
## On home laptop, execute:
~/development/git/soundblaster-x-g6-gui/venv/bin/python ~/development/jetbrains/pycharm-community-2024.1.2/plugins/python-ce/helpers/packaging_tool.py install wxPython
```

#### Create a virtual environment and download dependencies

Create a virtual environment and download the dependencies using pip:

```shell
# create virtual environment 'venv'
cd ~/soundblaster-x-g6-gui/
python -m venv venv

# install virtualenv package (if required) and activate 'venv'
pip install virtualenv
virtualenv venv
source venv/bin/activate

# install dependencies into 'venv'
pip install -r requirements.txt
```

#### Conclusion

The installation is complete, and you can start the GUI by running:

```shell
venv/bin/python src/g6_gui.py
```

## GUI usage

```text
usage: soundblaster-x-g6-gui [-h] [--dry-run] [--debug] [--version]

SoundBlaster X G6 GUI

options:
  -h, --help  show this help message and exit

General options:
  --dry-run   Used to verify the available hex_line files, without making any
              calls against the G6 device.
  --debug     Print communication data with the G6 device to the console.
  --version   show program's version number and exit
```

## Development

Before continuing this section, see the section **System requirements** and install the required system dependencies.

### Building the application

To build the application, run the following commands:

```shell
# builds the application into the dist/ directory
python -m build

# verifies the build
python -m twine check dist/*
```

### Deploying the application

Create a .pypirc file in your home directory with the following content:

```text
[testpypi]
  username = __token__
  password = <api-token>
```

Deploy the application on testpypi.org:

```shell
python -m twine upload --repository testpypi dist/* 
```

Download the application from testpypi.org and test it:

```shell
pipx install --pip-args="--index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple" soundblaster-x-g6-gui
```
