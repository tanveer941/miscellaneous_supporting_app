


# import py2neo
#
# from py2neo import Graph, Path, authenticate
# authenticate("localhost:7474", "tanveer", "tan_neo4j")
#
#
#
# graph = Graph("http://localhost:7474/")
#
# tx = graph.cypher.begin()
# for name in ["Alice", "Bob", "Carol"]:
#     tx.append("CREATE (person:Person {name:{name}}) RETURN person", name=name)
# alice, bob, carol = [result.one for result in tx.commit()]
#
# friends = Path(alice, "KNOWS", bob, "KNOWS", carol)
# graph.create(friends)


#=============================================================================
#
# You are connected as user neo4j
# to the server bolt://localhost:7687



from neo4j.v1 import GraphDatabase

class HelloWorldExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        print "self._driver :: ", self._driver

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        print "tx :: ", tx
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        print "result :: ", result
        return result.single()[0]

if __name__ == '__main__':
    hello_obj = HelloWorldExample("bolt://localhost:7687", "neo4j", "tan_neo4j")
    print "hello_obj :: ", hello_obj
    hello_obj.print_greeting("Add greeting data")
    hello_obj.close()
