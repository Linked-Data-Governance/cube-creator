from SPARQLWrapper import SPARQLWrapper2, JSON
from rdflib import Graph, URIRef, Literal

SPARQL_ENDPOINT = "https://test.lindas.admin.ch/query"
NAMED_GRAPH = "https://lindas.admin.ch/fatc/cube"
DATASET_URI = "https://education.ld.admin.ch/fatc/ch_degree_obsan_analysis"
file_path = "./lindas_graph.ttl"


def download_graph():
    dataset_uri_obj = URIRef(DATASET_URI)
    g = Graph()

    # Bind the namespaces for better readability
    g.bind("schema", "http://schema.org/", override=True)
    g.bind("cube", "https://cube.link/")
    g.bind("obsan", DATASET_URI + "/")

    sparql = SPARQLWrapper2(SPARQL_ENDPOINT)
    sparql.setReturnFormat(JSON)

    # The follwing request retrieves the metadata of the dataset
    sparql.setQuery(f"""
        PREFIX schema: <http://schema.org/>
        SELECT ?p ?o
        FROM <{NAMED_GRAPH}>
        WHERE {{
            <{DATASET_URI}> schema:hasPart ?cube .
            ?cube schema:version 1 ;
                    ?p ?o.
        }}
    """)

    print(sparql.queryString)

    results = sparql.query().bindings

    for r in results:
        if r['o'].value.startswith("http"):
            g.add((dataset_uri_obj, URIRef(
                r['p'].value), URIRef(r['o'].value)))
        else:
            g.add((dataset_uri_obj, URIRef(
                r['p'].value), Literal(r['o'].value)))

    # The following request retrieves the observations

    sparql.setQuery(f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX cube: <https://cube.link/>
        PREFIX schema: <http://schema.org/>

        SELECT ?obs ?obs_p ?obs_o

        FROM <{NAMED_GRAPH}>
        WHERE {{

            <{DATASET_URI}> schema:hasPart ?cube .
            ?cube schema:version 1 ; cube:observationSet ?obSet .
                ?obSet rdf:type cube:ObservationSet ; 
                cube:observation ?obs .
                ?obs ?obs_p ?obs_o .
        }}
    """)

    print(sparql.queryString)

    results = sparql.query().bindings
    for r in results:
        if r['obs_o'].value.startswith("http"):
            g.add((URIRef(r['obs'].value), URIRef(
                r['obs_p'].value), URIRef(r['obs_o'].value)))
        else:
            g.add((URIRef(r['obs'].value), URIRef(
                r['obs_p'].value), Literal(r['obs_o'].value)))

    g.serialize(destination=file_path, format='turtle', encoding='utf-8')


if __name__ == "__main__":
    download_graph()
    print(f"Graph downloaded to {file_path}")
