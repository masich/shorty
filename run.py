import argparse

from shorty.app import create_app

app = create_app()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Shorty service.')
    parser.add_argument('--port', type=int, action='store', default=app.config['DEFAULT_PORT'])
    parser.add_argument('--host', type=str, action='store', default=app.config['DEFAULT_HOST'])
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
