import bottle
import funkcije

bottle.debug(True)

@bottle.route('/')
@bottle.view('homepage')
def homepage():
    return "zivjo!"

bottle.run(host='localhost', port=8080)
