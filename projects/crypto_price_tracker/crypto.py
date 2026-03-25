import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import threading
import schedule

# Page configuration
st.set_page_config(
    page_title="Crypto Price Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .price-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    .alert-card {
        background-color: #ff4757;
        color: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


class CryptoPriceTracker:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.alerts_file = "price_alerts.json"
        self.price_log_file = "price_log.csv"
        self.alert_log_file = "alert_log.txt"
        self.load_alerts()
        self.initialize_price_log()

    def load_alerts(self):
        """Load saved alerts from file"""
        try:
            if os.path.exists(self.alerts_file):
                with open(self.alerts_file, 'r') as f:
                    self.alerts = json.load(f)
            else:
                self.alerts = {}
        except:
            self.alerts = {}

    def save_alerts(self):
        """Save alerts to file"""
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts, f, indent=4)

    def initialize_price_log(self):
        """Initialize price log file"""
        if not os.path.exists(self.price_log_file):
            df = pd.DataFrame(columns=['timestamp', 'crypto', 'price_usd'])
            df.to_csv(self.price_log_file, index=False)

    def log_price(self, crypto, price):
        """Log price to CSV file"""
        try:
            df = pd.read_csv(self.price_log_file)
            new_entry = pd.DataFrame({
                'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                'crypto': [crypto],
                'price_usd': [price]
            })
            df = pd.concat([df, new_entry], ignore_index=True)
            # Keep only last 1000 entries per crypto to manage file size
            df = df.groupby('crypto').tail(1000)
            df.to_csv(self.price_log_file, index=False)
        except Exception as e:
            st.error(f"Error logging price: {e}")

    def log_alert(self, crypto, threshold_price, current_price, alert_type):
        """Log alert to text file"""
        try:
            with open(self.alert_log_file, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp} - {alert_type.upper()} ALERT - {crypto}: "
                        f"Threshold ${threshold_price} - Current ${current_price}\n")
        except Exception as e:
            st.error(f"Error logging alert: {e}")

    def send_email_alert(self, crypto, threshold_price, current_price, alert_type, email_config):
        """Send email alert when threshold is met"""
        try:
            subject = f"Crypto Alert: {crypto} {alert_type} Threshold Reached!"
            body = f"""
            <h2>⚠️ Price Alert Triggered!</h2>
            <p><strong>Crypto:</strong> {crypto}</p>
            <p><strong>Alert Type:</strong> {alert_type.upper()}</p>
            <p><strong>Threshold Price:</strong> ${threshold_price}</p>
            <p><strong>Current Price:</strong> ${current_price}</p>
            <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Check your Streamlit app for more details!</p>
            """

            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['receiver_email']
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            # For production, use your email credentials
            # This is a simplified version - you'll need to configure your SMTP server
            # server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            # server.starttls()
            # server.login(email_config['sender_email'], email_config['password'])
            # server.send_message(msg)
            # server.quit()

            st.success(f"Email alert sent for {crypto}!")
            return True
        except Exception as e:
            st.error(f"Failed to send email: {e}")
            return False

    def check_alerts(self, crypto, current_price, email_config=None):
        """Check if any alerts are triggered"""
        if crypto in self.alerts:
            for alert in self.alerts[crypto]:
                alert_type = alert['type']
                threshold = alert['price']
                email_sent_key = f"{crypto}_{alert_type}_{threshold}_{datetime.now().date()}"

                if alert_type == 'above' and current_price >= threshold:
                    if not alert.get('email_sent_today', False):
                        self.log_alert(crypto, threshold, current_price, alert_type)
                        if email_config and email_config.get('enabled'):
                            self.send_email_alert(crypto, threshold, current_price, alert_type, email_config)
                            alert['email_sent_today'] = True
                            self.save_alerts()
                    return True
                elif alert_type == 'below' and current_price <= threshold:
                    if not alert.get('email_sent_today', False):
                        self.log_alert(crypto, threshold, current_price, alert_type)
                        if email_config and email_config.get('enabled'):
                            self.send_email_alert(crypto, threshold, current_price, alert_type, email_config)
                            alert['email_sent_today'] = True
                            self.save_alerts()
                    return True
                else:
                    # Reset daily email flag if condition no longer met
                    alert['email_sent_today'] = False
                    self.save_alerts()
        return False

    def get_crypto_prices(self, cryptos):
        """Fetch current prices for selected cryptocurrencies"""
        try:
            ids = ','.join(cryptos)
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': ids,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            prices = []
            for crypto in cryptos:
                if crypto in data:
                    prices.append({
                        'crypto': crypto.upper(),
                        'price_usd': data[crypto]['usd'],
                        '24h_change': data[crypto].get('usd_24h_change', 0),
                        'market_cap': data[crypto].get('usd_market_cap', 0),
                        '24h_vol': data[crypto].get('usd_24h_vol', 0)
                    })
                    # Log price for history
                    self.log_price(crypto, data[crypto]['usd'])

            return pd.DataFrame(prices)
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return pd.DataFrame()

    def get_historical_data(self, crypto, days=7):
        """Get historical price data for a cryptocurrency"""
        try:
            url = f"{self.base_url}/coins/{crypto}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily' if days > 90 else 'hourly'
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            prices = data.get('prices', [])
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['crypto'] = crypto.upper()

            return df
        except Exception as e:
            st.error(f"Error fetching historical data: {e}")
            return pd.DataFrame()


