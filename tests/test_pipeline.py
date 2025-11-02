import os
import subprocess
import sys
import tempfile


def test_train_creates_artifacts(tmp_path):
    outdir = tmp_path / "artifacts"
    outdir.mkdir()

    # Run the train CLI
    cmd = [sys.executable, "src/train.py", "--output-dir", str(outdir), "--version-file", str(tmp_path / 'version.txt')]
    # write an initial version file
    with open(tmp_path / 'version.txt', 'w', encoding='utf-8') as f:
        f.write('0.0.0\n')

    env = os.environ.copy()
    # Ensure the project root is on PYTHONPATH so `import src` works when running the script
    env["PYTHONPATH"] = os.getcwd()
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    print(res.stdout)
    print(res.stderr)
    assert res.returncode == 0

    # check that at least one model and metrics file exist
    files = list(outdir.iterdir())
    names = [p.name for p in files]
    assert any(n.startswith('model_v') and n.endswith('.pkl') for n in names)
    assert any(n.startswith('metrics_v') and n.endswith('.json') for n in names)
