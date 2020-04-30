"""Starts a local development server for uweb3 info."""

# Application
import ublog


def main():
  app = ublog.main()
  app.serve()


if __name__ == '__main__':
  main()
