# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import json

home_directory="."
#home_directory="/home/pasukhov/site"


def parse_panda(str):
    p = str.split(':')
    return {"name" : p[0], "lon" : p[1], "lat" : p[2], "comment" : p[3]}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        f = open(home_directory + "/names.dat", "r")
        self.add_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps([parse_panda(i) for i in f],
                              separators=(',', ':'), encoding='utf-8'))
    def post(self):
        print "Body"
        print self.request.body
        obj = json.loads(self.request.body, encoding='utf-8')
        f = open("./names.dat", "a")
        f.write("\n"
                + obj["name"] + ":"
                + obj["lon"] + ":"
                + obj["lat"] + ":"
                + obj["comment"])
        f.close()
        self.write("Id will be here")
        self.set_status(201)

def make_app():
    return tornado.web.Application([
        (r"/hugs/panda", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8733)
    tornado.ioloop.IOLoop.current().start()