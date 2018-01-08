
def test_root(client):
    # print(help(client.get("/")))
    response = client.get("/").json
    assert response['application'] == "Remote SGE"

def test_post_basic_job(client):
    response = client.post("/jobs.json")