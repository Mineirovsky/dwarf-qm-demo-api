from app.initializers import *

app = create_app()

initialize_container(app)
initialize_routers(app)
