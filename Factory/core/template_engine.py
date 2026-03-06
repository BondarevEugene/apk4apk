import json


def create_book_template(path):

    template = {

        "app": {
            "name": "NewBook",
            "version": "1.0"
        },

        "pages": [

            {
                "id": "page1",

                "layout": "column",

                "blocks": [

                    {
                        "type": "text",
                        "value": "Welcome to the book"
                    }

                ]
            }

        ]
    }

    with open(path, "w", encoding="utf8") as f:

        json.dump(template, f, indent=4)