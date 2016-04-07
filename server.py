# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import json
import uuid

from cassandra.cluster import Cluster

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

home_directory = "."
# home_directory="/home/pasukhov/site"


def parse_panda(str):
    p = str.split(':')
    return {"name": p[0], "lon": p[1], "lat": p[2], "comment": p[3]}


class DatabaseHandler(tornado.web.RequestHandler):
    cluster = Cluster(['localhost'])

    def get(self):
        self.add_header("Access-Control-Allow-Origin", "*")

        session = self.cluster.connect('hugs')
        hugs = session.execute("SELECT * FROM hugs")

        jhugs = [i.__dict__ for i in hugs]
        for i in jhugs:
            del i["id"]

        self.write(json.dumps(jhugs, separators=(',', ':'), encoding='utf-8'))

    def post(self):
        id = uuid.uuid1()
        obj = json.loads(self.request.body, encoding='utf-8')
        session = self.cluster.connect('hugs')
        hugs = session.execute(
            """insert into hugs
                (id, name, lon, lat, comment)
                values(%s, %s, %s, %s,%s)
            """,
            (id, obj["name"], float(obj["lon"]), float(obj["lat"]), obj["comment"])
        )
        self.write(str(id))
        self.set_status(201)


class DatabaseObjectHandler(tornado.web.RequestHandler):
    cluster = Cluster(['localhost'])

    def get(self, id):
        self.add_header("Access-Control-Allow-Origin", "*")
        uid = uuid.UUID(id)

        session = self.cluster.connect('hugs')
        hugs = session.execute("SELECT * FROM hugs where id = %s", (uid, ))

        if (len(hugs.current_rows) == 0):
            self.write("{}")
            return

        jhug = hugs.current_rows[0].__dict__
        jhug["id"] = str(jhug["id"])

        self.write(json.dumps(jhug, separators=(',', ':'), encoding='utf-8'))

    def delete(self, id):
        self.add_header("Access-Control-Allow-Origin", "*")
        uid = uuid.UUID(id)

        session = self.cluster.connect('hugs')
        session.execute("DELETE FROM hugs where id = %s", (uid, ))

        self.write(str(id))
        self.set_status(200)


def make_app():
    return tornado.web.Application([
        (r"/hugs/panda/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", DatabaseObjectHandler),
        (r"/hugs/panda", DatabaseHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8733)
    tornado.ioloop.IOLoop.current().start()