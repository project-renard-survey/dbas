from nose.tools import assert_true, assert_is_not_none

from api_v2.graphql.tests.lib import graphql_query


def test_statements_with_textversions():
    query = """
        query { 
            statements { 
                uid
                textversions {
                    content
                }
            }
        }
    """
    content = graphql_query(query)
    assert_true(len(content.get("statements")) > 1)


def test_query_single_statement():
    query = """
        query { 
            statement (uid: 2) { 
                uid
                textversions {
                    content
                }
            }
        }
    """
    content = graphql_query(query)
    assert_is_not_none(content)
