import os
import logging
import fastapi
import yara_x
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

#Logging errors
logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="compile_errors.log",
    filemode="w",  # Overwrite the file each time you run
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

#Test code to use and/or match YARA rules.
rules_dir="./packages/full/" #I used yara-forge Rule Sets
mal_dir = "./test-php-rev-shell.php" #dir to target file
app = FastAPI()

def compile_rule_files(directory: str ):
    compiler = yara_x.Compiler()    
    i=0
    for filename in os.listdir(directory):
        if filename.endswith(".yar"):
            i+=1
            filepath=os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:           
                    rule_content = f.read()
                    compiler.add_source(rule_content, origin=directory)
                    compiler.add_source
            except yara_x.CompileError as e:
                logger.error(f"{filepath} {e}")
                print(f"[ERROR] Failed to compile {filepath}")

    rules = compiler.build()
    return rules
            
rules = compile_rule_files(rules_dir)

scanner = yara_x.Scanner(rules)

@app.post("/scan")
async def scan_uploads_file(file: UploadFile=File(...)):
    # Save uploaded file temporarily
    contents = await file.read()
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    results = scanner.scan_file(temp_path)

    response = []
    for rule in results.matching_rules:
        rule_result = {
            "rule_id": rule.identifier,
            "matches": []
        }
        for pattern in rule.patterns:
            for match in pattern.matches:
                with open(temp_path, "rb") as f:
                    f.seek(match.offset)
                    matched_bytes = f.read(match.length)
                rule_result["matches"].append({
                    "pattern_id": pattern.identifier,
                    "offset": match.offset,
                    "length": match.length,
                    "matched_bytes": matched_bytes.hex()  # return hex string
                })
        response.append(rule_result)

    os.remove(temp_path)
    return JSONResponse(content=response)


