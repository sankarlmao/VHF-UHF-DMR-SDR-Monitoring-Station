import subprocess
import time
import sys
from datetime import datetime

# --- Configuration ---

# Replace these with your local frequencies (in Hz)
FREQUENCIES_TO_SCAN = [
    "460.100M",
    "460.250M",
    "460.375M",
    "460.500M",
    "155.8625M"
]

FREQ_CORRECTION_PPM = 0
SDR_GAIN = "35"
SAMPLE_RATE = "240k"

# DSD: -i - (read from stdin), -fa (auto-detect), -v 3 (verbose errors)
DSD_COMMAND = ["dsd", "-i", "-", "-fa", "-v", "3"]

LOG_FILE = "activity.log"

# --- End Configuration ---

def create_rtl_fm_command():
    """Builds the rtl_fm command string from the frequency list."""
    cmd = [
        "rtl_fm",
        "-M", "fm",
        "-s", SAMPLE_RATE,
        "-p", str(FREQ_CORRECTION_PPM),
        "-g", SDR_GAIN,
        "-E", "pad"
    ]
    cmd.extend(FREQUENCIES_TO_SCAN)
    return cmd

def log_message(message):
    """Logs a message to the console and a file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    
    print(formatted_message)
    
    try:
        with open(LOG_FILE, "a") as f:
            f.write(formatted_message + "\n")
    except IOError as e:
        print(f"Error writing to log file: {e}")

def main():
    """
    Main function to start and manage the SDR scanner.
    """
    try:
        rtl_fm_cmd = create_rtl_fm_command()
        log_message(f"Starting rtl_fm with command: {' '.join(rtl_fm_cmd)}")
        
        # Start rtl_fm, capturing its standard output
        rtl_proc = subprocess.Popen(rtl_fm_cmd, stdout=subprocess.PIPE)
        
        log_message(f"Starting DSD with command: {' '.join(DSD_COMMAND)}")
        
        # Start dsd, piping rtl_fm's output to its input
        # We capture dsd's standard error (stderr) to read its text output
        dsd_proc = subprocess.Popen(
            DSD_COMMAND, 
            stdin=rtl_proc.stdout, 
            stderr=subprocess.PIPE,
            text=True
        )

        log_message("--- Monitoring started ---")

        # Read output from DSD line by line
        for line in iter(dsd_proc.stderr.readline, ''):
            message = line.strip()
            if message:
                # Filter for interesting messages (e.g., DMR calls)
                if "DMR" in message or "Voice" in message:
                    log_message(f"DECODER: {message}")

    except FileNotFoundError as e:
        log_message(f"ERROR: Process not found. Is 'rtl_fm' or 'dsd' installed and in your PATH?")
        log_message(e)
    except KeyboardInterrupt:
        log_message("--- Monitoring stopped by user ---")
    except Exception as e:
        log_message(f"An unexpected error occurred: {e}")
    finally:
        # Clean up processes
        if 'rtl_proc' in locals() and rtl_proc.poll() is None:
            rtl_proc.terminate()
        if 'dsd_proc' in locals() and dsd_proc.poll() is None:
            dsd_proc.terminate()
        log_message("--- Processes cleaned up. Exiting. ---")

if __name__ == "__main__":
    main()

