import sys

from anytree import Node, RenderTree
from anytree.exporter import DotExporter

from scrape import scrape


# Initialize global variables
person_count = {}
issues = []


def getParents(url, node):
    # Collect parent information
    person, parent_urls = scrape.website(url)
    
    try:
        # Build parent node and attach to child's node
        new_node = Node(f"{person['Name']}\n{url}", node)
        person_count[person["Name"]] = person_count.get(person["Name"], 0) + 1
        print(f"{person_count[person['Name']]} | Number of parents: {len(parent_urls)}, person: {person['Name']}, links: {parent_urls}")

        # Recursion
        for parent_url in parent_urls:
            getParents(parent_url, new_node)
    except:
        print("Oops! Something happened....")

        # Count number of issues...
        person_count["ISSUE"] = person_count.get("ISSUE", 0) + 1
        issues.append(url)


def app(url):
    # Build root node
    person, parent_urls = scrape.website(url)
    root = Node(person["Name"])

    # Find root node's parents
    for parent_url in parent_urls:
        getParents(parent_url, root)
    
    # Visualize results
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))
    DotExporter(root).to_picture("root.png")

    # Summarize execution issues
    if (len(issues) > 0):
        print(f"{person_count['ISSUE']} issue(s) encountered during the execution. These were found at:")
        for issue in issues:
            print(f" - {issue}")


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Incorrect number of launch arguments, stopping execution...")
        sys.exit(-1)
    elif ("www.geni.com" not in sys.argv[1]):
        print("Invalid URL, please provide a working www.geni.com URL...")
        sys.exit(-1)
    
    # Trigger application on input argument
    app(sys.argv[1])
