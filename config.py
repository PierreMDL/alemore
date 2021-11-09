DEBUG = False

STATIC_FOLDER = "app/static"
IMAGES_FOLDER = "app/static/images"
IMAGES_SRC = "/static/images"

SQLALCHEMY_DATABASE_URI = "sqlite:///alemore.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
MAX_CONTENT_SIZE = (1100, 1100)  # hauteur, largeur
ALLOWED_EXTENSIONS = {"jpg", "jpeg"}
