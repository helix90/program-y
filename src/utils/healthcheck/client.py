"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import requests
import json
"""

import json

import requests
from flask import Flask, current_app, request

servers = {}

if __name__ == "__main__":

    print("Initiating Healthcheck App...")

    APP = Flask(__name__)

    @APP.route("/")
    def index():
        return current_app.send_static_file("healthcheck.html")

    # name=NAME, host=HOST, port=PORT
    @APP.route("/api/health/v1.0/register")
    def regiter():
        name = request.args.get("name")
        host = request.args.get("host")
        port = request.args.get("port")
        url = request.args.get("url")

        if name in servers:
            print("Re-register existing server [%s]" % name)
        else:
            print("Register server [%s]" % name)

        if url.startswith("/") is False:
            url = "/" + url

        servers[name] = "http://%s:%s%s" % (host, port, url)
        print(servers[name])

        return "OK"

    # name=NAME
    @APP.route("/api/health/v1.0/unregister")
    def unregiter():
        name = request.args.get("name")
        if name in servers:
            del servers[name]
            print("Unregistered server [%s]" % name)
        else:
            print("Unable to register server, unknown name [%s]" % name)
        return "OK"

    @APP.route("/api/health/v1.0/ping")
    def ping():
        healthchecks = get_health_check_from_servers(servers)
        return healthchecks_to_treedata(healthchecks)

    def healthchecks_to_treedata(healthchecks):
        treedata = {"source": []}

        if "pings" in healthchecks:
            healthcheck_pings = healthchecks["pings"]

            id = 1
            for healthcheck in healthcheck_pings:

                client = {"title": healthcheck["name"], "key": str(id)}
                id += 1

                bots = {"title": "Bots", "folder": True, "key": str(id), "children": []}
                id += 1

                logging = {
                    "title": "Logging",
                    "folder": True,
                    "key": str(id),
                    "children": [],
                }
                id += 1

                if "ping" in healthcheck:
                    ping = healthcheck["ping"]

                    if "logging" in ping:
                        logging["children"].append(
                            {
                                "title": "criticals: "
                                + str(ping["logging"]["criticals"]),
                                "key": str(id),
                            }
                        )
                        id += 1
                        logging["children"].append(
                            {
                                "title": "exceptions: "
                                + str(ping["logging"]["exceptions"]),
                                "key": str(id),
                            }
                        )
                        id += 1
                        logging["children"].append(
                            {
                                "title": "fatals: " + str(ping["logging"]["fatals"]),
                                "key": str(id),
                            }
                        )
                        id += 1
                        logging["children"].append(
                            {
                                "title": "errors: " + str(ping["logging"]["errors"]),
                                "key": str(id),
                            }
                        )
                        id += 1
                        logging["children"].append(
                            {
                                "title": "warnings: "
                                + str(ping["logging"]["warnings"]),
                                "key": str(id),
                            }
                        )
                        id += 1
                        logging["children"].append(
                            {
                                "title": "debugs: " + str(ping["logging"]["debugs"]),
                                "key": str(id),
                            }
                        )
                        id += 1
                        logging["children"].append(
                            {
                                "title": "infos: " + str(ping["logging"]["infos"]),
                                "key": str(id),
                            }
                        )
                        id += 1

                    type = {"title": "Type: " + ping["client"], "key": str(id)}
                    id += 1

                    questions = {
                        "title": "Questions: " + str(ping["questions"]),
                        "key": str(id),
                    }
                    id += 1

                    starttime = {
                        "title": "Start Time: " + ping["start_time"],
                        "key": str(id),
                    }
                    id += 1

                    if "bots" in ping:
                        for bot in ping["bots"]:
                            abot = {
                                "title": bot["id"],
                                "folder": True,
                                "key": str(id),
                                "children": [],
                            }
                            id += 1

                            abot["children"].append(
                                {
                                    "title": "Questions: " + str(bot["questions"]),
                                    "key": str(id),
                                }
                            )
                            id += 1

                            brains = {
                                "title": "Brains",
                                "folder": True,
                                "key": str(id),
                                "children": [],
                            }
                            id += 1

                            bots["children"].append(abot)
                            abot["children"].append(brains)

                            if "brains" in bot:
                                for brain in bot["brains"]:
                                    abrain = {
                                        "title": brain["id"],
                                        "folder": True,
                                        "key": str(id),
                                        "children": [],
                                    }
                                    id += 1
                                    brains["children"].append(abrain)
                                    abrain["children"].append(
                                        {
                                            "title": "Questions: "
                                            + str(brain["questions"]),
                                            "key": str(id),
                                        }
                                    )
                                    id += 1

                    client["children"] = [type, questions, starttime, bots, logging]

                treedata["source"].append(client)

        return json.dumps(treedata)

    # noinspection Pylint
    def get_health_check_from_serversX(servers):
        del servers

        data = {
            "pings": [
                {
                    "name": "webchat1",
                    "ping": {
                        "bots": [
                            {
                                "brains": [{"id": "brain", "questions": 0}],
                                "id": "bot",
                                "questions": 0,
                            }
                        ],
                        "client": "WebChat",
                        "logging": {
                            "criticals": 0,
                            "debugs": 8249,
                            "errors": 50,
                            "exceptions": 1,
                            "fatals": 0,
                            "infos": 842,
                            "warnings": 446,
                        },
                        "questions": 0,
                        "start_time": "2019-03-18 19:55:38.023020",
                    },
                },
                {
                    "name": "2brains",
                    "ping": {
                        "bots": [
                            {
                                "brains": [
                                    {"id": "brain1", "questions": 0},
                                    {"id": "brain2", "questions": 0},
                                ],
                                "id": "bot",
                                "questions": 0,
                            }
                        ],
                        "client": "WebChat",
                        "logging": {
                            "criticals": 0,
                            "debugs": 8249,
                            "errors": 50,
                            "exceptions": 1,
                            "fatals": 0,
                            "infos": 842,
                            "warnings": 446,
                        },
                        "questions": 0,
                        "start_time": "2019-03-18 19:55:38.023020",
                    },
                },
                {
                    "name": "2bots",
                    "ping": {
                        "bots": [
                            {
                                "brains": [{"id": "brain", "questions": 0}],
                                "id": "bot1",
                                "questions": 0,
                            },
                            {
                                "brains": [{"id": "brain", "questions": 0}],
                                "id": "bot2",
                                "questions": 0,
                            },
                        ],
                        "client": "WebChat",
                        "logging": {
                            "criticals": 0,
                            "debugs": 8249,
                            "errors": 50,
                            "exceptions": 1,
                            "fatals": 0,
                            "infos": 842,
                            "warnings": 446,
                        },
                        "questions": 0,
                        "start_time": "2019-03-18 19:55:38.023020",
                    },
                },
                {
                    "name": "2bots2brains",
                    "ping": {
                        "bots": [
                            {
                                "brains": [
                                    {"id": "brain1", "questions": 0},
                                    {"id": "brain2", "questions": 0},
                                ],
                                "id": "bot1",
                                "questions": 0,
                            },
                            {
                                "brains": [
                                    {"id": "brain1", "questions": 0},
                                    {"id": "brain2", "questions": 0},
                                ],
                                "id": "bot2",
                                "questions": 0,
                            },
                        ],
                        "client": "WebChat",
                        "logging": {
                            "criticals": 0,
                            "debugs": 8249,
                            "errors": 50,
                            "exceptions": 1,
                            "fatals": 0,
                            "infos": 842,
                            "warnings": 446,
                        },
                        "questions": 0,
                        "start_time": "2019-03-18 19:55:38.023020",
                    },
                },
            ]
        }

        return data

    def get_health_check_from_servers(servers):
        result = {"pings": []}

        for name, url in servers.items():
            healthcheck = {"name": name}
            ping = requests.get(url)
            healthcheck["ping"] = ping.json()
            result["pings"].append(healthcheck)

        return result

    APP.run()
