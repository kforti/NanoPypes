.. highlight:: shell

.. _install_albacore:

================
Install Albacore
================


Install Albacore
-----------------
First, Albacore must be installed on your system, which requires a license from Oxford Nanopore Technologies. If you’ve purchased a Nanopore sequencing device from ONT then you already have this license.\n

To install Albacore on your system, login to the ONT Community Portal and go the the downloads page: https://community.nanoporetech.com/downloads. The Albacore downloads are under Archived Software.\n

Nanopypes has only been tested on Mac and Linux. Download either the Mac software or Linux software for python 3.5 or above. This will download a .whl package that you can install with the following command from the directory containing the .whl::

    pip3 install --user <name_of_albacore_package.whl>

** Replace <name_of_albacore_package.whl> with the name of the downloaded .whl package. The --user command is necessary if you do not have sudo access.

Next, make sure that the albacore executable is properly added to your PATH. The name of the executable is::

    read_fast5_basecaller.py

It is likely located in::

    ~/.local/bin/.


