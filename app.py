import streamlit as st
import qrcode
from io import BytesIO
from datetime import date

st.set_page_config(
    page_title="Slide Traceability Demo",
    layout="wide"
)

st.caption(
    "Supports QR and barcode-based slide traceability workflows."
)
left_column, right_column = st.columns([1, 1])
# =====================================================
# MOCK SLIDE DATA
# =====================================================
mock_slide_records = {
    "SLIDE-1001": {
        "slide_id": "SLIDE-1001",
        "batch_id": "BATCH-22A",
        "operator_name": "Sarah Johnson",
        "manufacturing_date": "2026-05-25",
        "qc_status": "Approved",
        "certificate_status": "Available",
        "lifecycle_events": [
            "Manufactured",
            "Quality Checked",
            "Packaged",
            "Ready for Shipment"
        ]
    },

    "SLIDE-1002": {
        "slide_id": "SLIDE-1002",
        "batch_id": "BATCH-31B",
        "operator_name": "Michael Chen",
        "manufacturing_date": "2026-05-24",
        "qc_status": "Pending",
        "certificate_status": "Pending",
        "lifecycle_events": [
            "Manufactured",
            "Quality Inspection In Progress"
        ]
    },

    "SLIDE-1003": {
        "slide_id": "SLIDE-1003",
        "batch_id": "BATCH-18C",
        "operator_name": "Emma Wilson",
        "manufacturing_date": "2026-05-20",
        "qc_status": "Approved",
        "certificate_status": "Available",
        "lifecycle_events": [
            "Manufactured",
            "Quality Checked",
            "Sterilized",
            "Packaged",
            "Shipped"
        ]
    }
}

# =====================================================
# RIGHT COLUMN - LOOKUP RECORD
# =====================================================
# =====================================================
# RIGHT COLUMN - LOOKUP RECORD
# =====================================================
with right_column:

    st.subheader("Slide Lookup")

    selected_slide_id = st.selectbox(
        "Select Slide ID",
        options=list(mock_slide_records.keys())
    )

    lookup_button = st.button("Lookup Slide")

    if lookup_button:

        slide_data = mock_slide_records[selected_slide_id]

        st.success("Slide record found.")

        st.markdown("### Slide Information")

        st.write(f"**Slide ID:** {slide_data['slide_id']}")
        st.write(f"**Batch ID:** {slide_data['batch_id']}")
        st.write(f"**Operator:** {slide_data['operator_name']}")
        st.write(f"**Manufacturing Date:** {slide_data['manufacturing_date']}")
        st.write(f"**QC Status:** {slide_data['qc_status']}")
        st.write(f"**Certificate:** {slide_data['certificate_status']}")

        st.markdown("### Lifecycle Timeline")

        for lifecycle_event in slide_data["lifecycle_events"]:
            st.write(f"✅ {lifecycle_event}")
# -----------------------------
# Mock Storage
# -----------------------------
if "slide_records" not in st.session_state:
    st.session_state.slide_records = {}

# -----------------------------
# Helper Functions
# -----------------------------
def generate_qr_code_image_helper(slide_id_value: str):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )

    qr.add_data(slide_id_value)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")

    image_buffer = BytesIO()
    qr_image.save(image_buffer, format="PNG")

    return image_buffer.getvalue()


# -----------------------------
# Header
# -----------------------------
st.title("Microscope Slide Traceability Demo")
st.caption(
    "A lightweight proof-of-concept for slide lifecycle tracking and QR-based lookup workflows."
)

# -----------------------------
# Layout
# -----------------------------


# =====================================================
# LEFT COLUMN - CREATE RECORD
# =====================================================
with left_column:
    st.subheader("Create Slide Record")

    with st.form("create_slide_form"):
        slide_id = st.text_input("Slide ID", value="SLIDE-1001")
        batch_id = st.text_input("Batch ID", value="BATCH-22A")
        operator_name = st.text_input("Operator Name", value="Sarah Johnson")
        manufacturing_date = st.date_input(
            "Manufacturing Date",
            value=date.today()
        )

        qc_status = st.selectbox(
            "QC Status",
            [
                "Pending",
                "Approved",
                "Rejected"
            ]
        )

        submit_button = st.form_submit_button("Generate Traceability Record")

    if submit_button:
        slide_record = {
            "slide_id": slide_id,
            "batch_id": batch_id,
            "operator_name": operator_name,
            "manufacturing_date": str(manufacturing_date),
            "qc_status": qc_status,
            "certificate_status": "Available",
            "lifecycle_events": [
                "Manufactured",
                "Quality Checked",
                "Packaged",
                "Ready for Shipment"
            ]
        }

        st.session_state.slide_records[slide_id] = slide_record

        qr_code_image_bytes = generate_qr_code_image_helper(slide_id)

        st.success("Slide traceability record generated successfully.")

        st.image(
            qr_code_image_bytes,
            caption=f"QR Code for {slide_id}",
            width=220
        )

# =====================================================
# RIGHT COLUMN - LOOKUP RECORD
# =====================================================

# -----------------------------
# Footer Notes
# -----------------------------
st.divider()

st.markdown(
    """
    ### Demo Notes

    This demo intentionally uses mock in-memory data to demonstrate the workflow concept:

    - Slide record creation
    - Batch traceability
    - QR-based identification
    - Lifecycle visibility
    - Operational lookup workflow

    A production implementation could later integrate:

    - FastAPI
    - PostgreSQL
    - AWS RDS
    - Authentication
    - PDF certificate generation
    - Barcode scanner integration
    """
)
