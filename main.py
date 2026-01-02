# Main script to run the application

#from ui.enhanced_client import run_enhanced_cli

#if __name__ == "__main__":
    # Use the enhanced CLI with multi-question support
 #   run_enhanced_cli()

import sys
import os
import subprocess
from ui.enhanced_client import run_enhanced_cli


def run_gui():
    """Lansează interfața grafică Streamlit într-un sub-proces."""
    # Construim calea absolută către gui_app.py pentru a evita erori de path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    gui_path = os.path.join(current_dir, 'ui', 'gui_app.py')

    print(f"🚀 Se lansează interfața grafică din: {gui_path}")
    print("Apasă Ctrl+C în terminal pentru a opri serverul.")

    # Rulăm comanda: python -m streamlit run ui/gui_app.py
    # Folosim sys.executable pentru a fi siguri că folosim același Python (același venv)
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", gui_path])
    except KeyboardInterrupt:
        print("\nOpritor server...")


if __name__ == "__main__":
    print("\n" + "=" * 40)
    print("      SmarTest - MAIN MENU")
    print("=" * 40)
    print("1. Interfață Grafică (Recomandat)")
    print("2. Interfață Linie de Comandă (CLI)")
    print("=" * 40)

    choice = input("\nAlege o opțiune (1 sau 2): ").strip()

    if choice == "1":
        run_gui()
    elif choice == "2":
        run_enhanced_cli()
    else:
        print("Opțiune invalidă. Se pornește CLI implicit.")
        run_enhanced_cli()