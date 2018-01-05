Feature: Moving a running job to the remote

Scenario: Packaging a queued job
    Given Job id 34567 is queued locally
    When I request it to be shuttled
    #Then It should be placed on hold
    #And a request should be placed to the server
