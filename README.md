# Software Stack (The "Software" Part)

This project is built on a few key open-source tools.

1. **`rtl-sdr` Package:**
   - Provides the `librtlsdr` driver and the essential `rtl_fm` command-line tool.
   - **Installation (Linux/Mac):** 
     ```bash
     sudo apt install rtl-sdr   # for Debian/Ubuntu
     brew install rtl-sdr       # for Mac
     ```

2. **`DSD` (Digital Speech Decoder):**
   - This is the core decoder for DMR, P25, and other digital voice modes.
   - **Installation:** You will likely need to build this from source.
     ```bash
     git clone https://github.com/szechyjs/dsd.git
     cd dsd
     mkdir build && cd build
     cmake ..
     make
     sudo make install
     ```

   - **Note:** `DSDPlus` is a popular (but closed-source, Windows-only) alternative with excellent performance. This project will use the open-source `DSD`.
