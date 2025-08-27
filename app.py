from data_loader import load_data
from kpi import compute_kpis
from dashboard import dashboard

def main():
    df = load_data()
    df = compute_kpis(df)
    dashboard(df)

if __name__ == "__main__":
    main()
