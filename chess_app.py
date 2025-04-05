#!/usr/bin/env python

import asyncio
import json

from websockets.asyncio.server import serve
from randomchess import RandomChess, HumanPlayer

whitep = HumanPlayer('White')
blackp = HumanPlayer('Black')

async def handler(websocket):
    # Initialize a Connect Four game.
    print('Starting server')
    game = RandomChess(whitep, blackp)
    event = {
        "type": "play",
        "svg_board": str(game.svg_board()),
        "player": game.current_player().name,
        "move_list": [move.uci() for move in game.get_moves()],
    }
    await websocket.send(json.dumps(event))

    # Players take alternate turns, using the same browser.
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
            await websocket.send(json.dumps(event))

        # Send a "play" event to update the UI.
        event = {
            "type": "play",
            "svg_board": str(game.svg_board()),
            "player": game.current_player().name,
            "move_list": [move.uci() for move in game.get_moves()],
        }
        await websocket.send(json.dumps(event))


async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())