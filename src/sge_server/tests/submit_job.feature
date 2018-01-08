Feature: Receiving a submitted job

Scenario: Valid job is submitted
    When A new job is submitted
    Then The data should be extracted
