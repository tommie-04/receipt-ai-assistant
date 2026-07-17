from database import init_db, save_transaction, get_user_transactions
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="AI Receipt Assistant",
    page_icon="🧾",
    layout="centered"
)

init_db()

# Custom styling
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fb;
    }
    .transaction-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border-left: 4px solid #4f8cff;
    }
    .transaction-title {
        font-size: 18px;
        font-weight: 700;
        color: #1a1a1a;
    }
    .transaction-meta {
        color: #666666;
        font-size: 14px;
        margin-top: 4px;
    }
    .category-badge {
        display: inline-block;
        background-color: #eaf1ff;
        color: #4f8cff;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Category icons for a bit of visual flair
CATEGORY_ICONS = {
    "food": "🍔",
    "transport": "🚗",
    "shopping": "🛍️",
    "bills": "💡",
    "entertainment": "🎬",
    "other": "📦"
}

def get_icon(category):
    return CATEGORY_ICONS.get(category.lower(), "📦") if category else "📦"


 # Initialize session state for username if not already set
if "username" not in st.session_state:
    st.session_state.username = None

# If no username set yet, show login form
if st.session_state.username is None:
    st.title("🧾 AI Receipt Assistant")
    st.write("Enter a username to get started. No password needed for now.")

    username_input = st.text_input("Username")

    if st.button("Continue"):
        if username_input.strip() == "":
            st.error("Please enter a username.")
        else:
            st.session_state.username = username_input.strip()
            st.rerun()

    st.stop()  # Stop execution here until username is set   


# Header
st.title("🧾 AI Receipt Assistant")
st.write(f"Welcome, **{st.session_state.username}**! Upload a receipt, bank statement, or handwritten note.")

if st.button("Log out"):
    st.session_state.username = None
    st.rerun()


uploaded_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    with st.expander("View uploaded image", expanded=False):
        st.image(uploaded_file, use_container_width=True)

    image_bytes = uploaded_file.read()

    prompt = """
    You are a financial document analyzer. You will be shown an image that may or may not contain financial/transaction information.

    First, determine whether the image actually contains one of the following:
    - A receipt (printed or handwritten), possibly with multiple purchased items
    - A bank or credit card statement showing one or more transactions
    - A handwritten note listing expenses or payments

    If the image does NOT contain any financial or transaction information (for example, it is a landscape photo, a selfie, a random object, or unrelated content), respond with exactly this JSON:
    {"error": "no_financial_data", "message": "This image does not appear to contain a receipt, statement, or expense record."}

    If the image DOES contain financial/transaction information, return a JSON array of transactions, even if there is only one.
    Each transaction object must have these keys:
    - "merchant": the store, business, or payee name
    - "total": the total transaction amount (include currency symbol if visible)
    - "date": the transaction date (use "unknown" if not visible)
    - "category": your best guess at a spending category (e.g. food, transport, shopping, bills, entertainment, other)
    - "items": a list of individual line items if visible, each with "name" and "price". If no item-level detail is visible, return an empty list [].

    Only return the JSON (either the error object or the array). No extra explanation or text.
    """

    with st.spinner("Analyzing image..."):
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=uploaded_file.type),
                prompt
            ]
        )

    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        st.error("Something went wrong reading the AI's response. Please try again.")
        st.text(response.text)
        result = None

    if result is not None:
        if isinstance(result, dict) and result.get("error") == "no_financial_data":
            st.warning(result.get("message", "This doesn't look like a receipt or financial document."))

        elif isinstance(result, list):
            # Summary metrics row
            total_count = len(result)
            st.markdown(f"### Found {total_count} transaction{'s' if total_count != 1 else ''}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Transactions", total_count)
            with col2:
                categories_found = len(set(t.get("category", "other") for t in result))
                st.metric("Categories", categories_found)

            st.markdown("---")

            # Transaction cards
            for transaction in result:
                merchant = transaction.get("merchant", "Unknown")
                total = transaction.get("total", "N/A")
                date = transaction.get("date", "unknown")
                category = transaction.get("category", "other")
                icon = get_icon(category)
                items = transaction.get("items", [])

                # Save this transaction to the database
                save_transaction(
                    username=st.session_state.username,
                    merchant=merchant,
                    total=total,
                    date=date,
                    category=category,
                    items=items
                )

                card_html = f"""
                <div class="transaction-card">
                    <div class="transaction-title">{icon} {merchant} — {total}</div>
                    <div class="transaction-meta">📅 {date}</div>
                    <span class="category-badge">{category}</span>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                if items:
                    with st.expander(f"View {len(items)} item(s)", expanded=True):
                        for item in items:
                            item_name = item.get("name", "Unknown item")
                            item_price = item.get("price", "N/A")
                            item_html = f"""
                            <div style="
                                background-color: #f8f9fb;
                                border-radius: 8px;
                                padding: 10px 14px;
                                margin-bottom: 8px;
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                            ">
                                <span style="color: #333333; font-size: 14px;">🍽️ {item_name}</span>
                                <span style="color: #4f8cff; font-weight: 600; font-size: 14px;">{item_price}</span>
                            </div>
                            """
                            st.markdown(item_html, unsafe_allow_html=True)

        else:
            st.error("Unexpected response format from AI.")
            st.write(result)