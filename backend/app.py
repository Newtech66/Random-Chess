#!/usr/bin/env python

import asyncio
import json
import secrets

from websockets.asyncio.server import broadcast, serve
from randomchess import RandomChess, HumanPlayer

# TODO: Delete JOIN[join_key]
# TODO: Remove player 2 websocket connection

JOIN = {}

whitep = HumanPlayer('White')
blackp = HumanPlayer('Black')

async def error(websocket, message):
    """
    Send an error message.

    """
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

async def play(websocket, game, connected):
    """
    Receive and process moves from a player.

    """
    async for message in websocket:
        # Parse a "play" event from the UI.
        event = json.loads(message)
        assert event["type"] == "play"
        move_uci = event["move_uci"]

        # Play the move.
        game.play_move_uci(move_uci)

        # If game is over, send a "game_over" event.
        if game.is_game_over():
            outcome = game.end_game()
            player = "Draw"
            if outcome.winner:
                player = [blackp.name, whitep.name][outcome.winner]
            event = {
                "type": "game_over",
                "svg_board": game.svg_board(),
                "player": player,
                "termination": outcome.termination.name,
            }
            broadcast(connected, json.dumps(event))

        # Send a "play" event to update the UI.
        event = {
            "type": "play",
            "svg_board": str(game.svg_board()),
            "player": game.current_player().name,
            "move_list": [move.uci() for move in game.get_moves()],
        }
        broadcast(connected, json.dumps(event))

async def begin_game(game, connected):
    async for websocket in connected:
        await play(websocket, game, connected)

async def host(websocket):
    """
    Handle a connection from the first player: start a new game and wait for player 2 to join.

    """
    # Initialize a Connect Four game, the set of WebSocket connections
    # receiving moves from this game, and secret access tokens.
    game = RandomChess()
    game.add_white(whitep)
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    # Send the secret access tokens to the browser of the first player,
    # where they'll be used for building "join" and "watch" links.
    event = {
        "type": "host",
        "key": join_key,
    }
    print(f'Assigned key {join_key}')
    await websocket.send(json.dumps(event))

    # # So like, after the key has been sent, we need to wait until another player joins
    # message = await websocket.recv()
    # event = json.loads(message)
    # print(event)
    # assert event["event"] == "init"
    # ctype = event["type"]



async def join(websocket, join_key):
    """
    Handle a connection from the second player: join an existing game.

    """
    # Find the Random Chess game.
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    # Register to receive moves from this game.
    game.add_black(blackp)
    game.init_game()
    connected.add(websocket)
    try:
        # Receive and process moves from the second player.
        event = {
            "type": "start",
        }
        await websocket.send(json.dumps(event))
        await begin_game(websocket, game, connected)
    finally:
        connected.remove(websocket)
        del JOIN[join_key]

async def handler(websocket):
    """
    Handle a connection and dispatch it according to who is connecting.

    """
    # Receive and parse the "init" event from the UI.
    message = await websocket.recv()
    event = json.loads(message)
    print(event)
    assert event["event"] == "init"
    ctype = event["type"]

    if ctype == "join":
        # Second player joins an existing game.
        await join(websocket, event["key"])
    elif ctype == "host":
        # First player starts a new game.
        print('Received connection request')
        await host(websocket)
    else:
        raise ValueError(f"Unexpected event type {ctype}")


async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())