import subprocess
import json
import os,argparse

def get_subdatasets(dataset):
    """
    Use dasgoclient to list all subdatasets for the specified dataset pattern.
    """
    try:
        # Query DAS for subdatasets
        result = subprocess.check_output(
            ["dasgoclient", "-query", f"dataset={dataset}", "-json"],
            text=True
        )
        subdatasets = [entry['dataset'][0]['name'] for entry in json.loads(result)]
        return subdatasets
    except subprocess.CalledProcessError as e:
        print(f"Failed to query subdatasets: {e}")
        return []

def get_files(subdataset):
    """
    Use dasgoclient to list all files in a specific subdataset.
    """
    try:
        # Query DAS for files in the subdataset
        result = subprocess.check_output(
            ["dasgoclient", "-query", f"file dataset={subdataset}", "-json"],
            universal_newlines=True
        )
        files = [entry['file'][0]['name'] for entry in json.loads(result)]
        return files
    except subprocess.CalledProcessError as e:
        print(f"Failed to query files for {subdataset}: {e}")
        return []

def download_files(files, subdataset_dir):
    """
    Download each file using xrdcp to the specific subdataset directory.
    """
    for file_path in files:
        xrootd_path = f"root://cms-xrd-global.cern.ch/{file_path}"
        destination = os.path.join(subdataset_dir, os.path.basename(file_path))
        try:
            print(f"Downloading {xrootd_path} to {destination}")
            subprocess.run(["xrdcp", "-f", xrootd_path, destination], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to download {file_path}: {e}")


def show_subdataset_files(subdataset,fileN):
    files = get_files(subdataset)
    if not files:
        print(f"No files found for subdataset {subdataset}.")
    else:
        print(f"Found {len(files)} files. Starting download...")
        for count,f in enumerate(files[:fileN]):            
            print(f'{count+1}: {f}')

            
def download_subdataset_from_dataset(args):

    dataset =args.dataset
    main_dir=args.maindir
    fileN=args.fileN
    get_download=args.download

    #Step 1: Ensure the main directory exists
    os.makedirs(main_dir, exist_ok=True)
    
    #Step 2: Get all subdatasets
    subdatasets = get_subdatasets(dataset)
    
    if not subdatasets:
        print("No subdatasets found for the specified dataset pattern.")
    else:
        print(f"Found {len(subdatasets)} subdatasets. Processing each one...")

        #Step 3: Process each subdataset
        for subdataset in subdatasets:
            print(f"\nProcessing subdataset: {subdataset}")

            #Create a directory for the subdataset
            subdataset_dir = os.path.join(main_dir, subdataset.replace('/', '_'))
            os.makedirs(subdataset_dir, exist_ok=True)

            # Step 4: Get files in the current subdataset
            files = get_files(subdataset)
            
            if not files:
                print(f"No files found for subdataset {subdataset}.")
            else:
                print(f"Found {len(files)} files. Starting download...")

                for count,f in enumerate(files[:fileN]):
                    print(f'{count+1}: {f}')
                    
                # Step 5: Download each file into the subdataset directory
                if(get_download):download_files(files[:fileN], subdataset_dir)
                print(f"Completed download for subdataset {subdataset}.")


def Argument_Parser():
    parser=argparse.ArgumentParser()
    parser.add_argument('-d','--dataset',type=str,required=True,help="dataset/subdataset name")
    parser.add_argument('-o','--maindir',type=str,required=True,help="output directory")
    parser.add_argument('-n','--fileN'  ,type=int,required=False,default=10000,help="number of files")
    parser.add_argument('-s','--download',type=bool,required=False,default=False,help="download the files")
    
    args=parser.parse_args()

    return args
                
            
if __name__ == "__main__":

    args=Argument_Parser()

    ##show files of a subdataset
    show_subdataset_files(subdataset=args.dataset,fileN=args.fileN)
    
    ##download subdataset of datasets
    #download_subdataset_from_dataset(args)
