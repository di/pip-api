import json
import subprocess

toxenvs = subprocess.check_output(["tox", "--listenvs"]).decode().split("\n")

output = {
    "include": [
        {
            "toxenv": toxenv,
            "python-version": (
                "3.15-dev"
                if toxenv.startswith("py315-")
                else toxenv.split("-")[0][2] + "." + toxenv.split("-")[0][3:]
            ),
        }
        for toxenv in toxenvs
        if toxenv.startswith("py")
    ]
}

print(json.dumps(output))
