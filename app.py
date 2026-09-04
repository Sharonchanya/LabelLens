import streamlit as st
from ocr import read_text
from extractor import (
    extract_net_quantity,
    extract_mrp,
    extract_manufacturer,
    extract_date_information
)
from compliance import screen_compliance


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="LabelLens",
    page_icon="L",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');


    /* ---------------- GLOBAL ---------------- */

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #111827;
        color: #F8FAFC;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ---------------- SIDEBAR ---------------- */

    [data-testid="stSidebar"] {
        background: #0B1120;
        border-right: 1px solid #243244;
    }

    [data-testid="stSidebar"] * {
        color: #E2E8F0;
    }

    [data-testid="stSidebar"] hr {
        border-color: #243244;
    }


    /* ---------------- BRAND ---------------- */

    .brand-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -1px;
        color: #F8FAFC;
        margin-bottom: 0;
    }

    .brand-tagline {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #14B8A6;
        margin-top: 0.3rem;
    }


    /* ---------------- HERO ---------------- */

    .hero {
        padding: 3.5rem;
        border-radius: 20px;
        background:
            linear-gradient(
                135deg,
                #172554 0%,
                #111827 55%,
                #0F2F3A 100%
            );
        border: 1px solid #263650;
        margin-bottom: 2.5rem;
        box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.25);
    }

    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        letter-spacing: -2px;
        color: #F8FAFC;
        margin-bottom: 0.8rem;
    }

    .hero p {
        font-size: 1.1rem;
        line-height: 1.7;
        color: #94A3B8;
        margin-bottom: 0;
    }


    /* ---------------- SECTION TITLES ---------------- */

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
        letter-spacing: -0.5px;
    }


    /* ---------------- INFORMATION CARDS ---------------- */

    .info-card {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #2B3A4F;
        margin-bottom: 1rem;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.12);
    }

    .info-card h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: #F1F5F9;
        margin-top: 0;
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
    }

    .info-card p {
        color: #CBD5E1;
        line-height: 1.6;
    }


    /* ---------------- STATUS ---------------- */

    .status-detected {
        color: #14B8A6;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }

    .status-review {
        color: #F59E0B;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }


    /* ---------------- STATUS BANNERS ---------------- */

    .status-banner-review {
        padding: 1.8rem 2rem;
        border-radius: 16px;
        background: #251E12;
        border: 1px solid #5C4519;
        border-left: 4px solid #F59E0B;
        margin-bottom: 2rem;
    }

    .status-banner-review h2 {
        font-family: 'Space Grotesk', sans-serif;
        color: #FCD34D;
        margin-top: 0;
        margin-bottom: 0.6rem;
    }

    .status-banner-review p {
        color: #D6C8A8;
        margin-bottom: 0;
    }


    .status-banner-good {
        padding: 1.8rem 2rem;
        border-radius: 16px;
        background: #102C2C;
        border: 1px solid #1E5553;
        border-left: 4px solid #14B8A6;
        margin-bottom: 2rem;
    }

    .status-banner-good h2 {
        font-family: 'Space Grotesk', sans-serif;
        color: #5EEAD4;
        margin-top: 0;
        margin-bottom: 0.6rem;
    }

    .status-banner-good p {
        color: #B4D6D4;
        margin-bottom: 0;
    }


    /* ---------------- METRICS ---------------- */

    [data-testid="stMetric"] {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #2B3A4F;
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 1px;
    }

    [data-testid="stMetricValue"] {
        color: #F8FAFC;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
    }


    /* ---------------- BUTTONS ---------------- */

    .stButton > button {
        width: 100%;
        background: linear-gradient(
            135deg,
            #2563EB,
            #0F766E
        );
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border: none;
        color: #FFFFFF;
        opacity: 0.9;
        transform: translateY(-1px);
    }


    /* ---------------- FILE UPLOADER ---------------- */

    [data-testid="stFileUploader"] {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px dashed #3B82F6;
    }

    [data-testid="stFileUploader"] label {
        color: #CBD5E1;
    }


    /* ---------------- EXPANDER ---------------- */

    [data-testid="stExpander"] {
        background: #1E293B;
        border: 1px solid #2B3A4F;
        border-radius: 14px;
    }


    /* ---------------- ALERTS ---------------- */

    [data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ---------------- IMAGE ---------------- */

    [data-testid="stImage"] img {
        border-radius: 16px;
        border: 1px solid #2B3A4F;
    }


    /* ---------------- TEXT ---------------- */

    .stCaption {
        color: #64748B;
    }

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown(
        """
        <div class="brand-name">LabelLens</div>
        <div class="brand-tagline">Scan. Detect. Verify.</div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Home",
            "Scan Product",
            "Product History"
        ]
    )

    st.divider()

    st.markdown("### AI-ASSISTED SCREENING")

    st.caption(
        "A smart screening system designed to analyze "
        "packaged product labels and highlight information "
        "that may require human review."
    )


# ---------------- HOME PAGE ----------------

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <h1>LabelLens</h1>
            <p>
                Scan. Detect. Verify.
                <br><br>
                AI-assisted screening for packaged commodity labels.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">How It Works</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="info-card">
                <h3>01 — Scan</h3>
                <p>
                    Upload an image of a packaged product
                    label for analysis.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="info-card">
                <h3>02 — Detect</h3>
                <p>
                    OCR technology extracts important
                    information from the product label.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="info-card">
                <h3>03 — Verify</h3>
                <p>
                    LabelLens highlights information that
                    may require further human review.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        "LabelLens is an AI-assisted screening prototype. "
        "Results do not constitute a final legal or regulatory decision."
    )


# ---------------- SCAN PRODUCT PAGE ----------------

elif page == "Scan Product":

    st.markdown(
        """
        <div class="hero">
            <h1>Scan Product</h1>
            <p>
                Upload a packaged product label and let
                LabelLens analyze the information it contains.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Product Label",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        st.markdown(
            '<div class="section-title">Uploaded Label</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 1])

        with col1:

            st.image(
                uploaded_file,
                caption="Product Label"
            )

        with col2:

            st.markdown(
                """
                <div class="info-card">
                    <h3>Ready for Analysis</h3>
                    <p>
                        Your product image has been uploaded successfully.
                    </p>
                    <p>
                        LabelLens will scan the label and extract
                        relevant information for preliminary screening.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            scan_button = st.button("Scan Label")

        if scan_button:

            with st.spinner("Analyzing product label..."):

                # OCR
                results = read_text(uploaded_file)

                # Information extraction
                net_quantity = extract_net_quantity(results)
                mrp = extract_mrp(results)
                manufacturer = extract_manufacturer(results)
                date_information = extract_date_information(results)

                # Compliance screening
                screening_results = screen_compliance(
                    net_quantity,
                    mrp,
                    manufacturer,
                    date_information
                )


            # ---------------- CALCULATE RESULTS ----------------

            detected_count = sum(
                1 for result in screening_results
                if result["status"] == "Detected"
            )

            review_count = sum(
                1 for result in screening_results
                if result["status"] == "Review Required"
            )

            total_fields = len(screening_results)


            # ---------------- SCREENING RESULTS ----------------

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                '<div class="section-title">Screening Results</div>',
                unsafe_allow_html=True
            )


            # OVERALL STATUS

            if review_count > 0:

                st.markdown(
                    f"""
                    <div class="status-banner-review">
                        <h2>Review Recommended</h2>
                        <p>
                            {review_count} information field(s) could not
                            be reliably detected from the uploaded label.
                            Human verification is recommended.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="status-banner-good">
                        <h2>Information Successfully Detected</h2>
                        <p>
                            All information currently checked by this
                            prototype was successfully detected.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ---------------- SCREENING SUMMARY ----------------

            st.markdown(
                '<div class="section-title">Screening Summary</div>',
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "FIELDS CHECKED",
                    total_fields
                )

            with col2:
                st.metric(
                    "INFORMATION DETECTED",
                    f"{detected_count}/{total_fields}"
                )

            with col3:
                st.metric(
                    "NEEDS REVIEW",
                    review_count
                )


            # ---------------- EXTRACTED INFORMATION ----------------

            st.markdown(
                '<div class="section-title">Extracted Information</div>',
                unsafe_allow_html=True
            )

            for result in screening_results:

                field = result["field"]
                value = result["value"]
                status = result["status"]

                if status == "Detected":

                    status_text = "DETECTED"
                    status_class = "status-detected"

                else:

                    status_text = "REVIEW REQUIRED"
                    status_class = "status-review"

                st.markdown(
                    f"""
                    <div class="info-card">
                        <h3>{field}</h3>
                        <p style="font-size:1.1rem;">
                            {value}
                        </p>
                        <span class="{status_class}">
                            {status_text}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ---------------- AI ASSESSMENT ----------------

            st.markdown(
                '<div class="section-title">AI-Assisted Assessment</div>',
                unsafe_allow_html=True
            )

            if review_count > 0:

                st.warning(
                    f"{review_count} field(s) could not be reliably "
                    "detected from the uploaded image. "
                    "Human review is recommended."
                )

            else:

                st.success(
                    "All information currently checked by this prototype "
                    "was successfully detected."
                )

            st.caption(
                "This screening result is based on information detected "
                "from the uploaded image and does not constitute a final "
                "legal compliance decision."
            )


            # ---------------- RAW OCR RESULTS ----------------

            with st.expander("View All Detected Text"):

                for item in results:

                    confidence_percentage = (
                        item["confidence"] * 100
                    )

                    st.write(
                        f"**{item['text']}** "
                        f"— Confidence: "
                        f"{confidence_percentage:.1f}%"
                    )


# ---------------- PRODUCT HISTORY PAGE ----------------

elif page == "Product History":

    st.markdown(
        """
        <div class="hero">
            <h1>Product History</h1>
            <p>
                Track scanned products and build a digital
                compliance record over time.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "This feature is currently under development. "
        "Future versions of LabelLens can maintain a history "
        "of scanned products and their screening results."
    )