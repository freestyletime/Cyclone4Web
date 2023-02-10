import pytest
from pathlib import Path
from flask import Flask
from . import create_app
from .config import const


@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app):
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_entry(client):
    ''' 
    URL: / to /editor
    '''
    response = client.get('/', follow_redirects=True)
    # Check that there was one redirect response.
    assert len(response.history) == 2
    # Check that the second request was to the editor/index page.
    assert response.request.path == "/editor/"


def test_about(client):
    ''' 
    URL: /about
    '''
    response = client.get('/about')
    assert response.status_code == 200


def test_error_405(client):
    ''' 
    URL: /about
    '''
    response = client.post('/about')
    assert response.status_code == 200
    assert b"405 Error" in response.data


def test_error_404(client):
    ''' 
    URL: /mirror
    '''
    response = client.get('/mirror')
    assert response.status_code == 200
    assert b"404 Error" in response.data


def test_error_page(client):
    ''' 
    URL: /error
    '''
    response = client.get('/error', data={
        "code": 500,
        "des": "Internal Error"
    })
    assert response.status_code == 200


def test_runCode(client):
    ''' 
    URL: /editor/run
    '''
    response = client.post('/editor/run',
        data={
        "code": """graph G { 
                        abstract start node  S1 {} 
                        abstract node  S2 {} 
                        edge  t1 { S1 -> S1 } 
                        edge  t2 { S1 -> S2 } 
                        edge  t3 { S2 -> S1 } 
                        edge  t4 { S2 -> S2 } 
                        goal { 
                            check for 5 condition (!(S1->S1) && !(S2->S2)) reach (S2)
                        }
                    }""",
        "unique_user_id": "CYCLONE4WEB-USER-68597c1e-2731-4a22-affc-fcb5e7699111"
        })

    assert response.status_code == 200
    assert response.json["status"] == 0
    assert response.json["msg"] == const.SUCCESS_REQ


def test_send_trace_file(client):
    ''' 
    URL: /editor/file
    '''
    response = client.get('/editor/file?path=/Users/chenchristian/Development/PycharmProjects/Cyclone4Web/Cyclone/trace/G.trace',
        data={
            "unique_user_id": "CYCLONE4WEB-USER-68597c1e-2731-4a22-affc-fcb5e7699111"
        }
    )
    assert response.status_code == 200


def test_upload(client):
    ''' 
    URL: /editor/upload
    '''
    resources = Path(__file__).parent.parent / "tmp"
    response = client.post('/editor/upload',
        data={
            "unique_user_id": "CYCLONE4WEB-USER-68597c1e-2731-4a22-affc-fcb5e7699111",
            "file": ( resources / "Main.cyclone").open("rb")
        }
    )

    assert response.status_code == 200
    assert response.json["status"] == 0
    assert response.json["msg"] == const.SUCCESS_REQ_UPDATE


def test_downLoadFile(client):
    ''' 
    URL: /editor/save2LocalFile
    '''
    response = client.post('/editor/save2LocalFile',
        data={
            "unique_user_id": "CYCLONE4WEB-USER-68597c1e-2731-4a22-affc-fcb5e7699111",
            "code": """graph G { 
                        abstract start node  S1 {} 
                        abstract node  S2 {} 
                        edge  t1 { S1 -> S1 } 
                        edge  t2 { S1 -> S2 } 
                        edge  t3 { S2 -> S1 } 
                        edge  t4 { S2 -> S2 } 
                        goal { 
                            check for 5 condition (!(S1->S1) && !(S2->S2)) reach (S2)
                        }
                    }""",
            
        }
    )
    assert response.status_code == 200


def test_getExamplesList(client):
    ''' 
    URL: /editor/examples
    '''
    response = client.post('/editor/examples',
        data={
            "unique_user_id": "CYCLONE4WEB-USER-68597c1e-2731-4a22-affc-fcb5e7699111"
        }
    )

    assert response.status_code == 200
    assert response.json["status"] == 0
    assert response.json["msg"] == const.SUCCESS_REQ


def test_getExample(client):
    ''' 
    URL: /editor/example
    '''
    response = client.post('/editor/example',
        data={
            "unique_user_id": "CYCLONE4WEB-USER-68597c1e-2731-4a22-affc-fcb5e7699111",
            "file": "example6.cyclone",
            "folder": "chapter1"
        }
    )

    assert response.status_code == 200
    assert response.json["status"] == 0
    assert response.json["msg"] == const.SUCCESS_REQ