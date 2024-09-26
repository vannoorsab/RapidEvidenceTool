import os
import shutil
import hashlib
import json
from datetime import datetime
import subprocess
import argparse

def collect_files(source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(destination_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def generate_report(evidence_list, report_path):
    report = {
        "timestamp": datetime.now().isoformat(),
        "evidence": evidence_list
    }
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)

def collect_event_logs(destination_dir):
    os.makedirs(destination_dir, exist_ok=True)
    command = 'wevtutil epl Application "' + os.path.join(destination_dir, 'ApplicationLog.evtx') + '"'
    subprocess.run(command, shell=True)

def main():
    parser = argparse.ArgumentParser(description='Rapid Evidence Acquisition Tool for Windows')
    parser.add_argument('source', help='Source directory to collect evidence from (e.g., C:\\Users\\USERNAME\\Documents)')
    parser.add_argument('destination', help='Destination directory to store evidence')
    
    args = parser.parse_args()
    
    collected_files = []
    collect_files(args.source, args.destination)
    
    for item in os.listdir(args.destination):
        file_path = os.path.join(args.destination, item)
        collected_files.append({
            "file_name": item,
            "hash": hash_file(file_path)
        })
    
    collect_event_logs(args.destination)
    generate_report(collected_files, os.path.join(args.destination, 'report.json'))

if __name__ == "__main__":
    main()
 
