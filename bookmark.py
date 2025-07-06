import csv
import os
from jinja2 import Environment, FileSystemLoader


def create_chrome_bookmarks(csv_file, template_file, output_file):
    """
    Creates a Chrome bookmarks HTML file using Jinja2 templating.

    Args:
      csv_file: Path to the CSV file with 'path' and 'name' columns.
      template_file: Path to the Jinja2 template file.
      output_file: Path to the output HTML file.
    """

    # Load the Jinja2 template
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_file)))
    template = env.get_template(os.path.basename(template_file))

    # Process the CSV data
    bookmarks = {}
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            path = row[0].strip("/").split("/")
            name = row[1]
            title = row[2]
            url = f"{name}"
            current_level = bookmarks
            for folder in path:
                current_level = current_level.setdefault(folder, {})
            # Use a list to store multiple bookmarks at the same path
            if "bookmarks" not in current_level:
                current_level["bookmarks"] = []
            current_level["Bookmarks Bar"].append({"name": name, "url": url, "title": title})

    # Render the template
    with open(output_file, "w") as f:
        f.write(template.render(bookmarks=bookmarks))
if __name__ == "__main__":
    csv_file = "input.csv"
    template_file = "bookmarks_template.html"  # Replace with your template file
    output_file = "bookmarks.html"
    create_chrome_bookmarks(csv_file, template_file, output_file)
    print(f"Bookmarks HTML file created: {output_file}")
