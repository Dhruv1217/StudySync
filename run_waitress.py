from waitress import serve
from app import app

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  🚀 Starting Waitress Production WSGI Server...")
    print("  🌐 Running at: http://0.0.0.0:8080")
    print("=" * 50 + "\n")
    serve(app, host='0.0.0.0', port=8080)
