from pathlib import Path
import tempfile,shutil,subprocess,sys,os
HERE=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix="d0-ward-offline-") as t:
 root=Path(t)
 shutil.copytree(HERE/"OFFLINE_DEPENDENCY",root,dirs_exist_ok=True)
 shutil.copytree(HERE/"repo",root,dirs_exist_ok=True)
 subprocess.run([sys.executable,str(root/"02_REGISTRY/research/certificates/a4d_joint_lattice_ward_resonance_check.py")],cwd=root,check=True,env={**os.environ,"OPENBLAS_NUM_THREADS":"1","PYTHONDONTWRITEBYTECODE":"1"})
