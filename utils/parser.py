import os
import fitz
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image
from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class Document:
    page_content: str
    metadata: Dict[str, Any]


class PDFProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.pdf_document = fitz.open(file_path)
        self.docs = None
        
        # Create images folder
        os.makedirs("images", exist_ok=True)
        print(f"Loaded PDF: {file_path} ({self.pdf_document.page_count} pages)")

    def load_documents(self) -> List[Document]:
        """Load all documents from PDF"""
        if self.docs is not None:
            return self.docs
            
        docs = []
        for page_number in range(self.pdf_document.page_count):
            page = self.pdf_document[page_number]
            page_width = page.rect.width
            page_height = page.rect.height
            blocks = page.get_text("blocks")

            for block in blocks:
                x0, y0, x1, y1, text, *_ = block

                if not text.strip():
                    continue

                doc = Document(
                    page_content=text,
                    metadata={
                        "source": self.file_path,
                        "page_number": page_number + 1,
                        "category": "Text",
                        "coordinates": {
                            "points": [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                            "layout_width": page_width,
                            "layout_height": page_height
                        }
                    }
                )
                docs.append(doc)

        self.docs = docs
        print(f"Extracted {len(docs)} text blocks")
        return docs

    def visualize_page(self, page_number: int):
        """Create visualization for one page"""
        page_docs = [doc for doc in self.load_documents() 
                    if doc.metadata.get("page_number") == page_number]
        segments = [doc.metadata for doc in page_docs]
        
        pdf_page = self.pdf_document.load_page(page_number - 1)
        pix = pdf_page.get_pixmap()
        pil_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        fig, ax = plt.subplots(1, figsize=(10, 10))
        ax.imshow(pil_image)
        
        category_to_color = {
            "Title": "orchid",
            "Image": "forestgreen",
            "Table": "tomato",
        }
        categories = set()

        for segment in segments:
            points = segment["coordinates"]["points"]
            layout_width = segment["coordinates"]["layout_width"]
            layout_height = segment["coordinates"]["layout_height"]
            
            scaled_points = [
                (x * pix.width / layout_width, y * pix.height / layout_height)
                for x, y in points
            ]
            
            box_color = category_to_color.get(segment["category"], "deepskyblue")
            categories.add(segment["category"])
            
            rect = patches.Polygon(
                scaled_points, linewidth=1, edgecolor=box_color, facecolor="none"
            )
            ax.add_patch(rect)

        # Make legend
        legend_handles = [patches.Patch(color="deepskyblue", label="Text")]
        for category in ["Title", "Image", "Table"]:
            if category in categories:
                legend_handles.append(
                    patches.Patch(color=category_to_color[category], label=category)
                )
        
        ax.axis("off")
        ax.legend(handles=legend_handles, loc="upper right")
        plt.tight_layout()

        output_filename = f"images/page_{page_number}.png"
        plt.savefig(output_filename, dpi=300)
        plt.close()

        print(f"Saved page {page_number} visualization as {output_filename}")

    def visualize_all_pages(self):
        """Create visualizations for all pages"""
        print(f"Processing {self.pdf_document.page_count} pages...")
        
        for page_num in range(1, self.pdf_document.page_count + 1):
            self.visualize_page(page_num)
        
        print("All visualizations saved in images/")

    def get_all_text(self) -> str:
        """Get all text concatenated with page markers"""
        docs = self.load_documents()
        docs.sort(key=lambda x: x.metadata.get("page_number", 0))
        
        all_text = ""
        current_page = None
        
        for doc in docs:
            page_num = doc.metadata.get("page_number", 1)
            
            if current_page != page_num:
                if current_page is not None:
                    all_text += f"\n\n--- PAGE {page_num} ---\n\n"
                else:
                    all_text += f"--- PAGE {page_num} ---\n\n"
                current_page = page_num
            
            all_text += doc.page_content + "\n"
        
        return all_text

    def get_page_text(self, page_number: int) -> str:
        """Get text from specific page"""
        docs = self.load_documents()
        page_docs = [doc for doc in docs if doc.metadata.get("page_number") == page_number]
        return "\n".join([doc.page_content for doc in page_docs])


if __name__ == "__main__":
    file_path = "data/driveshield_specimen_policy_value_plan.pdf"
    processor = PDFProcessor(file_path)

    all_text = processor.get_all_text()
    print(f"\nTotal characters extracted: {len(all_text)}")
    
    # Create visualizations
    processor.visualize_page(1)  # Just page 1
    # processor.visualize_all_pages()  # All pages