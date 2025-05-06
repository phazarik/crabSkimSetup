import os,sys
import subprocess

def download_file(fileName,outputdir):
    xrootd_path = f"root://cms-xrd-global.cern.ch/{fileName}"
    destination = f"{outputdir}"
    
    try:
        print(f"Downloading {xrootd_path} to {destination}")
        subprocess.run(["xrdcp", "-f", xrootd_path, destination], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to download {file_path}: {e}")

        
if __name__ == "__main__":
    
    fileName=sys.argv[1]
    outputdir=sys.argv[2]

    download_file(fileName,outputdir)
