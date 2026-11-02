"""Run portable mechanical acceptance checks without altering the delivered package."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    inventory = ROOT/'SHA256SUMS.json'
    errors, results = [], []
    if inventory.exists():
        for relative, digest in json.loads(inventory.read_text(encoding='utf-8')).items():
            path = ROOT/relative
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
                errors.append('Checksum mismatch or missing file: '+relative)
    manifest = json.loads((ROOT/'Integration/manifest.json').read_text(encoding='utf-8'))
    # Original validators write their own reports; isolate those writes.
    with tempfile.TemporaryDirectory(prefix='depression_knowledge_check_') as temp:
        copied = Path(temp)/'knowledge'
        shutil.copytree(ROOT,copied,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        jobs = [(module,[str(copied/module/'validate_package.py')]) for module in manifest['modules']]
        jobs.extend([
            ('graph',[str(copied/'Workflow/Interview_Graph/preview_graph.py'),'--validate']),
            ('measurement',['-m','unittest','discover','-s',str(copied/'Measurement'),'-p','test_measurement.py']),
            ('handoff',['-m','unittest','discover','-s',str(copied/'Integration'),'-p','test_handoff.py'])])
        for name,args in jobs:
            run = subprocess.run([sys.executable,*args],cwd=copied,capture_output=True,text=True,encoding='utf-8',errors='replace')
            result={'suite':name,'passed':run.returncode==0}
            if run.returncode:
                result['error']=(run.stdout+run.stderr)[-4000:]
                errors.append('Failed suite: '+name)
            results.append(result)
    report={'status':'PASS' if not errors else 'FAIL','suites':results,'errors':errors,
            'scope':'Integrity, original module fixtures, annotated-state routing, measurement and handoff mechanics. Not clinical or model validation.'}
    print(json.dumps(report,indent=2))
    return 1 if errors else 0

if __name__=='__main__':
    raise SystemExit(main())
