# VHF/UHF/DMR SDR Monitoring Station

This project is a **software-defined radio (SDR) monitoring station** for scanning VHF, UHF, and Digital Mobile Radio (DMR) transmissions. It uses an RTL-SDR dongle, the `rtl_fm` utility, the DSD (Digital Speech Decoder) tool, and a Python script to tie it all together, parse the output, and log activity.

---

## Project Goal

- Scan a list of predefined frequencies.
- Detect analog (NFM) and digital (DMR) signals.
- For DMR, decode the metadata (Talkgroup, Radio ID, Slot).
- Log all activity to the console and a file.

---

## Architecture

The data flows through a simple pipeline:

[Hardware] -> [Scanner Tool] -> [Decoder Tool] -> [Python Script] -> [Log]


- **Hardware**: An RTL-SDR dongle and antenna capture the raw RF signals.
- **Scanner Tool (`rtl_fm`)**: Tunes and demodulates frequencies, outputting a raw audio stream.
- **Decoder Tool (DSD)**: Reads the raw audio, detects digital signals like DMR, decodes metadata, and optionally plays audio.
- **Python Script (`monitor.py`)**: Manages `rtl_fm` and `dsd` processes, pipes outputs, parses decoded metadata, and logs activity.
- **Log (`activity.log`)**: Simple text file where decoded metadata is written.

---

## Hardware Requirements

- **SDR (Software Defined Radio):**
  - *Starter*: RTL-SDR Blog V3 or V4 dongle (affordable option).
  - *Upgrade*: SDRplay RSPdx or Airspy R2 (higher performance and wider bandwidth).

- **Antenna**: 
  - Wideband scanner antenna (Discone recommended) or the dipole kit included with RTL-SDR.
  - *Note*: Antenna quality is critical for good reception.

---

## Software Stack

This project uses a few key open-source tools:

### rtl-sdr Package

Provides `librtlsdr` driver and the essential `rtl_fm` command-line tool.  

**Installation (Linux/Mac):**

```bash
sudo apt install rtl-sdr      # Linux
brew install rtl-sdr          # Mac


DSD (Digital Speech Decoder)

git clone https://github.com/szechyjs/dsd.git
cd dsd
mkdir build && cd build
cmake ..
make
sudo make install

```

