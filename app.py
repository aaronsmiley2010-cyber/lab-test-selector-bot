import os
import pandas as pd
from flask import Flask, request, make_response
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# Load the CSV once at startup
def load_tests(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    # remove $ and commas, convert to floats
    def clean_price(s):
        try:
            return float(str(s).replace("$", "").replace(",", ""))
        except Exception:
            return None
    df["Retail Price"] = df["Retail Price"].apply(clean_price)
    df["Discount Price"] = df["Discount Price"].apply(clean_price)
    # compute profit and profit margin
    df["Profit"] = df["Retail Price"] - df["Discount Price"]
    df["Profit Margin"] = df["Profit"] / df["Retail Price"]
    return df

# Instantiate Slack Bolt app
bolt_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

# Load your test data; ensure CSV is present in repo
TEST_DF = load_tests("Idexx Prices 2025 - Sheet1 (4).csv")

def recommend_tests(query: str, max_results: int = 5) -> pd.DataFrame:
    """
    Filter tests by keyword(s) in Name, Category, or Description.
    Rank by profit margin (descending), then profit, then price (ascending).
    """
    if not query:
        return TEST_DF.head(0)
    keywords = [word.lower() for word in query.split()]
    mask = pd.Series(False, index=TEST_DF.index)
    for col in ["Name", "Category", "Description"]:
        mask = mask | TEST_DF[col].fillna("").str.lower().str.contains('|'.join(keywords))
    # sort by profit margin and profit to find best value for clinic and owner
    results = TEST_DF[mask].sort_values(
        by=["Profit Margin", "Profit", "Retail Price"],
        ascending=[False, False, True]
    ).head(max_results)
    return results

@bolt_app.command("/choose_test")
def handle_choose_test(ack, respond, command):
    """Handle the /choose_test slash command."""
    ack()  # acknowledge the command immediately
    query = command.get("text", "").strip()
    if not query:
        respond("Please provide a search term, e.g. `/choose_test heartworm`.")
        return
    results = recommend_tests(query)
    if results.empty:
        respond(f"No tests found matching `{query}`. Try different keywords.")
        return

    # Format response
    blocks = []
    for _, row in results.iterrows():
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{row['Name']}* (Code: `{row['Code']}`)\n"
                            f"> Category: {row['Category']}\n"
                            f"> Price: ${row['Retail Price']:.2f} | Profit: ${row['Profit']:.2f} "
                            f"({row['Profit Margin']:.1%})\n"
                            f"> {row['Description'][:200]}..."
                }
            }
        )
        blocks.append({"type": "divider"})
    respond(blocks=blocks)

# Set up Flask server
flask_app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

# Slack slash commands and events will POST to /slack/events
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("/", methods=["GET"])
def index():
    return make_response("Lab Test Selector Bot is running!", 200)

if __name__ == "__main__":
    # Bind to port provided by Heroku
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)
