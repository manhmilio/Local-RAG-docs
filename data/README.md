# Sample PDF Documents for Testing

Place your medical PDF documents in this folder to enable RAG functionality.

## Recommended Document Types:

- Medical textbooks
- Disease symptom guides
- Treatment protocols
- Clinical guidelines
- Medical research papers (in Vietnamese or English)

## How to Add Documents:

1. Copy PDF files to this folder
2. Use the Upload feature in the web interface, OR
3. Run the reindex endpoint:
   ```
   POST http://localhost:8001/documents/reindex
   ```

## File Naming Convention:

Use descriptive names:
- ✅ cam_cum_trieu_chung.pdf
- ✅ diabetes_treatment_guide.pdf
- ✅ medical_symptoms_vietnamese.pdf
- ❌ doc1.pdf
- ❌ file.pdf

## Size Recommendations:

- Optimal: 1-10 MB per file
- Maximum: 50 MB per file
- Total: No hard limit, but performance degrades with > 100 files

## Example Documents:

You can test with these types of medical documents:
- Vietnamese medical encyclopedia
- WHO health guidelines (translated)
- Common disease symptom charts
- First aid manuals
- Medication reference guides
