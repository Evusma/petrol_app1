# ⛽ Diesel Price Dashboard

Time series dashboard to track the evolution of diesel prices at selected gas stations, with a fuel cost calculator to compare prices against the cheapest station in the list.

## 📖 About

This is a **personalized application** built to help me make quicker decisions, save time, and potentially reduce fuel expenses. It tracks diesel price evolution at gas stations near my home, using publicly available data.

## 👥 Intended Audience

This project was built as a personal tool, but it's also part of my **portfolio** — so it's meant for:

- **🔍 Data enthusiasts** — curious about a real-world, end-to-end mini data pipeline (API → DB → Dashboard).
- **💻 Dev community** — interested in seeing a practical Streamlit + PostgreSQL implementation.
- **🌱 Mentor developers** — This project is part of my learning journey. There are likely improvements to be made — feedback is always welcome, and I see this as a living project, not a finished product.

## ✨ Features

The app is a **Streamlit** application with three pages:

- **📈 Time-Series Dashboard** — Visualize diesel price trends over time for selected gas stations.
- **💰 Fuel Cost Calculator** — Choose a station and compare it against the cheapest one in the list to see how much you could save.
- **ℹ️ About** — Explanation of the dashboard, data source, and a contact form to send messages.

## 🏗️ Tech Stack

- **Frontend/App**: [Streamlit](https://streamlit.io/)
- **Visualization**: [Plotly](https://plotly.com/python/)
- **Data manipulation**: [Pandas](https://pandas.pydata.org/)
- **Database driver**: [psycopg](https://www.psycopg.org/)
- **HTTP requests**: [requests](https://requests.readthedocs.io/)
- **Environment management**: [python-dotenv](https://pypi.org/project/python-dotenv/)
- **Database**: PostgreSQL (cloud-managed)

## 🔄 Data Pipeline

Data is sourced from the public [data.gouv.fr](https://https://www.data.gouv.fr/datasets/prix-des-carburants-en-france-flux-instantane-v2-amelioree) datagouv fuel prices API, which updates every 10 minutes. However, this app refreshes its own database **once a day**.

The pipeline works as follows:

1. A **GitHub Action** runs on a daily schedule (cron job).
2. It executes [`scripts/update_db.py`](scripts/update_db.py).
3. This script calls the data.gouv.fr API and stores the retrieved data in the PostgreSQL database.
4. The Streamlit app reads from this database to render the dashboard.

```
data.gouv.fr API → update_db.py (GitHub Action, daily) → PostgreSQL → Streamlit App
```

## ⚙️ Configuration

By default, the dashboard tracks gas stations **near my home**. However, the app is easily customizable: simply edit the tuple of station IDs inside [`config.py`](config.py) to track whichever stations you're interested in.

```python
# config.py (example)
STATION_IDS = (
    "12345678",  # Station name/location
    "87654321",
    # add or remove station IDs as needed
)
```

## 📁 Project Structure

> ⚠️ *Placeholder — to be finalized.*

```
diesel-dashboard/
├── .devcontainer/
├── .github/
├── src/
│   └── streamlit_app/
│       ├── app.py
│       ├── pages/
│       │   ├── calculator.py
│       │   ├── dashboard.py
│       │   └── details.py
│       ├── config/
│       │   └── config.py
│       └── services/
│           └── database.py
├── scripts/
│   ├── update_db.py
│   └── contact_info.py
├── config.py
├── pyproject.toml
├── .env
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Access to a PostgreSQL database

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd diesel-dashboard

# Install the package and dependencies
pip install -e .
```

### Environment Variables

Create a `.env` file in the project root with the following variable:

```env
DB_URL=postgresql://user:password@host:port/dbname
```

⚠️ **Never commit your `.env` file!** Make sure it's listed in `.gitignore`.

### Running the App

```bash
streamlit run src/streamlit_app/app.py
```

## 🌐 Deployment

This app is deployed on **[Streamlit Community Cloud](https://petrol-price-dashboard.streamlit.app/)**.

## 📬 Contact

Have feedback or questions? Use the contact form on the **About** page of the app — your message will be stored directly in the database.     

## 📄 License

This is a personal project, built for individual use.