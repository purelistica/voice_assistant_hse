Feature: Save particular place
  Assistant saves certain location point from user and assigns a name

  Scenario: User asks to save current point and VA saves it with name and location
    Given service is working
    And location list is empty
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says "Save my location"
    Then VA names location
    When VA asks for confirmation
    And User confirms
    Then VA asks to set a name
    When User says Библиотека
    Then VA saves location
    And VA says "Done"

  Scenario: User asks to save current point, but VA determines incorrect location
    Given service is working
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says "Save my location"
    Then VA names location
    When VA asks for confirmation
    And User does not confirm
    Then VA says "Cancelled"

  Scenario: User asks to save current point, but the point with this name already exists
    Given service is working
    And location Библиотека exists in saved list
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says "Save my location"
    Then VA names location
    When VA asks for confirmation
    And User confirms
    Then VA asks to set a name
    When User says Библиотека
    Then VA says "Location already exists"

  Scenario: User asks to save current location and VA cannot determine location
    Given service is working
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says "Save my location"
    Then VA says 'Can't determine location'

  Scenario: User asks to save current location and VA cannot determine name
    Given service is working
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says "Save my location"
    Then VA names location
    When VA asks for confirmation
    And User confirms
    Then VA asks to set a name
    When User says nothing
    Then VA says 'Can't recognize name'

  Scenario: User asks to save location by address
    Given service is working
    When user says "Hello, Borya"
    Then VA says "Hello"
    When user says "Save location"
    Then VA asks "What is the address?"
    When user says address "Парусная улица дом 17"
    Then VA names location
    When VA asks for confirmation
    And User confirms
    Then VA asks to set a name
    When User says Пашин дом
    Then VA saves location
    And VA says "Done"