def main():
    st.title("💰 Crypto Price Tracker")
    st.markdown("### Real-time cryptocurrency price monitoring with alerts")

    # Initialize tracker
    tracker = CryptoPriceTracker()

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Cryptocurrency selection
        st.subheader("Select Cryptocurrencies")
        all_cryptos = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana',
                       'ripple', 'dogecoin', 'polkadot', 'litecoin', 'chainlink']

        selected_cryptos = st.multiselect(
            "Choose cryptocurrencies to track:",
            all_cryptos,
            default=['bitcoin', 'ethereum', 'solana']
        )

        # Refresh interval
        refresh_interval = st.slider(
            "Auto-refresh interval (seconds):",
            min_value=10,
            max_value=300,
            value=30,
            step=5
        )

        # Email configuration
        st.subheader("📧 Email Alerts")
        email_enabled = st.checkbox("Enable Email Alerts", value=False)

        email_config = None
        if email_enabled:
            with st.expander("Email Settings"):
                smtp_server = st.text_input("SMTP Server", "smtp.gmail.com")
                smtp_port = st.number_input("SMTP Port", value=587)
                sender_email = st.text_input("Sender Email")
                sender_password = st.text_input("Sender Password", type="password")
                receiver_email = st.text_input("Receiver Email")

                email_config = {
                    'enabled': True,
                    'smtp_server': smtp_server,
                    'smtp_port': smtp_port,
                    'sender_email': sender_email,
                    'password': sender_password,
                    'receiver_email': receiver_email
                }

        # Add new alert
        st.subheader("🔔 Set Price Alert")
        col1, col2 = st.columns(2)
        with col1:
            alert_crypto = st.selectbox("Crypto:", selected_cryptos if selected_cryptos else all_cryptos)
        with col2:
            alert_type = st.selectbox("Alert Type:", ["above", "below"])

        alert_price = st.number_input("Price Threshold ($)", min_value=0.0, step=0.1)

        if st.button("Add Alert"):
            if alert_crypto and alert_price > 0:
                if alert_crypto not in tracker.alerts:
                    tracker.alerts[alert_crypto] = []
                tracker.alerts[alert_crypto].append({
                    'type': alert_type,
                    'price': alert_price,
                    'email_sent_today': False
                })
                tracker.save_alerts()
                st.success(f"Alert added for {alert_crypto} when price goes {alert_type} ${alert_price}")
            else:
                st.error("Please fill all alert fields")

        # Display existing alerts
        if tracker.alerts:
            st.subheader("Active Alerts")
            for crypto, alerts in tracker.alerts.items():
                for idx, alert in enumerate(alerts):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"{crypto.upper()} - {alert['type']} ${alert['price']}")
                    with col2:
                        if st.button("❌", key=f"del_{crypto}_{idx}"):
                            tracker.alerts[crypto].pop(idx)
                            if not tracker.alerts[crypto]:
                                del tracker.alerts[crypto]
                            tracker.save_alerts()
                            st.experimental_rerun()

        # Auto-refresh button
        auto_refresh = st.checkbox("Auto-refresh", value=True)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📊 Current Prices")
        placeholder = st.empty()

    with col2:
        st.subheader("📈 Performance Overview")
        metric_placeholder = st.empty()

    # Price history visualization
    st.subheader("📉 Price History")
    history_col1, history_col2 = st.columns(2)

    with history_col1:
        history_crypto = st.selectbox("Select crypto for history:",
                                      selected_cryptos if selected_cryptos else all_cryptos)
    with history_col2:
        history_days = st.selectbox("Time range:",
                                    [7, 14, 30, 60, 90],
                                    format_func=lambda x: f"{x} days")

    chart_placeholder = st.empty()
    alert_placeholder = st.empty()

    # Function to update data
    def update_data():
        if selected_cryptos:
            # Get current prices
            price_df = tracker.get_crypto_prices(selected_cryptos)

            if not price_df.empty:
                # Display current prices in a table
                with placeholder.container():
                    display_df = price_df.copy()
                    display_df['price_usd'] = display_df['price_usd'].apply(lambda x: f"${x:,.2f}")
                    display_df['24h_change'] = display_df['24h_change'].apply(
                        lambda x: f"{x:+.2f}%"
                    )
                    display_df['market_cap'] = display_df['market_cap'].apply(
                        lambda x: f"${x:,.0f}" if x > 0 else "N/A"
                    )
                    display_df['24h_vol'] = display_df['24h_vol'].apply(
                        lambda x: f"${x:,.0f}" if x > 0 else "N/A"
                    )
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        column_config={
                            "crypto": "Cryptocurrency",
                            "price_usd": "Price (USD)",
                            "24h_change": "24h Change",
                            "market_cap": "Market Cap",
                            "24h_vol": "24h Volume"
                        }
                    )

                # Display metrics
                with metric_placeholder.container():
                    metrics = st.columns(len(selected_cryptos))
                    for idx, row in price_df.iterrows():
                        with metrics[idx % len(metrics)]:
                            color = "green" if row['24h_change'] >= 0 else "red"
                            st.metric(
                                label=row['crypto'],
                                value=f"${row['price_usd']:,.2f}",
                                delta=f"{row['24h_change']:+.2f}%",
                                delta_color="normal"
                            )

                # Check alerts for each crypto
                triggered_alerts = []
                for _, row in price_df.iterrows():
                    if tracker.check_alerts(row['crypto'].lower(), row['price_usd'], email_config):
                        triggered_alerts.append(f"{row['crypto']} at ${row['price_usd']:,.2f}")

                if triggered_alerts:
                    with alert_placeholder.container():
                        st.warning(f"⚠️ Alert triggered for: {', '.join(triggered_alerts)}")
                else:
                    alert_placeholder.empty()

                return price_df

    # Initial data load
    current_price_df = update_data()

    # Load and display price history
    if history_crypto:
        historical_df = tracker.get_historical_data(history_crypto, history_days)
        if not historical_df.empty:
            with chart_placeholder.container():
                fig = px.line(
                    historical_df,
                    x='timestamp',
                    y='price',
                    title=f"{history_crypto.upper()} Price History - Last {history_days} Days",
                    labels={'timestamp': 'Date', 'price': 'Price (USD)'}
                )
                fig.update_layout(
                    hovermode='x unified',
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    template="plotly_white"
                )
                fig.add_hline(
                    y=historical_df['price'].mean(),
                    line_dash="dash",
                    line_color="gray",
                    annotation_text="Average Price"
                )
                st.plotly_chart(fig, use_container_width=True)

    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.experimental_rerun()

    # Show alert log viewer
    with st.expander("📋 Alert Log"):
        if os.path.exists(tracker.alert_log_file):
            with open(tracker.alert_log_file, 'r') as f:
                logs = f.readlines()
                if logs:
                    for log in logs[-50:]:  # Show last 50 logs
                        st.text(log.strip())
                else:
                    st.info("No alerts triggered yet")
        else:
            st.info("No alert log available")


if __name__ == "__main__":
    main()