import argparse
from pathlib import Path
from typing import Optional
import time
from dataclasses import dataclass, field
import camelot.io as camelot
import pandas as pd
import gc

@dataclass
class Ctx:
    rootPath: Path = field(default=Path('.').resolve())
    outputFileExtension: str = field(default=".xlsx")
    outputPathStr: str = field(default="output")
    dataPathStr: str = field(default='data')
    outputFile: str = field(default="file")
    customSuffix: Optional[str] = field(default=None) 

    @property
    def outputPath(self) -> Path:
        return self.rootPath / self.outputPathStr
    
    @property
    def dataPath(self) -> Path:
        return self.rootPath / self.dataPathStr

    @property
    def outputFilePath(self) -> Path:
        base_name = self.outputFile + self.outputFileExtension
        p = self.outputPath / base_name
        if not p.exists():
            return p
        else:
            if self.customSuffix:
                formatted = self.customSuffix
            else:
                localTime = time.localtime()
                formatted = time.strftime('%Y_%m_%d_%X', localTime)
                formatted = formatted.replace(":", "")
            stem = p.stem  
            suffix = p.suffix 
            new_filename = f"{stem}_{formatted}{suffix}"
            return p.with_name(new_filename)

def main(pdf_filename: str, pages: str = '1', parallel: bool = True):
    ctx = Ctx()
    
    if not ctx.outputPath.exists():
        ctx.outputPath.mkdir(parents=True, exist_ok=True)
    
    if not ctx.dataPath.exists():
        print(f"Couldn't find data directory: {ctx.dataPath.resolve()}")
        print("Creating data directory...")
        ctx.dataPath.mkdir(parents=True, exist_ok=True)
    
    pdf_path = ctx.dataPath / pdf_filename
    
    if not pdf_path.exists():
        print(f"PDF file not found: {pdf_path.resolve()}")
        print(f"Please place '{pdf_filename}' in {ctx.dataPath.resolve()}")
        return
    
    print(f"Processing PDF: {pdf_path.resolve()}")
    print(f"Output will be placed in: {ctx.outputPath.resolve()}")

    flavors = ['lattice', 'stream', 'network', 'hybrid']
    localTime = time.localtime()
    formatted = time.strftime('%Y_%m_%d_%X', localTime)
    formatted = formatted.replace(":", "")
    ctx.customSuffix = formatted

    for flavor in flavors:
        try:
            pdf = str(pdf_path)
            tables = camelot.read_pdf(pdf, pages=pages, parallel=parallel, flavor=flavor)
            ctx.outputFile = f"{Path(pdf_filename).stem}_{flavor}"
            tables.export(str(ctx.outputFilePath), f='excel')
            print(f"Exported {flavor} tables to {ctx.outputFilePath}")

        except Exception as e:
            print(f"Error processing {flavor}: {e}")
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract tables from PDF and export to Excel.")
    parser.add_argument("pdf_filename", help="Name of the PDF file in the data directory")
    parser.add_argument("--pages", default='1', help="Pages to process (default: '1')")
    args = parser.parse_args()
    main(args.pdf_filename, args.pages)