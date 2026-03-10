import argparse
from pathlib import Path
from PIL import Image
from dataclasses import dataclass, field
from typing import Optional, List
import time

@dataclass
class Ctx:
    rootPath: Path = field(default=Path('.').resolve())
    outputFileExtension: str = field(default=".pdf")
    outputPathStr: str = field(default="output")
    outputFile: str = field(default="output")
    customSuffix: Optional[str] = field(default=None)

    @property
    def outputPath(self) -> Path:
        return self.rootPath / self.outputPathStr

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

def convert_images_to_pdf(ctx: Ctx, image_files: List[Path]):
    if not ctx.outputPath.exists():
        ctx.outputPath.mkdir(parents=True, exist_ok=True)

    if not image_files:
        print("No image files provided.")
        return

    print(f"Found {len(image_files)} image(s).")
    print(f"Output will be placed in: {ctx.outputPath.resolve()}")

    images = []
    for image_file in image_files:
        try:
            img = Image.open(image_file)
            if img.mode in ("RGBA", "P"):  # Convert to RGB if necessary
                img = img.convert("RGB")
            images.append(img)
        except Exception as e:
            print(f"Error processing image {image_file}: {e}")

    if images:
        ctx.customSuffix = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
        output_file = ctx.outputFilePath
        images[0].save(output_file, save_all=True, append_images=images[1:])
        print(f"PDF created successfully: {output_file}")
    else:
        print("No valid images to convert.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert images to a single PDF.")
    parser.add_argument("images", nargs="+", help="Paths to image files to include in the PDF.")
    parser.add_argument("--output", default="output", help="Name of the output PDF file (default: 'output')")
    args = parser.parse_args()

    ctx = Ctx(outputFile=args.output)
    image_paths = [Path(image) for image in args.images]
    convert_images_to_pdf(ctx, image_paths)