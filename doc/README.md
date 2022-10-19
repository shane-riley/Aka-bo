# Aka-bo Docs

This folder contains diagrams and documentation outlining the structure of the Aka-bo Gameserver.

- `/api`
- `/pages`
- `/comm`

## Folders

### API

The `/api` folder contains a REST API specification made using Swagger.

### Pages

The `/pages` folder contains information on the page layout for the Aka-bo gameserver.

### Comm

The `/comm` folder contains PlantUML-generated communication diagrams that describe in greater detail the workflows that are encapsulated by the pages and the api. These diagrams describe workflows of interest:

1. User logs in, modifies user information, logs out
2. User logs in, selects game, attempts matchmaking, cancels matchmaking
3. User logs in, selects game, attempts matchmaking, stops polling
4. User logs in, selects game, attempts matchmaking, finds game, plays game to completion, logs out
5. User logs in, selects game, attempts matchmaking, finds game, forfeits
6. User logs in, selects game, attempts matchmaking, finds game, leaves

### Storage

The `/storage` folder outlines how user information, matchmaking tickets, and game states are stored

## Notes

The communication diagrams reveal a number of thoughts:

- How do we initiate action on a server without an API call (for handling timeouts)?
- What can Firebase do for forgotten passwords, user data, etc?
- How do we make move API calls game-agnostic?
