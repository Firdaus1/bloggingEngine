from init import app, db

import views, views_auth, api

if __name__ == '__main__':
    app.run(debug=True)

