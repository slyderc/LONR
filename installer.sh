#!/bin/bash
INSTALL_PACKAGE="sudo apt-get -y install"
PYTHON_PACKAGE="python3"
if [ -f /usr/bin/pacman ]; then
    INSTALL_PACKAGE="sudo pacman -S --noconfirm"
    PYTHON_PACKAGE="python"
fi

echo "## NOT READY FOR PRIME-TIME YET.  Please keep an eye on the Git repo"
echo "for further developments."
exit 1

$INSTALL_PACKAGE telnet
$INSTALL_PACKAGE $PYTHON_PACKAGE
$INSTALL_PACKAGE $PYTHON_PACKAGE-pip
$INSTALL_PACKAGE $PYTHON_PACKAGE-dateutil
$INSTALL_PACKAGE git-core
if [ ! -d /opt/lonr ]; then
    sudo useradd -d /opt/lonr/ lonr
    sudo git clone https://github.com/slyderc/lonr /opt/lonr
    chown -R lonr:lonr /opt/lonr
fi
if [ -d /etc/systemd/system ]; then
    sudo cp /opt/lonr/lonr.service /etc/systemd/system/lonr.service
    sudo systemctl daemon-reload
    sudo systemctl enable lonr
    sudo systemctl start lonr
fi
