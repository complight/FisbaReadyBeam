# Description
A libray to control the [Fisba ReadyBeam laser light sources](https://www.fisba.com/en/readybeam-multicolor-laser-module).
At this time, this code is only tested on an `Ubuntu 22.04` operating system.

## Getting Started

### Installing
For installing this library using the following syntax in a Linux shell:

```bash
git clone https://github.com/complight/FisbaReadyBeam.git
cd FisbaReadyBeam
pip3 install -e .
```

or

```bash
git clone https://github.com/complight/FisbaReadyBeam.git
cd FisbaReadyBeam
pip3 install -r requirements.txt
sudo python3 setup.py install
```

### Testing
For testing the library, you can use the following syntax in a Linux shell:

```bash
pytest
```

If you do not have `pytest` installed in your operating system, try installing via:

```bash
pip3 install pytest
```

### Issues, Bugs, Comments and suggestion
Please use the issues section of this repository to reach out to us regarding your comment on this library.
