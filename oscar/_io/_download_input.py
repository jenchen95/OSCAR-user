"""
OSCAR Data Downloader
Handles the retrieval of the heavy scientific library from Zenodo.
"""
import zipfile
import requests
from .paths import get_in_dir  # Use the helper we built
from .._utils.load_config import load_config

def download_data(input_dir=None):
    """
    Initial setup: Downloads the complete input_data library from Zenodo.
    
    Args:
        input_dir (str or Path, optional): Custom path to store the library. 
                                           Defaults to PACKAGE_ROOT/data/input_data.
    """
    # 1. Load Zenodo URL from config
    config = load_config()
    url = config['paths']['zenodo_base_url']
    
    # 2. Resolve the target directory
    # If input_dir is None, get_in_dir() returns the default data/input_data
    target_dir = get_in_dir(input_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Place the temporary zip file in the parent of the target folder
    zip_path = target_dir.parent / "input_data.zip"
    
    print(f"Downloading OSCAR Input Library to: {target_dir}")
    print(f"Source URL: {url}")
    
    # 3. Download logic
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() # Check for download errors
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        # 4. Extraction
        print(f"Extracting files into {target_dir.parent}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # zip_ref.extractall(target_dir.parent) 
            # Note: Ensure your Zip file internal structure matches the target
            zip_ref.extractall(target_dir.parent)
            
        print("Setup complete. You can now run the model offline.")

    except Exception as e:
        print(f"Error during download: {e}")
    
    finally:
        # 5. Clean up the zip file even if it fails
        if zip_path.exists():
            zip_path.unlink()