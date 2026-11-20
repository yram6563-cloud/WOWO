import io
import zipfile
import streamlit as st
import fitz  # PyMuPDF

# Page Configuration
st.set_page_config(page_title="PDF Master Attacher", page_icon="📎", layout="centered")

st.title("📎 Automatic PDF Master Attacher")
st.write("Upload your **Master PDF** (e.g., `rest.pdf`) and your **Target PDFs**. The app will automatically attach the Master PDF to the **end** of each target file and package them into a downloadable `.zip` file.")

st.divider()

# 1. Master PDF Upload
master_file = st.file_uploader("1️⃣ Select your Master PDF (e.g., rest.pdf)", type=["pdf"], key="master")

# 2. Target PDFs Upload
target_files = st.file_uploader("2️⃣ Select Target PDFs (Upload multiple files)", type=["pdf"], accept_multiple_files=True, key="targets")

st.divider()

if master_file and target_files:
    if st.button("🚀 Combine & Generate PDFs", type="primary"):
        with st.spinner("Processing files..."):
            try:
                # Read Master PDF stream
                master_bytes = master_file.read()
                master_doc = fitz.open(stream=master_bytes, filetype="pdf")

                # Prepare in-memory ZIP buffer
                zip_buffer = io.BytesIO()

                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    success_count = 0
                    
                    for target in target_files:
                        target_bytes = target.read()
                        doc = fitz.open(stream=target_bytes, filetype="pdf")

                        # Append Master PDF at the end of current target PDF
                        doc.insert_pdf(master_doc)

                        # Save output to byte buffer
                        output_buffer = io.BytesIO()
                        doc.save(output_buffer, deflate=True)
                        doc.close()

                        # Prepend '0' to the original filename (e.g., 600000011.pdf -> 060000011.pdf)
                        output_filename = f"0{target.name}"
                        zip_file.writestr(output_filename, output_buffer.getvalue())
                        success_count += 1

                master_doc.close()
                zip_buffer.seek(0)

                st.success(f"🎉 Successfully attached Master PDF to {success_count} file(s)!")

                # Download ZIP Button
                st.download_button(
                    label="📦 Download All Combined PDFs (.zip)",
                    data=zip_buffer,
                    file_name="Combined_PDFs.zip",
                    mime="application/zip"
                )

            except Exception as e:
                st.error(f"Error processing documents: {e}")
elif master_file or target_files:
    st.info("Please upload both the Master PDF and at least one Target PDF to proceed.")