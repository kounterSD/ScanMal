# MalScan
## Table of contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Resources](#resources)

### Installation
The yara-x module is built on `rust`. Installing latest versions of `rustc` and `cargo` is required.

```bash
apt install rustc
apt install cargo
```
Install the python module requirements

```bash
pip install -r requirements.txt
```
### Usage
Starting the development server
```bash
fastapi dev main.py
```
Once the startup is completed, you can send POST request to `/scan` endpoint.
```bash
curl -F "file=@<path-to-target-file>" http://localhost:8000/scan
```
The JSON response information about all successful matches.

### Resources
The Rule Sets I used:
1. yara-forge
`https://yarahq.github.io`
