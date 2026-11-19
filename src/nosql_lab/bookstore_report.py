
#!/usr/bin/env python3
"""Generate a bookstore inventory report from MongoDB Atlas."""

import logging
import os

from pymongo import MongoClient

# Read credentials from the environment, never from source code.
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    """Connect to MongoDB and print books grouped by author."""
    client = None

    try:
        if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
            raise ValueError("Missing MongoDB environment variables.")

        # Connect using the Atlas URL and credentials.
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=10000,
        )

        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas")

        database = client["bookstore"]
        authors = database["authors"]
        books = database["books"]

        # Include original authors and one newly added author.
        author_ids = ["author_002", "author_003", "author_004"]

        total = authors.count_documents({"_id": {"$in": author_ids}})
        print(f"\nAuthors: {total}")

        for author in authors.find({"_id": {"$in": author_ids}}).sort("_id", 1):
            print(f"\n{author['name']}")

            # Find books referencing this author's ID.
            for book in books.find({"author_ids": author["_id"]}):
                print(f"  {book['title']} ({book['published_year']})")

    except Exception:
        logging.exception("Could not generate bookstore report")

    finally:
        if client is not None:
            client.close()
            logging.info("MongoDB connection closed")


if __name__ == "__main__":
    main()
