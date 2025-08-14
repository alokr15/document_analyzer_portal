import os
import fitz
import sys
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException

class DocumentHandler:
    """Class to handle PDF document ingestion and processing."""

    def __init__(self, data_dir=None, session_id=None):
        """Initialize the DocumentHandler with a session ID."""
        try:
            self.logger = CustomLogger().get_logger(__file__)
            self.data_dir = data_dir or os.getenv("DATA_STORAGE_PATH", 
                                                os.path.join(os.getcwd(), "data", "doc_analysis"))
            self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            # create session directory if it doesn't exist
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)
            self.logger.info("DocumentHandler initialized", session_id=self.session_id, data_dir=self.data_dir)
        except Exception as e:
            self.logger.error("Failed to initialize DocumentHandler", error=str(e))
            raise CustomException(f"Error initializing DocumentHandler: {str(e)}")

    def save_pdf(self, pdf_file):
        """Save the uploaded PDF file to a designated directory."""
        try:
            filename = os.path.basename(pdf_file.name)
            if not filename.lower().endswith('.pdf'):
                raise CustomException("Invalid file type. Only PDF files are allowed.")
            
            save_path = os.path.join(self.session_path, filename)
            with open(save_path, 'wb') as f:
                f.write(pdf_file.read())
            self.logger.info("PDF file saved successfully", filename=filename, save_path=save_path, session_id=self.session_id)
            return save_path

        except Exception as e:
            self.logger.error("Failed to save PDF", error=str(e))
            raise CustomException(f"Error saving PDF: {str(e)}")
        
    def read_pdf(self, pdf_path):
        """Read and extract text from the PDF file."""
        try:
            if not os.path.exists(pdf_path):
                raise CustomException(f"PDF file not found: {pdf_path}")
            
            text_chunks = []
            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc, start=1): # type: ignore
                    text_chunks.append(f"\n--- Page {page_num} ---\n{page.get_text()}")
            text = "\n".join(text_chunks)
            self.logger.info("PDF read successfully", pdf_path=pdf_path, num_pages=len(text_chunks))
            return text

        except Exception as e:
            self.logger.error("Failed to read PDF", error=str(e))
            raise CustomException(f"Error reading PDF: {str(e)}")    
        

if __name__ == "__main__":
    # Example usage
    try:
        file_path = "C:\\Users\\hp\\Documents\\document_analyzer_portal\\data\\doc_analysis\\sample.pdf"
        handler = DocumentHandler()
        pdf_path = handler.save_pdf(open(file_path, "rb"))
        text = handler.read_pdf(pdf_path)
        print("Extracted text:", text[:500])  # Print first 500 characters of extracted text
    except CustomException as e:    
        print(f"Error: {e}")    