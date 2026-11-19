db = db.getSiblingDB("bookstore");

// Load original authors and books
db.authors.drop();
const authors = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(authors);

db.books.drop();
const books = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(books);

// Add two new books
db.books.insertMany([
  {
    title: "1984",
    published_year: 1949,
    author_ids: ["author_004"]
  },
  {
    title: "The Hobbit",
    published_year: 1937,
    author_ids: ["author_005"]
  }
]);

// Step 5: List all original authors and books
print("Original authors:");
printjson(db.authors.find().toArray());

print("Original books:");
printjson(db.books.find().toArray());

// Add two new authors
db.authors.insertMany([
  {
    _id: "author_004",
    name: "George Orwell",
    bio: {
      short: "English novelist and essayist.",
      long: "George Orwell was an English writer known for 1984 and Animal Farm."
    }
  },
  {
    _id: "author_005",
    name: "J. R. R. Tolkien",
    nationality: "British",
    bio: {
      short: "English author and scholar.",
      long: "J. R. R. Tolkien was an English writer known for The Hobbit and The Lord of the Rings."
    }
  }
]);

// Find books by selected authors
print("Books by selected authors:");
printjson(
  db.books.find({
    author_ids: {
      $in: ["author_001", "author_004", "author_005"]
    }
  }).toArray()
);

// Verify final counts
print("Authors:", db.authors.countDocuments({}));
print("Books:", db.books.countDocuments({}));
