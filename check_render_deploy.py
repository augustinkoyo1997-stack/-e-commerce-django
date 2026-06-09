import os

def check():
    print("\n🔍 Vérification déploiement Render\n")
    ok = True

    # Fichiers obligatoires
    for f in ["requirements.txt", "Procfile", "manage.py", "ecommerce/settings.py"]:
        if os.path.exists(f):
            print(f"✅ {f}")
        else:
            print(f"❌ {f} manquant")
            ok = False

    # Vérifier gunicorn dans requirements.txt
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as req:
            if "gunicorn" in req.read():
                print("✅ gunicorn dans requirements.txt")
            else:
                print("❌ gunicorn absent de requirements.txt")
                ok = False

    # Vérifier Procfile
    if os.path.exists("Procfile"):
        with open("Procfile", "r", encoding="utf-8") as pf:
            if "gunicorn ecommerce.wsgi" in pf.read():
                print("✅ Procfile correct")
            else:
                print("⚠️ Procfile ne contient pas 'gunicorn ecommerce.wsgi'")

    print("\n✅ Prêt pour Render !" if ok else "\n❌ Corrigez les erreurs ci-dessus.\n")

if __name__ == "__main__":
    check()